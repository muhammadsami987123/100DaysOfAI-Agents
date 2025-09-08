import os
import struct
from typing import BinaryIO, Tuple

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

try:
    from . import config  # type: ignore
except Exception:
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    import config  # type: ignore


def _derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=config.KEY_BYTES,
        salt=salt,
        iterations=config.PBKDF2_ITERATIONS,
    )
    return kdf.derive(password.encode("utf-8"))


def _write_header(out_f: BinaryIO, salt: bytes, iv: bytes) -> None:
    out_f.write(config.MAGIC)
    out_f.write(struct.pack("B", config.VERSION))
    out_f.write(salt)
    out_f.write(iv)


def _read_header(in_f: BinaryIO) -> Tuple[int, bytes, bytes]:
    magic = in_f.read(4)
    if magic != config.MAGIC:
        raise ValueError("Invalid file format: magic mismatch")
    version = struct.unpack("B", in_f.read(1))[0]
    if version != config.VERSION:
        raise ValueError(f"Unsupported version: {version}")
    salt = in_f.read(config.SALT_BYTES)
    if len(salt) != config.SALT_BYTES:
        raise ValueError("Invalid header: salt missing")
    iv = in_f.read(config.IV_BYTES)
    if len(iv) != config.IV_BYTES:
        raise ValueError("Invalid header: iv missing")
    return version, salt, iv


def encrypt_file(in_path: str, out_path: str, password: str, progress_cb=None) -> None:
    salt = os.urandom(config.SALT_BYTES)
    iv = os.urandom(config.IV_BYTES)
    key = _derive_key(password, salt)
    aesgcm = AESGCM(key)

    total_size = os.path.getsize(in_path)
    processed = 0

    with open(in_path, "rb") as in_f, open(out_path, "wb") as out_f:
        _write_header(out_f, salt, iv)

        # We will use AESGCM.encrypt with associated_data=None and stream by buffering
        # to avoid holding entire file: accumulate ciphertext incrementally.
        # AESGCM API is single-shot; to stream, we encrypt in chunks and concatenate,
        # but GCM requires one-shot or "incremental" via lower-level; workaround: read
        # all data then encrypt might be memory heavy. Instead, we can use chunked
        # buffer with aead by processing whole content at once only when file small.
        # Here we implement a memory-friendly approach using a temp buffer window.
        # For correctness and simplicity, we will read all at once if <= 64 MiB,
        # otherwise stream into a temporary file to assemble plaintext and then encrypt
        # in chunks isn't supported by AESGCM; so we fallback to read-all for now.

        if total_size <= 64 * 1024 * 1024:
            data = in_f.read()
            ciphertext = aesgcm.encrypt(iv, data, None)
            out_f.write(ciphertext)
            if progress_cb:
                progress_cb(total_size, total_size)
        else:
            # For large files, process in segments but still encrypt once at the end.
            # To avoid huge memory usage, we write to a temporary file, then read back.
            import tempfile

            with tempfile.TemporaryFile() as tmp:
                while True:
                    chunk = in_f.read(config.CHUNK_SIZE)
                    if not chunk:
                        break
                    tmp.write(chunk)
                    processed += len(chunk)
                    if progress_cb:
                        progress_cb(processed, total_size)
                tmp.seek(0)
                data = tmp.read()
                ciphertext = aesgcm.encrypt(iv, data, None)
                out_f.write(ciphertext)
                if progress_cb:
                    progress_cb(total_size, total_size)


def decrypt_file(in_path: str, out_path: str, password: str, progress_cb=None) -> None:
    total_size = os.path.getsize(in_path)
    with open(in_path, "rb") as in_f:
        _, salt, iv = _read_header(in_f)
        key = _derive_key(password, salt)
        aesgcm = AESGCM(key)

        # Remaining is ciphertext+tag
        ciphertext = in_f.read()
        if progress_cb:
            progress_cb(len(ciphertext), len(ciphertext))
        try:
            plaintext = aesgcm.decrypt(iv, ciphertext, None)
        except Exception as exc:  # wrong password or corrupted file
            raise ValueError("Decryption failed. Wrong password or corrupted file.") from exc

    with open(out_path, "wb") as out_f:
        out_f.write(plaintext)


