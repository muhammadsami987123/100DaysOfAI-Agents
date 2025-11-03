# 🎶 JarvisMusicController – Voice-Controlled Music Player (CLI) - Day 92 of #100DaysOfAI-Agents

<div align="center">

![JarvisMusicController Banner](https://img.shields.io/badge/JarvisMusicController-Day%2092-blue?style=for-the-badge&logo=music&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-2.0--flash-orange?style=for-the-badge&logo=google&logoColor=white)
![CLI](https://img.shields.io/badge/Interface-CLI-red?style=for-the-badge&logo=terminal&logoColor=white)

**Control your music playback with simple voice commands in a CLI interface**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎧 Usage](#-usage) • [📚 Documentation](#-documentation) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is JarvisMusicController?

JarvisMusicController is an intelligent voice-controlled agent designed to provide a seamless music playback experience directly from your command-line interface. With simple voice commands, you can play, pause, skip, or stop your favorite tunes, making your music interaction hands-free and intuitive.

### 🌟 Key Highlights

- **🎤 Voice-Activated Control**: Play, pause, next, previous, and stop commands via voice.
- **🎵 Real-time Song Display**: See the currently playing song title in your CLI.
- **🧠 Optional LLM Integration**: Interpret complex commands using Gemini 2.0-flash for advanced control.
- **🛡️ Robust Error Handling**: Gracefully manages unrecognized commands or file issues.
- **💻 CLI-Based Interface**: Lightweight and efficient, perfect for terminal enthusiasts.

## 🎯 Features

### 🚀 Core Functionality
- ✅ **Voice Command Recognition**: Utilizes `speech_recognition` for accurate voice-to-text conversion.
- ✅ **Music Playback**: Integrates `pygame` and `pydub` for reliable audio playback.
- ✅ **Basic Playback Controls**: "Play", "Pause", "Next", "Previous", "Stop" commands.
- ✅ **Current Song Display**: Shows the title of the song being played.
- ✅ **Error Management**: Handles cases like no music files found or unrecognized voice input.

### 🧠 Advanced Features (Optional LLM Integration)
- ✅ **Contextual Command Interpretation**: Uses Gemini 2.0-flash to understand more complex requests.
- ✅ **Example Complex Commands**: "Play my top playlist", "Skip songs longer than 5 minutes" (requires further implementation).

## 💻 Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Python 3.8+ | Core application logic and command processing |
| **Voice Recognition** | `speech_recognition` | Converts spoken commands to text |
| **Audio Playback** | `pygame`, `pydub` | Manages music loading and playback |
| **LLM Integration** | Gemini 2.0-flash | Interprets complex voice commands |
| **Environment Management** | `python-dotenv` | Loads environment variables (e.g., API keys) |

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.8+** installed on your system.
- **Gemini API Key** (get one from [Google AI Studio](https://aistudio.google.com/app/apikey)).
- **Internet connection** for voice recognition and LLM integration.
- **Music files** (MP3, WAV, OGG) in the `music/` directory.

### 🔧 Installation

```bash
# 1. Clone the repository
git clone https://github.com/muhammadsami987123/100DaysOfAI-Agents.git
cd 100DaysOfAI-Agents/92_JarvisMusicController

# 2. Create and activate a virtual environment
python -m venv venv
# On Windows
.\\venv\\Scripts\\activate
# On Linux/macOS
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up your environment variables
# Create a .env file in the project root and add your Gemini API key:
echo GEMINI_API_KEY="YOUR_GEMINI_API_KEY" > .env
```

### 🎯 First Run

1. **Add Music**: Place your `.mp3`, `.wav`, or `.ogg` music files into the `music/` directory within the project.
2. **Run the Agent**:
   ```bash
   python main.py
   ```
3. **Speak Commands**: The agent will prompt you to speak commands like "Play", "Pause", "Next", "Previous", or "Stop".

## 🎧 Usage

To start the JarvisMusicController, simply run the `main.py` script. The agent will continuously listen for your voice commands.

```bash
python main.py
```

### 🗣️ Voice Commands

- **"Play"**: Starts playing the current song or resumes a paused song.
- **"Pause"**: Pauses the currently playing song.
- **"Next" / "Skip"**: Skips to the next song in the playlist.
- **"Previous" / "Back"**: Goes back to the previous song in the playlist.
- **"Stop"**: Stops playback completely.

### 🧪 Example CLI Session

```
> Listening for command...
User: Play
Now playing: "Blinding Lights - The Weeknd"

> Listening for command...
User: Next
Skipped to: "Levitating - Dua Lipa"

> Listening for command...
User: Pause
Playback paused.

> Listening for command...
User: Stop
Playback stopped.
```

## 🏗️ Project Architecture

### 📁 File Structure

```
92_JarvisMusicController/
├── 📄 .env                      # Environment variables (e.g., API keys)
├── 📄 README.md                 # Project documentation
├── 📄 requirements.txt          # Python dependencies
├── ⚙️ config.py                 # Configuration settings
├── 🤖 agent.py                 # Core JarvisMusicController logic
├── 📄 main.py                   # Main entry point to run the agent
├── 🎵 music/                    # Directory for your music files
└──  utils/                      # Utility functions
    └── 🧠 llm_service.py         # LLM integration for command interpretation
```

### 🎯 Key Components

#### 🤖 JarvisMusicController (`agent.py`)
- **Voice Recognition**: Captures and processes voice commands.
- **Music Management**: Loads, plays, pauses, and skips music tracks.
- **CLI Output**: Displays current song and playback status.
- **Command Processing**: Interprets and executes voice commands.

#### 🧠 LLMService (`utils/llm_service.py`)
- **Gemini Integration**: Connects to the Gemini API for advanced command interpretation.
- **Command Interpretation**: Translates complex natural language commands into actionable instructions.

#### ⚙️ Config (`config.py`)
- **API Key Management**: Securely loads API keys from `.env`.
- **Music Directory**: Defines the path to your music files.
- **Supported Formats**: Lists audio file extensions the agent can play.

## ⚙️ Configuration & Setup

### 🔑 API Key Setup

**Step 1: Get Gemini API Key**
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign up or log in to your Google account.
3. Create a new API key.
4. Copy the generated key.

**Step 2: Configure the Key**
Create a `.env` file in the root directory of the `92_JarvisMusicController` project and add your Gemini API key:

```
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
```

### 🎛️ Customization

Edit `config.py` to customize the application:

```python
# ...existing code...
class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    MUSIC_DIR = "music" # Directory where music files are stored
    SUPPORTED_AUDIO_FORMATS = [".mp3", ".wav", ".ogg"] # Supported audio file extensions
# ...existing code...
```

## 🧪 Testing & Quality Assurance

### 🔍 Manual Testing

- **Voice Command Accuracy**: Test various commands ("Play", "Pause", "Next", "Previous", "Stop") to ensure correct recognition and action.
- **Music Playback**: Verify that songs play, pause, and stop as expected.
- **Error Handling**: Test scenarios like no music files, invalid commands, or microphone issues.
- **LLM Interpretation**: If LLM is enabled, test complex commands to see if they are correctly interpreted.

### 🐛 Troubleshooting

**Common Issues & Solutions:**

| Issue | Cause | Solution |
|-------|-------|----------|
| **"Could not understand audio"** | Microphone issues, background noise, unclear speech | Check microphone, reduce noise, speak clearly |
| **"Could not request results from Google Speech Recognition service"** | Internet connectivity issues, API limits | Check internet connection, try again later |
| **"No music files found"** | `music/` directory is empty or missing | Add supported audio files to the `music/` directory |
| **"Error playing song"** | Unsupported audio format, corrupted file | Ensure files are MP3/WAV/OGG, check file integrity |
| **"GEMINI_API_KEY not found"** | Missing or incorrect API key in `.env` | Verify `GEMINI_API_KEY` in `.env` file |
| **"ModuleNotFoundError"** | Missing Python dependencies | Run `pip install -r requirements.txt` |

## 🔮 Future Roadmap

### 🚀 Planned Features

| Feature | Status | Description |
|---------|--------|-------------|\
| **Playlist Management** | 🔄 Planned | Create, save, and load custom playlists |
| **Volume Control** | 🔄 Planned | Voice commands for adjusting playback volume |
| **Song Search** | 🔄 Planned | Search for specific songs by title or artist |
| **Advanced LLM Commands** | 🔄 Planned | Implement more complex LLM-driven commands (e.g., "Play upbeat music") |
| **Cross-Platform Audio** | 🔄 Planned | Explore alternatives for broader audio playback compatibility |
| **GUI Interface** | 🔄 Planned | Develop an optional graphical user interface |

### 🎯 Enhancement Ideas

- **Music Metadata**: Display artist, album, and other song information.
- **Streaming Service Integration**: Connect to Spotify, Apple Music, etc.
- **Customizable Hotkeys**: Allow users to define keyboard shortcuts for controls.
- **Voice Feedback**: Agent provides verbal confirmation of commands.

## 🤝 Contributing

We welcome contributions to make JarvisMusicController even better!

### 🛠️ How to Contribute

1. **Fork the repository**.
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`.
3. **Make your changes** and test thoroughly.
4. **Commit your changes**: `git commit -m 'Add your amazing feature'`.
5. **Push to the branch**: `git push origin feature/your-feature-name`.
6. **Open a Pull Request**.

### 🎯 Areas for Contribution

- **New Features**: Implement planned features or suggest new ones.
- **Bug Fixes**: Identify and resolve issues.
- **Documentation**: Improve guides and examples.
- **Performance Optimization**: Enhance speed and efficiency.
- **LLM Integration**: Improve command interpretation and add more complex commands.

### 📋 Contribution Guidelines

- Follow the existing code style.
- Add tests for new features (if applicable).
- Update documentation as needed.
- Ensure all tests pass.
- Be respectful and constructive.

## 📞 Support & Community

### 🆘 Getting Help

1. **📖 Documentation**: Check this README and code comments.
2. **🐛 Troubleshooting**: Review the troubleshooting section.
3. **📊 Logs**: Check console output for error messages.
4. **🌐 API Status**: Verify Google Speech Recognition and Gemini API are operational.

### 💬 Community

- **GitHub Issues**: Report bugs and request features.
- **Discussions**: Ask questions and share ideas.

## 📄 License & Credits

### 📜 License

This project is part of the **#100DaysOfAI-Agents** challenge by **Muhammad Sami Asghar Mughal**.

**MIT License** - Feel free to use, modify, and distribute!

### 🙏 Acknowledgments

- **Google** for providing the Gemini API and Speech Recognition service.
- **Python community** for amazing libraries (`speech_recognition`, `pygame`, `pydub`, `python-dotenv`).
- **All contributors** who help improve this project.

### 🌟 Inspiration

This project was inspired by the desire to create an accessible and intuitive voice-controlled music player for CLI environments, leveraging the power of AI for enhanced command interpretation.

---

<div align="center">

## 🎉 Ready to Control Your Music with Your Voice?

**Transform your CLI into a voice-activated music hub!**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎧 Usage](#-usage) • [📚 Documentation](#-documentation)

---

**Made with ❤️ by the #100DaysOfAI-Agents community**

*Day 92 of 100 - Building the future of AI agents, one day at a time!*

</div>

