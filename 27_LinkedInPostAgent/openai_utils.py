import os
from typing import Optional

from config import get_openai_api_key


MAX_LEN = 3000


def _fake_ai_generate_post(topic: str, tone: str) -> str:
    # Offline-safe structured stub that creates a plausible LinkedIn post
    tone_title = tone.capitalize() if tone else "Professional"
    hook = f"{tone_title} thoughts on {topic}:"
    bullets = [
        f"Why it matters in 2026: impact on teams, products, and careers.",
        f"What to watch: real use-cases, not just demos or buzzwords.",
        f"Skills to build: problem framing, data literacy, and prompt craft.",
        f"Practical next step: start tiny, measure value, iterate weekly.",
    ]
    cta = "What are you experimenting with right now?"
    body = hook + "\n\n" + "\n".join(f"- {b}" for b in bullets) + "\n\n" + cta
    return body


def generate_post_with_ai(topic: str, tone: str = "professional") -> str:
    text = _fake_ai_generate_post(topic=topic, tone=tone)
    return trim_to_limit(text)


def enhance_post_text(text: str, tone: str = "professional", add_emojis: bool = True, add_hashtags: bool = True) -> str:
    enhanced = text.strip()
    if add_emojis:
        enhanced += "\n\n✨"
    if add_hashtags:
        hashtags = generate_hashtags(text, topic_hint=tone)
        if hashtags:
            enhanced += "\n" + " ".join(hashtags)
    # Keep tone implicit in wording; no bracketed prefixes
    return trim_to_limit(enhanced)


def generate_hashtags(text: str, topic_hint: Optional[str] = None) -> list[str]:
    # Simple heuristic; can be replaced with OpenAI
    keywords = []
    lowered = text.lower()
    if "ai" in lowered or "agent" in lowered:
        keywords.append("#AI")
        keywords.append("#Agents")
    if "learning" in lowered or "lessons" in lowered:
        keywords.append("#Learning")
        keywords.append("#CareerGrowth")
    if topic_hint:
        keywords.append(f"#{topic_hint.capitalize()}")
    return list(dict.fromkeys(keywords))[:6]


def trim_to_limit(text: str, max_len: int = MAX_LEN) -> str:
    if len(text) <= max_len:
        return text
    return text[: max_len - 1]


