# 🔄 AutoUpdaterBot — Day 62 of #100DaysOfAI-Agents

<div align="center">

![AutoUpdaterBot](https://img.shields.io/badge/AutoUpdaterBot-AI%20Powered-blue?style=for-the-badge&logo=github)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![Git](https://img.shields.io/badge/Git-Automation-orange?style=for-the-badge&logo=git)

**Intelligent CLI-Based GitHub Repository Updater with Smart Feedback**

[Features](#-features) • [Quick Start](#-quick-start) • [Usage](#-usage) • [Configuration](#-configuration) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [🎯 Usage](#-usage)
- [🛠️ Configuration](#-configuration)
- [📁 Project Structure](#-project-structure)
- [🐛 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🌟 Overview

AutoUpdaterBot is a CLI-based intelligent automation agent designed to streamline the process of updating local GitHub repositories. It automates pulling the latest changes, provides intelligent feedback on updates, and supports optional post-update actions like rebuilding or running tests. This bot is perfect for developers and AI engineers who need to keep their local projects synchronized effortlessly, especially in offline or local-first development environments, and for integrating into larger AI agent chains.

### Key Benefits

- **⚡️ Time-Saving**: Automates routine Git pull operations.
- **🧠 Intelligent Feedback**: Provides clear summaries of changes and commit messages.
- **🔄 Seamless Integration**: Ideal for AI agent chains that require up-to-date tools.
- **🛡️ Safe Operations**: Includes robust error handling for common Git issues.

---

## ✨ Features

### 🤖 Core Automation
- **Automated Pulls**: Fetches and merges latest changes from specified GitHub repositories.
- **Branch Support**: Option to specify a branch name, defaults to `main`.
- **Intelligent Summaries**: Provides a clear overview of updated files and commit messages.

### 🎯 Optional Actions
- **Rebuild Option**: Execute a `--rebuild` command after a successful pull.
- **Test Runner**: Execute `--run-tests` to verify functionality post-update.
- **Summary-Only Mode**: `--summary-only` flag to just show changes without applying them.

### 🛡️ Safety & Reliability
- **Error Handling**: Graceful handling of authentication errors, merge conflicts, and invalid repositories.
- **Pre-Update Checks**: Ensures repository existence and proper configuration before attempting pulls.
- **User-Friendly Feedback**: Clear messages for success, warnings, and errors.

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (3.9+ recommended)
- **Git** installed and configured on your system.
- **GitHub Account** (for private repositories, authentication setup is required).

### Installation

1. **Navigate to the project directory:**
   ```bash
   cd 62_AutoUpdaterBot
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

4. **Set up GitHub Personal Access Token (for private repos/rate limiting):**

   **Option A: Environment Variable (Recommended)**
   ```bash
   # Windows (Command Prompt)
   set GITHUB_TOKEN=your_github_pat_here

   # Windows (PowerShell)
   $env:GITHUB_TOKEN="your_github_pat_here"

   # Linux/Mac
   export GITHUB_TOKEN=your_github_pat_here
   ```

   **Option B: .env file**
   Create a `.env` file in the project root:
   ```env
   GITHUB_TOKEN=your_github_pat_here
   ```
   (Note: For public repos, a token is often not required but recommended for higher API rate limits).

### First Run

```bash
python cli.py
```
The bot will then prompt you for the GitHub repository URL and the target local folder.

#### Examples:

- **Basic Update:**
  ```bash
  python cli.py --repo "https://github.com/user/repo" --local-path "path/to/local/repo"
  ```

- **Update a specific branch and rebuild:**
  ```bash
  python cli.py --repo "https://github.com/user/repo" --local-path "path/to/local/repo" --branch "dev" --rebuild
  ```

- **Get summary only, no actual pull:**
  ```bash
  python cli.py --repo "https://github.com/user/repo" --local-path "path/to/local/repo" --summary-only
  ```

- **Auto-commit local changes before pulling:**
  ```bash
  python cli.py --repo "https://github.com/user/repo" --local-path "path/to/local/repo" --auto-commit
  ```

---

## 🎯 Usage

### Command Line Interface

```bash
python cli.py [OPTIONS]
```

**Options:**

| Flag              | Description                                        | Example                                                        |
|-------------------|----------------------------------------------------|----------------------------------------------------------------|
| `--repo <url>`    | GitHub repository URL (e.g., `https://github.com/user/repo`) | `--repo "https://github.com/octocat/Spoon-Knife"`              |
| `--local-path <path>` | Local directory where the repo is or will be cloned | `--local-path "C:/Users/Dev/my_project"`                        |
| `--branch <name>` | Optional: Specify a branch to pull from (default: `main`) | `--branch "development"`                                       |
| `--rebuild`       | Optional: Execute a `rebuild.sh` (or `rebuild.bat` on Windows) script after update | `--rebuild`                                                    |
| `--run-tests`     | Optional: Execute a `run_tests.sh` (or `run_tests.bat` on Windows) script after update | `--run-tests`                                                  |
| `--summary-only`  | Optional: Show changes summary without performing actual pull/update | `--summary-only`                                               |
| `--auto-commit`   | Optional: Automatically commit local changes before pulling | `--auto-commit`                                                |
| `--help`          | Show help message                                  | `--help`                                                       |

### Interactive Mode (Default if no arguments provided)

If you run `python cli.py` without any arguments, the bot will enter an interactive mode, prompting you for each required piece of information and confirming optional actions.

---

## 🛠️ Configuration

### Environment Variables

You can configure AutoUpdaterBot using environment variables in a `.env` file (recommended) or directly in your shell.

| Variable        | Description                                               | Default         | Required  |
|-----------------|-----------------------------------------------------------|-----------------|-----------|
| `GITHUB_TOKEN`  | Your GitHub Personal Access Token (for private repos and higher API limits) | `None`          | Optional  |
| `DEFAULT_BRANCH`| Default branch name to use if not specified in CLI.        | `main`          | Optional  |
| `LOG_LEVEL`     | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)     | `INFO`          | Optional  |

### .env Example
```env
GITHUB_TOKEN=ghp_your_personal_access_token
DEFAULT_BRANCH=main
LOG_LEVEL=INFO
```

---

## 📁 Project Structure

```
62_AutoUpdaterBot/
├── agent.py                 # Core AutoUpdaterBot logic (pull, summarize, execute actions)
├── cli.py                   # Command Line Interface parsing and interaction
├── config.py                # Environment variables and default settings
├── github_service.py        # Handles Git operations (clone, pull, diff, log)
├── requirements.txt         # Python dependencies
├── env.example              # Template for environment variables
├── install.bat              # Windows installation script
├── start.bat                # Windows startup script
├── README.md                # This documentation
└── test_autoupdater.py      # Unit tests for the bot
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. "Git command not found"
**Solution:** Ensure Git is installed on your system and added to your system's PATH. You can download Git from [git-scm.com](https://git-scm.com/).

#### 2. "Authentication failed for 'https://github.com/..."
**Solution:**
- For private repositories, you need a GitHub Personal Access Token (`GITHUB_TOKEN`).
- Ensure your `GITHUB_TOKEN` is correctly set in your `.env` file or as an environment variable.
- Make sure the token has the necessary `repo` scope (for full control) or `public_repo` (for public repos only).

#### 3. "Repository not found" or "Invalid GitHub URL"
**Solution:**
- Double-check the GitHub repository URL for typos.
- Ensure the repository exists and is accessible (if private, confirm authentication).

#### 4. "Merge conflict"
**Solution:** AutoUpdaterBot will notify you of merge conflicts. You will need to manually resolve these conflicts in your local repository.

```bash
# Example steps to resolve a merge conflict:
cd /path/to/local/repo
git status
# Edit files to resolve conflicts
git add .
git commit -m "Resolve merge conflict"
```

#### 5. "ModuleNotFoundError: No module named '...' "
**Solution:** Ensure all dependencies are installed. Activate your virtual environment and run `pip install -r requirements.txt`.

---

## 🤝 Contributing

This project is part of the **#100DaysOfAI-Agents** challenge. We welcome contributions!

### How to Contribute
1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes** and add tests
4. **Commit your changes**: `git commit -m 'Add your amazing feature'`
5. **Push to the branch**: `git push origin feature/your-feature-name`
6. **Open a Pull Request**

### Areas for Contribution
- **🐛 Bug Fixes**: Report and fix bugs.
- **✨ New Features**: Add new functionalities (e.g., support for other Git providers, pre-commit hooks).
- **📚 Documentation**: Improve README, add more examples.
- **🧪 Testing**: Enhance test coverage.

---

## 📄 License

This project is part of the **#100DaysOfAI-Agents** challenge by [Muhammad Sami Asghar Mughal](https://github.com/SamiMughal).

---

## 🙏 Acknowledgments

- **Git**: The distributed version control system.
- **Python**: The programming language that makes it all possible.
- **Rich**: For beautiful terminal output and UI (if integrated).
- **#100DaysOfAI-Agents** - For the motivation to build amazing AI tools.

---

**Happy Updating! 🚀**
