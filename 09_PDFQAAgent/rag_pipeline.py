from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any, Optional

from config import CONFIG
from openai_service import OpenAIService
from text_splitter import TokenTextSplitter, TextChunk
from vector_store import SimpleVectorStore


SYSTEM_PROMPT = (
    "You are PDFQAAgent. Answer the user's question strictly using the provided context snippets from the document. "
    "If the answer is not present in the snippets, say 'I don't know based on the provided document.' Do not use outside knowledge. "
    "Cite sources by listing the page numbers and short quotes used. Keep answers concise and accurate."
)


@dataclass
class RetrievedContext:
    text: str
    score: float
    page: int | None
    chunk_index: int


class RAGPipeline:
    def __init__(self, service: OpenAIService) -> None:
        self.service = service
        self.splitter = TokenTextSplitter()

    def build_store(self, doc_id: str, title: str, source: str, media_type: str, pages: List[str]) -> SimpleVectorStore:
        chunks: List[TextChunk] = self.splitter.split_pages(pages)
        store = SimpleVectorStore(doc_id, self.service)
        store.persist(title=title, source=source, media_type=media_type, chunks=chunks)
        return store

    def retrieve(self, store: SimpleVectorStore, question: str, k: int | None = None) -> List[RetrievedContext]:
        k = k or CONFIG.top_k
        top = store.top_k(question, k)
        retrieved: List[RetrievedContext] = []
        for idx, score in top:
            text = store.get_chunk(idx)
            meta = store.get_metadata(idx)
            retrieved.append(RetrievedContext(text=text, score=score, page=meta.page, chunk_index=meta.chunk_index))
        return retrieved

    def build_messages(
        self,
        question: str,
        contexts: List[RetrievedContext],
        history: Optional[List[Dict[str, str]]] = None,
    ) -> List[Dict[str, str]]:
        # Prepare conversation summary (recent N turns) without breaking grounding
        conversation_summary = ""
        if history:
            last_turns = history[-6:]
            lines: List[str] = []
            for turn in last_turns:
                q = (turn.get("question") or "").strip()
                a = (turn.get("answer") or "").strip()
                if q:
                    lines.append(f"Q: {q}")
                if a:
                    lines.append(f"A: {a}")
            conversation_summary = "\n".join(lines)

        # Truncate contexts to fit within token budget
        context_blocks: List[str] = []
        total_tokens = 0
        for rc in contexts:
            snippet = rc.text.strip()
            tokens = self.service.count_tokens(snippet)
            if total_tokens + tokens > CONFIG.max_context_tokens:
                break
            header = f"[Page {rc.page if rc.page is not None else '-'}, Chunk {rc.chunk_index}]\n"
            context_blocks.append(header + snippet)
            total_tokens += tokens
        context_text = "\n\n".join(context_blocks)

        user_content_parts: List[str] = []
        if conversation_summary:
            user_content_parts.append("Previous conversation (for context only):\n" + conversation_summary)
        user_content_parts.append("Context:\n\n" + context_text)
        user_content_parts.append("Question: " + question)

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "\n\n".join(user_content_parts)},
        ]
        return messages

    def answer(self, store: SimpleVectorStore, question: str, history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        contexts = self.retrieve(store, question)
        messages = self.build_messages(question, contexts, history)
        answer = self.service.chat_completion(messages)
        citations = [
            {
                "page": rc.page,
                "chunk_index": rc.chunk_index,
                "score": rc.score,
                "preview": (rc.text[:200] + ("…" if len(rc.text) > 200 else "")),
            }
            for rc in contexts
        ]
        return {"answer": answer, "citations": citations}
