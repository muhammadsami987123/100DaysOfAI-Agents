from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import json
import base64
from typing import Optional, Dict, Any
import logging
from datetime import datetime

from mindmap_agent import MindMapAgent
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="MindMapDiagramAgent",
    description="AI-powered mind map diagram generator",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Mount exports directory
app.mount("/exports", StaticFiles(directory="exports"), name="exports")

# Initialize the mind map agent
mindmap_agent = MindMapAgent()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main web interface"""
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/api/generate-mindmap")
async def generate_mindmap(
    text_input: str = Form(...),
    diagram_type: str = Form("mindmap"),
    theme: str = Form("light"),
    depth_levels: int = Form(3),
    language: str = Form("en")
):
    """
    Generate a mind map from unstructured text input
    """
    try:
        logger.info(f"Generating mindmap for input length: {len(text_input)}")
        
        # Generate the mind map structure
        result = await mindmap_agent.generate_mindmap(
            text_input=text_input,
            diagram_type=diagram_type,
            theme=theme,
            depth_levels=depth_levels,
            language=language
        )
        
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error generating mindmap: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate mindmap: {str(e)}")

@app.post("/api/export-diagram")
async def export_diagram(
    diagram_data: str = Form(...),
    export_format: str = Form("png"),
    filename: str = Form("mindmap")
):
    """
    Export the generated diagram in various formats
    """
    try:
        logger.info(f"Exporting diagram in {export_format} format")
        
        # Export the diagram
        result = await mindmap_agent.export_diagram(
            diagram_data=diagram_data,
            export_format=export_format,
            filename=filename
        )
        
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error exporting diagram: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to export diagram: {str(e)}")

@app.post("/api/save-session")
async def save_session(
    session_data: str = Form(...),
    session_name: str = Form("untitled")
):
    """
    Save the current session to browser storage
    """
    try:
        # This is handled client-side, but we can validate the data
        data = json.loads(session_data)
        
        return JSONResponse(content={
            "success": True,
            "message": "Session data validated successfully",
            "session_name": session_name
        })
        
    except Exception as e:
        logger.error(f"Error saving session: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid session data: {str(e)}")

@app.get("/api/themes")
async def get_themes():
    """
    Get available themes for the diagrams
    """
    themes = {
        "light": {
            "name": "Light",
            "background": "#ffffff",
            "text": "#333333",
            "primary": "#3b82f6",
            "secondary": "#6b7280"
        },
        "dark": {
            "name": "Dark",
            "background": "#1f2937",
            "text": "#f9fafb",
            "primary": "#60a5fa",
            "secondary": "#9ca3af"
        },
        "blue": {
            "name": "Blue",
            "background": "#eff6ff",
            "text": "#1e40af",
            "primary": "#3b82f6",
            "secondary": "#60a5fa"
        },
        "green": {
            "name": "Green",
            "background": "#f0fdf4",
            "text": "#166534",
            "primary": "#22c55e",
            "secondary": "#4ade80"
        },
        "purple": {
            "name": "Purple",
            "background": "#faf5ff",
            "text": "#7c3aed",
            "primary": "#8b5cf6",
            "secondary": "#a78bfa"
        }
    }
    
    return JSONResponse(content=themes)

@app.get("/api/diagram-types")
async def get_diagram_types():
    """
    Get available diagram types
    """
    diagram_types = {
        "mindmap": {
            "name": "Mind Map",
            "description": "Hierarchical diagram showing relationships between concepts",
            "icon": "🧠"
        },
        "flowchart": {
            "name": "Flowchart",
            "description": "Process flow diagram showing steps and decisions",
            "icon": "📊"
        },
        "orgchart": {
            "name": "Organization Chart",
            "description": "Hierarchical structure showing organizational relationships",
            "icon": "🏢"
        },
        "network": {
            "name": "Network Diagram",
            "description": "Network of interconnected nodes and relationships",
            "icon": "🌐"
        }
    }
    
    return JSONResponse(content=diagram_types)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    config = Config()
    uvicorn.run(
        "server:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG
    )
