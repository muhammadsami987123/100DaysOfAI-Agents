import openai
from typing import Dict, Any
from config.openai_config import OpenAIConfig

class HtmlExplainer:
    """Handles explanation of HTML code snippets"""

    def __init__(self, config: OpenAIConfig):
        self.config = config
        self.client = config.get_client()

    def explain_html(self, html_code: str) -> str:
        """
        Explains HTML code, including tag purpose, structure, best practices,
        and highlights deprecated or bad practices.

        Args:
            html_code: The HTML code snippet to explain.

        Returns:
            A Markdown-formatted explanation of the HTML code.
        """
        if not self.config.is_available():
            return self._fallback_html_explanation(html_code)

        prompt = self._create_explanation_prompt(html_code)
        try:
            response = self.client.chat.completions.create(
                model=self.config.get_model(),
                messages=[
                    {"role": "system", "content": self._get_system_prompt_explain()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.config.get_max_tokens(),
                temperature=self.config.get_temperature()
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error calling OpenAI API for HTML explanation: {e}")
            return self._fallback_html_explanation(html_code)

    def _get_system_prompt_explain(self) -> str:
        """System prompt for HTML explanation"""
        return """You are an expert HTML assistant. Your job is to explain HTML code snippets clearly and concisely. Highlight each tag's purpose, structure, and best practices. Point out deprecated tags or bad practices. Format your responses in clean Markdown with code blocks and clear headings.

Guidelines:
1. Always format your responses in clean Markdown.
2. Use code blocks with 'html' syntax for HTML snippets and 'text' for explanations.
3. Explain what each tag does and its typical usage.
4. Include practical examples when helpful.
5. Be concise but comprehensive.
6. Use emojis sparingly and appropriately.
7. Structure explanations with clear headings for each tag.
8. Explicitly mark deprecated or bad practices with a bold warning, e.g., **Deprecated:**.

Format examples like this:
### `Tag Name`
Brief description of what the tag does.

```html
<tag>Content</tag>
```

**Explanation:** Detailed explanation of the tag and its attributes.

**Best Practices:** Guidelines for effective use.

**When to use:** Specific use cases and scenarios."""

    def _create_explanation_prompt(self, html_code: str) -> str:
        """Create prompt for HTML explanation"""
        return f"""Please explain the following HTML code snippet in detail, focusing on each tag, its purpose, best practices, and any deprecated or bad practices:

```html
{html_code}
```

Provide: 
1. What each tag does
2. Its typical structure and attributes
3. Common use cases
4. Best practices for accessibility and SEO
5. Any warnings about deprecated elements or bad practices

Format the response in clean Markdown with proper code blocks, clear headings for each tag, and bold warnings for deprecated/bad practices."""

    def _fallback_html_explanation(self, html_code: str) -> str:
        """Fallback explanation when OpenAI is not available"""
        # Basic explanation for some common tags
        if "<div>" in html_code:
            return """### `<div>`
A generic container for flow content. It has no effect on the content or layout until styled in CSS.

**Note:** Detailed explanation not available offline. Please set up your OpenAI API key for full explanations."""
        elif "<h1>" in html_code:
            return """### `<h1>`
Represents a section heading. `<h1>` is the most important heading, typically used for the main title of a page.

**Note:** Detailed explanation not available offline. Please set up your OpenAI API key for full explanations."""
        elif "<center>" in html_code:
            return """### `<center>`
**Deprecated:** The `<center>` HTML element is a block-level element that displays its block-level or inline contents centered horizontally within its containing element. Use CSS for styling.

**Note:** Detailed explanation not available offline. Please set up your OpenAI API key for full explanations."""
        return f"""### HTML Code Explanation
Code: ```html\n{html_code}\n```

**Note:** AI-powered explanations not available offline.
Please set up your OpenAI API key for detailed explanations.

Common HTML Tags:
- `<div>` - Generic container
- `<h1>` - Main heading
- `<p>` - Paragraph
- `<a>` - Link
- `<img>` - Image"""
