## 📸 ImageCaptionBot - Day 45 of #100DaysOfAI-Agents

<div align="center">

![ImageCaptionBot Banner](https://img.shields.io/badge/ImageCaptionBot-Day%2045-blue?style=for-the-badge&logo=camera&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9%2B-green?style=for-the-badge&logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-orange?style=for-the-badge&logo=openai&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20Framework-red?style=for-the-badge&logo=fastapi&logoColor=white)

**Generate smart, context-aware captions for your images using OpenAI Vision**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🧩 API](#-api-documentation) • [🎨 UI](#-user-interface) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is ImageCaptionBot?

ImageCaptionBot is a sleek, UI-first agent that turns your images into engaging, platform-ready captions. It supports multiple languages and tones, produces multiple variations, and can tailor captions for different platforms like Instagram, LinkedIn, Facebook, Twitter, and WhatsApp. Ideal for social media managers, accessibility alt-text, content creators, and visual storytelling.

### 🌟 Key Highlights

- **🖼️ Multi-image Uploads**: Drag & drop or file picker (up to 10)
- **🌍 Multilingual Captions**: English, Urdu, Hindi
- **🎭 Tone Control**: Professional, Funny, Emotional
- **🔁 Variations**: Generate 5–20 unique captions per image
- **📱 Platform Cards**: Platform-specific formatting per caption
- **📋 One-click Copy & Export**: Copy per caption; export all as TXT/JSON/MD
- **⚡ Powered by OpenAI Vision**: gpt-4o / gpt-4.1 / gpt-4o-mini

## 🎯 Features

### 🚀 Core Functionality
- ✅ **AI Caption Generation**: Vision-powered, context-aware descriptions and captions
- ✅ **Per-Platform Output**: Instagram, LinkedIn, Facebook, Twitter, WhatsApp
- ✅ **Batch Mode**: Generate captions for multiple images at once
- ✅ **Tone & Style**: Control tone (professional/funny/emotional) and style (descriptive/creative/alt-text)
- ✅ **Variations**: Choose number of variations and temperature
- ✅ **Copy & Export**: Copy individual captions; export all results

### 🧠 Vision & Language Options
- ✅ **Languages**: English (`en`), Urdu (`ur`), Hindi (`hi`)
- ✅ **Styles**: Descriptive, Creative, Alt-text
- ✅ **Hashtags & Length**: Smart hashtag suggestions and length control

### 💻 User Interfaces
- ✅ **Modern Web UI**: Tailwind, glassmorphism, responsive
- ✅ **Drag & Drop**: Multi-upload with previews grid
- ✅ **Real-time Feedback**: Loading states and progress indicators
- ✅ **Mobile Friendly**: Works on phones and tablets

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Python 3.9+ | FastAPI server and API |
| **AI Engine** | OpenAI GPT-4o family | Vision captioning |
| **Web Framework** | FastAPI + Jinja2 | Serve UI and endpoints |
| **Frontend** | Vanilla JS + Tailwind CSS | Interactive UI |
| **Server** | Uvicorn | ASGI server |
| **Config** | python-dotenv | Env configuration |

## 🚀 Quick Start

### 📋 Prerequisites

- Python 3.9+
- OpenAI API Key (get from `https://platform.openai.com/api-keys`)

### ⚡ One-Click (Windows)

```bash
# From project root
cd 45_ImageCaptionBot
start.bat
```

### 🔧 Manual Installation

```bash
# 1) Create virtual environment
cd 45_ImageCaptionBot
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 2) Install dependencies
pip install -r requirements.txt

# 3) Configure environment
echo OPENAI_API_KEY=sk-... > .env
echo OPENAI_MODEL=gpt-4o-mini >> .env
echo HOST=127.0.0.1 >> .env
echo PORT=8015 >> .env
echo DEBUG=true >> .env

# 4) Run the server
python server.py
# Open: http://127.0.0.1:8015
```

PowerShell tip: If `&&` fails, run commands on separate lines.

## 🎯 First Use

1. Open the app in your browser
2. Drag & drop one or more images (JPG/PNG/WebP)
3. Select language, tone/style, and variations
4. Click "Generate Captions" and copy or export

## 🧪 Verify Installation

```bash
# Quick sanity check: server import and environment
python -c "import os; assert 'OPENAI_API_KEY' in os.environ; import server; print('✅ Ready')"
```

## 🧩 Project Structure

```
45_ImageCaptionBot/
├── server.py                # FastAPI app (UI + API)
├── vision_service.py        # OpenAI Vision integration
├── config.py                # Env config
├── requirements.txt         # Python dependencies
├── templates/
│   └── index.html           # Tailwind UI
├── static/
│   └── js/app.js           # Frontend logic
├── install.bat              # Windows setup helper
├── start.bat                # Windows start helper
└── README.md
```

## 🔧 Configuration

Create `.env` in `45_ImageCaptionBot/`:

```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
HOST=127.0.0.1
PORT=8015
DEBUG=true
```

You can also edit defaults in `config.py`.

## 🔌 API Documentation

### 📚 Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serve UI |
| `POST` | `/api/caption` | Single image → one caption |
| `POST` | `/api/captions/batch` | Multi-image → multi-platform captions |

#### `POST /api/caption` (multipart)
- Fields: `image` (file), `language` (`en|ur|hi`), `style` (`descriptive|creative|alt`)
- Returns: `{ caption, language, style }`

#### `POST /api/captions/batch` (multipart)
- Fields: `images[]` (files), `language` (`en|ur|hi`), `tone` (`professional|funny|emotional`), `variations` (int), `temperature` (float)
- Returns: `{ results: [{ filename, platforms: { instagram[], linkedin[], facebook[], twitter[], whatsapp[] } }], ... }`

### 📝 Example API Usage

```javascript
// Single image caption
const form = new FormData();
form.append('image', fileInput.files[0]);
form.append('language', 'en');
form.append('style', 'descriptive');

const res = await fetch('/api/caption', { method: 'POST', body: form });
const data = await res.json();
console.log(data.caption);
```

```python
# Batch captions
import requests

files = [
    ('images[]', ('pic1.jpg', open('pic1.jpg', 'rb'), 'image/jpeg')),
    ('images[]', ('pic2.png', open('pic2.png', 'rb'), 'image/png')),
]
data = {
    'language': 'en',
    'tone': 'professional',
    'variations': '8',
    'temperature': '0.7',
}
r = requests.post('http://127.0.0.1:8015/api/captions/batch', files=files, data=data)
print(r.json()['results'][0]['platforms']['instagram'])
```

## 🎨 User Interface

- **Glassmorphic Card**: Clean, modern, responsive
- **Previews Grid**: Visual confirmation of selected images
- **Selectors**: Language, tone, style, variations
- **Per-Platform Cards**: Organized outputs with copy buttons
- **Export**: TXT / JSON / MD

## 🐛 Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| "API key not found" | Missing `OPENAI_API_KEY` | Add to `.env` and restart |
| "Unsupported file type" | Non-image or invalid mime | Use JPG/PNG/WebP |
| CORS blocked | Cross-origin requests | Run UI and API from same origin or enable CORS |
| Model error | Key lacks Vision access | Use GPT-4o/gpt-4.1/gpt-4o-mini and valid key |

## 🔒 Security & Privacy

- No persistent storage; images processed in-memory
- API keys via environment variables only
- Use HTTPS in production

## 🔮 Roadmap

- Batch captions for galleries
- Hashtag suggestions
- Brand tone presets
- EXIF-aware prompts (location/time)

## 🤝 Contributing

Contributions are welcome! Feel free to open issues and PRs for UI/UX, performance, or new features.

## 📄 License

This project is part of the **#100DaysOfAI-Agents** challenge.

**MIT License** — use, modify, and distribute freely.
