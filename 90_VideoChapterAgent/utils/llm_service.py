import google.generativeai as genai
import openai
from config import GEMINI_API_KEY, OPENAI_API_KEY, GEMINI_MODEL, OPENAI_MODEL

class LLMService:
    def __init__(self, llm_type: str = "gemini"):
        self.llm_type = llm_type
        if self.llm_type == "gemini":
            genai.configure(api_key=GEMINI_API_KEY)
            self.model = genai.GenerativeModel(GEMINI_MODEL)
        elif self.llm_type == "openai":
            openai.api_key = OPENAI_API_KEY
        else:
            raise ValueError("Invalid LLM type. Choose 'gemini' or 'openai'.")

    def generate_content(self, prompt: str):
        if self.llm_type == "gemini":
            response = self.model.generate_content(prompt)
            return response.text
        elif self.llm_type == "openai":
            response = openai.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content

