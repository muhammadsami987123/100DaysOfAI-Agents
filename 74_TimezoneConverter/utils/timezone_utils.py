import pytz
from datetime import datetime

_ABBR_MAP = {
    # Common North America
    "pst": "America/Los_Angeles",
    "pdt": "America/Los_Angeles",
    "est": "America/New_York",
    "edt": "America/New_York",
    "cst": "America/Chicago",
    "cdt": "America/Chicago",
    "mst": "America/Denver",
    "mdt": "America/Denver",
    # Global
    "utc": "UTC",
    "gmt": "Etc/GMT",
    "cet": "Europe/Berlin",
    "cest": "Europe/Berlin",
    "ist": "Asia/Kolkata",  # India Standard Time (non-DST)
    "bst": "Europe/London",
    "jst": "Asia/Tokyo",
    "kst": "Asia/Seoul",
    "sgt": "Asia/Singapore",
    "hkt": "Asia/Hong_Kong",
    "aest": "Australia/Sydney",
    "aedt": "Australia/Sydney",
}

_LOCATION_MAP = {
    "new york": "America/New_York",
    "nyc": "America/New_York",
    "los angeles": "America/Los_Angeles",
    "la": "America/Los_Angeles",
    "san francisco": "America/Los_Angeles",
    "chicago": "America/Chicago",
    "london": "Europe/London",
    "berlin": "Europe/Berlin",
    "paris": "Europe/Paris",
    "dubai": "Asia/Dubai",
    "tokyo": "Asia/Tokyo",
    "seoul": "Asia/Seoul",
    "singapore": "Asia/Singapore",
    "hong kong": "Asia/Hong_Kong",
    "sydney": "Australia/Sydney",
    "melbourne": "Australia/Melbourne",
    "india": "Asia/Kolkata",
}

# Mapping/abbreviation logic can be expanded
def resolve_timezone_name(name: str) -> str:
    """Best effort: map user input to IANA/Olson timezone."""
    if not name:
        return None
    key = name.strip().lower()
    # direct maps
    if key in _ABBR_MAP:
        return _ABBR_MAP[key]
    if key in _LOCATION_MAP:
        return _LOCATION_MAP[key]
    # try punct/space normalization
    key2 = key.replace('_', ' ').replace('-', ' ').strip()
    if key2 in _LOCATION_MAP:
        return _LOCATION_MAP[key2]
    # already a valid tz?
    try:
        if name in pytz.all_timezones:
            return name
    except Exception:
        pass
    return None

def is_dst(dt: datetime, tz: str) -> bool:
    """Returns True if date/time is DST in given timezone, else False."""
    try:
        tz_info = pytz.timezone(tz)
        return bool(tz_info.localize(dt, is_dst=None).dst())
    except Exception:
        return False

def get_timezone_info(tz: str) -> dict:
    """Returns formatted info for a timezone."""
    try:
        tz_obj = pytz.timezone(tz)
        now = datetime.now(tz_obj)
        return {
            "zone": tz,
            "long_name": tz_obj.tzname(now),
            "offset": str(tz_obj.utcoffset(now) or "")
        }
    except Exception:
        return {"zone": tz, "error": "Invalid timezone"}
