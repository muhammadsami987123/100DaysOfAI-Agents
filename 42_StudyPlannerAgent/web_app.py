"""
StudyPlannerAgent Web Application
FastAPI web server for the study planning interface
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import uvicorn

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from utils.plan_generator import StudyPlanGenerator
from config import StudyConfig, get_api_key, setup_instructions

# Pydantic models for API
class StudyPlanRequest(BaseModel):
    goal: str = Field(..., description="Study goal", min_length=1, max_length=500)
    days_available: int = Field(..., description="Number of days available", ge=1, le=365)
    hours_per_day: int = Field(..., description="Hours per day", ge=1, le=12)
    learning_style: str = Field(..., description="Learning style")
    difficulty: str = Field(..., description="Difficulty level")
    subject: str = Field("", description="Subject area")
    template: str = Field("detailed", description="Plan template")

class StudyPlanResponse(BaseModel):
    success: bool
    plan: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class PlansListResponse(BaseModel):
    success: bool
    plans: List[Dict[str, Any]] = []
    total: int = 0

def create_app(plan_generator: StudyPlanGenerator):
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title=StudyConfig.WEB_TITLE,
        description=StudyConfig.WEB_DESCRIPTION,
        version=StudyConfig.WEB_VERSION
    )
    
    # Setup templates and static files
    templates = Jinja2Templates(directory="templates")
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    @app.get("/", response_class=HTMLResponse)
    async def home(request: Request):
        """Serve the main study planning interface"""
        return templates.TemplateResponse("index.html", {"request": request})
    
    @app.post("/api/generate", response_model=StudyPlanResponse)
    async def generate_study_plan(request: StudyPlanRequest):
        """Generate a new study plan"""
        try:
            # Validate learning style
            learning_styles = plan_generator.get_learning_styles()
            if request.learning_style not in learning_styles:
                request.learning_style = StudyConfig.DEFAULT_LEARNING_STYLE
            
            # Validate difficulty
            difficulty_levels = plan_generator.get_difficulty_levels()
            if request.difficulty not in difficulty_levels:
                request.difficulty = StudyConfig.DEFAULT_DIFFICULTY
            
            # Validate template
            templates = plan_generator.get_plan_templates()
            if request.template not in templates:
                request.template = "detailed"
            
            # Generate study plan
            plan_data = plan_generator.generate_study_plan(
                goal=request.goal,
                days_available=request.days_available,
                hours_per_day=request.hours_per_day,
                learning_style=request.learning_style,
                difficulty=request.difficulty,
                subject=request.subject,
                template=request.template
            )
            
            # Automatically save the plan in all formats so it can be downloaded later
            try:
                plan_generator.save_plan(plan_data, "json")
                plan_generator.save_plan(plan_data, "markdown")
                # PDF might fail if reportlab is not installed, so we catch that separately
                try:
                    plan_generator.save_plan(plan_data, "pdf")
                except Exception as pdf_error:
                    print(f"Warning: Could not save PDF (reportlab may not be installed): {pdf_error}")
            except Exception as e:
                print(f"Warning: Could not auto-save plan: {e}")
            
            return StudyPlanResponse(success=True, plan=plan_data)
            
        except Exception as e:
            return StudyPlanResponse(success=False, error=str(e))
    
    @app.get("/api/plans", response_model=PlansListResponse)
    async def get_plans():
        """Get list of all saved study plans"""
        try:
            plans = plan_generator.get_plan_list()
            return PlansListResponse(success=True, plans=plans, total=len(plans))
        except Exception as e:
            return PlansListResponse(success=False, error=str(e))
    
    @app.get("/api/plans/{plan_id}", response_model=StudyPlanResponse)
    async def get_plan(plan_id: str):
        """Get a specific study plan by ID"""
        try:
            plan_data = plan_generator.load_plan(plan_id)
            if not plan_data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Plan {plan_id} not found"
                )
            
            return StudyPlanResponse(success=True, plan=plan_data)
            
        except HTTPException:
            raise
        except Exception as e:
            return StudyPlanResponse(success=False, error=str(e))
    
    @app.delete("/api/plans/{plan_id}")
    async def delete_plan(plan_id: str):
        """Delete a study plan"""
        try:
            success = plan_generator.delete_plan(plan_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Plan {plan_id} not found or could not be deleted"
                )
            
            return {"success": True, "message": f"Plan {plan_id} deleted successfully"}
            
        except HTTPException:
            raise
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @app.get("/api/download/{plan_id}/{format}")
    async def download_plan(plan_id: str, format: str):
        """Download a study plan in specified format"""
        try:
            # Validate format
            export_formats = plan_generator.get_export_formats()
            if format not in export_formats:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Unsupported format: {format}"
                )
            
            # Load plan
            plan_data = plan_generator.load_plan(plan_id)
            if not plan_data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Plan {plan_id} not found"
                )
            
            # Save plan in requested format
            filepath = plan_generator.save_plan(plan_data, format)
            
            # Determine media type
            media_types = {
                "markdown": "text/markdown",
                "json": "application/json",
                "pdf": "application/pdf"
            }
            
            media_type = media_types.get(format, "application/octet-stream")
            
            return FileResponse(
                path=filepath,
                media_type=media_type,
                filename=f"study_plan_{plan_id}.{format if format != 'markdown' else 'md'}"
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error downloading plan: {str(e)}"
            )
    
    @app.get("/api/config")
    async def get_config():
        """Get application configuration"""
        try:
            config = {
                "learning_styles": plan_generator.get_learning_styles(),
                "difficulty_levels": plan_generator.get_difficulty_levels(),
                "study_subjects": plan_generator.get_study_subjects(),
                "plan_templates": plan_generator.get_plan_templates(),
                "export_formats": plan_generator.get_export_formats()
            }
            return {"success": True, "config": config}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": StudyConfig.WEB_VERSION
        }
    
    return app

def main():
    """Main entry point for web application"""
    # Check API key
    api_key = get_api_key()
    if not api_key:
        print("❌ Error: OpenAI API key not found!")
        print()
        setup_instructions()
        sys.exit(1)
    
    # Initialize plan generator
    try:
        plan_generator = StudyPlanGenerator(api_key)
        print("✅ StudyPlannerAgent initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing StudyPlannerAgent: {e}")
        sys.exit(1)
    
    # Create and run app
    app = create_app(plan_generator)
    
    print("🌐 Starting StudyPlannerAgent web interface...")
    print("📚 Open your browser to: http://127.0.0.1:8042")
    print("Press Ctrl+C to stop the server")
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8042,
        log_level="info"
    )

if __name__ == "__main__":
    main()
