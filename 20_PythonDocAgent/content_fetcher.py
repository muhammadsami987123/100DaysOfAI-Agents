from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup


CODE_BLOCK_RE = re.compile(r"```([a-zA-Z0-9_+-]*)\n([\s\S]*?)```", re.MULTILINE)


@dataclass
class FetchedContent:
    source: str  # 'url' | 'file' | 'inline'
    title: str
    text: str
    url: Optional[str] = None
    path: Optional[Path] = None


def fetch_from_url(url: str) -> FetchedContent:
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    html = resp.text
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else url

    # Prefer main/article/content blocks; fallback to visible text
    main = soup.find(["main", "article"]) or soup
    for block in main.find_all(["script", "style", "noscript"]):
        block.decompose()
    text = main.get_text("\n", strip=True)

    return FetchedContent(source="url", title=title, text=text, url=url)


def read_file(path: str | Path, encoding: str = "utf-8") -> FetchedContent:
    p = Path(path)
    text = p.read_text(encoding=encoding, errors="replace")
    title = p.name
    return FetchedContent(source="file", title=title, text=text, path=p)


def normalize_inline(label: str, text: str) -> FetchedContent:
    title = label or "Inline Snippet"
    return FetchedContent(source="inline", title=title, text=text)


def extract_code_blocks(markdown_text: str) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    for lang, body in CODE_BLOCK_RE.findall(markdown_text):
        blocks.append((lang or "", body.strip()))
    return blocks


