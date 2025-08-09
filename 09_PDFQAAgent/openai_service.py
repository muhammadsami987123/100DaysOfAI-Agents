from __future__ import annotations

from typing import List, Dict, Any
from openai import OpenAI
import tiktoken

from config import CONFIG


class OpenAIService:
    def __init__(self) -> None:
        if not CONFIG.openai_api_key:
            raise RuntimeError('OPENAI_API_KEY is not set in environment or .env')
        self.client = OpenAI()
        try:
            self.tokenizer = tiktoken.encoding_for_model(CONFIG.openai_model)
        except Exception:
            self.tokenizer = tiktoken.get_encoding('cl100k_base')

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        response = self.client.embeddings.create(
            model=CONFIG.embedding_model,
            input=texts,
        )
        return [d.embedding for d in response.data]

    def count_tokens(self, text: str) -> int:
        return len(self.tokenizer.encode(text))

    def chat_completion(self, messages: List[Dict[str, str]], temperature: float = 0.0) -> str:
        completion = self.client.chat.completions.create(
            model=CONFIG.openai_model,
            messages=messages,
            temperature=temperature,
        )
        return completion.choices[0].message.content or ''