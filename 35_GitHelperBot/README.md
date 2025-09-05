# 🤖 GitHelperBot - Day 35 of #100DaysOfAI-Agents

<div align="center">

![GitHelperBot](https://img.shields.io/badge/GitHelperBot-AI%20Powered-blue?style=for-the-badge&logo=git)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT%20API-purple?style=for-the-badge&logo=openai)
![Rich](https://img.shields.io/badge/Rich-Terminal%20UI-orange?style=for-the-badge&logo=terminal)

**Intelligent Terminal-Based Git Assistant with AI-Powered Suggestions**

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

GitHelperBot is an intelligent, AI-powered terminal assistant that revolutionizes how developers interact with Git. Whether you're a beginner learning Git or an experienced developer looking to streamline your workflow, GitHelperBot provides intelligent assistance, typo correction, and comprehensive explanations for all your Git needs.

### Key Benefits

- **⚡ Speed**: Instant typo correction and command suggestions
- **🧠 Intelligence**: AI-powered explanations and natural language processing
- **🛡️ Safety**: Comprehensive safety checks and dangerous command blocking
- **📊 Analytics**: Command history, favorites, and usage statistics
- **🎨 Beautiful UI**: Rich terminal interface with tables, panels, and colors
- **🔄 Multiple Interfaces**: Main menu, quick actions, and direct command processing

---

## ✨ Features

### 🤖 AI-Powered Intelligence
- **OpenAI GPT Integration**: Uses GPT-3.5-turbo for detailed command explanations
- **Smart Typo Correction**: Automatically detect and fix common Git command typos
- **Natural Language Processing**: Ask questions in plain English and get Git solutions
- **Context-Aware Responses**: AI understands Git workflows and provides relevant advice

### 🎯 Core Capabilities
- **Command Correction**: Fix typos like `git cmomit` → `git commit`
- **Safe Execution**: Execute commands with comprehensive safety checks and confirmation
- **File Generation**: Create `.gitignore` and `README.md` files for any project type
- **Usage Examples**: Provide common usage patterns for Git commands
- **Help System**: Comprehensive help and documentation

### 🎨 Enhanced User Experience
- **Beautiful Terminal UI**: Rich, colorful interface with tables, panels, and progress indicators
- **Interactive Menus**: Numbered suggestion lists and easy navigation
- **Command History**: Track all executed commands with success/failure status
- **Favorites System**: Mark frequently used commands for quick access
- **Usage Statistics**: Monitor your Git command patterns and success rates
- **Quick Actions**: One-key shortcuts for common Git workflows

### 🛡️ Safety-First Design
- **Dangerous Command Blocking**: Automatically block potentially harmful commands
- **Confirmation System**: All commands require explicit user confirmation
- **Timeout Protection**: Commands are limited to 30 seconds to prevent hanging
- **Error Handling**: Comprehensive error handling and user-friendly messages

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (3.9+ recommended)
- **Git** installed on your system
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys)) - Optional for AI features

### Installation

1. **Navigate to the project directory:**
   ```bash
   cd 35_GitHelperBot
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

4. **Set up OpenAI API key (optional):**
   
   **Option A: Environment Variable (Recommended)**
   ```bash
   # Windows (Command Prompt)
   set OPENAI_API_KEY=your_api_key_here
   
   # Windows (PowerShell)
   $env:OPENAI_API_KEY="your_api_key_here"
   
   # Linux/Mac
   export OPENAI_API_KEY=your_api_key_here
   ```
   
   **Option B: .env file**
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

### First Run

#### Main Menu (Recommended)
```bash
python agent.py --menu
```

#### Quick Actions
```bash
python agent.py --interactive
```

#### Single Command
```bash
python agent.py "git cmomit -m 'message'"
```

#### Generate Files
```bash
python agent.py --generate gitignore
python agent.py --generate readme
```

---

## 🎯 Usage

### Main Menu System

The main menu provides easy access to all GitHelperBot features:

```
📋 Main Menu
╭─────┬──────────────────────┬──────────────────────────────────────────╮
│ Key │ Option               │ Description                              │
├─────┼──────────────────────┼──────────────────────────────────────────┤
│ 1   │ Git Commands         │ Execute Git commands with assistance     │
│ 2   │ Natural Language     │ Ask questions about Git                  │
│ 3   │ Generate Files       │ Create .gitignore or README files        │
│ 4   │ Quick Actions        │ Common Git workflows                     │
│ 5   │ Help                 │ Show help information                    │
│ 0   │ Exit                 │ Leave the application                    │
╰─────┴──────────────────────┴──────────────────────────────────────────╯
```

### Quick Actions Menu

Access common Git workflows with single-key shortcuts:

```
⚡ Quick Actions
╭─────┬──────────────────────────────────────────┬────────────────────────────────╮
│ Key │ Command                                  │ Description                    │
├─────┼──────────────────────────────────────────┼────────────────────────────────┤
│ 1   │ git status                               │ Check repository status        │
│ 2   │ git add .                                │ Stage all changes              │
│ 3   │ git commit -m "message"                  │ Commit changes                 │
│ 4   │ git push origin main                     │ Push to remote                 │
│ 5   │ git pull origin main                     │ Pull from remote               │
│ 6   │ git branch                               │ List branches                  │
│ 7   │ git log --oneline -5                     │ Show recent commits            │
│ 8   │ generate gitignore                       │ Create .gitignore file         │
│ 9   │ generate readme                          │ Create README.md file          │
│ h   │ history                                  │ Show command history           │
│ f   │ favorites                                │ Show favorite commands         │
│ 0   │ help                                     │ Show help information          │
╰─────┴──────────────────────────────────────────┴────────────────────────────────╯
```

### Typo Correction Examples

GitHelperBot excels at detecting and correcting common Git command typos:

#### Basic Typo Detection
```bash
Input:  git cmomit -m "Initial commit"
Output: Did you mean: git commit -m "Initial commit"?
```

#### Multiple Suggestions
```bash
Input:  git chekout main
Suggestions:
  1. git checkout main
  2. git checkout -b main
  3. git checkout --help
```

#### Complex Command Correction
```bash
Input:  git pus --force origin main
Output: Did you mean: git push --force origin main?
```

### Natural Language Processing

Ask questions in plain English and get detailed Git solutions:

#### Example Queries
```bash
Query: "how to squash last 3 commits?"
Response: 
### Squashing Commits
To squash your last 3 commits:

```bash
git rebase -i HEAD~3
```

Then mark commits as **squash** in the editor.
```

#### Workflow Questions
```bash
Query: "how to create a new branch and switch to it?"
Response:
### Creating and Switching Branches

```bash
git checkout -b new-branch-name
# or
git switch -c new-branch-name
```

**Explanation:** Creates a new branch and immediately switches to it.
```

### File Generation

Generate project files with templates for different technologies:

#### Supported .gitignore Templates
- **Python**: Comprehensive Python project ignores
- **Node.js**: JavaScript/TypeScript project ignores
- **Java**: Java project ignores
- **General**: Universal project ignores

#### Example Usage
```bash
# Generate Python .gitignore
python agent.py --generate gitignore

# Generate README.md
python agent.py --generate readme
```

### Command History & Favorites

#### View Command History
```bash
Command: history
Output:
📜 Command History (Last 10 commands)
╭─────┬──────────────────────────────────────────┬────────┬─────────────╮
│ #   │ Command                                  │ Status │ Time        │
├─────┼──────────────────────────────────────────┼────────┼─────────────┤
│ 1   │ git status                               │ ✅     │ 14:30:25    │
│ 2   │ git add .                                │ ✅     │ 14:30:28    │
│ 3   │ git commit -m "Update README"            │ ✅     │ 14:30:35    │
│ 4   │ git push origin main                     │ ✅     │ 14:30:42    │
│ 5   │ git branch                               │ ✅     │ 14:31:15    │
╰─────┴──────────────────────────────────────────┴────────┴─────────────╯
```

#### Command Statistics
```bash
Command: stats
Output:
📊 Command Statistics
╭─────────────────────┬─────────╮
│ Metric              │ Value   │
├─────────────────────┼─────────┤
│ Total Commands      │ 25      │
│ Success Rate        │ 96.0%   │
╰─────────────────────┴─────────╯

Most Used Commands:
  git: 25 times
  git status: 8 times
  git add: 6 times
  git commit: 5 times
```

---

## 🛠️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | None | Optional |
| `OPENAI_MODEL` | OpenAI model to use | gpt-3.5-turbo | Optional |

### Command Line Options

```bash
python agent.py [OPTIONS] [COMMAND]

Options:
  --menu, -m              Show main menu (default)
  --interactive, -i       Run in interactive mode
  --generate {gitignore,readme}  Generate project files
  --help                  Show help message

Arguments:
  COMMAND                 Git command or natural language query
```

### Customization

#### Custom .gitignore Templates
Add custom templates by modifying `utils/file_generator.py`:

```python
def _load_gitignore_templates(self) -> Dict[str, str]:
    return {
        'python': "...",
        'nodejs': "...",
        'java': "...",
        'general': "...",
        'your_custom': "your custom template here"
    }
```

#### Extending Command Corrections
Add new typo patterns in `core/command_corrector.py`:

```python
def _load_common_typos(self) -> Dict[str, str]:
    return {
        'cmomit': 'commit',
        'chekout': 'checkout',
        'your_typo': 'correct_command'
    }
```

---

## 🔧 API Reference

### Command Line Interface

| Command | Description | Example |
|---------|-------------|---------|
| `python agent.py` | Start main menu | Default startup |
| `python agent.py --menu` | Show main menu | Interactive mode |
| `python agent.py --interactive` | Quick actions | Fast workflow |
| `python agent.py "command"` | Single command | Direct processing |
| `python agent.py --generate gitignore` | Generate .gitignore | File creation |
| `python agent.py --generate readme` | Generate README.md | Documentation |

### Internal API

#### CommandCorrector
```python
corrector = CommandCorrector()
correction = corrector.correct_command("git cmomit")
suggestions = corrector.get_suggestions("git chekout", max_suggestions=3)
examples = corrector.get_usage_examples("git clone")
```

#### CommandExecutor
```python
executor = CommandExecutor()
result = executor.execute_command("git status")
validation = executor.validate_command("git reset --hard")
```

#### CommandHistory
```python
history = CommandHistory()
history.add_command("git status", success=True, execution_time=0.5)
recent = history.get_recent_commands(limit=10)
favorites = history.get_favorite_commands()
stats = history.get_command_stats()
```

---

## 📁 Project Structure

```
35_GitHelperBot/
├── 📄 agent.py                   # Main CLI entry point
├── ⚙️ config/
│   └── 📄 openai_config.py       # OpenAI API configuration
├── 🧠 core/
│   ├── 📄 command_corrector.py   # Typo detection and correction
│   ├── 📄 command_explainer.py   # GPT-based explanations
│   └── 📄 command_executor.py    # Safe command execution
├── 🛠️ utils/
│   ├── 📄 cli_interface.py       # Rich terminal interface
│   ├── 📄 file_generator.py      # File generation utilities
│   └── 📄 command_history.py     # Command history and favorites
├── 🧪 tests/
│   └── 📄 test_commands.py       # Test suite
├── 🎬 demo.py                    # Basic feature demonstration
├── 🎬 demo_enhanced.py           # Enhanced UI demonstration
├── 📋 requirements.txt           # Python dependencies
├── 🔧 env.example               # Environment variables template
├── 🚀 install.bat               # Windows installation script
├── ▶️ start.bat                 # Windows startup script
└── 📖 README.md                 # This documentation
```

### Key Files

- **`agent.py`**: Main entry point with CLI argument parsing and menu system
- **`core/command_corrector.py`**: Typo detection, correction, and usage examples
- **`core/command_explainer.py`**: OpenAI GPT integration for explanations
- **`core/command_executor.py`**: Safe command execution with validation
- **`utils/cli_interface.py`**: Rich terminal UI with tables and panels
- **`utils/file_generator.py`**: .gitignore and README generation
- **`utils/command_history.py`**: Command tracking, favorites, and statistics

---

## 🎨 UI Features

### Visual Design
- **Rich Terminal Output**: Beautiful tables, panels, and colored text
- **Interactive Menus**: Numbered lists with easy selection
- **Progress Indicators**: Loading states and status updates
- **Error Handling**: Clear, user-friendly error messages
- **Success Feedback**: Confirmation messages and completion indicators

### Interactive Elements
- **Suggestion Menus**: Choose from multiple command suggestions
- **Confirmation Dialogs**: Safe execution with user confirmation
- **History Navigation**: Browse and select from command history
- **Favorites Management**: Mark and access favorite commands
- **Statistics Display**: Visual command usage analytics

### Responsive Design
- **Terminal Compatibility**: Works with all modern terminal emulators
- **Screen Size Adaptation**: Adjusts to different terminal sizes
- **Color Support**: Full color support with fallbacks for basic terminals
- **Unicode Support**: Emoji and special characters throughout

---

## 🔒 Safety Features

### Dangerous Command Detection
GitHelperBot automatically blocks potentially dangerous commands:

```bash
Blocked Commands:
- git reset --hard HEAD
- git push --force origin main
- git clean -fd
- git branch -D feature-branch
- git filter-branch --force
```

### Confirmation System
All commands require explicit user confirmation:

```bash
⚠️  DANGEROUS COMMAND DETECTED ⚠️

Command: git reset --hard HEAD

This command can cause data loss or irreversible changes.
Please make sure you understand what this command does before proceeding.

Are you absolutely sure you want to execute this? [y/N]
```

### Safety Measures
- **Timeout Protection**: Commands are limited to 30 seconds
- **Validation Checks**: All commands are validated before execution
- **Error Recovery**: Graceful handling of command failures
- **User Control**: Full control over command execution

---

## 🐛 Troubleshooting

### Common Issues

#### 1. "OpenAI API key not found"
**Solution:**
```bash
# Check if API key is set
echo $OPENAI_API_KEY

# Set API key (Linux/Mac)
export OPENAI_API_KEY=your_api_key_here

# Set API key (Windows)
set OPENAI_API_KEY=your_api_key_here
```

#### 2. "Git not found"
**Solution:**
```bash
# Install Git
# Windows: Download from https://git-scm.com/
# macOS: brew install git
# Linux: sudo apt-get install git

# Verify installation
git --version
```

#### 3. "Command failed: Permission denied"
**Solution:**
```bash
# Check file permissions
ls -la

# Fix permissions if needed
chmod +x your_file

# Check Git repository access
git status
```

#### 4. "Module not found errors"
**Solution:**
```bash
# Install dependencies
pip install -r requirements.txt

# Or install individually
pip install openai rich python-dotenv
```

#### 5. "Rich library display issues"
**Solution:**
```bash
# Update Rich library
pip install --upgrade rich

# Check terminal compatibility
python -c "from rich.console import Console; Console().print('Test')"
```

### Debug Mode

Enable debug logging by setting environment variable:
```bash
export DEBUG=1
python agent.py --menu
```

### Installation Verification

Run the test script to verify your installation:
```bash
python demo.py
python demo_enhanced.py
```

### Getting Help

1. **Check the terminal output** for detailed error messages
2. **Verify your OpenAI API key** is working with a simple test
3. **Try the terminal interface** for debugging
4. **Review the logs** for specific error details
5. **Check Git installation** and repository access

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

- **🐛 Bug Fixes**: Report and fix bugs
- **✨ New Features**: Add new Git command support or features
- **📚 Documentation**: Improve README, add examples
- **🎨 UI/UX**: Enhance the terminal interface
- **🧪 Testing**: Add more test coverage
- **🔧 Configuration**: Improve configuration options

### Development Setup

```bash
# Clone the repository
git clone <repository-url>
cd 35_GitHelperBot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
python tests/test_commands.py
python demo.py
python demo_enhanced.py
```

### Code Style

- Follow **PEP 8** Python style guidelines
- Use **type hints** for function parameters
- Add **docstrings** for all functions
- Write **comprehensive tests**
- Keep **commit messages** clear and descriptive

---

## 📄 License

This project is part of the **#100DaysOfAI-Agents** challenge by [Muhammad Sami Asghar Mughal](https://github.com/your-username).

### License Terms

- **Open Source**: This project is open source and available under the MIT License
- **Educational Use**: Free to use for educational and personal purposes
- **Commercial Use**: Contact the author for commercial licensing
- **Attribution**: Please credit the original author when using this code

---

## 🙏 Acknowledgments

### Open Source Libraries
- **[OpenAI](https://openai.com/)** - GPT API for intelligent explanations
- **[Rich](https://rich.readthedocs.io/)** - Beautiful terminal output and UI
- **[Python](https://python.org/)** - The programming language that makes it all possible
- **[Git](https://git-scm.com/)** - The version control system we're helping with

### Community
- **AI Community** - For inspiration and support
- **Open Source Contributors** - For the amazing tools that make this possible
- **Beta Testers** - For valuable feedback and bug reports

### Special Thanks
- **OpenAI Team** - For making powerful AI accessible
- **Rich Library Community** - For the excellent terminal UI framework
- **#100DaysOfAI-Agents** - For the motivation to build amazing AI tools

---

<div align="center">

**Happy Git-ing! 🚀**

[⬆️ Back to Top](#-githelperbot---day-35-of-100daysofai-agents)

*Transform your Git workflow with AI-powered intelligence and beautiful terminal interfaces!*

</div>