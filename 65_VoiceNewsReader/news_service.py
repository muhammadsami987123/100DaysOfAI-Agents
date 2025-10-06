from typing import List, Dict, Optional
import requests
from datetime import datetime
from urllib.parse import urlencode
from config import Config


class NewsService:
    """Fetch trending news using NewsAPI (preferred) with optional filters.
    Falls back gracefully to Bing News if configured.
    """

    def __init__(self):
        self.newsapi_key = Config.NEWSAPI_KEY
        self.bing_key = Config.BING_NEWS_KEY
        # Common country name/code normalization map
        self.country_map = {
            # codes map to themselves
            "us": "us", "gb": "gb", "uk": "gb", "pk": "pk", "in": "in", "ca": "ca", "au": "au",
            "de": "de", "fr": "fr", "it": "it", "es": "es", "sa": "sa", "ae": "ae",
            # names
            "united states": "us", "usa": "us", "america": "us",
            "united kingdom": "gb", "britain": "gb", "england": "gb",
            "pakistan": "pk", "india": "in", "canada": "ca", "australia": "au",
            "germany": "de", "france": "fr", "italy": "it", "spain": "es",
            "saudi arabia": "sa", "uae": "ae", "united arab emirates": "ae",
        }

        # NewsAPI language codes (note: Urdu is 'ud' on NewsAPI)
        self.language_map = {
            "en": "en", "english": "en",
            "ur": "ud", "urdu": "ud",
            "de": "de", "fr": "fr", "es": "es", "it": "it", "nl": "nl",
            "pt": "pt", "ru": "ru", "se": "se", "zh": "zh", "ar": "ar",
        }

    def fetch_top_headlines(
        self,
        *,
        category: Optional[str] = None,
        country: Optional[str] = None,
        q: Optional[str] = None,
        limit: int = 5,
        language: Optional[str] = None,
        date_range: Optional[str] = None,
    ) -> List[Dict]:
        """Choose best NewsAPI endpoint based on filters:
        - If keyword-only search (q present) and no country/category → use `everything` with language.
        - Else → use `top-headlines` with country/category/q and pageSize.
        Falls back to Bing News if configured.
        """
        limit = max(1, min(int(limit or 5), 10))
        use_keyword_only = bool(q) and not (country or category)
        if self.newsapi_key:
            try:
                if use_keyword_only:
                    return self._newsapi_everything(
                        q=q or "",
                        page_size=limit,
                        language=self._normalize_language(language),
                        date_range=date_range or "any",
                    )

                items = self._newsapi_top_headlines(
                    category=category,
                    country=self._normalize_country(country),
                    q=q,
                    page_size=limit,
                )

                # Smart fallback: if no items from top-headlines, try everything with best-effort query
                if not items:
                    fallback_q = (q or "").strip()
                    if not fallback_q:
                        parts = []
                        if category:
                            parts.append(str(category))
                        if country:
                            parts.append(self._country_name_for_query(country))
                        fallback_q = " ".join(parts) or "Top news"

                    # Prefer country-scoped RSS when a country is selected
                    norm_country = self._normalize_country(country)
                    if norm_country:
                        return self._google_news_rss(
                            q=fallback_q,
                            count=limit,
                            language=(language or "en"),
                            country=norm_country,
                        )

                    # Otherwise use NewsAPI everything
                    return self._newsapi_everything(
                        q=fallback_q,
                        page_size=limit,
                        language=self._normalize_language(language),
                        date_range=date_range or "any",
                    )

                return items
            except Exception:
                pass
        if self.bing_key:
            try:
                return self._bingnews_search(q=q or category or "Top news", count=limit)
            except Exception:
                pass
        # Last resort: Google News RSS (no API key). Works well for keyword searches.
        try:
            return self._google_news_rss(
                q=q or category or "Top news",
                count=limit,
                language=(language or "en"),
                country=(self._normalize_country(country) or "us"),
            )
        except Exception:
            return []

    def _newsapi_top_headlines(
        self,
        *,
        category: Optional[str],
        country: Optional[str],
        q: Optional[str],
        page_size: int,
        language: Optional[str],
    ) -> List[Dict]:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "apiKey": self.newsapi_key,
            "pageSize": page_size,
        }
        if country:
            params["country"] = country
        if category:
            params["category"] = category
        if q:
            params["q"] = q

        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        items: List[Dict] = []
        for a in data.get("articles", [])[:page_size]:
            items.append({
                "title": a.get("title"),
                "description": a.get("description") or "",
                "url": a.get("url"),
                "source": (a.get("source") or {}).get("name", ""),
                "publishedAt": a.get("publishedAt"),
            })
        return items

    def _newsapi_everything(self, *, q: str, page_size: int, language: Optional[str], date_range: Optional[str]) -> List[Dict]:
        url = "https://newsapi.org/v2/everything"
        params = {
            "apiKey": self.newsapi_key,
            "q": q,
            "sortBy": "publishedAt",
            "pageSize": page_size,
        }
        if language:
            params["language"] = language
        # Date range handling: day|week|month
        from datetime import datetime, timedelta
        now = datetime.utcnow()
        if (date_range or "").lower() == "day":
            from_date = (now - timedelta(days=1)).strftime("%Y-%m-%d")
            params["from"] = from_date
        elif (date_range or "").lower() == "week":
            from_date = (now - timedelta(days=7)).strftime("%Y-%m-%d")
            params["from"] = from_date
        elif (date_range or "").lower() == "month":
            from_date = (now - timedelta(days=30)).strftime("%Y-%m-%d")
            params["from"] = from_date
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        items: List[Dict] = []
        for a in data.get("articles", [])[:page_size]:
            items.append({
                "title": a.get("title"),
                "description": a.get("description") or "",
                "url": a.get("url"),
                "source": (a.get("source") or {}).get("name", ""),
                "publishedAt": a.get("publishedAt"),
            })
        return items

    def _normalize_country(self, value: Optional[str]) -> Optional[str]:
        if not value:
            return None
        key = str(value).strip().lower()
        return self.country_map.get(key, key if len(key) == 2 else None)

    def _normalize_language(self, value: Optional[str]) -> Optional[str]:
        if not value:
            return None
        key = str(value).strip().lower()
        return self.language_map.get(key, None)

    def _country_name_for_query(self, value: Optional[str]) -> str:
        if not value:
            return ""
        key = str(value).strip().lower()
        # reverse map code to a readable name
        reverse = {v: k for k, v in self.country_map.items()}
        name = reverse.get(key, key)
        # title-case nicely for query
        return name.title()

    def _google_news_rss(self, *, q: str, count: int, language: str, country: str) -> List[Dict]:
        # Build Google News RSS search URL
        base = "https://news.google.com/rss/search"
        gl = (country or "us").upper()
        hl = (language or "en").lower()
        ceid = f"{gl}:{hl}"
        params = {"q": q, "hl": hl, "gl": gl, "ceid": ceid}
        url = f"{base}?{urlencode(params)}"

        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        # Minimal XML parsing
        import xml.etree.ElementTree as ET
        root = ET.fromstring(resp.content)
        channel = root.find("channel")
        items_xml = channel.findall("item") if channel is not None else []
        items: List[Dict] = []
        for it in items_xml[:count]:
            title_el = it.find("title")
            link_el = it.find("link")
            pub_el = it.find("pubDate")
            source_el = it.find("{http://www.w3.org/2005/Atom}source")
            items.append({
                "title": title_el.text if title_el is not None else "",
                "description": "",
                "url": link_el.text if link_el is not None else "",
                "source": (source_el.text if source_el is not None else "Google News"),
                "publishedAt": pub_el.text if pub_el is not None else None,
            })
        return items

    def _bingnews_search(self, *, q: str, count: int) -> List[Dict]:
        url = "https://api.bing.microsoft.com/v7.0/news/search"
        params = {"q": q, "count": count, "mkt": "en-US", "freshness": "Day"}
        headers = {"Ocp-Apim-Subscription-Key": self.bing_key}
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        items: List[Dict] = []
        for v in data.get("value", [])[:count]:
            items.append({
                "title": v.get("name"),
                "description": v.get("description") or "",
                "url": v.get("url"),
                "source": ((v.get("provider") or [{}])[0] or {}).get("name", ""),
                "publishedAt": v.get("datePublished"),
            })
        return items


