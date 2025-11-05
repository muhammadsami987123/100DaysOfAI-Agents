# 🚀 AIProjectStarter - Day 94 of #100DaysOfAI-Agents

<div align="center">

![AIProjectStarter Banner](https://img.shields.io/badge/AIProjectStarter-Day%2094-blue?style=for-the-badge&logo=rocket&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20Framework-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-API-blue?style=for-the-badge&logo=google&logoColor=white)
![OpenAI GPT-4](https://img.shields.io/badge/OpenAI_GPT--4.1-API-orange?style=for-the-badge&logo=openai&logoColor=white)

**Your intelligent agent for quickly scaffolding new GPT-based projects with ready-to-use folder structure, boilerplate code, and configuration templates!**

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [🎭 Examples](#-examples) • [🏗️ Project Architecture](#-project-architecture) • [⚙️ Configuration](#-configuration--setup) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is AIProjectStarter?

AIProjectStarter is an intelligent agent that helps developers quickly scaffold new GPT-based projects. It automatically generates a complete project structure with boilerplate code, configuration files, and templates following the same modular style and structure as previous agents in the #100DaysOfAI-Agents series.

### 🌟 Key Highlights

- **📁 Automated Project Scaffolding**: Generates complete folder structures with all necessary files
- **💻 Boilerplate Code Generation**: Creates ready-to-use Python code for FastAPI, CLI, or API agents
- **🔧 LLM Integration**: Built-in support for Gemini 2.0-flash (default) and OpenAI GPT-4.1
- **📝 Smart Templates**: Generates README, .env, .gitignore, and requirements.txt automatically
- **🎨 Modern Web UI**: Beautiful, responsive interface with Tailwind CSS and dark/light mode
- **⚙️ Flexible Configuration**: Supports multiple project types and optional features

## 🎯 Features

### 🚀 Core Functionality
- ✅ **Project Type Support**: Web App (FastAPI), API Agent, Chatbot, CLI Agent, or Custom
- ✅ **LLM Integration**: Automatic setup for Gemini 2.0-flash or OpenAI GPT-4.1
- ✅ **Feature Flags**: Optional features like logging, file storage, JSON storage, file upload, frontend
- ✅ **Smart Folder Structure**: Generates appropriate directories based on project type
- ✅ **Boilerplate Code**: Creates agent.py, config.py, main.py, web_app.py, and utils/llm_service.py
- ✅ **Template Generation**: Auto-generates README, .env, .gitignore, and requirements.txt

### 🎨 User Experience
- ✅ **Modern Dashboard UI**: Intuitive web interface for project creation
- ✅ **Dark/Light Mode**: Comfortable viewing in any lighting condition
- ✅ **Preview Mode**: Preview project structure before creating files
- ✅ **Error Handling**: Clear error messages and success notifications
- ✅ **Responsive Design**: Works on desktop, tablet, and mobile devices

### 📊 Project Structure
- ✅ **Modular Design**: Follows the same structure as Days 84-86
- ✅ **Standard Layout**: utils/, templates/, static/, prompts/ directories
- ✅ **Configuration Management**: Centralized config.py with .env support
- ✅ **LLM Service**: Reusable LLMService class for Gemini and OpenAI

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.8+** installed on your system
- **Google Gemini API Key** (get one from [Google AI Studio](https://aistudio.google.com/app/apikey))
- **OpenAI API Key** (optional, get one from [OpenAI](https://platform.openai.com/account/api-keys))
- **Internet connection** for AI-powered scaffolding

### 🔧 Installation

```bash
# 1. Navigate to the agent's directory
cd 94_AIProjectStarter

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment (Windows)
venv\Scripts\activate
# On Linux/Mac, use: source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up environment variables
# Create a .env file in the 94_AIProjectStarter directory:
echo GEMINI_API_KEY=your_gemini_api_key_here > .env
echo OPENAI_API_KEY=your_openai_api_key_here >> .env
echo DEFAULT_LLM=gemini >> .env
# Replace 'your_gemini_api_key_here' and 'your_openai_api_key_here' with your actual API keys.
```

### 🎯 First Run (Web UI - Recommended)

```bash
# 1. Navigate to the agent's directory (if not already there)
cd 94_AIProjectStarter

# 2. Run the application
python main.py

# 3. Open your web browser and navigate to:
# http://127.0.0.1:8000
```

## 🎭 Examples & Usage

### 🌐 Web Interface

1. **Open the web interface** at `http://127.0.0.1:8000`
2. **Fill in the project details**:
   - Project Name: `DailyMotivationAgent`
   - Project Type: `CLI chatbot`
   - Preferred LLM: `Gemini 2.0-flash`
   - Features: `logging, json_storage`
   - Output Directory: (leave empty for Downloads folder)
3. **Click "Scaffold Project"** to generate the project
4. **Navigate to the generated project** and follow the README instructions

### 📝 Example: Creating a DailyMotivationAgent

**Input:**
- Project Name: `DailyMotivationAgent`
- Project Type: `cli`
- LLM: `gemini`
- Features: `logging, json_storage`

**Generated Output:**
```
daily_motivation_agent/
├── main.py
├── config.py
├── agent.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── cli/
├── utils/
│   ├── __init__.py
│   └── llm_service.py
├── prompts/
│   └── main_prompt.txt
├── logs/          (if logging feature enabled)
└── storage/        (if json_storage feature enabled)
```

### 💻 Programmatic Usage

You can also use the agent programmatically:

```python
from agent import AIProjectStarterAgent
from utils.llm_service import LLMService

# Initialize the agent
agent = AIProjectStarterAgent(llm_service=LLMService())

# Generate project structure
result = agent.scaffold_project(
    project_name="DailyMotivationAgent",
    project_type="cli",
    llm_preference="gemini",
    features=["logging", "json_storage"],
    output_dir=None  # Uses Downloads folder by default
)

if result["success"]:
    print(f"Project created at: {result['project_path']}")
else:
    print(f"Error: {result['error']}")
```

## 🏗️ Project Architecture

```
94_AIProjectStarter/
├── agent.py              # Main agent logic for project scaffolding
├── web_app.py            # FastAPI web application
├── main.py               # Entry point
├── config.py             # Configuration management
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
├── .gitignore            # Git ignore rules
├── utils/
│   ├── __init__.py
│   └── llm_service.py    # LLM service abstraction
├── templates/
│   └── index.html        # Web UI template
├── static/
│   └── main.css          # Custom styles
├── prompts/
│   └── scaffold_prompt.txt  # Prompt template
└── uploads/              # Upload directory (if needed)
```

## ⚙️ Configuration & Setup

### Environment Variables

Create a `.env` file in the project root:

```env
# LLM API Keys
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# LLM Configuration
DEFAULT_LLM=gemini
GEMINI_MODEL=gemini-2.0-flash
OPENAI_MODEL=gpt-4.1

# Other Settings
UPLOAD_DIR=./uploads
```

### Project Types

- **web_app**: FastAPI web application with templates and static files
- **api**: API agent with FastAPI endpoints
- **chatbot**: Chatbot with web interface
- **cli**: Command-line interface agent
- **other**: Generic project structure

### Optional Features

- **logging**: Adds `logs/` directory
- **file_storage**: Adds `storage/` directory
- **json_storage**: Adds `storage/` directory for JSON files
- **file_upload**: Adds `uploads/` directory and file upload support
- **frontend**: Adds templates and static directories

## 🔧 Advanced Usage

### Custom Project Templates

You can extend the agent to support custom project templates by modifying the `agent.py` file:

```python
# In agent.py, extend _generate_boilerplate_code method
def _generate_custom_template(self, project_name: str) -> str:
    # Your custom template logic here
    pass
```

### Batch Project Generation

Create multiple projects programmatically:

```python
projects = [
    {"name": "Agent1", "type": "web_app", "llm": "gemini"},
    {"name": "Agent2", "type": "cli", "llm": "openai"},
]

for project in projects:
    agent.scaffold_project(
        project_name=project["name"],
        project_type=project["type"],
        llm_preference=project["llm"]
    )
```

## 🧪 Testing & Quality Assurance

### Manual Testing

1. **Test project creation**:
   ```bash
   python main.py
   # Open http://127.0.0.1:8000
   # Create a test project
   # Verify all files are generated correctly
   ```

2. **Test generated project**:
   ```bash
   cd generated_test_project
   pip install -r requirements.txt
   python main.py
   ```

### Checklist

- ✅ Project folder structure is created correctly
- ✅ All boilerplate files are generated
- ✅ README.md contains setup instructions
- ✅ .env.example is created
- ✅ .gitignore is created
- ✅ requirements.txt includes all dependencies
- ✅ Generated project can be run successfully

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📝 License

This project is part of the #100DaysOfAI-Agents series and is open source.

## 🙏 Acknowledgments

- Built following the structure and patterns from Days 84-86 of #100DaysOfAI-Agents
- Uses Google Gemini 2.0-flash and OpenAI GPT-4.1 for LLM capabilities
- FastAPI for the web framework
- Tailwind CSS for styling

---

## 💭 A Personal Note

<div align="center">

**This was my dream project that I wanted to build, and this is currently my biggest project. This project represents numbers 94, 96 , 97, and 100 - milestones in my journey. While my full dream project in 2028 wasn't completed as planned, Alhamdulillah (الحمد لله) - by the grace of Allah, this project has come to fruition. This is a testament to perseverance, faith, and the belief that Allah's plans are always perfect. Thank you for being part of this journey! 🙏**

</div>

---

<div align="center">

**Made with ❤️ as part of #100DaysOfAI-Agents**

[⬆ Back to Top](#-aiprojectstarter---day-94-of-100daysofa-agents)

</div>

