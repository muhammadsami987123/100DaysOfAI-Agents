from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from agent import APIRequesterAgent
from config import Config
from utils.llm_service import LLMService
import json
import datetime

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Register custom Jinja2 filters
def format_datetime(timestamp):
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    return dt_object.strftime("%Y-%m-%d %H:%M:%S")

templates.env.filters['format_datetime'] = format_datetime
templates.env.filters['tojson'] = json.dumps

agent = APIRequesterAgent()
llm_service = LLMService()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    history = agent.get_request_history()
    return templates.TemplateResponse("index.html", {"request": request, "default_llm": Config.DEFAULT_LLM, "history": history})

@app.post("/send_request", response_class=HTMLResponse)
async def send_request_route(
    request: Request,
    url: str = Form(...),
    method: str = Form(...),
    headers: str = Form(""),
    body: str = Form(""),
    llm_choice: str = Form(Config.DEFAULT_LLM)
):
    error_message = None
    response_data = {}
    status_code = 0
    response_time = 0
    formatted_response = {}

    try:
        parsed_headers = json.loads(headers) if headers else {}
        parsed_body = json.loads(body) if body else None
    except json.JSONDecodeError as e:
        error_message = f"Invalid JSON in Headers or Body: {e}"
        history = agent.get_request_history()
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error_message": error_message,
            "default_llm": Config.DEFAULT_LLM,
            "selected_llm": llm_choice,
            "url": url,
            "method": method,
            "headers": headers,
            "body": body,
            "history": history
        })

    try:
        response_data, status_code, response_time = agent.send_request(url, method, parsed_headers, parsed_body)
        formatted_response = agent.format_response(response_data, status_code, response_time)
    except Exception as e:
        error_message = str(e)

    history = agent.get_request_history()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "result": formatted_response,
        "default_llm": Config.DEFAULT_LLM,
        "selected_llm": llm_choice,
        "error_message": error_message,
        "url": url,
        "method": method,
        "headers": headers,
        "body": body,
        "history": history
    })

@app.post("/api/send_request", response_class=JSONResponse)
async def api_send_request(
    url: str = Form(...),
    method: str = Form(...),
    headers: str = Form(""),
    body: str = Form(""),
    llm_choice: str = Form(Config.DEFAULT_LLM)
):
    try:
        parsed_headers = json.loads(headers) if headers else {}
        parsed_body = json.loads(body) if body else None
        
        llm_service.set_llm(llm_choice)
        response_data, status_code, response_time = agent.send_request(url, method, parsed_headers, parsed_body)
        formatted_response = agent.format_response(response_data, status_code, response_time)
        return JSONResponse(content=formatted_response)
    except json.JSONDecodeError as e:
        return JSONResponse(content={
            "error": f"Invalid JSON in Headers or Body: {e}"
        }, status_code=400)
    except Exception as e:
        return JSONResponse(content={
            "error": str(e)
        }, status_code=500)
