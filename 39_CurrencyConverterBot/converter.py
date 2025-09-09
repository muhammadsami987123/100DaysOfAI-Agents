import requests
import sys
import os
from datetime import datetime, timezone
from typing import Optional, Tuple, Dict, Any

# Support package and script modes
try:
    from .utils import load_json, save_json
    from . import config
except Exception:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from utils import load_json, save_json  # type: ignore
    import config  # type: ignore


CACHE_PATH = config.get_cache_path()


def _fetch_latest_rates(base: str) -> Optional[dict]:
    # Using exchangerate.host free API
    try:
        url = f"{config.EXCHANGE_RATE_API_BASE}/latest?base={base.upper()}"
        # If user provided API key (for services that support keys via query param)
        if getattr(config, "EXCHANGE_RATE_API_KEY", ""):
            url += f"&api_key={config.EXCHANGE_RATE_API_KEY}"
        resp = requests.get(url, timeout=config.get_request_timeout())
        if resp.status_code != 200:
            return None
        data = resp.json()
        if not data or "rates" not in data:
            return None
        data["_fetched_at"] = datetime.now(timezone.utc).isoformat()
        return data
    except Exception:
        return None


def _read_cache() -> Optional[dict]:
    return load_json(CACHE_PATH)


def _write_cache(snapshot: dict) -> bool:
    return save_json(CACHE_PATH, snapshot)


def convert(amount: float, from_code: str, to_code: str) -> Tuple[Optional[float], Optional[float], Dict[str, Any]]:
    """
    Returns (converted_amount, rate, meta)
    meta contains keys: { source: "api"|"cache", timestamp: str, warning?: str }
    """
    base = from_code.upper()
    target = to_code.upper()

    latest = _fetch_latest_rates(base)
    meta = {}
    if latest and latest.get("rates", {}).get(target) is not None:
        rate = float(latest["rates"][target])
        converted = amount * rate
        _write_cache({"base": base, "rates": latest["rates"], "timestamp": latest.get("date"), "_fetched_at": latest.get("_fetched_at")})
        meta = {
            "source": "api",
            "timestamp": latest.get("date") or latest.get("_fetched_at"),
        }
        return converted, rate, meta

    # Fallback to cache
    cache = _read_cache() or {}
    if cache.get("base") == base and cache.get("rates", {}).get(target) is not None:
        rate = float(cache["rates"][target])
        converted = amount * rate
        meta = {
            "source": "cache",
            "timestamp": cache.get("timestamp") or cache.get("_fetched_at"),
            "warning": "Using cached rates due to network/API issue.",
        }
        return converted, rate, meta

    # If cache base differs, try cross via cache by fetching base=EUR or USD if available
    if cache.get("rates") and cache.get("base") and cache["rates"].get(target) and cache["rates"].get(base):
        # rates map is in terms of cache["base"]. We want from base->target.
        # formula: amount * (rate_target / rate_base)
        rate_target = float(cache["rates"][target])
        rate_base = float(cache["rates"][base])
        rate = rate_target / rate_base
        converted = amount * rate
        meta = {
            "source": "cache",
            "timestamp": cache.get("timestamp") or cache.get("_fetched_at"),
            "warning": "Using cached cross rates due to network/API issue.",
        }
        return converted, rate, meta

    return None, None, {"error": "Rates unavailable for requested currencies."}


