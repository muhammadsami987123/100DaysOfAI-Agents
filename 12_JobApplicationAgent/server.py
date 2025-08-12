"""
FastAPI server for JobApplicationAgent
"""

import os
import logging
import tempfile
from typing import Optional
from pathlib import Path

from fastapi import FastAPI, File, Form, UploadFile, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from config import (
    PORT, HOST, DEBUG, MAX_FILE_SIZE, ALLOWED_EXTENSIONS,
    SUPPORTED_LANGUAGES, COVER_LETTER_LENGTHS, ADDITIONAL_DOCUMENTS, ERROR_MESSAGES,
    SUCCESS_MESSAGES, TEMPLATE_DIR, STATIC_DIR, UPLOAD_DIR
)
from job_agent import JobApplicationAgent
from document_generator import DocumentGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="JobApplicationAgent",
    description="AI-powered job application generator",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
try:
    job_agent = JobApplicationAgent()
    document_generator = DocumentGenerator()
    logger.info("JobApplicationAgent initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize JobApplicationAgent: {e}")
    job_agent = None
    document_generator = None

# Setup static files and templates
BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE_DIR / TEMPLATE_DIR))

# Mount static files
static_dir = BASE_DIR / STATIC_DIR
if not static_dir.exists():
    static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Create upload directory
upload_dir = BASE_DIR / UPLOAD_DIR
upload_dir.mkdir(exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    """Main web interface"""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "languages": SUPPORTED_LANGUAGES,
            "cover_letter_lengths": COVER_LETTER_LENGTHS,
        },
    )


@app.post("/api/generate-application")
async def generate_application(
    resume_file: UploadFile = File(...),
    job_description: str = Form(...),
    language: str = Form(default="en"),
    cover_letter_length: str = Form(default="medium"),
    additional_documents: str = Form(default="")
):
    """Generate complete job application package"""
    try:
        # Validate inputs
        if not job_agent:
            raise HTTPException(status_code=500, detail="Job agent not initialized")
        
        if not resume_file:
            raise HTTPException(status_code=400, detail=ERROR_MESSAGES["missing_resume"])
        
        if not job_description or len(job_description.strip()) < 50:
            raise HTTPException(status_code=400, detail=ERROR_MESSAGES["missing_job_description"])
        
        # Validate file
        file_extension = Path(resume_file.filename).suffix.lower()
        if file_extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail=ERROR_MESSAGES["invalid_file"])
        
        if resume_file.size > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail=ERROR_MESSAGES["file_too_large"])
        
        # Validate language
        if language not in SUPPORTED_LANGUAGES:
            raise HTTPException(status_code=400, detail=ERROR_MESSAGES["invalid_language"])
        
        # Parse additional documents
        additional_docs = []
        if additional_documents:
            additional_docs = [doc.strip() for doc in additional_documents.split(',') if doc.strip()]
            # Validate additional document types
            for doc_type in additional_docs:
                if doc_type not in ADDITIONAL_DOCUMENTS:
                    raise HTTPException(status_code=400, detail=f"Invalid document type: {doc_type}")
        
        # Save uploaded file temporarily
        temp_file_path = None
        try:
            # Create temporary file
            temp_fd, temp_file_path = tempfile.mkstemp(suffix=file_extension)
            os.close(temp_fd)
            
            # Save uploaded file
            with open(temp_file_path, "wb") as buffer:
                content = await resume_file.read()
                buffer.write(content)
            
            # Generate application
            result = job_agent.generate_application(
                resume_file_path=temp_file_path,
                job_description=job_description,
                language=language,
                cover_letter_length=cover_letter_length,
                additional_documents=additional_docs if additional_docs else None
            )
            
            if not result["success"]:
                raise HTTPException(status_code=500, detail=result["error"])
            
            return JSONResponse(content=result)
            
        finally:
            # Clean up temporary file
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Application generation failed: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["generation_failed"])


@app.post("/api/extract-job-from-url")
async def extract_job_from_url(url: str = Form(...)):
    """Extract job description from URL"""
    try:
        if not job_agent:
            raise HTTPException(status_code=500, detail="Job agent not initialized")
        
        if not url or not url.strip():
            raise HTTPException(status_code=400, detail="URL is required")
        
        result = job_agent.extract_job_from_url(url.strip())
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return JSONResponse(content=result)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"URL extraction failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to extract job description from URL")


@app.post("/api/analyze-resume")
async def analyze_resume(resume_file: UploadFile = File(...)):
    """Analyze resume only"""
    try:
        if not job_agent:
            raise HTTPException(status_code=500, detail="Job agent not initialized")
        
        if not resume_file:
            raise HTTPException(status_code=400, detail=ERROR_MESSAGES["missing_resume"])
        
        # Validate file
        file_extension = Path(resume_file.filename).suffix.lower()
        if file_extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail=ERROR_MESSAGES["invalid_file"])
        
        if resume_file.size > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail=ERROR_MESSAGES["file_too_large"])
        
        # Save uploaded file temporarily
        temp_file_path = None
        try:
            temp_fd, temp_file_path = tempfile.mkstemp(suffix=file_extension)
            os.close(temp_fd)
            
            with open(temp_file_path, "wb") as buffer:
                content = await resume_file.read()
                buffer.write(content)
            
            result = job_agent.analyze_resume_only(temp_file_path)
            
            if not result["success"]:
                raise HTTPException(status_code=500, detail=result["error"])
            
            return JSONResponse(content=result)
            
        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Resume analysis failed: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["processing_failed"])


@app.post("/api/analyze-job")
async def analyze_job(job_description: str = Form(...)):
    """Analyze job description only"""
    try:
        if not job_agent:
            raise HTTPException(status_code=500, detail="Job agent not initialized")
        
        if not job_description or len(job_description.strip()) < 50:
            raise HTTPException(status_code=400, detail=ERROR_MESSAGES["missing_job_description"])
        
        result = job_agent.analyze_job_only(job_description)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return JSONResponse(content=result)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Job analysis failed: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["processing_failed"])


@app.post("/api/download/resume/{format}")
async def download_resume(
    format: str,
    content: str = Form(...)
):
    """Download resume in specified format"""
    try:
        if not document_generator:
            raise HTTPException(status_code=500, detail="Document generator not initialized")
        
        if format not in ["pdf", "docx"]:
            raise HTTPException(status_code=400, detail="Unsupported format")
        
        # Generate document
        document_bytes = document_generator.generate_resume_document(content, format)
        
        # Set filename
        filename = f"customized_resume.{format}"
        
        # Return file
        import io
        return StreamingResponse(
            io.BytesIO(document_bytes),
            media_type=f"application/{format}",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    
    except Exception as e:
        logger.error(f"Resume download failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate document")


@app.post("/api/download/cover-letter/{format}")
async def download_cover_letter(
    format: str,
    content: str = Form(...)
):
    """Download cover letter in specified format"""
    try:
        if not document_generator:
            raise HTTPException(status_code=500, detail="Document generator not initialized")
        
        if format not in ["pdf", "docx"]:
            raise HTTPException(status_code=400, detail="Unsupported format")
        
        # Generate document
        document_bytes = document_generator.generate_cover_letter_document(content, format)
        
        # Set filename
        filename = f"cover_letter.{format}"
        
        # Return file
        import io
        return StreamingResponse(
            io.BytesIO(document_bytes),
            media_type=f"application/{format}",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    
    except Exception as e:
        logger.error(f"Cover letter download failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate document")


@app.post("/api/download/additional-document/{doc_type}/{format}")
async def download_additional_document(
    doc_type: str,
    format: str,
    content: str = Form(...)
):
    """Download additional document in specified format"""
    try:
        if not document_generator:
            raise HTTPException(status_code=500, detail="Document generator not initialized")
        
        if format not in ["pdf", "docx"]:
            raise HTTPException(status_code=400, detail="Unsupported format")
        
        if doc_type not in ADDITIONAL_DOCUMENTS:
            raise HTTPException(status_code=400, detail="Unsupported document type")
        
        # Generate document
        document_bytes = document_generator.generate_additional_document(content, doc_type, format)
        
        # Set filename
        doc_names = {
            "personal_statement": "personal_statement",
            "reference_page": "reference_page",
            "thank_you_note": "thank_you_note",
            "motivation_letter": "motivation_letter",
            "linkedin_bio": "linkedin_bio"
        }
        filename = f"{doc_names.get(doc_type, doc_type)}.{format}"
        
        # Return file
        import io
        return StreamingResponse(
            io.BytesIO(document_bytes),
            media_type=f"application/{format}",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    
    except Exception as e:
        logger.error(f"Additional document download failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate document")


@app.get("/api/languages")
async def get_languages():
    """Get supported languages"""
    return JSONResponse(content={"languages": SUPPORTED_LANGUAGES})


@app.get("/api/cover-letter-lengths")
async def get_cover_letter_lengths():
    """Get cover letter length options"""
    return JSONResponse(content={"lengths": COVER_LETTER_LENGTHS})


@app.get("/api/additional-documents")
async def get_additional_documents():
    """Get additional document types"""
    return JSONResponse(content={"documents": ADDITIONAL_DOCUMENTS})


@app.get("/api/supported-job-sites")
async def get_supported_job_sites():
    """Get supported job sites for URL extraction"""
    if not job_agent:
        raise HTTPException(status_code=500, detail="Job agent not initialized")
    
    return JSONResponse(content={"sites": job_agent.get_supported_job_sites()})


@app.get("/api/formats")
async def get_supported_formats():
    """Get supported document formats"""
    if not document_generator:
        raise HTTPException(status_code=500, detail="Document generator not initialized")
    
    return JSONResponse(content={"formats": document_generator.get_supported_formats()})


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(content={
        "status": "healthy",
        "job_agent": job_agent is not None,
        "document_generator": document_generator is not None
    })


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting JobApplicationAgent server on {HOST}:{PORT}")
    uvicorn.run(
        "server:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
        log_level="info"
    )
