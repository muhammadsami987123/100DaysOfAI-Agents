# 💻 TerminalHelperAI - Day 76 of #100DaysOfAI-Agents

<div align="center">

![TerminalHelperAI Banner](https://img.shields.io/badge/TerminalHelperAI-AI%20Powered-blue?style=for-the-badge&logo=terminal&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-green?style=for-the-badge&logo=python&logoColor=white)
![OpenAI/Gemini](https://img.shields.io/badge/AI-OpenAI%2FGemini-purple?style=for-the-badge&logo=openai&logoColor=white)
![Rich](https://img.shields.io/badge/Rich-Terminal%20UI-orange?style=for-the-badge&logo=terminal&logoColor=white)

**Intelligent Command-Line Assistant to Learn, Explore, and Generate Terminal Commands Easily.**

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [💡 Usage](#-usage) • [🛠️ Configuration](#-configuration) • [🤝 Contributing](#-contributing)

</div>

---

## 🌟 Overview

TerminalHelperAI is an intelligent, AI-powered command-line assistant designed to make the terminal experience easy and beginner-friendly, while also powerful for advanced users. It converts natural language instructions into safe, executable terminal commands with explanations, safety warnings, and contextual understanding across different operating systems and shells.

### 🌟 Key Highlights

- **🧠 AI-Powered Explanations**: Uses OpenAI GPT-4o-mini or Gemini-1.5-Flash-latest for detailed command explanations.
- **💻 OS-Aware Command Generation**: Auto-detects your OS (Windows/macOS/Linux) and preferred shell (PowerShell/Bash/Zsh) and tailors commands accordingly.
- **🛡️ Safety-First Design**: Highlights risky operations with clear warnings and suggests safer alternatives.
- **📝 Structured Output**: Provides responses with labeled sections: Command, Explanation, Safety Warning, Notes.
- **🌍 Multilingual Support**: Understands and responds in English, Urdu, and Hindi.
- **🔄 Short-Term Session Memory**: Remembers recent commands for connected, consistent follow-up conversations.
- **⚡ Streaming Output**: Experience responses appearing progressively with a dynamic loader for a smooth CLI UX.
- **🎨 Rich CLI Interface**: Beautiful terminal UI with colors, spinners, panels, and markdown rendering.

---

## ✨ Features

### 🚀 Core Functionality

- ✅ **Natural Language to Command**: Convert plain English descriptions into executable terminal commands.
- ✅ **Command Explanation**: Get clear, educational explanations for what each command, flag, and option does.
- ✅ **Safety Warnings**: Automatic detection of potentially dangerous commands with explicit warnings and safer alternatives.
- ✅ **OS & Shell Adaptation**: Commands are tailored to Windows (PowerShell), macOS (Bash/Zsh), and Linux (Bash/Zsh).
- ✅ **Interactive Learning**: Designed to help users learn terminal commands step-by-step.

### 🎯 Advanced Capabilities

- ✅ **Dual AI Model Support**: Choose between OpenAI GPT-4o-mini and Gemini-1.5-Flash-latest via `LLM_MODEL` config.
- ✅ **Intelligent Fallback**: Automatically attempts the secondary AI model if the primary fails to generate a response.
- ✅ **Context-Aware Responses**: AI understands Git basics, file operations, networking, system monitoring, package managers, and more.
- ✅ **Error Message Explanation (Roadmap)**: Future capability to explain confusing error messages.
- ✅ **Shell Alias Suggestions (Roadmap)**: Future capability to suggest aliases for faster workflows.
- ✅ **Best Practice Recommendations (Roadmap)**: Future capability to recommend best practices (e.g., using `-i` with `rm`).

### 🎨 User Experience

- ✅ **Real-time Streaming**: Responses appear word-by-word with a dynamic loader.
- ✅ **Clean CLI UX**: Clear status cues — Listening, Processing, Formatting, Responding.
- ✅ **Multilingual Interaction**: Ask questions in English, Urdu, or Hindi.
- ✅ **Persistent Session Memory**: Follow-up questions maintain context from previous interactions.

---

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.9+** installed on your system
- **OpenAI API Key** or **Gemini API Key** (or both for fallback support)
- **Internet connection** for AI command generation

### ⚡ Installation

1.  **Navigate to the project directory:**
    ```bash
    cd 76_TerminalHelperAI
    ```

2.  **Create and configure `.env` file:**
    Copy `env.example` to `.env` and add your API key(s):
    ```env
    LLM_MODEL=gemini # or openai
    GEMINI_API_KEY=your_gemini_api_key_here
    OPENAI_API_KEY=your_openai_api_key_here
    
    # Optional settings
    OPENAI_MODEL=gpt-4o-mini
    GEMINI_MODEL=gemini-1.5-flash-latest
    TEMPERATURE=0.7
    MAX_TOKENS=1000
    DEFAULT_SHELL=bash
    SAFETY_MODE=true
    MAX_HISTORY_MESSAGES=10
    ```

3.  **Run the installation script:**
    ```bash
    # Windows
    install.bat

    # macOS/Linux (create a similar install.sh script if needed)
    # python -m venv venv
    # source venv/bin/activate
    # pip install -r requirements.txt
    ```
    The `install.bat` script (or equivalent for Linux/macOS) will:
    - ✅ Check Python installation
    - ✅ Create a virtual environment
    - ✅ Install all dependencies

### 🎯 First Run

```bash
# Start the TerminalHelperAI
python main.py
```

Type `exit` or `quit` to end the session.

---

## 💡 Usage

TerminalHelperAI is designed for interactive use via the command line. Just type your questions and follow the prompts.

- You'll see these statuses:
  - **Listening…** waiting for your input
  - **Processing…** contacting AI (animated loader)
  - **Formatting…** preparing Markdown output
  - **Command Ready…** final nicely formatted output in a panel

- **Ask in English, Urdu, or Hindi.** Examples:
  - "How do I list all files in a folder?"
  - "Give me a command to zip a folder on Linux."
  - "How do I install Node.js using terminal on macOS?"
  - "Difference between > and >>?"
  - "Show hidden files on Windows."
  - "Remove all .tmp files in current folder."

- **Follow-up questions** will consider your previous commands during this session.

---

## 🛠️ Configuration

Edit `config.py` and your `.env` file to customize the agent's behavior.

### Environment Variables (`.env`)

| Variable               | Default                       | Description                                                | Required |
|------------------------|-------------------------------|------------------------------------------------------------|----------|
| `LLM_MODEL`            | `gemini`                      | Preferred AI model: `openai` or `gemini`                   | ✅       |
| `OPENAI_API_KEY`       | —                             | Your OpenAI API key                                        | conditional ✅ |
| `OPENAI_MODEL`         | `gpt-4o-mini`                 | OpenAI chat model to use                                   | ❌       |
| `GEMINI_API_KEY`       | —                             | Your Google Gemini API key                                 | conditional ✅ |
| `GEMINI_MODEL`         | `gemini-1.5-flash-latest`     | Google Gemini chat model to use                            | ❌       |
| `TEMPERATURE`          | `0.7`                         | Creativity level (0.0–1.0)                                 | ❌       |
| `MAX_TOKENS`           | `1000`                        | Output token limit for AI responses                        | ❌       |
| `DEFAULT_SHELL`        | `bash`                        | Default shell for unknown OS, or if not detected           | ❌       |
| `SAFETY_MODE`          | `true`                        | Enable safety warnings and safer alternatives              | ❌       |
| `MAX_HISTORY_MESSAGES` | `10`                          | Number of recent messages to include in short-term memory  | ❌       |

---

## 📁 Project Structure

```
76_TerminalHelperAI/
├── agents/
│   └── terminal_helper_agent.py    # Core AI logic, API integration, streaming, history
├── utils/
├── config.py                       # Environment loading, API keys, model settings
├── main.py                         # CLI entry point, UI rendering, OS detection
├── requirements.txt                # Python dependencies (openai, rich, python-dotenv, google-generativeai)
├── install.bat                     # Windows installation script
├── start.bat                       # Windows startup script
├── env.example                     # Example environment variables file
└── README.md                       # This comprehensive documentation
```

### 🎯 Key Components

- **`main.py`**: Handles CLI user interface, OS detection, and orchestrates calls to the `TerminalHelperAgent`.
- **`agents/terminal_helper_agent.py`**: Contains the core AI logic, including `_build_system_prompt_content` for dynamic prompt generation, API client initialization (OpenAI/Gemini), and the `stream` method for generating and streaming responses.
- **`config.py`**: Manages environment variables, API keys, model settings, and general application configuration.
- **`requirements.txt`**: Lists all Python packages required for the project (`openai`, `rich`, `python-dotenv`, `google-generativeai`).

---

## 🛡️ Safety Notes

TerminalHelperAI prioritizes user safety:

- **Destructive Operations**: Commands that can cause data loss (e.g., `rm -rf /`, `format C:`) are clearly marked with safety warnings.
- **Safer Alternatives**: The agent will suggest safer flags (e.g., `-i` for `rm`, `--dry-run` for destructive operations) or alternative approaches.
- **Confirmation**: Always review the generated command carefully before executing it in your actual terminal, especially for destructive operations.

---

## 🗺️ Roadmap

### 🚀 Planned Features

| Feature                           | Status    | Description                                                 |
|-----------------------------------|-----------|-------------------------------------------------------------|
| Command Execution w/ Confirmation | 🔄 Planned | Allow direct execution of safe commands with user confirmation |
| Command History & Favorites       | 🔄 Planned | Track and favorite frequently used commands                 |
| Custom Command Templates          | 🔄 Planned | User-defined templates for common tasks                     |
| Explain Confusing Error Messages  | 🔄 Planned | AI-powered explanations for terminal error outputs           |
| Suggest Shell Aliases             | 🔄 Planned | Recommend aliases to optimize user workflows                |
| Recommend Best Practices          | 🔄 Planned | Provide tips for efficient and safe terminal usage          |
| Multi-Shell Output                | 🔄 Planned | Optionally show commands for different shells side-by-side |
| Batch Command Processing          | 🔄 Planned | Execute multiple commands in sequence                       |

---

## 📝 Version History

- **v1.1.0** — Dual AI Model Support (OpenAI & Gemini) with Fallback Mechanism, Improved System Prompt Handling
- **v1.0.0** — Initial release: OS detection, safety warnings, streaming output, multilingual support, rich CLI UI

---

## 🤝 Contributing

We welcome contributions to make TerminalHelperAI even more powerful and user-friendly! Please refer to the guidelines below.

### 🛠️ How to Contribute

1.  **Fork the repository**
2.  **Create a feature branch**: `git checkout -b feature/your-feature-name`
3.  **Make your changes** and test thoroughly
4.  **Commit your changes**: `git commit -m 'Add your amazing feature'`
5.  **Push to the branch**: `git push origin feature/your-feature-name`
6.  **Open a Pull Request**

### 🎯 Areas for Contribution

-   **New Features**: Implement roadmap items or new ideas.
-   **Command Mappings**: Improve AI's ability to generate specific commands.
-   **Safety Checks**: Enhance detection and suggestions for dangerous operations.
-   **CLI UX**: Improve the terminal interface and user experience.
-   **Documentation**: Refine this README, add examples, or create tutorials.
-   **Testing**: Expand the test suite for robustness.
-   **Bug Fixes**: Identify and resolve issues.

### 📋 Contribution Guidelines

-   Follow the existing code style (PEP 8).
-   Add type hints and docstrings for new functions/classes.
-   Ensure all tests pass before submitting a pull request.
-   Be respectful and constructive in all interactions.

---

## 📄 License & Credits

### 📜 License

This project is part of the **#100DaysOfAI-Agents** challenge by **Muhammad Sami Asghar Mughal**.

**MIT License** - Feel free to use, modify, and distribute!

### 🙏 Acknowledgments

-   **OpenAI** for providing powerful large language models.
-   **Google Gemini** for providing innovative generative AI models.
-   **Rich** library for creating beautiful terminal UIs.
-   **Python community** for the extensive ecosystem of libraries and tools.
-   **All contributors** who help improve this project.

---

<div align="center">

## 🎉 Ready to Master Your Terminal?

**Transform your command-line experience with AI-powered intelligence!**

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [💡 Usage](#-usage) • [🛠️ Configuration](#-configuration)

---

**Made with ❤️ by the #100DaysOfAI-Agents community**

*Day 76 of 100 - Building the future of AI agents, one day at a time!*

</div>
