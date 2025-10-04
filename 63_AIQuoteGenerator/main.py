from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
import os
from pathlib import Path

from config import Config
from ai_agent import AIQuoteGenerator

# Initialize FastAPI app
app = FastAPI(
    title=Config.APP_TITLE,
    description=Config.APP_DESCRIPTION,
    version="1.0.0"
)

# Initialize AIQuoteGenerator agent with error handling
quote_agent: Optional[AIQuoteGenerator] = None
try:
    quote_agent = AIQuoteGenerator()
except Exception as e:
    print(f"Warning: Could not initialize AIQuoteGenerator: {e}")
    quote_agent = None

# Setup templates and static files
# Ensure templates and static directories exist
current_dir = Path(__file__).parent
templates_dir = current_dir / "templates"
static_dir = current_dir / "static"
static_js_dir = static_dir / "js"
static_css_dir = static_dir / "css"

# Create directories if they don't exist
templates_dir.mkdir(parents=True, exist_ok=True)
static_dir.mkdir(parents=True, exist_ok=True)
static_js_dir.mkdir(parents=True, exist_ok=True)
static_css_dir.mkdir(parents=True, exist_ok=True)

templates = Jinja2Templates(directory=str(templates_dir))
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Pydantic models
class QuoteRequest(BaseModel):
    mood: str
    tone: str
    output_format: str

class QuoteResponse(BaseModel):
    success: bool
    quote: Optional[str] = None
    image_url: Optional[str] = None
    tweet_ready: Optional[str] = None
    error: Optional[str] = None

@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    try:
        Config.validate()
        print("✅ AIQuoteGenerator application initialized successfully!")
        if quote_agent is None:
            print("⚠️ Quote agent not available - some features may be limited")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        raise

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main quote generation interface"""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app_title": Config.APP_TITLE,
            "app_description": Config.APP_DESCRIPTION,
            "moods": Config.MOODS,
            "tones": Config.TONES,
            "output_formats": Config.OUTPUT_FORMATS
        }
    )

@app.post("/api/generate_quote", response_model=QuoteResponse)
async def generate_quote_api(request: QuoteRequest):
    """
    Generate a motivational quote based on user input.
    """
    try:
        if quote_agent is None:
            return QuoteResponse(
                success=False,
                error="AI Quote Generator is not available."
            )
        
        response = await quote_agent.generate_quote(
            mood=request.mood,
            tone=request.tone,
            output_format=request.output_format
        )
        return QuoteResponse(
            success=response.get("success", False),
            quote=response.get("quote"),
            image_url=response.get("image_url"),
            tweet_ready=response.get("tweet_ready"),
            error=response.get("error")
        )
    except Exception as e:
        print(f"Error in generate_quote_api: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": Config.APP_TITLE,
        "version": "1.0.0",
        "agent_available": quote_agent is not None
    }

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Handle 404 errors"""
    return JSONResponse(
        status_code=404,
        content={"error": "Endpoint not found", "detail": "The requested endpoint does not exist"}
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: HTTPException):
    """Handle 500 errors"""
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": "An unexpected error occurred"}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=Config.DEBUG,
        log_level="info"
    )
