from __future__ import annotations

import json
import secrets
from typing import Any, Dict, List

from flask import Flask, jsonify, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

from config import CONFIG, UPLOADS_DIR, DOCS_DIR, TEMPLATES_DIR, STATIC_DIR
from openai_service import OpenAIService
from document_loaders import (
    load_pdf_from_path,
    load_docx_from_path,
    load_txt_from_path,
    load_from_url,
)
from rag_pipeline import RAGPipeline
from vector_store import SimpleVectorStore
from logger import log_chat


ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}


app = Flask(
    __name__,
    template_folder=str(TEMPLATES_DIR),
    static_folder=str(STATIC_DIR),
)

openai_service = OpenAIService()
rag = RAGPipeline(openai_service)

# Simple in-memory session store: session_id -> { doc_id: str, history: List[Dict] }
SESSIONS: Dict[str, Dict[str, Any]] = {}


def ensure_session(session_id: str | None) -> str:
    sid = session_id or secrets.token_hex(8)
    if sid not in SESSIONS:
        SESSIONS[sid] = {"doc_id": "", "history": []}
    return sid


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/session", methods=["POST"])
def create_session():
    sid = ensure_session(None)
    return jsonify({"success": True, "session_id": sid})


@app.route("/api/upload", methods=["POST"])
def upload():
    sess_id = request.form.get("session_id") or request.args.get("session_id")
    sid = ensure_session(sess_id)

    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        return jsonify({"success": False, "error": f"Unsupported file type: .{ext}"}), 400

    doc_id = secrets.token_hex(8)
    save_path = UPLOADS_DIR / f"{doc_id}_{filename}"
    file.save(str(save_path))

    if ext == "pdf":
        doc = load_pdf_from_path(save_path)
    elif ext == "docx":
        doc = load_docx_from_path(save_path)
    else:
        doc = load_txt_from_path(save_path)

    store = rag.build_store(doc_id, title=doc.title, source=str(save_path), media_type=doc.media_type, pages=doc.pages)

    meta = {
        "session_id": sid,
        "doc_id": doc_id,
        "title": doc.title,
        "source": str(save_path),
        "media_type": doc.media_type,
        "num_pages": len(doc.pages),
        "num_chars": sum(len(p) for p in doc.pages),
        "vector_ready": store.is_ready(),
    }
    (DOCS_DIR / doc_id).mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / doc_id / "upload_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    # bind session to doc
    SESSIONS[sid]["doc_id"] = doc_id
    SESSIONS[sid]["history"] = []

    return jsonify({"success": True, **meta})


@app.route("/api/fetch_url", methods=["POST"])
def fetch_url():
    data = request.get_json(force=True)
    sess_id = data.get("session_id")
    sid = ensure_session(sess_id)

    url = (data.get("url") or "").strip()
    if not url:
        return jsonify({"success": False, "error": "URL is required"}), 400

    doc_id = secrets.token_hex(8)
    try:
        doc = load_from_url(url)
    except Exception as e:
        return jsonify({"success": False, "error": f"Failed to fetch URL: {e}"}), 400

    store = rag.build_store(doc_id, title=doc.title, source=url, media_type=doc.media_type, pages=doc.pages)

    meta = {
        "session_id": sid,
        "doc_id": doc_id,
        "title": doc.title,
        "source": url,
        "media_type": doc.media_type,
        "num_pages": len(doc.pages),
        "num_chars": sum(len(p) for p in doc.pages),
        "vector_ready": store.is_ready(),
    }
    (DOCS_DIR / doc_id).mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / doc_id / "url_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    SESSIONS[sid]["doc_id"] = doc_id
    SESSIONS[sid]["history"] = []

    return jsonify({"success": True, **meta})


@app.route("/api/ingest_text", methods=["POST"])
def ingest_text():
    data = request.get_json(force=True)
    sid = ensure_session(data.get("session_id"))
    text = (data.get("text") or "").strip()
    title = (data.get("title") or "Manual text").strip()
    if not text:
        return jsonify({"success": False, "error": "text is required"}), 400

    doc_id = secrets.token_hex(8)
    pages = [text]
    store = rag.build_store(doc_id, title=title, source=f"session:{sid}:manual", media_type="txt", pages=pages)

    meta = {
        "session_id": sid,
        "doc_id": doc_id,
        "title": title,
        "source": "manual",
        "media_type": "txt",
        "num_pages": len(pages),
        "num_chars": len(text),
        "vector_ready": store.is_ready(),
    }
    (DOCS_DIR / doc_id).mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / doc_id / "manual_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    SESSIONS[sid]["doc_id"] = doc_id
    SESSIONS[sid]["history"] = []

    return jsonify({"success": True, **meta})


@app.route("/api/history", methods=["GET"])
def get_history():
    sid = request.args.get("session_id")
    if not sid or sid not in SESSIONS:
        return jsonify({"success": False, "error": "Invalid session"}), 400
    return jsonify({"success": True, "session_id": sid, "doc_id": SESSIONS[sid].get("doc_id", ""), "history": SESSIONS[sid].get("history", [])})


@app.route("/api/chat", methods=["POST"])
def chat():
    data: Dict[str, Any] = request.get_json(force=True)
    question = (data.get("question") or "").strip()
    doc_id = (data.get("doc_id") or "").strip()
    sid = ensure_session(data.get("session_id"))

    if not question:
        return jsonify({"success": False, "error": "Question is required"}), 400
    if not doc_id:
        return jsonify({"success": False, "error": "doc_id is required"}), 400

    store = SimpleVectorStore(doc_id, openai_service)
    if not store.is_ready():
        return jsonify({"success": False, "error": "Document vectors not ready. Re-upload or refetch."}), 400

    history = SESSIONS[sid].get("history", [])
    result = rag.answer(store, question, history)

    # update history
    entry = {"question": question, "answer": result.get("answer", ""), "citations": result.get("citations", [])}
    history.append(entry)
    SESSIONS[sid]["history"] = history[-50:]  # cap

    log_chat(doc_id, question, result.get("answer", ""), result.get("citations", []), extra={"session_id": sid})
    return jsonify({"success": True, **result, "doc_id": doc_id, "session_id": sid, "history": history})


@app.route('/static/<path:path>')
def send_static(path: str):
    return send_from_directory(str(STATIC_DIR), path)


if __name__ == "__main__":
    app.run(host=CONFIG.host, port=CONFIG.port, debug=CONFIG.debug)
