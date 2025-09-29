import openai
from typing import Any, Dict
from config.openai_config import OpenAIConfig

class JsonExplainer:
    """Handles explanation and suggestions for JSON data using OpenAI GPT"""

    def __init__(self, config: OpenAIConfig):
        self.config = config
        self.client = config.get_client()

    def explain_json(self, json_data: Dict[str, Any], was_fixed: bool = False) -> str:
        """
        Explains the structure, key-value meanings, and nesting levels of JSON data.

        Args:
            json_data: The parsed JSON object.
            was_fixed: A boolean indicating if the JSON was automatically fixed prior to explanation.

        Returns:
            A Markdown-formatted explanation.
        """
        if not self.config.is_available():
            return self._fallback_explanation(json_data, was_fixed)

        prompt = self._create_explanation_prompt(json_data, was_fixed)
        try:
            response = self.client.chat.completions.create(
                model=self.config.get_model(),
                messages=[
                    {"role": "system", "content": self._get_system_prompt_explain(was_fixed)},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.config.get_max_tokens(),
                temperature=self.config.get_temperature()
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error calling OpenAI API for JSON explanation: {e}")
            return self._fallback_explanation(json_data, was_fixed)

    def _get_system_prompt_explain(self, was_fixed: bool) -> str:
        """System prompt for JSON explanation"""
        base_prompt = """You are an expert JSON data analyst. Your task is to explain JSON structures clearly and concisely, including key-value meanings, data types, nesting levels, and potential use cases. Provide suggestions for clarity or optimization if keys are unclear or deeply nested. Format your responses in clean Markdown with code blocks and clear headings.

Guidelines:
1. Always format your responses in clean Markdown.
2. Use code blocks with 'json' syntax for JSON snippets and 'text' for explanations.
3. Explain the overall structure first.
4. Detail each top-level key: its purpose, data type, and typical values.
5. Explain nested objects/arrays recursively.
6. Provide suggestions for improvement, especially for deep nesting or ambiguous keys.
7. Use emojis sparingly and appropriately.
8. Structure explanations with clear headings for each section/key.
"""
        if was_fixed:
            base_prompt += "\nAdditionally, inform the user that the JSON was automatically corrected before analysis, and briefly explain what kinds of corrections were made (e.g., adding double quotes to keys or string values)."
        return base_prompt

    def _create_explanation_prompt(self, json_data: Dict[str, Any], was_fixed: bool) -> str:
        """Create prompt for JSON explanation"""
        import json
        json_string = json.dumps(json_data, indent=2)
        prompt_text = f"""Please explain the following JSON data in detail. Focus on:

```json
{json_string}
```

Provide:
1. Overall structure (Is it an object, array of objects, etc.?)
2. For each top-level key (and important nested keys):
   - Its purpose/meaning
   - Data type (string, number, boolean, array, object)
   - Example values
3. Nesting levels and relationships between objects.
4. Suggestions for improvement (e.g., if keys are ambiguous, or if data is excessively nested).

Format the response in clean Markdown with proper code blocks, clear headings, and bold warnings/suggestions.
"""
        if was_fixed:
            prompt_text += "\nAlso, mention that the input JSON was automatically corrected to be valid JSON before this analysis. Briefly describe the types of corrections made (e.g., unquoted keys were wrapped in double quotes)."
        return prompt_text

    def _fallback_explanation(self, json_data: Dict[str, Any], was_fixed: bool) -> str:
        """Fallback explanation when OpenAI is not available"""
        import json
        json_string = json.dumps(json_data, indent=2)
        fixed_note = "(Note: The JSON was automatically corrected.)" if was_fixed else ""
        return f"""### JSON Explanation (Offline Mode) {fixed_note}

**Parsed JSON:**
```json
{json_string}
```

**Note:** AI-powered explanations are not available offline. Please set up your OpenAI API key for detailed analysis and suggestions.

**Basic Observations:**
- This is a JSON {type(json_data).__name__.lower()}.
- Top-level keys: {', '.join(json_data.keys()) if isinstance(json_data, dict) else 'N/A'}

**Suggestion:** To get comprehensive explanations of key meanings, data types, nesting, and improvement suggestions, please configure your OpenAI API key.
"""
