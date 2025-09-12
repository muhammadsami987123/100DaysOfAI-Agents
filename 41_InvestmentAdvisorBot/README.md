# 💰 InvestmentAdvisorBot - Day 41 of #100DaysOfAI-Agents

<div align="center">

![InvestmentAdvisorBot Badge](https://img.shields.io/badge/InvestmentAdvisorBot-Day%2041-blue?style=for-the-badge&logo=money&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8%2B-green?style=for-the-badge&logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT-orange?style=for-the-badge&logo=openai&logoColor=white)

**Beginner-friendly, CLI-first simulated financial advisor. Works offline with heuristics, or online with OpenAI for richer guidance. Exports Markdown and JSON.**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🧪 Verify Installation](#-verify-installation) • [🏗️ Architecture](#-project-architecture) • [⚙️ Configuration](#-configuration--setup) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is InvestmentAdvisorBot?

InvestmentAdvisorBot is a command-line assistant that helps newcomers create a simple investment plan. Provide basic profile inputs (income, age, risk tolerance, goal), and the bot returns:

- A suggested savings rate
- An asset allocation across stocks, bonds, mutual funds, gold, crypto, and cash
- A concise rationale tailored to your profile
- Optional exports as Markdown and JSON

This project is purely educational and does not execute trades.

### 🌟 Key Highlights

- **CLI-first experience** with an enhanced interactive mode
- **Offline heuristic fallback** (no API key required)
- **OpenAI integration** for richer, personalized explanations
- **Exports** to Markdown (.md) and JSON (.json)
- **Optional 5-year simulation** with `--simulate-returns`
- **Chat mode** with terminal-friendly UI

## 🧩 How This Solves a Real-World Problem

Many beginners struggle to start investing due to information overload, conflicting advice, and fear of making mistakes. This tool reduces that friction by:

- Providing a simple, opinionated starting plan based on income, age, risk, and goals
- Teaching core concepts (savings rate, asset allocation, risk) with plain-language explanations
- Offering an offline mode so learning and planning work without accounts or subscriptions
- Enabling consistency via exportable Markdown/JSON you can revisit, track, and share
- Demonstrating trade-offs with an illustrative 5-year projection to set realistic expectations
- Encouraging better habits (pay-yourself-first, diversification, long-term thinking)

Example: A 25-year-old with variable income and “medium” risk tolerance can quickly get a reasonable savings target, a diversified allocation, and a short rationale—then export it to share with a mentor or keep as a baseline to improve over time.

## 🎯 Features

### 🚀 Core Functionality
- ✅ AI-backed advice (uses OpenAI when `OPENAI_API_KEY` is present)
- ✅ Heuristic fallback for offline use
- ✅ Clean Markdown output: Financial Summary, Investment Plan, Suggested Allocation, Why This Plan Fits You
- ✅ Export to Markdown and JSON

### 🧾 Extras
- ✅ `--simulate-returns`: simple 5-year projection (illustrative)
- ✅ `--language`: placeholder for multilingual outputs (en, ur, hi)
- ✅ `--chat`: conversational mode with a Rich-style UI
- ✅ `--non-interactive`: run without prompts (great for scripts/tests)

## 🚀 Quick Start

### 📋 Prerequisites

- Python 3.8+
- (Optional) OpenAI API key (`OPENAI_API_KEY`) for GPT-based advice

### ⚡ Installation

```powershell
# 1) Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) (Optional) Provide your API key
set OPENAI_API_KEY=sk-your_key_here
```

### 🎯 First Run

```powershell
# Quick, non-interactive run (auto-saves Markdown and JSON)
python main.py --income 2000 --age 28 --risk medium --goal retirement --export-json --non-interactive

# Interactive guided menu
python main.py

# Chat mode
python main.py --chat

# With OpenAI (ensure key is set)
set OPENAI_API_KEY=sk-your_key_here
python main.py --income 3000 --age 35 --risk high --goal long-term --export-json
```

## 🧪 Verify Installation

```powershell
python test_agent.py
```

Expected checks:
- ✅ Python and dependencies load
- ✅ Heuristic advisor runs
- ✅ Markdown output generated

## 📄 Output Format

Default Markdown sections:

- ## Financial Summary
- ## Investment Plan
- ## Suggested Allocation
- ## Why This Plan Fits You

With `--export-json`, a JSON file is also written containing the profile, allocation, and markdown text.

## 📊 Simulation

Use `--simulate-returns` for a simple 5-year projection using fixed heuristic annual returns per asset class. This is illustrative, not a forecast.

## 🏗️ Project Architecture

```
41_InvestmentAdvisorBot/
├── config.py             # API key helper and setup instructions
├── investment_agent.py   # Core advisor logic (OpenAI + heuristic fallback)
├── main.py               # CLI entrypoint and interactive menu
├── requirements.txt      # Dependencies
├── README.md             # This file
├── test_agent.py         # Simple non-interactive smoke test
└── todos.json (optional) # Example storage for other agents
```

### Technical Notes

- Heuristic allocation works offline; OpenAI calls are used only when `OPENAI_API_KEY` is set. Model name and parameters can be tuned in `investment_agent.py`.

## ⚙️ Configuration & Setup

Set your OpenAI key via environment variable or a `.env` file.

```powershell
# Windows
set OPENAI_API_KEY=sk-your_api_key

# macOS/Linux
export OPENAI_API_KEY=sk-your_api_key
```

Or create `~/.env` with:

```
OPENAI_API_KEY=sk-your_api_key
```

## 🐛 Troubleshooting

| Issue | Cause | Solution |
|------|-------|----------|
| "OpenAI API key not found" | Missing/invalid key | Set `OPENAI_API_KEY` or use offline mode |
| "Module not found" | Missing dependencies | Run `pip install -r requirements.txt` |
| "Permission denied" | File system restrictions | Run shell as admin or change directory |

## 🔮 Future Roadmap

| Feature | Status | Description |
|---------|--------|-------------|
| PDF export | Planned | Export advice to PDF (reportlab/weasyprint) |
| Token streaming | Planned | Streamed responses in chat mode |
| Multilingual templates | Planned | Localized Markdown layouts |
| Unit tests | Planned | Tests for heuristic allocation logic |

## 🤝 Contributing

Contributions are welcome! Suggested improvements:

- Add configurable model and prompt templates
- Add PDF export and better multilingual support
- Implement true token streaming from OpenAI to the chat UI
- Add unit tests for heuristic allocation logic

To contribute:
1. Fork the repository
2. Create a feature branch
3. Open a pull request with tests and description

## 🛡️ Safety & Disclaimer

This tool provides educational suggestions only. It is not a licensed financial advisor and does not execute trades. Always consult a certified professional before making real financial decisions.

## 📄 License & Credits

This project is part of the **#100DaysOfAI-Agents** challenge by **Muhammad Sami Asghar Mughal**.

**MIT License** - Feel free to use, modify, and distribute!

---

<div align="center">

## 🎉 Ready to plan smarter?

**Generate a simple, beginner-friendly investment plan right from your terminal.**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🧪 Verify Installation](#-verify-installation)

---

**Made with ❤️ by the #100DaysOfAI-Agents community**

*Day 41 of 100 - Building the future of AI agents, one day at a time!*

</div>
