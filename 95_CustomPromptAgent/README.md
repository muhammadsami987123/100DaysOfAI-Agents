# 🧾 CustomPromptAgent - Day 95 of #100DaysOfAI-Agents

<div align="center">

![CustomPromptAgent Banner](https://img.shields.io/badge/CustomPromptAgent-Day%2095-6366f1?style=for-the-badge&logo=pen-fancy&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-3776ab?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20Framework-009485?style=for-the-badge&logo=fastapi&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-UI%20Framework-38bdf8?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Gemini 2.0](https://img.shields.io/badge/Gemini_2.0-flash-4285f4?style=for-the-badge&logo=google&logoColor=white)
![OpenAI GPT-4.1](https://img.shields.io/badge/OpenAI-GPT--4.1-412991?style=for-the-badge&logo=openai&logoColor=white)

**Build high-quality AI prompts dynamically with live preview, smart templates, and AI-powered enhancement**

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [🎯 Examples](#-examples) • [🏗️ Architecture](#-project-architecture) • [📞 Support](#-support--community)

</div>

---

## ✨ What is CustomPromptAgent?

CustomPromptAgent is an intelligent prompt engineering assistant that helps you craft better AI prompts through a structured, interactive interface. Whether you're a developer, content creator, or prompt engineer, this tool simplifies the process of building effective prompts for Gemini 2.0-flash or GPT-4.1 through dynamic form inputs and real-time preview.

### 🌟 Key Highlights

- **🎯 Structured Prompt Building**: 6 input fields (role, task, tone, format, audience, context)
- **📊 Live Real-Time Preview**: See your prompt update instantly as you type
- **💾 Smart Template Management**: Save, load, download, and organize prompt blueprints
- **🧠 AI Enhancement**: 5 enhancement types - Balanced, Technical, Creative, Strategic, Educational
- **🎙️ Voice Input Support**: Dictate any field using Web Speech API (Chrome/Edge/Safari)
- **📥 Multi-Format Export**: Download prompts as .txt or .json files
- **🌓 Modern Dark/Light Theme**: Responsive UI with theme persistence
- **⚡ No Authentication Required**: Start building prompts instantly

---

## 🎯 Features

### 🚀 Core Functionality
- ✅ **Dynamic Prompt Builder**: 6 structured input fields for comprehensive prompt design
- ✅ **Real-Time Preview**: Instant live preview as you type without page refresh
- ✅ **Smart Template System**: Save, load, delete, and manage prompt templates
- ✅ **AI Enhancement**: 5 enhancement types (Balanced, Technical, Creative, Strategic, Educational)
- ✅ **Voice Input Support**: Web Speech API integration for hands-free input
- ✅ **Multi-Format Export**: Download as .txt or .json files
- ✅ **Error Handling**: User-friendly error messages and graceful fallbacks

### 🎨 User Experience
- ✅ **Modern Responsive UI**: Built with TailwindCSS for beautiful, mobile-friendly design
- ✅ **Dark/Light Theme**: Toggle between themes with persistent user preference
- ✅ **Real-Time Validation**: Instant feedback on form inputs
- ✅ **Copy to Clipboard**: One-click prompt copying
- ✅ **Visual Feedback**: Loading states, success messages, error alerts
- ✅ **Auto-Focus Elements**: Keyboard navigation support

### 📊 Template Management
- ✅ **Save Templates**: Store prompt blueprints for future reuse
- ✅ **Load Templates**: Quickly populate form with saved configurations
- ✅ **Delete Templates**: Remove unwanted templates
- ✅ **Download Templates**: Export as JSON for backup or sharing
- ✅ **Template Preview**: See saved templates with creation date

### 🧠 LLM Integration
- ✅ **Dual LLM Support**: Gemini 2.0-flash (free) and GPT-4.1 (paid)
- ✅ **Enhancement Focus**: 5 different refinement lenses (balanced, technical, creative, strategic, educational)
- ✅ **Graceful Degradation**: Works without API keys for core features
- ✅ **Error Recovery**: Automatic fallback when LLM unavailable

---

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.9+** installed on your system
- **Gemini API Key** (free - get from [Google AI Studio](https://aistudio.google.com/app/apikey))
- **OpenAI API Key** (optional, paid - get from [OpenAI Platform](https://platform.openai.com/account/api-keys))
- **Internet connection** for AI enhancement features

### ⚡ One-Minute Setup

```bash
# 1. Install dependencies
cd 95_CustomPromptAgent
pip install -r requirements.txt

# 2. Create .env file
echo GEMINI_API_KEY=your_key_here > .env
echo DEFAULT_LLM=gemini >> .env

# 3. Run the server
python main.py

# 4. Open browser
# Visit: http://127.0.0.1:8000
```

### 🔧 Manual Installation

```bash
# 1. Navigate to project
cd 95_CustomPromptAgent

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure API key
# Create .env file with:
# GEMINI_API_KEY=your_api_key_here
# DEFAULT_LLM=gemini
```

### 🎯 First Run

```bash
# Start the server
python main.py

# You should see:
# "Uvicorn running on http://0.0.0.0:8000"

# Open in browser:
# http://127.0.0.1:8000
```

---

## 🎯 Examples & Usage

### 🌐 Web Interface Walkthrough

1. **Fill the Form**
   - Role: Enter the AI's role (e.g., "Marketing Copywriter")
   - Task: Describe what you want (e.g., "Write a product description")
   - Tone: Set the writing style (e.g., "Friendly, persuasive")
   - Output Format: Choose format (e.g., "Paragraph", "Bullet points")
   - Target Audience: Who is this for? (e.g., "Startup founders")
   - Context: Any additional requirements

2. **Preview in Real-Time**
   - See your prompt build instantly on the right panel
   - Character count updates automatically
   - Metadata cards show your selections

3. **Build Prompt**
   - Click "Build with Server"
   - Server processes and displays final prompt
   - Shows in "Server Build Result" box

4. **Enhance (Optional)**
   - Click "Enhance with AI"
   - Choose enhancement type (Balanced, Technical, Creative, Strategic, Educational)
   - LLM improves the prompt
   - Result appears below

5. **Save & Export**
   - Click "Save Template" to store for later
   - Click copy icon to copy to clipboard
   - Click download icon to save as .txt or .json

### 📊 Example Prompt Creation

| Input Field | Example Value |
|------------|--------------|
| **Role** | Marketing Strategist |
| **Task** | Write a launch announcement for a new AI product |
| **Tone** | Enthusiastic and professional |
| **Output Format** | LinkedIn post |
| **Target Audience** | Tech startup founders |
| **Context** | Emphasize real-time collaboration features |

**Generated Prompt:**
```
"You are a marketing strategist. Your task is to write a launch announcement 
for a new AI product. Use a enthusiastic and professional tone. Target your 
response to tech startup founders. Format your response as linkedin post. 
Additional context: Emphasize real-time collaboration features."
```

### 🎨 Tips for Better Prompts

**✍️ Be Specific:**
- ❌ "Write content"
- ✅ "Write a compelling product launch email"

**🎯 Add Context:**
- ❌ "Developer role"
- ✅ "Senior Python developer with 10 years experience"

**📝 Define Constraints:**
- ❌ "Generate text"
- ✅ "Generate 150-word product description with 3 key benefits"

---

## 🏗️ Project Architecture

### 📁 File Structure

```
95_CustomPromptAgent/
├── 📄 main.py                   # Server entry point
├── ⚙️ config.py                 # Configuration & environment
├── 🤖 agent.py                  # Prompt builder logic
├── 🌐 web_app.py                # FastAPI endpoints
├── 📋 requirements.txt          # Python dependencies
├── 🎨 .gitignore                # Git exclusions
├── 📁 templates/
│   └── index.html              # Full-featured web UI
├── 🎨 static/
│   └── main.css                # Custom styling
├── 🔧 utils/
│   ├── __init__.py
│   └── llm_service.py          # LLM wrapper (Gemini/OpenAI)
├── 📖 prompts/                  # Prompt templates (reserved)
└── 💾 storage/
    └── templates/              # User-saved templates
```

### 🔧 Technical Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | Python 3.9+ | Core application |
| **Web Framework** | FastAPI | REST API & web server |
| **Frontend** | Vanilla JavaScript + TailwindCSS | Interactive UI |
| **LLM Integration** | Gemini 2.0-flash / GPT-4.1 | AI enhancement |
| **Template Engine** | Jinja2 | HTML rendering |
| **Data Storage** | JSON + File System | Template persistence |
| **Server** | Uvicorn | ASGI web server |

### 🎯 Key Components

#### 🤖 CustomPromptAgent (`agent.py`)
- **Prompt Building**: Assembles prompts from input components
- **Template Management**: Save, load, delete operations
- **Prompt Enhancement**: LLM-powered prompt improvement
- **Error Handling**: Graceful fallbacks and validation

#### 🌐 Web Application (`web_app.py`)
- **REST API**: 7 endpoints for all operations
- **HTML Rendering**: Jinja2-based template responses
- **JSON API**: For JavaScript frontend communication
- **Error Handling**: User-friendly error responses

#### 🎨 Frontend (`templates/index.html` + `static/main.css`)
- **Interactive Form**: 6 input fields with real-time validation
- **Live Preview**: Updates as you type
- **Template Management UI**: Save, load, delete interface
- **Voice Input**: Web Speech API integration
- **Keyboard Shortcuts**: Power user features

#### 🔌 LLM Service (`utils/llm_service.py`)
- **Multi-Provider Support**: Gemini and OpenAI
- **Response Parsing**: Handles various response formats
- **Error Handling**: Fallback mechanisms
- **Configuration Management**: API key setup

---

## ⚙️ Configuration & Setup

### 🔑 API Key Configuration

**Option 1: .env File (Recommended)**
```env
# Get FREE key from: https://aistudio.google.com/app/apikey
GEMINI_API_KEY=your_gemini_key_here
DEFAULT_LLM=gemini

# OR get PAID key from: https://platform.openai.com/account/api-keys
OPENAI_API_KEY=your_openai_key_here
DEFAULT_LLM=openai
```

**Option 2: Environment Variables**
```bash
# Windows
set GEMINI_API_KEY=your_key_here

# Linux/macOS
export GEMINI_API_KEY=your_key_here
```

### 🎛️ Advanced Configuration

Edit `config.py` to customize:

```python
# Default LLM
DEFAULT_LLM = "gemini"  # or "openai"

# Model versions
GEMINI_MODEL = "gemini-2.0-flash"
OPENAI_MODEL = "gpt-4.1"

# Storage
TEMPLATES_DIR = "./storage/templates"
UPLOAD_DIR = "./uploads"
```

---

## 🔌 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/` | Main web interface |
| `POST` | `/build` | Build prompt from form |
| `POST` | `/api/build_prompt` | Build prompt (JSON) |
| `POST` | `/save_template` | Save template |
| `POST` | `/load_template` | Load template |
| `POST` | `/delete_template` | Delete template |
| `GET` | `/api/templates` | List all templates |
| `POST` | `/enhance` | Enhance prompt with LLM |

---

## 🧪 Testing & Verification

### ✅ Quick Test

```bash
# Start server
python main.py

# Open browser
http://127.0.0.1:8000

# Test form:
1. Fill: Role = "Teacher", Task = "Explain AI"
2. Click "Build with Server"
3. ✅ Result shows in "Server Build Result"
```

### 🔍 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| **Blank page** | Check F12 console for errors, refresh cache |
| **Enhance not working** | Verify .env has API key, restart server |
| **Templates not saving** | Check `storage/templates/` folder exists |
| **Port 8000 in use** | Change port in `main.py` or kill process |

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| `SETUP.md` | Step-by-step setup guide |
| `TROUBLESHOOTING.md` | Common issues & fixes |
| `FINAL_FIXES.md` | Technical implementation details |
| `TEST_CHECKLIST.md` | Comprehensive testing guide |
| `QUICK_TEST.md` | Quick 5-10 minute tests |

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork the project**
2. **Create feature branch**: `git checkout -b feature/your-feature`
3. **Make changes** and test thoroughly
4. **Submit pull request**

### Areas for Contribution
- New enhancement types
- UI/UX improvements
- Additional LLM providers
- Performance optimization
- Documentation improvements
- Bug fixes

---

## 📞 Support & Community

### 🆘 Getting Help

1. **Check Documentation**: README, SETUP.md, TROUBLESHOOTING.md
2. **Run Tests**: Follow TEST_CHECKLIST.md
3. **Check Logs**: Browser console (F12) and server output
4. **Review Issues**: Look for similar problems

### 🐛 Reporting Issues

Include:
- OS and Python version
- Steps to reproduce
- Error messages (full console output)
- Expected vs actual behavior

---

## 📄 License & Credits

### 📜 License

This project is part of **#100DaysOfAI-Agents** challenge.

**MIT License** - Feel free to use, modify, and distribute!

### 🙏 Acknowledgments

- **Google** for Gemini 2.0-flash API
- **OpenAI** for GPT-4.1 API
- **FastAPI** team for the excellent framework
- **TailwindCSS** for beautiful UI framework
- **Python community** for amazing libraries

---

<div align="center">

## 🎉 Ready to Build Better Prompts?

**Start crafting high-quality AI prompts with dynamic templates and real-time enhancement!**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎯 Examples](#-examples)

---

**Made with ❤️ by the #100DaysOfAI-Agents community**

*Day 95 of 100 - Building the future of AI agents, one day at a time!*

</div>
