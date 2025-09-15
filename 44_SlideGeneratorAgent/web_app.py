"""
Web application for SlideGeneratorAgent using FastAPI, matching Day 36 structure
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import CONFIG
from llm_service import LLMService


BASE_DIR = Path(__file__).parent.resolve()
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
SLIDES_DIR = BASE_DIR / "slides"
def _download_image(url: str, out_dir: Path, idx: int) -> Optional[str]:
    try:
        import os
        import hashlib
        import mimetypes
        import requests

        out_dir.mkdir(parents=True, exist_ok=True)
        # derive filename from URL hash to avoid collisions
        h = hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]
        # try to guess extension
        ext = os.path.splitext(url)[1].lower()
        if not ext or len(ext) > 5:
            # fallback based on content-type later
            ext = ""
        resp = requests.get(url, timeout=CONFIG.image_timeout_sec, stream=True)
        resp.raise_for_status()
        ctype = resp.headers.get("Content-Type", "").split(";")[0].strip()
        if not ext:
            guessed = mimetypes.guess_extension(ctype or "") or ".jpg"
            ext = guessed
        fname = f"img_{idx}_{h}{ext}"
        fpath = out_dir / fname
        with open(fpath, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        # return web path relative to slides mount
        return f"/slides/{out_dir.name}/{fname}"
    except Exception:
        return None



def _slugify(value: str) -> str:
    import re

    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\-\s]", "", value)
    value = re.sub(r"\s+", "-", value)
    return value or "topic"


def _estimate_minutes(num_slides: int) -> int:
    # Assume ~15 seconds per slide for concise reading; clamp to at least 1 minute
    return max(1, int(round(num_slides * 0.25)))


def _slides_to_markdown(topic: str, slides: List[Dict[str, List[str]]]) -> str:
    lines: List[str] = [f"# {topic}"]
    for s in slides:
        lines.append("")
        lines.append(f"## {s['title']}")
        image_url = s.get("image_url") if isinstance(s, dict) else None
        if image_url:
            lines.append(f"![image]({image_url})")
        for b in s["bullets"]:
            lines.append(f"- {b}")
    return "\n".join(lines) + "\n"


def _slides_to_html(topic: str, slides: List[Dict[str, List[str]]]) -> str:
    items = []
    for s in slides:
        bullets = "\n".join(f"<li class=\"list-disc ml-6\">{b}</li>" for b in s["bullets"])
        image_html = ""
        image_url = s.get("image_url") if isinstance(s, dict) else None
        if image_url:
            image_html = f"<img src=\"{image_url}\" alt=\"{s['title']}\" class=\"w-full rounded-lg border border-slate-200 mt-3\" loading=\"lazy\" />"
        items.append(
            f"""
            <article class=\"rounded-xl border border-slate-200 shadow-sm p-5 bg-white\">
              <h2 class=\"text-lg font-semibold text-slate-800\">{s['title']}</h2>
              {image_html}
              <ul class=\"mt-3 space-y-1 text-slate-700\">{bullets}</ul>
            </article>
            """
        )
    content = "\n".join(items)
    return f"""
<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{topic} — Slides</title>
  <script src=\"https://cdn.tailwindcss.com\"></script>
  <style>body{{background:#f7fafc}}</style>
  </head>
  <body class=\"min-h-screen\">
    <main class=\"max-w-4xl mx-auto p-6 space-y-4\">
      <header class=\"mb-2\"><h1 class=\"text-2xl font-bold text-slate-900\">{topic}</h1></header>
      <section class=\"grid gap-4\">{content}</section>
    </main>
  </body>
</html>
"""


def _save(topic: str, slides: List[Dict[str, List[str]]]) -> Dict[str, str]:
    SLIDES_DIR.mkdir(parents=True, exist_ok=True)
    safe = _slugify(topic)
    out_dir = SLIDES_DIR / safe
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / "slides.md"
    html_path = out_dir / "index.html"
    # optionally download images and rewrite image_url to local paths
    if CONFIG.download_images:
        for i, s in enumerate(slides):
            url = s.get("image_url") if isinstance(s, dict) else None
            if url:
                local = _download_image(url, out_dir, i)
                if local:
                    s["image_url"] = local
    md_path.write_text(_slides_to_markdown(topic, slides), encoding="utf-8")
    html_path.write_text(_slides_to_html(topic, slides), encoding="utf-8")
    return {"topic_dir": str(out_dir), "md": str(md_path), "html": str(html_path), "slug": safe}


def create_app() -> FastAPI:
    app = FastAPI(title="SlideGeneratorAgent")

    # Ensure directories exist
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    SLIDES_DIR.mkdir(parents=True, exist_ok=True)

    templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
    # expose slides dir for serving downloaded images
    app.mount("/slides", StaticFiles(directory=str(SLIDES_DIR)), name="slides")

    llm = LLMService()

    @app.get("/", response_class=HTMLResponse)
    async def home(request: Request) -> HTMLResponse:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "languages": [
                    {"code": "en", "label": "English"},
                    {"code": "ur", "label": "Urdu"},
                    {"code": "hi", "label": "Hindi"},
                ],
            },
        )

    @app.post("/api/generate")
    async def generate(payload: Dict[str, str]):
        topic = (payload.get("topic") or "").strip()
        language = (payload.get("language") or "en").strip()
        if not topic:
            return JSONResponse({"success": False, "error": "Topic is required"}, status_code=400)
        if not llm.is_enabled():
            return JSONResponse({"success": False, "error": "LLM not configured. Set OPENAI_API_KEY."}, status_code=400)

        slides = llm.generate(topic, language)
        if not slides:
            return JSONResponse({"success": False, "error": "Failed to generate slides"}, status_code=500)

        saved = _save(topic, slides)
        return JSONResponse(
            {
                "success": True,
                "slides": slides,
                "saved": saved,
                "slide_count": len(slides),
                "est_minutes": _estimate_minutes(len(slides)),
                "slug": saved["slug"],
                "llm": True,
            }
        )

    @app.get("/download/{topic_slug}/slides.md")
    async def download_md(topic_slug: str):
        path = SLIDES_DIR / topic_slug / "slides.md"
        if not path.exists():
            return JSONResponse({"success": False, "error": "File not found"}, status_code=404)
        return FileResponse(str(path), filename="slides.md", media_type="text/markdown")

    @app.get("/download/{topic_slug}/index.html")
    async def download_html(topic_slug: str):
        path = SLIDES_DIR / topic_slug / "index.html"
        if not path.exists():
            return JSONResponse({"success": False, "error": "File not found"}, status_code=404)
        return FileResponse(str(path), filename="slides.html", media_type="text/html")

    return app


