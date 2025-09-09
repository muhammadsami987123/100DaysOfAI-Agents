import os
import sys
from typing import Optional, Tuple

# Support package and script modes
try:
    from .utils import parse_simple_query, sanitize_currency, parse_amount
    from . import config
except Exception:
    import os as _os
    sys.path.append(_os.path.dirname(_os.path.abspath(__file__)))
    from utils import parse_simple_query, sanitize_currency, parse_amount  # type: ignore
    import config  # type: ignore

try:
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None  # type: ignore


SYSTEM_PROMPT = (
    "You extract currency conversion intents. Given any user text, return JSON with keys: "
    "amount (number), from_currency (3-letter code), to_currency (3-letter code). "
    "If uncertain or missing fields, return null for those fields. Do not include any text besides JSON."
)


def parse_query(text: str) -> Optional[Tuple[float, str, str]]:
    # First try simple regex fallback to keep it fast and offline-friendly
    simple = parse_simple_query(text)
    if simple:
        return simple

    api_key = config.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
    if not api_key or OpenAI is None:
        return None

    try:
        client = OpenAI(api_key=api_key)
        content = f"User: {text}\nRespond with JSON only."
        resp = client.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": content},
            ],
            temperature=0,
        )
        raw = resp.choices[0].message.content or ""
        # Attempt to parse minimal JSON
        import json

        data = json.loads(raw)
        amount = parse_amount(str(data.get("amount"))) if data.get("amount") is not None else None
        from_code = sanitize_currency(str(data.get("from_currency", "")))
        to_code = sanitize_currency(str(data.get("to_currency", "")))
        if amount is None or not from_code or not to_code:
            return None
        return amount, from_code, to_code
    except Exception:
        return None


def brief_insight(base: str, target: str) -> Optional[str]:
    api_key = config.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
    if not api_key or OpenAI is None:
        return None
    try:
        client = OpenAI(api_key=api_key)
        prompt = (
            f"Provide a one-sentence, non-speculative context about the recent relationship between {base} and {target}. "
            f"Avoid financial advice and dates."
        )
        resp = client.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=60,
        )
        return (resp.choices[0].message.content or "").strip()
    except Exception:
        return None


