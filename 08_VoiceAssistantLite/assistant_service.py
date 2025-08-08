from __future__ import annotations

import time
from typing import Optional

from openai import OpenAI

from config import CONFIG


class AssistantService:
    def __init__(self) -> None:
        if not hasattr(CONFIG, "openai_api_key"):
            # Backward compat: attribute added later
            pass
        self.client = OpenAI()
        self.assistant_id = CONFIG.assistant_id
        if not self.assistant_id:
            # Create a lightweight assistant if one isn't provided
            instructions = CONFIG.assistant_instructions
            assistant = self.client.beta.assistants.create(
                name="VoiceAssistantLite",
                instructions=instructions,
                model=CONFIG.openai_model,
                tools=[],
            )
            self.assistant_id = assistant.id

    def ask(self, text: str, timeout_seconds: float = 30.0) -> str:
        thread = self.client.beta.threads.create()
        self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=text,
        )
        run = self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant_id,
        )

        # Poll for completion
        start = time.time()
        while True:
            current = self.client.beta.threads.runs.retrieve(
                thread_id=thread.id, run_id=run.id
            )
            if current.status in {"completed", "requires_action", "failed", "cancelled", "expired"}:
                break
            if time.time() - start > timeout_seconds:
                break
            time.sleep(0.5)

        if current.status != "completed":
            return "Sorry, I could not complete the request right now. Please try again."

        messages = self.client.beta.threads.messages.list(
            thread_id=thread.id, order="desc", limit=5
        )
        for m in messages.data:
            if m.role == "assistant":
                # Extract text parts only
                parts = []
                for c in m.content:
                    if c.type == "text":
                        parts.append(c.text.value)
                if parts:
                    return "\n\n".join(parts).strip()
        return ""


