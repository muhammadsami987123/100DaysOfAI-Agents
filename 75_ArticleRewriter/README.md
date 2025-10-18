# 📝 ArticleRewriter - Day 75 of #100DaysOfAI-Agents

<div align="center">

![ArticleRewriter Banner](https://img.shields.io/badge/ArticleRewriter-Day%2075-blue?style=for-the-badge&logo=edit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![AI Models](https://img.shields.io/badge/AI-Gemini%202.0%20%7C%20OpenAI-orange?style=for-the-badge&logo=google&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20Framework-red?style=for-the-badge&logo=fastapi&logoColor=white)

**Transform your content with AI-powered tone and style rewriting**

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [🌐 UI](#-web-interface) • [🔌 API](#-api) • [⚙️ Config](#%EF%B8%8F-configuration--setup) • [🧪 Troubleshooting](#-troubleshooting)

</div>

---

## ✨ What is ArticleRewriter?

ArticleRewriter is an intelligent AI-powered tool that transforms any text content into different writing tones and styles while preserving the original meaning and key information. Whether you need to make casual content more formal, add personality to business writing, or simplify complex technical content, ArticleRewriter has you covered.

### 🌟 Key Highlights

- **🎯 Multiple Tone Options**: 7 different writing tones (Formal, Casual, Professional, Witty, Poetic, Persuasive, Simplified)
- **🌍 Multi-Language Support**: Rewrite in English, Urdu, Spanish, French, German, and Arabic
- **🔄 Multiple Variations**: Generate 2-3 alternative versions of your rewritten content
- **💾 Save & Download**: Save rewrites in TXT or Markdown format
- **🎨 Modern UI**: Beautiful, responsive interface with glassmorphic design
- **⚡ Fast Processing**: Quick AI-powered content transformation

## 🎯 Features

### 🚀 Core Functionality
- ✅ **AI-Powered Rewriting**: Uses Gemini 2.0 Flash or OpenAI GPT-4o-mini for intelligent content transformation
- ✅ **Tone Adaptation**: Transform content to 7 different writing styles
- ✅ **Language Support**: Rewrite content in 6 different languages
- ✅ **Variation Generation**: Get 2-3 alternative versions of rewritten content
- ✅ **Content Preservation**: Maintains original meaning and key information
- ✅ **File Management**: Save and download rewritten content

### 💻 User Interface
- ✅ **Modern Design**: Glassmorphic UI with smooth animations
- ✅ **Responsive Layout**: Works perfectly on desktop, tablet, and mobile
- ✅ **Real-time Feedback**: Live word and character count
- ✅ **Example Content**: Pre-loaded examples to get started quickly
- ✅ **Copy & Download**: Easy content copying and file downloading
- ✅ **Toast Notifications**: User-friendly success and error messages

### 🔌 Backend & AI
- ✅ **FastAPI Backend**: High-performance async API endpoints
- ✅ **Dual AI Integration**: Gemini 2.0 Flash or OpenAI GPT-4o-mini for intelligent content rewriting
- ✅ **Error Handling**: Comprehensive error handling and fallback responses
- ✅ **File Storage**: Organized output file management

## 🚀 Quick Start

### 📋 Prerequisites
- Python 3.8+
- Gemini API key (get one from [Google AI Studio](https://aistudio.google.com/app/apikey)) OR OpenAI API key (get one from [OpenAI Platform](https://platform.openai.com/api-keys))

### ⚡ Installation

#### Option 1: One-Click Installation (Windows)
```bash
# Run the installer
install.bat

# The installer will:
# ✅ Check Python installation
# ✅ Create virtual environment
# ✅ Install all dependencies
# ✅ Create .env file template
# ✅ Run installation tests
```

#### Option 2: Manual Installation
```bash
# 1. Navigate to the project directory
cd 75_ArticleRewriter

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
# Create .env file with your API key (Gemini or OpenAI)
echo LLM_MODEL=gemini > .env
echo GEMINI_API_KEY=your_gemini_api_key_here >> .env
echo OPENAI_API_KEY=your_openai_api_key_here >> .env
echo DEBUG=True >> .env
```

### 🎯 First Run

#### Option 1: Web Interface (Recommended)
```bash
# Windows
start.bat

# Linux/Mac
source venv/bin/activate
python main.py

# Open your browser to:
# http://localhost:8075
```

#### Option 2: Direct Python
```bash
python main.py
```

### 🧪 Verify Installation
```bash
# Run the test suite
python test_installation.py

# Expected output:
# ✅ Python version compatible
# ✅ All dependencies installed
# ✅ Configuration loaded
# ✅ ArticleRewriterAgent initialized
# ✅ Web app ready
```

## 🌐 Web Interface

The web interface provides an intuitive experience for content rewriting:

1. **📝 Enter Content**: Paste your article, blog post, or any text content
2. **🎨 Choose Tone**: Select from 7 different writing tones
3. **🌍 Pick Language**: Choose from 6 supported languages
4. **⚙️ Set Options**: Toggle variations generation on/off
5. **🚀 Rewrite**: Click "Rewrite Content" to transform your text
6. **📋 Copy/Download**: Copy to clipboard or download as file

### 🎨 Available Tones

| Tone | Description | Best For |
|------|-------------|----------|
| **Formal** | Professional, academic language | Business reports, academic papers |
| **Casual** | Conversational, friendly tone | Blogs, social media, personal content |
| **Professional** | Business-focused, authoritative | Corporate communications, reports |
| **Witty** | Humorous, engaging with personality | Creative content, entertainment |
| **Poetic** | Artistic, flowing, expressive | Creative writing, artistic content |
| **Persuasive** | Compelling, sales-oriented | Marketing, sales content |
| **Simplified** | Clear, easy-to-understand | Educational content, general audiences |

### 🌍 Supported Languages

- **English** - Default language
- **Urdu (اردو)** - Urdu language support
- **Spanish (Español)** - Spanish language support
- **French (Français)** - French language support
- **German (Deutsch)** - German language support
- **Arabic (العربية)** - Arabic language support

## 🔌 API

### Endpoints

#### Rewrite Content
```
POST /api/rewrite
```

**Request:**
```json
{
  "content": "The weather is nice today. I think we should go for a walk in the park.",
  "tone": "formal",
  "language": "english",
  "generate_variations": true
}
```

**Response:**
```json
{
  "success": true,
  "rewritten_content": "The current weather conditions are favorable. I recommend that we proceed with a walk in the park.",
  "variations": [
    "The weather is quite pleasant today. I suggest we take a stroll in the park.",
    "Today's weather is excellent. I believe a walk in the park would be beneficial."
  ],
  "metadata": {
    "original_length": 89,
    "rewritten_length": 95,
    "tone": "formal",
    "language": "english",
    "timestamp": "2025-01-18T23:10:00",
    "word_count": 18,
    "variations_count": 2
  },
  "error": null
}
```

#### Save Content
```
POST /api/save
```

#### Get Available Tones
```
GET /api/tones
```

#### Get Available Languages
```
GET /api/languages
```

#### Download File
```
GET /api/download/{filename}
```

#### Health Check
```
GET /api/health
```

## 🏗️ Project Structure

```
75_ArticleRewriter/
├── main.py                           # FastAPI application entry point
├── config.py                         # Configuration and settings
├── agents/
│   └── article_rewriter_agent.py     # Core AI rewriting logic
├── templates/
│   └── index.html                    # Main web interface
├── static/
│   └── js/
│       └── app.js                    # Frontend JavaScript
├── prompts/
│   └── tone_prompt.txt               # AI prompt templates
├── outputs/                          # Generated rewrite files
├── requirements.txt                  # Python dependencies
├── install.bat                       # Windows installation script
├── start.bat                         # Windows startup script
├── test_installation.py              # Installation test suite
└── README.md                         # This documentation
```

## ⚙️ Configuration & Setup

### Environment Variables

Create a `.env` file in the project root:

```env
# Choose your preferred LLM model: "gemini" or "openai"
LLM_MODEL=gemini

# Gemini Configuration (if using Gemini)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash

# OpenAI Configuration (if using OpenAI)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# Server Configuration
DEBUG=True
HOST=0.0.0.0
PORT=8075
```

### API Key Setup

#### Option 1: Gemini API (Recommended)
1. **Get Gemini API Key**:
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Sign up or log in
   - Create a new API key
   - Copy the key

2. **Add to .env file**:
   ```env
   LLM_MODEL=gemini
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

#### Option 2: OpenAI API
1. **Get OpenAI API Key**:
   - Visit [OpenAI Platform](https://platform.openai.com/api-keys)
   - Sign up or log in
   - Create a new API key
   - Copy the key (starts with `sk-`)

2. **Add to .env file**:
   ```env
   LLM_MODEL=openai
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

### Customization

You can customize the available tones and languages by modifying `config.py`:

```python
# Add new tones
TONES = {
    "your_tone": {
        "name": "Your Tone",
        "description": "Description of your tone",
        "keywords": ["keyword1", "keyword2"]
    }
}

# Add new languages
LANGUAGES = {
    "your_lang": {
        "name": "Your Language",
        "code": "yl",
        "description": "Description of your language"
    }
}
```

## 🧪 Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| **"No OpenAI API key"** | Missing API key | Set `OPENAI_API_KEY` in .env file |
| **"Failed to rewrite content"** | API quota exceeded | Check OpenAI usage and billing |
| **"Module not found"** | Missing dependencies | Run `pip install -r requirements.txt` |
| **"Port already in use"** | Port 8075 occupied | Change port in config or kill process |
| **"Content not loading"** | JavaScript errors | Check browser console for errors |

### Debug Mode

Enable debug mode by setting `DEBUG=True` in your `.env` file for detailed logging.

### Performance Tips

- **Content Length**: For best results, keep content under 2000 words
- **API Limits**: Monitor your OpenAI API usage and billing
- **Caching**: Consider implementing caching for frequently rewritten content

## 💡 Usage Examples

### Example 1: Casual to Formal
**Input (Casual):**
> "The weather is nice today. I think we should go for a walk in the park."

**Output (Formal):**
> "The current weather conditions are favorable. I recommend that we proceed with a walk in the park."

### Example 2: Professional to Witty
**Input (Professional):**
> "Our company has achieved significant growth this quarter. We increased revenue by 25% and expanded our customer base."

**Output (Witty):**
> "Well, well, well! Look who's been busy making money moves! Our company just pulled off a spectacular quarter, boosting revenue by a whopping 25% and welcoming a whole bunch of new customers to the party."

### Example 3: Technical to Simplified
**Input (Technical):**
> "The new software update includes several bug fixes and performance improvements. Users will notice faster loading times and fewer crashes."

**Output (Simplified):**
> "The new software update fixes problems and makes things work better. Your apps will load faster and crash less often."

## 🔮 Future Enhancements

### Planned Features
- **Batch Processing**: Rewrite multiple documents at once
- **Custom Tone Training**: Train AI on your specific writing style
- **Integration APIs**: Connect with popular content management systems
- **Advanced Analytics**: Track rewriting patterns and improvements
- **Collaborative Features**: Share and collaborate on rewrites
- **Template Library**: Pre-built templates for common content types

## 🤝 Contributing

We welcome contributions to make ArticleRewriter even better!

### 🛠️ How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes** and test thoroughly
4. **Commit your changes**: `git commit -m 'Add your feature'`
5. **Push to the branch**: `git push origin feature/your-feature-name`
6. **Open a Pull Request**

### 🎯 Areas for Contribution

- **New Tones**: Add more writing styles and tones
- **Language Support**: Add support for more languages
- **UI Improvements**: Enhance the user interface
- **Performance**: Optimize AI processing speed
- **Documentation**: Improve guides and examples
- **Testing**: Add more comprehensive tests

## 📄 License & Credits

### 📜 License

This project is part of the **#100DaysOfAI-Agents** challenge by **Muhammad Sami Asghar Mughal**.

**MIT License** - Feel free to use, modify, and distribute!

### 🙏 Acknowledgments

- **OpenAI** for providing the powerful GPT-4o-mini model
- **FastAPI** team for the excellent web framework
- **Tailwind CSS** for the beautiful styling system
- **Python community** for the rich ecosystem of libraries

---

**Built with ❤️ for Day 75 of 100 Days of AI Agents**

*Transform your content with the power of AI!*
