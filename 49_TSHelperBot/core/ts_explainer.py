import openai
from typing import Dict, Any
from config.openai_config import OpenAIConfig

class TSExplainer:
    """Handles explanation of JavaScript/TypeScript code snippets"""

    def __init__(self, config: OpenAIConfig):
        self.config = config
        self.client = config.get_client()

    def explain_code(self, code_snippet: str, language: str = "ts") -> str:
        """
        Explains JavaScript/TypeScript code, including purpose, structure, and best practices.

        Args:
            code_snippet: The JS/TS code snippet to explain.
            language: The language of the code ("js" or "ts").

        Returns:
            A Markdown-formatted explanation of the code.
        """
        if not self.config.is_available():
            return self._fallback_code_explanation(code_snippet, language)

        prompt = self._create_explanation_prompt(code_snippet, language)
        try:
            response = self.client.chat.completions.create(
                model=self.config.get_model(),
                messages=[
                    {"role": "system", "content": self._get_system_prompt_explain(language)},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.config.get_max_tokens(),
                temperature=self.config.get_temperature()
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error calling OpenAI API for code explanation: {e}")
            return self._fallback_code_explanation(code_snippet, language)

    def _get_system_prompt_explain(self, language: str) -> str:
        """System prompt for code explanation"""
        return f"You are an expert {language.upper()} assistant. Your job is to explain {language.upper()} code snippets clearly and concisely. Highlight each part's purpose, structure, and best practices. Point out potential issues or areas for improvement. Format your responses in clean Markdown with code blocks and clear headings.\n\nGuidelines:\n1. Always format your responses in clean Markdown.\n2. Use code blocks with '{language}' syntax for code snippets and 'text' for explanations.\n3. Explain what each part of the code does and its typical usage.\n4. Include practical examples when helpful.\n5. Be concise but comprehensive.\n6. Structure explanations with clear headings.\n\nFormat examples like this:\n### `Function Name`\nBrief description of what the function does.\n\n\`\`\`{language}\nfunctionName() {{ /* ... */ }}\`\`\`\n\n**Explanation:** Detailed explanation of the function and its parameters.\n\n**Best Practices:** Guidelines for effective use.\n\n**When to use:** Specific use cases and scenarios.\""

    def _create_explanation_prompt(self, code_snippet: str, language: str) -> str:
        """Create prompt for code explanation"""
        return f"Please explain the following {language.upper()} code snippet in detail, focusing on its purpose, structure, best practices, and any potential issues:\n\n\`\`\`{language}\n{code_snippet}\`\`\`\n\nProvide:\n1. What the code does\n2. Its typical structure and components\n3. Common use cases\n4. Best practices for readability, performance, and maintainability\n5. Any warnings about potential errors or bad practices\n\nFormat the response in clean Markdown with proper code blocks, clear headings for each major part, and bold warnings for issues."

    def _fallback_code_explanation(self, code_snippet: str, language: str) -> str:
        """Fallback explanation when OpenAI is not available"""
        # Basic explanation for some common patterns
        if "function" in code_snippet or "const" in code_snippet or "let" in code_snippet:
            return f"""### {language.upper()} Code Explanation
Code: \`\`\`{language}\n{code_snippet}\`\`\`\n\n**Note:** Detailed explanation not available offline. Please set up your OpenAI API key for full explanations.\n\nThis snippet likely defines variables, functions, or classes. For a deeper dive, connect to OpenAI!"""
        return f"""### {language.upper()} Code Explanation
Code: \`\`\`{language}\n{code_snippet}\`\`\`\n\n**Note:** AI-powered explanations not available offline. Please set up your OpenAI API key for detailed explanations.\n\nCommon {language.upper()} patterns:\n- Functions: `function myFunction() {{...}}` or `const myFunction = () => {{...}}`\n- Variables: `const myVar = 'value';` or `let anotherVar = 10;`\n- Classes: `class MyClass {{...}}`"""
