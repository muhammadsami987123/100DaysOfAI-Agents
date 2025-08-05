# 🌍 TranslatorAgent - Day 5 of #100DaysOfAI-Agents

<div align="center">

![TranslatorAgent](https://img.shields.io/badge/TranslatorAgent-AI%20Powered-blue?style=for-the-badge&logo=openai)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20Framework-red?style=for-the-badge&logo=fastapi)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT%20API-purple?style=for-the-badge&logo=openai)

**Instant translation with AI-powered accuracy and voice capabilities**

[Features](#-features) • [Quick Start](#-quick-start) • [Usage](#-usage) • [Languages](#-languages) • [API](#-api) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [🌍 Usage](#-usage)
- [🗣️ Voice Features](#-voice-features)
- [🛠️ Configuration](#-configuration)
- [🔧 API Reference](#-api-reference)
- [📁 Project Structure](#-project-structure)
- [🎯 Use Cases](#-use-cases)
- [🔒 Security & Privacy](#-security--privacy)
- [🐛 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🌟 Overview

TranslatorAgent is an intelligent translation tool that combines OpenAI's GPT technology with traditional translation APIs to provide accurate, context-aware translations. Whether you need to translate text, speech, or documents, this tool adapts to your needs with smart language detection and multiple interface options.

### Key Benefits

- **⚡ Speed**: Instant translations with AI-powered accuracy
- **🎯 Accuracy**: Context-aware translations that preserve meaning
- **🗣️ Voice Support**: Speech-to-text and text-to-speech capabilities
- **🌍 Multi-Language**: Support for 100+ languages
- **💡 Intelligence**: Smart language detection and context preservation
- **🔄 Multiple Interfaces**: Web UI and CLI for different use cases

---

## ✨ Features

### 🤖 AI-Powered Translation
- **OpenAI GPT Integration**: Uses GPT-4o-mini for context-aware translations
- **Smart Language Detection**: Automatically detects source language
- **Context Preservation**: Maintains meaning and tone across languages
- **Professional Polish**: Generates natural, fluent translations

### 🌍 Language Support
- **100+ Languages**: Comprehensive language coverage
- **Bidirectional Translation**: Translate between any supported language pair
- **Language Detection**: Automatic source language identification
- **Regional Variants**: Support for regional language variations

### 🗣️ Voice Capabilities
- **Speech-to-Text**: Speak your text for translation
- **Text-to-Speech**: Hear translations spoken aloud
- **Voice Control**: Toggle voice features on/off
- **Multiple TTS Engines**: Cross-platform voice support

### 🖥️ Multiple Interfaces
- **Web Interface**: Beautiful, responsive UI with real-time translation
- **Terminal Interface**: Command-line tool for quick translations
- **Quick Mode**: Generate translations directly from command line arguments

### 🛠️ Advanced Features
- **Translation History**: Track and reuse previous translations
- **Export Options**: Copy to clipboard or download as text files
- **Language Preferences**: Save your preferred language pairs
- **Real-time Translation**: See translations as you type
- **Batch Translation**: Translate multiple texts at once

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (3.9+ recommended)
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))
- **Internet Connection** (for API calls)

### Installation

1. **Navigate to the project directory:**
   ```bash
   cd 05_TranslatorAgent
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key:**

   **Option A: Environment Variable (Recommended)**
   ```bash
   # Windows (Command Prompt)
   set OPENAI_API_KEY=your_api_key_here
   
   # Windows (PowerShell)
   $env:OPENAI_API_KEY="your_api_key_here"
   
   # Linux/Mac
   export OPENAI_API_KEY=your_api_key_here
   ```

   **Option B: .env file**
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

### First Run

#### Web Interface (Recommended)
```bash
python main.py --web
```
Then open your browser to `http://127.0.0.1:8005`

#### Terminal Interface
```bash
python main.py --terminal
```

#### Quick Translation
```bash
python main.py --quick "Hello, how are you?" --target es
```

---

## 🌍 Usage

### Web Interface

1. **Start the web server:**
   ```bash
   python main.py --web
   ```

2. **Open your browser** to `http://127.0.0.1:8005`

3. **Translate your text:**
   - Enter text in the source language
   - Select target language from dropdown
   - Enable voice features if desired
   - Click "Translate" or press Enter

4. **Review and use:**
   - View the translation with pronunciation
   - Click "Copy Translation" to copy to clipboard
   - Use "Download" to save as text file
   - Click "Speak" to hear the translation

### Terminal Interface

```bash
# Start terminal mode
python main.py --terminal

# Available commands:
🌍 TranslatorAgent> translate "Hello world" to Spanish
🌍 TranslatorAgent> detect "Bonjour le monde"
🌍 TranslatorAgent> languages
🌍 TranslatorAgent> history
🌍 TranslatorAgent> help
🌍 TranslatorAgent> quit
```

### Quick Commands

```bash
# Basic translation
python main.py --quick "Hello, how are you?" --target es

# Translation with specific source language
python main.py --quick "Bonjour le monde" --source fr --target en

# Language detection
python main.py --detect "Hola mundo"

# Voice translation
python main.py --voice "Hello world" --target fr
```

### Advanced Usage

```bash
# Custom port
python main.py --web --port 8006

# Custom host
python main.py --web --host 0.0.0.0

# Quick translation with voice
python main.py --quick "Good morning" --target ja --voice
```

---

## 🗣️ Voice Features

### Speech-to-Text
- **Microphone Input**: Speak your text for translation
- **Language Detection**: Automatically detects spoken language
- **Noise Reduction**: Filters background noise for better accuracy
- **Real-time Processing**: See transcription as you speak

### Text-to-Speech
- **Natural Voice**: Hear translations in natural-sounding voice
- **Multiple Voices**: Different voices for different languages
- **Speed Control**: Adjust speech rate for better comprehension
- **Pronunciation Guide**: Clear pronunciation of translated text

### Voice Controls
- **Enable/Disable**: Toggle voice features on/off
- **Stop Speech**: Halt ongoing speech playback
- **Voice Settings**: Adjust volume, speed, and voice selection
- **Keyboard Shortcuts**: Quick voice control with keyboard

---

## 🛠️ Configuration

### Customizing Defaults

Edit `config.py` to customize:

```python
class TranslatorConfig:
    # Default translation settings
    DEFAULT_SOURCE_LANG = "auto"
    DEFAULT_TARGET_LANG = "en"
    
    # Voice settings
    VOICE_ENABLED = True
    SPEECH_RATE = 150
    VOICE_VOLUME = 0.8
    
    # GPT settings
    MAX_TOKENS = 500
    TEMPERATURE = 0.3
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `TRANSLATOR_PORT` | Web server port | 8005 |
| `TRANSLATOR_HOST` | Web server host | 127.0.0.1 |
| `VOICE_ENABLED` | Enable voice features | true |
| `SPEECH_RATE` | Text-to-speech rate | 150 |

---

## 🔧 API Reference

### Web API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main web interface |
| `/api/translate` | POST | Translate text |
| `/api/detect` | POST | Detect language |
| `/api/languages` | GET | Get supported languages |
| `/api/history` | GET | Get translation history |
| `/api/voice/speak` | POST | Text-to-speech |
| `/api/voice/listen` | POST | Speech-to-text |
| `/api/health` | GET | Health check |

### Request Format

```json
{
    "text": "Hello, how are you?",
    "source_lang": "en",
    "target_lang": "es",
    "voice_enabled": true
}
```

### Response Format

```json
{
    "success": true,
    "translation": "Hola, ¿cómo estás?",
    "source_lang": "en",
    "target_lang": "es",
    "pronunciation": "OH-lah, KOH-moh ehs-TAHS",
    "confidence": 0.95
}
```

### Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--web` | Start web interface | False |
| `--terminal` | Start terminal interface | False |
| `--quick` | Quick translation | None |
| `--detect` | Language detection | None |
| `--voice` | Enable voice features | False |
| `--source` | Source language | auto |
| `--target` | Target language | en |
| `--host` | Web server host | 127.0.0.1 |
| `--port` | Web server port | 8005 |

---

## 📁 Project Structure

```
05_TranslatorAgent/
├── 📄 main.py                 # Main entry point and CLI
├── 🤖 translator_agent.py     # Core TranslatorAgent class
├── 🌐 web_app.py              # FastAPI web application
├── ⚙️ config.py               # Configuration and language settings
├── 🗣️ voice_service.py        # Speech-to-text and text-to-speech
├── 🌍 language_service.py     # Language detection and support
├── 📋 requirements.txt        # Python dependencies
├── 📖 README.md              # This documentation
├── 🧪 test_*.py              # Test scripts
├── 📁 templates/             # HTML templates
│   └── 📄 index.html        # Main web interface
└── 📁 static/               # Static files
    ├── 🎨 css/
    │   └── style.css        # CSS styles
    └── ⚡ js/
        └── app.js           # JavaScript functionality
```

### Key Files

- **`main.py`**: Entry point with CLI argument parsing
- **`translator_agent.py`**: Core AI translation logic
- **`web_app.py`**: FastAPI web server implementation
- **`config.py`**: Configuration and language settings
- **`voice_service.py`**: Speech-to-text and text-to-speech functionality
- **`language_service.py`**: Language detection and support
- **`templates/index.html`**: Main web interface template
- **`static/css/style.css`**: Modern, responsive styling
- **`static/js/app.js`**: Interactive web functionality

---

## 🎯 Use Cases

### 💼 Business Communication

| Scenario | Languages | Example |
|----------|-----------|---------|
| **International Meetings** | EN ↔ ES, FR, DE, JA | Translate meeting notes |
| **Customer Support** | EN ↔ ZH, AR, RU | Help international customers |
| **Document Translation** | EN ↔ FR, DE, ES | Translate business documents |
| **Email Communication** | EN ↔ JA, KO, ZH | International email correspondence |

### 🎓 Educational

| Scenario | Languages | Example |
|----------|-----------|---------|
| **Language Learning** | EN ↔ ES, FR, DE | Practice vocabulary |
| **Academic Research** | EN ↔ ZH, JA, KO | Read foreign research papers |
| **Study Materials** | EN ↔ AR, RU, HI | Translate educational content |
| **Student Communication** | EN ↔ ES, FR, DE | Help international students |

### 🌍 Travel & Tourism

| Scenario | Languages | Example |
|----------|-----------|---------|
| **Travel Planning** | EN ↔ ES, FR, IT | Translate travel information |
| **Restaurant Menus** | EN ↔ JA, ZH, TH | Understand local cuisine |
| **Directions** | EN ↔ AR, RU, HI | Navigate foreign cities |
| **Cultural Exchange** | EN ↔ ES, FR, DE | Communicate with locals |

### 📱 Personal Communication

| Scenario | Languages | Example |
|----------|-----------|---------|
| **Social Media** | EN ↔ ES, FR, DE | Connect with international friends |
| **Family Communication** | EN ↔ ZH, AR, RU | Communicate with family abroad |
| **Online Dating** | EN ↔ ES, FR, JA | Connect with people worldwide |
| **Gaming** | EN ↔ JA, KO, ZH | Understand foreign games |

---

## 🔒 Security & Privacy

### Data Protection

- **🔐 API Key Security**: API keys are stored securely using environment variables
- **📝 No Permanent Storage**: Translation content is not stored permanently
- **🔒 Encrypted Communication**: All communication with OpenAI is encrypted
- **👤 Privacy First**: No personal data is logged or stored

### Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** for sensitive data
3. **Regularly rotate** your OpenAI API keys
4. **Monitor API usage** to control costs
5. **Review translations** for accuracy before use

### API Usage

- **Cost Control**: Each translation uses approximately 50-100 tokens
- **Rate Limits**: Respect OpenAI's rate limits
- **Error Handling**: Graceful handling of API failures
- **Fallback Options**: Terminal mode available if web interface fails

---

## 🐛 Troubleshooting

### Common Issues

#### ❌ "OpenAI API key not found"
**Solution:**
```bash
# Check if API key is set
echo $OPENAI_API_KEY

# Set API key (Linux/Mac)
export OPENAI_API_KEY=your_api_key_here

# Set API key (Windows)
set OPENAI_API_KEY=your_api_key_here
```

#### ❌ "Failed to translate text"
**Solutions:**
1. Check your internet connection
2. Verify your OpenAI API key is valid
3. Ensure you have sufficient API credits
4. Try the terminal interface for debugging

#### ❌ "Voice not working"
**Solutions:**
```bash
# Check microphone permissions
# Windows: Settings > Privacy > Microphone
# macOS: System Preferences > Security & Privacy > Microphone

# Install audio dependencies
pip install pyaudio speechrecognition

# Check system audio drivers
```

#### ❌ "Web interface not loading"
**Solutions:**
```bash
# Check if port is available
netstat -an | grep 8005

# Try different port
python main.py --web --port 8006

# Check dependencies
pip install -r requirements.txt
```

#### ❌ "Module not found errors"
**Solution:**
```bash
# Install dependencies
pip install -r requirements.txt

# Or install individually
pip install openai fastapi uvicorn jinja2 colorama pydantic speechrecognition pyaudio
```

### Debug Mode

```bash
# Run with verbose output
python main.py --web --debug

# Check API health
curl http://127.0.0.1:8005/api/health
```

### Getting Help

1. **Check the terminal output** for detailed error messages
2. **Verify your OpenAI API key** is working with a simple test
3. **Try the terminal interface** for debugging
4. **Check the `/api/health` endpoint** for service status
5. **Review the logs** for specific error details

---

## 🤝 Contributing

This project is part of the **#100DaysOfAI-Agents** challenge. We welcome contributions!

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Areas for Contribution

- **🐛 Bug Fixes**: Report and fix bugs
- **✨ New Features**: Add new language support or features
- **📚 Documentation**: Improve README, add examples
- **🎨 UI/UX**: Enhance the web interface
- **🧪 Testing**: Add more test coverage
- **🔧 Configuration**: Improve configuration options

### Development Setup

```bash
# Clone the repository
git clone <repository-url>
cd 05_TranslatorAgent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
python test_installation.py
python test_translation.py
python test_voice.py
```

### Code Style

- Follow **PEP 8** Python style guidelines
- Use **type hints** for function parameters
- Add **docstrings** for all functions
- Write **comprehensive tests**
- Keep **commit messages** clear and descriptive

---

## 📄 License

This project is part of the **#100DaysOfAI-Agents** challenge by [Muhammad Sami Asghar Mughal](https://github.com/your-username).

### License Terms

- **Open Source**: This project is open source and available under the MIT License
- **Educational Use**: Free to use for educational and personal purposes
- **Commercial Use**: Contact the author for commercial licensing
- **Attribution**: Please credit the original author when using this code

---

## 🙏 Acknowledgments

### Open Source Libraries
- **[OpenAI](https://openai.com/)** - GPT API for intelligent translation
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern web framework for the API
- **[Uvicorn](https://www.uvicorn.org/)** - Lightning-fast ASGI server
- **[Jinja2](https://jinja.palletsprojects.com/)** - Template engine for web interface
- **[Colorama](https://pypi.org/project/colorama/)** - Cross-platform colored terminal output
- **[SpeechRecognition](https://pypi.org/project/SpeechRecognition/)** - Speech-to-text functionality
- **[pyttsx3](https://pypi.org/project/pyttsx3/)** - Text-to-speech functionality

### Community
- **AI Community** - For inspiration and support
- **Open Source Contributors** - For the amazing tools that make this possible
- **Beta Testers** - For valuable feedback and bug reports

### Special Thanks
- **OpenAI Team** - For making powerful AI accessible
- **FastAPI Community** - For the excellent documentation and support
- **#100DaysOfAI-Agents** - For the motivation to build amazing AI tools

---

<div align="center">

**Happy translating! 🌍✨**

[⬆️ Back to Top](#-translatoragent---day-5-of-100daysofai-agents)

</div> 