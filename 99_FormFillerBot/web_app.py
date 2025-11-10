from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from agent import FormFillerBot
from config import Config
from utils.llm_service import LLMService
import os
import json

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

form_filler_bot = FormFillerBot(llm_service=LLMService())


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    user_data = form_filler_bot.get_user_data()
    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "default_llm": Config.DEFAULT_LLM,
            "user_data": user_data
        }
    )


@app.post("/api/user-data", response_class=JSONResponse)
async def get_user_data():
    """Get user data as JSON."""
    try:
        data = form_filler_bot.get_user_data()
        return {"success": True, "data": data}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post("/api/update-data", response_class=JSONResponse)
async def update_user_data(
    request: Request,
    data_updates: str = Form(...),
    llm_choice: str = Form(Config.DEFAULT_LLM),
):
    """Update user data."""
    try:
        form_filler_bot.llm_service.set_llm(llm_choice)
        updates = json.loads(data_updates)
        result = form_filler_bot.update_user_data(updates)
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post("/api/analyze-form", response_class=JSONResponse)
async def analyze_form(
    request: Request,
    form_fields: str = Form(...),
    form_html: str = Form(""),
    llm_choice: str = Form(Config.DEFAULT_LLM),
):
    """Analyze form fields and get fill suggestions."""
    try:
        form_filler_bot.llm_service.set_llm(llm_choice)
        fields_list = json.loads(form_fields)
        result = form_filler_bot.get_fill_suggestions(fields_list, form_html)
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}


@app.post("/manage-data", response_class=HTMLResponse)
async def manage_data_route(
    request: Request,
    llm_choice: str = Form(Config.DEFAULT_LLM),
):
    """Update user data via form submission."""
    error_message = None
    success_message = None
    
    try:
        form_filler_bot.llm_service.set_llm(llm_choice)
        
        # Build updates dictionary from form fields
        # Use Request form() to get all form data
        form_data = await request.form()
        
        updates = {}
        
        # Personal info - check if any personal info fields are in the form
        personal_info = {}
        personal_fields = ['first_name', 'last_name', 'full_name', 'email', 'phone', 
                          'date_of_birth', 'address', 'city', 'state', 'zip_code', 'country']
        for field in personal_fields:
            if field in form_data:
                personal_info[field] = form_data[field] or ""
        if personal_info: updates["personal_info"] = personal_info
        
        # Professional info
        professional = {}
        professional_fields = ['job_title', 'company', 'linkedin', 'github', 'portfolio']
        for field in professional_fields:
            if field in form_data:
                professional[field] = form_data[field] or ""
        if professional: updates["professional"] = professional
        
        # Education
        education = {}
        education_fields = ['degree', 'university', 'graduation_year']
        for field in education_fields:
            if field in form_data:
                education[field] = form_data[field] or ""
        if education: updates["education"] = education
        
        if updates:
            result = form_filler_bot.update_user_data(updates)
            if result.get("success"):
                success_message = "Data updated successfully!"
            else:
                error_message = result.get("error", "Failed to update data")
        else:
            error_message = "No data provided to update"
    except Exception as e:
        error_message = str(e)
        import traceback
        traceback.print_exc()
    
    user_data = form_filler_bot.get_user_data()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "user_data": user_data,
            "error_message": error_message,
            "success_message": success_message,
            "default_llm": Config.DEFAULT_LLM,
            "selected_llm": llm_choice,
        },
    )


@app.post("/analyze", response_class=HTMLResponse)
async def analyze_form_route(
    request: Request,
    form_fields: str = Form(...),
    form_html: str = Form(""),
    llm_choice: str = Form(Config.DEFAULT_LLM),
):
    """Analyze form and return fill suggestions."""
    error_message = None
    analysis_result = None
    
    try:
        form_filler_bot.llm_service.set_llm(llm_choice)
        fields_list = json.loads(form_fields)
        analysis_result = form_filler_bot.get_fill_suggestions(fields_list, form_html)
        
        if "error" in analysis_result:
            error_message = analysis_result["error"]
    except Exception as e:
        error_message = str(e)
        import traceback
        traceback.print_exc()
    
    user_data = form_filler_bot.get_user_data()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "user_data": user_data,
            "analysis_result": analysis_result,
            "error_message": error_message,
            "default_llm": Config.DEFAULT_LLM,
            "selected_llm": llm_choice,
        },
    )

