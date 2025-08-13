from __future__ import annotations

import os
import json
from typing import Optional
from datetime import datetime

from fastapi import FastAPI, Form, File, UploadFile, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import (
    PORT, HOST, MAX_FILE_SIZE, UPLOAD_DIR, OUTPUT_DIR,
    SUPPORTED_LANGUAGES, UI_LANGUAGES, validate_config,
    get_language_from_extension, get_language_from_content, ERROR_MESSAGES, SUCCESS_MESSAGES
)
from code_review_service import CodeReviewService, CodeReviewError
from github_service import GitHubService


# Initialize FastAPI app
app = FastAPI(
    title="CodeReviewerBot",
    description="AI-powered code review agent for developers",
    version="1.0.0"
)

# Setup directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
static_dir = os.path.join(BASE_DIR, "static")
upload_dir = os.path.join(BASE_DIR, UPLOAD_DIR)
output_dir = os.path.join(BASE_DIR, OUTPUT_DIR)

# Create directories if they don't exist
for directory in [static_dir, upload_dir, output_dir]:
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Initialize services
try:
    code_review_service = CodeReviewService()
    github_service = GitHubService()
    print("✅ Services initialized successfully")
    print(f"🤖 Using OpenAI model: {code_review_service.model}")
    if code_review_service.supports_json:
        print("✅ Model supports structured JSON responses")
    else:
        print("⚠️  Model doesn't support structured JSON responses - using fallback parsing")
except Exception as e:
    print(f"❌ Failed to initialize services: {e}")
    print("   Please check your .env file and ensure OPENAI_API_KEY is set correctly")
    code_review_service = None
    github_service = None


@app.on_event("startup")
async def startup_event():
    """Validate configuration on startup."""
    errors = validate_config()
    if errors:
        print("Configuration errors:")
        for error in errors:
            print(f"  - {error}")
        print("Please fix these errors before starting the server.")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    """Serve the main web interface."""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "supported_languages": SUPPORTED_LANGUAGES,
            "ui_languages": UI_LANGUAGES,
        },
    )


@app.post("/api/review")
async def review_code(
    code: Optional[str] = Form(default=None),
    language: Optional[str] = Form(default=None),
    ui_language: str = Form(default="english"),
    file: Optional[UploadFile] = File(default=None),
    github_url: Optional[str] = Form(default=None),
) -> JSONResponse:
    """
    Main endpoint for code review.
    
    Accepts code through:
    - Direct text input
    - File upload
    - GitHub URL
    """
    try:
        print(f"🔍 Review request received:")
        print(f"   Code provided: {bool(code and code.strip())}")
        print(f"   File provided: {bool(file and file.filename)}")
        print(f"   GitHub URL provided: {bool(github_url and github_url.strip())}")
        print(f"   Language: {language}")
        print(f"   UI Language: {ui_language}")
        
        # Validate input
        input_methods = sum([
            1 if code and code.strip() else 0,
            1 if file and file.filename else 0,
            1 if github_url and github_url.strip() else 0
        ])
        
        if input_methods == 0:
            raise HTTPException(status_code=400, detail=ERROR_MESSAGES["empty_code"])
        
        if input_methods > 1:
            raise HTTPException(status_code=400, detail="Please provide code through only one method (text, file, or GitHub URL)")
        
        # Resolve input code
        input_code, detected_language, filename = await _resolve_input(
            code=code, file=file, github_url=github_url
        )
        
        if not input_code:
            raise HTTPException(status_code=400, detail=ERROR_MESSAGES["empty_code"])
        
        # Use provided language or detected language
        review_language = language or detected_language
        
        if review_language not in SUPPORTED_LANGUAGES:
            raise HTTPException(status_code=400, detail=ERROR_MESSAGES["unsupported_language"])
        
        # Check if service is available
        if not code_review_service:
            raise HTTPException(
                status_code=503, 
                detail="Code review service is not available. Please check your OpenAI API key configuration."
            )
        
        # Perform code review
        review_result = code_review_service.review_code(
            code=input_code,
            language=review_language,
            ui_language=ui_language
        )
        
        # Generate code summary
        code_summary = code_review_service.generate_code_summary(input_code, review_language)
        
        # Prepare response
        response_data = {
            "success": True,
            "message": SUCCESS_MESSAGES["analysis_complete"],
            "data": {
                "language": review_result.language,
                "filename": filename,
                "issues": [
                    {
                        "category": issue.category,
                        "severity": issue.severity,
                        "line_number": issue.line_number,
                        "message": issue.message,
                        "suggestion": issue.suggestion,
                        "code_snippet": issue.code_snippet
                    }
                    for issue in review_result.issues
                ],
                "suggestions": review_result.suggestions,
                "refactored_code": review_result.refactored_code,
                "scores": review_result.scores,
                "summary": review_result.summary,
                "statistics": {
                    "total_issues": review_result.total_issues,
                    "critical_issues": review_result.critical_issues,
                    "code_summary": code_summary
                },
                "timestamp": datetime.now().isoformat()
            }
        }
        
        return JSONResponse(content=response_data)
        
    except CodeReviewError as e:
        return JSONResponse(
            content={"success": False, "error": str(e)},
            status_code=400
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error in review_code: {e}")
        return JSONResponse(
            content={"success": False, "error": ERROR_MESSAGES["code_analysis_failed"]},
            status_code=500
        )


@app.post("/api/validate-github")
async def validate_github_url(github_url: str = Form(...)) -> JSONResponse:
    """Validate GitHub URL and return repository information."""
    try:
        if not github_service.validate_github_url(github_url):
            return JSONResponse(
                content={"valid": False, "error": "Invalid GitHub URL format"},
                status_code=400
            )
        
        github_info = github_service.extract_github_info(github_url)
        if not github_info:
            return JSONResponse(
                content={"valid": False, "error": "Could not parse GitHub URL"},
                status_code=400
            )
        
        # Check if repository is public
        if github_info['type'] == 'repo':
            is_public = github_service.is_public_repository(
                github_info['owner'], github_info['repo']
            )
            if not is_public:
                return JSONResponse(
                    content={"valid": False, "error": "Repository must be public"},
                    status_code=400
                )
        
        return JSONResponse(content={
            "valid": True,
            "github_info": github_info
        })
        
    except Exception as e:
        return JSONResponse(
            content={"valid": False, "error": str(e)},
            status_code=500
        )


@app.get("/api/languages")
async def get_supported_languages() -> JSONResponse:
    """Get list of supported programming languages."""
    return JSONResponse(content={
        "languages": SUPPORTED_LANGUAGES,
        "ui_languages": UI_LANGUAGES
    })


@app.get("/api/health")
async def health_check() -> JSONResponse:
    """Health check endpoint."""
    return JSONResponse(content={
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "code_review": code_review_service is not None,
            "github": github_service is not None
        }
    })


async def _resolve_input(
    code: Optional[str],
    file: Optional[UploadFile],
    github_url: Optional[str]
) -> tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Resolve input code from various sources.
    
    Returns:
        Tuple of (code_content, detected_language, filename)
    """
    # Direct text input
    if code and code.strip():
        detected_language = get_language_from_content(code.strip())
        return code.strip(), detected_language, None
    
    # File upload
    if file and file.filename:
        # Validate file size
        if file.size and file.size > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail=ERROR_MESSAGES["file_too_large"])
        
        # Validate file extension
        detected_language = get_language_from_extension(file.filename)
        if detected_language == "unknown":
            raise HTTPException(status_code=400, detail=ERROR_MESSAGES["invalid_file"])
        
        # Read file content
        content = await file.read()
        try:
            code_content = content.decode("utf-8")
        except UnicodeDecodeError:
            code_content = content.decode("latin-1", errors="ignore")
        
        return code_content, detected_language, file.filename
    
    # GitHub URL
    if github_url and github_url.strip():
        content, filename, detected_language = github_service.fetch_from_url(github_url.strip())
        
        if not content:
            raise HTTPException(status_code=400, detail=ERROR_MESSAGES["github_fetch_failed"])
        
        return content, detected_language, filename
    
    return None, None, None


@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Handle 404 errors."""
    return JSONResponse(
        content={"error": "Endpoint not found"},
        status_code=404
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: HTTPException):
    """Handle 500 errors."""
    return JSONResponse(
        content={"error": "Internal server error"},
        status_code=500
    )


if __name__ == "__main__":
    import uvicorn
    
    # Check for configuration errors
    errors = validate_config()
    if errors:
        print("❌ Configuration errors found:")
        for error in errors:
            print(f"   {error}")
        print("\nPlease fix these errors before starting the server.")
        exit(1)
    
    print(f"🚀 Starting CodeReviewerBot on http://{HOST}:{PORT}")
    print(f"📁 Upload directory: {upload_dir}")
    print(f"📁 Output directory: {output_dir}")
    print(f"🌐 Supported languages: {', '.join(SUPPORTED_LANGUAGES.keys())}")
    print(f"🎯 UI languages: {', '.join(UI_LANGUAGES.keys())}")
    
    uvicorn.run(
        "server:app",
        host=HOST,
        port=PORT,
        reload=True,
        log_level="info"
    )
