# 🔗 URLShortenerBot - Day 55 of #100DaysOfAI-Agents

<div align="center">

![URLShortenerBot Banner](https://img.shields.io/badge/URLShortenerBot-Day%2055-blue?style=for-the-badge&logo=link&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-red?style=for-the-badge&logo=flask&logoColor=white)

**Instantly create clean, trackable short links from long URLs with AI-powered efficiency**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎭 Examples](#-examples) • [📚 Documentation](#-documentation) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is URLShortenerBot?

URLShortenerBot is an intelligent assistant designed to streamline the process of shortening long URLs using public shortening APIs like TinyURL. It provides a user-friendly interface to generate clean, trackable short links, with advanced features such as custom aliases, QR code generation, and direct clipboard integration. This tool is perfect for developers, marketers, and content creators who need efficient URL management.

### 🌟 Key Highlights

- **🔗 Public API Integration**: Currently supports TinyURL (extendable to Bitly, shrtco.de, etc.)
- **✍️ Custom Aliases**: Create memorable short links (if supported by API)
- **📷 QR Code Generation**: Instantly generate QR codes for easy sharing
- **📋 Clipboard Integration**: One-click copy of shortened URLs
- **🌙 Dark/Light Mode**: Aesthetic UI toggle for preferred viewing
- **🌍 Multilingual Support**: Ready for Urdu, Hindi, English, and more
- **🚀 Dual Interface**: Intuitive web UI and powerful CLI mode
- **📊 Click Tracking (Mocked)**: Placeholder for future analytics integration

## 🎯 Features

### 🚀 Core Functionality

- ✅ **URL Shortening**: Convert long URLs into concise, shareable links
- ✅ **API Flexibility**: Easily switch between or integrate multiple shortening services
- ✅ **Real-time Feedback**: Instant display of shortened links and messages
- ✅ **Responsive Design**: Adapts beautifully to all screen sizes (desktop, tablet, mobile)
- ✅ **Loading States**: Visual feedback during API calls for a smooth UX

### 🎭 Creative Options

- ✅ **Customizable Aliases**: Personalize your short links for branding or memorability
- ✅ **QR Code Generation**: Enhance shareability with scannable QR codes
- ✅ **Language Selection**: Choose interface language (English, Urdu, Hindi implemented)
- ✅ **Theme Toggle**: Switch between elegant light and dark modes

### 💻 User Interfaces

- ✅ **Modern Web UI**: Sleek, intuitive, and interactive web interface with smooth transitions
- ✅ **Functional CLI Mode**: For quick, scriptable URL shortening via command line

### 📊 Management & Analytics

- ✅ **Clipboard Integration**: Automatically copy results to clipboard
- ✅ **Download Options (Future)**: Placeholder for downloading QR codes or short links
- ✅ **Mock Tracking**: Simulated click tracking (ready for real integration)

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.8+** installed on your system
- **TinyURL API Key** (get one from [TinyURL Developer Dashboard](https://tinyurl.com/app/dashboard/api)) if using TinyURL
- **Internet connection** to reach the shortening API

### 🔧 Manual Installation

```bash
# 1. Clone or download the project
git clone <repository-url>
cd 55_URLShortenerBot

# 2. Create virtual environment (if not already done)
python -m venv venv

# 3. Activate virtual environment
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up API key (for TinyURL)
# Create a .env file in the project root and add your TinyURL API Key:
# TINYURL_API_KEY=your_actual_tinyurl_api_key_here
```

### 🎯 First Run

```bash
# Option 1: Web Interface (Recommended)
python main.py
# Open your browser to: http://127.0.0.1:5000

# Option 2: Terminal Interface
python main.py --url https://www.example.com/long-url --alias my-alias --copy --qr
```

### 🧪 Verify Installation

```bash
# Run the test suite
pytest test_url_shortener.py
```

## 🎭 Examples & Usage

### 🌐 Web Interface

1.  **Enter Long URL**: Paste the URL you want to shorten.
2.  **Add Custom Alias (Optional)**: Provide a custom keyword for your short link.
3.  **Select Options**: Choose to copy to clipboard or generate a QR code.
4.  **Shorten**: Click the "Shorten URL" button and see the results instantly.

### 💻 Terminal Interface

```bash
# Basic shortening
python main.py --url "https://www.example.com/long-page"

# With custom alias and copy to clipboard
python main.py --url "https://www.example.com/another-long-url" --alias mycustomlink --copy

# With QR code generation
python main.py --url "https://www.example.com/qr-test" --qr
```

## 🏗️ Project Architecture

### 📁 File Structure

```
55_URLShortenerBot/
├── 📄 main.py                   # Entry point for UI and CLI modes
├── ⚙️ config.py                 # Configuration settings (API keys, defaults)
├── 🤖 url_shortener_agent.py    # Core URL shortening and QR generation logic
├── 🌐 web_app.py                # Flask web application routes and logic
├── 📋 requirements.txt          # Python dependencies
├── 🧪 test_url_shortener.py     # Unit and integration tests
├── 📚 templates/                # HTML templates for the web UI
│   └── index.html              # Main web application page
├── 🎨 static/                   # Static assets (CSS, JS, images)
│   ├── css/
│   │   └── style.css           # Modern, responsive CSS styling
│   └── js/
│       └── app.js              # Frontend interactivity and AJAX calls
├── 🖼️ .env                      # Environment variables (for API keys - **DO NOT COMMIT**)
└── 📄 README.md                # This comprehensive documentation
```

### 🔧 Technical Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Python 3.8+ | Core application logic |
| **Web Framework** | Flask | Web server and API endpoints |
| **API Integration** | Requests | HTTP requests to external shortening APIs |
| **QR Codes** | qrcode, Pillow | QR code generation |
| **Environment Vars** | python-dotenv | Secure API key management |
| **Frontend** | HTML5, CSS3, JavaScript | Modern, responsive UI |
| **Styling** | Custom CSS + Inter/Roboto Mono fonts | High-end visual design |
| **Clipboard** | pyperclip | Cross-platform clipboard access |

## ⚙️ Configuration & Setup

### 🔑 API Key Setup (for TinyURL)

1.  **Get TinyURL API Key**: Sign up at [TinyURL](https://tinyurl.com/) and navigate to your developer dashboard to create an API key.
2.  **Create `.env` file**: In the root of the `55_URLShortenerBot` directory, create a file named `.env`.
3.  **Add your API key**: Inside `.env`, add the following line (replace with your actual key):
    `TINYURL_API_KEY=your_actual_tinyurl_api_key_here`

### 🌍 Language Configuration

Edit `config.py` to customize or add supported languages:

```python
# ... existing code ...
    LANGUAGES = ['en', 'hi', 'ur'] # Add/remove language codes here
    DEFAULT_LANGUAGE = 'en'
# ... existing code ...
```

## 🧪 Testing & Quality Assurance

### 🔍 Running Tests

To run the unit and integration tests:

```bash
pytest test_url_shortener.py
```

**Expected Test Cases:**

-   ✅ Basic URL shortening functionality
-   ✅ Custom alias handling
-   ✅ Invalid URL input handling
-   ✅ QR code generation

## 🤝 Contributing

We welcome contributions to make URLShortenerBot even better!

### 🛠️ How to Contribute

1.  **Fork the repository**.
2.  **Create a feature branch**: `git checkout -b feature/new-api-integration`.
3.  **Make your changes** and test thoroughly.
4.  **Commit your changes**: `git commit -m 'Add Bitly API support'`.
5.  **Push to the branch**: `git push origin feature/new-api-integration`.
6.  **Open a Pull Request**.

### 🎯 Areas for Contribution

-   **New API Integrations**: Add support for other URL shortening services (Bitly, shrtco.de, etc.)
-   **UI/UX Enhancements**: Further refine the user interface and experience.
-   **Advanced Features**: Implement click tracking, analytics dashboards, user accounts.
-   **Localization**: Expand multilingual support with actual translations.
-   **Documentation**: Improve guides and examples.

## 📞 Support & Community

### 🆘 Getting Help

-   **GitHub Issues**: Report bugs and request features.
-   **Documentation**: Refer to this README for setup and usage.
-   **Troubleshooting**: Check terminal logs for error messages.

## 📄 License & Credits

### 📜 License

This project is part of the **#100DaysOfAI-Agents** challenge by **Muhammad Sami Asghar Mughal**.

**MIT License** - Feel free to use, modify, and distribute!

---

<div align="center">

## 🎉 Ready to Shorten URLs?

**Transform your long links into elegant, shareable short URLs!**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎭 Examples](#-examples) • [📚 Documentation](#-documentation)

---

**Made with ❤️ by the #100DaysOfAI-Agents community**

*Day 55 of 100 - Building the future of AI agents, one day at a time!*

</div>
