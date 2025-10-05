# 📝 TextCleanerAgent - Day 64 of #100DaysOfAI-Agents

<div align="center">

![TextCleanerAgent Banner](https://img.shields.io/badge/TextCleanerAgent-Day%2064-blue?style=for-the-badge&logo=markdown&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-API-red?style=for-the-badge&logo=google&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-lightgrey?style=for-the-badge&logo=flask&logoColor=white)

**Transform messy text into polished, grammatically correct, and well-formatted content with AI.**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎭 Examples](#-examples) • [📚 Documentation](#-documentation) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is TextCleanerAgent?

TextCleanerAgent is an intelligent AI-powered assistant designed to take messy, unstructured, or poorly written text and transform it into a polished, grammatically correct, and well-formatted version. Powered by Google's Gemini API, this agent enhances readability and coherence while strictly maintaining the original meaning of the content. It supports various input types, including plain text, `.txt` and `.docx` files, and URLs.

### 🌟 Key Highlights

- **✅ Grammar & Spelling Correction**: Automatically identifies and rectifies grammatical errors, punctuation mistakes, and spelling errors.
- **✅ Sentence Structure Improvement**: Enhances sentence flow, coherence, and overall readability.
- **✅ Unnecessary Element Removal**: Eliminates extraneous symbols, excessive line breaks, and other clutter.
- **✅ Meaning Preservation**: Ensures that the core message and original intent of the text remain intact.
- **✅ Clean Formatting**: Organizes content into well-structured, readable paragraphs.

## 🎯 Features

### 🚀 Core Functionality
- ✅ **AI-Powered Text Cleaning**: Utilizes Google's Gemini API for advanced text processing.
- ✅ **Multi-Format Input**: Supports plain text, `.txt` files, `.docx` files, and URLs.
- ✅ **Coherence Enhancement**: Improves sentence structure and overall text flow.
- ✅ **Error Correction**: Fixes grammar, punctuation, and spelling with high accuracy.
- ✅ **Output Formatting**: Presents cleaned text in well-structured paragraphs.

### 💻 User Interfaces
- ✅ **Modern Web UI**: Provides an intuitive and responsive web-based interface.
- ✅ **Flexible CLI**: Offers a powerful command-line interface for scripting and direct use.
- ✅ **Real-time Feedback**: Displays results instantly in both interfaces.

### 📊 Optional Features
- ✅ **Summarization**: Generates a concise summary of the cleaned text upon request.
- ✅ **Before/After Comparison**: Shows both the original and cleaned versions for easy review.
- ✅ **Multi-language Handling**: Processes and cleans text in various languages with an English fallback.

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.8+** installed on your system
- **Google Gemini API Key** (get one from [Google AI Studio](https://ai.google.dev/))
- **Internet connection** for AI text cleaning and URL fetching

### 🔧 Manual Installation

```bash
# 1. Clone or download the project
git clone <repository-url>
cd 64_TextCleanerAgent

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up environment
echo GEMINI_API_KEY=your_gemini_api_key_here > .env
# For Flask web app, also set a secret key (optional but recommended)
echo FLASK_SECRET_KEY=a_strong_random_secret_key > .env
```

### 🎯 First Run

```bash
# Option 1: Web Interface (Recommended)
python -m 64_TextCleanerAgent.main --mode web
# Open: http://127.0.0.1:5000/ (default Flask port)

# Option 2: Command-Line Interface
# Clean text directly
python -m 64_TextCleanerAgent.main --mode cli --text "This sentence has som misstakes and bad grammer."

# Clean text from a file (e.g., sample.txt)
# python -m 64_TextCleanerAgent.main --mode cli --file "path/to/your/sample.txt" --diff

# Clean text from a URL
# python -m 64_TextCleanerAgent.main --mode cli --url "https://www.example.com/article.html" --summarize
```

## 🎭 Examples & Usage

### 🌐 Web Interface

The web interface offers a user-friendly way to clean and enhance text:

1.  **📝 Input Text**: Enter text directly, upload a `.txt` or `.docx` file, or provide a URL.
2.  **⚙️ Select Options**: Choose to summarize the cleaned text or view a before/after comparison.
3.  **🚀 Clean Text**: Click "Clean Text" to process your input.
4.  **👁️ View Results**: See the polished text, and optionally, its summary or the original-to-cleaned diff.

### 💻 Command-Line Interface

The CLI provides flexibility for integrating TextCleanerAgent into scripts or for quick, direct use.

```bash
# Basic text cleaning
python -m 64_TextCleanerAgent.main --mode cli --text "hello world this is a very messy sentence with many  errors. ! ! "

# Cleaning text with summarization
python -m 64_TextCleanerAgent.main --mode cli --text "The quick brown fox jumps over the lazy dog. This is a very common sentence used for testing. It contains all letters of the alphabet." --summarize

# Cleaning text from a .txt file and showing the difference
# Assuming you have a file named 'sample.txt' in the same directory
# python -m 64_TextCleanerAgent.main --mode cli --file "sample.txt" --diff

# Cleaning text from a .docx file
# Assuming you have a file named 'document.docx' in the same directory
# python -m 64_TextCleanerAgent.main --mode cli --file "document.docx"

# Cleaning content from a URL
# python -m 64_TextCleanerAgent.main --mode cli --url "https://www.gutenberg.org/files/1342/1342-h/1342-h.htm" --summarize --diff
```

## 🏗️ Project Architecture

### 📁 File Structure

```
64_TextCleanerAgent/
├── 📄 main.py                   # Main entry point with CLI/Web mode selection
├── ⚙️ config.py                 # Configuration and settings management
├── 🤖 text_cleaner_agent.py     # Core AI text cleaning and processing logic
├── 🌐 web_app.py                # Flask web application with routes and logic
├── 📋 requirements.txt          # Python dependencies
├── 📚 templates/                # HTML templates for the web interface
│   └── index.html              # Main page for text cleaning
├── 🎨 static/                   # Static assets
│   └── style.css               # Stylesheet for the web interface
└── 📄 README.md                # This comprehensive documentation
```

### 🔧 Technical Stack

| Component       | Technology          | Purpose                             |
|-----------------|---------------------|-------------------------------------|
| **Backend**     | Python 3.8+         | Core application logic              |
| **AI Engine**   | Google Gemini API   | Text cleaning, grammar, summarization |
| **Web Framework** | Flask               | Web application and routing         |
| **HTML Parsing**| BeautifulSoup       | Extracting text from URLs           |
| **DOCX Handling**| python-docx         | Reading .docx file content          |
| **Environment** | python-dotenv       | Managing environment variables      |
| **Template Engine** | Jinja2            | HTML template rendering             |
| **Frontend**    | HTML5, CSS3         | User interface for web app          |

## ⚙️ Configuration & Setup

### 🔑 API Key Setup

**Step 1: Get Google Gemini API Key**
1. Visit [Google AI Studio](https://ai.google.dev/)
2. Sign up or log in to your Google account.
3. Navigate to "Get API Key" or similar section.
4. Create a new API key.
5. Copy the generated key.

**Step 2: Configure the Key**

```bash
# Option 1: Environment Variable (Recommended for production)
# Windows
set GEMINI_API_KEY=your_gemini_api_key_here

# Linux/Mac
export GEMINI_API_KEY=your_gemini_api_key_here

# Option 2: .env File (Recommended for development)
# Create a .env file in the 64_TextCleanerAgent directory:
echo GEMINI_API_KEY=your_gemini_api_key_here > .env

# For Flask web app, also set a secret key (optional but recommended for security)
echo FLASK_SECRET_KEY=a_strong_random_secret_key >> .env
```

### 🎛️ Advanced Configuration

Edit `config.py` to customize application settings:

```python
# 64_TextCleanerAgent/config.py

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "supersecretkey")
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'txt', 'docx'}
```

- `GEMINI_API_KEY`: Your Google Gemini API key.
- `FLASK_SECRET_KEY`: A secret key for Flask application security (important for session management).
- `UPLOAD_FOLDER`: Directory to temporarily store uploaded files.
- `ALLOWED_EXTENSIONS`: File extensions permitted for upload (currently `.txt`, `.docx`).

## 🤝 Contributing

We welcome contributions to make TextCleanerAgent even better!

### 🛠️ How to Contribute

1.  **Fork the repository**
2.  **Create a feature branch**: `git checkout -b feature/your-feature-name`
3.  **Make your changes** and test thoroughly
4.  **Commit your changes**: `git commit -m 'Add your feature'`
5.  **Push to the branch**: `git push origin feature/your-feature-name`
6.  **Open a Pull Request**

### 🎯 Areas for Contribution

- **New Input Formats**: Add support for more file types (e.g., PDF).
- **Language Support**: Enhance multi-language cleaning capabilities.
- **UI Improvements**: Improve the web interface design and responsiveness.
- **Performance**: Optimize text processing and API calls.
- **Documentation**: Enhance guides and examples.
- **Testing**: Add more unit and integration tests.
- **Bug Fixes**: Report and fix any identified issues.

### 📋 Contribution Guidelines

- Follow the existing code style.
- Add tests for new features.
- Update documentation as needed.
- Ensure all tests pass.
- Be respectful and constructive.

## 📞 Support & Community

### 🆘 Getting Help

1.  **📖 Documentation**: Check this README and code comments.
2.  **🔍 Troubleshooting**: Review common issues and solutions.
3.  **📊 Logs**: Check console output for error messages.
4.  **🌐 API Status**: Verify Google Gemini API is operational.

### 🐛 Reporting Issues

When reporting issues, please include:

- **System Information**: OS, Python version, browser.
- **Error Messages**: Full error output.
- **Steps to Reproduce**: What you were doing when it happened.
- **Expected vs Actual**: What you expected vs what happened.

### 💬 Community

- **GitHub Issues**: Report bugs and request features.
- **Discussions**: Ask questions and share ideas.

## 📄 License & Credits

### 📜 License

This project is part of the **#100DaysOfAI-Agents** challenge by **Muhammad Sami Asghar Mughal**.

**MIT License** - Feel free to use, modify, and distribute!

### 🙏 Acknowledgments

- **Google** for providing the Gemini API.
- **Flask** team for the excellent web framework.
- **Python community** for amazing libraries.
- **All contributors** who help improve this project.

### 🌟 Inspiration

This project was inspired by the need for intelligent tools that can effortlessly refine and enhance written content, making it accessible and efficient for everyone.

---

<div align="center">

## 🎉 Ready to Polish Your Text?

**Transform your raw text into clear, concise, and professional content with the power of AI!**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎭 Examples](#-examples) • [📚 Documentation](#-documentation)

---

**Made with ❤️ by the #100DaysOfAI-Agents community**

*Day 64 of 100 - Building the future of AI agents, one day at a time!*

</div>
