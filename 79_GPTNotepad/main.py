from fastapi import FastAPI, Request, HTTPException, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import uvicorn
import os

from config import Config
from agents.agent import GPTSummarizerAgent

# Initialize FastAPI app
app = FastAPI(
    title=Config.APP_TITLE,
    description=Config.APP_DESCRIPTION,
    version=Config.APP_VERSION
)

# Initialize summarizer agent
summarizer_agent = GPTSummarizerAgent()

# Static files setup
BASE_DIR = Path(__file__).parent
app.mount("/frontend", StaticFiles(directory=BASE_DIR / "frontend"), name="frontend")

@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    try:
        Config.validate()
        print("✅ GPTNotepad initialized successfully!")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        raise

@app.get("/")
async def read_root():
    with open(BASE_DIR / "frontend" / "index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.post("/summarize")
async def summarize(
    note: str = Form(None),
    url: str = Form(None),
    file: UploadFile = File(None)
):
    if file is not None:
        file_bytes = await file.read()
        note_text = summarizer_agent.extract_text_from_file(file, file_bytes)
        source = file.filename
    elif url:
        note_text = summarizer_agent.extract_text_from_url(url)
        source = url
    elif note:
        note_text = note
        source = "manual input"
    else:
        raise HTTPException(status_code=400, detail="No note, file, or URL provided for summarization.")

    if not note_text or not note_text.strip():
        raise HTTPException(status_code=400, detail="Failed to extract text from the provided input.")

    result = summarizer_agent.summarize_with_notes(note_text)
    if not result.get("summary") or not result.get("notes"):
        raise HTTPException(status_code=500, detail="Failed to generate summary or notes.")

    return JSONResponse(content=result)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=Config.DEBUG,
        log_level="info"
    )
