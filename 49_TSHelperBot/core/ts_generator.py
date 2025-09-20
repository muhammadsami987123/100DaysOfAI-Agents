import openai
from typing import Dict, Any
from config.openai_config import OpenAIConfig

class TSGenerator:
    """Handles generation of JavaScript/TypeScript from natural language descriptions"""

    def __init__(self, config: OpenAIConfig):
        self.config = config
        self.client = config.get_client()

    def generate_code(self, description: str, language: str = "ts", minimal: bool = False) -> str:
        """
        Generates JavaScript or TypeScript code based on a natural language description.

        Args:
            description: A natural language description of the desired code.
            language: The target language for generation ("js" or "ts").
            minimal: If True, generate minimal code markup.

        Returns:
            The generated code as a string.
        """
        if not self.config.is_available():
            return self._fallback_code_generation(description, language, minimal)

        prompt = self._create_generation_prompt(description, language, minimal)
        try:
            response = self.client.chat.completions.create(
                model=self.config.get_model(),
                messages=[
                    {"role": "system", "content": self._get_system_prompt_generate(language, minimal)},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.config.get_max_tokens(),
                temperature=self.config.get_temperature()
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error calling OpenAI API for code generation: {e}")
            return self._fallback_code_generation(description, language, minimal)

    def _get_system_prompt_generate(self, language: str, minimal: bool) -> str:
        """System prompt for code generation"""
        base_prompt = f"You are an expert {language.upper()} developer. Your task is to generate clean, semantic, and efficient {language.upper()} code based on user descriptions. Always prioritize best practices, readability, and maintainability. Wrap the generated code in a Markdown code block with '{language}' language specifier."
        if language == "ts":
            base_prompt += " Ensure the output is valid TypeScript with proper type annotations."
        if minimal:
            base_prompt += " Generate minimal markup, focusing only on the requested elements without extra boilerplate if not explicitly asked."
        return base_prompt

    def _create_generation_prompt(self, description: str, language: str, minimal: bool) -> str:
        """Create prompt for code generation"""
        prompt = f"Generate {language.upper()} code for the following description: '{description}'."
        if language == "ts":
            prompt += " Ensure it includes type annotations."
        if minimal:
            prompt += " Keep the markup minimal."
        return prompt

    def _fallback_code_generation(self, description: str, language: str, minimal: bool) -> str:
        """Fallback code generation when OpenAI is not available"""
        if "function" in description.lower() and "email" in description.lower():
            return f"""\`\`\`{language}
// Fallback: Code generation not available offline. Please set up your OpenAI API key.
// Description: {description}
function validateEmail(email: string): boolean {{ return /^[^\s@]+@[^\s@]+\\.[^\s@]+$/.test(email); }}
\`\`\`"""
        elif "hello world" in description.lower():
            return f"""\`\`\`{language}
// Fallback: Code generation not available offline. Please set up your OpenAI API key.
// Description: {description}
console.log("Hello, World!");
\`\`\`"""
        return f"""\`\`\`{language}
// Code generation not available offline. Please set up your OpenAI API key.
// Description: {description}
// Version: {language}, Minimal: {minimal}
console.log("Fallback: AI not available.");
\`\`\`"""
