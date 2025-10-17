# 🕒 TimezoneConverter - Day 74 of #100DaysOfAI-Agents

<div align="center">

![TimezoneConverter Banner](https://img.shields.io/badge/TimezoneConverter-Day%2074-purple?style=for-the-badge&logo=clockify&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-green?style=for-the-badge&logo=python&logoColor=white)
![LLM](https://img.shields.io/badge/LLM-Gemini%202.0%20%7C%20OpenAI-orange?style=for-the-badge&logo=google&logoColor=white)
![CLI](https://img.shields.io/badge/Interface-CLI-blue?style=for-the-badge)

**Convert times between time zones using natural language — DST aware and friendly**

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [🧪 Examples](#-examples) • [⚙️ Config](#%EF%B8%8F-configuration--setup) • [🐛 Troubleshooting](#-troubleshooting) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is TimezoneConverter?

TimezoneConverter is a CLI AI agent that understands natural language like “Convert 3 PM PST to IST” or “What’s noon in Chicago in London time?” and returns accurate, DST‑aware conversions with clear formatting.

### 🌟 Key Highlights

- **🧠 Natural Language Parsing**: Uses Gemini or OpenAI to extract time, source, and target zones
- **🕰 DST Awareness**: Correctly accounts for daylight saving time
- **🔎 Ambiguity Handling**: Maps common abbreviations and city names to IANA time zones
- **⌨️ Clean CLI**: Minimal, readable output with emojis
- **📝 History Log**: Saves conversions to `log.txt`

## 🎯 Features

### 🚀 Core Functionality
- ✅ Convert times using 12‑hour or 24‑hour formats
- ✅ Understands cities and abbreviations (e.g., PST, IST, London, Tokyo)
- ✅ DST and regional shifts are accounted for via pytz
- ✅ Robust fallbacks when the LLM is unavailable or returns non‑JSON

### 🧠 Parsing Intelligence
- ✅ LLM‑powered JSON extraction (time, date, source TZ, target TZ)
- ✅ Regex fallback for quick parsing when LLM fails
- ✅ Heuristic timezone resolution for popular cities and abbreviations

### 💻 CLI Experience
- ✅ Simple prompt, readable output
- ✅ Helpful error messages and examples
- ✅ Logs every query + result to `log.txt`

---

## 🚀 Quick Start

### 📋 Prerequisites
- **Python 3.10+**
- **Gemini or OpenAI API key** (Gemini recommended by default in config)

### 🔧 Installation
```bash
cd 74_TimezoneConverter
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
# source venv/bin/activate

pip install -r requirements.txt
```

### 🔑 Environment
Create a `.env` in the project root (or set env vars):
```env
# Choose a provider and model
MODEL_PROVIDER=gemini
MODEL_NAME=gemini-2.0-flash

# Keys (set at least one based on provider)
GEMINI_API_KEY=your-gemini-key
# OPENAI_API_KEY=your-openai-key

# Optional defaults
DEFAULT_SOURCE_TIMEZONE=UTC
DEFAULT_TARGET_TIMEZONE=Asia/Kolkata
```

### ▶️ Run
```bash
python -m cli.main
```
Note: Run as a module so imports resolve correctly.

---

## 🧪 Examples
Try these in the CLI prompt:
- `Convert 3 PM PST to IST`
- `What's 12 noon in Chicago in London time?`
- `22:00 UTC to CET`
- `8:30 am EST to Singapore time?`
- `I have a call at 5 PM in Tokyo. What time is it in San Francisco?`

Example Output:
```
🕒 03:00 AM (Next Day) — Asia/Dubai (Gulf Standard Time)
🗓 Date: 2025-10-18
🧭 Source Timezone: Eastern Daylight Time (EDT)
🌍 Target Timezone: Gulf Standard Time (GST)
```

---

## 🏗️ Project Structure
```
74_TimezoneConverter/
├── agents/
│   └── timezone_converter_agent.py    # Core agent logic (LLM + conversion)
├── cli/
│   └── main.py                        # CLI interface
├── prompts/
│   └── system_prompt.txt              # Extraction prompt for LLM
├── utils/
│   └── timezone_utils.py              # Abbrev/city maps, DST helpers
├── config.py                          # Env/config loader
├── factory.py                         # Agent factory
├── log.txt                            # Conversion history
├── README.md                          # This file
└── requirements.txt                   # Dependencies
```

### 🔧 Technical Stack
| Component | Technology | Purpose |
|-----------|------------|---------|
| **Core** | Python 3.10+ | CLI agent |
| **Timezones** | pytz, tzdata | Accurate conversions, DST |
| **LLM** | Gemini 2.0 / OpenAI | Natural language parsing |
| **Config** | python-dotenv | Environment management |

---

## ⚙️ Configuration & Setup

### Provider Selection
- Set `MODEL_PROVIDER=gemini` (default) or `openai`
- Set `MODEL_NAME` accordingly (e.g., `gemini-2.0-flash` or `gpt-4o-mini`)

### Default Timezones
- `DEFAULT_SOURCE_TIMEZONE` and `DEFAULT_TARGET_TIMEZONE` are used when missing in input.

### Logging
- Conversions are appended to `log.txt` as `ISO_TIMESTAMP | query | JSON_RESULT`.

---

## 🐛 Troubleshooting

| Issue | Cause | Solution |
|------|-------|----------|
| `ModuleNotFoundError: factory` | Running script file directly | Use `python -m cli.main` from project root |
| LLM JSON error | Model returned prose or empty | Fallback regex parser will attempt extraction |
| `Time or timezone not specified clearly` | Missing time or invalid TZ | Include explicit time and recognizable locations/abbreviations |
| `Invalid timezone` in output | Unrecognized abbreviation/location | Try a city or IANA TZ (e.g., `America/New_York`) |

---

## 🤝 Contributing
- PRs welcome for better timezone mappings, parsing rules, and tests
- Please keep changes focused and match the existing code style

## 📄 License & Credits
This project is part of the **#100DaysOfAI-Agents** challenge by **Muhammad Sami Asghar Mughal**.

**MIT License** — use, modify, and share freely.
