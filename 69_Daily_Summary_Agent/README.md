# 🗞️ DailySummaryAgent - Day 69 of #100DaysOfAI-Agents

<div align="center">

![DailySummaryAgent Banner](https://img.shields.io/badge/DailySummaryAgent-Day%2069-blue?style=for-the-badge&logo=google&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-API-blue?style=for-the-badge&logo=google&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-red?style=for-the-badge&logo=flask&logoColor=white)
![TTS](https://img.shields.io/badge/TTS-gTTS-orange?style=for-the-badge&logo=google&logoColor=white)

**Your AI assistant for personalized daily summaries combining tasks and top news with audio!**

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [🎭 Examples](#-examples) • [🏗️ Project Architecture](#-project-architecture) • [⚙️ Configuration](#-configuration--setup) • [🧪 Testing](#-testing--quality-assurance) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is DailySummaryAgent?

DailySummaryAgent is a smart assistant designed to provide users with a quick, personalized summary of their day. It intelligently combines the user's task list (completed and pending) with top trending news updates, presenting them in a clean, concise, and professional format. Optionally, it can provide motivation or tips for the next day, and supports an audio (TTS) version of the summary.

### 🌟 Key Highlights

- **📰 Personalized Summaries**: Combines user tasks and news into a single, cohesive daily brief.
- **💡 AI-Powered News Fetching**: Utilizes Google Gemini API to retrieve top trending news headlines based on user preference.
- **🗣️ Text-to-Speech (TTS)**: Generates an audio version of the daily summary for convenient listening.
- **📝 Task Management Integration**: Analyzes and summarizes both completed and pending tasks provided by the user.
- **🎨 Modern UI**: Features a clean, responsive, and intuitive web interface with dark/light mode, inspired by leading dashboard designs.
- **⚙️ Configurable**: All configurations (API keys, models, etc.) are handled via a `.env` file and a `Config` class.

## 🎯 Features

### 🚀 Core Functionality
- ✅ **AI-Powered Summary Generation**: Integrates with Google Gemini API for intelligent content summarization.
- ✅ **Dynamic News Fetching**: Fetches top news headlines from various categories using the Gemini API.
- ✅ **Task Processing**: Processes user-provided completed and pending tasks.
- ✅ **Comprehensive Daily Brief**: Combines tasks and news into a structured summary with distinct sections.
- ✅ **Audio Summaries**: Converts the generated text summary into an audio file using gTTS for an accessible experience.

### 🎨 User Experience
- ✅ **Modern Dashboard UI**: Intuitive two-column layout for inputs and outputs, inspired by popular web dashboards.
- ✅ **Dark/Light Mode**: User-friendly theme toggle for comfortable viewing in any lighting condition.
- ✅ **Clear Input Guidance**: Enhanced labels and hints for task and news preference inputs.
- ✅ **Visual Feedback**: Prominent loading spinner and error message display for smooth interaction.
- ✅ **Initial Welcome Screen**: Engaging welcome message with an example output to guide new users.

### 📊 Management & Integration
- ✅ **Centralized Configuration**: Uses a `Config` class and `.env` file for easy management of API keys and settings.
- ✅ **Modular Codebase**: Organized Python files for clear separation of concerns (Flask app, news fetching, summarization, TTS).

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.8+** installed on your system.
- **Google Gemini API Key** (get one from [Google AI Studio](https://aistudio.google.com/app/apikey)).
- **Internet connection** for AI summarization and news fetching.

### 🔧 Manual Installation

   ```bash
# 1. Navigate to the agent's directory
cd 69_Daily_Summary_Agent

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment (Windows)
venc\Scripts\activate
# On Linux/Mac, use: source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up environment variable
# Create a .env file in the 69_Daily_Summary_Agent directory:
echo GEMINI_API_KEY=your_gemini_api_key_here > .env
# Replace 'your_gemini_api_key_here' with your actual API key.
```

### 🎯 First Run (Web UI - Recommended)

   ```bash
# 1. Navigate to the agent's directory (if not already there)
cd 69_Daily_Summary_Agent

# 2. Run the application
python main.py

# 3. Then, open your web browser and navigate to:
# http://127.0.0.1:5000
```

## 🎭 Examples & Usage

### 🌐 Web Interface

The intuitive web interface allows you to easily get your daily summary:

1.  **Enter Your Tasks**: Provide your completed and pending tasks, separated by commas.
2.  **Choose News Preference**: Specify a news category (e.g., "Technology", "Sports", "Business") or leave as "General".
3.  **Generate Summary**: Click "Generate Summary" to receive your personalized daily brief.
4.  **Listen to Audio**: Click "Play Audio Summary" to listen to the generated brief.

### 💡 Example Scenario:

-   **Morning Briefing**: Enter yesterday's completed tasks and today's pending tasks, along with your preferred news category, to get a comprehensive overview of your day, both visually and audibly.

## 🏗️ Project Architecture

### 📁 File Structure

```
69_Daily_Summary_Agent/
├── main.py                 # Entry point to run the Flask web_app
├── web_app.py              # Flask web application with API routes
├── config.py               # Configuration settings for API keys, models, etc.
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (e.g., GEMINI_API_KEY)
├── README.md               # This comprehensive documentation
├── templates/
│   └── index.html          # HTML template for the UI (dashboard layout)
├── static/
│   ├── main.css            # Custom CSS for styling (dark mode, etc.)
│   └── summary.mp3         # Generated audio files (saved here)
└── utils/
    ├── news_api.py         # Handles fetching news headlines from Gemini API
    ├── summary_service.py  # Generates summaries (tasks + news) using Gemini API
    └── tts_utils.py        # Handles Text-to-Speech conversion using gTTS
```

### 🔧 Technical Stack

| Component        | Technology          | Purpose                                  |
|------------------|---------------------|------------------------------------------|
| **Backend**      | Python 3.8+         | Core application logic                   |
| **AI Engine**    | Google Gemini API   | News fetching and summary generation     |
| **Web Framework**| Flask               | REST API and web server                  |
| **Template Engine**| Jinja2              | HTML template rendering                  |
| **Frontend**     | HTML5, CSS3, JavaScript | Modern, responsive UI with interactive elements |
| **Styling**      | Tailwind CSS        | Responsive design and aesthetic enhancements |
| **Text-to-Speech**| gTTS                | Converts text summaries to audio         |
| **Environment**  | python-dotenv       | Environment variable management          |

### 🎯 Key Components

#### 🤖 DailySummaryAgent (`web_app.py`)
- **Orchestration**: Manages the flow from user input to summary generation and TTS output.
- **Flask Routes**: Handles `/` (UI) and `/summarize` (API) endpoints.

#### 📰 News API Utility (`utils/news_api.py`)
- **News Fetching**: Interacts with the Gemini API to get trending news headlines.

#### 💡 Summary Service (`utils/summary_service.py`)
- **Summary Generation**: Uses the Gemini API to create coherent summaries from tasks and news.
- **Structured Output**: Ensures summaries are formatted into distinct sections for tasks and news.

#### 🔊 TTS Utility (`utils/tts_utils.py`)
- **Audio Conversion**: Utilizes `gTTS` to convert text summaries into spoken audio files.

#### ⚙️ Configuration (`config.py`)
- **Centralized Settings**: Defines API keys, Gemini model, TTS language, and other configurable parameters.

## ⚙️ Configuration & Setup

### 🔑 API Key Setup

**Step 1: Get Google Gemini API Key**
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign up or log in to your Google account.
3. Create a new API key.
4. Copy the generated API key (starts with `AIza...`).

**Step 2: Configure the Key**

Create a `.env` file in the `69_Daily_Summary_Agent` directory with your API key:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

*   **Important**: Do NOT commit your `.env` file to version control. The `.gitignore` file is already configured to ignore it.

### 🎛️ Advanced Configuration

Edit `config.py` to customize application settings:

```python
# AI Model Settings
GEMINI_MODEL = "gemini-2.0-flash"  # Or another suitable Gemini model (e.g., 'gemini-1.5-flash')

# TTS Settings
TTS_LANGUAGE = "en"  # Language for Text-to-Speech (e.g., 'en', 'ur', 'hi')
AUDIO_DIR = "static" # Directory to save audio files (relative to agent root)

# News Settings
MAX_NEWS_HEADLINES = 5  # Number of news headlines to fetch
DEFAULT_NEWS_PREFERENCE = "General" # Default news category if not specified by user
```

## 🧪 Testing & Quality Assurance

### 🔍 Installation Testing

After following the "Manual Installation" steps, verify the following:

-   ✅ Python virtual environment is created and activated.
-   ✅ All dependencies listed in `requirements.txt` are installed without errors.
-   ✅ `.env` file is created with your `GEMINI_API_KEY`.

### 🚀 Functional Testing

1.  **Launch the Web UI**: Run `python main.py` and navigate to `http://127.0.0.1:5000`.
2.  **Test Summary Generation**: Enter sample tasks and a news preference (e.g., "Technology") and click "Generate Summary". Verify that both "Your Daily Tasks Summary" and "Today’s Top News" sections are populated with relevant content.
3.  **Test Audio Playback**: After a summary is generated, click "Play Audio Summary" and ensure the audio plays correctly.
4.  **Test Dark/Light Mode**: Toggle the theme switch and ensure all UI elements adapt correctly.
5.  **Test Error Handling**: Try submitting without an API key (by temporarily removing it from `.env` or using an invalid key) to see the error message.

### 🐛 Troubleshooting

**Common Issues & Solutions:**

| Issue                                   | Cause                               | Solution                                         |
|-----------------------------------------|-------------------------------------|--------------------------------------------------|
| **"API key not found"**               | Missing or invalid `GEMINI_API_KEY` | Ensure `.env` file is correct or API key is set as environment variable. |
| **"Error fetching news"**             | Network issue or API quota          | Check your internet connection or Gemini API usage. |
| **"Could not generate summary"**      | Gemini API issue or invalid prompt  | Check Gemini API key; simplify news preference. |
| **"No such file or directory: '...\static\summary.mp3'"** | Permissions or path issue           | Ensure the `static` directory is writable.       |
| **"Port already in use"**             | Flask default port (5000) is occupied | Restart your system or use a different port (advanced Flask configuration). |

## 🔮 Future Roadmap

### 🚀 Planned Features

| Feature                        | Status     | Description                                     |
|--------------------------------|------------|-------------------------------------------------|
| **Scheduled Digests**          | 🔄 Planned | Allow users to schedule daily/weekly summaries. |
| **Personalized Motivation**    | 🔄 Planned | Dynamically generate motivation/tips based on tasks. |
| **Task Management Integration**| 🔄 Planned | Integrate with external task management APIs (e.g., Trello, Todoist). |
| **Multiple News Sources**      | 🔄 Planned | Expand news fetching to include more APIs/sources. |
| **User Authentication**        | 🔄 Planned | Implement secure user accounts and personalized settings. |

### 🎯 Enhancement Ideas

-   **Customizable News Filters**: Allow users to select specific news sources or exclude certain topics.
-   **Summary Length Control**: Provide options to control the verbosity of the generated summary.
-   **Notification System**: Implement notifications for when a new daily summary is ready.
-   **Shareable Summaries**: Allow users to easily share their daily briefs.

## 🤝 Contributing

We welcome contributions to make DailySummaryAgent even better!

### 🛠️ How to Contribute

1.  **Fork the repository**.
2.  **Create a feature branch**: `git checkout -b feature/your-feature-name`.
3.  **Make your changes** and test thoroughly.
4.  **Commit your changes**: `git commit -m 'feat: Add amazing new summary feature'`.
5.  **Push to the branch**: `git push origin feature/your-feature-name`.
6.  **Open a Pull Request** with a clear description of your changes.

### 🎯 Areas for Contribution

-   **UI/UX Improvements**: Further enhance the user interface and experience.
-   **Backend Optimizations**: Improve the efficiency and speed of summary generation and news fetching.
-   **New Integrations**: Add support for more task management tools or news APIs.
-   **Error Handling**: Make error messages even more user-friendly and robust.
-   **Testing**: Expand unit and integration tests.

### 📋 Contribution Guidelines

-   Follow the existing code style and naming conventions.
-   Add unit tests for new functionality.
-   Update documentation (README.md) as needed.
-   Ensure all automated tests pass.
-   Be respectful and constructive in all interactions.

## 📞 Support & Community

### 🆘 Getting Help

1.  **📖 Documentation**: Refer to this README for comprehensive information.
2.  **🐛 Troubleshooting**: Check the troubleshooting section for common issues.
3.  **📊 Console Logs**: Review your terminal output for any error messages or warnings.
4.  **🌐 Internet Connection**: Ensure you have a stable internet connection for API calls.

### 🐛 Reporting Issues

When reporting issues via GitHub Issues, please include:

-   **System Information**: Your OS, Python version, and browser used.
-   **Full Error Messages**: Copy and paste the complete error traceback if applicable.
-   **Steps to Reproduce**: A clear, concise description of how to reproduce the bug.
-   **Expected vs. Actual Behavior**: What you expected to happen versus what actually occurred.

### 💬 Community

-   **GitHub Issues**: For bug reports and feature requests.
-   **GitHub Discussions**: For general questions, ideas, and sharing your experience.

## 📄 License & Credits

### 📜 License

This project is part of the **#100DaysOfAI-Agents** challenge by **Muhammad Sami Asghar Mughal**.

**MIT License** - Feel free to use, modify, and distribute the code for personal and commercial purposes.

### 🙏 Acknowledgments

-   **Google Gemini API** for powerful AI capabilities.
-   **Flask** for the lightweight and flexible web framework.
-   **Tailwind CSS** and **Font Awesome** for UI components and icons.
-   **gTTS** for Text-to-Speech functionality.
-   **The Python community** for a rich ecosystem of libraries.
-   **All contributors** who help improve this project.

### 🌟 Inspiration

This project was inspired by the need for a personalized daily briefing tool that is:

-   **Comprehensive**: Combines personal tasks and global news.
-   **Intelligent**: Powered by advanced AI for high-quality summaries.
-   **User-Friendly**: Featuring a modern and intuitive interface with audio accessibility.
-   **Productive**: Saves time and improves focus for users.

---

<div align="center">

## 🎉 Ready for your Daily Brief?

**Stay informed and organized with your AI-powered daily summary!**

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [🎭 Examples](#-examples) • [🏗️ Project Architecture](#-project-architecture)

---

**Made with ❤️ by Muhammad Sami Asghar Mughal for Day 69 of #100DaysOfAI-Agents**

</div>
