import os
from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from agent import VideoChapterAgent
from config import UPLOAD_DIR

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Jinja2Templates
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def startup_event():
    os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload-video/")
async def upload_video(request: Request, video_file: UploadFile = File(...), llm_model: str = Form("gemini")):
    video_filename = video_file.filename
    file_path = os.path.join(UPLOAD_DIR, video_filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await video_file.read())

    llm_model = "gemini"
    agent = VideoChapterAgent(llm_model)
    result = agent.process_video(file_path, llm_model)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "video_filename": video_filename,
        "transcript": result["transcript"],
        "chapters": result["chapters"],
        "selected_llm": llm_model
    })

@app.get("/video/{filename}")
async def serve_video(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="video/mp4")
    return {"error": "File not found"}
