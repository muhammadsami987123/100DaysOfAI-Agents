import openai
from typing import Dict, Any
from config.openai_config import OpenAIConfig

class TSDebugger:
    """Handles debugging of JavaScript/TypeScript code snippets"""

    def __init__(self, config: OpenAIConfig):
        self.config = config
        self.client = config.get_client()

    def debug_code(self, code_snippet: str, error_message: str = None, language: str = "ts") -> str:
        """
        Identifies and fixes errors in JavaScript/TypeScript code.

        Args:
            code_snippet: The JS/TS code snippet to debug.
            error_message: Optional. The error message received (if any).
            language: The language of the code ("js" or "ts").

        Returns:
            A Markdown-formatted response with error identification and fixed code.
        """
        if not self.config.is_available():
            return self._fallback_code_debugging(code_snippet, error_message, language)

        prompt = self._create_debugging_prompt(code_snippet, error_message, language)
        try:
            response = self.client.chat.completions.create(
                model=self.config.get_model(),
                messages=[
                    {"role": "system", "content": self._get_system_prompt_debug(language)},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.config.get_max_tokens(),
                temperature=self.config.get_temperature()
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error calling OpenAI API for code debugging: {e}")
            return self._fallback_code_debugging(code_snippet, error_message, language)

    def _get_system_prompt_debug(self, language: str) -> str:
        """System prompt for code debugging"""
        return f"You are an expert {language.upper()} debugger. Your task is to analyze user-provided {language.upper()} code, identify syntax or logic errors, explain them clearly, and provide a corrected version of the code. If an error message is provided, use it to guide your debugging. Wrap the corrected code in a Markdown code block with '{language}' language specifier. Provide clear explanations of the error and the fix.\n\nGuidelines:\n1. Clearly identify the error type and location.\n2. Explain why the error occurs.\n3. Provide the corrected code.\n4. Explain the changes made to fix the error.\n5. Keep explanations concise and developer-friendly.\""

    def _create_debugging_prompt(self, code_snippet: str, error_message: str, language: str) -> str:
        """Create prompt for code debugging"""
        prompt = f"Please debug the following {language.upper()} code snippet. Identify any syntax or logic errors, explain them, and provide the corrected code.\n\n\`\`\`{language}\n{code_snippet}\`\`\`\n"
        if error_message:
            prompt += f"\nAn error message was received: `{error_message}`\n"
        prompt += "\nProvide:\n1. A clear identification of the error(s).\n2. An explanation of why the error(s) occurred.\n3. The corrected code snippet.\n4. An explanation of the changes made to fix the error."
        return prompt

    def _fallback_code_debugging(self, code_snippet: str, error_message: str, language: str) -> str:
        """Fallback code debugging when OpenAI is not available"""
        error_info = f"Error Message: {error_message}" if error_message else "No specific error message provided."
        return f"""### {language.upper()} Debugging Assistant (Offline Mode)

**Code Snippet to Debug:**
\`\`\`{language}\n{code_snippet}\`\`\`

**Issue:** Unable to perform AI-powered debugging offline. Please set up your OpenAI API key for full debugging capabilities.

**{error_info}**

**Suggestion:** Manually review your code for common issues such as syntax errors, incorrect variable names, missing imports, or logic flaws. For {language.upper()} specifically, check for proper type usage if it's a TypeScript file, or common JavaScript pitfalls like `this` context or asynchronous operations.

**Basic Checklist for Debugging:**
- [ ] Check for typos in variable and function names.
- [ ] Ensure all parentheses, braces, and brackets are closed.
- [ ] Verify correct use of semicolons (if applicable).
- [ ] Inspect console logs for runtime errors.
- [ ] For TypeScript, check type mismatches.
- [ ] Break down complex functions into smaller, testable parts.
\`\`\`{language}\n// No automated fix available offline. Review your code based on the suggestions above.\n{code_snippet}\`\`\`"""
