"""
Web application for EmailWriterAgent using FastAPI
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
from pathlib import Path

from config import EmailConfig

class EmailRequest(BaseModel):
    prompt: str
    template: str = "formal"
    recipient: str = ""
    sender: str = ""
    signature: str = ""
    tone: Optional[str] = None

class EmailResponse(BaseModel):
    success: bool
    email: Optional[Dict[str, str]] = None
    error: Optional[str] = None

def create_app(email_agent):
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title=EmailConfig.WEB_TITLE,
        description=EmailConfig.WEB_DESCRIPTION,
        version=EmailConfig.WEB_VERSION
    )
    
    # Setup templates and static files
    templates = Jinja2Templates(directory="templates")
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    @app.get("/", response_class=HTMLResponse)
    async def home(request: Request):
        """Serve the main email composition interface"""
        templates_data = email_agent.get_templates()
        return templates.TemplateResponse(
            "index.html", 
            {
                "request": request,
                "templates": templates_data,
                "default_from": EmailConfig.DEFAULT_FROM,
                "default_signature": EmailConfig.DEFAULT_SIGNATURE
            }
        )
    
    @app.post("/api/generate-email", response_model=EmailResponse)
    async def generate_email(request: EmailRequest):
        """Generate an email using the EmailAgent"""
        try:
            if not request.prompt.strip():
                return EmailResponse(
                    success=False,
                    error="Email prompt is required"
                )
            
            email = email_agent.generate_email(
                prompt=request.prompt,
                template=request.template,
                recipient=request.recipient,
                sender=request.sender,
                signature=request.signature,
                tone=request.tone
            )
            
            return EmailResponse(
                success=True,
                email=email
            )
            
        except Exception as e:
            return EmailResponse(
                success=False,
                error=str(e)
            )
    
    @app.get("/api/templates")
    async def get_templates():
        """Get available email templates"""
        try:
            templates = email_agent.get_templates()
            return {"success": True, "templates": templates}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @app.get("/api/history")
    async def get_history():
        """Get email generation history"""
        try:
            history = email_agent.get_email_history()
            return {"success": True, "history": history}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @app.get("/api/health")
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "service": "EmailWriterAgent",
            "version": EmailConfig.WEB_VERSION
        }
    
    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc: HTTPException):
        """Handle 404 errors"""
        return JSONResponse(
            status_code=404,
            content={"error": "Endpoint not found"}
        )
    
    @app.exception_handler(500)
    async def internal_error_handler(request: Request, exc: HTTPException):
        """Handle 500 errors"""
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error"}
        )
    
    return app 