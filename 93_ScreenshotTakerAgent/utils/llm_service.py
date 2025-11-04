import google.generativeai as genai
import openai
from config import config

class LLMService:
    """
    A service class for interacting with Large Language Models (LLMs).
    """
    def __init__(self, provider="gemini"):
        """
        Initializes the LLMService with the specified provider.
        """
        self.provider = provider
        if self.provider == "gemini":
            if not config.GEMINI_API_KEY:
                raise ValueError("Gemini API key not found in environment variables.")
            genai.configure(api_key=config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        elif self.provider == "openai":
            if not config.OPENAI_API_KEY:
                raise ValueError("OpenAI API key not found in environment variables.")
            openai.api_key = config.OPENAI_API_KEY
            self.model = "gpt-4.1"
        else:
            raise ValueError("Unsupported LLM provider.")

    def generate_response(self, prompt):
        """
        Generates a response from the LLM based on the given prompt.
        """
        try:
            if self.provider == "gemini":
                response = self.model.generate_content(prompt)
                return response.text
            elif self.provider == "openai":
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content
        except Exception as e:
            return f"An error occurred: {e}"
