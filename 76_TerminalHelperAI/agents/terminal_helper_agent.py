import platform
import openai
import os # Added for Gemini client
import google.generativeai as genai # Added for Gemini client
from typing import Dict, Optional
from config import (
    Config
)

class TerminalHelperAgent:
    def __init__(self, api_key: Optional[str] = None) -> None:
        self.openai_client = None
        self.gemini_model = None
        self.model_choice = Config.LLM_MODEL

        self.temperature = Config.TEMPERATURE
        self.max_tokens = Config.MAX_TOKENS
        self.safety_mode = Config.SAFETY_MODE
        self._history: list[dict] = []

        # Removed: self.system_instruction = self._build_system_prompt_content(Config.OS_PROFILE)

        self._init_clients(api_key)

    def _init_clients(self, api_key: Optional[str]) -> None:
        # Initialize OpenAI client
        if Config.OPENAI_API_KEY:
            try:
                self.openai_client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
                print("✅ OpenAI client initialized.")
            except Exception as e:
                print(f"❌ Error initializing OpenAI client: {e}")
                self.openai_client = None
        
        # Initialize Gemini client
        if Config.GEMINI_API_KEY:
            try:
                genai.configure(api_key=Config.GEMINI_API_KEY)
                self.gemini_model = genai.GenerativeModel(Config.GEMINI_MODEL)
                print("✅ Gemini client initialized.")
            except Exception as e:
                print(f"❌ Error initializing Gemini client: {e}")
                self.gemini_model = None
        
        if not self.openai_client and not self.gemini_model:
            raise ValueError("No valid API clients initialized. Set OPENAI_API_KEY or GEMINI_API_KEY in .env.")

    def _build_system_prompt_content(self, os_profile: Dict[str, str]) -> str:
        os_name = os_profile.get("name", "Windows")
        shell = os_profile.get("shell", Config.DEFAULT_SHELL)

        safety_instruction = """
Warn users before giving any potentially dangerous command (e.g., deleting files). 
Don’t provide any command that: Erases files (rm -rf /), Alters system boot (dd, mkfs), Uses sudo without explanation. Unless explicitly requested, and with a clear safety warning.
Prefer safe alternatives (e.g., -i flag for rm, --dry-run for destructive operations).
        """ if self.safety_mode else ""

        return (
            "You are TerminalHelperAI, a command-line assistant trained to help users learn, explore, and generate terminal commands interactively. "
            "Your role is to make the command-line experience easy and beginner-friendly, while also powerful for advanced users.\n\n"
            "Your Responsibilities:\n"
            "1. Understand the user’s environment\n"
            f"   Assume the user's OS is {os_name} and their preferred shell is {shell}. Tailor commands for that OS and shell.\n"
            "2. Command Generation + Explanation\n"
            "   - Generate the correct terminal command for the user's request.\n"
            "   - Provide a short and clear explanation for what the command does.\n"
            "   - Break down flags and options used in the command (educational-style).\n"
            f"   {safety_instruction}"
            "3. Structured Output\n"
            "   Provide output using these labeled sections strictly in order: \n"
            "   1) Command\n"
            "   2) Explanation\n"
            "   3) Safety Warning (if applicable, state 'No' if safe)\n"
            "   4) Notes (optional, for bonus features like aliases, best practices, error explanation)\n"
            "   If the question is ambiguous, ask a single brief clarification first; otherwise proceed.\n"
            "   Always detect the user's language from their message and respond in that language (English, Urdu, or Hindi preferred)."
        )

    def stream(self, user_message: str, os_profile: Dict[str, str]):
        # Dynamically build system prompt for each call to ensure OS profile is up-to-date
        system_prompt_content = self._build_system_prompt_content(os_profile)

        # For Gemini, system instruction is included in the first user message
        gemini_messages = []
        # Prepend system prompt to the first user message
        initial_gemini_user_content = f"{system_prompt_content}\n\nUser Request: {user_message}"
        gemini_messages.append({"role": "user", "parts": [initial_gemini_user_content]})
        
        # Add history, mapping roles for Gemini
        for entry in self._history[-Config.MAX_HISTORY_MESSAGES:]:
            if entry["role"] == "user":
                gemini_messages.append({"role": "user", "parts": [entry["content"]]})
            elif entry["role"] == "assistant":
                gemini_messages.append({"role": "model", "parts": [entry["content"]]})

        # Prepare messages for OpenAI
        openai_messages = [
            {"role": "system", "content": system_prompt_content}
        ]
        if self._history:
            openai_messages.extend(self._history[-Config.MAX_HISTORY_MESSAGES:])
        openai_messages.append({"role": "user", "content": user_message})

        collected: list[str] = []
        stream = None

        # Try primary model first
        if self.model_choice == "gemini" and self.gemini_model:
            try:
                # Gemini expects messages with system instruction integrated into the first user message
                stream = self.gemini_model.generate_content(gemini_messages, stream=True)
            except Exception as e:
                print(f"Warning: Gemini stream failed: {e}. Falling back to OpenAI.")
                stream = None
        
        if not stream and self.openai_client:
            try:
                stream = self.openai_client.chat.completions.create(
                    model=Config.OPENAI_MODEL, 
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    stream=True,
                    messages=openai_messages, 
                )
            except Exception as e:
                print(f"Warning: OpenAI stream failed: {e}. No fallback available.")
                stream = None
        
        if not stream:
            yield "Error: No AI model available or all models failed to generate a response."
            return

        for chunk in stream:
            try:
                if self.model_choice == "gemini": 
                    content = chunk.text
                else: 
                    delta = chunk.choices[0].delta
                    content = delta.content
                
                if content:
                    collected.append(content)
                    yield content
            except Exception:
                continue
        
        if collected:
            self._history.extend([
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": "".join(collected).strip()},
            ])
