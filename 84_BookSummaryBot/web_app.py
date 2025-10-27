from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from agent import BookSummaryAgent
from config import Config
from utils.llm_service import LLMService
import os
import shutil
from PyPDF2 import PdfReader
import aiofiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

book_summary_agent = BookSummaryAgent(llm_service=LLMService())

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "default_llm": Config.DEFAULT_LLM}
    )

@app.post("/summarize", response_class=HTMLResponse)
async def summarize_chapter_route(
    request: Request,
    chapter_text: str = Form(None),
    file: UploadFile = File(None),
    chapter_url: str = Form(None),
    llm_choice: str = Form(Config.DEFAULT_LLM),
):
    content_to_summarize = ""
    error_message = None

    if file and file.filename:
        try:
            file_extension = file.filename.split(".").pop().lower()
            if file_extension not in ["txt", "pdf"]:
                raise HTTPException(status_code=400, detail="Unsupported file type. Only .txt and .pdf are allowed.")

            upload_path = os.path.join(Config.UPLOAD_DIR, file.filename)
            async with aiofiles.open(upload_path, "wb") as out_file:
                while content := await file.read(1024):
                    await out_file.write(content)

            if file_extension == "txt":
                async with aiofiles.open(upload_path, "r", encoding="utf-8") as f:
                    content_to_summarize = await f.read()
            elif file_extension == "pdf":
                with open(upload_path, "rb") as f:
                    reader = PdfReader(f)
                    for page in reader.pages:
                        content_to_summarize += page.extract_text() or ""

            os.remove(upload_path) # Clean up the uploaded file

        except Exception as e:
            error_message = f"Error processing file: {str(e)}"
            print(f"File processing error: {e}")

    elif chapter_text:
        content_to_summarize = chapter_text

    elif chapter_url:
        try:
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.get(chapter_url)
                response.raise_for_status() # Raise an exception for HTTP errors
                content_to_summarize = response.text
        except httpx.HTTPStatusError as e:
            error_message = f"HTTP error fetching URL: {e.response.status_code} - {e.response.text}"
        except httpx.RequestError as e:
            error_message = f"Error fetching URL: {e}"

    if not content_to_summarize and not error_message:
        error_message = "No content provided for summarization. Please paste text, upload a file, or provide a URL."

    summary_output = {"summary": "", "key_points": []}
    if content_to_summarize and not error_message:
        try:
            print(f"Attempting to summarize content with LLM: {llm_choice}")
            # Temporarily set the LLM for this request
            book_summary_agent.llm_service.set_llm(llm_choice)
            
            print("Calling summarize_chapter...")
            summary_output = book_summary_agent.summarize_chapter(content_to_summarize)
            print(f"Received summary_output: {summary_output}")
            
            # Validate the response structure
            if not isinstance(summary_output, dict):
                print(f"Warning: summary_output is not a dict: {type(summary_output)}")
                summary_output = {"summary": str(summary_output), "key_points": []}
            if "summary" not in summary_output:
                print("Warning: summary key missing from response")
                summary_output["summary"] = "No summary generated"
            if "key_points" not in summary_output:
                print("Warning: key_points key missing from response")
                summary_output["key_points"] = []
                
            print(f"Final summary_output: {summary_output}")
                
        except Exception as e:
            error_message = f"Error generating summary: {str(e)}"
            print(f"Summary generation error: {e}")
            import traceback
            traceback.print_exc()
            summary_output = {"summary": "", "key_points": []}

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "summary_output": summary_output,
            "error_message": error_message,
            "default_llm": Config.DEFAULT_LLM,
            "selected_llm": llm_choice,
        },
    )
