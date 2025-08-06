# 🤖 VoiceNoteAgent - Day 6 of #100DaysOfAI-Agents

> **📝 Note**: This is the CLI-only version of VoiceNoteAgent. All web interface components have been removed to focus on command-line functionality.

A powerful voice note-taking agent that records, transcribes, and manages voice notes locally. Perfect for capturing ideas, reminders, and thoughts on the go without requiring internet connectivity.

## 🎯 Purpose

VoiceNoteAgent allows users to quickly create, transcribe, and store voice notes using natural language. Whether you're brainstorming ideas, setting quick reminders, or capturing thoughts on the go, this agent converts your voice into text and saves it with a timestamp — all without internet dependency.

## 🔧 Key Features

- **🎤 Voice-to-Text Transcription** using speech_recognition
- **📁 Local File Saving** as .txt or .json with timestamps
- **🔊 Text-to-Speech Playback** of saved notes
- **🧠 GPT Integration** (Optional): Summarize long notes or auto-title them
- **💻 100% Offline-capable** (no external APIs required)
- **🔍 Search and Filter** capabilities
- **📊 Statistics and Analytics** for your notes
- **🎨 Beautiful CLI Interface** with colored output

## 🛠️ Tech Stack

- **Python 3.7+**
- **speech_recognition** - Voice transcription
- **pyttsx3** - Text-to-Speech engine
- **PyAudio** - Audio input/output
- **colorama** - Cross-platform colored output
- **pocketsphinx** - Offline speech recognition (optional)

## 🚀 Quick Start

### Prerequisites

1. **Python 3.7 or higher**
2. **Working microphone**
3. **Speakers or headphones** (for TTS playback)

### Installation

1. **Clone or download the VoiceNoteAgent files**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **For Windows users** (if PyAudio fails):
   ```bash
   pip install pipwin
   pipwin install pyaudio
   ```

4. **For macOS users:**
   ```bash
   brew install portaudio
   pip install pyaudio
   ```

5. **For Linux users:**
   ```bash
   sudo apt-get install python3-pyaudio portaudio19-dev
   pip install pyaudio
   ```

### Running the Agent

```bash
python main.py
```

## 📖 Usage Guide

### Basic Commands

| Command | Description | Example |
|---------|-------------|---------|
| `record` / `r` / `new` | Record a new voice note | `record` |
| `list` / `l` / `show` | List all voice notes | `list` |
| `play <id>` | Play a note using TTS | `play 1` |
| `show <id>` | Display full note content | `show 2` |
| `search <term>` | Search notes by content | `search meeting` |
| `delete <id>` | Delete a note | `delete 3` |
| `stats` | Show statistics | `stats` |
| `help` / `h` / `?` | Show help | `help` |
| `quit` / `q` / `exit` | Exit the application | `quit` |

### Example Usage

```bash
🎙️  VoiceNoteAgent> record
⏱️  Enter recording duration in seconds (default 10): 15
🎤 Recording... Speak now! (Press Ctrl+C to stop early)
Recording for 15 seconds...
✅ Recording completed!
🔄 Transcribing audio...
✅ Transcription successful!
✅ Transcription: Remember to review the AI Agents repo before Sunday
📝 Enter a title for this note (or press Enter for auto-title): AI Review Reminder
✅ Note saved successfully!
📝 Note ID: 1
📁 TXT file: voice_notes/note_1_20240115_143022.txt

🎙️  VoiceNoteAgent> list
📝 Voice Notes (1 of 1):
--------------------------------------------------------------------------------
[1] AI Review Reminder
   📅 2024-01-15 14:30:22 | 📊 8 words
   📝 Remember to review the AI Agents repo before Sunday

🎙️  VoiceNoteAgent> play 1
🔊 Playing note #1: AI Review Reminder
🔊 Speaking: Remember to review the AI Agents repo before Sunday...
✅ Speech playback completed!

🎙️  VoiceNoteAgent> search AI
🔍 Found 1 matching notes:
--------------------------------------------------------------------------------
[1] AI Review Reminder
   📅 2024-01-15 14:30:22 | 📊 8 words
   📝 Remember to review the AI Agents repo before Sunday
```

## 📁 File Structure

```
06_VoiceNoteAgent/
├── main.py              # Main application
├── config.py            # Configuration and setup
├── test_agent.py        # Test suite
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── voice_notes.json    # Notes database (created automatically)
└── voice_notes/        # Individual TXT files (created automatically)
    ├── note_1_20240115_143022.txt
    ├── note_2_20240115_150045.txt
    └── ...
```

## 🔧 Configuration

### Speech Recognition

The agent supports multiple speech recognition engines:

1. **Google Speech Recognition** (requires internet)
   - Higher accuracy
   - Supports multiple languages
   - Requires internet connection

2. **Sphinx** (offline)
   - Works without internet
   - Lower accuracy
   - English only
   - Requires `pocketsphinx` package

The agent automatically tries both methods and uses the first successful one.

### Text-to-Speech

- **Windows**: Uses built-in SAPI voices
- **macOS**: Uses built-in NSSpeechSynthesizer
- **Linux**: Requires espeak or festival

### File Storage

- **JSON Database**: `voice_notes.json` - Contains all note metadata
- **TXT Files**: `voice_notes/` directory - Individual note files with full content
- **Automatic Backup**: Both formats are maintained simultaneously

## 🧪 Testing

Run the test suite to verify functionality:

```bash
python test_agent.py
```

Or run a system check:

```bash
python config.py check
```

## 💡 Tips for Best Results

### Recording
- **Speak clearly** and at a normal pace
- **Minimize background noise**
- **Use 10-30 second recordings** for best accuracy
- **Test with short phrases** first
- **Ensure microphone is properly connected**

### Transcription
- **Google Speech Recognition** works best with internet
- **Sphinx** is good for offline use but less accurate
- **Clear pronunciation** improves accuracy
- **Avoid overlapping speech**

### Playback
- **Adjust system volume** before playing notes
- **Use headphones** for private listening
- **TTS quality** varies by operating system

## 🔍 Advanced Features

### Search Capabilities
- Search by note content
- Search by note title
- Case-insensitive matching
- Partial word matching

### Statistics
- Total number of notes
- Total word count
- Average words per note
- Notes by date
- Usage patterns

### File Management
- Automatic timestamp organization
- Individual TXT file export
- JSON database for programmatic access
- Automatic cleanup on deletion

## 🛠️ Troubleshooting

### Common Issues

1. **"Microphone not available"**
   - Check microphone connection
   - Verify system permissions
   - Test microphone in system settings

2. **"PyAudio installation failed"**
   - Windows: Use `pipwin install pyaudio`
   - macOS: Install portaudio first
   - Linux: Install system dependencies

3. **"Speech recognition not working"**
   - Check internet connection (for Google)
   - Install pocketsphinx for offline use
   - Verify microphone is working

4. **"TTS not working"**
   - Windows: Check SAPI voices
   - macOS: Check NSSpeechSynthesizer
   - Linux: Install espeak or festival

### System Requirements

- **Python**: 3.7 or higher
- **Memory**: 100MB RAM
- **Storage**: 10MB for application + note storage
- **Audio**: Working microphone and speakers
- **OS**: Windows 10+, macOS 10.14+, or Linux

## 🔮 Future Enhancements

- **Voice Commands**: "Hey Jarvis, take a note"
- **Hotkey Support**: Ctrl+Alt+V to start recording
- **Cloud Sync**: Optional cloud backup
- **Voice Cloning**: Custom TTS voices
- **Note Categories**: Organize by tags/categories
- **Export Options**: PDF, Word, Markdown
- **Voice Summary**: Daily/weekly note summaries
- **Integration**: Connect with other AI agents

## 🤝 Contributing

This is part of the #100DaysOfAI-Agents challenge. Feel free to:

- Report bugs
- Suggest features
- Submit improvements
- Share your voice notes (anonymously)

## 📄 License

This project is part of the #100DaysOfAI-Agents challenge by Muhammad Sami Asghar Mughal.

## 🙏 Acknowledgments

- **SpeechRecognition** library for voice transcription
- **pyttsx3** for text-to-speech functionality
- **colorama** for beautiful CLI output
- **OpenAI** for inspiration in AI agent development

---

**🎉 Ready to capture your thoughts with voice!**

Run `python main.py` to start your voice note-taking journey. 