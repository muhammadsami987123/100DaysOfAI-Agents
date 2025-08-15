# 🌐 BrowserOpenerAgent - Day 15 of #100DaysOfAI-Agents

A voice and CLI-driven agent that opens URLs in the system's default web browser. Supports natural language commands and voice input for opening websites with intelligent site name mapping, smart search capabilities, and fallback to Google search.

## 🚀 Features

- **Voice Command Recognition**: Use speech recognition with silence detection to open websites with natural language
- **Smart Search Within Websites**: Automatically search within specific websites (YouTube, Google, GitHub, etc.)
- **CLI Interface**: Text-based commands with clean, minimal UI feedback
- **Smart URL Parsing**: Automatically detects and opens valid URLs
- **Site Name Mapping**: Recognizes common site names (YouTube, Google, GitHub, etc.)
- **Google Search Fallback**: Automatically searches Google for unknown sites with graceful messaging
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Voice Feedback**: Text-to-speech confirmation of actions
- **Clean UI**: Minimal, smooth interface with clear status indicators
- **Logging**: Comprehensive logging for debugging and tracking
- **False Positive Prevention**: Only acts on confidently recognized voice input

## 📋 Requirements

- Python 3.7+
- Microphone (for voice mode)
- Speakers (for voice feedback)
- Internet connection
- Default web browser configured

## 🛠️ Installation

### Quick Setup

1. **Navigate to the BrowserOpenerAgent directory:**
   ```bash
   cd 15_BrowserOpenerAgent
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **For voice recognition (optional but recommended):**
   ```bash
   # Windows
   pip install pyaudio
   
   # macOS
   brew install portaudio
   pip install pyaudio
   
   # Linux (Ubuntu/Debian)
   sudo apt-get install python3-pyaudio portaudio19-dev
   pip install pyaudio
   ```

### Manual Installation

If you encounter issues with PyAudio, try these alternatives:

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux:**
```bash
sudo apt-get install python3-pyaudio portaudio19-dev python3-dev
pip install pyaudio
```

## 🎯 Usage

### Starting the Agent

```bash
# CLI mode (default)
python main.py

# Voice mode
python main.py --voice

# CLI mode without voice feedback
python main.py --no-voice

# Show list of supported sites
python main.py --help-sites

# Show help
python main.py --help
```

### Voice Commands

The agent recognizes natural language commands with improved accuracy:

#### Basic Commands
```bash
🎤 "Open YouTube"
🎤 "Go to Google"
🎤 "Launch GitHub"
🎤 "Visit OpenAI"
🎤 "Open https://example.com"
```

#### Smart Search Commands
```bash
🎤 "Open YouTube and search for lo-fi music"
🎤 "Go to Google and search for AI tools"
🎤 "Launch GitHub and search for python projects"
🎤 "Open Wikipedia and search for machine learning"
🎤 "Visit Amazon and search for headphones"
```

#### Advanced Commands
```bash
🎤 "Please open Facebook"
🎤 "Can you open my portfolio"
🎤 "I want to go to Stack Overflow"
🎤 "Navigate to Wikipedia"
```

### CLI Commands

Type commands directly in the CLI interface:

```bash
🌐 BrowserOpenerAgent> Open YouTube
🌐 BrowserOpenerAgent> Go to Google and search for AI tools
🌐 BrowserOpenerAgent> Launch GitHub and search for python projects
🌐 BrowserOpenerAgent> Open https://openai.com
🌐 BrowserOpenerAgent> Visit my portfolio
```

## 🗂️ Supported Sites

The agent automatically maps common site names to their URLs and supports smart search:

### Social Media
- **YouTube**: `https://youtube.com` | Search: `https://youtube.com/results?search_query={}`
- **Facebook**: `https://facebook.com` | Search: `https://facebook.com/search/top/?q={}`
- **Twitter**: `https://twitter.com` | Search: `https://twitter.com/search?q={}`
- **Instagram**: `https://instagram.com` | Search: `https://instagram.com/explore/tags/{}`
- **LinkedIn**: `https://linkedin.com` | Search: `https://linkedin.com/search/results/all/?keywords={}`
- **Reddit**: `https://reddit.com` | Search: `https://reddit.com/search/?q={}`
- **TikTok**: `https://tiktok.com` | Search: `https://tiktok.com/search?q={}`

### Search Engines
- **Google**: `https://google.com` | Search: `https://google.com/search?q={}`
- **Bing**: `https://bing.com` | Search: `https://bing.com/search?q={}`
- **Yahoo**: `https://yahoo.com` | Search: `https://search.yahoo.com/search?p={}`
- **DuckDuckGo**: `https://duckduckgo.com` | Search: `https://duckduckgo.com/?q={}`

### Tech Companies
- **OpenAI**: `https://openai.com` | Search: `https://openai.com/search?q={}`
- **GitHub**: `https://github.com` | Search: `https://github.com/search?q={}`
- **Stack Overflow**: `https://stackoverflow.com` | Search: `https://stackoverflow.com/search?q={}`
- **Microsoft**: `https://microsoft.com` | Search: `https://microsoft.com/search?q={}`
- **Apple**: `https://apple.com` | Search: `https://apple.com/search?q={}`
- **Amazon**: `https://amazon.com` | Search: `https://amazon.com/s?k={}`
- **Netflix**: `https://netflix.com` | Search: `https://netflix.com/search?q={}`
- **Spotify**: `https://spotify.com` | Search: `https://open.spotify.com/search/{}`

### News & Information
- **Wikipedia**: `https://wikipedia.org` | Search: `https://wikipedia.org/wiki/Special:Search?search={}`
- **BBC**: `https://bbc.com` | Search: `https://bbc.com/search?q={}`
- **CNN**: `https://cnn.com` | Search: `https://cnn.com/search?q={}`
- **Reuters**: `https://reuters.com` | Search: `https://reuters.com/search/news?blob={}`

### Development & Learning
- **W3Schools**: `https://w3schools.com` | Search: `https://w3schools.com/search?q={}`
- **MDN**: `https://developer.mozilla.org` | Search: `https://developer.mozilla.org/en-US/search?q={}`
- **Python.org**: `https://python.org` | Search: `https://python.org/search/?q={}`
- **PyPI**: `https://pypi.org` | Search: `https://pypi.org/search/?q={}`

### Common Services
- **Gmail**: `https://gmail.com` | Search: Not supported
- **Outlook**: `https://outlook.com` | Search: Not supported
- **Dropbox**: `https://dropbox.com` | Search: Not supported
- **Google Drive**: `https://drive.google.com` | Search: Not supported
- **Google Maps**: `https://maps.google.com` | Search: `https://maps.google.com/maps?q={}`
- **Google Translate**: `https://translate.google.com` | Search: `https://translate.google.com/?sl=auto&tl=en&text={}`

## 🎤 Voice Mode Features

### Improved Voice Recognition
- **Silence Detection**: Automatically stops listening when you finish speaking
- **Background Noise Reduction**: Higher energy threshold to reduce false positives
- **Shorter Timeouts**: Faster response times with 8-second timeout
- **Minimum Length Check**: Only processes commands with 3+ characters
- **Better Error Handling**: Graceful handling of unintelligible speech

### Voice Triggers
The agent recognizes these voice command patterns:
- "Open"
- "Go to"
- "Launch"
- "Navigate to"
- "Visit"
- "Browse to"
- "Please open"
- "Can you open"
- "Would you open"
- "I want to go to"

### Search Keywords
Smart search is triggered by these keywords:
- "search for"
- "search"
- "find"
- "look for"
- "look up"
- "show me"
- "and search for"
- "and find"
- "and look for"

### Voice Feedback
- Confirms when listening for commands
- Announces the site being opened or searched
- Provides clean success/error feedback
- Speaks goodbye when exiting

## 💻 CLI Mode Features

### Clean Interface
- **Minimal Status Messages**: Simple states like "🎤 Listening...", "🧠 Processing...", "🌐 Opening browser...", "✅ Done!"
- **Clean Site Names**: Shows "YouTube" instead of "https://youtube.com"
- **Smart Search Feedback**: "🧠 Processing: YouTube search for 'lo-fi music'"
- **Graceful Fallback**: "🤔 Couldn't understand your command. Redirecting to Google search."

### Command Processing
- Natural language parsing
- URL validation
- Site name recognition
- Smart search detection
- Automatic Google search fallback

## 🔧 Configuration

### Voice Settings
You can modify voice settings in the code:
- Speech rate (default: 175 words per minute)
- Language hint (default: "en-US")
- Microphone timeout (default: 8 seconds)
- Energy threshold (default: 4000 for noise reduction)
- Pause threshold (default: 0.8 seconds for silence detection)

### Site Mappings
Add custom site mappings by editing the `site_mappings` dictionary in `main.py`:

```python
self.site_mappings = {
    "myportfolio": {
        "url": "https://myportfolio.com", 
        "search_url": "https://myportfolio.com/search?q={}"
    },
    "company": {
        "url": "https://mycompany.com",
        "search_url": None  # No search support
    },
    # Add more mappings here
}
```

## 📝 Examples

### Opening Popular Sites
```bash
# Voice commands
🎤 "Open YouTube"          → Opens YouTube homepage
🎤 "Go to Google"          → Opens Google homepage
🎤 "Launch GitHub"         → Opens GitHub homepage
🎤 "Visit OpenAI"          → Opens OpenAI homepage

# CLI commands
🌐 BrowserOpenerAgent> Open YouTube
🌐 BrowserOpenerAgent> Go to Google
🌐 BrowserOpenerAgent> Launch GitHub
```

### Smart Search Examples
```bash
# Voice commands
🎤 "Open YouTube and search for lo-fi music"     → Searches YouTube for "lo-fi music"
🎤 "Go to Google and search for AI tools"        → Searches Google for "AI tools"
🎤 "Launch GitHub and search for python projects" → Searches GitHub for "python projects"
🎤 "Open Wikipedia and search for machine learning" → Searches Wikipedia for "machine learning"

# CLI commands
🌐 BrowserOpenerAgent> Open YouTube and search for lo-fi music
🌐 BrowserOpenerAgent> Go to Google and search for AI tools
🌐 BrowserOpenerAgent> Launch GitHub and search for python projects
```

### Opening Direct URLs
```bash
# Voice commands
🎤 "Open https://example.com"
🎤 "Go to https://myportfolio.dev"

# CLI commands
🌐 BrowserOpenerAgent> Open https://example.com
🌐 BrowserOpenerAgent> Go to https://myportfolio.dev
```

### Search Fallback
```bash
# Voice commands
🎤 "Open python tutorials"     → Searches Google for "python tutorials"
🎤 "Go to machine learning"    → Searches Google for "machine learning"
🎤 "Visit my custom site"      → Searches Google for "my custom site"

# CLI commands
🌐 BrowserOpenerAgent> Open python tutorials
🌐 BrowserOpenerAgent> Go to machine learning
```

## 🐛 Troubleshooting

### Voice Recognition Issues

**Problem**: "No speech detected" or poor recognition
**Solutions**:
1. Check microphone permissions
2. Ensure quiet environment
3. Speak clearly and at normal volume
4. Try different microphone if available
5. The agent now has better noise reduction and silence detection

**Problem**: PyAudio installation fails
**Solutions**:
1. Use pipwin on Windows: `pip install pipwin && pipwin install pyaudio`
2. Install portaudio first on macOS: `brew install portaudio`
3. Install system dependencies on Linux: `sudo apt-get install python3-pyaudio`

### Browser Issues

**Problem**: Browser doesn't open
**Solutions**:
1. Check if default browser is set
2. Verify internet connection
3. Try opening browser manually first
4. Check firewall settings

### General Issues

**Problem**: Import errors
**Solution**: Install missing dependencies:
```bash
pip install -r requirements.txt
```

**Problem**: Permission errors
**Solution**: Run with appropriate permissions or check file/directory access

## 📊 Logging

The agent creates a `browser_opener.log` file with detailed information:
- Voice recognition attempts
- URL processing steps
- Browser opening attempts
- Error messages and stack traces

## 🔄 Exit Commands

To exit the agent:
- **Voice mode**: Say "exit", "quit", "stop", or "goodbye"
- **CLI mode**: Type "exit", "quit", or "stop"
- **Both modes**: Press Ctrl+C

## 🎨 Customization

### Adding Custom Sites
Edit the `site_mappings` dictionary in `main.py`:

```python
self.site_mappings = {
    # Existing mappings...
    "myblog": {
        "url": "https://myblog.com",
        "search_url": "https://myblog.com/search?q={}"
    },
    "company": {
        "url": "https://mycompany.com",
        "search_url": None
    },
}
```

### Modifying Voice Triggers
Edit the `voice_triggers` list in `main.py`:

```python
self.voice_triggers = [
    # Existing triggers...
    "start", "begin", "access",
]
```

### Adding Search Keywords
Edit the `search_keywords` list in `main.py`:

```python
self.search_keywords = [
    # Existing keywords...
    "query", "lookup", "find me",
]
```

### Changing Speech Rate
Modify the rate parameter in `SpeechOutput`:

```python
self.speech_output = SpeechOutput(enable_voice, rate=150)  # Slower
self.speech_output = SpeechOutput(enable_voice, rate=200)  # Faster
```

## 🧪 Testing

Run the test suite to verify functionality:

```bash
python test_agent.py
```

The tests cover:
- URL validation
- Site mapping
- Smart search functionality
- Voice trigger removal
- Clean site names
- Browser opening
- Agent initialization

## 🤝 Contributing

Feel free to contribute by:
- Adding more site mappings with search URLs
- Improving voice recognition accuracy
- Adding new smart search features
- Fixing bugs
- Improving documentation

## 📄 License

This project is part of the #100DaysOfAI-Agents challenge.

## 🙏 Acknowledgments

- Speech recognition powered by Google Speech Recognition API
- Text-to-speech powered by pyttsx3
- Rich CLI interface powered by Rich library
- Cross-platform browser support via webbrowser module

---

**Day 15 of #100DaysOfAI-Agents** - Building intelligent agents one day at a time! 🚀
