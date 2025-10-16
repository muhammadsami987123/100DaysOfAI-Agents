from typing import List, Dict, Optional
from utils.llm_service import LLMService


def _sanitize(text: str) -> str:
	return (text or "").strip()


def _title_case(title: str) -> str:
	clean = _sanitize(title)
	if not clean:
		return "Untitled Episode"
	return clean[0].upper() + clean[1:]


def _default_guest_for_topic(topic: str) -> str:
	low = topic.lower()
	if any(k in low for k in ["health", "medicine", "bio", "wellness"]):
		return "Doctor or HealthTech Entrepreneur"
	if any(k in low for k in ["education", "edtech", "learn", "school"]):
		return "EdTech Founder or Innovator"
	if any(k in low for k in ["finance", "invest", "crypto", "fintech"]):
		return "FinTech Analyst or Founder"
	if any(k in low for k in ["startup", "product", "growth", "marketing"]):
		return "Startup Founder or Growth Marketer"
	if any(k in low for k in ["environment", "sustain", "climate"]):
		return "Climate Researcher or Sustainability Leader"
	return "Domain Expert or Practitioner"


def _outline_segments(topic: str, guest_type: str) -> List[str]:
	return [
		f"Opening: Why {topic} matters right now",
		f"Guest Perspective: {guest_type} shares lived experience",
		f"Deep Dive: Trends, challenges, and opportunities in {topic}",
		"Audience Q&A or Hot Takes: Address common misconceptions",
		"Closing: Key insights and next steps"
	]


def _key_takeaways(topic: str) -> List[str]:
	return [
		f"Clear understanding of {topic} trends",
		"Actionable strategies you can apply this week",
		"Pitfalls to avoid and realistic expectations",
		"Resources and tools to continue exploring",
	]


def _twist_suggestions(topic: str) -> List[str]:
	return [
		f"Live mini-audit related to {topic} with the guest",
		"Bring a listener on-air for a lightning consult",
		"Record in an unusual setting relevant to the theme",
		"Run a 5-minute myth-busting speed round",
	]


def _generate_title(topic: str) -> str:
	base = _sanitize(topic)
	if not base:
		return "Fresh Ideas: A Deep Dive"
	return _title_case(f"{base}: What No One Tells You")


def generate_podcast_idea(topic: str, guest_type: Optional[str] = None) -> Dict[str, List[str] | str]:
	clean_topic = _sanitize(topic)
	if not clean_topic:
		raise ValueError("Topic is required")

	guest = _sanitize(guest_type) or _default_guest_for_topic(clean_topic)
	# Try LLM first
	service = LLMService()
	prompt = (
		"You are PodcastIdeaBot. Return STRICT JSON only. Keys: "
		"title (string), outline (array of 3-5 strings), guest_type (string), "
		"takeaways (array of 3-5 strings), audience (string), twist (string).\n\n"
		f"Topic: {clean_topic}\n"
		f"Suggested/Preferred guest type: {guest}\n\n"
		"Requirements:\n"
		"- Title: catchy, natural, podcast-ready.\n"
		"- Outline: realistic conversation flow (opening, guest perspective, deep dive, debate/Q&A, closing).\n"
		"- Takeaways: 3-5 concrete insights.\n"
		"- Audience: who benefits most.\n"
		"- Twist: one creative idea (format, live demo, challenge, location).\n"
		"Do NOT include any extra prose outside JSON."
	)
	data = service.ideate_podcast(prompt)
	if data and isinstance(data, dict) and data.get("title"):
		# Minimal normalization and fallback for missing fields
		return {
			"title": data.get("title") or _generate_title(clean_topic),
			"outline": data.get("outline") or _outline_segments(clean_topic, guest),
			"guest_type": data.get("guest_type") or guest,
			"takeaways": data.get("takeaways") or _key_takeaways(clean_topic),
			"audience": data.get("audience") or "Listeners interested in the topic and practical insights",
			"twist": data.get("twist") or _twist_suggestions(clean_topic)[0],
		}

	# Rule-based fallback
	title = _generate_title(clean_topic)
	outline = _outline_segments(clean_topic, guest)
	takeaways = _key_takeaways(clean_topic)
	twist = _twist_suggestions(clean_topic)[0]

	return {
		"title": title,
		"outline": outline,
		"guest_type": guest,
		"takeaways": takeaways,
		"audience": "Listeners interested in the topic and practical insights",
		"twist": twist,
	}


def generate_multiple_ideas(topic: str, guest_type: Optional[str] = None, count: int = 1) -> List[Dict[str, List[str] | str]]:
	count = max(1, min(5, int(count or 1)))
	ideas: List[Dict[str, List[str] | str]] = []
	for i in range(count):
		idea = generate_podcast_idea(topic, guest_type)
		# Slightly vary twist per idea
		twists = _twist_suggestions(topic)
		idea["twist"] = twists[i % len(twists)]
		ideas.append(idea)
	return ideas


def generate_episode_script(idea: dict) -> str:
    """
    Generate a full podcast script based on the provided idea dict
    (includes title, outline, guest_type, takeaways, audience, twist).
    Tries LLM if available; otherwise, uses a structured template.
    """
    # Compose prompt
    topic = idea.get('title') or 'Podcast Topic'
    outline = idea.get('outline') or []
    guest_type = idea.get('guest_type') or ''
    takeaways = idea.get('takeaways') or []
    audience = idea.get('audience') or ''
    twist = idea.get('twist') or ''

    # Try LLM (if available)
    try:
        service = LLMService()
        script_prompt = (
            f"You are PodcastScriptBot. Write a realistic, 3-5 minute podcast episode script for the following podcast episode idea.\n\n"
            f"Title: {topic}\n"
            f"Outline: {'; '.join(outline)}\n"
            f"Guest Type: {guest_type}\n"
            f"Takeaways: {'; '.join(takeaways)}\n"
            f"Audience: {audience}\n"
            f"Twist: {twist}\n"
            "\nRequirements:\n- Script must sound like a friendly, dynamic podcast show. Structure like intro, guest intro, main convo, guest takes, rapid-fire, closing, etc.\n"
            "- Every section should feel natural in present-tense, with some dialogue.\n- Use clear labeled cues (Host, Guest, etc).\n- Include a creative use of the twist in the flow (if relevant).\n- Make it easy to adapt for recording, not too generic.\n- About 400-600 words.\n- Reply with the script only. No metadata or preamble.\n"
        )
        # Use LLMService, prefer Gemini then OpenAI
        script_text_result = None
        if hasattr(service, "gemini_model") and service.gemini_model is not None:
            result = service.gemini_model.generate_content(script_prompt)
            script_text_result = getattr(result, "text", None)
        elif hasattr(service, "openai_client") and service.openai_client is not None:
            resp = service.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are PodcastScriptBot."},
                    {"role": "user", "content": script_prompt},
                ],
                temperature=0.6,
            )
            script_text_result = resp.choices[0].message.content if resp.choices else None
        if script_text_result:
            return script_text_result.strip()
    except Exception:
        pass

    # Fallback: Manual template (rule-based)
    parts = [f"[INTRO]", f"Host: Welcome to our podcast! Today’s episode is '{topic}'."]
    if audience:
        parts.append(f"(For: {audience})")
    parts.append(f"\n[OUTLINE]")
    for i, seg in enumerate(outline or []):
        parts.append(f"  {i+1}. {seg}")
    parts.append(f"\n[GUEST INTRO]")
    if guest_type:
        parts.append(f"Host: Please welcome our guest, a {guest_type}!\nGuest: Thank you for having me!")
    parts.append(f"\n[MAIN DISCUSSION]")
    for seg in outline or []:
        parts.append(f"Host: Let's talk about: {seg}")
        parts.append(f"Guest: [Shares perspective]")
    if takeaways:
        parts.append(f"\n[KEY TAKEAWAYS]")
        for t in takeaways:
            parts.append(f"- {t}")
    if twist:
        parts.append(f"\n[UNIQUE TWIST]\nHost: Time for something special: {twist}")
    parts.append(f"\n[CLOSING]\nHost: That's a wrap. Thanks to our guest and our listeners!")
    return '\n'.join(parts)


