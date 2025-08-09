from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional
import tiktoken

from config import CONFIG


@dataclass
class TextChunk:
    text: str
    page: Optional[int]
    chunk_index: int


class TokenTextSplitter:
    def __init__(self, chunk_size: int | None = None, chunk_overlap: int | None = None, model_name: str | None = None) -> None:
        self.chunk_size = chunk_size or CONFIG.chunk_size_tokens
        self.chunk_overlap = chunk_overlap or CONFIG.chunk_overlap_tokens
        model = model_name or CONFIG.openai_model
        try:
            self.tokenizer = tiktoken.encoding_for_model(model)
        except Exception:
            self.tokenizer = tiktoken.get_encoding('cl100k_base')

    def split_text(self, text: str, page: Optional[int] = None) -> List[TextChunk]:
        tokens = self.tokenizer.encode(text)
        chunks: List[TextChunk] = []
        start = 0
        idx = 0
        while start < len(tokens):
            end = start + self.chunk_size
            token_slice = tokens[start:end]
            chunk_text = self.tokenizer.decode(token_slice)
            chunks.append(TextChunk(text=chunk_text, page=page, chunk_index=idx))
            start = end - self.chunk_overlap
            if start < 0:
                start = 0
            idx += 1
            if end >= len(tokens):
                break
        return chunks

    def split_pages(self, pages: List[str]) -> List[TextChunk]:
        all_chunks: List[TextChunk] = []
        for page_num, page_text in enumerate(pages, start=1):
            page_chunks = self.split_text(page_text, page=page_num)
            all_chunks.extend(page_chunks)
        return all_chunks