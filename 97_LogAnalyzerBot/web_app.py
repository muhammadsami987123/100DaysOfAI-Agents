"""
FastAPI Web Application for LogAnalyzerBot
Provides web interface for log analysis
"""

import os
import json
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from agent import LogAnalyzerBot
from config import UPLOAD_FOLDER, MAX_FILE_SIZE, ALLOWED_EXTENSIONS

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# Initialize FastAPI app
app = FastAPI(title="LogAnalyzerBot", description="AI-Powered Log Analysis Tool")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize agent
agent = LogAnalyzerBot()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render home page"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/upload")
async def upload_log_file(file: UploadFile = File(...)):
    """Upload and parse log file"""
    try:
        # Check file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            return JSONResponse(
                status_code=400,
                content={"error": f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"}
            )
        
        # Read file content
        content = await file.read()
        
        # Check file size
        if len(content) > MAX_FILE_SIZE:
            return JSONResponse(
                status_code=400,
                content={"error": f"File too large. Maximum size: {MAX_FILE_SIZE / 1024 / 1024}MB"}
            )
        
        # Save file
        file_path = os.path.join(UPLOAD_FOLDER, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Load and parse
        result = agent.load_log_file(file_path)
        
        if result['success']:
            return JSONResponse(content={
                "success": True,
                "message": result['message'],
                "total_entries": result['total_entries'],
                "file_path": file_path
            })
        else:
            return JSONResponse(status_code=500, content={"error": result['error']})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/api/analyze-content")
async def analyze_content(content: str = Form(...)):
    """Analyze pasted log content"""
    try:
        result = agent.load_log_content(content)
        
        if result['success']:
            return JSONResponse(content={
                "success": True,
                "message": result['message'],
                "total_entries": result['total_entries']
            })
        else:
            return JSONResponse(status_code=500, content={"error": result['error']})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/api/analyze")
async def analyze_logs(
    start_date: str = Form(None),
    end_date: str = Form(None),
    log_levels: str = Form(None),
    keyword: str = Form(None),
    include_ai: bool = Form(True)
):
    """Perform log analysis with filters"""
    try:
        # Parse dates
        start_dt = datetime.fromisoformat(start_date) if start_date else None
        end_dt = datetime.fromisoformat(end_date) if end_date else None
        
        # Parse log levels
        levels = log_levels.split(',') if log_levels else None
        
        # Filter entries
        filtered_entries = agent.filter_entries(
            start_date=start_dt,
            end_date=end_dt,
            log_levels=levels,
            keyword=keyword
        )
        
        # Get summary
        summary = agent.get_summary(filtered_entries)
        
        # Add AI insights if requested
        if include_ai and agent.client:
            summary['ai_insights'] = agent.get_ai_insights(summary)
        
        return JSONResponse(content=summary)
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/api/explain-error")
async def explain_error(
    error_message: str = Form(...),
    log_level: str = Form("ERROR"),
    source: str = Form("unknown"),
    frequency: int = Form(1)
):
    """Get AI explanation for specific error"""
    try:
        context = {
            'log_level': log_level,
            'source': source,
            'frequency': frequency
        }
        
        explanation = agent.explain_error(error_message, context)
        
        return JSONResponse(content={
            "success": True,
            "explanation": explanation
        })
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/api/status")
async def get_status():
    """Get current status of loaded logs"""
    try:
        return JSONResponse(content={
            "loaded": len(agent.log_entries) > 0,
            "total_entries": len(agent.log_entries),
            "api_available": agent.client is not None
        })
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
