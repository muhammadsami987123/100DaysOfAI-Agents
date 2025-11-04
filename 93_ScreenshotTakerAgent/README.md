# 📸 ScreenshotTakerAgent - Day 93 of #100DaysOfAI-Agents

<div align="center">

![ScreenshotTakerAgent Banner](https://img.shields.io/badge/ScreenshotTakerAgent-Day%2093-blue?style=for-the-badge&logo=camera&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![Speech Recognition](https://img.shields.io/badge/SpeechRecognition-Voice%20Commands-lightgrey?style=for-the-badge&logo=google-assistant&logoColor=white)
![PyAutoGUI](https://img.shields.io/badge/PyAutoGUI-Screenshot%20Tool-red?style=for-the-badge&logo=windows&logoColor=white)
![LLM Integration](https://img.shields.io/badge/LLM%20Integration-Gemini%202.0--flash-orange?style=for-the-badge&logo=google&logoColor=white)

**Capture your desktop or application windows with simple voice commands**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎭 Examples](#-examples) • [📚 Documentation](#-documentation) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is ScreenshotTakerAgent?

ScreenshotTakerAgent is an intelligent AI-powered assistant that allows users to capture screenshots of their desktop or active application windows using intuitive voice commands. Designed for efficiency and ease of use, this agent streamlines your workflow by eliminating the need for manual keyboard shortcuts or mouse clicks for screen capture.

### 🌟 Key Highlights

- **🗣️ Voice-Controlled**: Capture screenshots with natural language commands.
- **🖥️ Full Screen & Window Capture**: Take screenshots of your entire display or just the active window.
- **⏰ Automatic Timestamps**: Screenshots are automatically saved with unique timestamps for easy organization.
- **💾 Smart Saving**: Option to name and save screenshots by voice.
- **📂 Organized Storage**: Screenshots are stored in a structured folder (`screenshots/`).
- **🖼️ Open Last Screenshot**: Quickly open the most recently captured image with a voice command.
- **🧠 LLM Integration**: Utilizes Gemini 2.0-flash (default) or OpenAI GPT-4.1 for robust command interpretation.
- **🛡️ Error Handling**: Gracefully handles unrecognized commands and potential issues.

## 🎯 Features

### 🚀 Core Functionality
- ✅ **Voice Command Recognition**: Interprets spoken commands for screenshot actions.
- ✅ **Full Screen Capture**: Captures the entire desktop display.
- ✅ **Active Window Capture**: Focuses and captures only the currently active application window.
- ✅ **Timestamped Filenames**: Automatically names screenshots with `YYYY-MM-DD_HH-MM-SS.png` format.
- ✅ **Screenshot Directory Management**: Creates and manages a dedicated `screenshots/` folder.

### 🗣️ Voice Command Options
- ✅ **"Take screenshot"**: Captures the full screen.
- ✅ **"Capture window"**: Captures the active window.
- ✅ **"Save screenshot [name]"**: Saves the last taken screenshot with an optional custom name.
- ✅ **"Open last screenshot"**: Opens the most recently saved screenshot for quick review.

### 💻 User Interfaces
- ✅ **Command-Line Interface (CLI)**: Provides a simple and direct way to interact with the agent.
- ✅ **Minimal Web GUI (Optional)**: A basic Flask-based web interface for visual interaction (under development).

### 🎨 Advanced Features
- ✅ **LLM-Powered Command Interpretation**: Uses advanced language models to understand varied voice commands.
- ✅ **Robust Error Handling**: Provides clear feedback for unrecognized commands or operational failures.
- ✅ **Modular Python Structure**: Follows a clean, maintainable, and extensible codebase.

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.8+** installed on your system.
- **OpenAI API Key** or **Gemini API Key** (if using LLM integration).
- **Internet connection** for voice recognition and LLM services.

### 🔧 Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/muhammadsami987123/100DaysOfAI-Agents.git
    cd 100DaysOfAI-Agents/93_ScreenshotTakerAgent
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    ./venv/Scripts/activate
    ```

3.  **Install required packages**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your API keys** (if using LLM integration) in a `.env` file in the root of the `93_ScreenshotTakerAgent` directory:
    ```
    GEMINI_API_KEY="your_gemini_api_key"
    OPENAI_API_KEY="your_openai_api_key"
    ```

## 🏃 Usage

Run the main application from your terminal:

```bash
python main.py
```

### 🎙️ Voice Commands:

-   "Take screenshot": Captures the full screen.
-   "Capture window": Captures the active window.
-   "Save screenshot [name]": Saves the image with a timestamp, optionally with a custom name.
-   "Open last screenshot": Opens the most recent screenshot.

## 🎭 Example CLI Session:

```
> Listening for command...
User: Take screenshot
LLM Response: Intent: take_screenshot
Window: False
Screenshot saved: screenshots/2025-11-04_12-45-30.png

> Listening for command...
User: Capture window
LLM Response: Intent: take_screenshot
Window: True
Window screenshot saved: screenshots/window_2025-11-04_12-46-10.png

> Listening for command...
User: Open last screenshot
LLM Response: Intent: open_last_screenshot
Opening screenshot: screenshots/window_2025-11-04_12-46-10.png

> Listening for command...
User: Save screenshot my important document
LLM Response: Intent: save_screenshot
Name: my important document
Screenshot saved as: screenshots/my important document.png
```

## 📚 Documentation

-   `agent.py`: Core logic for voice recognition, screenshot capture, and command processing.
-   `config.py`: Manages API keys and application settings.
-   `main.py`: Entry point for the CLI application.
-   `web_app.py`: (Optional) Flask application for a minimal web interface.
-   `utils/llm_service.py`: Handles interactions with Gemini and OpenAI LLMs.
-   `prompts/screenshot_prompt.txt`: Defines the prompt used for LLM command interpretation.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue for any bugs or feature requests.
