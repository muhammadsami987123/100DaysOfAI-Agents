# 🧠 ImageDownloaderBot - Day 82 of #100DaysOfAI-Agents

<div align="center">

![ImageDownloaderBot](https://img.shields.io/badge/ImageDownloaderBot-Day%2082-blue?style=for-the-badge&logo=image&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20Framework-red?style=for-the-badge&logo=fastapi&logoColor=white)

</div>

---

## 📌 Overview

ImageDownloaderBot is an agent that can generate images from text prompts (using Gemini or OpenAI) and download public images from URLs. It provides a unified Image Board UI to preview, enlarge, and download images saved locally by the backend.

This README mirrors the structure of the Day 36 StoryWriterAgent README and is tailored for the image-focused project.

---

## ✨ Key Features

- Prompt-based image generation (Gemini / OpenAI)
- Download images from public URLs (Unsplash, Imgur, direct links)
- Unified Image Board with previews, timestamps, prompt metadata
- Modal / zoom view for large previews
- Download saved images locally
- Responsive UI built with Next.js + Tailwind CSS

---

## ⚙️ Tech Stack

- Frontend: Next.js + TypeScript, Tailwind CSS
- Backend: FastAPI (Python)
- HTTP client: httpx (async)
- Image helpers: aiofiles, Pillow (optional)
- AI: Google Gemini (via google-generativeai) and OpenAI (DALL·E)

---

## 🔧 Quick Install (Backend)

1. Create / activate a Python virtual environment inside the backend folder (recommended):

```powershell
cd 82_ImageDownloaderBot/backend
python -m venv venv
.\venv\Scripts\activate
```

2. Install Python dependencies:

```powershell
pip install -r requirements.txt
```

3. Create a `.env` file (copy from `.env.example`) and add your API keys:

```text
GEMINI_API_KEY="your_gemini_api_key_here"
# If you don't use OpenAI, you can omit OPENAI_API_KEY
OPENAI_API_KEY="your_openai_api_key_here"
```

4. Run the backend (from project root or parent of `backend`):

```powershell
# from repository root
uvicorn backend.main:app --reload
# or from the backend folder (use --app-dir or absolute module path if needed)
```

The backend will be available at `http://127.0.0.1:8000` by default.

---

## 🔧 Quick Install (Frontend)

1. Install dependencies:

```powershell
cd 82_ImageDownloaderBot/frontend
npm install
```

2. Set `NEXT_PUBLIC_BACKEND_URL` in `.env.local` (or use defaults):

```text
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

3. Run the Next.js dev server:

```powershell
npm run dev
```

Open the UI at `http://localhost:3000`.

---

## 🔐 API Key Notes

- Place your keys in `82_ImageDownloaderBot/backend/.env` (do not commit your `.env` to git).
- If you only want to test Gemini, set `GEMINI_API_KEY` and you can omit `OPENAI_API_KEY`.
- If you see `400 API key expired` from Gemini, generate a fresh key from Google Cloud / AI Studio and update `.env`.

---

## 🧩 API Endpoints (Examples)

- Generate image from prompt:

```bash
curl -X POST "http://127.0.0.1:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{ "prompt": "A futuristic cyberpunk city skyline at sunset", "model": "gemini" }'
```

- Download image from URL:

```bash
curl -X POST "http://127.0.0.1:8000/download" \
     -H "Content-Type: application/json" \
     -d '{ "url": "https://example.com/your-image.jpg" }'
```

Responses return JSON with the saved local path and metadata.

---

## 🧪 Troubleshooting & Common Issues

- Error: `API key expired` or `API key invalid` — regenerate key and update `.env`.
- Error: `attempted relative import with no known parent package` when running uvicorn from backend folder — run `uvicorn backend.main:app --reload` from the repository root so Python treats `backend` as a package.
- If the frontend shows `Invalid src prop` from `next/image` referencing an external host (e.g. `via.placeholder.com`), add that host to `next.config.js` under `images.domains` or use an <img> tag for local testing.

---

## ✅ Quick Testing Prompts

- Prompt: `A futuristic cyberpunk city skyline at sunset, glowing neon lights and flying cars.` — expect 1–4 generated thumbnails.
- URL test: `https://images.unsplash.com/photo-...` — should download and appear in Image Board.

---

## 📚 Project Structure (key files)

```
82_ImageDownloaderBot/
├── backend/
│   ├── main.py
│   ├── routes/
│   │   ├── generate_image.py
│   │   └── download_image.py
│   └── utils/
│       ├── gemini_helper.py
│       ├── openai_helper.py
│       └── file_handler.py
├── frontend/
│   ├── pages/
│   │   └── index.tsx
│   ├── components/
│   └── styles/
├── README.md
└── .env.example
```

---

## 🔭 Next Steps & Improvements

- Wire up real Gemini image generation when a supported text-to-image API is available.
- Add secure static file serving and authorization for file downloads.
- Add pagination/filters and tags to the Image Board.
- Persist image metadata in a small database (SQLite) instead of only the filesystem.

---

If you want, I can now:

1. Add `next.config.js` entries to allow placeholder hosts for development.
2. Wire automatic retries and clearer error messages on the backend.
3. Add a tiny integration test script that calls `/generate` and `/download`.

Tell me which of those you'd like next.
