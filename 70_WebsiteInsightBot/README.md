# 📚 WebsiteInsightBot - Day 70 of #100DaysOfAI-Agents

<div align="center">

![WebsiteInsightBot Banner](https://img.shields.io/badge/WebsiteInsightBot-Day%2070-blue?style=for-the-badge&logo=internetexplorer&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-Flash%202.0-orange?style=for-the-badge&logo=googlegemini&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20Framework-red?style=for-the-badge&logo=fastapi&logoColor=white)

**Analyze any website for deep insights, SEO keywords, and sentiment with AI-powered efficiency!**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎭 Examples](#-examples) • [📚 Documentation](#-documentation) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is WebsiteInsightBot?

WebsiteInsightBot is an intelligent AI agent designed to analyze and summarize the core content of any given website, extracting meaningful insights, SEO keywords, and sentiment in a clean, structured format. It helps you quickly grasp the essence of a webpage, identify critical SEO terms, and understand the overall tone, making it invaluable for content analysis, competitive research, and general information gathering.

### 🌟 Key Highlights

- **🧠 AI-Powered Analysis**: Leverages Google Gemini 2.0 Flash for superior summarization, keyword extraction, and sentiment detection.
- **📝 Flexible Summarization**: Get concise 1-2 paragraph summaries or detailed long-form reports.
- **🔑 SEO Keyword Extraction**: Identifies 5-15 relevant keywords for content optimization.
- **💡 Sentiment Analysis**: Determines if the page's tone is Positive, Negative, or Neutral, with a brief explanation.
- **🌍 Multi-language Support**: Automatically detects non-English content and processes it into English summaries.
- **🛡️ Robust Error Handling**: Gracefully manages unreachable URLs, empty content, and API issues.
- **💻 Modern Web UI**: Features a beautiful, responsive interface with dynamic themes, dark mode, loading animations, and copy-to-clipboard functionality.
- **📊 Site Metadata**: Displays website title and favicon for better context.

## 🎯 Features

### 🚀 Core Functionality
- ✅ **AI Content Extraction**: Retrieves main textual content (skips ads, sidebars, footers).
- ✅ **LLM-driven Summaries**: Generates human-readable summaries using Gemini 2.0 Flash.
- ✅ **Keyword Intelligence**: Extracts relevant SEO-focused keywords.
- ✅ **Tone Detection**: Classifies sentiment (Positive/Negative/Neutral) with reasons.
- ✅ **URL Validation**: Accepts only valid `http/https` URLs.
- ✅ **Real-time Feedback**: Loading indicators and clear error messages.

### 🎭 Customization Options
- ✅ **Summary Length**: Toggle between short (concise) and long-form (detailed) summaries.
- ✅ **Theming**: Select between Blue, Green, or Pink color gradients, plus dark/light mode.
- ✅ **Responsive Design**: Optimized for desktop, tablet, and mobile devices.
- ✅ **About/Tips Modal**: Provides quick usage tips and project info.

### 💻 User Interface Enhancements
- ✅ **Dynamic UI**: Card-style results, icons for clarity, and smooth animations.
- ✅ **Loading Skeletons**: Visual placeholders during content analysis.
- ✅ **Copy Buttons**: Easily copy summary and keywords to clipboard.
- ✅ **Animated Title**: Engaging page title animation.
- ✅ **Rich Footer**: Includes project credits, GitHub, and contact links.
- ✅ **Site Branding**: Displays website title and favicon for analyzed URLs.
- ✅ **API Model Badge**: Clearly indicates the Gemini LLM model in use.
- ✅ **Analysis Timestamp**: Shows when the insights were generated.

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.8+** installed on your system.
- **Google Gemini API Key** (get one from [Google AI Studio](https://makersuite.google.com/)).
- **Internet connection** for website fetching and AI analysis.

### 🔧 Installation

```bash
# 1. Clone the repository
git clone https://github.com/muhammadsami987123/100DaysOfAI-Agents.git
cd 100DaysOfAI-Agents/70_WebsiteInsightBot

# 2. Create and activate a virtual environment
python -m venv venv
# On Windows
vend\Scripts\activate
# On Linux/Mac
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

### 🔑 API Key Setup

**Set your Gemini API key as an environment variable (recommended):**

```bash
# On Windows
$env:GEMINI_API_KEY="your_gemini_api_key_here"

# On Linux/Mac
export GEMINI_API_KEY="your_gemini_api_key_here"
```

### 🎯 First Run

```bash
# 1. Start the web application
uvicorn app:app --reload

# 2. Open your browser
# Navigate to: http://127.0.0.1:8000

# 3. Enter a URL and click "Generate Insights"
```

### 🧪 Run Tests

```bash
# Navigate to the project root (70_WebsiteInsightBot)
pytest tests/
```

## 🎭 Examples & Usage

The web interface is intuitive and easy to use:

1. **Enter URL**: Type or paste any valid `http/https` website URL into the input field.
2. **Choose Summary Length**: Check the "Long-form summary" checkbox for detailed reports.
3. **Generate Insights**: Click the "Generate Insights" button.
4. **View Results**: The summary, keywords, and sentiment will appear in a beautifully formatted card layout.
5. **Customize**: Experiment with Dark Mode and different themes (Blue, Green, Pink).

**🎯 Pro Tips:**
- Use the `copy` buttons to quickly grab the summary or keywords.
- Click the ℹ️ button for quick tips and project info.
- The page title animates during analysis and updates with the website's title.

## 🏗️ Project Architecture

### 📁 File Structure

```
70_WebsiteInsightBot/
├── 📄 app.py                  # FastAPI web application (API and UI serving)
├── 🤖 agent.py                 # Core AI agent logic (Gemini integration, content extraction)
├── 📋 requirements.txt        # Python dependencies
├── 🧪 tests/                   # Automated pytest suite
│   └── test_agent.py           # Tests for the core agent logic
├── 📚 template/                # HTML templates for the UI
│   └── index.html              # Main web interface
└── 📄 README.md                # This documentation file
```

### 🔧 Technical Stack

| Component       | Technology          | Purpose                                  |
|-----------------|---------------------|------------------------------------------|
| **Backend**     | Python 3.8+, FastAPI | Core API and web server                  |
| **AI Engine**   | Google Gemini 2.0 Flash | Summarization, keywords, sentiment       |
| **Web Scraping**| BeautifulSoup4, Requests | HTML parsing and content fetching        |
| **Frontend**    | HTML5, Tailwind CSS, JS | Modern, responsive, interactive UI       |
| **Language Det.**| `langdetect`       | Auto-detects content language            |
| **Server**      | Uvicorn             | ASGI web server                          |

### 🎯 Key Components

#### 🤖 Agent (`agent.py`)
- **LLM Integration**: Communicates with Google Gemini API.
- **Content Processing**: Extracts visible text, handles meta-data (title, favicon).
- **Analysis Orchestration**: Calls LLM for summary, keywords, sentiment.
- **Error Management**: Provides structured errors for UI.

#### 🌐 Web Application (`app.py`)
- **REST API**: Exposes `/analyze` endpoint for insights generation.
- **UI Serving**: Serves `index.html` from the `template` directory.
- **CORS Middleware**: Enables cross-origin requests for development.

#### 🎨 Frontend (`template/index.html`)
- **Dynamic UI**: Renders insights, manages loading/error states.
- **Theming**: Implements dark mode and multiple color gradients.
- **Interactivity**: Handles user input, toggles, copy actions, modals.

## ⚙️ Configuration & Setup

### 🔑 API Key Setup

- **Google Gemini API Key**: Obtain from [Google AI Studio](https://makersuite.google.com/) and set as `GEMINI_API_KEY` environment variable.

### 🎛️ Advanced Configuration

- **LLM Model**: The default LLM model is `gemini-2.0-flash`. This can be adjusted in `agent.py` if other Gemini models are desired and accessible with your API key.
- **Prompt Engineering**: The `PROMPT_FORMAT` in `agent.py` can be modified to fine-tune AI output for specific needs.

## 🧪 Testing & Quality Assurance

### 🔍 Unit Tests (`tests/test_agent.py`)

- **Mocks LLM calls**: Ensures tests run fast without hitting the actual Gemini API.
- **Covers key scenarios**: Valid URL, unreachable site, no valuable content, non-English content, long-form summary.

```bash
# Run all tests
pytest tests/
```

### 🐛 Troubleshooting

| Issue                                | Cause                                     | Solution                                                                |
|--------------------------------------|-------------------------------------------|-------------------------------------------------------------------------|
| **"Gemini API key is missing"**      | `GEMINI_API_KEY` not set.                 | Set environment variable as per [API Key Setup](#-api-key-setup).     |
| **"Gemini API error 404"**           | Incorrect API endpoint or model name.     | Verify `GEMINI_MODEL` in `agent.py` and API key permissions.          |
| **"The website is unreachable"**     | Website is down or blocked.               | Check URL, try another site, or verify internet connection.           |
| **"No valuable content found"**      | Page mostly ads/scripts or protected.    | Try a different page with more text content.                          |
| **Blank UI / Content Missing**       | HTML/CSS rendering issue in browser.      | Open browser DevTools (F12) to check `Console` and `Elements` tabs for errors. Ensure main `div` is not hidden. |
| **"Module not found"**               | Missing Python dependencies.              | Run `pip install -r requirements.txt`.                                  |

## 🤝 Contributing

We welcome contributions to WebsiteInsightBot!

### 🛠️ How to Contribute

1. **Fork the repository**.
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`.
3. **Make your changes** and test thoroughly.
4. **Commit your changes**: `git commit -m 'feat: Add new feature'`.
5. **Push to the branch**: `git push origin feature/your-feature-name`.
6. **Open a Pull Request**.

### 🎯 Areas for Contribution

- **UI/UX Improvements**: Further visual enhancements, new themes.
- **New Features**: Implement additional analysis types (e.g., readability score, entity extraction).
- **LLM Integration**: Support for other LLM providers (e.g., OpenAI, Claude).
- **Testing**: Add more comprehensive test cases.
- **Documentation**: Improve guides and examples.

### 📋 Contribution Guidelines

- Follow existing code style and conventions.
- Add/update tests for new or changed functionality.
- Update documentation as needed.
- Ensure all existing tests pass.

## 📞 Support & Community

- **GitHub Issues**: Report bugs and request features [here](https://github.com/muhammadsami987123/100DaysOfAI-Agents/issues).
- **Email**: sami.developer.official@gmail.com
- **Twitter/X**: [@muhammadsami987](https://twitter.com/muhammadsami987)

## 📄 License & Credits

### 📜 License

This project is part of the **#100DaysOfAI-Agents** challenge by **Muhammad Sami Asghar Mughal**.

**MIT License** - Feel free to use, modify, and distribute!

### 🙏 Acknowledgments

- **Google Gemini** for powering the AI analysis.
- **FastAPI** team for the robust web framework.
- **Tailwind CSS** for simplifying UI development.
- **BeautifulSoup4** and **Requests** for web scraping.
- **All contributors** who help improve this project.

### 🌟 Inspiration

Inspired by the need for quick, insightful web content analysis, this tool aims to make information gathering more efficient and engaging for developers, marketers, and researchers alike.

---

<div align="center">

## 🎉 Ready to Gain Insights?

**Transform any webpage into actionable intelligence with the power of AI!**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎭 Examples](#-examples) • [📚 Documentation](#-documentation)

---

**Made with ❤️ by Muhammad Sami Asghar Mughal as part of the #100DaysOfAI-Agents community**

*Day 70 of 100 - Building the future of AI agents, one day at a time!*

</div>
