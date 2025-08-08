## 🤖 VoiceAssistantLite - Day 8 of #100DaysOfAI-Agents

> A minimal CLI-based voice assistant that listens to your voice, recognizes speech in multiple languages, matches your question to a set of FAQs, and answers with spoken audio.

---

## 🎯 Purpose

VoiceAssistantLite lets you ask common questions hands‑free. It records from your microphone, converts speech to text (Google or local Whisper), finds the closest match from a predefined FAQ list using fuzzy search, and replies aloud using text‑to‑speech.

---

## ✨ Features

- **🎤 Voice Input**: Record directly from your microphone
- **🧠 Speech Recognition (STT)**: Choose between
  - Google Web Speech (free via `SpeechRecognition`)
  - Local Whisper (optional install, multilingual and robust)
- **🔎 Smart FAQ Matching**: Fuzzy matching via `rapidfuzz`
- **🔊 Text-to-Speech (TTS)**: Offline TTS using `pyttsx3`
- **🌐 Multilingual**: Configure your language (e.g., `en-US`, `es-ES`, `hi-IN`) or auto‑detect with Whisper
- **📝 Logging**: Log each Q/A to JSONL or CSV for analytics
- **🧩 Modular Codebase**: Clean, extensible structure
- **🤝 OpenAI Assistants API (Optional)**: Ask any question; falls back to local FAQs if API is not configured
- **⏳ Thinking Indicator**: A CLI spinner shows while the assistant processes your request
- **🔁 Continuous Voice Mode**: Press Enter to start hands‑free conversation; stop anytime with Ctrl+C

---

## 🛠️ Tech Stack

- **Python 3.9+**
- `speech_recognition`, `PyAudio` (microphone access)
- `pyttsx3` (offline TTS)
- `rapidfuzz` (fuzzy matching)
- `python-dotenv` (config via `.env`)
- Optional: `openai-whisper` (local Whisper STT) + `ffmpeg`, `openai` (Assistants API)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Working microphone and speakers

### Installation
1) Navigate to the project directory
```bash
cd 08_VoiceAssistantLite
```

2) Create and activate a virtual environment (recommended)
```bash
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS/Linux
```

3) Install dependencies
```bash
pip install -r requirements.txt
```

4) Create a .env file in the project root and configure environment
```env
STT_PROVIDER=google        # google | whisper_local
LANGUAGE=en-US             # e.g., en-US, es-ES, hi-IN; use auto with whisper_local
LOG_ENABLED=true
LOG_FORMAT=jsonl           # jsonl | csv
LOG_FILE=logs/qa_log.jsonl
TTS_RATE=170               # speaking rate (wpm)
```

5) (Optional) Enable local Whisper
```bash
pip install openai-whisper
# Install ffmpeg if missing (Windows example): choco install ffmpeg
```

6) (Optional) Enable OpenAI Assistants API
```bash
pip install openai
# Set your API key in .env
# OPENAI_API_KEY=sk-...
# Optionally set ASSISTANT_ID to reuse an existing assistant, otherwise one is created dynamically.
```

### Run
```bash
python main.py
```

Once running:
- Press Enter on an empty prompt to start **continuous voice mode** (keeps listening and answering until Ctrl+C).
- Or type your question and press Enter for a one‑off response.

---

## 📖 Usage Guide

Example session:
```
🎧 VoiceAssistantLite (Day 8)
Press Enter to start listening, or type a question.
Type 'exit' or 'quit' to stop.

>  [Press Enter]
🎙️  Listening... speak now
🧠 Transcribing (google, en-US)...
📝 You said: What are your support hours?
⠋ Thinking...
🔎 Best match: support hours  (92%)
💬 Answer: Our support is available 24/7 via email and chat.
🔊 Speaking answer...

🎙️  Listening... speak now    # Continuous voice mode keeps going until Ctrl+C
🧠 Transcribing (google, en-US)...
📝 You said: Do you support multiple languages?
⠋ Thinking...
🔎 Best match: Do you support multiple languages?  (88%)
💬 Answer: Yes, we support multiple languages. Voice input works with Google STT or local Whisper.
🔊 Speaking answer...

> exit
👋 Goodbye!
```

### Keyboard shortcuts
- Press `Ctrl+C` to stop continuous voice mode and return to the prompt.
- Type `exit` or `quit` to close the app.

---

## 📁 Project Structure

```
08_VoiceAssistantLite/
├── main.py               # CLI entry point
├── cli.py                # CLI loop and user interaction
├── config.py             # Environment/config management
├── stt_service.py        # Speech-to-text providers (Google, Whisper local)
├── tts_service.py        # Text-to-speech engine
├── faq_matcher.py        # Fuzzy FAQ matcher
├── logger.py             # JSONL/CSV logging
├── assistant_service.py  # OpenAI Assistants API integration (optional)
├── faqs.json             # Sample FAQs (edit to customize)
├── requirements.txt      # Dependencies
├── install.bat           # Windows quick install
├── start.bat             # Windows launcher
├── test_installation.py  # Basic sanity checks
└── README.md             # This file
```

---

## 🔧 Configuration

### Environment Variables (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| `STT_PROVIDER` | `google` or `whisper_local` | `google` |
| `LANGUAGE` | BCP‑47 language code; `auto` in Whisper | `en-US` |
| `LOG_ENABLED` | Enable/disable logging | `true` |
| `LOG_FORMAT` | `jsonl` or `csv` | `jsonl` |
| `LOG_FILE` | Log file path | `logs/qa_log.jsonl` |
| `TTS_RATE` | Speaking words per minute | `170` |
| `OPENAI_API_KEY` | OpenAI API key to enable Assistants API | - |
| `OPENAI_MODEL` | Model used by the assistant | `gpt-4o-mini` |
| `ASSISTANT_ID` | Existing assistant id (optional) | - |
| `ASSISTANT_INSTRUCTIONS` | System prompt for the assistant | Short TTS-friendly replies |

### Editing FAQs
Update `faqs.json` with your own questions, aliases (translations/paraphrases), and answers. The matcher will pick the closest match above a similarity threshold.

### Notes on real‑time information
If you enable the OpenAI Assistants API (by setting `OPENAI_API_KEY`), the assistant can answer general knowledge questions using the model. Answers that require very recent information may depend on the model’s knowledge cut‑off unless browsing is enabled in your own assistant configuration.

---

## 🐛 Troubleshooting

### PyAudio installation (Windows)
- If `pip install pyaudio` fails:
  - Use prebuilt wheels: `https://www.lfd.uci.edu/~gohlke/pythonlibs/`
  - Or: `pip install pipwin && pipwin install pyaudio`

### Microphone not found
- Set a default input device in your OS
- Check permissions and reconnect the device

### Whisper local not working
- Ensure `openai-whisper` and `ffmpeg` are installed
- Set `LANGUAGE=auto` for auto‑detect, or a specific language code

### No answer found
- Add more aliases/translations to `faqs.json`
- Lower the similarity threshold in `config.py` if needed
- Or set up `OPENAI_API_KEY` to let the Assistants API answer

---

## 📄 License

This project is part of the #100DaysOfAI-Agents challenge. MIT licensed.

---

## 🙏 Acknowledgments

- `SpeechRecognition`, `PyAudio` for audio capture & Google STT
- `openai-whisper` for local transcription
- `pyttsx3` for offline TTS
- `rapidfuzz` for fuzzy matching
- `python-dotenv` for configuration


