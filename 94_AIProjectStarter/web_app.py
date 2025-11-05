from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from agent import AIProjectStarterAgent
from config import Config
from utils.llm_service import LLMService
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

agent = AIProjectStarterAgent(llm_service=LLMService())


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "default_llm": Config.DEFAULT_LLM,
            "default_output_dir": Config.DEFAULT_OUTPUT_DIR
        }
    )


@app.post("/scaffold", response_class=HTMLResponse)
async def scaffold_route(
    request: Request,
    project_name: str = Form(...),
    project_type: str = Form(...),
    llm_preference: str = Form("gemini"),
    features: str = Form(""),
    output_dir: str = Form(""),
    llm_choice: str = Form(Config.DEFAULT_LLM),
):
    error_message = None
    result = None
    
    try:
        agent.llm_service.set_llm(llm_choice)
        
        # Parse features from comma-separated string
        features_list = [f.strip() for f in features.split(",") if f.strip()] if features else []
        
        # Use Downloads folder as default if output_dir is empty
        final_output_dir = output_dir.strip() if output_dir and output_dir.strip() else None
        
        # Scaffold the project
        result = agent.scaffold_project(
            project_name=project_name,
            project_type=project_type,
            llm_preference=llm_preference,
            features=features_list,
            output_dir=final_output_dir
        )
        
        if not result.get("success"):
            error_message = result.get("error", "Unknown error occurred")
            
    except Exception as e:
        error_message = str(e)
        result = {"success": False, "error": str(e)}

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": result,
            "error_message": error_message,
            "default_llm": Config.DEFAULT_LLM,
            "selected_llm": llm_choice,
            "default_output_dir": Config.DEFAULT_OUTPUT_DIR,
        },
    )


@app.post("/preview", response_class=HTMLResponse)
async def preview_route(
    request: Request,
    project_name: str = Form(...),
    project_type: str = Form(...),
    llm_preference: str = Form("gemini"),
    features: str = Form(""),
    llm_choice: str = Form(Config.DEFAULT_LLM),
):
    """Preview project structure without creating files."""
    error_message = None
    preview_data = None
    
    try:
        agent.llm_service.set_llm(llm_choice)
        
        # Parse features from comma-separated string
        features_list = [f.strip() for f in features.split(",") if f.strip()] if features else []
        
        # Generate project structure preview
        preview_data = agent.generate_project_structure(
            project_name=project_name,
            project_type=project_type,
            llm_preference=llm_preference,
            features=features_list
        )
            
    except Exception as e:
        error_message = str(e)
        preview_data = None

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "preview_data": preview_data,
            "error_message": error_message,
            "default_llm": Config.DEFAULT_LLM,
            "selected_llm": llm_choice,
            "default_output_dir": Config.DEFAULT_OUTPUT_DIR,
            "form_data": {
                "project_name": project_name,
                "project_type": project_type,
                "llm_preference": llm_preference,
                "features": features,
            }
        },
    )

