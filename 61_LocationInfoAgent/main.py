from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uvicorn
import os
from pathlib import Path

from config import Config

# Initialize FastAPI app
app = FastAPI(
    title=Config.APP_TITLE,
    description=Config.APP_DESCRIPTION,
    version="1.0.0"
)

# Initialize LocationInfoAgent with error handling
location_agent = None
try:
    from location_agent import LocationInfoAgent
    location_agent = LocationInfoAgent()
except Exception as e:
    print(f"Warning: Could not initialize LocationInfoAgent: {e}")
    location_agent = None

# Setup templates and static files
BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Pydantic models
class LocationRequest(BaseModel):
    place: str
    include_voice: bool = True

class LocationResponse(BaseModel):
    success: bool
    location_data: Optional[Dict[str, Any]] = None
    ai_response: Optional[str] = None
    map_embed_url: Optional[str] = None
    image_urls: List[str] = []
    voice_text: Optional[str] = None
    error: Optional[str] = None

@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    try:
        Config.validate()
        print("✅ Location Info Agent initialized successfully!")
        if location_agent is None:
            print("⚠️  Location Agent not available - some features may be limited")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        raise

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main location information interface"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/explore", response_model=LocationResponse)
async def explore_location(request: LocationRequest):
    """
    Get location information for a given place.
    """
    try:
        if not request.place.strip():
            return LocationResponse(
                success=False,
                error="Location name is required",
                ai_response="Please enter a location name to explore."
            )
        
        if location_agent is None:
            return LocationResponse(
                success=False,
                error="Location agent not available",
                ai_response="The AI location agent is not available. Please check server logs."
            )
        
        response = await location_agent.get_location_info(
            place=request.place.strip(),
            include_voice=request.include_voice
        )
        
        return LocationResponse(**response)
        
    except Exception as e:
        print(f"Error in explore_location: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/api/voice/stop")
async def stop_voice():
    """Stop any ongoing voice output"""
    try:
        if location_agent is None:
            raise HTTPException(status_code=500, detail="Location agent not available")
        
        location_agent.stop_voice()
        return {"message": "Voice stopped successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error stopping voice: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Location Info Agent",
        "version": "1.0.0",
        "agent_available": location_agent is not None
    }

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Handle 404 errors"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Endpoint not found", 
            "detail": "The requested endpoint does not exist",
            "ai_response": "I'm sorry, that endpoint does not exist. Please try a valid API route."
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle custom HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "ai_response": f"An error occurred: {exc.detail}"
        }
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Handle all other unexpected errors"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "ai_response": "An unexpected internal error occurred. Please try again later."
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
