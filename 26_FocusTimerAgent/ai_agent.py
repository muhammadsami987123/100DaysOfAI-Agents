from __future__ import annotations

from typing import List

# Support running as a module or as a script
try:
	from .config import CONFIG
except Exception:  # pragma: no cover
	from config import CONFIG  # type: ignore


def _ensure_openai():
	try:
		from openai import OpenAI  # type: ignore
	except Exception as exc:  # pragma: no cover
		raise RuntimeError("OpenAI package missing. Install openai>=1.0.0") from exc
	if not CONFIG.openai_api_key:
		raise RuntimeError("OPENAI_API_KEY is not set.")
	return OpenAI(api_key=CONFIG.openai_api_key)


def coach_message(context: str, mood: str = "neutral", minutes_left: int | None = None) -> str:
	"""Return a brief motivational coaching message tailored to the session.

	- context: e.g., "starting focus", "mid-session", "struggling", "ending soon".
	- mood: e.g., "energized", "tired", "distracted".
	- minutes_left: optional integer minutes remaining.
	"""
	client = _ensure_openai()

	sys_prompt = (
		"You are FocusTimerCoach, a concise motivational assistant that helps users stay focused. "
		"Provide 1-2 sentences max. Be specific, supportive, and practical. Avoid cliches."
	)
	user_prompt = (
		f"Context: {context}\n"
		f"Mood: {mood}\n"
		f"Minutes left: {minutes_left if minutes_left is not None else 'unknown'}\n"
		"Respond with a single short message."
	)

	resp = client.chat.completions.create(
		model=CONFIG.openai_model,
		messages=[
			{"role": "system", "content": sys_prompt},
			{"role": "user", "content": user_prompt},
		],
		temperature=0.7,
		max_tokens=120,
	)
	return resp.choices[0].message.content.strip()


