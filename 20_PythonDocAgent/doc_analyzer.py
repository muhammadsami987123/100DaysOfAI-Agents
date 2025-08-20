from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from config import get_language_config


SYSTEM_PROMPT = (
    "You are PythonDocAgent, an expert Python educator and code reviewer. "
    "Given Python code or technical documentation, you: "
    "1) explain functions, classes, decorators, loops, and complex logic, "
    "2) detect bugs, edge cases, and suggest best practices, "
    "3) produce section-wise summaries for long inputs, "
    "4) respond in the user's requested language (English/Hindi/Urdu), "
    "5) return concise, high-signal answers with syntax-highlighted code fences."
)


@dataclass
class ConversationMemory:
    max_turns: int
    turns: List[dict] = field(default_factory=list)

    def add(self, role: str, content: str) -> None:
        self.turns.append({"role": role, "content": content})
        if len(self.turns) > self.max_turns:
            overflow = len(self.turns) - self.max_turns
            self.turns = self.turns[overflow:]

    def to_messages(self) -> List[dict]:
        return list(self.turns)


def build_explain_prompt(language: str, content_title: str, text: str) -> str:
    l = get_language_config(language)
    return (
        f"{l['explain']}\n\n"
        f"Content Title: {content_title}\n\n"
        "Please:\n"
        "- Explain key functions/classes/decorators\n"
        "- Describe loops and complex control flow\n"
        "- Identify potential bugs and risky patterns\n"
        "- Suggest Pythonic improvements and best practices\n"
        "- Provide concise examples in code fences where helpful\n\n"
        "Content:\n" + text
    )


def build_summary_prompt(language: str, content_title: str, text: str) -> str:
    l = get_language_config(language)
    return (
        f"{l['summarize']}\n\n"
        f"Content Title: {content_title}\n\n"
        "Create a section-wise summary with headings. Include:\n"
        "- Overview\n- Key Components\n- Important APIs or Functions\n- Best Practices/Notes\n\n"
        "Content:\n" + text
    )


def build_walkthrough_prompt(language: str, content_title: str, text: str, line_from: int, line_to: int) -> str:
    l = get_language_config(language)
    return (
        f"{l['walkthrough']}\n\n"
        f"Content Title: {content_title}\n"
        f"Focus Lines: {line_from}-{line_to}\n\n"
        "Explain line-by-line in concise bullet points.\n\n"
        "Content:\n" + text
    )


