# 📄 ResumeParserAgent — Day 59 of #100DaysOfAI-Agents

<div align="center">

![ResumeParserAgent](https://img.shields.io/badge/ResumeParserAgent-AI%20Powered-blue?style=for-the-badge&logo=openai)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-API-purple?style=for-the-badge&logo=google)
![Rich](https://img.shields.io/badge/Rich-Terminal%20UI-orange?style=for-the-badge&logo=terminal)

**Intelligent CLI-Based AI HR Assistant for Resume Parsing**

[Features](#-features) • [Quick Start](#-quick-start) • [Usage](#-usage) • [Configuration](#-configuration) • [API](#-api) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [🎯 Usage](#-usage)
- [🛠️ Configuration](#-configuration)
- [🔧 API Reference](#-api-reference)
- [📁 Project Structure](#-project-structure)
- [🎨 UI Features](#-ui-features)
- [🔒 Safety Features](#-safety-features)
- [🐛 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🌟 Overview

ResumeParserAgent is an intelligent, AI-powered CLI tool designed to streamline HR screening by automating resume parsing. It extracts, structures, and summarizes candidate information from various resume formats (PDF, DOCX, TXT), helping recruiters quickly identify relevant data and build comprehensive resume databases.

### Key Benefits

- **⚡ Speed**: Rapid parsing and extraction of key candidate information.
- **🧠 Intelligence**: AI-powered extraction of structured data, summaries, and skills.
- **🎨 Beautiful UI**: Rich terminal interface with clear, color-coded output.
- **🔄 Multi-format Support**: Handles `.pdf`, `.docx`, and `.txt` resume files.

---

## ✨ Features

### 🤖 AI-Powered Intelligence
- **Google Gemini Integration**: Utilizes Gemini API for intelligent content extraction and summarization.
- **Structured Data Extraction**: Accurately extracts Full Name, Email, Phone Number, LinkedIn/GitHub, Education, Work Experience, Skills, and Certifications/Projects.
- **Resume Summarization**: Generates concise 3-5 line summaries of resumes.
- **Skills-Only Extraction**: Isolates and lists technical and soft skills.

### 🎯 Core Capabilities
- **Multi-format Resume Parsing**: Robustly processes PDF, DOCX, and TXT files.
- **CLI Flags**: Supports `--summary`, `--skills-only`, `--json`, and `--validate` flags for tailored output.
- **JSON Output**: Provides parsed data in a clean, structured JSON format.
- **Field Validation**: Checks for the presence of key fields like Name, Email, and Phone Number.

### 🎨 Enhanced User Experience
- **Beautiful Terminal UI**: Rich, colorful interface with panels, tables, and progress indicators.
- **Interactive Prompts**: Guides users through input and action choices.
- **Syntax-Colored Output**: JSON output with syntax highlighting for readability.

### 🛡️ Safety-First Design
- **Error Handling**: Comprehensive error handling for file operations and API calls.
- **Confirmation System**: Saving files requires explicit user confirmation.
- **API Timeout Protection**: Prevents hanging on long API requests.

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (3.9+ recommended)
- **Google Gemini API Key** ([Get one here](https://aistudio.google.com/app/apikey)) - Required for AI features

### Installation

1. **Navigate to the project directory:**
   ```bash
   cd 59_ResumeParserAgent
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Google Gemini API key:**

   **Option A: Environment Variable (Recommended)**
   ```bash
   # Windows (Command Prompt)
   set GEMINI_API_KEY=your_gemini_api_key_here

   # Windows (PowerShell)
   $env:GEMINI_API_KEY="your_gemini_api_key_here"

   # Linux/Mac
   export GEMINI_API_KEY=your_gemini_api_key_here
   ```

   **Option B: .env file**
   Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

### First Run

Run the main script and follow the prompts:

```bash
python main.py
```

### Examples with Flags

- **Summarize a resume from a file:**
  ```bash
  python main.py --summary file my_resume.pdf
  ```
- **Extract only skills from pasted text:**
  ```bash
  python main.py --skills-only text "John Doe..."
  ```
- **Parse a DOCX and save output as JSON:**
  ```bash
  python main.py --json file my_resume.docx
  ```
- **Parse a TXT file and validate key fields:**
  ```bash
  python main.py --validate file my_resume.txt
  ```

---

## 🎯 Usage

The ResumeParserAgent is designed for interactive use with file paths or pasted text, augmented by CLI flags for specific operations.

### Basic Usage

Upon running `python main.py`, the agent will prompt you to either upload a file or paste resume text.

```
Hello! I am ResumeParserAgent, your AI HR assistant...
Please upload a resume file to begin parsing, or paste the resume text directly.
Enter 'file <path_to_file>' or 'text <your_resume_text>':
> file path/to/your/resume.pdf
```

### CLI Flags

| Flag              | Description                                        |
|-------------------|----------------------------------------------------|
| `--summary`       | Summarize the resume in 3-5 lines                  |
| `--skills-only`   | Extract only technical and soft skills             |
| `--json`          | Save parsed output as `resume_parsed.json`         |
| `--validate`      | Check if key fields (Name, Email, Phone) are missing |

---

## 🛠️ Configuration

### Environment Variables

| Variable         | Description                                        | Default       | Required |
|------------------|----------------------------------------------------|---------------|----------|
| `GEMINI_API_KEY` | Your Google Gemini API key                         | None          | Required |
| `GEMINI_MODEL`   | Gemini model to use                                | `gemini-pro`  | Optional |
| `TEMPERATURE`    | Creativity level for AI (0.0-1.0)                  | `0.7`         | Optional |
| `MAX_TOKENS`     | Maximum output tokens for AI response              | `1500`        | Optional |

---

## 🔧 API Reference

### Command Line Interface

| Command                                                    | Description                             | Example                                              |
|------------------------------------------------------------|-----------------------------------------|------------------------------------------------------|
| `python main.py`                                           | Start interactive mode                  | `python main.py`                                     |
| `python main.py file <path>`                               | Parse file                              | `python main.py file my_resume.pdf`                  |
| `python main.py text "<text>"`                             | Parse inline text                       | `python main.py text "John Doe..."`                  |
| `python main.py --summary [file/text]`                     | Summarize resume                        | `python main.py --summary file my_resume.docx`       |
| `python main.py --skills-only [file/text]`                 | Extract skills only                     | `python main.py --skills-only text "Python, Java..."`|
| `python main.py --json [file/text]`                        | Save parsed output as JSON              | `python main.py --json file my_resume.pdf`           |
| `python main.py --validate [file/text]`                    | Validate key fields                     | `python main.py --validate file my_resume.txt`       |
| `exit`, `quit`, `q`                                        | Exit the application                    | `quit`                                               |

---

## 📁 Project Structure

```
59_ResumeParserAgent/
├── 📄 main.py                   # Main CLI entry point
├── ⚙️ config/
│   └── 📄 gemini_config.py       # Google Gemini API configuration
├── 🧠 core/
│   ├── 📄 parser.py              # Resume file parsing (PDF, DOCX, TXT)
│   └── 📄 extractor.py           # AI-powered extraction, summarization, skills
├── 🛠️ utils/
│   └── 📄 cli_interface.py       # Rich terminal interface
├── 📋 requirements.txt           # Python dependencies
├── 🔧 env.example               # Environment variables template
├── 🚀 install.bat               # Windows installation script
├── ▶️ start.bat                 # Windows startup script
└── 📖 README.md                 # This documentation
```

### Key Files

- **`main.py`**: Main entry point with CLI argument parsing and orchestration.
- **`config/gemini_config.py`**: Google Gemini API integration and configuration.
- **`core/parser.py`**: Logic for reading and converting different resume file formats to text.
- **`core/extractor.py`**: AI-powered logic for detailed data extraction, summarization, and skill identification.
- **`utils/cli_interface.py`**: Rich terminal UI for interactive prompts and formatted output.

---

## 🎨 UI Features

### Visual Design
- **Rich Terminal Output**: Beautiful panels, tables, and colored text for improved readability.
- **Interactive Prompts**: User-friendly prompts for input and confirmations.
- **Progress Indicators**: Loading animations for API calls and processing tasks.
- **Error Handling**: Clear, color-coded error messages.
- **Success Feedback**: Visual confirmations for successful operations.

### Interactive Elements
- **Confirmation Dialogs**: For saving files.
- **Dynamic Prompts**: Context-aware prompts for user input.

### Responsive Design
- **Terminal Compatibility**: Designed to work across various modern terminal emulators.
- **Color Support**: Full color support with graceful degradation for basic terminals.

---

## 🔒 Safety Features

### Input Validation
- **File Existence Check**: Verifies if specified local files exist before processing.
- **Resume Content Check**: Ensures that resume text is not empty before parsing.

### Safety Measures
- **API Call Timeouts**: Prevents long-running or hanging API requests.
- **Graceful Error Handling**: Manages API failures and file I/O errors robustly.
- **User Control**: Explicit user confirmation required for file saving operations.

---

## 🐛 Troubleshooting

### Common Issues

#### 1. "Google Gemini API key not found"
**Solution:**
```bash
# Check if API key is set
echo $GEMINI_API_KEY

# Set API key (Linux/Mac)
export GEMINI_API_KEY=your_gemini_api_key_here

# Set API key (Windows)
set GEMINI_API_KEY=your_gemini_api_key_here
```
Alternatively, create a `.env` file in the project root with `GEMINI_API_KEY=your_gemini_api_key_here`.

#### 2. "Module not found errors"
**Solution:**
```bash
# Install dependencies
pip install -r requirements.txt

# Or install individually
pip install google-generativeai pypdf python-docx python-dotenv rich
```

#### 3. "Error reading PDF/DOCX"
**Solution:** Ensure the file is not corrupted and is accessible. Check the error message for specifics. Some complex PDF/DOCX formats might not be fully supported by the underlying libraries.

### Getting Help

1. **Check the terminal output** for detailed error messages.
2. **Verify your Google Gemini API key** is correctly configured.
3. **Review the project's `README.md`** for up-to-date information and examples.

---

## 🤝 Contributing

This project is part of the **#100DaysOfAI-Agents** challenge. We welcome contributions!

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Areas for Contribution

- **🐛 Bug Fixes**: Report and fix bugs.
- **✨ New Features**: Add support for more resume formats, advanced parsing, or AI features.
- **📚 Documentation**: Improve README, add examples, or create tutorials.
- **🎨 UI/UX**: Enhance the terminal interface or add more interactive elements.
- **🧪 Testing**: Add more unit and integration test coverage.

---

## 📄 License

This project is open-source and available under the MIT License.

### License Terms

- **Open Source**: This project is open source and available under the MIT License.
- **Educational Use**: Free to use for educational and personal purposes.
- **Commercial Use**: Contact the author for commercial licensing.
- **Attribution**: Please credit the original author when using this code.

---

## 🙏 Acknowledgments

### Open Source Libraries
- **[Google Gemini API](https://ai.google.dev/)** - For powerful AI capabilities.
- **[Rich](https://rich.readthedocs.io/)** - For beautiful terminal output and UI.
- **[Python](https://python.org/)** - The programming language that makes it all possible.
- **[PyPDF](https://pypdf.readthedocs.io/)** - For PDF file parsing.
- **[Python-Docx](https://python-docx.readthedocs.io/)** - For DOCX file parsing.
- **[Python-Dotenv](https://pypi.org/project/python-dotenv/)** - For environment variable management.

### Community
- **AI Community** - For inspiration and support.
- **Open Source Contributors** - For the amazing tools that make this possible.
- **Beta Testers** - For valuable feedback and bug reports.

### Special Thanks
- **Google AI Team** - For making powerful AI accessible.
- **Rich Library Community** - For the excellent terminal UI framework.
- **#100DaysOfAI-Agents** - For the motivation to build amazing AI tools.

---

<div align="center">

**Happy Parsing! 🚀**

[⬆️ Back to Top](#📄-resumeparseragent-—-day-59-of-#100daysofai-agents)

*Automate your HR screening with intelligent resume parsing and structured data extraction!*

</div>
