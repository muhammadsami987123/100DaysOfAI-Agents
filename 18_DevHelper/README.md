# 🧰 DevHelper CLI Bot — Day 18 of #100DaysOfAI-Agents

A CLI-based Developer Assistant that behaves like a smart terminal chatbot. It helps with developer tasks such as:

- How to create/run HTML, Python, or JavaScript projects
- Explaining or generating terminal commands
- File operations guidance (create, delete, rename)
- Providing code snippets and step-by-step instructions
- Understanding questions in English, Urdu, or Hindi
- Auto-detecting your OS (Windows/macOS/Linux) and tailoring commands accordingly
- Streaming responses and short-term session memory for connected, consistent replies

---

## ✨ Key Features

- **OS Detection**: Auto-detects your OS and outputs PowerShell commands for Windows, Bash for macOS/Linux.
- **Structured Replies**: Always responds with labeled sections: Explanation, Steps, Commands, Code, Notes.
- **Multilingual**: Understands English, Urdu, and Hindi; attempts to reply in your input language.
- **Short-Term Memory (Session)**: Remembers the most recent turns (configurable) so follow-ups are consistent.
- **Streaming Output**: Uses OpenAI streaming; you see the answer appear progressively with a dynamic loader.
- **Fallback Defaults**: If file/folder names aren’t specified, uses `new_file.txt` and `New Folder`.
- **Clarification Handling**: Asks a brief clarifying question when the request is ambiguous.
- **Clean CLI UX**: Clear status cues — Listening, Processing, Formatting, Responding — with `rich` styling.

---

## 🧩 Tech Stack

- **Language**: Python 3.9+
- **AI**: OpenAI Chat Completions API
- **CLI UX**: `rich` for color, spinners, panels, markdown rendering
- **Config**: `python-dotenv` for environment variables

---

## 🚀 Quick Start

### 1) Navigate
```bash
cd 18_DevHelper_CLI_Bot
```

### 2) Create `.env`
```env
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_MODEL=gpt-4o-mini
TEMPERATURE=0.3
MAX_TOKENS=800
VOICE_INPUT=false
MAX_HISTORY_MESSAGES=10
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

---

## 🧠 How It Works

- **Session Memory**: The bot keeps a rolling window of recent user/assistant turns (default 10 messages). This makes follow-up questions feel connected to earlier context. Memory resets when you restart the app.
- **Streaming**: Uses OpenAI’s streaming to yield tokens as they arrive. The CLI shows a loader and progressively renders the final Markdown output.
- **OS-Specific Output**: Detects Windows/macOS/Linux and chooses appropriate shells and commands (PowerShell vs Bash).
- **Defaults**: When names are missing, it uses `new_file.txt` and `New Folder` automatically.

---

## 🔧 Configuration

| Variable               | Default         | Description                                                | Required |
|------------------------|-----------------|------------------------------------------------------------|----------|
| `OPENAI_API_KEY`       | —               | Your OpenAI API key                                        | ✅       |
| `OPENAI_MODEL`         | `gpt-4o-mini`   | OpenAI chat model                                          | ❌       |
| `TEMPERATURE`          | `0.3`           | Creativity level (0.0–1.0)                                 | ❌       |
| `MAX_TOKENS`           | `800`           | Output token limit                                         | ❌       |
| `VOICE_INPUT`          | `false`         | Reserved for future voice input toggle                     | ❌       |
| `MAX_HISTORY_MESSAGES` | `10`            | Number of recent messages to include in short-term memory  | ❌       |
| `DEFAULT_FILE_NAME`    | `new_file.txt`  | Default file name when not specified                       | ❌       |
| `DEFAULT_FOLDER_NAME`  | `New Folder`    | Default folder name when not specified                     | ❌       |

---

## 📁 Project Structure

```
18_DevHelper_CLI_Bot/
├── assistant.py        # Core DevHelper class (OS-aware, memory, streaming)
├── config.py           # Env loading + configuration
├── main.py             # CLI entry point (UI, loaders, streaming render)
├── requirements.txt    # openai, rich, python-dotenv
├── install.bat         # Windows: venv + deps
├── start.bat           # Windows: activate + run
└── README.md           # This file
```

---

## 💡 Usage

- You’ll see these statuses:
  - **Listening…** waiting for your input
  - **Processing…** contacting OpenAI (animated loader)
  - **Formatting…** preparing Markdown
  - **Responding…** final nicely formatted output in a panel

- Ask in English, Urdu, or Hindi. Examples:
  - “How to delete a folder using terminal on Windows?”
  - “Mujhe HTML ka sample project chahiye”
  - “Create a Python virtual environment and run a script”
  - “Rename a file on macOS”

- Follow-up questions will consider your previous messages during this session.

---

## 🧪 Example Sessions

### 1) Windows — Delete a folder
Input:
> How to delete a folder using terminal on Windows?

Output sections include:
- Explanation: safety guidance and overview
- Steps: exact sequence
- Commands: PowerShell and CMD variations
- Notes: guardrails (e.g., confirmation flags), undo considerations

### 2) Urdu — HTML sample project
Input:
> Mujhe HTML ka sample project chahiye

Output includes:
- مختصر وضاحت
- قدم بہ قدم ہدایات
- فولڈر اور فائلیں بنانے کے کمانڈز
- چلانے کا طریقہ (`start index.html` / `open index.html`)
- مکمل HTML نمونہ کوڈ

### 3) Follow-up with memory
Input:
> Use the same folder name as before but add a CSS file too

Output will reuse the earlier folder name from this session (short-term memory) and provide updated steps/commands.

---

## 🛡️ Safety Notes

- Destructive operations (e.g., `rm -rf`, `Remove-Item -Recurse -Force`) are shown with caution. Read the steps carefully and ensure paths are correct before executing.
- Prefer using a test directory first. On Windows, PowerShell `-WhatIf` can be used to simulate actions.

---

## 🔍 Troubleshooting

- “OpenAI API key missing” → Create `.env` with `OPENAI_API_KEY`.
- “Strange characters in terminal” → Use a UTF-8 capable terminal (Windows Terminal/PowerShell).
- “Network/SSL errors” → Check proxy/firewall, retry later.
- “It forgot earlier context” → Memory is per-session and bounded; increase `MAX_HISTORY_MESSAGES` if needed.

---

## 🗺️ Roadmap

- Optional voice input (behind `VOICE_INPUT` flag)
- Command-only quick view mode
- In-CLI memory management commands (e.g., clear, export)
- Persistable session transcripts

---

## 📝 Version History

- **v1.1.0** — Streaming output, dynamic loaders, short-term session memory
- **v1.0.0** — Initial release: OS detection, structured answers, multilingual support

---

## 🤝 Contributing

Pull requests to improve prompts, add examples, or enhance CLI UX are welcome.

---

## 📄 License

This project is part of the #100DaysOfAI-Agents challenge by Muhammad Sami Asghar Mughal.
