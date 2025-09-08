import json
import os
import time
from typing import Any, Dict

try:
    from . import config  # type: ignore
except Exception:
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    import config  # type: ignore


def log_event(event: str, details: Dict[str, Any]) -> None:
    if not config.ENABLE_JSONL_LOG:
        return
    os.makedirs(os.path.dirname(config.LOG_FILE), exist_ok=True)
    record = {
        "ts": time.time(),
        "event": event,
        **details,
    }
    try:
        with open(config.LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:
        pass


