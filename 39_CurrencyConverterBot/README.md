# 💱 CurrencyConverterBot - Day 39 of #100DaysOfAI-Agents

<div align="center">

![CurrencyConverterBot Banner](https://img.shields.io/badge/CurrencyConverterBot-Day%2039-blue?style=for-the-badge&logo=money&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-orange?style=for-the-badge&logo=openai&logoColor=white)
![exchangerate.host](https://img.shields.io/badge/API-exchangerate.host-red?style=for-the-badge)

**Smart, offline-resilient currency conversion with natural-language queries and a neat CLI UX**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [💻 CLI](#-cli-interface) • [🤖 Chatbot](#-chatbot-mode) • [⚙️ Configuration](#%EF%B8%8F-configuration--env) • [🧪 Troubleshooting](#-troubleshooting)

</div>

---

## ✨ What is CurrencyConverterBot?

CurrencyConverterBot converts between world currencies using live data from `exchangerate.host`, with a fast offline fallback to a local cache. It understands natural language ("Convert 50 GBP to PKR"), resolves country names to ISO codes ("usa" → USD, "pakistan" → PKR), and can add brief GPT insights. A menu-driven CLI provides a consistent, professional terminal experience.

### 🌟 Key Highlights

- **🔌 Live Rates** via `exchangerate.host` with cache fallback
- **🗣 Natural Language** parsing (regex + optional OpenAI)
- **🌍 Country/Name Resolver**: map names like "pakistan" → `PKR`
- **🧠 GPT Insights** (optional): short context lines about currencies
- **💬 Chatbot Mode**: ask questions or do quick conversions
- **🧱 Markdown-in-Panel** output for clean terminal UX (Rich)

## 🎯 Features

### 🚀 Core Functionality
- ✅ Currency conversion with exchange rate, total, timestamp, source
- ✅ Offline fallback to `cache.json` with clear warnings
- ✅ Input validation and user-friendly errors
- ✅ Save conversions to `conversions.log`

### 🤖 Intelligent Extras
- ✅ Natural-language parsing (regex first, GPT fallback if available)
- ✅ Country/currency resolver (local dataset + GPT fallback)
- ✅ Optional one-line GPT insight about the currency pair

### 💻 CLI Experience
- ✅ Menu-based UI with markdown panels and consistent styling
- ✅ One-shot arguments for quick conversions
- ✅ Chatbot mode with live-rate "tool" behavior

## 📁 Project Structure

```
39_CurrencyConverterBot/
├── __init__.py
├── __main__.py               # Enables: python -m 39_CurrencyConverterBot
├── main.py                   # CLI entry (menu + one-shot + chatbot)
├── agents.py                 # OpenAI + exchangerate.host + resolver agents
├── converter.py              # Live rates + cache fallback
├── gpt_parser.py             # NL parsing + brief insights
├── utils.py                  # Helpers (formatting, parsing, json IO)
├── currency_data.py          # Local country/name → ISO currency map
├── config.py                 # Central config, loads .env
├── cache.json                # Cached rates snapshot
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

### 📋 Prerequisites
- Python 3.8+

### ⚡ Install
```bash
pip install -r 39_CurrencyConverterBot/requirements.txt
```

### 🔑 Environment (optional but recommended)
Create a `.env` in the repo root or in `39_CurrencyConverterBot/`:
```env
OPENAI_API_KEY=sk-...           # enables GPT parsing/insights/chatbot
OPENAI_MODEL=gpt-4o-mini        # optional override
EXCHANGE_RATE_API_BASE=https://api.exchangerate.host
EXCHANGE_RATE_API_KEY=          # if you have a key (appended as api_key=...)
REQUEST_TIMEOUT_SECONDS=10
```

### ▶️ Run
```bash
python -m 39_CurrencyConverterBot
# or
python 39_CurrencyConverterBot/main.py
```

### 🎯 One-shot
```bash
python -m 39_CurrencyConverterBot 100 USD INR
```

## 💻 CLI Interface

When you run the app you’ll see a menu like:

```
💱 CurrencyConverterBot — Your Smart Finance Assistant

1. Convert (amount, FROM, TO)
2. Natural language query
3. Chatbot (GPT)
4. Exit
```

Examples:
- 1 → Amount: 200; From: usa; To: pakistan → resolves to USD → PKR
- 2 → "Convert 10,000 yen to Canadian dollars"

Result formatting uses markdown-in-panel for clarity:

```
### 💱 Conversion Result

- **Exchange Rate**: `1 USD = 83.2100 INR`
- **Total**: `₹8,321.00`
- **Data as of**: `2025-09-09T12:34:56Z`
- **Source**: `api`
```

If offline, a note shows the cached source:

```
- **Source**: `cache`
- **Note**: Using cached rates due to network/API issue.
```

## 🤖 Chatbot Mode

Choose option 3 to open a short, focused chatbot. It:
- Parses conversion-like prompts first and calls live rates
- Falls back to GPT answers if not a conversion
- Renders replies as markdown panels

Examples:
- "100 usd to pkr"
- "Is EUR stronger than GBP recently?" (concise, non-advisory response)

## ⚙️ Configuration & .env

Editable in `config.py` (auto-loads `.env`):

```python
EXCHANGE_RATE_API_BASE = os.getenv("EXCHANGE_RATE_API_BASE", "https://api.exchangerate.host")
REQUEST_TIMEOUT_SECONDS = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "10"))
EXCHANGE_RATE_API_KEY = os.getenv("EXCHANGE_RATE_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
```

## 🧠 How It Works

- `converter.py`: Calls `exchangerate.host /latest?base=...` and caches the snapshot. If live fails, uses `cache.json` (direct or cross via base).
- `gpt_parser.py`: Regex-first parsing; if it fails and GPT is enabled, uses a structured JSON extraction prompt.
- `agents.py`: Thin agent layer for parsing/insight (OpenAI) and conversion (exchangerate.host). Includes `CurrencyResolverAgent` to map country/name → ISO code.
- `main.py`: Menu-driven CLI with Markdown panels; one-shot args; chatbot loop.

## 🧪 Troubleshooting

| Issue | Cause | Solution |
|------|-------|----------|
| "attempted relative import" when running `python main.py` | Running as a script outside package context | Prefer `python -m 39_CurrencyConverterBot` or run `python 39_CurrencyConverterBot/main.py` from repo root |
| GPT unavailable in chatbot/insight | No `OPENAI_API_KEY` | Add it to `.env` or environment |
| Offline or API down | Network issue | Bot falls back to `cache.json` and warns |
| Unknown currency name | Not in local map | Try 3-letter ISO code or enable GPT for fallback |

## 🔧 Development Tips

- Extend `currency_data.py` with more countries/currencies as needed
- Adjust `OPENAI_MODEL` if you have access to other models
- Redirect logs by tailing `conversions.log`

## 📜 License

MIT — Part of the #100DaysOfAI-Agents series.

## CurrencyConverterBot (Day 39)

Your smart, offline-resilient currency converter. Converts between currencies using live rates with graceful fallback to cached data, plus natural-language queries and optional brief insights.

### Features
- Live conversion via `exchangerate.host`
- Natural language parsing ("Convert 100 USD to INR")
- Offline fallback with `cache.json`
- Helpful validation and error messages
- Optional short insights via OpenAI (if `OPENAI_API_KEY` set)

### Project Structure
```
39_CurrencyConverterBot/
├── main.py              # CLI entry point
├── converter.py         # API + cache logic
├── gpt_parser.py        # NL parsing and optional insights
├── utils.py             # Helpers and validators
├── cache.json           # Cached rates and metadata
├── requirements.txt
└── README.md
```

### Installation
1) Create/activate a virtual environment (optional but recommended)
2) Install requirements:
```bash
pip install -r requirements.txt
```

### Environment (optional)
- Set `OPENAI_API_KEY` to enable GPT parsing and insights. Without it, a robust regex parser is used.

### Usage
Run the CLI:
```bash
python main.py
```
Example prompts:
- `Convert 100 USD to INR`
- `how much is 50 gbp in pkr?`
- `10,000 yen to Canadian dollars`

Sample output:
```
Exchange Rate: 1 USD = 83.21 INR
Total: ₹8,321.00
Data as of: 2025-09-09 12:34:56 UTC

Save this conversion? (Y/N)
```

### Offline behavior
- On successful API calls, the latest full rates snapshot is cached in `cache.json`.
- If the API is unreachable, the converter uses the cache (if present) and prints a warning.

### Notes
- Currency symbols in totals are best-effort based on ISO codes.
- Validation will warn for unsupported/unknown currency codes.


