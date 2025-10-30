
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp, Receive, Scope, Send
from agent import GitHubRepoAnalyzer

class CacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if request.url.path.startswith("/static"):
            response.headers["Cache-Control"] = "public, max-age=31536000"
        return response
from utils.llm_service import LLMService
from config import Config

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Gzip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Add caching headers for static files
app.add_middleware(CacheMiddleware)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

llm_service = LLMService()
agent = GitHubRepoAnalyzer(llm_service=llm_service)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "default_llm": Config.DEFAULT_LLM_MODEL,
            "selected_llm": Config.DEFAULT_LLM_MODEL,
            "summary": None,
            "repo_url": ""
        }
    )

@app.post("/analyze", response_class=HTMLResponse)
async def analyze_repo_route(request: Request, repo_url: str = Form(...), llm_choice: str = Form(Config.DEFAULT_LLM_MODEL)):
    error_message = None
    summary = None
    try:
        llm_service.set_llm(llm_choice)
        summary = await agent.analyze_repo(repo_url, llm_choice)
    except Exception as e:
        error_message = str(e)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "default_llm": Config.DEFAULT_LLM_MODEL,
            "selected_llm": llm_choice,
            "summary": summary,
            "repo_url": repo_url,
            "error_message": error_message
        }
    )
