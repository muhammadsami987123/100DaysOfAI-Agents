from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from agent import DreamInterpreterAgent
from config import Config
from utils.llm_service import LLMService

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

agent = DreamInterpreterAgent(llm_service=LLMService())


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "default_llm": Config.DEFAULT_LLM})


@app.post("/interpret", response_class=HTMLResponse)
async def interpret_route(request: Request, dream_text: str = Form(...), llm_choice: str = Form(Config.DEFAULT_LLM)):
    error_message = None
    if not dream_text or dream_text.strip() == "":
        error_message = "Please provide a dream description."
        return templates.TemplateResponse("index.html", {"request": request, "error_message": error_message, "default_llm": Config.DEFAULT_LLM})

    try:
        agent.llm.set_llm(llm_choice)
        result = agent.interpret(dream_text)
    except Exception as e:
        result = {"interpretation": "", "symbols": [], "message": "Error: " + str(e)}
        error_message = str(e)

    return templates.TemplateResponse("index.html", {"request": request, "result": result, "default_llm": Config.DEFAULT_LLM, "selected_llm": llm_choice, "error_message": error_message})


@app.post("/api/interpret", response_class=JSONResponse)
async def api_interpret(dream_text: str = Form(...), llm_choice: str = Form(Config.DEFAULT_LLM)):
    agent.llm.set_llm(llm_choice)
    result = agent.interpret(dream_text)
    return JSONResponse(content=result)
