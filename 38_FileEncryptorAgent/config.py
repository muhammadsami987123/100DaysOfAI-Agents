import os


APP_NAME = "FileEncryptorAgent"

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENCRYPTED_DIR = os.path.join(BASE_DIR, "encrypted")
DECRYPTED_DIR = os.path.join(BASE_DIR, "decrypted")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# Crypto settings
PBKDF2_ITERATIONS = 300_000
SALT_BYTES = 16
IV_BYTES = 12
KEY_BYTES = 32  # AES-256
TAG_BYTES = 16

# File format
MAGIC = b"FENC"
VERSION = 1

# I/O streaming
CHUNK_SIZE = 1024 * 1024  # 1 MiB

# Logging
ENABLE_JSONL_LOG = True
LOG_FILE = os.path.join(LOGS_DIR, "operations.jsonl")


def ensure_directories() -> None:
    os.makedirs(ENCRYPTED_DIR, exist_ok=True)
    os.makedirs(DECRYPTED_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)


