# 🔐 FileEncryptorAgent - Day 38 of #100DaysOfAI-Agents

<div align="center">

![FileEncryptorAgent Banner](https://img.shields.io/badge/FileEncryptorAgent-Day%2038-blue?style=for-the-badge&logo=lock&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8%2B-green?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20UI-red?style=for-the-badge&logo=flask&logoColor=white)

**Local‑first file encryption and decryption with AES‑256 (GCM)**

[🚀 Quick Start](#-quick-start) • [🧩 Features](#-features) • [🔒 Security](#-security) • [🧪 Troubleshooting](#-troubleshooting) • [📄 License](#-license)

</div>

---

## ✨ What is FileEncryptorAgent?

FileEncryptorAgent securely encrypts and decrypts files on your machine using password‑based encryption. It never sends data to external services and uses modern, authenticated cryptography.

### 🌟 Highlights

- **AES‑256 GCM** with PBKDF2‑HMAC‑SHA256 key derivation
- **Per‑file random salt & IV** for strong security
- **Beautiful Web UI (Flask + Tailwind)** for ease of use
- **Large file support** with progress feedback
- **Safe outputs** to `encrypted/` and `decrypted/`
- **Optional JSONL logs** in `logs/operations.jsonl`

## 🧩 Features

### 🚀 Core Functionality

- ✅ Encrypt any file to `encrypted/<name>.<ext>.enc`
- ✅ Decrypt `.enc` files to `decrypted/<name>.<ext>`
- ✅ Integrity protection: wrong passwords trigger errors
- ✅ Auto‑create folders and optional logging

### 💻 Web Interface

- ✅ Drag‑and‑drop upload areas
- ✅ Clear success/error messages and helpful tips
- ✅ Download links for encrypted/decrypted outputs

## 🚀 Quick Start

### 📋 Prerequisites

- Python 3.8+
- Windows PowerShell or any terminal

### ⚡ One‑Click Installation

```bash
# Windows - from inside the project folder
install.bat
```

### 🔧 Manual Installation

```bash
cd 38_FileEncryptorAgent
pip install -r requirements.txt
```

### ▶️ First Run (Web UI)

```bash
python web_server.py
# or
start_web.bat
```

Open: http://127.0.0.1:5005

### 📂 Output Locations

- Encrypted files → `38_FileEncryptorAgent/encrypted/`
- Decrypted files → `38_FileEncryptorAgent/decrypted/`
- Optional logs (JSONL) → `38_FileEncryptorAgent/logs/operations.jsonl`

### 🧭 How to Use

1) In the Encrypt card: choose or drop a file, enter password and confirm, then Encrypt

2) In the Decrypt card: choose or drop a `.enc` file, enter password, then Decrypt

3) Download the resulting file or open the output folders

### 🖼️ Screenshots (Optional)

Add images here to showcase the UI (use local paths or links):

- Web Home: `templates/index.html`
- Encrypt success message
- Decrypt success message

## 🔒 Security

- Key derivation: **PBKDF2‑HMAC‑SHA256**, 32‑byte key, high iteration count
- Random 16‑byte salt and 12‑byte IV per file
- Authenticated encryption: **AES‑GCM** with integrity check
- No passwords or keys are stored locally
- Wrong password or tampering → decryption fails with an error

### File Format

- Header: magic `FENC` (4B), version (1B), salt (16B), iv (12B)
- Body: ciphertext
- Trailer: GCM tag (16B)

### Folders

- `encrypted/` and `decrypted/` are created automatically
- Optional logs at `logs/operations.jsonl`

### ⚠️ Limitations

- AES‑GCM uses a single‑shot API here; for very large files, the app uses a temporary buffer to keep memory stable before final encryption/decryption.
- Changing the code or header format will make older files incompatible.

## 🧪 Troubleshooting

| Issue | Cause | Solution |
|------|-------|----------|
| Port 5005 busy | Another process is using it | Change `port` in `web_server.py` or stop the other process |
| "Decryption failed" | Wrong password or file corrupted | Re‑enter the correct password; verify source file |
| Import error | Ran from the wrong folder | Run `python web_server.py` inside `38_FileEncryptorAgent` |

## 🛣️ Roadmap

- Drag‑state progress during upload + server‑side streaming
- Per‑file metadata page (size, checksum, created time)
- Optional checksum display (SHA‑256)
- Theming (dark mode)

## 🙋 FAQ

- Q: Can I recover a file without the password?
  - A: No. The password derives the key; without it, decryption is not possible.
- Q: Is my password stored anywhere?
  - A: No. It’s used in memory to derive a key and never saved.
- Q: Can I change the iteration count?
  - A: Yes, edit `PBKDF2_ITERATIONS` in `config.py`.

## 📄 License

Part of the **#100DaysOfAI‑Agents** series. MIT License.

## 38 - FileEncryptorAgent

Local-first CLI to encrypt and decrypt files with password-based AES-256 (GCM). No external APIs. Supports large files with streaming, colored output, overwrite checks, and batch mode.

### Features
- AES-256 GCM with PBKDF2-HMAC-SHA256 key derivation and per-file random salt
- Encrypt to `./encrypted/filename.ext.enc`
- Decrypt to `./decrypted/filename.ext` (original extension preserved from input)
- Masked password input with confirmation on encrypt
- Large file streaming with progress bar
- Overwrite prompts and unknown file-type warnings (on decrypt)
- Batch encrypt/decrypt multiple files
- Optional JSONL logging to `./logs/operations.jsonl`

### Security Notes
- Keys are derived from your password via PBKDF2 (SHA-256, 32-byte key, high iteration count)
- Random 16-byte salt and 12-byte IV per file
- We never store passwords or keys
- Authenticated encryption (GCM) validates integrity; wrong passwords produce errors

### Install
```bash
cd 38_FileEncryptorAgent
pip install -r requirements.txt
# or on Windows
install.bat
```

### Run (GUI)
```bash
python web_server.py  # or: start_web.bat
```

<!-- Desktop EXE removed per request; focusing on CLI and Web GUI only. -->

### Usage (Menu)
1) Encrypt a file → enter path, confirm password, choose overwrite if needed
2) Decrypt a file → enter `.enc` path, choose overwrite if needed
3) Help → quick tips
4) Exit

### Batch Mode
- From the main menu, you can input multiple comma-separated file paths
  - Example: `path\to\a.txt, path\to\b.pdf, path\to\c.jpg`

### File Format
- Header: magic `FENC` (4 bytes), version (1 byte = 1), salt (16 bytes), iv (12 bytes)
- Body: ciphertext (streamed)
- Trailer: GCM tag (16 bytes)

### Folders
- `./encrypted/` and `./decrypted/` auto-created
- Logs at `./logs/operations.jsonl` (optional)

### Bonus Features
- Batch encrypt/decrypt via comma-separated input paths
  - Example (Encrypt): Enter `C:\files\a.txt, C:\files\b.pdf` at the prompt
  - Example (Decrypt): Enter `C:\files\a.txt.enc, C:\files\b.pdf.enc`
- Optional JSONL operation logs in `./logs/operations.jsonl`
  - Each line is a JSON object with `ts`, `event`, `input`, `output` or `error`
  - Disable by setting `ENABLE_JSONL_LOG = False` in `config.py`
- Future: GUI upgrade path (HTML + Tailwind) consistent with earlier agents

### Disclaimer
This tool aims for practical local encryption with modern primitives, but it is not a formal security audit. Use responsibly.

### GUI Plan (Future)
- Tech: Reuse the pattern from earlier agents (Flask + HTML + Tailwind)
- Pages:
  - Home: two cards — Encrypt and Decrypt
  - Encrypt: file picker, password + confirm fields (masked), progress bar
  - Decrypt: file picker for `.enc`, password field (masked), progress bar
- UX:
  - Drag-and-drop file area with type hints; show warnings for unknown types
  - Toasts/snackbars for success/error; color-coded statuses
  - Download link for output, plus links to `encrypted/` and `decrypted/`
- Backend:
  - Flask routes `/encrypt` and `/decrypt` that call the same `crypto_core`
  - Stream uploads to a temp file, process, then return download or status JSON
  - Optional JSONL logging shared with CLI
- Assets:
  - Tailwind via CDN; minimal JS for progress and form handling
  - Keep entirely local; no external APIs

  