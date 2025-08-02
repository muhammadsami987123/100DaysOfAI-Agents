from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
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

# Initialize weather agent with error handling
weather_agent = None
try:
    from ai_agent import WeatherAgent
    weather_agent = WeatherAgent()
except Exception as e:
    print(f"Warning: Could not initialize WeatherAgent: {e}")
    weather_agent = None

# Setup templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Pydantic models
class WeatherRequest(BaseModel):
    city: str
    include_voice: bool = True

class WeatherResponse(BaseModel):
    success: bool
    weather_data: Optional[dict] = None
    ai_response: Optional[str] = None
    voice_text: Optional[str] = None
    error: Optional[str] = None

@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    try:
        Config.validate()
        print("✅ Weather Speaker Agent initialized successfully!")
        if weather_agent is None:
            print("⚠️  Weather Agent not available - some features may be limited")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        raise

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main weather interface"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/test-weather/{city}")
async def test_weather(city: str):
    """Test endpoint to verify weather service is working"""
    try:
        from weather_service import WeatherService
        weather_service = WeatherService()
        
        weather_data, error = await weather_service.get_weather_data(city)
        
        if error:
            return {"success": False, "error": error, "data": None}
        
        return {"success": True, "error": None, "data": weather_data}
    except Exception as e:
        return {"success": False, "error": str(e), "data": None}

@app.post("/api/weather", response_model=WeatherResponse)
async def get_weather(request: WeatherRequest):
    """
    Get weather information for a city
    
    Args:
        request: WeatherRequest containing city name and voice preference
        
    Returns:
        WeatherResponse with weather data and AI enhancement
    """
    try:
        if not request.city.strip():
            return WeatherResponse(
                success=False,
                error="City name is required"
            )
        
        if weather_agent is None:
            return WeatherResponse(
                success=False,
                error="Weather agent not available"
            )
        
        # Get weather response from agent
        response = await weather_agent.get_weather_response(
            city=request.city.strip(),
            include_voice=request.include_voice
        )
        
        # Ensure all fields are properly set
        return WeatherResponse(
            success=response.get("success", False),
            weather_data=response.get("weather_data"),
            ai_response=response.get("ai_response"),
            voice_text=response.get("voice_text"),
            error=response.get("error")
        )
        
    except Exception as e:
        print(f"Error in get_weather: {e}")
        return WeatherResponse(
            success=False,
            error=f"Internal server error: {str(e)}"
        )

@app.post("/api/weather/tips")
async def get_weather_tips(request: WeatherRequest):
    """
    Get AI-generated weather tips for a city
    
    Args:
        request: WeatherRequest containing city name
        
    Returns:
        JSON response with weather tips
    """
    try:
        if not request.city.strip():
            raise HTTPException(status_code=400, detail="City name is required")
        
        if weather_agent is None:
            raise HTTPException(status_code=500, detail="Weather agent not available")
        
        # Get weather data first
        weather_response = await weather_agent.get_weather_response(
            city=request.city.strip(),
            include_voice=False
        )
        
        if not weather_response["success"]:
            raise HTTPException(status_code=404, detail=weather_response["error"])
        
        # Get tips
        tips = await weather_agent.get_weather_tips(weather_response["weather_data"])
        
        return {"tips": tips}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/api/voice/stop")
async def stop_voice():
    """Stop any ongoing voice output"""
    try:
        if weather_agent is None:
            return {"message": "Weather agent not available"}
        
        weather_agent.stop_voice()
        return {"message": "Voice stopped successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error stopping voice: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Weather Speaker Agent",
        "version": "1.0.0",
        "agent_available": weather_agent is not None
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