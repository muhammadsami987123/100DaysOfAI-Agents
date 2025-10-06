# 🗞️ VoiceNewsReader - Day 65 of #100DaysOfAI-Agents

<div align="center">

![VoiceNewsReader Banner](https://img.shields.io/badge/VoiceNewsReader-Day%2065-blue?style=for-the-badge&logo=google&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-TTS-orange?style=for-the-badge&logo=google&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20Framework-red?style=for-the-badge&logo=fastapi&logoColor=white)

**Your AI assistant that reads trending news aloud with high‑quality TTS**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🧪 Verify](#-verify-installation) • [🌐 APIs](#-api-documentation) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is VoiceNewsReader?

VoiceNewsReader fetches fresh, relevant headlines and reads them aloud so you can stay informed while driving, working, or relaxing. Filters help you focus on what matters most: category, country, keywords, language, and date range.

### 🌟 Key Highlights

- **📰 Multi‑source fetching**: NewsAPI (top‑headlines/everything) with smart fallbacks (Bing, Google News RSS)
- **🎛️ Accurate Filters**: Category, Country, Keywords, Language, Date Range (day/week/month)
- **🔊 Natural Speech**: Gemini TTS by default, with gTTS/pyttsx3 fallbacks
- **🎧 Audio + Transcript**: Play in the browser, download audio, view transcript
- **🌍 Multilingual**: English and Urdu supported out of the box

## 🎯 Features

### 🚀 Core Functionality
- ✅ **Precise filtering** across category/country or keyword searches
- ✅ **Keyword mode** uses NewsAPI “everything” with language + date range
- ✅ **Country‑aware fallback** to Google News RSS when APIs return zero
- ✅ **Exact item limit** respected (1–10)
- ✅ **Downloadable audio** saved under `audio/`

### 💻 User Interface
- ✅ **Modern Tailwind UI** with two‑column layout
- ✅ **Plain View** toggle for minimal reading list
- ✅ **Clear errors** and loading feedback

### 🔊 Voice Options
- ✅ **Voice gender**: female/male
- ✅ **Rate (wpm) & Pitch** controls
- ✅ **Language**: en, ur (mapped to NewsAPI `ud`)

## 🚀 Quick Start

### 📋 Prerequisites

- Python 3.8+
- Recommended: `NEWSAPI_KEY`
- Optional: `GEMINI_API_KEY` (or set `TTS_ENGINE=gtts`)

### ⚡ One‑Click Installation (Windows)

```bash
install.bat
```

### 🔧 Manual Installation

```bash
cd 65_VoiceNewsReader
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# .env
echo NEWSAPI_KEY=your_newsapi_key_here > .env
echo GEMINI_API_KEY=your_gemini_api_key_here >> .env
echo TTS_ENGINE=gemini >> .env
```

### 🎯 First Run

```bash
python main.py
# Open: http://localhost:8000
```

## 🧪 Verify Installation

```bash
python test_installation.py
# ✅ Python version OK
# ✅ Packages imported
# ✅ Config validated
# ✅ FastAPI app import OK
```

## 🎭 Examples & Usage

### 🌐 Web Interface

1. **Enter Keywords** (e.g., “AI”, “cricket”, “markets”)
2. **Pick Filters**: Category, Country, Language, Date Range, Limit
3. **Choose Voice**: Gender, Rate, Pitch
4. **Read News**: Player appears with transcript and a styled list of stories
5. **Plain View**: Toggle for a compact text-only list

**Pro tips:**
- For keyword searches only, set Category/Country to “Any”
- Use Date Range: “Week” to narrow down recency
- Increase Limit up to 10 for broader digests

## 🏗️ Project Architecture

### 📁 File Structure

```
65_VoiceNewsReader/
├── main.py                 # FastAPI app
├── config.py               # Settings and env
├── news_service.py         # Fetch + normalization + fallbacks
├── news_agent.py           # Orchestration (fetch → script → TTS)
├── tts_service.py          # Gemini/gTTS/pyttsx3
├── templates/
│   └── index.html          # Tailwind UI
├── static/                 # Auto-created
├── audio/                  # Auto-created
├── requirements.txt
├── install.bat
├── start.bat
└── test_installation.py
```

### 🔧 Technical Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | FastAPI | API + UI hosting |
| **News** | NewsAPI, Bing, Google News RSS | Robust fetching with fallbacks |
| **TTS** | Gemini, gTTS, pyttsx3 | High‑quality speech |
| **Frontend** | Tailwind + Vanilla JS | Clean, responsive UI |
| **Server** | Uvicorn | ASGI server |

### 🎯 Key Components

#### 📰 NewsService (`news_service.py`)
- Top‑headlines/everything selection
- Country/language normalization
- Fallback to Bing/Google News RSS

#### 🤖 VoiceNewsAgent (`news_agent.py`)
- Builds concise script from headlines
- Calls TTS and persists audio for download

#### 🔊 TTSService (`tts_service.py`)
- Prefers Gemini; falls back to gTTS/pyttsx3
- Rate/Pitch/Language handling

## ⚙️ Configuration & Setup

```env
NEWSAPI_KEY=your_newsapi_key_here
BING_NEWS_KEY=optional_bing_key
GEMINI_API_KEY=your_gemini_api_key_here
TTS_ENGINE=gemini   # gemini|gtts|pyttsx3
```

## 🌐 API Documentation

### POST `/api/read`

Request body:

```json
{
  "category": "technology|sports|business|null",
  "country": "us|gb|in|pk|null",
  "q": "keyword",
  "limit": 5,
  "language": "en|ur",
  "date_range": "any|day|week|month",
  "voice_gender": "female|male",
  "voice_rate": 150,
  "voice_pitch": 1.0,
  "transcript": true
}
```

Response:

```json
{
  "success": true,
  "items": [{"title":"...","source":"...","url":"...","publishedAt":"..."}],
  "audio_url": "/audio/news_xxx.mp3",
  "audio_mime": "audio/mpeg",
  "audio_filename": "news_xxx.mp3",
  "transcript": "1. Headline — Source. Summary\n..."
}
```

## 🐛 Troubleshooting

| Issue | Cause | Solution |
|------|-------|----------|
| No results | Strict filters | Remove category/country; try keywords + date range |
| Country ignored | Name vs code mismatch | Use dropdown (e.g., India → `in`) |
| Urdu fetch | NewsAPI uses `ud` | UI `ur` is mapped to `ud` internally |
| No audio | TTS engine missing | Set `GEMINI_API_KEY` or `TTS_ENGINE=gtts` |

## 🔮 Future Roadmap

| Feature | Status | Description |
|---------|--------|-------------|
| More languages | Planned | Arabic, Spanish, French, etc. |
| Scheduled digests | Planned | Daily/weekly at user time |
| Source controls | Planned | Include/exclude sources, dedupe |
| Shareable snippets | Planned | Export audio + text cards |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make changes and test thoroughly
4. Commit: `git commit -m "Add feature"`
5. Push: `git push origin feature/your-feature`
6. Open a Pull Request

## 📄 License & Credits

This project is part of the **#100DaysOfAI-Agents** challenge by **Muhammad Sami Asghar Mughal**.

**MIT License** — use, modify, distribute.

---

<div align="center">

## 🎉 Ready to Listen?

**Stay informed with AI‑powered voice news.**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🌐 APIs](#-api-documentation)

---

**Made with ❤️ for Day 65**

</div>


