# 🧹 TextFixer Assistant — Day 21 of #100DaysOfAI-Agents

A lightweight, always-running desktop assistant that corrects grammar, spelling, punctuation, and basic style in any app. Select text anywhere, hit the hotkey (default: Ctrl+.), and your text is corrected in-place — no switching windows or copy/paste.

---

## ✨ Features

- Runs in the background after launch
- Global selection correction via hotkey (default: **Ctrl+.**)
- Undo via **Ctrl+Shift+W** (uses app undo when available)
- Provider support: **LanguageTool** (default) or **OpenAI**
- Language auto-detection or forced language (e.g., `en-US`)
- Style preferences: neutral, formal, casual
- Minimal latency with clipboard-based copy/correct/paste
- Optional Windows toast confirmation (non-intrusive "Corrected")
- Restores your clipboard automatically after paste

---

## 🛠️ Tech Stack

- Python 3.9+
- `pynput` for global hotkeys
- `pyperclip` for clipboard operations
- `language-tool-python` (public API) or `openai` for AI corrections
- `.env` for configuratilo

---

## 🚀 Quick Start (Windows)

```powershell
cd 21_TextFixer_Assistant
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy env.example .env
# Edit .env to set PROVIDER and options
python main.py
```

Or use batch scripts:

```powershell
cd 21_TextFixer_Assistant
.\install.bat
.\start.bat
```

> Default hotkeys:
> - Fix: Ctrl+.
> - Undo: Ctrl+Shift+W

### Run silently in background
- Keep the terminal minimized. The listener is non-blocking and low-CPU.
- Optionally add a shortcut to `start.bat` in Windows Startup:
  1. Press Win+R → `shell:startup`
  2. Paste a shortcut to `start.bat` here

---

## ⚙️ Configuration (.env)

```env
PROVIDER=languagetool   # languagetool | openai
LANGUAGE=auto           # en-US, en-GB, de-DE, fr-FR, or auto
STYLE=neutral           # neutral | formal | casual
HOTKEY=<ctrl>+.
UNDO_HOTKEY=<ctrl>+<shift>+w

# Timing tweaks (milliseconds)
COPY_WAIT_MS=80         # Increase if paste is unreliable
PASTE_WAIT_MS=60        # Increase if target app is slow

# UX toggles
LOG_ENABLED=true
RESTORE_CLIPBOARD=true
TOAST_ENABLED=true
TOAST_DURATION_MS=800

# If PROVIDER=openai
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
```

---

## 🧩 How It Works

1. On hotkey, the assistant triggers `Ctrl+C` to copy the selection
2. Sends the text to the selected provider
3. Replaces the selection by setting clipboard and pressing `Ctrl+V`
4. Stores last change so you can undo with `Ctrl+Shift+W` (uses app undo when available)

> Note: Some apps may restrict clipboard or block synthetic key events; results may vary.

---

## 🧪 Testing

- Try on websites (e.g., WhatsApp Web, Gmail), text editors, and chat apps
- Switch providers: set `PROVIDER=openai` and add `OPENAI_API_KEY`
- Adjust timing if paste happens too quickly: increase `COPY_WAIT_MS`/`PASTE_WAIT_MS`

---

## ⚡ Performance Tuning (low-latency, low-CPU)

- **Use LanguageTool (default)**: lower overhead vs remote LLM calls. If you need stronger style changes, switch to OpenAI.
- **Keep delays small**: defaults are optimized (`COPY_WAIT_MS=80`, `PASTE_WAIT_MS=60`). If you see missed pastes, increase by +40ms steps.
- **Clipboard restore**: keep `RESTORE_CLIPBOARD=true` for seamless UX; has negligible cost.
- **Disable toast**: set `TOAST_ENABLED=false` if you prefer zero UI.
- **Network**: public LanguageTool API can add latency; consider a local LanguageTool server for fastest results.
- **OpenAI**: remote calls depend on your internet latency; not ideal for sub-100ms needs.

Local LanguageTool (advanced):
- Running a local server can reduce latency and avoid rate limits. See LanguageTool docs. If you switch, `language-tool-python` will use the server automatically when configured.

---

## 🔐 Privacy & Safety

- Clipboard content is used transiently for copy/paste; no data is stored by default
- With LanguageTool Public API, text is sent to `api.languagetool.org`
- With OpenAI, text is sent to OpenAI under your API key
- Do not use with confidential text if that is a concern

---

## 📁 Project Structure

```
21_TextFixer_Assistant/
├── config.py               # App configuration
├── correction_service.py   # Providers: LanguageTool, OpenAI
├── hotkey_listener.py      # Global hotkey and clipboard logic
├── main.py                 # Entry point for background runner
├── requirements.txt        # Dependencies
├── install.bat             # Windows installer
├── start.bat               # Windows launcher
├── env.example             # Example environment config
└── README.md               # This file
```

---

## 🙋 FAQ & Troubleshooting

- **Hotkey doesn't trigger?**
  - Run terminal as Administrator (some apps intercept keys)
  - Change `HOTKEY` in `.env` to avoid collisions
  - Ensure exact pynput format, e.g. `<ctrl>+.` or `<ctrl>+<alt>+y`

- **Nothing is pasted / partial paste?**
  - Increase `PASTE_WAIT_MS` (try 100–140)
  - Some apps block synthetic paste; try a different target to confirm
  - Ensure the text is selected and the field is editable

- **Clipboard changed unexpectedly?**
  - Keep `RESTORE_CLIPBOARD=true` (default). This restores your original clipboard after paste.

- **Toast not showing?**
  - Install `win10toast` (in requirements). Supported on Windows 10+ only
  - It’s optional; set `TOAST_ENABLED=false` to disable

- **OpenAI: Missing API key**
  - Set `OPENAI_API_KEY` in `.env` and restart
  - Verify billing/quotas if requests fail

- **LanguageTool: Rate-limited or slow**
  - Public API may throttle; try later or run a local server
  - For speed-critical flows, keep corrections short or local

- **"Undo:" printed in console**
  - Fixed in `start.bat` by escaping the pipe (`^|`)

- **Wrong folder name (space) error**
  - Use `21_TextFixer_Assistant` (no spaces). Running from `21_Text Fixer_Assistant` will use older files.

- **Permission issues / no effect**
  - Some corporate setups block global hooks. Run as Admin or try a personal machine

- **App freezes or lags**
  - The hotkey handler runs in a background thread; if you still see lag, ensure antivirus isn’t sandboxing the process and increase the delays slightly

---

## 🔧 Ways to Improve Further

- **Local LanguageTool server** for near-instant corrections and no rate limits
- **Model fallback**: try LanguageTool first, then OpenAI for ambiguous cases
- **Domain presets**: style presets for email, chat, docs
- **Undo buffer**: store more history entries for multi-step undo
- **Per-app configs**: different hotkeys or delays per application
- **Multi-language UI**: hotkeys to toggle `LANGUAGE` on the fly

---

## 📄 License

Part of #100DaysOfAI-Agents. MIT licensed.


