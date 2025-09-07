# 📰 NewsSummarizerAgent - Day 37 of #100DaysOfAI-Agents

<div align="center">

![NewsSummarizerAgent Banner](https://img.shields.io/badge/NewsSummarizerAgent-Day%2037-blue?style=for-the-badge&logo=news&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-orange?style=for-the-badge&logo=openai&logoColor=white)
![SerpAPI](https://img.shields.io/badge/Search-SerpAPI-red?style=for-the-badge&logo=google&logoColor=white)

**Fetch, search, and summarize the day’s news with a clean, interactive CLI**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [💻 CLI Usage](#-cli-usage) • [💾 Exports](#-exports) • [🧪 Testing](#-testing) • [🛠 Troubleshooting](#-troubleshooting)

</div>

---

## ✨ What is NewsSummarizerAgent?

NewsSummarizerAgent automatically fetches daily news from the web (via SerpAPI), extracts full article text, and summarizes it using OpenAI. It’s perfect for journalists, researchers, and analysts who want quick, structured briefings saved locally in Markdown, PDF, or JSON.

### 🌟 Key Highlights
- **🔎 Smart Fetch**: SerpAPI Google News/Web with keyword filters
- **🧠 AI Summaries**: 3–5 bullets + label (Alert-Level | Trending | Regional)
- **🖥️ Enhanced CLI**: Interactive prompts, spinners, colored output, tables
- **💾 Local-First**: Save to `data/summaries/YYYY-MM-DD_news_summary.*`
- **📂 Multi-Format**: Export to Markdown, PDF, JSON

## 🎯 Features

### 🚀 Core Functionality
- ✅ Date-based or keyword-based fetching
- ✅ Full-text extraction with `newspaper3k`
- ✅ OpenAI-powered concise summaries
- ✅ Section headings: “Top News” or “Top results for: <keyword>”
- ✅ Result count control (suggests 2–3 for short queries)

### 💻 Enhanced Terminal UI
- ✅ Colored panels and status spinners (Rich)
- ✅ Results table with Title, Source, Label, Keyword
- ✅ Interactive prompts for date, keywords, category, result count
- ✅ “Open saved file now?” cross‑platform action

## 🚀 Quick Start

### 📋 Prerequisites
- Python 3.8+
- OpenAI API key
- SerpAPI key

### 🔧 Installation
```bash
cd 37_NewsSummarizer
pip install -r requirements.txt

# Environment (.env)
echo OPENAI_API_KEY=your_openai_key >> .env
echo SERPAPI_API_KEY=your_serpapi_key >> .env
echo OPENAI_MODEL=gpt-4o-mini >> .env
```

### 🎯 First Run
```bash
# Interactive mode (recommended)
python cli.py --interactive

# Non-interactive examples
python cli.py --date 2025-09-07
python cli.py --search "Pakistan Floods" --date 2025-09-06
python cli.py --date 2025-09-07 --category tech --search "AI regulation"
```

## 💻 CLI Usage

- When using `--interactive`, you can:
  - Pick a date
  - Enter keywords (optional)
  - Set category tag (optional)
  - Choose how many top results to include
  - Choose export format: md (default), pdf, json
  - Open the saved file immediately

- Output preview includes:
  - Section title (Top News or Top results for: <query>)
  - Table: Title | Source | Label | Keyword
  - Success message with full save path

## 💾 Exports

Saved to `data/summaries/` with names like:
- `YYYY-MM-DD_news_summary.md`
- `YYYY-MM-DD_news_summary.pdf`
- `YYYY-MM-DD_news_summary.json`

Markdown structure per article:
- Date, Headline, Source, Tags, 3–5 bullets, Label, Link

## 🏗️ Project Structure

```
37_NewsSummarizer/
├── cli.py                 # Interactive CLI (Rich UI, exports)
├── news_fetcher.py        # SerpAPI + newspaper3k extraction
├── summarizer.py          # OpenAI summarization (3–5 bullets + label)
├── config.py              # Settings and .env loading
├── utils.py               # Helpers (date parsing, directories)
├── requirements.txt       # Dependencies
└── data/
    └── summaries/         # Output directory (auto-created)
```

## ⚙️ Configuration

Set via environment or `.env`:
```
OPENAI_API_KEY=...
SERPAPI_API_KEY=...
OPENAI_MODEL=gpt-4o-mini
DATA_DIR=data
```

## 🧪 Testing

- Manual sanity test:
```bash
python cli.py --interactive
# Choose small result count and md export to verify file write
```
- Verify output file appears in `data/summaries/` and opens on confirmation.

## 🛠 Troubleshooting

| Issue | Cause | Fix |
|------|-------|-----|
| Missing OPENAI_API_KEY | Not set in env | Add to `.env` or environment |
| Missing SERPAPI_API_KEY | Not set in env | Add to `.env` or environment |
| No articles fetched | Query too niche or rate limits | Try broader keywords or wait |
| Empty summaries | Article extraction failed | Retry or try a different query |
| PDF export error | ReportLab missing | `pip install -r requirements.txt` |

## 📄 License & Credits

This project is part of **#100DaysOfAI-Agents**.

**MIT License** — free to use and modify.

**Thanks** to OpenAI, SerpAPI, and the Python open‑source ecosystem.
