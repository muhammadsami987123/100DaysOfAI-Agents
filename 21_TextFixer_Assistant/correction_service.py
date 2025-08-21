from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

import requests

from config import CONFIG


class CorrectionProvider(ABC):
    @abstractmethod
    def correct(self, text: str, language: Optional[str] = None, style: Optional[str] = None) -> str:
        raise NotImplementedError


class LanguageToolProvider(CorrectionProvider):
    def __init__(self) -> None:
        try:
            import language_tool_python  # type: ignore
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(
                "language-tool-python is required for LanguageTool provider. Add it to requirements.txt"
            ) from exc
        # Use public API (no local Java server)
        self._lt = language_tool_python.LanguageToolPublicAPI(
            language=CONFIG.language if CONFIG.language else "auto"
        )

    def correct(self, text: str, language: Optional[str] = None, style: Optional[str] = None) -> str:
        # language_tool_python applies corrections and returns the corrected string
        # Style variants are not directly supported; rely on level="picky" improvements.
        return self._lt.correct(text)


class OpenAIProvider(CorrectionProvider):
    def __init__(self) -> None:
        try:
            from openai import OpenAI  # type: ignore
        except Exception as exc:  # pragma: no cover
            raise RuntimeError("openai package is required for OpenAI provider.") from exc
        if not CONFIG.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is required for OpenAI provider.")
        self._client = OpenAI()
        self._model = CONFIG.openai_model

    def correct(self, text: str, language: Optional[str] = None, style: Optional[str] = None) -> str:
        lang = (language or CONFIG.language or "auto").strip()
        tone = (style or CONFIG.style or "neutral").strip()
        system_prompt = (
            "You are TextFixer, a precise text-correction assistant. "
            "Correct grammar, spelling, punctuation, and basic style while preserving meaning. "
            "Prefer concise, natural phrasing. If the input contains multiple sentences, correct them all. "
            "If the language is specified, use it; otherwise detect automatically. "
            "Style preference: {tone}. Return only the corrected text with no quotes or extra commentary."
        ).format(tone=tone)
        user_prompt = f"Language: {lang}. Style: {tone}.\nCorrect this text:\n{text}"
        completion = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.1,
        )
        response_text = completion.choices[0].message.content or ""
        return response_text.strip()


def get_correction_provider() -> CorrectionProvider:
    provider = (CONFIG.provider or "languagetool").strip().lower()
    if provider == "openai":
        return OpenAIProvider()
    if provider == "languagetool":
        return LanguageToolProvider()
    raise ValueError(f"Unknown provider: {provider}")


