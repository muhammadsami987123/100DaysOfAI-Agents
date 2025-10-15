# ✍️ PromptImproverAgent - Day 72 of #100DaysOfAI-Agents

<div align="center">

![PromptImproverAgent Banner](https://img.shields.io/badge/PromptImproverAgent-Day%2072-teal?style=for-the-badge&logo=google&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-green?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20Framework-blue?style=for-the-badge&logo=fastapi&logoColor=white)
![LLM](https://img.shields.io/badge/LLM-Gemini%202.0%20%7C%20OpenAI-orange?style=for-the-badge)

**Turn messy prompts into clear, structured, high‑quality prompts for any LLM**

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [🌐 UI](#-web-interface) • [🔌 API](#-api) • [⚙️ Config](#%EF%B8%8F-configuration--setup) • [🧪 Troubleshooting](#-troubleshooting)

</div>

---

## ✨ What is PromptImproverAgent?

PromptImproverAgent is your personal Prompt Coach. Paste any rough/unclear prompt; the agent clarifies, adds missing context, and restructures it for optimal results across GPT, Gemini, Claude, or other LLMs. It also suggests 2–3 alternative versions in different styles (formal, creative, concise) and explains why it improved the prompt that way.

### 🌟 Key Highlights
- **🎯 Clear, structured outputs** optimized for LLMs
- **🪄 2–3 alternative styles** (formal, creative, concise, etc.)
- **🧠 Optional tone/style selector**
- **⚡ Fast web UI** (HTML + Tailwind) served via FastAPI
- **🔁 Modular LLMs**: Gemini 2.0 Flash or OpenAI GPT selectable via config

## 🎯 Features

### 🚀 Core Functionality
- ✅ Clarifies ambiguous user prompts
- ✅ Adds minimal missing context
- ✅ Restructures for best LLM performance
- ✅ Generates 2–3 alternative prompts
- ✅ Explains the rationale concisely

### 💻 User Interface
- ✅ Beautiful Tailwind UI (glassmorphic, responsive)
- ✅ Loading indicators and smooth scroll
- ✅ Copy buttons with feedback animations
- ✅ Text wrapping to avoid overflow

### 🔌 Backend & LLM
- ✅ FastAPI backend with `/improve` endpoint
- ✅ Config‑driven provider: `gemini` or `gpt`
- ✅ Robust JSON parsing and fallbacks if the model returns prose

## 🚀 Quick Start

### 📋 Prerequisites
- Python 3.10+
- API key for Gemini or OpenAI (optional for fallback mode)

### ⚡ Install & Run
```bash
cd 72_PromptImproverAgent
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Environment (choose one model)
# PowerShell example:
$env:LLM_MODEL = "gemini"      # or "gpt"
$env:GEMINI_API_KEY = "your-gemini-key"
# OR
$env:OPENAI_API_KEY = "your-openai-key"

uvicorn main:app --reload
# Open http://127.0.0.1:8000/
```

## 🌐 Web Interface
1. Paste your rough prompt
2. Pick an optional tone/style
3. Click "Improve Prompt"
4. Copy the improved prompt or any variation

UI Enhancements:
- Text wrapping (`whitespace-pre-wrap`, `break-words`)
- Copy feedback and subtle animations
- Smooth scroll to results

## 🔌 API

### Endpoint
```
POST /improve
```

### Request
```json
{
  "raw_prompt": "write an email to my boss abt being sick",
  "tone": "formal"
}
```

### Response
```json
{
  "improved_prompt": "Write a formal email to your manager explaining that you are unwell and unable to work today. Include subject, greeting, reason, duration, handoff, and a polite closing.",
  "variations": [
    "Compose a concise sick-leave email to my supervisor for today.",
    "Draft a professional message informing my manager that I’m unwell and will be unavailable.",
    "Create a detailed sick-day email with subject, reason, expected return, and next steps."
  ],
  "explanation": "Clarified intent, specified structure (subject, reason, duration, handoff), and aligned tone for workplace communication."
}
```

## 🏗️ Project Structure
```
72_PromptImproverAgent/
├── main.py                 # FastAPI app (serves UI + /improve)
├── agent.py                # PromptImproverAgent orchestration
├── utils/
│   ├── __init__.py
│   └── llm_service.py      # LLM integration (Gemini/OpenAI)
├── templates/
│   └── index.html          # Tailwind UI
├── prompts/
│   └── prompt_improvement.txt  # System template for Prompt Coach
├── config.py               # Loads env keys & model choice
├── requirements.txt        # Dependencies
└── README.md
```

## ⚙️ Configuration & Setup

Environment variables:
- `LLM_MODEL` = `gemini` | `gpt`
- `GEMINI_API_KEY` = your Gemini API key
- `OPENAI_API_KEY` = your OpenAI API key
- Optional overrides:
  - `GEMINI_MODEL_NAME` (default: `gemini-2.0-flash`)
  - `OPENAI_MODEL_NAME` (default: `gpt-4o-mini`)

## 🧪 Troubleshooting

| Issue | Cause | Fix |
|------|-------|-----|
| `ModuleNotFoundError: agents` | Legacy import path | We use `from agent import PromptImproverAgent` in `main.py` |
| UI text overflows boxes | Long content | Already fixed with `whitespace-pre-wrap` + `break-words` |
| Variations show `[object Object]` | Model returns objects | Normalized to strings in `agent.py` |
| 401/invalid API key | Missing env | Set `LLM_MODEL` and the respective API key |
| No LLM output | Network/keys not set | Fallback response returns structured placeholders |

## 🤝 Contributing
- PRs welcome for UI polish, new styles, or provider adapters.
- Please follow existing code style and keep changes focused.

## 📄 License & Credits
This project is part of the **#100DaysOfAI-Agents** challenge by **Muhammad Sami Asghar Mughal**.

**MIT License** — use, modify, and share freely.
