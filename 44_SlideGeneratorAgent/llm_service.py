from __future__ import annotations

from typing import Dict, List, Optional

from openai import OpenAI

from config import CONFIG


SYSTEM_PROMPT = (
    "You are SlideGeneratorAgent. Generate professional, presentation-ready slides with strong structure and clarity. "
    "Each slide must include a short, punchy title and 3-5 concise bullets. "
    "Avoid redundancy, keep bullets parallel and specific, and maintain a consistent tone."
)


class LLMService:
    def __init__(self) -> None:
        if not CONFIG.openai_api_key:
            self.client = None
        else:
            self.client = OpenAI(api_key=CONFIG.openai_api_key)

    def is_enabled(self) -> bool:
        return self.client is not None

    def generate(self, topic: str, language: str) -> List[Dict[str, List[str]]]:
        if not self.client:
            raise RuntimeError("LLM not configured")

        want_images = CONFIG.include_images
        min_slides = max(1, int(CONFIG.slides_min))
        max_slides = max(min_slides, int(CONFIG.slides_max))

        user_prompt = (
            f"Topic: {topic}\n"
            f"Language: {language}\n"
            f"Create between {min_slides} and {max_slides} slides (prefer the upper bound).\n"
            "Return pure JSON ONLY, no markdown/code fences. Schema per item: {\n"
            "  \"title\": string,\n"
            "  \"bullets\": string[3..5],\n"
            "  \"image_url\": string | null  // optional illustrative image (royalty-free, representative)\n"
            "}\n"
            "The JSON root must be an array of slide objects."
            + ("\nInclude an appropriate image_url for each slide." if want_images else "\nSet image_url to null.")
        )

        resp = self.client.chat.completions.create(
            model=CONFIG.model,
            temperature=0.7,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        )
        content = resp.choices[0].message.content or "[]"

        import json

        try:
            data = json.loads(content)
            if not isinstance(data, list):
                raise ValueError("Invalid JSON root")
            # normalize
            slides: List[Dict[str, List[str]]] = []
            for item in data:
                title = str(item.get("title", "Slide")).strip()
                bullets = [str(x).strip() for x in item.get("bullets", []) if str(x).strip()]
                image_url: Optional[str] = item.get("image_url")
                image_url = (str(image_url).strip() or None) if image_url is not None else None
                slides.append({
                    "title": title,
                    "bullets": bullets[:6],
                    "image_url": image_url if want_images else None,
                })
            # constrain count to configured bounds
            return slides[:max_slides]
        except Exception:
            # if parsing fails, return empty to allow fallback in caller
            return []


