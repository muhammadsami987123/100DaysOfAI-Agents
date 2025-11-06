from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from agent import CustomPromptAgent
from config import Config
from utils.llm_service import LLMService

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

agent = CustomPromptAgent(llm_service=LLMService())


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    saved_templates = agent.list_templates()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "default_llm": Config.DEFAULT_LLM,
            "selected_llm": Config.DEFAULT_LLM,
            "saved_templates": saved_templates
        }
    )


@app.post("/build", response_class=HTMLResponse)
async def build_prompt_route(
    request: Request,
    role: str = Form(""),
    task: str = Form(""),
    output_format: str = Form(""),
    tone: str = Form(""),
    target_audience: str = Form(""),
    additional_context: str = Form(""),
    llm_choice: str = Form(Config.DEFAULT_LLM),
):
    """Build a prompt from form inputs."""
    error_message = None
    result = None
    
    try:
        agent.llm_service.set_llm(llm_choice)
        result = agent.build_prompt(
            role=role,
            task=task,
            output_format=output_format,
            tone=tone,
            target_audience=target_audience,
            additional_context=additional_context
        )
    except Exception as e:
        error_message = str(e)
        result = {"prompt": "", "metadata": {}}

    saved_templates = agent.list_templates()
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": result,
            "error_message": error_message,
            "default_llm": Config.DEFAULT_LLM,
            "selected_llm": llm_choice,
            "saved_templates": saved_templates,
            "form_data": {
                "role": role,
                "task": task,
                "output_format": output_format,
                "tone": tone,
                "target_audience": target_audience,
                "additional_context": additional_context
            }
        },
    )


@app.post("/api/build_prompt", response_class=JSONResponse)
async def api_build_prompt(
    role: str = Form(""),
    task: str = Form(""),
    output_format: str = Form(""),
    tone: str = Form(""),
    target_audience: str = Form(""),
    additional_context: str = Form(""),
):
    """API endpoint to build a prompt without rendering the template."""
    try:
        result = agent.build_prompt(
            role=role,
            task=task,
            output_format=output_format,
            tone=tone,
            target_audience=target_audience,
            additional_context=additional_context,
        )
        return JSONResponse(content={"success": True, "data": result})
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


@app.post("/save_template", response_class=JSONResponse)
async def save_template_route(
    template_name: str = Form(...),
    role: str = Form(""),
    task: str = Form(""),
    output_format: str = Form(""),
    tone: str = Form(""),
    target_audience: str = Form(""),
    additional_context: str = Form(""),
):
    """Save a prompt template."""
    try:
        prompt_data = agent.build_prompt(
            role=role,
            task=task,
            output_format=output_format,
            tone=tone,
            target_audience=target_audience,
            additional_context=additional_context
        )
        result = agent.save_template(template_name, prompt_data)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": str(e)},
            status_code=500
        )


@app.post("/load_template", response_class=JSONResponse)
async def load_template_route(template_name: str = Form(...)):
    """Load a saved template."""
    result = agent.load_template(template_name)
    return JSONResponse(content=result)


@app.post("/delete_template", response_class=JSONResponse)
async def delete_template_route(template_name: str = Form(...)):
    """Delete a saved template."""
    result = agent.delete_template(template_name)
    return JSONResponse(content=result)


@app.get("/api/templates", response_class=JSONResponse)
async def list_templates_api():
    """API endpoint to list all templates."""
    templates = agent.list_templates()
    return JSONResponse(content={"templates": templates})


@app.post("/enhance", response_class=JSONResponse)
async def enhance_prompt_route(
    prompt: str = Form(...),
    enhancement_type: str = Form("general"),
    llm_choice: str = Form(Config.DEFAULT_LLM),
):
    """Enhance a prompt using LLM."""
    try:
        if not prompt or not prompt.strip():
            return JSONResponse(
                content={"success": False, "error": "Prompt cannot be empty"},
                status_code=400
            )
        
        agent.llm_service.set_llm(llm_choice)
        result = agent.enhance_prompt(prompt, enhancement_type)
        
        # Ensure success flag is set
        if "success" not in result:
            result["success"] = True
        
        return JSONResponse(content=result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            content={
                "success": False, 
                "error": str(e),
                "enhanced_prompt": prompt  # Return original prompt on error
            },
            status_code=500
        )

