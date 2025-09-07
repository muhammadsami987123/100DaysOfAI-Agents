from dataclasses import dataclass
from typing import List, Optional
import os
from openai import OpenAI


@dataclass
class ArticleSummary:
    title: str
    source: str
    url: str
    tags: List[str]
    bullets: List[str]
    label: str  # Alert-Level | Trending | Regional


class Summarizer:
    def __init__(self, openai_api_key: Optional[str] = None) -> None:
        api_key = openai_api_key or os.getenv("OPENAI_API_KEY", "")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required in environment or config.")
        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def _build_prompt(self, title: str, url: str, source: str, category: Optional[str], text: str) -> str:
        return (
            "You are a newsroom assistant. Read the article text and produce a concise brief.\n"
            "Return 3-5 bullets that cover: main issue, key facts, impact, and tone.\n"
            "Also assign a label: one of [Alert-Level, Trending, Regional].\n\n"
            f"Title: {title}\n"
            f"Source: {source}\n"
            f"URL: {url}\n"
            f"Category: {category or 'general'}\n\n"
            f"Article Text:\n{text}\n\n"
            "Format strictly as:\n"
            "BULLETS:\n- ...\n- ...\n- ...\nLABEL: <one-word>\n"
        )

    def summarize(self, *, title: str, url: str, source: str, category: Optional[str], text: str = "") -> ArticleSummary:
        prompt = self._build_prompt(title, url, source, category, text or "")
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You write concise, factual news briefs."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        content = completion.choices[0].message.content.strip()

        bullets: List[str] = []
        label = "Trending"
        section = "bullets"
        for line in content.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.upper().startswith("LABEL:"):
                label = line.split(":", 1)[1].strip() or label
                section = "label"
                continue
            if line.upper().startswith("BULLETS:"):
                section = "bullets"
                continue
            if section == "bullets" and line.startswith("-"):
                bullets.append(line.lstrip("- "))

        tags = [t for t in [category, "news"] if t]
        return ArticleSummary(
            title=title,
            source=source,
            url=url,
            tags=tags,
            bullets=bullets[:5] if bullets else ["No summary available."],
            label=label or "Trending",
        )
