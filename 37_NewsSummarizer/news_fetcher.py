from dataclasses import dataclass
from typing import List, Optional
import os
from urllib.parse import urlparse
from newspaper import Article
from serpapi import GoogleSearch


@dataclass
class NewsItem:
    title: str
    url: str
    source: str
    category: Optional[str] = None


class NewsFetcher:
    def __init__(self, serpapi_key: Optional[str] = None) -> None:
        self.serpapi_key = serpapi_key or os.getenv("SERPAPI_API_KEY", "")
        if not self.serpapi_key:
            raise ValueError("SERPAPI_API_KEY is required in environment or config.")

    def _extract_source(self, url: str) -> str:
        netloc = urlparse(url).netloc
        return netloc.replace("www.", "")

    def _extract_text(self, url: str) -> str:
        try:
            article = Article(url, language="en")
            article.download()
            article.parse()
            return article.text or ""
        except Exception:
            return ""

    def fetch(self, *, date: str, search: Optional[str], category: Optional[str]) -> List[NewsItem]:
        query = search or "Top news"

        params = {
            "engine": "google_news",
            "q": query,
            "api_key": self.serpapi_key,
            "gl": "us",
            "hl": "en",
        }

        search_engine = GoogleSearch(params)
        results = search_engine.get_dict()
        articles = results.get("news_results", []) or []

        items: List[NewsItem] = []
        for a in articles[:10]:
            link = a.get("link") or a.get("source_url") or ""
            title = a.get("title") or ""
            if not link or not title:
                continue
            source = self._extract_source(link)
            items.append(NewsItem(title=title, url=link, source=source, category=category))

        # If Google News yields nothing, fallback to Google Search (web)
        if not items:
            web_params = {
                "engine": "google",
                "q": query,
                "api_key": self.serpapi_key,
                "gl": "us",
                "hl": "en",
                "num": 10,
            }
            web_results = GoogleSearch(web_params).get_dict()
            organic = web_results.get("organic_results", []) or []
            for r in organic:
                link = r.get("link")
                title = r.get("title")
                if not link or not title:
                    continue
                source = self._extract_source(link)
                items.append(NewsItem(title=title, url=link, source=source, category=category))

        return items

    def fetch_with_text(self, *, date: str, search: Optional[str], category: Optional[str]) -> List[dict]:
        items = self.fetch(date=date, search=search, category=category)
        enriched: List[dict] = []
        for item in items:
            text = self._extract_text(item.url)
            enriched.append({
                "title": item.title,
                "url": item.url,
                "source": item.source,
                "category": item.category,
                "text": text,
            })
        return enriched
