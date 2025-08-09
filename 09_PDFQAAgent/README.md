## 📄 PDFQAAgent – Day 9 of #100DaysOfAI-Agents

A production-quality, NotebookLM‑inspired agent that answers questions strictly from your own sources (PDF, DOCX/TXT, URL, or pasted text). It features a premium UI, session chat history, citations, JSONL logging, and a lightweight on‑disk vector store.

---

### ✨ What’s Included
- **Modern UI (Tailwind, dark theme)**
  - Intake tabs: Upload PDF, Enter URL, Paste text
  - Real‑time toasts and overlay loaders (uploading, fetching, indexing)
  - Three‑pane layout: Sources | Chat | Studio (placeholders)
  - Chat shows typing indicator and citations (page + chunk)
  - Session chat history with quick navigation
- **RAG backend**
  - Token‑aware chunking with overlap
  - OpenAI embeddings + cosine retrieval (NumPy, on‑disk store)
  - Strict grounding: “I don’t know…” when out‑of‑context
- **Robust extraction**
  - `pypdf` for PDFs
  - `python-docx` for DOCX
  - `trafilatura` with BeautifulSoup+`lxml` fallback for HTML
- **Observability**
  - JSONL logging per chat turn: question, preview, citations, session_id

---

### 🛠️ Tech Stack
- Backend: Flask (Python 3.10+)
- LLM/Embeddings: OpenAI SDK (`gpt-4o-mini`, `text-embedding-3-small` by default)
- Parsing: `pypdf`, `python-docx`, `trafilatura`, `beautifulsoup4`, `lxml`
- Vector store: NumPy + cosine similarity (persisted to disk)
- Config: `python-dotenv`
- UI: Tailwind CSS + vanilla JS

---

### 🚀 Quick Start

1) Create venv and install deps
```bash
cd 09_PDFQAAgent
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

2) Configure environment
Create `.env` in `09_PDFQAAgent/` with:
```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small
HOST=127.0.0.1
PORT=8000
DEBUG=true
CHUNK_SIZE_TOKENS=400
CHUNK_OVERLAP_TOKENS=40
TOP_K=6
MAX_CONTEXT_TOKENS=4000
LOG_ENABLED=true
LOG_FILE=logs/pdfqa_log.jsonl
```

3) Run the app
```bash
python server.py
# Open http://127.0.0.1:8000
```

Tip: Use Ctrl+Shift+R for a hard refresh after code changes.

---

### 💡 Using the App
- **Upload PDF**: drag & drop or select a file
  - Instant toast confirms reception; overlay indicates extraction
  - On success, you’ll see pages, characters, and file type
- **Enter URL**: paste an article or direct PDF link
  - Toast confirms paste; overlay shows “Fetching URL and extracting text…”
  - Robust extraction with HTML fallback
- **Paste text**: drop raw text
  - Dark‑on‑light input for readability; overlay during indexing
- **Chat**: ask grounded questions
  - Typing indicator while thinking
  - Answers show citations like `p.3#2`
  - Sidebar stores session history (click to reconstruct chat)

---

### 🧩 API Endpoints (JSON)
- `POST /api/session` → `{ session_id }`
- `POST /api/upload` (multipart) → `{ doc_id, num_pages, num_chars, ... }`
  - fields: `file`, `session_id`
- `POST /api/fetch_url` → `{ doc_id, num_pages, num_chars, ... }`
  - body: `{ url, session_id }`
- `POST /api/ingest_text` → `{ doc_id, num_pages, num_chars, ... }`
  - body: `{ text, title?, session_id }`
- `POST /api/chat` → `{ answer, citations[], history[] }`
  - body: `{ question, doc_id, session_id }`
- `GET /api/history?session_id=...` → `{ history[] }`

All answers are grounded strictly to retrieved chunks; if not found, the agent responds: “I don’t know based on the provided document.”

---

### 🧠 RAG Design
- Chunking: token‑aware with configurable overlap (`CHUNK_SIZE_TOKENS`, `CHUNK_OVERLAP_TOKENS`)
- Vector store: `data/docs/<doc_id>/` stores `embeddings.npy`, `chunks.jsonl`, `meta.json`
- Retrieval: cosine similarity over embeddings; `TOP_K` controls context width
- Context budget: `MAX_CONTEXT_TOKENS` ensures prompts stay within model limits
- Citations: page and chunk index are included with each answer

---

### 📝 Logging
- Enabled via `LOG_ENABLED=true`
- Writes JSONL to `LOG_FILE` (default `logs/pdfqa_log.jsonl`)
- Each record: timestamp, session_id, question, answer preview, citations

---

### 🔧 Configuration Summary
| Variable | Default | Notes |
|---|---|---|
| `OPENAI_API_KEY` | – | Required for embeddings and chat |
| `OPENAI_MODEL` | `gpt-4o-mini` | Change as desired |
| `EMBEDDING_MODEL` | `text-embedding-3-small` | Cost‑/speed‑optimized |
| `CHUNK_SIZE_TOKENS` | 400 | Token chunk size |
| `CHUNK_OVERLAP_TOKENS` | 40 | Overlap to preserve context |
| `TOP_K` | 6 | Retrieved chunks per query |
| `MAX_CONTEXT_TOKENS` | 4000 | Context cutoff when composing prompt |
| `LOG_ENABLED` | true | Enable JSONL logging |
| `LOG_FILE` | `logs/pdfqa_log.jsonl` | Output path |

---

### 🐛 Troubleshooting
- **No answers / “I don’t know…”**
  - Check `num_chars` in the upload response; if it’s near zero, the source didn’t yield text (try a direct PDF or richer article URL)
  - Verify `OPENAI_API_KEY` and internet connectivity
- **UI still shows “simulated”**
  - Browser cached an old page; use Ctrl+Shift+R or incognito
- **PDF upload succeeds but chat fails**
  - Check Flask console for errors
  - Ensure your key has access to the selected model
- **Windows path issues**
  - Run PowerShell as admin or use cmd; keep the project path ASCII‑only

---

### 📦 Project Structure
```
09_PDFQAAgent/
├── server.py                 # Flask API + session & history
├── config.py                 # .env config & paths
├── openai_service.py         # Embeddings + chat + token counting
├── document_loaders.py       # PDF/DOCX/TXT/URL loaders (robust HTML extraction)
├── text_splitter.py          # Token-aware chunking
├── vector_store.py           # NumPy vector store (cosine)
├── rag_pipeline.py           # Retrieval + prompt assembly + citations
├── logger.py                 # JSONL logging
├── templates/
│   └── index.html            # Premium UI (tabs, loaders, chat, history)
├── static/
│   ├── css/style.css         # Minimal shared styles
│   └── js/app.js             # (Not used in the inline demo variant)
├── data/
│   ├── uploads/              # Uploaded files
│   └── docs/<doc_id>/        # Embeddings/chunks/meta
├── logs/                     # JSONL logs (if enabled)
└── requirements.txt
```

---

### 🗺️ Roadmap (optional additions)
- Source panel with page counts and quick‑jump links
- Message actions (copy / expand / quote‑with‑citation)
- Dark‑mode preference persistence
- SSE/streaming progress for large documents
- Disk‑backed session store (SQLite) for persistence across restarts

---

### 🙏 Inspiration
This project is inspired by Google DeepMind’s NotebookLM experience, adapted for a local Flask + OpenAI SDK stack.

---

### 📄 License
MIT — part of the #100DaysOfAI-Agents challenge.
