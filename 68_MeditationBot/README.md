# 🧘 MeditationBot - Day 68 of #100DaysOfAI-Agents

<div align="center">

![MeditationBot Banner](https://img.shields.io/badge/MeditationBot-Day%2068-green?style=for-the-badge&logo=meditation&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-Pro-blue?style=for-the-badge&logo=google&logoColor=white)
![FastAPI](https://img.shields.io/badge/Flask-Web%20Framework-red?style=for-the-badge&logo=flask&logoColor=white)

**Find your calm with AI-guided meditation sessions.**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [💡 Problem Solved](#-problem-it-solves) • [📚 Documentation](#-documentation) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is MeditationBot?

MeditationBot is an AI-powered guide designed to lead users through short, focused meditation sessions. It aims to help individuals reduce stress, improve focus, or simply relax through calming instructions, breathing exercises, and optional soothing background sounds. Leveraging the power of Large Language Models, MeditationBot provides dynamic and personalized meditation experiences.

### 🌟 Key Highlights

- **🧘 Dynamic Meditation Sessions**: AI-generated scripts tailored to user needs.
- **⏰ Customizable Durations**: Choose from 2, 5, or 10-minute sessions.
- **🗣️ Text-to-Speech (TTS)**: Guided meditations with voice playback using `gTTS`.
- **🎶 Calming Background Sounds**: Options for forest stream, ocean waves, or gentle rain.
- **🌬️ Breathing Animation**: Visual cues for mindful breathing during sessions.
- **🌐 Web UI**: Modern and responsive interface built with Flask and Tailwind CSS.

## 💡 Problem It Solves

In today's fast-paced world, many people struggle with stress, burnout, and distractions. MeditationBot offers an accessible, on-demand solution by providing guided meditations that are:

-   **Simple**: Easy to start and follow.
-   **Voice-Guided**: Enhances immersion and reduces screen dependency.
-   **Customizable**: Adaptable to specific needs (relaxation, focus, sleep, stress relief) and preferred lengths.

This bot brings the benefits of meditation to users' fingertips, helping them find moments of peace and mental clarity whenever and wherever they need it.

## 🎯 Features

### 🚀 Core Functionality
- ✅ **AI Meditation Generation**: Powered by Google Gemini for dynamic script creation.
- ✅ **Guided Audio Sessions**: Text-to-Speech for a soothing voice-guided experience.
- ✅ **Interactive UI**: User-friendly controls for meditation type and duration.
- ✅ **Background Ambiance**: Selectable calming sounds to enhance the experience.
- ✅ **Visual Breathing Aid**: Simple animation to guide breathing.

### 🎭 Customization Options
- ✅ **Multiple Meditation Types**: Relaxation, Focus, Sleep, Stress Relief.
- ✅ **Flexible Durations**: 2, 5, or 10-minute sessions.
- ✅ **Soundscapes**: Options for 'None', 'Forest Stream', 'Ocean Waves', 'Gentle Rain'.

### 💻 User Interface
- ✅ **Modern Web UI**: Beautiful, responsive interface with Tailwind CSS.
- ✅ **Real-time Feedback**: Script display and audio playback synchronization.

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.8+** installed on your system
- **Google Gemini API Key** (get one from [Google AI Studio](https://aistudio.google.com/app/apikey))
- **Internet connection** for AI meditation generation
- **Actual `.mp3` audio files** for background sounds (place in `static/`)

### 🔧 Installation

```bash
# 1. Clone or download the project
git clone <repository-url>
cd 68_MeditationBot

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows
vb\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up environment variable
# Create a .env file in the 68_MeditationBot directory:
# GEMINI_API_KEY="your_gemini_api_key_here"
```

### 🎯 First Run

```bash
# Start the Flask web application
python main.py

# Open your web browser and navigate to:
http://127.0.0.1:5000
```

## 🎭 Examples & Usage

### 🌐 Web Interface

The web interface provides an interactive experience for guided meditation:

1.  **🧘 Choose Meditation Type**: Select from 'Relaxation', 'Focus', 'Sleep', or 'Stress Relief'.
2.  **⏰ Set Duration**: Pick a session length of 2, 5, or 10 minutes.
3.  **🎶 Select Background Sound**: Choose 'None', 'Forest Stream', 'Ocean Waves', or 'Gentle Rain'.
4.  **🚀 Start Meditation**: Click "Start Meditation" and follow the voice-guided instructions.
5.  **🌬️ Observe Animation**: A breathing circle will guide your mindful breathing.

## 🏗️ Project Architecture

### 📁 File Structure

```
68_MeditationBot/
├── 📄 main.py                   # Flask application entry point and routes
├── 🤖 meditation_agent.py       # Core AI meditation generation and TTS logic
├── 📋 requirements.txt          # Python dependencies
├── 📚 templates/                # HTML templates
│   └── index.html              # Main meditation interface
├── 🎨 static/                   # Static assets
│   ├── css/
│   │   └── style.css           # Custom CSS for breathing animation
│   ├── forest_stream.mp3       # Placeholder for Forest Stream background audio
│   ├── ocean_waves.mp3         # Placeholder for Ocean Waves background audio
│   └── gentle_rain.mp3         # Placeholder for Gentle Rain background audio
├── 📄 README.md                 # This comprehensive documentation
└── 📄 .env                      # Environment variables (e.g., GEMINI_API_KEY)
```

### 🔧 Technical Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Python 3.8+ | Core application logic |
| **AI Engine** | Google Gemini 2.0 Flash | Dynamic meditation script generation |
| **Web Framework** | Flask | REST API and web server |
| **TTS Library** | gTTS | Text-to-Speech conversion |
| **Template Engine** | Jinja2 | HTML template rendering |
| **Frontend** | Vanilla JavaScript | Interactive user interface |
| **Styling** | Tailwind CSS + Custom CSS | Modern, responsive design, animations |
| **Data Storage** | Environment Variables | API key management |

### 🎯 Key Components

#### 🤖 MeditationBot (`meditation_agent.py`)
- **Core AI Logic**: Handles Google Gemini API integration.
- **Script Generation**: Creates meditation scripts based on user selections.
- **TTS Conversion**: Converts script text to audio for guided sessions.

#### 🌐 Flask Application (`main.py`)
- **Web Server**: Manages web routes and serves HTML/static files.
- **API Endpoints**: Handles requests for starting meditation sessions.
- **Data Flow**: Passes meditation options and audio scripts between frontend and backend.

#### 🎨 Frontend (`templates/index.html` & `static/`)
- **Interactive UI**: Modern interface for user input.
- **Audio Playback**: Manages background music and TTS audio.
- **Breathing Animation**: Visual feedback for mindful breathing.

## ⚙️ Configuration & Setup

### 🔑 API Key Setup

**Step 1: Get Google Gemini API Key**
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign up or log in to your Google account
3. Create a new API key
4. Copy the key

**Step 2: Configure the Key**

Create a `.env` file in the `68_MeditationBot` directory and add your API key:

```
GEMINI_API_KEY="your_gemini_api_key_here"
```

### 🎶 Background Audio Files

Place your desired `.mp3` audio files in the `68_MeditationBot/static/` directory with the following names:
- `forest_stream.mp3`
- `ocean_waves.mp3`
- `gentle_rain.mp3`

These files are crucial for the background sound feature to work correctly.

## 🧪 Testing & Quality Assurance

### 🔍 Functional Testing

To verify the core functionality:

1.  **Launch the application** (`python main.py`).
2.  **Open in browser** (`http://127.0.0.1:5000`).
3.  **Select Meditation Options**: Choose a type, duration, and background sound.
4.  **Start Session**: Click "Start Meditation".

**Expected Behavior:**
-   The LLM should generate a meditation script.
-   TTS audio should play each line of the script sequentially.
-   The selected background sound should play on loop.
-   The breathing animation should be visible and active.
-   No errors should appear in the browser console or server logs.

### 🐛 Troubleshooting

**Common Issues & Solutions:**

| Issue | Cause | Solution |
|-------|-------|----------|
| **"Error: Could not start meditation session."** | Missing or invalid Gemini API Key, empty audio files, or network issue. | Ensure `GEMINI_API_KEY` is set in `.env`, replace placeholder audio files with actual `.mp3`s, and check internet connection. |
| **No TTS audio playback** | Missing `gTTS` library, API key issue, or browser autoplay restrictions. | Run `pip install -r requirements.txt`, verify `GEMINI_API_KEY`, and check browser settings for autoplay permissions. |
| **Background sound not playing** | Empty audio files, incorrect file paths, or browser autoplay restrictions. | Replace placeholder audio files, ensure correct filenames in `static/`, and check browser settings. |
| **Breathing animation not visible/working** | CSS loading issue or JavaScript error. | Check `static/style.css` and browser developer console for errors. |

## 🔮 Future Roadmap

### 🚀 Planned Features

| Feature | Status | Description |
|---------|--------|-------------|
| **Multi-language Support** | 🔄 Planned | Allow meditations in different languages. |
| **Custom Session Lengths** | 🔄 Planned | User-defined meditation durations. |
| **More Background Sounds** | 🔄 Planned | Expand the library of calming audio options. |
| **Advanced Breathing Visualizations** | 🔄 Planned | More complex and customizable breathing animations. |
| **User Progress Tracking** | 🔄 Planned | Save and track meditation history and preferences. |
| **Integration with Wearables** | 🔄 Planned | Connect to health devices for biofeedback. |

## 🤝 Contributing

We welcome contributions to make MeditationBot even better! If you have ideas, bug reports, or want to contribute code, please feel free to engage.

### 🛠️ How to Contribute

1.  **Fork the repository**.
2.  **Create a feature branch**: `git checkout -b feature/your-feature-name`.
3.  **Make your changes** and test thoroughly.
4.  **Commit your changes**: `git commit -m 'Add your concise commit message'`.
5.  **Push to the branch**: `git push origin feature/your-feature-name`.
6.  **Open a Pull Request** with a clear description of your changes.

### 🎯 Areas for Contribution

-   **New Meditation Types**: Expand the range of guided meditation themes.
-   **UI/UX Improvements**: Enhance the visual design and user experience.
-   **TTS Voices**: Experiment with different voice options for TTS.
-   **Background Audio Library**: Contribute new high-quality background sound files.
-   **Breathing Animation Variations**: Develop alternative visual breathing aids.
-   **Bug Fixes**: Help identify and resolve issues.

## 📞 Support & Community

### 🆘 Getting Help

1.  **Documentation**: Refer to this README for setup and usage.
2.  **Troubleshooting**: Check the troubleshooting section for common issues.
3.  **Browser Console/Server Logs**: Inspect for detailed error messages.
4.  **GitHub Issues**: Report bugs or ask questions on the project's GitHub repository.

## 📄 License & Credits

### 📜 License

This project is part of the **#100DaysOfAI-Agents** challenge by **Muhammad Sami Asghar Mughal**.

**MIT License** - Feel free to use, modify, and distribute!

### 🙏 Acknowledgments

-   **Google Gemini** for powering the dynamic meditation script generation.
-   **Flask** and **Jinja2** for the web framework and templating.
-   **gTTS** for the Text-to-Speech functionality.
-   **Tailwind CSS** for a streamlined and modern UI design.
-   The **Python community** for invaluable libraries.
-   **All contributors** who help improve this project.

### 🌟 Inspiration

MeditationBot was created to address the growing need for accessible and customizable mindfulness tools, inspired by:

-   The positive impact of guided meditation on stress reduction and focus.
-   The potential of AI to personalize and enhance well-being practices.
-   The desire to make daily meditation simple, engaging, and available to everyone.

---

<div align="center">

## ✨ Find Your Inner Calm with MeditationBot! ✨

**Start your personalized meditation journey today.**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [💡 Problem Solved](#-problem-it-solves)

---

**Made with ❤️ by the #100DaysOfAI-Agents community**

*Day 68 of 100 - Building the future of AI agents, one day at a time!*

</div>
