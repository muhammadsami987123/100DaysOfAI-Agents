import platform
import openai
from typing import Dict, Optional, Tuple

from config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    TEMPERATURE,
    MAX_TOKENS,
    MAX_HISTORY_MESSAGES,
    DEFAULT_SHELL,
    SAFETY_MODE,
)


def detect_os() -> Dict[str, str]:
    system = platform.system()
    if system == "Windows":
        return {"id": "windows", "name": "Windows", "shell": "powershell"}
    if system == "Darwin":
        return {"id": "macos", "name": "macOS", "shell": "bash"}
    if system == "Linux":
        return {"id": "linux", "name": "Linux", "shell": "bash"}
    return {"id": system.lower() or "unknown", "name": system or "Unknown", "shell": DEFAULT_SHELL}


class TerminalGPT:
    def __init__(self, api_key: Optional[str] = None) -> None:
        api_key_to_use = api_key or OPENAI_API_KEY
        if not api_key_to_use:
            raise ValueError("Missing OpenAI API key. Set OPENAI_API_KEY in .env.")
        openai.api_key = api_key_to_use
        self.model = OPENAI_MODEL
        self.temperature = TEMPERATURE
        self.max_tokens = MAX_TOKENS
        self.safety_mode = SAFETY_MODE
        # Keep a short rolling memory of the session
        self._history: list[dict] = []

    def _build_system_prompt(self, os_profile: Dict[str, str]) -> str:
        os_id = os_profile.get("id", "windows")
        os_name = os_profile.get("name", "Windows")
        shell = os_profile.get("shell", "bash")

        return (
            "You are TerminalGPT, an intelligent command-line assistant. "
            "Convert natural language instructions into safe, executable terminal commands. "
            "Always respond in the same language as the user's input. "
            f"Target OS: {os_name} with {shell} shell. "
            "Provide output using these labeled sections strictly in order:\n"
            "1) Command\n"
            "2) Explanation\n"
            "3) Safety Warning\n"
            "4) Notes\n"
            "Format the command in a code block. "
            "For safety warnings, use 'Yes' if risky, 'No' if safe, plus brief reason. "
            "Prefer safe alternatives (e.g., -i flag for rm, --dry-run for destructive operations). "
            "Keep explanations concise but clear. "
            "If the request is ambiguous, ask for clarification first."
        )

    def ask(self, user_message: str, os_profile: Optional[Dict[str, str]] = None) -> str:
        os_prof = os_profile or detect_os()
        system_prompt = self._build_system_prompt(os_prof)

        # Build messages including short-term history
        messages = [{"role": "system", "content": system_prompt}]
        # include last N exchanges from history
        if self._history:
            messages.extend(self._history[-MAX_HISTORY_MESSAGES:])
        messages.append({"role": "user", "content": user_message})

        response = openai.ChatCompletion.create(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            messages=messages,
        )
        content = response["choices"][0]["message"]["content"].strip()
        # Save to history
        self._history.extend([
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": content},
        ])
        return content

    def stream(self, user_message: str, os_profile: Optional[Dict[str, str]] = None):
        """Yield content chunks as they arrive from OpenAI for a smoother CLI loader."""
        os_prof = os_profile or detect_os()
        system_prompt = self._build_system_prompt(os_prof)

        # Build messages including short-term history
        messages = [{"role": "system", "content": system_prompt}]
        if self._history:
            messages.extend(self._history[-MAX_HISTORY_MESSAGES:])
        messages.append({"role": "user", "content": user_message})

        stream = openai.ChatCompletion.create(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stream=True,
            messages=messages,
        )
        collected: list[str] = []
        for chunk in stream:
            try:
                delta = chunk["choices"][0].get("delta", {})
                content = delta.get("content")
                if content:
                    collected.append(content)
                    yield content
            except Exception:
                # Ignore malformed chunks; continue streaming
                continue
        # Save to history at the end
        if collected:
            assistant_text = "".join(collected).strip()
            self._history.extend([
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": assistant_text},
            ])
