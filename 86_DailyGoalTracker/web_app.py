from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from agent import DailyGoalTrackerAgent
from config import Config
from utils.llm_service import LLMService
import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

agent = DailyGoalTrackerAgent(llm_service=LLMService())


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    today_goals = agent.get_today_goals()
    return templates.TemplateResponse("index.html", {"request": request, "default_llm": Config.DEFAULT_LLM_MODEL, "today_goals": today_goals})


@app.post("/add_goal", response_class=HTMLResponse)
async def add_goal_route(request: Request, goal_input: str = Form(...), llm_choice: str = Form(Config.DEFAULT_LLM_MODEL)):
    error_message = None
    if not goal_input or goal_input.strip() == "":
        error_message = "Please enter a goal."
    else:
        try:
            agent.llm.set_llm(llm_choice)
            new_goals = agent.add_goals(goal_input)
        except Exception as e:
            error_message = str(e)

    today_goals = agent.get_today_goals()
    return templates.TemplateResponse("index.html", {"request": request, "error_message": error_message, "default_llm": Config.DEFAULT_LLM_MODEL, "selected_llm": llm_choice, "today_goals": today_goals})


@app.post("/update_goal_status", response_class=HTMLResponse)
async def update_goal_status_route(request: Request, goal_id: int = Form(...), completed: bool = Form(...), llm_choice: str = Form(Config.DEFAULT_LLM_MODEL)):
    error_message = None
    try:
        agent.llm.set_llm(llm_choice)
        agent.update_goal_status(goal_id, completed)
    except Exception as e:
        error_message = str(e)

    today_goals = agent.get_today_goals()
    return templates.TemplateResponse("index.html", {"request": request, "error_message": error_message, "default_llm": Config.DEFAULT_LLM_MODEL, "selected_llm": llm_choice, "today_goals": today_goals})


@app.post("/generate_review", response_class=HTMLResponse)
async def generate_review_route(request: Request, llm_choice: str = Form(Config.DEFAULT_LLM_MODEL)):
    error_message = None
    review_result = None
    try:
        agent.llm.set_llm(llm_choice)
        review_result = agent.generate_daily_review()
    except Exception as e:
        error_message = str(e)

    today_goals = agent.get_today_goals()
    return templates.TemplateResponse("index.html", {"request": request, "error_message": error_message, "default_llm": Config.DEFAULT_LLM_MODEL, "selected_llm": llm_choice, "today_goals": today_goals, "review_result": review_result})


@app.post("/api/add_goal", response_class=JSONResponse)
async def api_add_goal(goal_input: str = Form(...), llm_choice: str = Form(Config.DEFAULT_LLM_MODEL)):
    agent.llm.set_llm(llm_choice)
    new_goals = agent.add_goals(goal_input)
    return JSONResponse(content=new_goals)


@app.post("/api/update_goal_status", response_class=JSONResponse)
async def api_update_goal_status(goal_id: int = Form(...), completed: bool = Form(...), llm_choice: str = Form(Config.DEFAULT_LLM_MODEL)):
    agent.llm.set_llm(llm_choice)
    updated_goal = agent.update_goal_status(goal_id, completed)
    return JSONResponse(content=updated_goal)


@app.post("/api/generate_review", response_class=JSONResponse)
async def api_generate_review(llm_choice: str = Form(Config.DEFAULT_LLM_MODEL)):
    agent.llm.set_llm(llm_choice)
    review_result = agent.generate_daily_review()
    return JSONResponse(content=review_result)
