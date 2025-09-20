import openai
from typing import Dict, Any
from config.openai_config import OpenAIConfig

class TSRefactorer:
    """Handles refactoring and optimization of JavaScript/TypeScript code snippets"""

    def __init__(self, config: OpenAIConfig):
        self.config = config
        self.client = config.get_client()

    def refactor_code(self, code_snippet: str, language: str = "ts", minimal: bool = False) -> str:
        """
        Refactors and optimizes JavaScript/TypeScript code.

        Args:
            code_snippet: The JS/TS code snippet to refactor.
            language: The language of the code ("js" or "ts").
            minimal: If True, generate minimal code markup.

        Returns:
            The refactored code as a string.
        """
        if not self.config.is_available():
            return self._fallback_code_refactoring(code_snippet, language, minimal)

        prompt = self._create_refactoring_prompt(code_snippet, language, minimal)
        try:
            response = self.client.chat.completions.create(
                model=self.config.get_model(),
                messages=[
                    {"role": "system", "content": self._get_system_prompt_refactor(language, minimal)},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.config.get_max_tokens(),
                temperature=self.config.get_temperature()
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error calling OpenAI API for code refactoring: {e}")
            return self._fallback_code_refactoring(code_snippet, language, minimal)

    def _get_system_prompt_refactor(self, language: str, minimal: bool) -> str:
        """System prompt for code refactoring"""
        base_prompt = f"You are an expert {language.upper()} code refactorer and optimizer. Your task is to analyze user-provided {language.upper()} code, identify areas for improvement (e.g., readability, performance, modern syntax, best practices), and provide a refactored, cleaner version. Always explain the changes made. Wrap the refactored code in a Markdown code block with '{language}' language specifier."
        if language == "ts":
            base_prompt += " Ensure proper type annotations are maintained or added."
        if minimal:
            base_prompt += " Keep comments minimal and focus on code brevity."
        return base_prompt

    def _create_refactoring_prompt(self, code_snippet: str, language: str, minimal: bool) -> str:
        """Create prompt for code refactoring"""
        prompt = f"Please refactor and optimize the following {language.upper()} code snippet. Focus on improving readability, performance, and adherence to modern best practices. Provide the improved code and a brief explanation of the changes:\n\n\`\`\`{language}\n{code_snippet}\n\`\`\`\n"
        if minimal:
            prompt += " Keep explanations and comments minimal."
        return prompt

    def _fallback_code_refactoring(self, code_snippet: str, language: str, minimal: bool) -> str:
        """Fallback code refactoring when OpenAI is not available"""
        return f"""\`\`\`{language}
// Fallback: Code refactoring not available offline. Please set up your OpenAI API key.
// Original Code:
{code_snippet}

// Suggestion: Consider manual refactoring for improved readability and performance.
\`\`\`"""
