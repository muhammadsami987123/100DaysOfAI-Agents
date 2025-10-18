"""
FastAPI backend for ArticleRewriter
"""

from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uvicorn
from pathlib import Path
import os

from config import Config
from agents.article_rewriter_agent import ArticleRewriterAgent

# Initialize FastAPI app
app = FastAPI(
    title=Config.APP_TITLE,
    description=Config.APP_DESCRIPTION,
    version=Config.APP_VERSION
)

# Initialize ArticleRewriterAgent
rewriter_agent = None
try:
    rewriter_agent = ArticleRewriterAgent()
except Exception as e:
    print(f"Warning: Could not initialize ArticleRewriterAgent: {e}")
    rewriter_agent = None

# Setup templates and static files
BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Pydantic models
class RewriteRequest(BaseModel):
    content: str
    tone: str = "formal"
    language: str = "english"
    generate_variations: bool = True

class RewriteResponse(BaseModel):
    success: bool
    rewritten_content: Optional[str] = None
    variations: List[str] = []
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class SaveRequest(BaseModel):
    rewrite_data: Dict[str, Any]
    format: str = "txt"

class SaveResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    file_path: Optional[str] = None
    error: Optional[str] = None

@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    try:
        Config.validate()
        print("✅ ArticleRewriter initialized successfully!")
        if rewriter_agent is None:
            print("⚠️  ArticleRewriter agent not available - some features may be limited")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        raise

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main article rewriting interface"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "tones": Config.TONES,
        "languages": Config.LANGUAGES
    })

@app.post("/api/rewrite", response_model=RewriteResponse)
async def rewrite_article(request: RewriteRequest):
    """
    Rewrite article content in the specified tone and language
    """
    try:
        if not request.content.strip():
            return RewriteResponse(
                success=False,
                error="No content provided for rewriting"
            )
        
        if rewriter_agent is None:
            return RewriteResponse(
                success=False,
                error="ArticleRewriter agent not available"
            )
        
        # Validate tone and language
        if request.tone not in Config.TONES:
            return RewriteResponse(
                success=False,
                error=f"Invalid tone. Available tones: {list(Config.TONES.keys())}"
            )
        
        if request.language not in Config.LANGUAGES:
            return RewriteResponse(
                success=False,
                error=f"Invalid language. Available languages: {list(Config.LANGUAGES.keys())}"
            )
        
        result = rewriter_agent.rewrite_article(
            content=request.content,
            tone=request.tone,
            language=request.language,
            generate_variations=request.generate_variations
        )
        
        return RewriteResponse(**result)
        
    except Exception as e:
        print(f"Error in rewrite_article: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/api/save", response_model=SaveResponse)
async def save_rewrite(request: SaveRequest):
    """Save rewritten content to file"""
    try:
        if rewriter_agent is None:
            return SaveResponse(
                success=False,
                error="ArticleRewriter agent not available"
            )
        
        if request.format not in ["txt", "md"]:
            return SaveResponse(
                success=False,
                error="Invalid format. Supported formats: txt, md"
            )
        
        file_path = rewriter_agent.save_rewrite(request.rewrite_data, request.format)
        
        if file_path:
            return SaveResponse(
                success=True,
                message=f"Rewrite saved successfully",
                file_path=file_path
            )
        else:
            return SaveResponse(
                success=False,
                error="Failed to save rewrite"
            )
            
    except Exception as e:
        return SaveResponse(
            success=False,
            error=f"Error saving rewrite: {str(e)}"
        )

@app.get("/api/tones")
async def get_tones():
    """Get available tones for rewriting"""
    return {"tones": Config.TONES}

@app.get("/api/languages")
async def get_languages():
    """Get available languages for rewriting"""
    return {"languages": Config.LANGUAGES}

@app.get("/api/stats")
async def get_stats():
    """Get statistics about saved rewrites"""
    if rewriter_agent is None:
        return {"error": "ArticleRewriter agent not available"}
    
    return rewriter_agent.get_stats()

@app.get("/api/download/{filename}")
async def download_file(filename: str):
    """Download a saved rewrite file"""
    try:
        file_path = Path(Config.OUTPUTS_DIR) / filename
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        return FileResponse(
            path=str(file_path),
            filename=filename,
            media_type='application/octet-stream'
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading file: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "ArticleRewriter",
        "version": Config.APP_VERSION,
        "agent_available": rewriter_agent is not None
    }

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Handle 404 errors"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Endpoint not found",
            "detail": "The requested endpoint does not exist"
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle custom HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "detail": str(exc.detail)
        }
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Handle all other unexpected errors"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc)
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=Config.DEBUG,
        log_level="info"
    )
