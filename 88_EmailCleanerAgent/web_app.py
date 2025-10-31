from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from agent import EmailCleanerAgent
from utils.llm_service import LLMService
from config import Config

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

llm_service = LLMService(api_key=Config.GOOGLE_API_KEY, provider="gemini")
agent = EmailCleanerAgent(llm_service)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/scan", response_class=HTMLResponse)
async def scan_inbox(request: Request):
    emails = agent.fetch_emails()
    classified_emails = agent.analyze_and_classify_emails(emails)
    return templates.TemplateResponse("index.html", {"request": request, "emails": classified_emails})

@app.post("/action", response_class=HTMLResponse)
async def take_action(request: Request, email_id: str = Form(...), action: str = Form(...)):
    if action == "delete":
        agent.delete_email(email_id)
    elif action == "archive":
        agent.archive_email(email_id)
    
    emails = agent.fetch_emails()
    classified_emails = agent.analyze_and_classify_emails(emails)
    return templates.TemplateResponse("index.html", {"request": request, "emails": classified_emails, "message": f"Email {action}d successfully."})
