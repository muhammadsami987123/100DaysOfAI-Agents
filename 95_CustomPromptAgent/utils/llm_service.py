import os
import json
from typing import Dict, Any
from config import Config

try:
    import google.generativeai as genai
    HAS_GENAI = True
except Exception:
    genai = None
    HAS_GENAI = False

try:
    from openai import OpenAI
    HAS_OPENAI = True
except Exception:
    OpenAI = None
    HAS_OPENAI = False


class LLMService:
    """Simple LLM wrapper that attempts to use Gemini by default and OpenAI as optional.

    If neither is configured, generate_content will return a fallback mock response.
    """

    def __init__(self):
        self.current_llm = Config.DEFAULT_LLM
        self.gemini_client = None
        self.openai_client = None
        self._init_clients()

    def _init_clients(self):
        if HAS_GENAI and Config.GEMINI_API_KEY:
            try:
                genai.configure(api_key=Config.GEMINI_API_KEY)
                self.gemini_client = genai.GenerativeModel(Config.GEMINI_MODEL)
            except Exception as e:
                print(f"Failed to initialize Gemini client: {e}")
                self.gemini_client = None
        else:
            if not HAS_GENAI:
                print("google.generativeai package not available; Gemini client disabled")
            else:
                print("GEMINI_API_KEY not set; Gemini client not initialized")

        if HAS_OPENAI and Config.OPENAI_API_KEY:
            try:
                self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
            except Exception as e:
                print(f"Failed to initialize OpenAI client: {e}")
                self.openai_client = None
        else:
            if not HAS_OPENAI:
                print("openai package not available; OpenAI client disabled")
            else:
                print("OPENAI_API_KEY not set; OpenAI client not initialized")

    def set_llm(self, llm_choice: str) -> None:
        if llm_choice in ("gemini", "openai"):
            self.current_llm = llm_choice
        else:
            print(f"Unknown llm choice {llm_choice}, keeping {self.current_llm}")

    def _read_template(self, template_name: str) -> str:
        template_path = os.path.join(os.path.dirname(__file__), "..", "prompts", template_name)
        try:
            with open(template_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""

    def generate_content(self, prompt: str) -> Dict[str, Any]:
        """Try to generate content using the selected LLM; fall back gracefully.

        Returns a dict with keys: summary (str), message (str)
        """
        try:
            if self.current_llm == "gemini" and self.gemini_client:
                response = self.gemini_client.generate_content(prompt)
                text = getattr(response, "text", str(response))
                return self._parse_text_response(text)

            if self.current_llm == "openai" and self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model=Config.OPENAI_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                )
                text = response.choices[0].message.content
                return self._parse_text_response(text)

            # Fallback: if Gemini requested but not available, try OpenAI client
            if self.current_llm == "gemini" and self.openai_client:
                print("Gemini unavailable, falling back to OpenAI")
                response = self.openai_client.chat.completions.create(
                    model=Config.OPENAI_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                )
                text = response.choices[0].message.content
                return self._parse_text_response(text)

            # No LLM available: return a simple generated result
            print("No LLM client available, returning fallback response")
            return {"summary": prompt[:100] + "...", "message": "Try setting OPENAI_API_KEY or GEMINI_API_KEY for richer results."}

        except Exception as e:
            print(f"Error generating content: {e}")
            return {"summary": f"Error generating content: {e}", "message": ""}

    def _parse_text_response(self, text: str) -> Dict[str, Any]:
        """Naive parsing: try to extract JSON object, else return text as summary."""
        cleaned = text.strip()
        # Try to find JSON substring
        try:
            start = cleaned.find("{")
            end = cleaned.rfind("}")
            if start != -1 and end != -1 and end > start:
                json_text = cleaned[start:end+1]
                parsed = json.loads(json_text)
                return parsed
        except Exception:
            pass

        return {"summary": cleaned, "message": ""}

