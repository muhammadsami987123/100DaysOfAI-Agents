from typing import List
import requests
from config import Config


def fetch_latest_insights(topic: str) -> List[str]:
    """Fetch recent insights about a topic using SerpAPI or NewsAPI.

    Falls back gracefully if keys are missing.
    Returns a list of short bullet-style insights.
    """
    insights: List[str] = []

    if Config.NEWSAPI_KEY:
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                "q": topic,
                "sortBy": "publishedAt",
                "language": "en",
                "pageSize": 5,
                "apiKey": Config.NEWSAPI_KEY,
            }
            resp = requests.get(url, params=params, timeout=10)
            if resp.ok:
                data = resp.json()
                for article in data.get("articles", [])[:5]:
                    title = article.get("title")
                    source = (article.get("source") or {}).get("name", "")
                    if title:
                        insights.append(f"{title} — {source}")
        except Exception:
            pass

    # If no insights yet, return a default hint to proceed
    if not insights:
        insights.append(f"Key updates about {topic} in the last day")
    return insights


