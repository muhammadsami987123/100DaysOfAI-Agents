# 🤖 JarvisMouseControl - Day 43 of #100DaysOfAI-Agents

<div align="center">

![JarvisMouseControl Badge](https://img.shields.io/badge/JarvisMouseControl-Day%2043-blue?style=for-the-badge&logo=robot&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8%2B-green?style=for-the-badge&logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT-orange?style=for-the-badge&logo=openai&logoColor=white)
![Multilingual](https://img.shields.io/badge/Multilingual-EN%20%7C%20UR%20%7C%20HI-purple?style=for-the-badge&logo=translate&logoColor=white)

**Voice-controlled mouse automation agent with local language support (Urdu, Hindi, English). Helps people with limited mobility, visual focus, or multitasking needs to control their computer mouse using voice commands.**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🌍 Multilingual Support](#-multilingual-support) • [🛠️ Installation](#-installation) • [📖 Usage](#-usage) • [🏗️ Architecture](#-architecture) • [⚙️ Configuration](#-configuration) • [🔧 Improvements](#-improvements) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is JarvisMouseControl?

JarvisMouseControl is an intelligent voice-controlled mouse automation agent that enables hands-free computer control through natural language voice commands. It supports multiple languages (English, Urdu, Hindi) and uses AI-powered natural language processing to understand and execute mouse actions.

### 🆕 Latest Improvements

- **🔧 Fixed Microphone Detection**: Improved microphone detection using proven methods from `voice_working.py`
- **🔄 Dynamic Mode Switching**: Switch between voice and text modes on the fly with the `voice` command
- **🛠️ Better Error Handling**: Enhanced error handling and fallback mechanisms
- **📱 Multiple Entry Points**: Various ways to run the agent for different use cases
- **🔍 Enhanced Troubleshooting**: Better diagnostic tools and error messages

### 🌟 Key Highlights

- **🎤 Voice Control**: Hands-free mouse control using voice commands
- **🌍 Multilingual Support**: English, Urdu (اردو), and Hindi (हिंदी)
- **🤖 AI-Powered**: OpenAI integration for intelligent command understanding
- **🛡️ Safety Features**: Built-in safety bounds and failsafe mechanisms
- **⌨️ Text Mode**: Alternative text input for environments without voice
- **🔊 Voice Feedback**: Optional text-to-speech confirmation of actions
- **⚡ Real-time**: Instant command recognition and execution

## 🧩 How This Solves a Real-World Problem

Many users struggle with traditional mouse control due to:

- **Limited Mobility**: Physical disabilities or injuries affecting hand movement
- **Visual Focus**: Need to keep eyes on screen while controlling mouse
- **Multitasking**: Hands busy with other tasks while using computer
- **Language Barriers**: Non-English speakers needing voice control in their native language
- **Accessibility**: Elderly users or those with motor skill challenges

JarvisMouseControl addresses these challenges by providing:

- **Hands-free Operation**: Complete mouse control through voice commands
- **Multilingual Support**: Native language support for Urdu and Hindi speakers
- **Intelligent Understanding**: AI-powered natural language processing
- **Safety First**: Built-in safety mechanisms to prevent accidental actions
- **Easy Setup**: Simple installation and configuration process

---

## 🚀 Quick Start

### 1) Navigate to Project
```bash
cd 43_JarvisMouseControl
```

### 2) Install Dependencies
```bash
# Windows
install.bat

# Or manually
pip install -r requirements.txt
```

### 3) Set OpenAI API Key (Optional but Recommended)
```bash
# Windows
set OPENAI_API_KEY=sk-your_api_key_here

# macOS/Linux
export OPENAI_API_KEY=sk-your_api_key_here
```

### 4) Run the Agent

#### Main Application
```bash
# English mode (default)
python main.py --language en

# Urdu mode
python main.py --language ur

# Hindi mode
python main.py --language hi

# Text mode only (no voice)
python main.py --no-voice

# Test components
python main.py --test
```

#### Alternative Entry Points
```bash
# Working voice demo (recommended for testing)
python voice_working.py

# Simple voice test
python test_voice_simple.py

# Simple startup with dependency checking
python start.py

# Run as administrator (Windows)
run_as_admin.bat

# Interactive demo
python demo.py
```

---

## 📖 Features

### Core Functionality
- ✅ **Voice Command Recognition**: Real-time speech-to-text processing
- ✅ **Mouse Automation**: Complete mouse control (move, click, scroll, drag)
- ✅ **Multilingual Support**: English, Urdu, and Hindi voice commands
- ✅ **AI-Powered Understanding**: OpenAI integration for natural language processing
- ✅ **Safety Features**: Screen bounds checking and failsafe mechanisms
- ✅ **Text Mode**: Alternative input method for voice-free environments
- ✅ **Voice Feedback**: Optional text-to-speech confirmation of actions
- ✅ **Smart Microphone Detection**: Automatic detection of working microphones
- ✅ **Dynamic Mode Switching**: Switch between voice and text modes on the fly

### Supported Actions
- **Movement**: Move cursor up, down, left, right with distance control
- **Clicking**: Left click, double click, right click
- **Scrolling**: Scroll up and down with configurable amounts
- **Dragging**: Drag and drop functionality
- **Control**: Start, stop, and quit the agent

### Language Support
- **English**: "move up", "click", "scroll down", "double click"
- **Urdu**: "اوپر جاؤ", "کلک کرو", "نیچے سکرول کرو", "دو بار کلک کرو"
- **Hindi**: "ऊपर जाओ", "क्लिक करो", "नीचे स्क्रॉल करो", "दो बार क्लिक करो"

---

## 🌍 Multilingual Support

### English Commands
```
move up          - Move cursor up
move down        - Move cursor down
move left        - Move cursor left
move right       - Move cursor right
click            - Left click
double click     - Double click
right click      - Right click
scroll up        - Scroll up
scroll down      - Scroll down
drag             - Drag and drop
stop             - Stop the agent
```

### Urdu Commands (اردو)
```
اوپر جاؤ         - Move cursor up
نیچے جاؤ         - Move cursor down
بائیں جاؤ        - Move cursor left
دائیں جاؤ        - Move cursor right
کلک کرو          - Left click
دو بار کلک کرو   - Double click
دائیں کلک کرو    - Right click
اوپر سکرول کرو   - Scroll up
نیچے سکرول کرو   - Scroll down
کھینچو           - Drag and drop
رکو              - Stop the agent
```

### Hindi Commands (हिंदी)
```
ऊपर जाओ          - Move cursor up
नीचे जाओ         - Move cursor down
बाएं जाओ         - Move cursor left
दाएं जाओ         - Move cursor right
क्लिक करो         - Left click
दो बार क्लिक करो  - Double click
दाएं क्लिक करो    - Right click
ऊपर स्क्रॉल करो   - Scroll up
नीचे स्क्रॉल करो  - Scroll down
खींचो            - Drag and drop
रुको             - Stop the agent
```

---

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Microphone (for voice input)
- Speakers (for voice feedback)
- Internet connection (for OpenAI API)

### Step-by-Step Installation

1. **Clone or Download the Project**
   ```bash
   git clone <repository-url>
   cd 43_JarvisMouseControl
   ```

2. **Install Python Dependencies**
   ```bash
   # Windows
   install.bat
   
   # Or manually
   pip install -r requirements.txt
   ```

3. **Set Up OpenAI API Key (Optional)**
   ```bash
   # Create .env file
   echo OPENAI_API_KEY=sk-your_api_key_here > .env
   
   # Or set environment variable
   set OPENAI_API_KEY=sk-your_api_key_here  # Windows
   export OPENAI_API_KEY=sk-your_api_key_here  # macOS/Linux
   ```

4. **Test Installation**
   ```bash
   python main.py --test
   ```

---

## 📖 Usage

### Basic Usage

#### Voice Mode (Default)
```bash
# Start with English
python main.py --language en

# Start with Urdu
python main.py --language ur

# Start with Hindi
python main.py --language hi
```

#### Text Mode
```bash
# Text input only (no voice)
python main.py --no-voice

# No voice feedback
python main.py --no-tts
```

### Command Line Options

```bash
python main.py [OPTIONS]

Options:
  -l, --language {en,ur,hi}  Language for voice commands (default: en)
  --no-voice                 Disable voice input (text mode only)
  --no-tts                   Disable text-to-speech feedback
  --test                     Test components and exit
  --debug                    Enable debug output
  -h, --help                 Show help message
```

### Interactive Commands

While running, you can use these text commands:

- `help` - Show available commands
- `lang <code>` - Change language (en/ur/hi)
- `voice` - Try to enable voice mode (if disabled)
- `quit` / `exit` - Exit the program

### Voice Commands

Simply speak any of the supported commands in your selected language:

**English Examples:**
- "Move up" - Moves cursor up
- "Click here" - Performs left click
- "Scroll down" - Scrolls down
- "Double click" - Performs double click

**Urdu Examples:**
- "اوپر جاؤ" - Moves cursor up
- "کلک کرو" - Performs left click
- "نیچے سکرول کرو" - Scrolls down
- "دو بار کلک کرو" - Performs double click

**Hindi Examples:**
- "ऊपर जाओ" - Moves cursor up
- "क्लिक करो" - Performs left click
- "नीचे स्क्रॉल करो" - Scrolls down
- "दो बार क्लिक करो" - Performs double click

---

## 🏗️ Architecture

### Project Structure
```
43_JarvisMouseControl/
├── 📄 main.py                   # Main entry point and CLI interface
├── ⚙️ config.py                 # Configuration and settings management
├── 🎤 voice_handler.py          # Speech recognition and TTS
├── 🖱️ mouse_controller.py       # Mouse automation using pyautogui
├── 📄 voice_working.py          # Working voice demo with proven microphone detection
├── 📄 test_voice_simple.py      # Simple voice test utility
├── 📄 fix_mic_permissions.py    # Microphone permission fix utility
├── 📄 start.py                  # Simple startup script
├── 📄 demo.py                   # Interactive demo script
├── 📄 run_as_admin.bat          # Run as administrator script
├── 📄 IMPROVEMENTS.md           # Documentation of improvements made
├── 📁 utils/
│   ├── 📄 command_parser.py     # Natural language processing
│   └── 📄 translations.json     # Multilingual command mappings
├── 📄 requirements.txt          # Python dependencies
├── 📄 install.bat              # Windows installation script
├── 📄 start.bat                # Windows quick start script
└── 📄 README.md                # This file
```

### Component Overview

1. **Main Controller** (`main.py`)
   - CLI interface and argument parsing
   - Component orchestration
   - Main application loop

2. **Configuration** (`config.py`)
   - Settings and constants
   - Language configurations
   - API key management

3. **Voice Handler** (`voice_handler.py`)
   - Speech recognition using Google Speech API
   - Text-to-speech using pyttsx3
   - Microphone and speaker management

4. **Mouse Controller** (`mouse_controller.py`)
   - Mouse automation using pyautogui
   - Safety bounds checking
   - Action execution and feedback

5. **Command Parser** (`utils/command_parser.py`)
   - Natural language processing
   - OpenAI integration for advanced understanding
   - Local pattern matching fallback

6. **Translations** (`utils/translations.json`)
   - Multilingual command mappings
   - Feedback messages in all languages
   - Command patterns and modifiers

7. **Voice Demo** (`voice_working.py`)
   - Working voice demo with proven microphone detection
   - Alternative entry point for testing voice functionality
   - Simplified interface for troubleshooting

8. **Utilities**
   - `test_voice_simple.py` - Simple voice test utility
   - `fix_mic_permissions.py` - Microphone permission fix utility
   - `start.py` - Simple startup script with dependency checking
   - `demo.py` - Interactive demo script
   - `run_as_admin.bat` - Run as administrator script for Windows

9. **Documentation**
   - `IMPROVEMENTS.md` - Detailed documentation of improvements made
   - Enhanced README with better troubleshooting and usage examples

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file or set environment variables:

```env
# OpenAI API (optional but recommended)
OPENAI_API_KEY=sk-your_api_key_here
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.3
OPENAI_MAX_TOKENS=500

# Voice Settings
VOICE_ENABLED=true
VOICE_TIMEOUT=5.0
VOICE_ENERGY_THRESHOLD=300

# Text-to-Speech Settings
TTS_ENABLED=true
TTS_RATE=180
TTS_VOLUME=0.8

# Language Settings
DEFAULT_LANGUAGE=en

# Mouse Settings
MOUSE_SPEED=1.0
MOUSE_DURATION=0.5
SCROLL_AMOUNT=3
CLICK_DELAY=0.1

# Safety Settings
ENABLE_SAFETY=true
```

### Configuration Options

| Setting | Description | Default | Options |
|---------|-------------|---------|---------|
| `DEFAULT_LANGUAGE` | Default language | `en` | `en`, `ur`, `hi` |
| `VOICE_ENABLED` | Enable voice input | `true` | `true`, `false` |
| `TTS_ENABLED` | Enable voice feedback | `true` | `true`, `false` |
| `MOUSE_SPEED` | Mouse movement speed | `1.0` | `0.1` - `2.0` |
| `SCROLL_AMOUNT` | Scroll distance | `3` | `1` - `10` |
| `ENABLE_SAFETY` | Enable safety bounds | `true` | `true`, `false` |

---

## 🧪 Testing

### Test Components
```bash
python main.py --test
```

### Working Voice Demo
```bash
# Test voice functionality with proven microphone detection
python voice_working.py

# Simple voice test
python test_voice_simple.py
```

### Test Voice Recognition
```bash
# Test microphone
python -c "from voice_handler import VoiceHandler; VoiceHandler().test_microphone()"

# Test speakers
python -c "from voice_handler import VoiceHandler; VoiceHandler().test_speakers()"
```

### Test Mouse Control
```bash
# Test mouse controller
python -c "from mouse_controller import MouseController; MouseController().get_current_position()"
```

---

## 🐛 Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "Microphone not found" | No microphone detected | Check microphone connection and permissions |
| "Speech recognition error" | Network or API issue | Check internet connection and try again |
| "Mouse control failed" | PyAutoGUI issue | Check screen resolution and permissions |
| "OpenAI API error" | Invalid API key | Verify API key and account status |
| "Language not supported" | Invalid language code | Use `en`, `ur`, or `hi` |
| "Voice mode not working" | Microphone permission issue | Run `python voice_working.py` to test |

### Quick Fixes

```bash
# Test voice functionality
python voice_working.py

# Test simple voice recognition
python test_voice_simple.py

# Fix microphone permissions (Windows)
python fix_mic_permissions.py

# Run as administrator
run_as_admin.bat

# Check all components
python main.py --test
```

### Debug Mode
```bash
python main.py --debug
```

### Voice Issues
- Ensure microphone is working and not muted
- Check microphone permissions in system settings
- Try different microphone if available
- Adjust `VOICE_ENERGY_THRESHOLD` in config
- Run `python voice_working.py` to test voice functionality
- Try running as administrator on Windows
- Check Windows microphone privacy settings

### Mouse Issues
- Ensure screen is not locked
- Check if other applications are blocking mouse control
- Verify screen resolution settings
- Try running as administrator (Windows)

---

## 🔧 Improvements

### Latest Updates

The JarvisMouseControl agent has been significantly improved with the following enhancements:

- **🔧 Fixed Microphone Detection**: Improved microphone detection using proven methods from `voice_working.py`
- **🔄 Dynamic Mode Switching**: Switch between voice and text modes on the fly with the `voice` command
- **🛠️ Better Error Handling**: Enhanced error handling and fallback mechanisms
- **📱 Multiple Entry Points**: Various ways to run the agent for different use cases
- **🔍 Enhanced Troubleshooting**: Better diagnostic tools and error messages

### Detailed Improvements

For a complete list of improvements, bug fixes, and technical details, see [IMPROVEMENTS.md](IMPROVEMENTS.md).

### Quick Test

```bash
# Test the improved voice functionality
python voice_working.py

# Run the interactive demo
python demo.py

# Test all components
python main.py --test
```

---

## 🤝 Contributing

### Adding New Languages

1. **Update `config.py`**:
   ```python
   SUPPORTED_LANGUAGES = ["en", "ur", "hi", "new_lang"]
   LANGUAGE_NAMES = {
       "en": "English",
       "ur": "Urdu", 
       "hi": "Hindi",
       "new_lang": "New Language"
   }
   ```

2. **Add translations to `utils/translations.json`**:
   ```json
   "new_lang": {
       "move_up": ["command1", "command2"],
       "click": ["click_command"]
   }
   ```

3. **Update voice handler language codes**:
   ```python
   language_codes = {
       "en": "en-US",
       "ur": "ur-PK",
       "hi": "hi-IN",
       "new_lang": "new_lang-COUNTRY"
   }
   ```

### Adding New Commands

1. **Add to `utils/translations.json`**:
   ```json
   "new_action": {
       "en": ["english command"],
       "ur": ["urdu command"],
       "hi": ["hindi command"]
   }
   ```

2. **Add to `mouse_controller.py`**:
   ```python
   elif action == "new_action":
       return self._new_action()
   ```

3. **Update command parser patterns**:
   ```python
   COMMAND_PATTERNS = {
       "en": {
           "new_action": ["command1", "command2"]
       }
   }
   ```

---

## 📄 License

This project is part of the #100DaysOfAI-Agents challenge and is available under the MIT License.

---

## 🙏 Acknowledgments

- **OpenAI** for GPT integration and natural language processing
- **Google** for Speech Recognition API
- **PyAutoGUI** for mouse automation capabilities
- **SpeechRecognition** and **pyttsx3** for voice handling
- **#100DaysOfAI-Agents** community for inspiration and support

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Run `python main.py --test` to verify installation
3. Check the [Issues](https://github.com/your-repo/issues) page
4. Create a new issue with detailed information

---

<div align="center">

**🤖 JarvisMouseControl - Making Computer Control Accessible Through Voice**

*Day 43 of #100DaysOfAI-Agents Challenge*

[⬆️ Back to Top](#-jarvismousecontrol---day-43-of-100daysofaia-agents)

</div>
