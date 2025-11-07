"""FastAPI Web Application for BookmarkManager Agent"""
from fastapi import FastAPI, Request, Form, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from agent import BookmarkManagerAgent
from config import Config
from utils.llm_service import LLMService
from utils.storage_manager import StorageManager
import json
import os

app = FastAPI(title="BookmarkManager", description="Smart Bookmark Management Agent")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize agent
bookmark_agent = BookmarkManagerAgent(
    llm_service=LLMService(),
    storage_manager=StorageManager()
)


# ==================== PAGE ROUTES ====================

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Render the main bookmark dashboard"""
    try:
        result = bookmark_agent.get_bookmark_stats()
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "default_llm": Config.DEFAULT_LLM,
                "stats": result if result.get("success") else {}
            }
        )
    except Exception as e:
        print(f"Error loading root: {e}")
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "default_llm": Config.DEFAULT_LLM,
                "stats": {}
            }
        )


# ==================== API ROUTES ====================

@app.post("/api/bookmarks/add")
async def add_bookmark(
    url: str = Form(...),
    title: str = Form(...),
    tags: str = Form(""),
    category: str = Form(""),
):
    """Add a new bookmark"""
    try:
        tags_list = [t.strip() for t in tags.split(",") if t.strip()]
        category = category.strip() or "uncategorized"
        
        result = bookmark_agent.add_bookmark(url, title, tags_list, category)
        
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({
            "success": False,
            "message": f"Error adding bookmark: {str(e)}"
        })


@app.get("/api/bookmarks/all")
async def get_all_bookmarks():
    """Get all bookmarks"""
    try:
        result = bookmark_agent.get_all_bookmarks()
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({
            "success": False,
            "message": f"Error retrieving bookmarks: {str(e)}"
        })


@app.get("/api/bookmarks/by-tag")
async def get_bookmarks_by_tag(tag: str = Query(...)):
    """Get bookmarks by tag"""
    try:
        result = bookmark_agent.search_bookmarks_by_tag(tag)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({
            "success": False,
            "message": f"Error retrieving bookmarks: {str(e)}"
        })


@app.get("/api/bookmarks/by-category")
async def get_bookmarks_by_category(category: str = Query(...)):
    """Get bookmarks by category"""
    try:
        result = bookmark_agent.search_bookmarks_by_category(category)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({
            "success": False,
            "message": f"Error retrieving bookmarks: {str(e)}"
        })


@app.post("/api/bookmarks/search")
async def search_bookmarks(
    query: str = Form(...),
    method: str = Form("semantic"),
    llm_choice: str = Form("gemini")
):
    """Search bookmarks (semantic or basic)"""
    try:
        if method == "semantic":
            result = bookmark_agent.semantic_search_bookmarks(query, llm_choice)
        else:
            # Basic search
            bookmarks = bookmark_agent.storage_manager.search_bookmarks(query)
            result = {
                "success": True,
                "query": query,
                "bookmarks": bookmarks,
                "count": len(bookmarks),
                "method": "basic_search"
            }
        
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({
            "success": False,
            "message": f"Error searching bookmarks: {str(e)}"
        })


@app.delete("/api/bookmarks/{bookmark_id}")
async def delete_bookmark(bookmark_id: int):
    """Delete a bookmark"""
    try:
        result = bookmark_agent.delete_bookmark(bookmark_id)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({
            "success": False,
            "message": f"Error deleting bookmark: {str(e)}"
        })


@app.delete("/api/bookmarks/by-tag/{tag}")
async def delete_bookmarks_by_tag(tag: str):
    """Delete all bookmarks with a specific tag"""
    try:
        result = bookmark_agent.delete_bookmarks_by_tag(tag)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({
            "success": False,
            "message": f"Error deleting bookmarks: {str(e)}"
        })


@app.get("/api/tags")
async def get_all_tags():
    """Get all tags"""
    try:
        result = bookmark_agent.get_all_tags()
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({
            "success": False,
            "message": f"Error retrieving tags: {str(e)}"
        })


@app.get("/api/categories")
async def get_all_categories():
    """Get all categories"""
    try:
        result = bookmark_agent.get_all_categories()
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({
            "success": False,
            "message": f"Error retrieving categories: {str(e)}"
        })


@app.get("/api/stats")
async def get_bookmark_stats():
    """Get bookmark statistics"""
    try:
        result = bookmark_agent.get_bookmark_stats()
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({
            "success": False,
            "message": f"Error retrieving stats: {str(e)}"
        })


@app.post("/api/export")
async def export_bookmarks():
    """Export all bookmarks as JSON"""
    try:
        result = bookmark_agent.export_bookmarks()
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({
            "success": False,
            "message": f"Error exporting bookmarks: {str(e)}"
        })


@app.post("/api/import")
async def import_bookmarks(request: Request):
    """Import bookmarks from JSON"""
    try:
        body = await request.json()
        result = bookmark_agent.import_bookmarks(body)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({
            "success": False,
            "message": f"Error importing bookmarks: {str(e)}"
        })


# ==================== HEALTH CHECK ====================

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse({
        "status": "healthy",
        "service": "BookmarkManager",
        "version": "1.0.0"
    })

