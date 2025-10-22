from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

from summarize import GPTSummarizer

app = FastAPI()

# Initialize summarizer agent
summarizer = GPTSummarizer()

# Static files setup
BASE_DIR = Path(__file__).parent
app.mount("/frontend", StaticFiles(directory=BASE_DIR / "frontend"), name="frontend")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open(BASE_DIR / "frontend" / "index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.post("/summarize")
async def summarize_note(request: Request):
    data = await request.json()
    note = data.get("note")

    if not note:
        raise HTTPException(status_code=400, detail="No note provided for summarization.")

    summary = summarizer.summarize_text(note)
    
    # Check if the summary contains an error message
    if summary and summary[0].startswith("Error:"):
        raise HTTPException(status_code=500, detail=summary[0])

    return JSONResponse(content={"summary": summary})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
