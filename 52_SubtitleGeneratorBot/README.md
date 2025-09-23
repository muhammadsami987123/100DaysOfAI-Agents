# 🎬 SubtitleGeneratorBot - Day 52 of #100DaysOfAI-Agents

<div align="center">

![SubtitleGeneratorBot Banner](https://img.shields.io/badge/SubtitleGeneratorBot-Day%2052-blue?style=for-the-badge&logo=subtitles&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9%2B-green?style=for-the-badge&logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-Whisper%20%2B%20GPT--4o-orange?style=for-the-badge&logo=openai&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20Framework-red?style=for-the-badge&logo=fastapi&logoColor=white)

**Generate accurate, editable subtitles from audio/video files and public URLs**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🧰 Configuration](#-configuration) • [🌐 API](#-api-documentation) • [🎨 UI](#-user-interface) • [🧪 Troubleshooting](#-troubleshooting)

</div>

---

## ✨ What is SubtitleGeneratorBot?

SubtitleGeneratorBot is a media assistant that turns your audio/video into clean subtitles. Upload a local file or paste a media link (including optional YouTube support), select language and output format, and download SRT/VTT/TXT. Ideal for creators, educators, and accessibility.

### 🌟 Key Highlights

- **📤 Dual Input**: Upload MP4/MP3/WAV/MOV or paste a public URL
- **🌍 Languages**: Choose source language; optional translation ready
- **💾 Formats**: Export **SRT**, **VTT**, and **TXT** together
- **📝 Editable Workflow**: Clean timestamps and easy line editing
- **🧠 Real ASR (Optional)**: OpenAI Whisper via REST; safe fallback stub
- **▶️ YouTube Support (Optional)**: Uses yt-dlp + ffmpeg to fetch audio
- **📂 Local-first**: Saves to `subtitles/{slug}/{slug}.{ext}`

## 🎯 Features

### 🚀 Core Functionality
- ✅ File upload or URL ingestion
- ✅ Source language selection
- ✅ Output formats: SRT, VTT, TXT
- ✅ Local storage with consistent naming
- ✅ JSON API + responsive UI

### 🧠 AI & Processing
- ✅ OpenAI Whisper transcription (via `USE_REAL_TRANSCRIPTION=true`)
- ✅ Heuristic sentence segmentation → timestamps
- ✅ Fallback stub transcription for demo/testing

### 🌐 URL Support
- ✅ Direct media URLs (mp3/mp4/wav/mov)
- ✅ Optional YouTube audio extraction via `yt-dlp` + `ffmpeg`

### 💻 User Interface
- ✅ Modern card UI (Tailwind CDN)
- ✅ Options: language, format, auto-sync, speaker labels
- ✅ Download buttons for each format

---

## 🚀 Quick Start

### 📋 Prerequisites
- Python 3.9+
- (Optional) OpenAI API Key for real ASR
- (Optional) ffmpeg in PATH for YouTube support

### ⚡ One-Click (Windows)
```bash
cd 52_SubtitleGeneratorBot
start.bat
# Open: http://127.0.0.1:8022
```

### 🔧 Manual Installation
```bash
cd 52_SubtitleGeneratorBot
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### 🔑 Enable Real Transcription (Optional)
Create `.env` in `52_SubtitleGeneratorBot/`:
```env
USE_REAL_TRANSCRIPTION=true
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini-transcribe
```

### ▶️ Enable YouTube Support (Optional)
```env
ENABLE_YOUTUBE=true
# Ensure ffmpeg is installed and on PATH
```

---

## 🧰 Configuration

Environment variables (via `.env` or process env):

| Key | Default | Description |
|-----|---------|-------------|
| `HOST` | `127.0.0.1` | Server host |
| `PORT` | `8022` | Server port |
| `DEBUG` | `false` | Debug mode |
| `USE_REAL_TRANSCRIPTION` | `false` | Use OpenAI Whisper if true |
| `OPENAI_API_KEY` | - | Your OpenAI key |
| `OPENAI_MODEL` | `gpt-4o-mini-transcribe` | Whisper model name |
| `ENABLE_YOUTUBE` | `false` | Enable yt-dlp for YouTube |
| `REQUEST_TIMEOUT_SEC` | `60` | HTTP timeout seconds |
| `TMP_DIR` | `./tmp` | Temp dir for downloads |

Notes:
- Outputs are saved under `subtitles/{slug}/` and served at `/subtitles/...`.
- If real ASR fails, app falls back to a safe stub.

---

## 🏗️ Project Structure

```
52_SubtitleGeneratorBot/
├── main.py                 # Uvicorn entrypoint
├── server.py               # FastAPI app + routes (UI/API)
├── subtitle_service.py     # Transcription, segmentation, formatting
├── config.py               # Env/config management
├── templates/
│   └── index.html          # Tailwind UI
├── static/
│   └── js/app.js          # Frontend interactions
├── subtitles/              # Generated files (auto-created)
├── requirements.txt        # Dependencies
├── install.bat             # Windows installer
├── start.bat               # Windows runner
└── README.md               # This documentation
```

### 🔧 Technical Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Backend | Python 3.9+ | Core application |
| Web | FastAPI + Jinja2 | UI + API |
| AI | OpenAI Whisper (REST) | Transcription |
| Frontend | Tailwind + Vanilla JS | UX |
| Storage | File system | Subtitles output |
| Downloader | requests, yt-dlp (optional) | URL/YouTube ingest |

---

## 🌐 API Documentation

### `GET /`
- Serve the web UI.

### `POST /api/process` (multipart form)
Fields:
- `file` (optional): Uploaded media
- `media_url` (optional): Direct media or YouTube URL
- `source_lang`: Source language code (e.g., `en`)
- `fmt`: `srt|vtt|txt` (UI still generates all)
- `auto_sync` (bool), `speaker_labels` (bool), `translate` (optional)

Response:
```json
{
  "success": true,
  "slug": "uploaded-media",
  "download": {
    "srt": "/subtitles/uploaded-media/uploaded-media.srt",
    "vtt": "/subtitles/uploaded-media/uploaded-media.vtt",
    "txt": "/subtitles/uploaded-media/uploaded-media.txt"
  },
  "fmt": "srt",
  "real": true,
  "youtube": true
}
```

### `GET /download/{slug}/{filename}`
- Download generated SRT/VTT/TXT.

---

## 🎨 User Interface

- Clean card layout with Tailwind
- Upload or paste URL, select language/options
- Progress/Status text and download buttons
- Files are saved locally for iterative editing

---

## 🧪 Troubleshooting

| Issue | Cause | Fix |
|------|-------|-----|
| 400 from `/api/process` | No file or URL provided | Provide one input |
| Whisper fails | Key/Model/Network issue | Check `.env`, model, and connectivity |
| YouTube fails | ffmpeg not installed or disabled | Install ffmpeg; set `ENABLE_YOUTUBE=true` |
| 404 on downloads | Files not generated | Re-run process; check `subtitles/{slug}` |
| Proxy error in OpenAI client | Local proxies | We use plain REST calls to avoid client-proxy issues |

---

## 🔮 Roadmap
- Inline subtitle editor with live preview
- Word-level timestamps and auto-chunking
- Speaker diarization (when available)
- Batch processing and queue
- Translate-to language output

---

## 📄 License & Credits
Part of **#100DaysOfAI-Agents**. MIT License.

Thanks to FastAPI, Jinja2, Tailwind, OpenAI, and the Python community.
