from __future__ import annotations

import time
from typing import Dict, Generator, List, Optional, Tuple
from openai import OpenAI

from config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    TEMPERATURE,
    MAX_TOKENS,
    DEFAULT_TONE,
    DEFAULT_LANGUAGE,
    MAX_TURNS_PER_THREAD,
    KEYWORDS,
    BLACKLIST_CONTACTS,
)
from sources import Message


class ConversationMemory:
    def __init__(self) -> None:
        self.thread_id_to_messages: Dict[str, List[Dict[str, str]]] = {}

    def add(self, thread_id: str, role: str, content: str) -> None:
        messages = self.thread_id_to_messages.setdefault(thread_id, [])
        messages.append({"role": role, "content": content})
        if len(messages) > MAX_TURNS_PER_THREAD * 2:
            # Keep the last N exchanges (user+assistant pairs)
            self.thread_id_to_messages[thread_id] = messages[-MAX_TURNS_PER_THREAD * 2 :]

    def get(self, thread_id: str) -> List[Dict[str, str]]:
        return list(self.thread_id_to_messages.get(thread_id, []))


def build_system_prompt(tone: str, language: str) -> str:
    return (
        "You are AutoReplyBot, an email/chat auto-responder. "
        "Write concise, context-aware replies. "
        f"Tone: {tone}. "
        "Detect the user's language; if a preferred language is provided, use it strictly. "
        f"Preferred language: {language}. "
        "Guidelines:\n"
        "- Keep replies brief but helpful.\n"
        "- If the message is ambiguous, ask up to one clarifying question.\n"
        "- Preserve politeness and professionalism.\n"
        "- Include actionable next steps if relevant.\n"
        "- For email, include a greeting and sign-off. For chat, be lighter.\n"
        "- Never fabricate facts; if unsure, be transparent.\n"
    )


class AutoReplyBot:
    def __init__(self, api_key: Optional[str] = None) -> None:
        api_key_to_use = api_key or OPENAI_API_KEY
        if not api_key_to_use:
            raise ValueError("Missing OpenAI API key. Set OPENAI_API_KEY in .env.")
        self.client = OpenAI(api_key=api_key_to_use)
        self.model = OPENAI_MODEL
        self.temperature = TEMPERATURE
        self.max_tokens = MAX_TOKENS
        self.memory = ConversationMemory()

    def _should_skip(self, message: Message) -> Tuple[bool, str]:
        sender_lower = (message.sender or "").lower()
        if any(bad in sender_lower for bad in BLACKLIST_CONTACTS):
            return True, "Sender is blacklisted"
        if KEYWORDS:
            text = f"{message.subject} {message.content}".lower()
            if not any(kw.lower() in text for kw in KEYWORDS):
                return True, "No configured keywords matched"
        return False, ""

    def _build_messages(self, message: Message, tone: str, language: str) -> List[Dict[str, str]]:
        system_prompt = build_system_prompt(tone=tone, language=language)
        history = self.memory.get(message.thread_id)
        messages: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]
        if history:
            messages.extend(history[-MAX_TURNS_PER_THREAD * 2 :])
        user_content = (
            f"Channel: {message.channel}\n"
            f"Subject/Topic: {message.subject}\n"
            f"From: {message.sender} | To: {message.recipient}\n"
            f"Timestamp: {message.timestamp}\n\n"
            f"Message:\n{message.content}"
        )
        messages.append({"role": "user", "content": user_content})
        return messages

    def generate_reply(self, message: Message, tone: Optional[str] = None, language: Optional[str] = None) -> str:
        tone_to_use = tone or DEFAULT_TONE
        lang_to_use = language or DEFAULT_LANGUAGE
        prompt_messages = self._build_messages(message, tone=tone_to_use, language=lang_to_use)
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            messages=prompt_messages,
        )
        content = response.choices[0].message.content.strip()
        # Add to memory
        self.memory.add(message.thread_id, "user", prompt_messages[-1]["content"])
        self.memory.add(message.thread_id, "assistant", content)
        return content

    def stream_reply(self, message: Message, tone: Optional[str] = None, language: Optional[str] = None) -> Generator[str, None, str]:
        tone_to_use = tone or DEFAULT_TONE
        lang_to_use = language or DEFAULT_LANGUAGE
        prompt_messages = self._build_messages(message, tone=tone_to_use, language=lang_to_use)
        stream = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stream=True,
            messages=prompt_messages,
        )
        collected: List[str] = []
        for chunk in stream:
            try:
                delta = chunk.choices[0].delta if hasattr(chunk.choices[0], "delta") else {}
                content = getattr(delta, "content", None) if delta else None
                if content:
                    collected.append(content)
                    yield content
            except Exception:
                continue
        final_text = "".join(collected).strip()
        if final_text:
            self.memory.add(message.thread_id, "user", prompt_messages[-1]["content"])
            self.memory.add(message.thread_id, "assistant", final_text)
        return final_text

    def classify_for_auto_mode(self, message: Message) -> Tuple[bool, str]:
        skip, reason = self._should_skip(message)
        if skip:
            return False, reason
        return True, "Allowed"


