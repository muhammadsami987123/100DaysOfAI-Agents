# 🎨 AIComicWriter — Day 51 of #100DaysOfAI-Agents

<div align="center">

![AIComicWriter Banner](https://img.shields.io/badge/AIComicWriter-Day%2051-blue?style=for-the-badge&logo=comics&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![AI Models](https://img.shields.io/badge/AI%20Models-HuggingFace%20%7C%20OpenAI-orange?style=for-the-badge&logo=openai&logoColor=white)
![CLI](https://img.shields.io/badge/Interface-CLI-red?style=for-the-badge&logo=terminal&logoColor=white)

**Generate, Suggest, and Refactor Comic Scripts with AI-Powered Creativity**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎭 Examples](#-examples) • [⚙️ Configuration](#-configuration) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is AIComicWriter?

AIComicWriter is a CLI-based intelligent agent designed to empower users in creating complete, creative, and humorous comic book scripts. From a simple prompt or a rough draft, this agent generates well-structured comic panels, offers fresh ideas, and refines existing drafts to improve pacing, humor, and visual storytelling.

### 🌟 Key Highlights

-   **✍️ AI Comic Generation**: Transform ideas into panel-by-panel comic scripts with dialogue.
-   **💡 Random Idea Suggestions**: Overcome writer's block with creative loglines and titles.
-   **📝 Comic Draft Refactoring**: Improve pacing, humor, and visual structure of existing drafts.
-   **⚙️ Flexible AI Backend**: Choose between Hugging Face `transformers` or OpenAI API for generation.
-   **🎨 Rich CLI UI**: An interactive, visually appealing command-line interface with `rich`.
-   **💾 Export Options**: Save generated scripts and ideas to `.md` or `.txt` files.
-   **📋 Customizable Output**: Control tone, number of panels, and output format.
-   **📋 Clipboard Integration**: Easily copy generated content to your clipboard.

---

## 🎯 Features

### 🚀 Core Functionality
-   ✅ **AI-Powered Generation**: Create structured comic scripts from diverse prompts.
-   ✅ **Creative Idea Generation**: Get inspiring random comic ideas with titles and loglines.
-   ✅ **Intelligent Refactoring**: Improve existing comic drafts for enhanced narrative flow and humor.
-   ✅ **Dynamic Prompts**: Interactive input for all generation and refactoring options.
-   ✅ **Error Handling**: Robust error messages and graceful fallback for AI backend issues.

### 🎭 Creative Options
-   ✅ **Tone Selection**: Choose from `funny`, `dramatic`, `dark`, `action`, `sci-fi`, `fantasy`.
-   ✅ **Panel Customization**: Specify the desired number of comic panels (default: 6).
-   ✅ **Flexible AI Models**: Seamlessly switch between Hugging Face (default) and OpenAI models.

### 💻 User Interface
-   ✅ **Interactive Main Menu**: Easy navigation through different agent functionalities.
-   ✅ **Rich Terminal Output**: Beautifully formatted text, tables, and panels using `rich`.
-   ✅ **Progress Spinners**: Visual feedback during AI processing tasks.
-   ✅ **Help Documentation**: Integrated `--help` and a menu option for detailed usage.
-   ✅ **Output Formatting**: Markdown output by default, with an option for plain text.
-   ✅ **Clipboard Copy**: One-click option to copy generated content to clipboard.

---

## 🚀 Quick Start

### 📋 Prerequisites

-   **Python 3.8+** installed on your system
-   **Internet connection** for AI model downloads (Hugging Face) or API calls (OpenAI)
-   **OpenAI API Key** (get one from [OpenAI Platform](https://platform.openai.com/api-keys)) - *Optional, for using OpenAI's models*

### ⚡ Installation

1.  **Navigate to the project directory:**
    ```bash
    cd 51_AIComicWriter
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv

    # Windows
    venv\Scripts\activate

    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up OpenAI API key (Optional):**
    If you wish to use OpenAI's models, set your `OPENAI_API_KEY` as an environment variable or create a `.env` file in the project root:
    
    **Option A: Environment Variable (Recommended)**
    ```bash
    # Windows (Command Prompt)
    set OPENAI_API_KEY=your_openai_api_key_here

    # Windows (PowerShell)
    $env:OPENAI_API_KEY="your_openai_api_key_here"

    # Linux/Mac
    export OPENAI_API_KEY=your_openai_api_key_here
    ```

    **Option B: .env file**
    Create a `.env` file in the `51_AIComicWriter` directory:
    ```env
    OPENAI_API_KEY=your_openai_api_key_here
    # Optional: Specify OpenAI model (e.g., gpt-4o-mini, gpt-3.5-turbo)
    # OPENAI_MODEL=gpt-3.5-turbo
    ```

---

### Running AIComicWriter

#### Interactive Menu Mode (Recommended)
Run the agent without any arguments to enter the interactive menu:
```bash
python main.py
```
This will present you with a menu of options to generate, suggest, or refactor comic scripts. Within the interactive menu, you will be prompted if you wish to use the OpenAI API for that specific task.

#### Direct Command Line Usage
You can also use the agent directly from the command line with specific commands and flags:
```bash
# Generate a funny comic about a cat taking over the world using Hugging Face (default)
python main.py generate \
  --topic "A cat that wants to take over the world" \
  --characters "Mr. Whiskers (cat), Dave (lazy roommate)" \
  --tone funny \
  --panels 6 \
  --save cat_comic.md

# Generate a dramatic comic using OpenAI API
python main.py generate \
  --topic "A space explorer finding an ancient alien artifact" \
  --characters "Captain Eva, Zorp the Alien" \
  --tone dramatic \
  --panels 8 \
  --use-openai \
  --save space_comic.md

# Get a random comic idea and save it to a file using OpenAI API
python main.py random --use-openai --save random_idea.md

# Refactor a comic draft (you will be prompted to paste the draft) using Hugging Face
python main.py refactor --format text --save refactored.txt
```

---

## 🎭 Examples & Usage

### 💻 Terminal Interface

The enhanced terminal interface offers powerful command-line functionality and an interactive menu:

```bash
# Start the interactive menu (recommended for first-time users)
python main.py

# Access help documentation
python main.py --help
# Or from the interactive menu, select option 4: View Help
```

#### Main Menu Options:
-   **1. Generate Comic from Prompt**: Create a new comic script from your ideas.
-   **2. Suggest a Random Comic Idea**: Get a fresh, creative comic concept.
-   **3. Refactor My Comic Draft**: Improve an existing comic draft.
-   **4. View Help**: Show detailed command and flag information.
-   **0. Exit**: Exit the application.

#### Detailed Command-Line Examples:

##### Generate Comic from Prompt
Generate a complete comic script by providing a topic, characters, tone, and number of panels.
```bash
python main.py generate \
  --topic "A cat that wants to take over the world" \
  --characters "Mr. Whiskers (cat), Dave (lazy roommate)" \
  --tone funny \
  --panels 6 \
  --save cat_comic.md \
  # Add --use-openai flag here if you want to use OpenAI API
```

##### Suggest a Random Comic Idea
Get a fresh, AI-generated comic idea with a title and logline.
```bash
python main.py random --save random_idea.md --use-openai
```

##### Refactor My Comic Draft
Paste an existing comic draft into the CLI, and the agent will improve its pacing, humor, or visual structure. The agent will prompt you for the draft after you run the command.
```bash
python main.py refactor --format text --save improved_draft.txt --use-openai
```

### ⚙️ Customization Flags:

-   `--tone <funny|dramatic|dark|action|sci-fi|fantasy>`: Specify the tone of the comic (default: `funny`).
-   `--panels <number>`: Set the desired number of panels (default: `6`).
-   `--format <markdown|text>`: Choose the output format (default: `markdown`).
-   `--save <filename.md/.txt>`: Export the comic script to a file.
-   `--use-openai`: Use OpenAI API for generation (requires `OPENAI_API_KEY`). By default, Hugging Face `t5-small` is used.

---

## 🏗️ Project Architecture

### 📁 File Structure

```
51_AIComicWriter/
├── 📄 main.py                   # Main CLI entry point and interactive menu
├── ⚙️ config.py                 # Configuration for AI backends (Hugging Face/OpenAI)
├── 🧠 core/
│   ├── 📄 comic_generator.py        # Logic for AI comic script generation
│   ├── 📄 random_idea_generator.py  # Logic for AI random comic idea generation
│   └── 📄 comic_refactorer.py       # Logic for AI comic draft refactoring
├── 🛠️ utils/
│   └── 📄 cli_interface.py       # Rich terminal UI for enhanced output
├── 📋 requirements.txt           # Python dependencies (click, transformers, torch, rich, pyperclip, openai, python-dotenv)
├── 🔧 .env.example              # Environment variables template
├── 📄 README.md                # This comprehensive documentation
├── 📄 test_input.md            # Example input for testing comic generation
└── 📚 venv/                    # Python virtual environment (ignored by Git)
```

### 🔧 Technical Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Python 3.8+ | Core application logic |
| **AI Engine** | Hugging Face Transformers | Default text generation (e.g., T5-small) |
| **AI Engine (Optional)** | OpenAI API (GPT-3.5-turbo) | Advanced text generation |
| **CLI Framework** | Click | Building the command-line interface |
| **UI Enhancements** | Rich | Beautiful and interactive terminal output |
| **Environment** | python-dotenv | Loading environment variables |
| **Clipboard** | pyperclip | Copying output to clipboard |

---

## 🤝 Contributing

We welcome contributions to make AIComicWriter even better!

### 🛠️ How to Contribute

1.  **Fork the repository**
2.  **Create a feature branch**: `git checkout -b feature/your-feature-name`
3.  **Make your changes** and test thoroughly
4.  **Commit your changes**: `git commit -m 'Add new feature: brief description'`
5.  **Push to the branch**: `git push origin feature/your-feature-name`
6.  **Open a Pull Request**

### 🎯 Areas for Contribution

-   **New AI Models**: Integrate other text generation models.
-   **Improved Parsing**: Enhance the parsing of generated comic scripts.
-   **UI Improvements**: Further refine the interactive CLI experience.
-   **More Customization**: Add more flags for fine-grained control over generation.
-   **Testing**: Add more comprehensive test cases.
-   **Bug Fixes**: Report and fix any issues.

---

## 📞 Support & Community

### 🆘 Getting Help

1.  **📖 Documentation**: Check this README and in-code comments.
2.  **🔍 Troubleshooting**: Review common issues.
3.  **📊 Logs**: Check terminal output for error messages.
4.  **🌐 API Status**: Verify Hugging Face and OpenAI API services are operational.

### 🐛 Reporting Issues

When reporting issues, please include:
-   **System Information**: OS, Python version.
-   **Error Messages**: Full error output or traceback.
-   **Steps to Reproduce**: What you were doing when it happened.
-   **Expected vs Actual**: What you expected vs what actually happened.

### 💬 Community

-   **GitHub Issues**: Report bugs and request features.

---

## 📄 License & Credits

### 📜 License

This project is part of the **#100DaysOfAI-Agents** challenge by **Muhammad Sami Asghar Mughal**.

**MIT License** - Feel free to use, modify, and distribute!

### 🙏 Acknowledgments

-   **Hugging Face** for providing open-source transformers and models.
-   **OpenAI** for their powerful API.
-   **Click** for the command-line interface framework.
-   **Rich** for the beautiful terminal rendering.
-   **Python community** for amazing libraries.
-   **All contributors** who help improve this project.

---

<div align="center">

## 🎉 Ready to Create Your Comics?

**Unleash your creativity and generate amazing comic scripts with AIComicWriter!**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎭 Examples](#-examples) • [⚙️ Configuration](#-configuration)

---

**Made with ❤️ by the #100DaysOfAI-Agents community**

*Day 51 of 100 - Building the future of AI agents, one day at a time!*

</div>
