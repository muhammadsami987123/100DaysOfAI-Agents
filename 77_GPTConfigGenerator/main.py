from fastapi import FastAPI, Body, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import os
from agent import GPTConfigGenerator

app = FastAPI(title="GPTConfigGenerator", version="1.0.0")

# Initialize the agent
agent = GPTConfigGenerator()

# Serve static files (if directory exists)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Pydantic models for request/response
class ConfigGenerationRequest(BaseModel):
    user_request: str
    config_type: Optional[str] = "auto"
    format: Optional[str] = "json"

class ConfigExplanationRequest(BaseModel):
    config_content: str
    format: str

class ConfigConversionRequest(BaseModel):
    config_content: str
    from_format: str
    to_format: str

class ConfigValidationRequest(BaseModel):
    config_content: str
    format: str

@app.get("/")
async def serve_frontend():
    """Serve the main web interface"""
    return FileResponse("templates/index.html")

@app.post("/api/generate")
async def generate_config(request: ConfigGenerationRequest):
    """Generate a configuration file based on user request"""
    try:
        result = agent.generate_config(
            user_request=request.user_request,
            config_type=request.config_type,
            format=request.format
        )
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating config: {str(e)}")

@app.post("/api/explain")
async def explain_config(request: ConfigExplanationRequest):
    """Explain a configuration file in natural language"""
    try:
        result = agent.explain_config(
            config_content=request.config_content,
            format=request.format
        )
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error explaining config: {str(e)}")

@app.post("/api/convert")
async def convert_config(request: ConfigConversionRequest):
    """Convert configuration between different formats"""
    try:
        result = agent.convert_config(
            config_content=request.config_content,
            from_format=request.from_format,
            to_format=request.to_format
        )
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting config: {str(e)}")

@app.post("/api/validate")
async def validate_config(request: ConfigValidationRequest):
    """Validate a configuration file"""
    try:
        result = agent.validate_config(
            config_content=request.config_content,
            format=request.format
        )
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validating config: {str(e)}")

@app.get("/api/formats")
async def get_supported_formats():
    """Get list of supported configuration formats"""
    try:
        formats = agent.get_supported_formats()
        return JSONResponse(content={"formats": formats})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting formats: {str(e)}")

@app.get("/api/config-types")
async def get_config_types():
    """Get available configuration types"""
    try:
        config_types = agent.get_config_types()
        return JSONResponse(content={"config_types": config_types})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting config types: {str(e)}")

@app.get("/api/suggestions")
async def get_suggestions(config_type: str = "auto", format: str = "json"):
    """Get configuration suggestions"""
    try:
        suggestions = agent.get_suggestions(config_type, format)
        return JSONResponse(content={"suggestions": suggestions})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting suggestions: {str(e)}")

@app.get("/api/defaults")
async def get_default_values():
    """Get default configuration values"""
    try:
        defaults = agent.get_default_values()
        return JSONResponse(content={"defaults": defaults})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting defaults: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(content={"status": "healthy", "service": "GPTConfigGenerator"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
