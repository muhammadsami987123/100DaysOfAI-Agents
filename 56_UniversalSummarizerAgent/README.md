# 🧠 UniversalSummarizerAgent - Day 56 of #100DaysOfAI-Agents

<div align="center">

![UniversalSummarizerAgent Banner](https://img.shields.io/badge/UniversalSummarizerAgent-Day%2056-purple?style=for-the-badge&logo=markdown&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-API-blue?style=for-the-badge&logo=google&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-red?style=for-the-badge&logo=flask&logoColor=white)

**Summarize any content into clear, concise, and context-aware overviews with AI power!**

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [🎭 Examples](#-examples) • [📚 Documentation](#-documentation) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is UniversalSummarizerAgent?

UniversalSummarizerAgent is an advanced multi-input summarization tool designed to generate clean, concise, and context-aware summaries from various types of content. It moves beyond simple email summarization to become your go-to AI assistant for digesting information from diverse sources.

### 🌟 Key Highlights

- **📄 Multi-Input Support**: Summarize plain text, uploaded files (.pdf, .docx, .txt), and public URLs.
- **💡 Multiple Output Formats**: Get summaries in Bullet Points, Key Takeaways, Executive Summary, or Action Items Only.
- **🌍 Multilingual**: Supports summarization in English, Urdu, and Hindi.
- **🎨 Modern UI**: Clean, responsive, and intuitive web interface with dark/light mode.
- **💾 Easy Export**: Download summaries as PDF or TXT files.
- **⚡ Fast Processing**: Efficient AI model integration for quick summarization.

## 🎯 Features

### 🚀 Core Functionality
- ✅ **AI-Powered Summarization**: Utilizes Google Gemini API for high-quality summaries.
- ✅ **Content Extraction**: Automatically extracts text from URLs, PDFs, and DOCX files.
- ✅ **Flexible Input**: Paste text directly, upload files, or provide a URL.
- ✅ **Adaptive Output**: Generates summaries tailored to your chosen format.
- ✅ **Language Detection/Selection**: Intelligently processes content in multiple languages.

### 🎨 User Experience
- ✅ **Modern Web UI**: Beautiful, responsive interface with subtle animations.
- ✅ **Dark/Light Mode**: User-friendly theme toggle for comfortable viewing.
- ✅ **Loading Animation**: Visual feedback during summary generation.
- ✅ **Download Options**: Convenient one-click download for summaries.

### 📊 Management & Integration
- ✅ **Configurable Settings**: Easy-to-manage options for model parameters, languages, and formats.
- ✅ **Clean Architecture**: Modular Python codebase for easy expansion and maintenance.

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.8+** installed on your system.
- **Google Gemini API Key** (get one from [Google AI Studio](https://aistudio.google.com/app/apikey)).
- **Internet connection** for AI summarization and URL fetching.

### ⚡ One-Click Installation (Windows)

   ```bash
# Navigate to the agent's directory
cd 56_EmailSummarizer

# Run the installer
install.bat

# The installer will:
# ✅ Create a virtual environment
# ✅ Activate the virtual environment
# ✅ Install all Python dependencies
# ✅ Confirm installation completion
```

### 🔧 Manual Installation

   ```bash
# 1. Clone or download the project
git clone https://github.com/your-username/100DaysOfAI-Agents.git
cd 100DaysOfAI-Agents/56_EmailSummarizer

# 2. Create virtual environment
   python -m venv venv

# 3. Activate virtual environment
# Windows
venc\Scripts\activate
# Linux/Mac (adjust if needed, but this agent is designed for Windows install script)
# source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up environment variable
# Create a .env file in the 56_EmailSummarizer directory:
echo GEMINI_API_KEY=your_gemini_api_key_here > .env
# Or set as a system environment variable
```

### 🎯 First Run (Web UI - Recommended)

   ```bash
# Navigate to the agent's directory (if not already there)
cd 56_EmailSummarizer

# Run the application
start.bat

# Then, open your web browser and navigate to:
# http://127.0.0.1:5000
```

## 🎭 Examples & Usage

### 🌐 Web Interface

The intuitive web interface allows you to easily summarize content:

1.  **Select Content Type**: Choose between Text, URL, PDF, DOCX, or TXT.
2.  **Provide Content**: Paste text, enter a URL, or upload your file.
3.  **Choose Output Format**: Select Bullet Points, Key Takeaways, Executive Summary, or Action Items Only.
4.  **Select Language**: Choose English, Urdu, or Hindi for the summary.
5.  **Summarize**: Click "Summarize Content" and view the generated summary.
6.  **Download**: Export your summary as a PDF or TXT file.

### 💡 Example Scenarios:

-   **Summarizing a News Article**: Select "URL", paste a news link, choose "Executive Summary", and get the gist in seconds.
-   **Condensing a Research Paper**: Upload a PDF, select "Key Takeaways", and quickly grasp the main points.
-   **Extracting Action Items from Meeting Notes**: Paste meeting text, select "Action Items Only", and stay organized.

## 📚 Content Types & Summary Formats

### 📄 Supported Content Types

| Content Type | Description | Best Use Cases |
|--------------|-------------|----------------|
| **Text**     | Plain text input directly pasted into the UI. | Quick notes, short emails, direct excerpts. |
| **URL**      | A public web address from which text content will be extracted. | News articles, blog posts, research papers, web pages. |
| **PDF**      | Upload a PDF document for text extraction and summarization. | Reports, academic papers, e-books. |
| **DOCX**     | Upload a Microsoft Word document (.docx) for text extraction. | Official documents, drafts, long-form content. |
| **TXT**      | Upload a plain text file (.txt) for summarization. | Code snippets, raw data, simple documents. |

### 💡 Available Summary Formats

| Format             | Description                                     | Use Case                                  |
|--------------------|-------------------------------------------------|-------------------------------------------|
| **Bullet Points**  | Concise points highlighting key information.    | Quick overview, listing facts.            |
| **Key Takeaways**  | Focuses on the most important insights and lessons. | Learning, strategic planning.             |
| **Executive Summary**| A brief, high-level overview for decision-makers. | Business reports, project proposals.      |
| **Action Items Only**| Extracts only the actionable tasks and decisions. | Meeting minutes, project management.      |

### 🌍 Supported Languages

| Language | Code | Native Name |
|----------|------|-------------|
| **English**| `en` | English     |
| **Urdu**   | `ur` | اردو       |
| **Hindi**  | `hi` | हिन्दी      |

## 🏗️ Project Architecture

### 📁 File Structure

```
56_EmailSummarizer/ # Renamed from 14_EmailSummarizer
├── 📄 main.py                      # Main entry point for the Flask app
├── ⚙️ config.py                    # Configuration settings for API keys, formats, languages
├── 🤖 universal_summarizer_agent.py # Core AI summarization logic and content extraction
├── 🌐 web_app.py                   # Flask web application with API routes
├── 📋 requirements.txt             # Python dependencies
├── 📦 install.bat                  # Windows installation script
├── 🚀 start.bat                    # Windows startup script to run web_app.py
├── 📚 templates/                   # HTML templates for the UI
│   └── index.html                 # Main interface for summarization
├── 📄 .env.example                 # Example file for environment variables
└── 📄 README.md                    # This comprehensive documentation
```

### 🔧 Technical Stack

| Component        | Technology          | Purpose                                  |
|------------------|---------------------|------------------------------------------|
| **Backend**      | Python 3.8+         | Core application logic                   |
| **AI Engine**    | Google Gemini API   | Universal content summarization          |
| **Web Framework**| Flask               | REST API and web server                  |
| **Template Engine**| Jinja2              | HTML template rendering                  |
| **Frontend**     | HTML5, CSS3, JavaScript | Modern, responsive UI with interactive elements |
| **Styling**      | Bootstrap 5, Custom CSS | Responsive design and aesthetic enhancements |
| **File Parsing** | requests, BeautifulSoup4, python-docx, PyPDF2 | Content extraction from URLs and files |
| **Environment**  | python-dotenv       | Environment variable management          |
| **PDF Generation** | ReportLab           | Generating PDF summaries                 |

### 🎯 Key Components

#### 🤖 UniversalSummarizerAgent (`universal_summarizer_agent.py`)
- **Core AI Logic**: Integrates with Google Gemini API.
- **Summarization**: Generates concise summaries based on prompt, format, and language.
- **Content Extraction**: Handles parsing text from various sources (URL, PDF, DOCX, TXT).

#### 🌐 Web Application (`web_app.py`)
- **Flask Routes**: Manages `/`, `/summarize`, and `/download` endpoints.
- **UI Rendering**: Renders `index.html` with dynamic content.
- **API Handling**: Processes summarization requests and file downloads.

#### 🎨 Frontend (`templates/index.html`)
- **Interactive UI**: Allows users to input content, select options, and view summaries.
- **Dark/Light Mode**: Provides a toggle for theme switching.
- **Responsive Design**: Ensures usability across all devices.

#### ⚙️ Configuration (`config.py`)
- **Centralized Settings**: Defines API key, model parameters, supported languages, and summary formats.

## ⚙️ Configuration & Setup

### 🔑 API Key Setup

**Step 1: Get Google Gemini API Key**
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign up or log in to your Google account.
3. Create a new API key.
4. Copy the generated API key (starts with `AIza...`).

**Step 2: Configure the Key**

Create a `.env` file in the `56_EmailSummarizer` directory with your API key:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

*   **Important**: Do NOT commit your `.env` file to version control. The `.gitignore` file is already configured to ignore it.

### 🎛️ Advanced Configuration

Edit `config.py` to customize application settings:

```python
# AI Model Settings
MODEL_NAME = "gemini-1.5-flash"  # Or another suitable Gemini model
TEMPERATURE = 0.7                # Creativity level (0.0-1.0)
MAX_TOKENS = 1500                # Maximum output tokens for summary

# Language Options
# Add or remove languages as needed
LANGUAGE_OPTIONS = {
    "English": "en",
    "Urdu": "ur",
    "Hindi": "hi"
}

# Summary Formats
# Customize or add new summary formats
SUMMARY_FORMATS = {
    "Bullet Points": "bullet_points",
    "Key Takeaways": "key_takeaways",
    "Executive Summary": "executive_summary",
    "Action Items Only": "action_items_only"
}
```

## 🧪 Testing & Quality Assurance

### 🔍 Installation Testing

After running `install.bat`, manually verify the following:

-   ✅ Python virtual environment is created and activated.
-   ✅ All dependencies listed in `requirements.txt` are installed without errors.
-   ✅ `.env` file is created (or environment variable is set) with your `GEMINI_API_KEY`.

### 🚀 Functional Testing

1.  **Launch the Web UI**: Run `start.bat` and navigate to `http://127.0.0.1:5000`.
2.  **Test Text Summarization**: Paste a long text, choose a format/language, and summarize.
3.  **Test URL Summarization**: Provide a public URL (e.g., a news article), choose a format/language, and summarize.
4.  **Test File Uploads**: Upload a `.txt`, `.pdf`, and `.docx` file, and test summarization for each.
5.  **Test Download**: Verify that both PDF and TXT download options work correctly.
6.  **Test Dark/Light Mode**: Toggle the theme and ensure all UI elements adapt correctly.

### 🐛 Troubleshooting

**Common Issues & Solutions:**

| Issue                               | Cause                               | Solution                                         |
|-------------------------------------|-------------------------------------|--------------------------------------------------|
| **"API key not found"**           | Missing or invalid `GEMINI_API_KEY` | Ensure `.env` file is correct or API key is set as environment variable. |
| **"Error fetching URL"**          | Invalid URL or network issue        | Check the URL and your internet connection.        |
| **"Error reading PDF/DOCX file"** | Corrupted/unsupported file or library issue | Ensure file is valid; check `requirements.txt` dependencies are installed. |
| **"Content is required."**        | No input provided                   | Ensure text, URL, or file content is provided.   |
| **"Port already in use"**         | Flask default port (5000) is occupied | Restart your system or use a different port (advanced Flask configuration). |

## 🔮 Future Roadmap

### 🚀 Planned Features

| Feature                        | Status     | Description                                     |
|--------------------------------|------------|-------------------------------------------------|
| **Auto Language Detection**    | 🔄 Planned | Automatically detect content language.          |
| **Tone Analysis & Adaptation** | 🔄 Planned | Analyze content tone and adapt summary style.   |
| **Image/OCR Support**          | 🔄 Planned | Extract text from images and summarize.         |
| **Batch Summarization**        | 🔄 Planned | Process multiple files/URLs at once.            |
| **Summarization History**      | 🔄 Planned | Store and retrieve past summaries.              |
| **User Authentication**        | 🔄 Planned | Secure user accounts and personalized settings. |

### 🎯 Enhancement Ideas

-   **Advanced Summarization Models**: Integrate with more specialized models for specific content types.
-   **Custom Summary Prompts**: Allow users to define their own custom AI prompts.
-   **Integration with Cloud Storage**: Direct summarization from Google Drive, Dropbox, etc.
-   **Semantic Search on Summaries**: Enable searching through generated summaries.
-   **Mobile Application**: Develop native mobile apps for on-the-go summarization.

## 🤝 Contributing

We welcome contributions to make UniversalSummarizerAgent even better!

### 🛠️ How to Contribute

1.  **Fork the repository**.
2.  **Create a feature branch**: `git checkout -b feature/your-feature-name`.
3.  **Make your changes** and test thoroughly.
4.  **Commit your changes**: `git commit -m 'feat: Add amazing new summarization feature'`.
5.  **Push to the branch**: `git push origin feature/your-feature-name`.
6.  **Open a Pull Request** with a clear description of your changes.

### 🎯 Areas for Contribution

-   **UI/UX Improvements**: Further enhance the user interface and experience.
-   **New Content Type Parsers**: Add support for more file formats (e.g., markdown, epub).
-   **Language Support**: Expand the list of supported languages.
-   **Performance Optimization**: Improve summarization speed and efficiency.
-   **Error Handling**: Make error messages even more user-friendly and robust.

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

-   **Google Gemini API** for powerful AI summarization capabilities.
-   **Flask** for the lightweight and flexible web framework.
-   **Bootstrap** and **Font Awesome** for UI components and icons.
-   **The Python community** for a rich ecosystem of libraries.
-   **All contributors** who help improve this project.

### 🌟 Inspiration

This project was inspired by the need for a versatile summarization tool that is:

-   **Universal**: Capable of handling diverse content types.
-   **Intelligent**: Powered by advanced AI for high-quality summaries.
-   **User-Friendly**: Featuring a modern and intuitive interface.
-   **Productive**: Saving time and improving focus for users.

---

<div align="center">

## 🎉 Ready to Summarize Smarter?

**Transform how you consume information with the power of AI!**

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [🎭 Examples](#-examples) • [📚 Documentation](#-documentation)

---

**Made with ❤️ by the #100DaysOfAI-Agents community**

*Day 56 of 100 - Building the future of AI agents, one day at a time!*

</div>

