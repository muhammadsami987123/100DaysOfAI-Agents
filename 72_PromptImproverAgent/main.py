from fastapi import FastAPI, Body
from fastapi.responses import FileResponse
import os
from agent import PromptImproverAgent

app = FastAPI()

agent = PromptImproverAgent()

@app.get('/')
def serve_frontend():
    base_dir = os.path.dirname(__file__)
    index_path = os.path.join(base_dir, 'templates', 'index.html')
    return FileResponse(index_path)

@app.post('/improve')
def improve(
    raw_prompt: str = Body(...),
    tone: str = Body(None)
):
    result = agent.improve_prompt(raw_prompt, tone)
    return result
