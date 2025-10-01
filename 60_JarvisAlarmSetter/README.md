# ⏰ JarvisAlarmSetter - Day 60 of #100DaysOfAI-Agents

<div align="center">

![JarvisAlarmSetter Banner](https://img.shields.io/badge/JarvisAlarmSetter-Day%2060-blue?style=for-the-badge&logo=clock&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-lightgray?style=for-the-badge&logo=flask&logoColor=white)

**Manage your time hands-free with intelligent voice-controlled alarms**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎭 Examples](#-examples) • [📚 Documentation](#-documentation) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is JarvisAlarmSetter?

JarvisAlarmSetter is a smart voice-enabled assistant agent designed to help users manage alarms seamlessly. It integrates Speech-to-Text (STT) for voice command input, Natural Language Understanding (NLU) to interpret complex time and recurrence requests, and Text-to-Speech (TTS) for confirmations and alarm triggers. A clean web-based UI allows users to visually manage, edit, and delete all active alarms.

### 🌟 Key Highlights

- **🗣️ Voice Commands**: Set, update, and cancel alarms using natural language.
- **👂 Natural Language Understanding (NLU)**: Interprets diverse time expressions like "6 AM tomorrow," "in 25 minutes," "after lunch," and recurring alarms like "every Monday."
- **📢 Text-to-Speech (TTS) Feedback**: Provides audio confirmations for all actions and speaks alarm messages.
- **🖥️ Interactive Web UI**: A clean interface to display, edit, and delete alarms.
- **🔄 Recurring Alarms**: Supports daily, weekly, and custom recurrence patterns.
- **⏰ Flexible Scheduling**: Set one-time reminders or recurring alarms with ease.

## 🎯 Features

### 🚀 Core Functionality
- ✅ **Voice-Activated Alarm Setting**: Use spoken commands to create alarms.
- ✅ **Intelligent Time Parsing**: Understands various time formats and relative durations.
- ✅ **Recurring Alarm Support**: Schedule alarms for specific days of the week or daily.
- ✅ **Alarm Modification**: Voice or UI-based editing of existing alarms.
- ✅ **Alarm Cancellation**: Easily dismiss or delete alarms.
- ✅ **Persistent Alarms**: Alarms are saved and reloaded upon application restart.

### 💻 User Interfaces
- ✅ **Modern Web UI**: Responsive design for easy management of alarms.
- ✅ **Real-time Alarm Display**: View all active and scheduled alarms in a clean list.
- ✅ **Edit/Delete Options**: Directly modify or remove alarms from the UI.
- ✅ **Voice Interaction**: Primary interaction through speech commands for hands-free use.

### 📊 Management & Analytics
- ✅ **Alarm List**: Comprehensive display of all scheduled alarms.
- ✅ **JSON Persistence**: Alarms are stored in a `alarms.json` file for data integrity.
- ✅ **Scheduler Integration**: Uses APScheduler for robust and reliable alarm triggering.

### 🎨 Advanced Features
- ✅ **Speech Recognition**: Utilizes `SpeechRecognition` library for accurate STT.
- ✅ **Text-to-Speech**: Uses `gTTS` and `pyttsx3` for clear and customizable audio feedback.
- ✅ **Multi-threading**: Runs voice assistant and web UI concurrently for a seamless experience.

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.8+** installed on your system.
- **Internet connection** for `gTTS` and `SpeechRecognition` (Google Web Speech API).
- **Microphone** for voice commands.
- **Speaker** for TTS feedback.

### 🔧 Manual Installation

```bash
# 1. Navigate to the project directory
cd 60_JarvisAlarmSetter

# 2. Create a virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Download NLTK data (for enhanced NLU)
python -m nltk.downloader punkt averaged_perceptron_tagger
# Or if you use spaCy (optional, for more advanced NLU):
# python -m spacy download en_core_web_sm
```

### 🎯 First Run

```bash
# Run the application
python main.py

# Open your web browser to:
# http://127.0.0.1:5000/

# The voice assistant will start listening in the terminal.
```

## 🎭 Examples & Usage

### 🌐 Web Interface

Access the web interface at `http://127.0.0.1:5000/`.

1.  **Set New Alarm**: Fill in the time, message, and optional recurrence, then click "Set Alarm".
2.  **View Current Alarms**: All active alarms are listed with their details.
3.  **Edit/Delete Alarms**: Use the "Edit" and "Delete" buttons next to each alarm to manage them.

### 🗣️ Voice Commands

Once the application is running and the voice assistant is listening (check your terminal for "Listening for commands..."), speak your commands.

**Examples:**
-   "Set an alarm for 6 AM tomorrow."
-   "Remind me in 25 minutes."
-   "Cancel the alarm at 3 PM."
-   "Set an alarm for every Monday at 7 PM to attend the meeting."
-   "What are my alarms?"
-   "List all alarms."

**TTS Feedback Examples:**
-   "Your 6 AM alarm has been set."
-   "Reminder set for 25 minutes from now."
-   "The alarm at 3 PM has been cancelled."

### 📝 Usage Tips
-   **Clear Speech**: Speak clearly and directly into your microphone.
-   **Natural Language**: Experiment with different phrases for setting alarms; the NLU is designed to understand various expressions.
-   **UI for Precision**: For complex edits or specific alarm IDs, the UI provides more granular control.

## ⚙️ Configuration & Setup

### 🎛️ Advanced Configuration

Edit `config.py` to customize application settings:

```python
class Config:
    DEBUG = True
    PORT = 5000
    ALARM_FILE = 'alarms.json'
    # Add other configuration settings here, e.g., API keys for STT/TTS services
    # Example: GOOGLE_CLOUD_SPEECH_API_KEY = os.getenv('GOOGLE_CLOUD_SPEECH_API_KEY')
```

### 🌍 Language Configuration (for TTS/STT)

Adjust the language settings in `stt_service.py` and `tts_service.py` if you need to use a language other than English. The `SpeechRecognition` library's `recognize_google` method and `gTTS` both support various languages.

## 🏗️ Project Architecture

### 📁 File Structure

```
60_JarvisAlarmSetter/
├── main.py                # Main application entry point, starts UI and voice assistant
├── config.py              # Configuration settings for Flask app and AlarmManager
├── agent.py               # Core JarvisAlarmSetter logic, NLU, and command processing
├── ui.py                  # Flask web application routes and logic
├── voice.py               # Integrates STT and TTS, and passes commands to the agent
├── alarm_manager.py       # Handles alarm scheduling, persistence, and triggering with APScheduler
├── stt_service.py         # Speech-to-Text service using SpeechRecognition
├── tts_service.py         # Text-to-Speech service using pyttsx3 and gTTS
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── alarms.json            # (Auto-generated) Stores alarm data persistently
└── static/
    ├── css/               # CSS files for styling the UI
    │   └── style.css
    └── js/                # JavaScript files for UI interactivity
        └── script.js
└── templates/
    └── index.html         # Main HTML template for the UI
```

### 🔧 Technical Stack

| Component        | Technology           | Purpose                                      |
|------------------|----------------------|----------------------------------------------|
| **Backend**      | Python 3.8+          | Core application logic                       |
| **Web Framework**| Flask                | Web UI and API endpoints                     |
| **STT**          | SpeechRecognition    | Converts spoken commands to text             |
| **TTS**          | gTTS, pyttsx3        | Converts text confirmations/alarms to speech |
| **Scheduler**    | APScheduler          | Manages alarm scheduling and triggering      |
| **NLU (Basic)**  | Regex, NLTK (optional)| Parses natural language for time/recurrence  |
| **Frontend**     | HTML, CSS, JavaScript| Interactive user interface                   |
| **Data Storage** | JSON File System     | Persistence for alarms                       |

### 🎯 Key Components

#### 🤖 JarvisAlarmSetter Agent (`agent.py`)
- **Command Processing**: Interprets voice commands.
- **NLU Integration**: Extracts time, message, and recurrence from commands.
- **TTS Interaction**: Provides spoken feedback and alarm announcements.

#### 🔊 STT Service (`stt_service.py`)
- **Audio Input**: Captures audio from the microphone.
- **Speech Recognition**: Converts audio to text using Google Web Speech API.

#### 📢 TTS Service (`tts_service.py`)
- **Text-to-Speech**: Generates spoken output from text.
- **Flexible Output**: Can save audio to file or play directly.

#### ⏰ Alarm Manager (`alarm_manager.py`)
- **Alarm CRUD**: Add, cancel, update, and retrieve alarms.
- **Persistence**: Loads and saves alarms to `alarms.json`.
- **Scheduling**: Integrates `APScheduler` to trigger alarms at specified times.

#### 🌐 Web UI (`ui.py`, `templates/`, `static/`)
- **Interactive Display**: Shows all active alarms.
- **Form Submission**: Allows users to add/edit alarms via a web form.
- **Client-side Logic**: `script.js` handles dynamic updates and interactions.

## 🧪 Testing & Quality Assurance

### 🔍 Installation Testing

(A `test_installation.py` would typically be created here to verify dependencies, configurations, and basic functionality. For now, manual verification is expected.)

### 🐛 Troubleshooting

**Common Issues & Solutions:**

| Issue                                | Cause                                     | Solution                                                                |
|--------------------------------------|-------------------------------------------|-------------------------------------------------------------------------|
| **"Could not understand audio"**     | Poor microphone quality, background noise | Ensure a quiet environment, speak clearly, check microphone settings.   |
| **"Speech recognition error"**       | No internet, API limits, bad API key (if used) | Check internet connection, verify API keys, try again later.           |
| **Alarms not triggering**            | Incorrect time format, scheduler not running | Verify time string format, ensure `main.py` is running without errors.  |
| **Web UI not loading**               | Flask app not running, port in use        | Ensure `python main.py` is executed, check if port 5000 is free.       |
| **"ModuleNotFoundError"**            | Missing dependencies                      | Run `pip install -r requirements.txt`.                                  |

## 🔮 Future Roadmap

### 🚀 Planned Features

| Feature                    | Status    | Description                                                 |
|----------------------------|-----------|-------------------------------------------------------------|
| **Advanced NLU**           | 🔄 Planned | Integrate full NLTK/spaCy for more complex phrase parsing   |
| **Voice-based Editing**    | 🔄 Planned | Enable full editing of alarms via voice commands            |
| **Customizable Alarm Sounds** | 🔄 Planned | Allow users to set custom audio files for alarms            |
| **System Notifications**   | 🔄 Planned | Integrate OS-level notifications for triggered alarms       |
| **Cloud Integration**      | 🔄 Planned | Sync alarms with Google Calendar or other services          |
| **Multi-user Support**     | 🔄 Planned | Manage alarms for different users/profiles                  |
| **GUI Application**        | 🔄 Planned | Develop a standalone desktop application (e.g., PyQt/Tkinter) |

### 🎯 Enhancement Ideas

-   **Contextual Understanding**: Improve agent's ability to infer context (e.g., "next Tuesday").
-   **Snooze Functionality**: Add ability to snooze a ringing alarm.
-   **Voice Biometrics**: Implement voice recognition for secure alarm management.
-   **Integration with Other Agents**: Allow alarms to trigger actions in other Jarvis agents.

## 🤝 Contributing

We welcome contributions to make JarvisAlarmSetter even better!

### 🛠️ How to Contribute

1.  **Fork the repository**.
2.  **Create a feature branch**: `git checkout -b feature/your-feature-name`.
3.  **Make your changes** and test thoroughly.
4.  **Commit your changes**: `git commit -m 'Add new feature'`.
5.  **Push to the branch**: `git push origin feature/your-feature-name`.
6.  **Open a Pull Request**.

### 🎯 Areas for Contribution

-   **NLU Improvements**: Enhance time parsing and command understanding.
-   **UI/UX Enhancements**: Improve the web interface design and usability.
-   **Error Handling**: Make the agent more robust to unexpected inputs.
-   **Testing**: Add unit and integration tests for various components.
-   **New Features**: Implement planned features from the roadmap.

## 📞 Support & Community

### 🆘 Getting Help

1.  **Documentation**: Refer to this README for setup and usage.
2.  **Troubleshooting**: Check the troubleshooting section for common issues.
3.  **Codebase**: Review the code for detailed implementation.

### 🐛 Reporting Issues

When reporting issues, please include:
-   **System Information**: OS, Python version, browser.
-   **Error Messages**: Full error output or console logs.
-   **Steps to Reproduce**: Detailed steps to replicate the issue.
-   **Expected vs Actual**: What you expected to happen versus what actually occurred.

### 💬 Community

-   **GitHub Issues**: Report bugs and request features.
-   **Discussions**: Ask questions and share ideas.

## 📄 License & Credits

### 📜 License

This project is part of the **#100DaysOfAI-Agents** challenge by **Muhammad Sami Asghar Mughal**.

**MIT License** - Feel free to use, modify, and distribute!

### 🙏 Acknowledgments

-   **SpeechRecognition** library for robust STT.
-   **gTTS** and **pyttsx3** for text-to-speech capabilities.
-   **APScheduler** for reliable alarm scheduling.
-   **Flask** for the web framework.
-   **Python community** for the ecosystem of libraries.

### 🌟 Inspiration

This project was inspired by the need for a hands-free, intelligent assistant to manage daily reminders and schedules, especially for those who benefit from voice-controlled interfaces or are busy multitaskers.

---

<div align="center">

## 🎉 Ready to Automate Your Reminders?

**Experience seamless time management with JarvisAlarmSetter!**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎭 Examples](#-examples) • [📚 Documentation](#-documentation)

---

**Made with ❤️ by the #100DaysOfAI-Agents community**

*Day 60 of 100 - Building the future of AI agents, one day at a time!*

</div>
