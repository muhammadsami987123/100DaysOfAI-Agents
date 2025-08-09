from __future__ import annotations

import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional

from config import CONFIG


@dataclass
class LogRecord:
    timestamp: float
    event: str
    doc_id: Optional[str]
    question: Optional[str]
    answer_preview: Optional[str]
    citations: Optional[List[Dict[str, Any]]]
    meta: Dict[str, Any]


class JsonlLogger:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, record: LogRecord) -> None:
        line = json.dumps(asdict(record), ensure_ascii=False)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")


def log_chat(doc_id: str, question: str, answer: str, citations: List[Dict[str, Any]], extra: Dict[str, Any] | None = None) -> None:
    if not CONFIG.log_enabled:
        return
    logger = JsonlLogger(CONFIG.log_file)
    preview = (answer[:300] + ("…" if len(answer) > 300 else "")) if answer else ""
    rec = LogRecord(
        timestamp=time.time(),
        event="chat",
        doc_id=doc_id,
        question=question,
        answer_preview=preview,
        citations=citations,
        meta=extra or {},
    )
    logger.write(rec)
