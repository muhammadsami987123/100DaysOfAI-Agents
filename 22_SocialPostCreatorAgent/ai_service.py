from typing import List

from config import Config


def _ensure_openai():
    try:
        from openai import OpenAI  # type: ignore
    except Exception as exc:
        raise RuntimeError("OpenAI package missing. Install openai>=1.0.0") from exc
    if not Config.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not set.")
    return OpenAI(api_key=Config.OPENAI_API_KEY)


def generate_social_post(platform: str, topic: str, tone: str, insights: List[str]) -> str:
    """Generate a social media post for the specified platform."""
    client = _ensure_openai()
    
    # Get platform-specific constraints
    char_limit = Config.PLATFORM_LIMITS.get(platform, 280)
    
    # Platform-specific system prompts
    platform_prompts = {
        "Twitter": (
            "You are a social media expert writing engaging tweets. "
            f"Respect the {char_limit}-character limit. Use hashtags sparingly but effectively. "
            "Keep it concise and engaging. No emojis unless tone is playful."
        ),
        "Facebook": (
            "You are a social media expert writing engaging Facebook posts. "
            f"Respect the {char_limit}-character limit. "
            "Write in a conversational tone that encourages engagement and comments. "
            "Use line breaks for readability."
        ),
        "Instagram": (
            "You are a social media expert writing Instagram captions. "
            f"Respect the {char_limit}-character limit. "
            "Include relevant hashtags at the end (5-10 hashtags). "
            "Write engaging captions that encourage likes and comments."
        ),
        "LinkedIn": (
            "You are a professional content writer for LinkedIn. "
            f"Respect the {char_limit}-character limit. "
            "Write in a professional, business-focused tone. "
            "Include insights and professional hashtags. Use line breaks for readability."
        ),
        "TikTok": (
            "You are a social media expert writing TikTok captions. "
            f"Respect the {char_limit}-character limit. "
            "Keep it short, catchy, and trending. Use relevant hashtags."
        ),
        "YouTube": (
            "You are a social media expert writing YouTube descriptions. "
            f"Respect the {char_limit}-character limit. "
            "Write engaging descriptions that encourage views and subscriptions. "
            "Include relevant keywords and hashtags."
        )
    }
    
    system = platform_prompts.get(platform, platform_prompts["Twitter"])
    
    insights_bullets = "\n".join(f"- {i}" for i in insights)
    user = (
        f"Platform: {platform}\nTopic: {topic}\nTone: {tone}\nInsights:\n{insights_bullets}\n\n"
        f"Write ONE {platform} post <= {char_limit} characters tailored to the tone and platform style."
    )

    resp = client.chat.completions.create(
        model=Config.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.7,
        max_tokens=char_limit + 50,  # Allow some extra tokens for generation
    )

    text = resp.choices[0].message.content.strip()
    
    # Ensure we don't exceed the character limit
    if len(text) > char_limit:
        text = text[:char_limit - 3] + "..."
    
    return text


def generate_tweet(topic: str, tone: str, insights: List[str]) -> str:
    """Legacy function for backward compatibility - now calls generate_social_post for Twitter"""
    return generate_social_post("Twitter", topic, tone, insights)


