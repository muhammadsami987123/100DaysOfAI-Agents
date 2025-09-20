import openai
from typing import Dict, Any
from config.openai_config import OpenAIConfig

class TSConverter:
    """Handles conversion of JavaScript <-> TypeScript"""

    def __init__(self, config: OpenAIConfig):
        self.config = config
        self.client = config.get_client()

    def convert_code(self, code_snippet: str, target_language: str) -> str:
        """
        Converts JavaScript or TypeScript code to the target language.

        Args:
            code_snippet: The code snippet to convert.
            target_language: The target language ("js" or "ts").

        Returns:
            The converted code as a string.
        """
        if not self.config.is_available():
            return self._fallback_code_conversion(code_snippet, target_language)

        prompt = self._create_conversion_prompt(code_snippet, target_language)
        try:
            response = self.client.chat.completions.create(
                model=self.config.get_model(),
                messages=[
                    {"role": "system", "content": self._get_system_prompt_convert(target_language)},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.config.get_max_tokens(),
                temperature=self.config.get_temperature()
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error calling OpenAI API for code conversion: {e}")
            return self._fallback_code_conversion(code_snippet, target_language)

    def _get_system_prompt_convert(self, target_language: str) -> str:
        """System prompt for code conversion"""
        from_lang = "TypeScript" if target_language == "js" else "JavaScript"
        to_lang = "JavaScript" if target_language == "js" else "TypeScript"
        base_prompt = f"You are an expert {from_lang} to {to_lang} converter. Your task is to accurately convert user-provided code snippets from {from_lang} to {to_lang}. Focus on correctness, maintaining functionality, and applying {to_lang} best practices. Wrap the converted code in a Markdown code block with '{target_language}' language specifier."
        if target_language == "ts":
            base_prompt += " Ensure all necessary type annotations are added."
        elif target_language == "js":
            base_prompt += " Ensure all TypeScript-specific syntax (like type annotations) is removed while retaining functionality."
        return base_prompt

    def _create_conversion_prompt(self, code_snippet: str, target_language: str) -> str:
        """Create prompt for code conversion"""
        from_lang = "TypeScript" if target_language == "js" else "JavaScript"
        to_lang = "JavaScript" if target_language == "js" else "TypeScript"
        return f"Convert the following {from_lang} code snippet to {to_lang}:\n\n```{{" + (from_lang.lower() if from_lang != "TypeScript" else "ts") + "}}\n{code_snippet}\n```\n\nEnsure the converted code is clean, functional, and adheres to {to_lang} best practices. If converting to TypeScript, add appropriate type annotations."

    def _fallback_code_conversion(self, code_snippet: str, target_language: str) -> str:
        """Fallback code conversion when OpenAI is not available"""
        from_lang = "TypeScript" if target_language == "js" else "JavaScript"
        to_lang = "JavaScript" if target_language == "js" else "TypeScript"
        return f"""```{{" + target_language + "}}\n// Fallback: Code conversion not available offline. Please set up your OpenAI API key.\n// Original ({from_lang}):\n{code_snippet}\n\n// Unable to convert to {to_lang} offline. Manual conversion required.\n```"""
