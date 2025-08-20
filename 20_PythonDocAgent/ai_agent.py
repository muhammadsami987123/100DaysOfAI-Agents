from __future__ import annotations

"""
OpenAI client wrapper for PythonDocAgent.
Provides streaming and non-streaming generation helpers.
"""

from typing import Generator, Optional

from openai import OpenAI

from config import load_settings


class OpenAIClient:
	def __init__(self) -> None:
		self.settings = load_settings()
		self.client = OpenAI(api_key=self.settings.openai_api_key)

	def stream_chat(self, system_prompt: str, messages: list[dict], temperature: Optional[float] = None) -> Generator[str, None, None]:
		temperature = self.settings.temperature if temperature is None else temperature
		stream = self.client.chat.completions.create(
			model=self.settings.openai_model,
			messages=[{"role": "system", "content": system_prompt}] + messages,
			temperature=temperature,
			max_tokens=self.settings.max_tokens,
			stream=True,
		)
		for chunk in stream:
			try:
				delta = chunk.choices[0].delta
				if delta and getattr(delta, "content", None):
					yield delta.content
			except Exception:
				continue

	def complete_chat(self, system_prompt: str, messages: list[dict], temperature: Optional[float] = None) -> str:
		temperature = self.settings.temperature if temperature is None else temperature
		resp = self.client.chat.completions.create(
			model=self.settings.openai_model,
			messages=[{"role": "system", "content": system_prompt}] + messages,
			temperature=temperature,
			max_tokens=self.settings.max_tokens,
			stream=False,
		)
		return resp.choices[0].message.content or ""


