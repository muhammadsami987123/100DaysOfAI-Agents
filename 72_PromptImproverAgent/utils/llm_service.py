import os
import json
from typing import Optional, Dict, Any

from config import LLM_MODEL, GEMINI_API_KEY, OPENAI_API_KEY

class LLMService:
    def __init__(self):
        self.model_choice = (LLM_MODEL or 'gemini').lower()
        self.gemini_client = None
        self.gemini_model = None
        self.openai_client = None
        self._init_clients()

    def _init_clients(self) -> None:
        if self.model_choice == 'gemini' and GEMINI_API_KEY:
            try:
                import google.generativeai as genai
                genai.configure(api_key=GEMINI_API_KEY)
                # Default fast model; can be overridden via env if desired
                model_name = os.environ.get('GEMINI_MODEL_NAME', 'gemini-2.0-flash')
                self.gemini_model = genai.GenerativeModel(model_name)
                self.gemini_client = genai
            except Exception:
                self.gemini_client = None
                self.gemini_model = None
        elif self.model_choice in ('gpt', 'openai') and OPENAI_API_KEY:
            try:
                from openai import OpenAI
                self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
            except Exception:
                self.openai_client = None

    def _read_template(self) -> str:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        template_path = os.path.join(base_dir, 'prompts', 'prompt_improvement.txt')
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return (
                "You are my Prompt Coach. Improve the following prompt. "
                "Return JSON with keys improved_prompt, variations, explanation.\n\n"
                "User's rough prompt:\n{{ raw_prompt }}\n\n[Optional: Target style/Tone: {{ tone }}]"
            )

    def _render_prompt(self, raw_prompt: str, tone: Optional[str]) -> str:
        template = self._read_template()
        rendered = template.replace('{{ raw_prompt }}', raw_prompt or '')
        rendered = rendered.replace('{{ tone }}', tone or '')
        return rendered

    def _parse_json(self, text: str) -> Dict[str, Any]:
        try:
            return json.loads(text)
        except Exception:
            # Try to extract JSON block if wrapped in prose
            start = text.find('{')
            end = text.rfind('}')
            if start != -1 and end != -1 and end > start:
                snippet = text[start:end+1]
                try:
                    return json.loads(snippet)
                except Exception:
                    pass
            return {}

    def improve_prompt(self, prompt: str, tone: Optional[str] = None) -> Dict[str, Any]:
        rendered = self._render_prompt(prompt, tone)

        # Prefer configured provider
        if self.model_choice == 'gemini' and self.gemini_model is not None:
            try:
                result = self.gemini_model.generate_content(rendered)
                text = (result.text or '').strip()
                data = self._parse_json(text)
                if data:
                    return {
                        'improved': data.get('improved_prompt') or data.get('improved') or '',
                        'alternatives': data.get('variations') or data.get('alternatives') or [],
                        'explanation': data.get('explanation') or ''
                    }
            except Exception:
                pass

        if self.openai_client is not None:
            try:
                model_name = os.environ.get('OPENAI_MODEL_NAME', 'gpt-4o-mini')
                resp = self.openai_client.chat.completions.create(
                    model=model_name,
                    messages=[
                        { 'role': 'system', 'content': 'You are a Prompt Coach. Reply ONLY in strict JSON.' },
                        { 'role': 'user', 'content': rendered }
                    ],
                    temperature=0.4,
                )
                text = (resp.choices[0].message.content or '').strip()
                data = self._parse_json(text)
                if data:
                    return {
                        'improved': data.get('improved_prompt') or data.get('improved') or '',
                        'alternatives': data.get('variations') or data.get('alternatives') or [],
                        'explanation': data.get('explanation') or ''
                    }
            except Exception:
                pass

        # Fallback when providers are unavailable
        return {
            'improved': f"Rewrite clearly with structure: {prompt}",
            'alternatives': [
                f"Formal: Please {prompt}",
                f"Concise: {prompt}",
                f"Creative: Imagine {prompt}",
            ],
            'explanation': 'Returned fallback result because no LLM response was available.'
        }
