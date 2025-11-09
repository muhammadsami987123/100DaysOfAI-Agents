"""
FastAPI Web Application for EBookReaderAgent
Provides web interface for eBook reading and analysis
"""

import os
import json
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from agent import EBookReaderAgent
from config import Config
from utils.llm_service import LLMService
from datetime import datetime

# Create necessary directories
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)
os.makedirs(Config.OUTPUT_FOLDER, exist_ok=True)

# Initialize FastAPI app
app = FastAPI(title="EBookReaderAgent", description="AI-Powered eBook Reader and Analyzer")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize agent
agent = EBookReaderAgent(llm_service=LLMService())


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render home page"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "default_llm": Config.DEFAULT_LLM
    })


@app.post("/api/upload")
async def upload_book(file: UploadFile = File(...)):
    """Upload and parse book file"""
    try:
        # Check file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in Config.ALLOWED_EXTENSIONS:
            return JSONResponse(
                status_code=400,
                content={"error": f"Invalid file type. Allowed: {', '.join(Config.ALLOWED_EXTENSIONS)}"}
            )
        
        # Read file content
        content = await file.read()
        
        # Check file size
        if len(content) > Config.MAX_FILE_SIZE:
            return JSONResponse(
                status_code=400,
                content={"error": f"File too large. Maximum size: {Config.MAX_FILE_SIZE / 1024 / 1024}MB"}
            )
        
        # Save file
        file_path = os.path.join(Config.UPLOAD_FOLDER, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Load and parse book
        result = agent.load_book(file_path)
        
        if result['success']:
            # Get book info
            book_info = agent.get_book_info()
            return JSONResponse(content={
                "success": True,
                "message": result['message'],
                "book_info": book_info,
                "file_path": file_path
            })
        else:
            return JSONResponse(status_code=500, content={"error": result['error']})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/api/load-from-url")
async def load_book_from_url(url: str = Form(...)):
    """Load and parse book from a public URL"""
    try:
        # Validate URL
        if not url.startswith(('http://', 'https://')):
            return JSONResponse(
                status_code=400,
                content={"error": "Invalid URL format. Must start with http:// or https://"}
            )
        
        # Load and parse book from URL
        result = agent.load_book(url)
        
        if result['success']:
            # Get book info
            book_info = agent.get_book_info()
            return JSONResponse(content={
                "success": True,
                "message": result['message'],
                "book_info": book_info,
                "source": "url"
            })
        else:
            return JSONResponse(status_code=500, content={"error": result['error']})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/api/book-info")
async def get_book_info():
    """Get information about currently loaded book"""
    try:
        book_info = agent.get_book_info()
        return JSONResponse(content=book_info)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/api/summarize-chapter")
async def summarize_chapter(chapter_number: int = Form(...)):
    """Generate summary for a specific chapter"""
    try:
        result = agent.summarize_chapter(chapter_number)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/api/summarize-all")
async def summarize_all():
    """Generate summaries for all chapters"""
    try:
        result = agent.summarize_all_chapters()
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/api/key-takeaways")
async def get_key_takeaways(num_takeaways: int = Form(10)):
    """Get key takeaways from the book"""
    try:
        result = agent.get_key_takeaways(num_takeaways)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/api/ask-question")
async def ask_question(
    question: str = Form(...),
    chapter_number: int = Form(None)
):
    """Ask a question about the book"""
    try:
        result = agent.ask_question(question, chapter_number if chapter_number else None)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/api/get-quotes")
async def get_quotes(
    chapter_number: int = Form(None),
    num_quotes: int = Form(5)
):
    """Get important quotes from the book"""
    try:
        result = agent.get_important_quotes(chapter_number if chapter_number else None, num_quotes)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/api/analyze")
async def analyze_book(
    include_summaries: bool = Form(True),
    include_takeaways: bool = Form(True),
    include_quotes: bool = Form(True)
):
    """Complete book analysis"""
    try:
        result = agent.analyze_book(
            include_summaries=include_summaries,
            include_takeaways=include_takeaways,
            include_quotes=include_quotes
        )
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/api/set-llm")
async def set_llm(llm_choice: str = Form(...)):
    """Set the LLM to use"""
    try:
        agent.llm_service.set_llm(llm_choice)
        return JSONResponse(content={
            "success": True,
            "message": f"LLM set to {llm_choice}"
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/api/status")
async def get_status():
    """Get current status"""
    try:
        return JSONResponse(content={
            "book_loaded": agent.current_book_loaded,
            "api_available": agent.llm_service.gemini_client is not None or agent.llm_service.openai_client is not None,
            "current_llm": agent.llm_service.current_llm
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
