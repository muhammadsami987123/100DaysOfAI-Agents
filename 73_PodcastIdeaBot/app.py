from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from agent import generate_multiple_ideas, generate_episode_script


app = FastAPI()
templates = Jinja2Templates(directory="template")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
	return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate")
async def generate(request: Request, topic: str = Form(None), guest_type: str = Form(None), count: int = Form(1)):
	if not topic:
		data = await request.json()
		topic = (data.get("topic") or "").strip()
		guest_type = (data.get("guest_type") or "").strip()
		count = int(data.get("count") or 1)
	try:
		ideas = generate_multiple_ideas(topic, guest_type, count)
	except Exception as exc:
		return JSONResponse(content={"error": str(exc)}, status_code=400)
	return JSONResponse(content={"ideas": ideas})


@app.post("/generate_script")
async def generate_script(request: Request):
    data = await request.json()
    idea = data.get("idea")
    if not idea or not isinstance(idea, dict):
        return JSONResponse(content={"error": "No valid idea data provided."}, status_code=400)
    try:
        script = generate_episode_script(idea)
    except Exception as exc:
        return JSONResponse(content={"error": str(exc)}, status_code=400)
    return JSONResponse(content={"script": script})


