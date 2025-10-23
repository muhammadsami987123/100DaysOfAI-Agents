# ✨ DailyMotivationAgent - Day 80 of #100DaysOfAI-Agents

<div align="center">

![DailyMotivationAgent Banner](https://img.shields.io/badge/DailyMotivationAgent-Day%2080-blueviolet?style=for-the-badge&logo=openai&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-Flash-orange?style=for-the-badge&logo=google&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20Framework-red?style=for-the-badge&logo=fastapi&logoColor=white)

**Your daily spark, one quote and message at a time, with an uplifting voice.**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎭 Examples](#-examples) • [📚 Documentation](#-documentation) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is DailyMotivationAgent?

DailyMotivationAgent is an intelligent AI-powered assistant designed to provide users with a daily dose of inspiration. It generates a unique motivational quote and an encouraging 2-3 sentence message, then reads them aloud using text-to-speech (TTS). The agent features a modern, responsive web application built with FastAPI and a dynamic frontend, offering a seamless and uplifting user experience.

### 🌟 Key Highlights

- **🧠 AI-Powered Content Generation**: Utilizes Google Gemini (default) or OpenAI GPT-4o Mini for generating fresh, impactful quotes and messages.
- **🗣️ Text-to-Speech (TTS)**: Reads the generated content aloud, providing an audio link for a personalized experience (supports English and Urdu).
- **🎨 Premium UI/UX**: Features a modern dark theme with glassmorphism effects, gold accents, and a fully responsive design for a sleek, engaging experience.
- **🖼️ Dynamic Image Backgrounds**: Quotes and messages are displayed beautifully overlaid on random aesthetic image backgrounds, enhancing visual impact.
- **🌍 Language Selection**: Users can choose between English and Urdu for both text generation and TTS.
- **🚀 Fast & Engaging**: Includes a "Crafting inspiration..." loading animation for a realistic feel and smooth transitions.
- **💾 Interactive Options**: Copy text, download audio, and share functionalities with visual feedback.
- **💬 Welcome & About Popups**: Enhances user engagement with a welcome message on load and an informative About page.

## 🎯 Features

### 🚀 Core Functionality

- ✅ **AI Content Generation**: Generates unique motivational quotes and encouraging messages.
- ✅ **Voice Output**: Converts generated text into speech using gTTS.
- ✅ **Dynamic Backgrounds**: Displays content over stunning, randomly selected images.
- ✅ **User-Friendly Interface**: Intuitive design for easy navigation and interaction.
- ✅ **Responsive Design**: Adapts seamlessly to various screen sizes and devices.

### 🎭 Creative Options

- ✅ **Motivational Quotes**: Short and impactful quotes for daily inspiration.
- ✅ **Encouragement Messages**: 2-3 sentence uplifting messages that inspire action, confidence, or hope.
- ✅ **Language Support**: Generates content and audio in English and Urdu.

### 💻 User Interfaces

- ✅ **Modern Web UI**: Beautiful, interactive, and responsive web application.
- ✅ **Welcome Popup**: Engages users on their first visit.
- ✅ **About Page Popup**: Provides detailed information about the agent.
- ✅ **Loading Animations**: Visual feedback during content generation.

### 📊 Management & Analytics

- (Currently no specific management or analytics features for this agent, focusing on core motivation delivery.)

### 🎨 Advanced Features

- ✅ **Glassmorphism Design**: Stylish UI elements with translucent backgrounds.
- ✅ **Gold Accents**: Premium look and feel with golden highlights.
- ✅ **Interactive Buttons**: Visual feedback on copy and download actions.
- ✅ **Error Handling**: Graceful display of error messages via a dedicated modal.

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.8+** installed on your system
- **Google Gemini API Key** and/or **OpenAI API Key** (get one from [Google AI Studio](https://aistudio.google.com/app/apikey) or [OpenAI Platform](https://platform.openai.com/api-keys))
- **Internet connection** for AI content generation, TTS, and image backgrounds.

### ⚡ One-Click Installation (Windows)

```bash
# Not available for this project, manual steps below.
```

### 🔧 Manual Installation

```bash
# 1. Clone or download the project
git clone <repository-url>
cd 80_DailyMotivationAgent

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux (use 'source' instead of 'call')
source venv/bin/activate

# 4. Install dependencies
pip install -r backend/requirements.txt

# 5. Set up environment variables
# Create a .env file in the 80_DailyMotivationAgent directory:
echo GEMINI_API_KEY="your_gemini_api_key_here" > .env
echo OPENAI_API_KEY="your_openai_api_key_here" >> .env
echo DEFAULT_MODEL_PROVIDER="gemini" # or "openai" >> .env
echo HOST="0.0.0.0" >> .env
echo PORT="8000" >> .env
echo DEBUG="True" >> .env
```

### 🎯 First Run

```bash
# Start the FastAPI web application
uvicorn backend.main:app --reload

# Open your browser to: http://localhost:8000
```

### 🧪 Verify Installation

```bash
# (No specific test_installation.py for this project, manual verification by running the app.)
```

## 🎭 Examples & Usage

### 🌐 Web Interface

The web interface provides an interactive experience for daily motivation:

1.  **Welcome Popup**: Upon visiting, a popup will ask if you wish to generate a quote.
2.  **Generate Content**: Click "Yes, Generate!" or "New Quote" button.
3.  **Language Selection**: Choose between "English" or "Urdu" from the dropdown.
4.  **View & Listen**: A motivational quote and message will appear over a dynamic background image, and the audio will play automatically.
5.  **Interact**: Use "Download Audio" to save the MP3, or "Copy Text" to copy the quote and message to your clipboard.
6.  **About Page**: Click "About" in the Navbar to open a popup with detailed information about the agent.

**🎯 Pro Tips:**
- Refresh the page to see the welcome popup again.
- Try different languages to hear the TTS in action.

## 🏗️ Project Architecture

### 📁 File Structure

```
80_DailyMotivationAgent/
├── 📄 main.py                   # FastAPI application entry point and routes
├── ⚙️ config.py                 # Configuration and settings management
├── 🤖 agent.py                  # Core AI content generation logic
├── 🗣️ tts.py                    # Text-to-Speech service logic
├── 📋 requirements.txt          # Python dependencies
├── 📚 frontend/                 # Frontend assets
│   ├── index.html              # Main HTML template for the UI
│   ├── style.css               # Tailwind CSS and custom styles
│   └── app.js                  # Frontend JavaScript for interactivity
├── 🎨 static/                   # Static files
│   └── audio/                  # Generated audio files (MP3s)
├── 📄 README.md                 # This comprehensive documentation
└── 📄 .env                      # Environment variables (API keys, etc.)
```

### 🔧 Technical Stack

| Component         | Technology            | Purpose                                       |
|-------------------|-----------------------|-----------------------------------------------|
| **Backend**       | Python 3.8+, FastAPI  | API, web server, AI orchestration             |
| **AI Engine**     | Google Gemini, OpenAI | Quote & message generation                    |
| **TTS Library**   | gTTS                  | Text-to-Speech conversion                     |
| **Template Engine** | Jinja2                | HTML template rendering                       |
| **Frontend**      | HTML, Tailwind CSS, JS | Interactive UI, dynamic content, animations   |
| **Data Storage**  | `.env`                | API key management                            |
| **Server**        | Uvicorn               | ASGI web server                               |

### 🎯 Key Components

#### 🤖 DailyMotivationAgent (`backend/agent.py`)
- **Core AI Logic**: Handles Google Gemini and OpenAI API integration.
- **Content Generation**: Creates motivational quotes and messages based on prompts.
- **Prompt Rendering**: Uses Jinja2 for dynamic prompt creation.

#### 🗣️ TTSService (`backend/tts.py`)
- **TTS Conversion**: Converts text into MP3 audio files using gTTS.
- **Audio Storage**: Saves generated audio to `static/audio/` and provides URLs.

#### 🌐 FastAPI Application (`backend/main.py`)
- **Web Server**: Manages web routes and serves HTML/static files.
- **API Endpoints**: Handles requests for generating motivation and serving About content.
- **Service Integration**: Orchestrates communication between agent and TTS services.

#### 🎨 Frontend (`frontend/` & `static/`)
- **Interactive UI**: Modern, responsive web interface with dynamic elements.
- **Popup Management**: Controls the display of welcome and about modals.
- **Language Selection**: Manages user's preferred language for content.
- **Audio Playback**: Embeds an audio player for listening to generated content.

## ⚙️ Configuration & Setup

### 🔑 API Key Setup

**Step 1: Get API Keys**
1.  **Google Gemini**: Visit [Google AI Studio](https://aistudio.google.com/app/apikey), sign up/log in, and create an API key.
2.  **OpenAI**: Visit [OpenAI Platform](https://platform.openai.com/api-keys), sign up/log in, and create an API key.

**Step 2: Configure the Keys**

Create a `.env` file in the `80_DailyMotivationAgent` directory and add your API keys:

```env
GEMINI_API_KEY="your_gemini_api_key_here"
OPENAI_API_KEY="your_openai_api_key_here"
DEFAULT_MODEL_PROVIDER="gemini" # or "openai"
HOST="0.0.0.0"
PORT="8000"
DEBUG="True"
```

### 🎛️ Advanced Configuration

Edit `backend/config.py` to customize application settings, such as default model names, server host/port, debug mode, and TTS engine:

```python
# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Default Models
DEFAULT_MODEL_PROVIDER = os.getenv("DEFAULT_MODEL_PROVIDER", "gemini") # 'gemini' or 'openai'
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-flash-latest")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# TTS Configuration
TTS_ENGINE = os.getenv("TTS_ENGINE", "gtts") # 'gtts' (only option for now)
AUDIO_DIR = "static/audio"

# Prompt file path
PROMPT_FILE = "prompts/motivation_prompt.txt"
```

## 🧪 Testing & Quality Assurance

### 🔍 Functional Testing

To verify the core functionality:

1.  **Launch the application** (`uvicorn backend.main:app --reload`).
2.  **Open in browser** (`http://127.0.0.1:8000`).
3.  **Interact with Welcome Popup**: Click "Yes, Generate!"
4.  **Generate New Quotes**: Click the "New Quote" button.
5.  **Test Language Selection**: Switch between English and Urdu.
6.  **Download Audio/Copy Text**: Verify button functionalities and visual feedback.
7.  **About Page**: Click "About" in the Navbar to open a popup with detailed information about the agent.

**Expected Behavior:**
-   The welcome popup appears on initial load.
-   Motivational quotes and messages are generated and displayed.
-   TTS audio plays correctly for selected languages.
-   Image backgrounds update dynamically.
-   All buttons (`New Quote`, `Download Audio`, `Copy Text`, `About`, popup close buttons) are functional and provide visual feedback.
-   The About popup displays the README content accurately.
-   No errors appear in the browser console or server logs.

### 🐛 Troubleshooting

**Common Issues & Solutions:**

| Issue                            | Cause                                                | Solution                                                                                   |
|----------------------------------|------------------------------------------------------|--------------------------------------------------------------------------------------------|
| **"API key not configured"**     | Missing or invalid `GEMINI_API_KEY`/`OPENAI_API_KEY` | Set appropriate API keys in your `.env` file.                                              |
| **"Failed to load motivation"**  | Backend error, network issue, or invalid API response | Check backend logs for errors, verify internet connection, ensure API keys are valid.      |
| **No TTS audio playback**        | `gTTS` error or browser autoplay restrictions         | Check backend logs for gTTS errors, ensure browser allows autoplay.                        |
| **Image not loading**            | Network issue or Picsum Photos unavailable           | Check internet connection, try refreshing.                                                 |
| **`ModuleNotFoundError`**        | Missing Python dependencies                          | Run `pip install -r backend/requirements.txt`.                                             |
| **Port already in use**          | Port 8000 is occupied                                | Change `PORT` in `.env` (e.g., to `8001`) or kill the process using the port.              |
| **About content not displayed**  | Error fetching `README.md` from backend or markdown-it not loaded | Check browser console for errors, ensure `/api/about` endpoint is working, verify markdown-it CDN. |

## 🔮 Future Roadmap

### 🚀 Planned Features

| Feature                | Status        | Description                                       |
|------------------------|---------------|---------------------------------------------------|
| **Theme Toggle**       | 🔄 Planned    | Switch between light and dark modes.              |
| **User Personalization** | 🔄 Planned    | Allow users to set preferences (name, default language). |
| **Scheduled Motivation** | 🔄 Planned    | Send daily motivations via email or notifications. |
| **More TTS Voices**    | 🔄 Planned    | Offer different voice options for TTS.            |
| **Custom Prompts**     | 🔄 Planned    | Let users provide specific themes for motivation. |

### 🎯 Enhancement Ideas

-   Integrate a custom "New Quote" button within the main motivation display.
-   Improve the styling of the audio player for more seamless integration.
-   Add more diverse image sources for backgrounds.

## 🤝 Contributing

We welcome contributions to make DailyMotivationAgent even better!

### 🛠️ How to Contribute

1.  **Fork the repository**.
2.  **Create a feature branch**: `git checkout -b feature/your-feature-name`.
3.  **Make your changes** and test thoroughly.
4.  **Commit your changes**: `git commit -m 'Add amazing feature'`.
5.  **Push to the branch**: `git push origin feature/your-feature-name`.
6.  **Open a Pull Request** with a clear description of your changes.

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

-   **Google Gemini** and **OpenAI** for powering the AI content generation.
-   **FastAPI** and **Jinja2** for the backend web framework and templating.
-   **gTTS** for the Text-to-Speech functionality.
-   **Tailwind CSS** for a streamlined and modern UI design.
-   **Picsum Photos** for dynamic background images.
-   The **Python community** for invaluable libraries.
-   **All contributors** who help improve this project.

### 🌟 Inspiration

DailyMotivationAgent was created to provide an accessible and engaging way for users to receive daily motivation, inspired by:
- The positive impact of uplifting messages on mindset and well-being.
- The potential of AI to personalize and enhance daily routines.
- The desire to make motivation readily available through a modern web application.

---

<div align="center">

## 🎉 Ready for Your Daily Spark?

**Get inspired, stay motivated, and achieve your goals with AI-powered encouragement!**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎭 Examples](#-examples)

---

**Made with ❤️ by the #100DaysOfAI-Agents community**

*Day 80 of 100 - Building the future of AI agents, one day at a time!*

</div>
