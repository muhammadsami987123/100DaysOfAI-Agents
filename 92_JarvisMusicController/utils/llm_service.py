import google.generativeai as genai
from config import Config

class LLMService:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')

    def interpret_command(self, command: str) -> str:
        try:
            response = self.model.generate_content(f"Interpret the following music command: {command}. Respond with a single keyword like 'play', 'pause', 'next', 'previous', 'stop', or a more complex instruction if applicable.")
            return response.text.strip().lower()
        except Exception as e:
            print(f"Error interpreting command with LLM: {e}")
            return ""
