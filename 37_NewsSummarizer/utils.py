import os
from datetime import datetime
from typing import Optional


def ensure_directory(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def parse_date(date_str: Optional[str]) -> str:
    if not date_str:
        return datetime.utcnow().strftime("%Y-%m-%d")
    try:
        # Accept YYYY-MM-DD
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD.")
