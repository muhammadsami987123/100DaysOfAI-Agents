# 💻 TerminalGPT — Day 34 of #100DaysOfAI-Agents

A CLI-based terminal command assistant that converts natural language into safe, executable terminal commands with explanations and safety warnings.

## ✨ Key Features

- **Natural Language Processing**: Convert plain English to terminal commands
- **OS Detection**: Auto-detects your OS and outputs PowerShell commands for Windows, Bash for macOS/Linux
- **Safety First**: Highlights risky operations with warnings and suggests safer alternatives
- **Structured Output**: Always responds with labeled sections: Command, Explanation, Safety Warning, Notes
- **Multilingual**: Understands English, Urdu, and Hindi; attempts to reply in your input language
- **Short-Term Memory**: Remembers recent commands in the session for better context
- **Streaming Output**: Uses OpenAI streaming; you see the answer appear progressively with a dynamic loader
- **Rich CLI UX**: Beautiful terminal interface with colors, spinners, and panels

## 🧩 Tech Stack

- **Language**: Python 3.9+
- **AI**: OpenAI Chat Completions API
- **CLI UX**: `rich` for color, spinners, panels, markdown rendering
- **Config**: `python-dotenv` for environment variables

## 🚀 Quick Start

### 1) Navigate
```bash
cd 34_TerminalGPT
```

### 2) Create `.env`
```env
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_MODEL=gpt-4o-mini
TEMPERATURE=0.1
MAX_TOKENS=400
DEFAULT_SHELL=bash
SAFETY_MODE=true
MAX_HISTORY_MESSAGES=6
```

### 3) Install dependencies
```bash
# Windows (PowerShell)
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# macOS/Linux
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4) Run
```bash
python main.py
```

Type `exit` or `quit` to end the session.

## 🧠 How It Works

- **Session Memory**: Keeps a rolling window of recent user/assistant turns (default 6 messages) for better context
- **Streaming**: Uses OpenAI's streaming to yield tokens as they arrive with a dynamic loader
- **OS-Specific Output**: Detects Windows/macOS/Linux and chooses appropriate shells and commands
- **Safety Mode**: Always suggests safer alternatives for destructive operations

## 🔧 Configuration

| Variable               | Default         | Description                                                | Required |
|------------------------|-----------------|------------------------------------------------------------|----------|
| `OPENAI_API_KEY`       | —               | Your OpenAI API key                                        | ✅       |
| `OPENAI_MODEL`         | `gpt-4o-mini`   | OpenAI chat model                                          | ❌       |
| `TEMPERATURE`          | `0.1`           | Creativity level (0.0–1.0)                                 | ❌       |
| `MAX_TOKENS`           | `400`           | Output token limit                                         | ❌       |
| `DEFAULT_SHELL`        | `bash`          | Default shell for unknown OS                               | ❌       |
| `SAFETY_MODE`          | `true`          | Enable safety warnings and safer alternatives              | ❌       |
| `MAX_HISTORY_MESSAGES` | `6`             | Number of recent messages to include in short-term memory  | ❌       |

## 📁 Project Structure

```
34_TerminalGPT/
├── terminal_agent.py    # Core TerminalGPT class (OS-aware, memory, streaming)
├── config.py            # Env loading + configuration
├── main.py              # CLI entry point (UI, loaders, streaming render)
├── requirements.txt     # openai, rich, python-dotenv
├── install.bat          # Windows: venv + deps
├── start.bat            # Windows: activate + run
└── README.md            # This file
```

## 💡 Usage

- You'll see these statuses:
  - **Listening…** waiting for your input
  - **Processing…** contacting OpenAI (animated loader)
  - **Formatting…** preparing Markdown
  - **Command Ready…** final nicely formatted output in a panel

- Ask in English, Urdu, or Hindi. Examples:
  - "Show hidden files"
  - "Create a new Python file"
  - "Remove all .tmp files in current folder"
  - "Find the size of each folder"
  - "List running processes"
  - "Copy file to backup directory"

- Follow-up questions will consider your previous commands during this session.

## 🧪 Example Sessions

### 1) Windows — Show hidden files
Input:
> Show hidden files

Output sections include:
- **Command**: PowerShell command with proper flags
- **Explanation**: What the command does
- **Safety Warning**: No (safe operation)
- **Notes**: Additional tips or alternatives

### 2) macOS — Remove temporary files
Input:
> Remove all .tmp files in current folder

Output includes:
- **Command**: `find . -name "*.tmp" -type f -delete` (with safety flags)
- **Explanation**: Recursive search and deletion
- **Safety Warning**: Yes - explains why it's risky
- **Notes**: Suggests `-print` flag first to preview

### 3) Follow-up with memory
Input:
> Do the same but for .log files

Output will reuse the context from the previous command and provide updated steps.

## 🛡️ Safety Notes

- Destructive operations are clearly marked with safety warnings
- Safer alternatives are suggested (e.g., `-i` flag for rm, `--dry-run` for destructive operations)
- Commands are tested for common pitfalls and edge cases
- Always review the command before executing, especially for destructive operations

## 🔍 Troubleshooting

- "OpenAI API key missing" → Create `.env` with `OPENAI_API_KEY`
- "Strange characters in terminal" → Use a UTF-8 capable terminal (Windows Terminal/PowerShell)
- "Network/SSL errors" → Check proxy/firewall, retry later
- "It forgot earlier context" → Memory is per-session and bounded; increase `MAX_HISTORY_MESSAGES` if needed

## 🗺️ Roadmap

- Command execution with confirmation prompts
- Command history and favorites
- Custom command templates
- Integration with popular shells (zsh, fish)
- Batch command processing

## 📝 Version History

- **v1.0.0** — Initial release: OS detection, safety warnings, streaming output, multilingual support

## 🤝 Contributing

Pull requests to improve command mappings, add safety checks, or enhance CLI UX are welcome.

## 📄 License

This project is part of the #100DaysOfAI-Agents challenge by Muhammad Sami Asghar Mughal.


