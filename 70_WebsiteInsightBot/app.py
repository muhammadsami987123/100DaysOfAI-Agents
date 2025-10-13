from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
sys.path.append(os.path.dirname(__file__))
from agent import website_insight_bot
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()
    url = data.get("url")
    long_form = data.get("long_form", False)
    result = website_insight_bot(url, long_form=long_form)
    return JSONResponse(content=result)

@app.get("/")
async def serve_index():
    index_path = os.path.join(os.path.dirname(__file__), "template", "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(content=html)
