from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

from rapidfuzz import fuzz, process

from config import CONFIG


@dataclass
class FAQ:
    id: str
    question: str
    answer: str
    aliases: List[str]


class FAQMatcher:
    def __init__(self, faqs_path: Optional[str] = None, threshold: int = 70) -> None:
        self.faqs_path = Path(faqs_path or CONFIG.faqs_path)
        self.threshold = threshold
        self.faqs: List[FAQ] = []
        self._load()

    def _load(self) -> None:
        if not self.faqs_path.exists():
            self.faqs = []
            return
        data = json.loads(self.faqs_path.read_text(encoding="utf-8"))
        self.faqs = []
        for idx, item in enumerate(data):
            faq = FAQ(
                id=str(item.get("id", idx + 1)),
                question=item.get("question", "").strip(),
                answer=item.get("answer", "").strip(),
                aliases=[a.strip() for a in item.get("aliases", []) if isinstance(a, str)],
            )
            self.faqs.append(faq)

    def best_match(self, query: str) -> Tuple[Optional[FAQ], int, str]:
        if not query.strip() or not self.faqs:
            return None, 0, ""
        # Build corpus: include question + aliases
        candidates: List[Tuple[str, FAQ]] = []
        for faq in self.faqs:
            candidates.append((faq.question, faq))
            for alias in faq.aliases:
                candidates.append((alias, faq))

        choices = [c[0] for c in candidates]
        match, score, idx = process.extractOne(
            query,
            choices,
            scorer=fuzz.WRatio,
        )
        if match is None:
            return None, 0, ""
        matched_faq = candidates[idx][1]
        if score < self.threshold:
            return None, score, match
        return matched_faq, int(score), match


