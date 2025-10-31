import os
from google.generativeai import GenerativeModel
from openai import OpenAI

class LLMService:
    def __init__(self, api_key, provider="gemini"):
        self.provider = provider
        if provider == "gemini":
            self.model = GenerativeModel(api_key)
        elif provider == "openai":
            self.client = OpenAI(api_key=api_key)

    def generate(self, prompt):
        if self.provider == "gemini":
            response = self.model.generate_content(prompt)
            return response.text
        elif self.provider == "openai":
            response = self.client.completions.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=150
            )
            return response.choices[0].text.strip()
