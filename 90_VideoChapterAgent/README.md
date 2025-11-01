# 🎬 VideoChapterAgent - Day 90 of #100DaysOfAI-Agents

<div align="center"></div>

![VideoChapterAgent Banner](https://img.shields.io/badge/VideoChapterAgent-Day%2090-blue?style=for-the-badge&logo=video&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![LLMs](https://img.shields.io/badge/LLMs-Gemini%202.0--flash%20%7C%20GPT--4.1-orange?style=for-the-badge&logo=google&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20Framework-red?style=for-the-badge&logo=fastapi&logoColor=white)

**Automatically split videos into meaningful chapters using AI-powered transcription and analysis**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎭 Examples](#-examples) • [📚 Documentation](#-documentation) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is VideoChapterAgent?

VideoChapterAgent is an intelligent AI assistant designed to simplify video content consumption and management. It takes any video file, generates a detailed transcript, and then leverages advanced AI to identify logical sections and automatically split the video into meaningful chapters with timestamps. This agent is perfect for educators, content creators, or anyone who wants to quickly navigate long videos and extract key information.

### 🌟 Key Highlights

- **🎥 Video Upload**: Supports common video formats (mp4, mov, etc.)
- **📝 AI Transcription**: Generates accurate transcripts from video audio using Whisper or similar models.
- **🧠 Intelligent Chaptering**: Analyzes transcripts to identify logical sections and create chapters.
- **⏱️ Timestamp Generation**: Provides precise start and end times for each chapter.
- **⬇️ Downloadable Segments**: Optionally download individual video chapters.
- **📖 Full Transcript Output**: Get the complete transcript with chapter markers.
- **🌐 Dual LLM Support**: Default Gemini 2.0-flash, with optional OpenAI GPT-4.1.
- **💻 Modern Web UI**: Clean, responsive, and mobile-friendly interface with video player and chapter markers.

## 🎯 Features

### 🚀 Core Functionality
- ✅ **Video Upload**: Easily upload video files for processing.
- ✅ **AI-Powered Transcription**: Utilizes advanced models for high-quality audio-to-text conversion.
- ✅ **Smart Chapter Detection**: AI analyzes transcript content to define chapter boundaries.
- ✅ **Timestamp Accuracy**: Generates precise timestamps for each chapter.
- ✅ **Chapter List Output**: Displays a clear list of chapters with titles and time ranges.
- ✅ **Downloadable Chapters**: Option to download video segments for each chapter.
- ✅ **Full Transcript with Markers**: Provides the complete transcript with chapter indicators.
- ✅ **LLM Selection**: Choose between Gemini 2.0-flash (default) and OpenAI GPT-4.1.

### 💻 User Interface
- ✅ **Modern Web UI**: Intuitive and responsive design built with HTML and TailwindCSS.
- ✅ **Video Player Integration**: Displays the uploaded video with interactive chapter markers.
- ✅ **Output Panel**: Dedicated sections for chapter list, full transcript, and download options.
- ✅ **Mobile-Friendly**: Fully responsive layout for seamless use on all devices.
- ✅ **Scrollable Transcript**: Easy navigation through the full transcript.

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.8+** installed on your system
- **FFmpeg** installed and accessible in your system's PATH (for video processing)
- **Google Gemini API Key** (get one from [Google AI Studio](https://aistudio.google.com/app/apikey))
- **Optional: OpenAI API Key** (get one from [OpenAI Platform](https://platform.openai.com/api-keys))
- **Internet connection** for AI model interaction

### ⚡ One-Click Installation

```bash
# Windows - Run the installer
install.bat

# The installer will:
# ✅ Check Python installation
# ✅ Create virtual environment
# ✅ Install all dependencies
# ✅ Set up configuration files
# ✅ Run installation tests
```

### 🔧 Manual Installation

```bash
# 1. Clone or download the project
git clone <repository-url>
cd 90_VideoChapterAgent

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up environment variables
echo GEMINI_API_KEY=your_gemini_api_key_here > .env
echo OPENAI_API_KEY=your_openai_api_key_here >> .env
```

### 🎯 First Run

```bash
# Start the web application
python main.py

# Open your browser and navigate to: http://localhost:8000
```

### 🧪 Verify Installation

```bash
# Run the test suite
python -m pytest test/

# Expected output:
# ✅ Python version compatible
# ✅ All dependencies installed
# ✅ Configuration loaded
# ✅ Agent initialized
# ✅ Web app ready
```

## 🎭 Examples & Usage

### 🌐 Web Interface

The web interface provides an intuitive experience for video chaptering:

1. **⬆️ Upload Video**: Click the "Upload Video" button and select your video file (e.g., `ProductivityTips.mp4`).
2. **🧠 Select LLM**: Choose your preferred LLM (Gemini 2.0-flash or OpenAI GPT-4.1) from the dropdown.
3. **🚀 Process**: Click "Generate Chapters" and wait for the agent to process the video.
4. **📖 View Output**: The output panel will display:
   - **Chapter List**: Titles and timestamps for each chapter.
   - **Full Transcript**: The complete video transcript with chapter markers.
   - **Download Buttons**: Options to download individual chapter segments or the full transcript.
5. **▶️ Interact with Video Player**: The integrated video player will show chapter markers, allowing you to jump to specific sections.

**🎯 Pro Tips:**
- For faster processing, use shorter videos.
- Ensure your video has clear audio for better transcription accuracy.
- Experiment with different LLMs to see which provides the best chaptering results for your content.

### ⚡ Example Input & Output

**Example Input:**
- Video: `ProductivityTips.mp4`

**Expected Output:**
- Chapter 1: Introduction (00:00–02:15)
- Chapter 2: Morning Routine Tips (02:16–05:45)
- Chapter 3: Time Management Techniques (05:46–09:30)
- Chapter 4: Conclusion & Summary (09:31–10:20)

## 🏗️ Project Architecture

### 📁 File Structure

```
90_VideoChapterAgent/
├── 📄 .env                      # Environment variables (API keys)
├── 📄 .gitignore                # Git ignore file
├── 🤖 agent.py                 # Core AI logic for transcription and chaptering
├── ⚙️ config.py                 # Configuration and settings management
├── 📄 main.py                   # Main entry point for the FastAPI application
├── 📄 README.md                 # This comprehensive documentation
├── 📋 requirements.txt          # Python dependencies
├── 🌐 web_app.py                # FastAPI web application with API endpoints
├── 📦 install.bat               # Windows installation script
├── 🖼 Images/                   # Placeholder for images
├── 📝 prompts/                  # LLM prompt templates
│   └── chapter_prompt.txt      # Prompt for chapter generation
├── 🎨 static/                   # Static assets
│   └── main.css                # TailwindCSS for styling
├── 📚 templates/                # HTML templates
│   └── index.html              # Main web interface
├── 🧪 test/                     # Unit and integration tests
│   ├── test_agent.py           # Tests for agent.py
│   └── test_web_app.py         # Tests for web_app.py
├── ⬆️ uploads/                  # Directory for uploaded video files
└── 🛠️ utils/                    # Utility functions
    └── llm_service.py          # Handles LLM interactions (Gemini, OpenAI)
```

### 🔧 Technical Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Python 3.8+ | Core application logic |
| **Web Framework** | FastAPI | REST API and web server |
| **LLMs** | Google Gemini 2.0-flash, OpenAI GPT-4.1 | Chapter generation and analysis |
| **Video/Audio Processing** | FFmpeg, pydub, Whisper (or similar) | Video splitting and transcription |
| **Frontend** | HTML, TailwindCSS, JavaScript | Interactive user interface |
| **Environment Management** | python-dotenv | Loading environment variables |
| **Server** | Uvicorn | ASGI web server |

### 🎯 Key Components

#### 🤖 `agent.py`
- **Video Processing**: Handles video file manipulation (splitting, audio extraction).
- **Transcription**: Integrates with Whisper or similar models for accurate audio transcription.
- **Chapter Generation**: Utilizes LLMs to analyze transcripts and identify logical chapter breaks.
- **Timestamp Calculation**: Determines precise start and end times for each chapter.

#### 🌐 `web_app.py`
- **FastAPI Endpoints**: Defines API routes for video upload, chapter generation, and transcript retrieval.
- **File Handling**: Manages video file uploads and storage.
- **LLM Integration**: Orchestrates calls to the `LLMService` for chaptering.
- **Frontend Rendering**: Serves the `index.html` template.

#### 🎨 Frontend (`templates/index.html`, `static/main.css`)
- **Video Upload Interface**: Allows users to upload video files.
- **LLM Selection**: Dropdown for choosing between Gemini and OpenAI.
- **Video Player**: Displays the uploaded video with interactive chapter markers.
- **Output Display**: Presents the chapter list, full transcript, and download options.
- **Responsive Design**: Ensures optimal viewing across various devices.

#### 🛠️ `utils/llm_service.py`
- **LLM Abstraction**: Provides a unified interface for interacting with different LLMs (Gemini, OpenAI).
- **Prompt Management**: Handles prompt engineering for chapter generation.
- **API Key Management**: Securely loads API keys from environment variables.

## ⚙️ Configuration & Setup

### 🔑 API Key Setup

**Step 1: Get API Keys**
- **Google Gemini**: Visit [Google AI Studio](https://aistudio.google.com/app/apikey), sign up/log in, and create an API key.
- **OpenAI**: Visit [OpenAI Platform](https://platform.openai.com/api-keys), sign up/log in, and create an API key.

**Step 2: Configure the Keys**

Create a `.env` file in the project root and add your API keys:

```
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 🎛️ Advanced Configuration

Edit `config.py` to customize the application:

```python
# LLM Settings
DEFAULT_LLM_MODEL = "gemini-pro"  # Default LLM model to use
OPENAI_MODEL = "gpt-4"            # OpenAI model to use
TEMPERATURE = 0.7                 # Creativity level for LLM (0.0-1.0)

# File Storage Settings
UPLOAD_DIR = "uploads"            # Directory for uploaded video files
CHAPTERS_DIR = "chapters"         # Directory for generated video chapters
TRANSCRIPTS_DIR = "transcripts"   # Directory for generated transcripts

# Web Interface Settings
WEB_TITLE = "VideoChapterAgent"
WEB_DESCRIPTION = "AI-powered video chaptering and transcription"
WEB_VERSION = "1.0.0"
```

## 🧪 Testing & Quality Assurance

### 🔍 Installation Testing

Run the comprehensive test suite to verify everything is working:

```bash
python -m pytest test/
```

**Test Coverage:**
- ✅ **Python Version**: Compatibility check (3.8+)
- ✅ **Dependencies**: All required packages installed
- ✅ **File Structure**: All necessary files present
- ✅ **Configuration**: Settings loaded correctly
- ✅ **API Integration**: LLM connection tests
- ✅ **Agent Core**: Video processing and chaptering logic tests
- ✅ **Web App**: FastAPI application tests
- ✅ **File System**: Directory creation and permissions

## 🐛 Troubleshooting

This section provides solutions to common issues you might encounter while setting up and running the VideoChapterAgent.

### 1. `ImportError: cannot import name 'CHAPTERS_DIR' from 'config'`

**Type of Error:** Python `ImportError`

**Cause:** This error occurs when `agent.py` or `web_app.py` tries to import a directory constant (like `CHAPTERS_DIR` or `TRANSCRIPTS_DIR`) from `config.py`, but these constants are not defined in `config.py`.

**Solution:**
Ensure that your `config.py` file defines all necessary directory paths. It should look similar to this:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY") # Or GEMINI_API_KEY if you named it that
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# LLM Models
GEMINI_MODEL = "gemini-2.0-flash"
OPENAI_MODEL = "gpt-4"

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")
TRANSCRIPTS_DIR = os.path.join(BASE_DIR, "transcripts")

# Create directories if they don't exist
for directory in [UPLOAD_DIR, PROMPTS_DIR, CHAPTERS_DIR, TRANSCRIPTS_DIR]:
    os.makedirs(directory, exist_ok=True)
```

### 2. `ValueError: Invalid LLM type. Choose 'gemini' or 'openai'.`

**Type of Error:** Python `ValueError`

**Cause:** This error indicates that the `LLMService` class in `utils/llm_service.py` received an `llm_type` argument that is neither "gemini" nor "openai". This usually happens if the `llm_model` value passed from `web_app.py` to `agent.py` is incorrect or malformed.

**Solution:**
Ensure that `web_app.py` is passing either "gemini" or "openai" to the `VideoChapterAgent` constructor and its `process_video` method.

In `web_app.py`, locate the `upload_video` function and ensure the `llm_model` is correctly set:

```python
# ...existing code...

@app.post("/upload-video/")
async def upload_video(
    request: Request,
    video_file: UploadFile = File(...),
    llm_model: str = Form("gemini") # Ensure this is "gemini" or "openai"
):
    # ...existing code...
    llm_model = "gemini" # Explicitly set to ensure correct value
    agent = VideoChapterAgent(llm_model)
    result = agent.process_video(video_path, llm_model) # Pass llm_model here
    # ...existing code...
```

### 3. `FileNotFoundError: [WinError 2] The system cannot find the file specified` (FFmpeg)

**Type of Error:** Python `FileNotFoundError` (Operating System Error)

**Cause:** This error means that the `ffmpeg` executable, which is required for audio extraction and video splitting, is not found by your system. The `ffmpeg-python` library is a wrapper and requires the actual FFmpeg program to be installed and accessible in your system's PATH.

**Solution:**
You need to install FFmpeg on your Windows machine and add it to your system's PATH.

1.  **Download FFmpeg:**
    *   Go to the official FFmpeg website: `https://ffmpeg.org/download.html`
    *   Click on the Windows icon and download a "release build" or "full build" `.zip` file.
2.  **Extract FFmpeg:**
    *   Extract the contents of the `.zip` file to a simple location, e.g., `C:\ffmpeg`.
    *   Locate the `bin` folder inside the extracted `ffmpeg` directory (e.g., `C:\ffmpeg\bin`). This folder contains `ffmpeg.exe`.
3.  **Add FFmpeg to your System's PATH:**
    *   Search for "Environment Variables" in the Windows search bar and select "Edit the system environment variables".
    *   In the System Properties window, click "Environment Variables...".
    *   Under "System variables", find and select the `Path` variable. Click "Edit...".
    *   Click "New" and add the full path to your FFmpeg `bin` folder (e.g., `C:\ffmpeg\bin`).
    *   Click "OK" on all windows to save.
4.  **Verify Installation:**
    *   Open a **new** PowerShell or Command Prompt window.
    *   Type `ffmpeg -version` and press Enter. You should see FFmpeg version information.

After these steps, restart your FastAPI application.

### 4. API Key Errors (e.g., "defect api key gemini")

**Type of Error:** API Authentication Error

**Cause:** This error occurs when the application cannot find a valid API key for the selected LLM (Gemini or OpenAI), or the key provided is incorrect/expired. This can be due to:
    *   The `.env` file not being loaded.
    *   The environment variable name in `.env` not matching what `config.py` expects.
    *   The API key itself being invalid.

**Solution:**

1.  **Verify `.env` file:**
    *   Ensure you have a `.env` file in the root directory of the `90_VideoChapterAgent` folder.
    *   The `.env` file should contain your API keys, for example:
        ```
        GOOGLE_API_KEY=your_gemini_api_key_here
        OPENAI_API_KEY=your_openai_api_key_here
        ```
    *   **Important:** If you are using a Google API Key for Gemini, ensure the variable name is `GOOGLE_API_KEY` in your `.env` file, as `config.py` is configured to read `os.getenv("GOOGLE_API_KEY")`.

2.  **Check `config.py`:**
    *   Ensure `config.py` is correctly loading the environment variables. The relevant lines should look like this:
        ```python
        # ...existing code...
        from dotenv import load_dotenv
        load_dotenv()

        # API Keys
        GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY") # Matches .env
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        # ...existing code...
        ```
3.  **Obtain Valid API Keys:**
    *   **Google Gemini API Key:** Get one from [Google AI Studio](https://aistudio.google.com/app/apikey).
    *   **OpenAI API Key:** Get one from [OpenAI Platform](https://platform.openai.com/api-keys).

After making sure your `.env` file is correctly configured with valid API keys and `config.py` is reading them, restart your application.

## 📞 Support & Community

### 🆘 Getting Help

1. **📖 Documentation**: Check this README and code comments
2. **🧪 Test Suite**: Run `python -m pytest test/`
3. **🔍 Troubleshooting**: Review the troubleshooting section
4. **📊 Logs**: Check console output for error messages
5. **🌐 API Status**: Verify Google AI Studio and OpenAI API are operational

### 🐛 Reporting Issues

When reporting issues, please include:
- **System Information**: OS, Python version, browser
- **Error Messages**: Full error output
- **Steps to Reproduce**: What you were doing when it happened
- **Expected vs Actual**: What you expected vs what happened

### 💬 Community

- **GitHub Issues**: Report bugs and request features
- **Discussions**: Ask questions and share ideas
- **Showcase**: Share your amazing chaptered videos!

## 📄 License & Credits

### 📜 License

This project is part of the **#100DaysOfAI-Agents** challenge by **Muhammad Sami Asghar Mughal**.

**MIT License** - Feel free to use, modify, and distribute!

### 🙏 Acknowledgments

- **Google AI Studio** for providing the Gemini API
- **OpenAI** for providing the GPT-4.1 API
- **FastAPI** team for the excellent web framework
- **Python community** for amazing libraries (pydub, ffmpeg-python, python-dotenv, etc.)
- **All contributors** who help improve this project

### 🌟 Inspiration

This project was inspired by the need for efficient video content analysis and the desire to make long videos more accessible and digestible through AI-powered chaptering.

---

<div align="center">

## 🎉 Ready to Chapter Your Videos?

**Transform your video content with AI-powered chaptering and transcription!**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎭 Examples](#-examples) • [📚 Documentation](#-documentation)

---

**Made with ❤️ by the #100DaysOfAI-Agents community**

*Day 90 of 100 - Building the future of AI agents, one day at a time!*

</div>