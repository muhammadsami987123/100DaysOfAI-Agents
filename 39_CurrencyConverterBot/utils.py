import json
import re
from datetime import datetime, timezone
from typing import Optional, Tuple


_CURRENCY_SYMBOLS = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "JPY": "¥",
    "CNY": "¥",
    "INR": "₹",
    "PKR": "₨",
    "CAD": "$",
    "AUD": "$",
    "CHF": "CHF",
}


def get_currency_symbol(code: str) -> str:
    return _CURRENCY_SYMBOLS.get(code.upper(), code.upper())


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def parse_amount(value: str) -> Optional[float]:
    try:
        cleaned = value.replace(",", "").strip()
        return float(cleaned)
    except Exception:
        return None


def sanitize_currency(code: str) -> Optional[str]:
    if not code:
        return None
    code = code.strip().upper()
    if not re.fullmatch(r"[A-Z]{3}", code):
        return None
    return code


def load_json(path: str) -> Optional[dict]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def save_json(path: str, data: dict) -> bool:
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def format_total(amount: float, code: str) -> str:
    symbol = get_currency_symbol(code)
    return f"{symbol}{amount:,.2f}"


def parse_simple_query(text: str) -> Optional[Tuple[float, str, str]]:
    # Regex fallback for simple queries like "Convert 100 USD to INR" or "50 GBP in PKR"
    pattern = re.compile(
        r"(?i)\b(?:convert\s*)?(?P<amount>[\d,]+(?:\.\d+)?)\s*(?P<from>[a-zA-Z]{3})\s*(?:to|in)\s*(?P<to>[a-zA-Z]{3})\b"
    )
    m = pattern.search(text)
    if not m:
        return None
    amount = parse_amount(m.group("amount"))
    from_code = sanitize_currency(m.group("from"))
    to_code = sanitize_currency(m.group("to"))
    if amount is None or not from_code or not to_code:
        return None
    return amount, from_code, to_code


