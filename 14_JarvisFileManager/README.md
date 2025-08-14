# 🗂️ JarvisFileManager - Day 14 of #100DaysOfAI-Agents

Voice-controlled, multilingual file manager for your terminal. Speak in English, Hindi, or Urdu to create, open, delete, or list files/folders with smart path handling, live CLI feedback, and TTS confirmations.

---

## ✨ What's Included

- **Voice Input (Mic)** with EN/HI/UR support
- **Natural Command Understanding** (not just templates)
- **Smart Paths**: Defaults to `~/Desktop` if none provided; understands “inside Downloads/Documents/Desktop” etc.
- **Live CLI Feedback**: “🎤 Listening…”, “🧠 Understanding…”, “🔄 Opening…”, “🗑️ Deleting…”, “✅ Creating …”
- **TTS Confirmations**: Speaks success and optional errors
- **Action Logging**: All actions logged to `logs.txt`
- **History**: `show created` lists items created via this tool

---

## 🛠️ Tech Stack

- **Python** (pure CLI)
- **STT**: `speech_recognition` (Google; Sphinx fallback if available)
- **TTS**: `pyttsx3` (offline)
- **Language Detection**: `langdetect`
- **CLI UI**: `rich`
- **Filesystem**: `os`, `pathlib`

---

## ✅ Prerequisites

- Python 3.8+
- Microphone (if using voice mode)
- For microphone input on some systems, `PyAudio` may be required by `speech_recognition`:
  - Windows (easiest):
    - Option A: `pip install pipwin` then `pipwin install pyaudio`
    - Option B: Install a prebuilt wheel from the Unofficial Binaries site
  - macOS: `brew install portaudio` then `pip install pyaudio`
  - Linux (Debian/Ubuntu): `sudo apt install portaudio19-dev` then `pip install pyaudio`

---

## 🚀 Quick Start

### 1) Navigate
```bash
cd 14_JarvisFileManager
```

### 2) Install Dependencies
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3) Run
```powershell
python main.py
```

### CLI Options

| Flag | Default | Description |
|------|---------|-------------|
| `--log` | `logs.txt` | Path to log file |
| `--no-voice` | off | Disable text-to-speech output |
| `--speak-errors` | off | Also speak error messages |
| `--lang` | `auto` | STT language hint (e.g., `en-US`, `hi-IN`, `ur-PK`) |
| `--text` | - | Provide a text command instead of using the mic |
| `--once` | off | Process one command and exit |

---

## 🗣️ Example Commands (EN/HI/UR)

- Urdu: `Desktop پر notes.txt نام کی فائل بناو`
- Urdu: `downloads ڈائریکٹری میں فولڈر بناو`
- Hindi: `downloads के अंदर data नाम का folder बनाओ`
- Hindi: `डाउनलोड फोल्डर के अंदर एक फोल्डर बनाओ`
- English: `delete file test.txt from documents`
- English: `make a new file inside Desktop`
- English: `open folder Projects on desktop`
- Any: `show created`

Notes:
- If no path is provided, it defaults to `Desktop`.
- Commands like “make a folder inside Downloads” create the folder within `~/Downloads`.
- If no name is provided (e.g., “make a folder inside Downloads”), a sensible default is generated.

---

## 📦 What Happens

- **Create**: Creates file/folder at resolved path (parents not auto-created beyond the known base); generates unique default names if unspecified
- **Open**: Opens in OS default app/file explorer
- **Delete**: Removes files or folders (folders recursively)
- **Show**: `show created` lists history from `created_items.json`; `show desktop` lists Desktop contents

---

## 🔎 Live Status & Feedback

- Listening: “🎤 Listening…”
- Understanding: “🧠 Understanding your command…”
- During actions: “✅ Creating …”, “🔄 Opening…”, “🗑️ Deleting…”, “🔄 Processing…”
- Success: Green check with final path
- Errors: Clear red message (optionally spoken)

---

## 🔧 Configuration & Notes

- No `.env` required
- Logs saved at `logs.txt` (change via `--log`)
- Created items index saved to `created_items.json`
- TTS is offline (`pyttsx3`); STT uses Google recognizer by default
- Language detection uses `langdetect`; you can override STT language via `--lang`

---

## 🐛 Troubleshooting

### Microphone not detected / “Voice input unavailable”
- Check OS sound settings and default input device
- Test text mode: `python main.py --text "create file demo.txt on desktop" --once`
- Install PyAudio if required (see Prerequisites)

### Permission or path errors
- “Error: Directory not found”: Ensure the base directory exists (e.g., custom profiles without `Downloads`)
- Try creating on Desktop first to validate permissions

### TTS plays no sound
- Windows: `pyttsx3` uses SAPI5 voices; ensure system voices installed and audio not muted
- macOS: Uses `nsss`; Linux: `espeak`/`espeak-ng` may be required

### STT accuracy or language issues
- Use `--lang hi-IN` or `--lang ur-PK` when speaking Hindi/Urdu
- Speak clearly; reduce background noise

### PowerShell execution quirks
If you see chaining issues, run commands separately:
```powershell
cd 14_JarvisFileManager
python main.py
```

---

## 🌍 Language Coverage

- **English**: create, make, open, delete, show/list/display; directories: Desktop, Downloads, Documents, Pictures, Music, Videos
- **Hindi**: बनाओ/बना दो/खोलो/हटाओ/मिटाओ; फ़ाइल/फ़ोल्डर; डेस्कटॉप/डाउनलोड्स/डॉक्यूमेंट्स
- **Urdu**: بناؤ/بنا دو/کھولو/ڈلیٹ/حذف; فائل/فولڈر; ڈیسک ٹاپ/ڈاؤن لوڈز/دستاویزات

---

## 📁 Project Structure

```
14_JarvisFileManager/
├── main.py               # CLI app (voice + text commands)
├── requirements.txt      # Dependencies
└── README.md             # This file
```

---

## 🔮 Future Enhancements

- Safer delete with recycle-bin integration
- Natural language disambiguation prompts
- Batch operations: “Create three files …”
- Whisper or faster offline multilingual STT

---

## 📝 License

This project is part of the #100DaysOfAI-Agents challenge by Muhammad Sami Asghar Mughal.

---

## 🔄 Version History

- v1.1: Live “Listening/Understanding/Processing” statuses; smarter directory handling; default name generation; expanded multilingual intents
- v1.0: Initial release with voice-controlled file operations and logs


