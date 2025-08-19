## Day 19 — AutoReplyBot (Email/Chat Auto-Responder)

### Overview
AutoReplyBot is a CLI-based intelligent agent that reads messages from a predefined source (JSON inbox or chat log), understands context using GPT, and generates appropriate replies in manual or auto mode. It supports tones, multi-language replies, token-based conversation memory (per thread, up to 100 turns), and streaming output. Each generated message can be copied easily from the terminal and is saved to an outbox file.

### Features
- Manual mode: Preview and optionally edit the suggested reply before sending
- Auto mode: Send GPT-generated replies automatically with a pre-configured tone
- Multi-language support: auto-detect or force a preferred language
- Memory: per-thread rolling memory up to 100 turns
- Streaming responses: smoother CLI experience (toggle with `--no-stream`)
- Copy option: replies rendered plainly for quick copy; also saved to `data/outbox.json`
- Status indicators: "Reading message", "Generating reply", "Reply sent"
- Configurable keywords, tone, and blacklist contacts
 - Optional Gmail integration: read unread messages and send replies

### Optional Add-ons (placeholders)
- Schedule replies (toggle via env; implement hook)
- Voice support (toggle via env; integrate TTS/STT if desired)
- Webhook integration (map live inbox/chat APIs to JSON schema used here)

### Project Structure
```
19_AutoReplyBot/
├── main.py            # Entry point
├── cli.py             # CLI, manual/auto modes, streaming UI
├── agent.py           # Core AutoReplyBot logic, memory, OpenAI calls
├── sources.py         # JSON sources for inbox/chat, outbox writer
├── gmail_service.py   # Gmail OAuth + read/send helpers
├── config.py          # Env and defaults
├── requirements.txt   # Dependencies
├── data/
│   ├── inbox.json     # Sample email inbox
│   ├── chat_log.json  # Sample chat log
│   └── outbox.json    # Replies written here
└── README.md          # This file
```

### Installation
1) Create/activate a virtual environment (Windows):
```powershell
python -m venv venv
./venv/Scripts/Activate.ps1
```

2) Install dependencies:
```powershell
pip install -r requirements.txt
```

3) Set your OpenAI API key:
```powershell
$env:OPENAI_API_KEY="your_api_key_here"
```
Or create a `.env` file in `19_AutoReplyBot/`:
```
OPENAI_API_KEY=your_api_key_here
```

### Gmail Setup (Optional)

#### 1) Create `credentials.json` (Google Cloud)
Follow these steps to enable Gmail API and generate a Desktop OAuth client:
- Go to the Google Cloud Console (`https://console.cloud.google.com`)
- Create or select a project
- Enable the Gmail API:
  - APIs & Services → Library → search "Gmail API" → Enable
- Configure OAuth consent screen:
  - External or Internal → add app name and email → Save
- Create OAuth client credentials:
  - APIs & Services → Credentials → Create Credentials → OAuth client ID
  - Application type: Desktop app → Create
  - Download the JSON and rename it to `credentials.json`
- Place it at: `19_AutoReplyBot/data/credentials.json`

#### 2) Configure environment (.env)
Create `19_AutoReplyBot/.env` with:
```
OPENAI_API_KEY=your_openai_key_here

GMAIL_ENABLED=true
GMAIL_QUERY=is:unread -category:promotions -category:social
GMAIL_MAX_RESULTS=20
GMAIL_CREDENTIALS_FILE=./data/credentials.json
GMAIL_TOKEN_FILE=./data/token.json
GMAIL_USER=me
```

Notes:
- `GMAIL_USER=me` means the authenticated account. Keep it as `me` for most cases.
- First run will open a browser to authorize the app. A token is saved to `data/token.json`.

#### 3) Run with Gmail sending enabled
Use `--send` to actually deliver emails through Gmail (otherwise drafts are only written to `data/outbox.json`).
```powershell
cd 19_AutoReplyBot
python main.py --mode manual --source gmail --send
```

#### 4) Troubleshooting Gmail send
- Not sending and UI says saved to outbox:
  - Ensure `--send` is provided and `GMAIL_ENABLED=true`.
- Token missing Gmail send permission:
  - Delete the token to force re-auth: `del data\token.json` (Windows) or `rm data/token.json` (macOS/Linux)
  - Run again and complete the browser auth flow.
- Wrong credentials path:
  - Ensure `GMAIL_CREDENTIALS_FILE` points to `./data/credentials.json`.
- Still not in Sent folder:
  - The app now re-prompts if scopes are insufficient and replies in-thread using Gmail `threadId`.
  - Check the console output for "Sent via Gmail: <id>". If missing, review warnings printed by the CLI.

### Usage
Run from the `19_AutoReplyBot` directory:
```powershell
python main.py --mode manual --source both --tone friendly --lang auto
```

CLI options:
- `--mode`: `manual` or `auto` (default: manual)
- `--source`: `email`, `chat`, or `both` (default: both)
- For Gmail: `--source gmail` and add `--send` to actually send replies
- `--tone`: `formal`, `friendly`, `technical`, `concise` (default from env)
- `--lang`: Preferred language or `auto` (default from env)
- `--max`: Max messages to process (default 50)
- `--no-stream`: Disable streaming

Interactive manual mode tips:
- You will see a list of messages. Enter the number to open.
- Use `ignore N` to remove a suggestion from the list.
- After composing, choose `send`, `back` to return to the list, or `exit`.

### Data Format
`data/inbox.json` (emails):
```json
[
  {
    "id": "e1",
    "from": "john@example.com",
    "to": "me@example.com",
    "subject": "Meeting Tomorrow",
    "body": "Can we move our meeting to 2 PM?",
    "timestamp": "2025-01-01T10:00:00Z",
    "thread_id": "t-123"
  }
]
```

`data/chat_log.json` (chats):
```json
[
  {
    "id": "c1",
    "from": "alice",
    "to": "me",
    "text": "hey, can you review my PR today?",
    "timestamp": "2025-01-01T11:00:00Z",
    "thread_id": "t-abc"
  }
]
```

Replies are written to `data/outbox.json` as an array of objects with `thread_id`, `in_reply_to`, `channel`, `reply`, `timestamp`.

### Notes
- For real email/chat integrations, build adapters that convert live messages to the above JSON schema and call the CLI periodically or via webhook.
- Blacklist and keyword filters are configurable via environment variables.
- For consistent structure and style, this project follows previous days' patterns (Day 6/7/18) for CLI/streaming and configuration management.


