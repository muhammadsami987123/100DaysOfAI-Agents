from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import List, Dict, Tuple
import numpy as np

from config import DOCS_DIR
from text_splitter import TextChunk
from openai_service import OpenAIService


@dataclass
class VectorMetadata:
    page: int | None
    chunk_index: int


class SimpleVectorStore:
    def __init__(self, doc_id: str, service: OpenAIService) -> None:
        self.doc_id = doc_id
        self.service = service
        self.dir = DOCS_DIR / doc_id
        self.dir.mkdir(parents=True, exist_ok=True)
        self._embeddings_path = self.dir / "embeddings.npy"
        self._chunks_path = self.dir / "chunks.jsonl"
        self._meta_path = self.dir / "meta.json"
        self._embeddings: np.ndarray | None = None
        self._chunks: List[str] | None = None
        self._metadatas: List[VectorMetadata] | None = None

    def persist(self, title: str, source: str, media_type: str, chunks: List[TextChunk]) -> None:
        texts = [c.text for c in chunks]
        embeddings = self.service.embed_texts(texts)
        arr = np.array(embeddings, dtype=np.float32)
        np.save(self._embeddings_path, arr)
        self._embeddings = arr

        with self._chunks_path.open("w", encoding="utf-8") as f:
            for c in chunks:
                f.write(json.dumps({"text": c.text}) + "\n")
        self._chunks = texts

        metadatas = [VectorMetadata(page=c.page, chunk_index=c.chunk_index) for c in chunks]
        self._metadatas = metadatas
        meta = {
            "title": title,
            "source": source,
            "media_type": media_type,
            "num_chunks": len(chunks),
        }
        meta_with_chunks = meta | {"metadatas": [asdict(m) for m in metadatas]}
        self._meta_path.write_text(json.dumps(meta_with_chunks, ensure_ascii=False, indent=2), encoding="utf-8")

    def load(self) -> None:
        if self._embeddings is None and self._embeddings_path.exists():
            self._embeddings = np.load(self._embeddings_path)
        if self._chunks is None and self._chunks_path.exists():
            texts: List[str] = []
            with self._chunks_path.open("r", encoding="utf-8") as f:
                for line in f:
                    obj = json.loads(line)
                    texts.append(obj["text"])
            self._chunks = texts
        if self._metadatas is None and self._meta_path.exists():
            meta = json.loads(self._meta_path.read_text(encoding="utf-8"))
            self._metadatas = [VectorMetadata(**m) for m in meta.get("metadatas", [])]

    def is_ready(self) -> bool:
        return self._embeddings_path.exists() and self._chunks_path.exists() and self._meta_path.exists()

    def top_k(self, query: str, k: int = 6) -> List[Tuple[int, float]]:
        self.load()
        assert self._embeddings is not None and self._chunks is not None
        query_emb = np.array(self.service.embed_texts([query])[0], dtype=np.float32)
        doc_emb = self._embeddings
        # cosine similarity
        dot = doc_emb @ query_emb
        norms = np.linalg.norm(doc_emb, axis=1) * (np.linalg.norm(query_emb) + 1e-8)
        sims = dot / (norms + 1e-8)
        idxs = np.argsort(-sims)[:k]
        return [(int(i), float(sims[int(i)])) for i in idxs]

    def get_chunk(self, idx: int) -> str:
        assert self._chunks is not None
        return self._chunks[idx]

    def get_metadata(self, idx: int) -> VectorMetadata:
        assert self._metadatas is not None
        return self._metadatas[idx]

    def get_doc_meta(self) -> Dict:
        if self._meta_path.exists():
            return json.loads(self._meta_path.read_text(encoding="utf-8"))
        return {}
