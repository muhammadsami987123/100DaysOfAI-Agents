# 🖼️ SlideGeneratorAgent - Day 44 of #100DaysOfAI-Agents

<div align="center">

![Slides Badge](https://img.shields.io/badge/SlideGeneratorAgent-Day%2044-blue?style=for-the-badge&logo=microsoftpowerpoint&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8%2B-green?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20Framework-red?style=for-the-badge&logo=fastapi&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-ChatCompletions-orange?style=for-the-badge&logo=openai&logoColor=white)

**Turn any topic into a professional 20–22 slide deck with optional images**

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [🧰 Configuration](#-configuration--env) • [🌐 API](#-api) • [🧪 Troubleshooting](#-troubleshooting)

</div>

---

## ✨ What is SlideGeneratorAgent?

SlideGeneratorAgent is an AI-powered web app that converts a single topic into a well-structured slide deck. It produces 20–22 concise slides with clear titles, 3–5 bullets each, and optional images. Export the deck as Markdown or standalone HTML, and keep everything locally in your `slides/` folder.

### 🌟 Key Highlights

- 20–22 slides per topic, optimized for clarity and coverage
- Each slide: title + 3–5 concise bullets
- Optional images per slide (remote or locally downloaded)
- Beautiful live preview with thumbnails and navigation
- One-click downloads: `.md` and `.html`
- Local-first storage in `slides/{slug}/`

## 🎯 Features

### 🚀 Core
- ✅ Topic-to-slides generation with language selection (English, Urdu, Hindi)
- ✅ 20–22 slides target with configurable min/max
- ✅ Optional images per slide via `INCLUDE_IMAGES`
- ✅ Optional local image downloading via `DOWNLOAD_IMAGES`
- ✅ Export to Markdown and standalone HTML

### 💻 Web UI
- ✅ Dark/Light theme toggle, Compact mode, Font size slider (persisted)
- ✅ Progress bar during generation
- ✅ Slide thumbnails and previous/next controls
- ✅ Error handling with helpful messages

### 📁 Storage
- ✅ Saves to `slides/{topic-slug}/slides.md` and `slides/{topic-slug}/index.html`
- ✅ When downloading images, files are served from `/slides/{slug}/img_*.{ext}`

## 🏗️ Project Structure

```
44_SlideGeneratorAgent/
├── main.py                 # Uvicorn entrypoint
├── web_app.py              # FastAPI app + routes
├── llm_service.py          # OpenAI integration and JSON normalization
├── config.py               # Settings via env/.env
├── templates/
│   └── index.html          # Web UI (Tailwind via CDN)
├── static/                 # Static assets (optional)
├── slides/                 # Generated decks (auto-created)
├── requirements.txt        # Python dependencies
├── install.bat             # Windows installer (creates .env template)
├── start.bat               # Windows runner (loads .env, runs server)
└── README.md               # This file
```

## 🚀 Quick Start

### 📋 Prerequisites
- Python 3.8+
- OpenAI API key

### ⚡ One-Click (Windows)
```bash
install.bat
```
This will create a venv, install dependencies, and scaffold `.env` with sensible defaults.

### 🔧 Manual Install
```bash
pip install -r requirements.txt
```

Create `.env` (or export env vars):
```env
OPENAI_API_KEY=your_openai_api_key_here
SLIDES_MODEL=gpt-4o-mini
PORT=8080
SLIDES_MIN=20
SLIDES_MAX=22
INCLUDE_IMAGES=true
DOWNLOAD_IMAGES=false
IMAGE_TIMEOUT_SEC=10
```

Run the server:
```bash
python main.py
```
Open `http://localhost:8080`.

## 🧰 Configuration & Env

- `OPENAI_API_KEY` (required): your OpenAI key
- `SLIDES_MODEL` (default: `gpt-4o-mini`)
- `PORT` (default: `8080`)
- `SLIDES_MIN` (default: `20`)
- `SLIDES_MAX` (default: `22`)
- `INCLUDE_IMAGES` (default: `true`) — ask LLM to include `image_url` per slide
- `DOWNLOAD_IMAGES` (default: `false`) — download images into `slides/{slug}` and rewrite URLs to local paths
- `IMAGE_TIMEOUT_SEC` (default: `10`) — per-image download timeout

Notes:
- When `DOWNLOAD_IMAGES=true`, the app mounts `/slides` to serve local images.
- Already-generated decks won’t be retrofitted; regenerate to populate images.

## 🧭 Usage
1. Enter a topic and choose a language
2. Click “Generate Slides”
3. Browse slides in the preview pane and via thumbnails
4. Download `.md` or `.html` (files are saved to `slides/{slug}/`)

Keyboard shortcut: `Ctrl/Cmd + Enter` to generate.

## 🌐 API

### POST `/api/generate`
Request body:
```json
{ "topic": "ai agents", "language": "en" }
```
Response:
```json
{
  "success": true,
  "slides": [
    { "title": "...", "bullets": ["..."], "image_url": "https://... or /slides/..." }
  ],
  "slide_count": 21,
  "est_minutes": 5,
  "slug": "ai-agents",
  "llm": true
}
```

### GET `/download/{slug}/slides.md`
Returns Markdown deck.

### GET `/download/{slug}/index.html`
Returns standalone HTML deck (Tailwind via CDN).

## 🧪 Troubleshooting

- Images not showing:
  - Set `INCLUDE_IMAGES=true` and consider `DOWNLOAD_IMAGES=true`
  - Increase `IMAGE_TIMEOUT_SEC` to 20 and regenerate
  - Check browser network tab for 404s under `/slides/...`
- Empty or short output:
  - Ensure a valid `OPENAI_API_KEY` and that your model is accessible
  - Try a clearer topic name (e.g., “Neural Networks” vs “nn”)
- Server not starting: ensure port is free or update `PORT` in `.env`

## 🔮 Roadmap

- Preset outlines per topic type (e.g., biography, how‑to, research summary)
- Slide citations and “References” slide
- PDF export
- More themes and typography options

## 📜 License & Credits

Part of the **#100DaysOfAI-Agents** challenge.

**MIT License** — free to use, modify, and distribute.

Thanks to FastAPI, Jinja2, Tailwind CDN, and the Python community.
 - `DOWNLOAD_IMAGES`: `true|false` to download images locally and rewrite URLs (default false)
 - `IMAGE_TIMEOUT_SEC`: per-image download timeout (default 10)


