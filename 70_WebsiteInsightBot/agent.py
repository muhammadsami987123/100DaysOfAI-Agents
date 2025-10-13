import requests
from bs4 import BeautifulSoup
from langdetect import detect, LangDetectException
import os
import re
from typing import Dict, Any

# --- Gemini LLM Integration ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", None)
GEMINI_MODEL = "gemini-2.0-flash"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key=" + GEMINI_API_KEY if GEMINI_API_KEY else None

# Prompt template for LLM
PROMPT_FORMAT = """
You're WebsiteInsightBot, an intelligent agent. Your tasks:
1. {summary_instruction}
2. Extract 5-15 SEO keywords.
3. Detect and explain sentiment (Positive/Negative/Neutral).
Output ONLY in this markdown format:
Website Summary:
(Summary...)
Top Keywords:
(List/keywords...)
Sentiment:
(Sentiment + 1-line reason)
---
CONTENT (in English or translated):
"""
def call_gemini_llm(context: str, long_form: bool) -> str:
    if not GEMINI_API_URL:
        return "ERROR: Gemini API key is missing."
    summary_instruction = (
        "Write a detailed, multi-paragraph summary of the website's key points, tone, and information."
        if long_form else
        "Write a concise 1-2 sentence summary of the website's main idea(s)."
    )
    prompt = PROMPT_FORMAT.format(summary_instruction=summary_instruction) + context
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    resp = requests.post(GEMINI_API_URL, json=data)
    if resp.status_code != 200:
        return f"ERROR: Gemini API error {resp.status_code}"
    out = resp.json()
    try:
        return (
            out["candidates"][0]["content"]["parts"][0]["text"]
            if "candidates" in out and out["candidates"] and "content" in out["candidates"][0]
            else "ERROR: Unexpected LLM response"
        )
    except Exception:
        return "ERROR: Failed to parse Gemini response."

def fetch_visible_text_and_meta(url: str):
    """Fetches main text, title, and favicon url from page."""
    try:
        resp = requests.get(url, timeout=10)
    except Exception:
        return "__UNREACHABLE__", None, None
    if resp.status_code != 200:
        return "__UNREACHABLE__", None, None
    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style", "footer", "nav", "aside"]):
        tag.decompose()
    texts = soup.stripped_strings
    content = " ".join(t for t in texts if len(t) > 30)
    # Site title
    title = soup.title.string.strip() if soup.title and soup.title.string else url
    # Favicon
    favicon = None
    iconlink = soup.find("link", rel=lambda x: x and "icon" in x.lower())
    if iconlink and iconlink.get("href"):
        favicon = iconlink["href"]
        # Absolute URL if needed
        if not favicon.startswith("http"):
            from urllib.parse import urljoin
            favicon = urljoin(url, favicon)
    return content.strip() if content else "__EMPTY__", title, favicon

def website_insight_bot(url: str, long_form: bool = False) -> Dict[str, Any]:
    """Orchestrates fetching, prepping, and analyzing page."""
    if not (url.startswith("http://") or url.startswith("https://")):
        return {"error": "Only valid URLs (http/https) are accepted."}
    text, title, favicon = fetch_visible_text_and_meta(url)
    if text == "__UNREACHABLE__":
        return {"error": "The website is currently unreachable or restricted."}
    if text == "__EMPTY__":
        return {"error": "No valuable content found."}
    # Detect language
    try:
        lang = detect(text)
    except LangDetectException:
        lang = "unknown"
    if lang != "en":
        main_context = f"\n(Original language: {lang})\n{text}"
    else:
        main_context = text
    # Call Gemini for insight
    llm_result = call_gemini_llm(main_context, long_form=long_form)
    if llm_result.startswith("ERROR"):
        return {"error": llm_result}
    # Parse markdown output with more robust splitting
    summary, keywords, sentiment = "", "", ""
    m = re.search(r"Website Summary:\s*(.*?)\n+Top Keywords:\s*(.*?)\n+Sentiment:\s*(.*)", llm_result, re.DOTALL | re.IGNORECASE)
    if m:
        summary = m.group(1).strip()
        keywords = m.group(2).strip()
        sentiment = m.group(3).strip()
    else:
        # fallback: try to split by headings
        parts = re.split(r"^Website Summary:|^Top Keywords:|^Sentiment:", llm_result, flags=re.MULTILINE)
        if len(parts) >= 4:
            summary, keywords, sentiment = [x.strip() for x in parts[1:4]]
        else:
            summary = llm_result.strip()
    return {
        "summary": summary,
        "keywords": keywords,
        "sentiment": sentiment,
        "site_title": title,
        "site_favicon": favicon,
        "model": GEMINI_MODEL
    }
