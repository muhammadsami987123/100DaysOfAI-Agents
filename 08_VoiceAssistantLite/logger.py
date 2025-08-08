from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from config import CONFIG


@dataclass
class QALogEntry:
    timestamp: str
    input_text: str
    matched_question: str
    matched_score: int
    answer: str
    stt_provider: str
    language_used: str


class QALogger:
    def __init__(self) -> None:
        self.enabled = CONFIG.log_enabled
        self.format = CONFIG.log_format
        self.path = Path(CONFIG.log_file)
        self.path.parent.mkdir(parents=True, exist_ok=True)

        if self.format == "csv" and not self.path.exists():
            # Create CSV with header
            with self.path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=[
                        "timestamp",
                        "input_text",
                        "matched_question",
                        "matched_score",
                        "answer",
                        "stt_provider",
                        "language_used",
                    ],
                )
                writer.writeheader()

    def log(self, entry: QALogEntry) -> None:
        if not self.enabled:
            return
        if self.format == "csv":
            self._log_csv(entry)
        else:
            self._log_jsonl(entry)

    def _log_jsonl(self, entry: QALogEntry) -> None:
        record: Dict[str, Any] = {
            "timestamp": entry.timestamp,
            "input_text": entry.input_text,
            "matched_question": entry.matched_question,
            "matched_score": entry.matched_score,
            "answer": entry.answer,
            "stt_provider": entry.stt_provider,
            "language_used": entry.language_used,
        }
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def _log_csv(self, entry: QALogEntry) -> None:
        with self.path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                entry.timestamp,
                entry.input_text,
                entry.matched_question,
                entry.matched_score,
                entry.answer,
                entry.stt_provider,
                entry.language_used,
            ])


def make_log_entry(
    input_text: str,
    matched_question: str,
    matched_score: int,
    answer: str,
    language_used: str,
) -> QALogEntry:
    return QALogEntry(
        timestamp=datetime.utcnow().isoformat(timespec="seconds") + "Z",
        input_text=input_text,
        matched_question=matched_question,
        matched_score=int(matched_score),
        answer=answer,
        stt_provider=CONFIG.stt_provider,
        language_used=language_used,
    )


