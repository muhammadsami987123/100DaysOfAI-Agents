from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Body
import agent

app = FastAPI()
templates = Jinja2Templates(directory="template")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate-ideas")
async def generate_ideas(request: Request, topic: str = Form(None), num_ideas: int = Form(5)):
    if not topic:
        data = await request.json()
        topic = data.get("topic", "")
        num_ideas = int(data.get("num_ideas", 5))
    ideas = agent.generate_ideas(topic, num_ideas=num_ideas)
    return JSONResponse(content={"ideas": ideas})
