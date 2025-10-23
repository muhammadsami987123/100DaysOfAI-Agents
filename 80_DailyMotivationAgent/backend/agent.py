import os
import google.generativeai as genai
from openai import OpenAI
from jinja2 import Environment, FileSystemLoader

from backend.config import Config

class DailyMotivationAgent:
    def __init__(self):
        self.template_env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), '..' , 'prompts')))
        self.prompt_template = self.template_env.get_template(Config.PROMPT_FILE.split('/')[-1])

        if Config.GEMINI_API_KEY:
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.gemini_model = genai.GenerativeModel(Config.GEMINI_MODEL_NAME)
        else:
            self.gemini_model = None

        if Config.OPENAI_API_KEY:
            self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
        else:
            self.openai_client = None

        Config.validate()

    def _generate_content_gemini(self, prompt: str) -> str:
        if not self.gemini_model:
            raise ValueError("Gemini API key not configured.")
        response = self.gemini_model.generate_content(prompt)
        return response.text

    def _generate_content_openai(self, prompt: str) -> str:
        if not self.openai_client:
            raise ValueError("OpenAI API key not configured.")
        response = self.openai_client.chat.completions.create(
            model=Config.OPENAI_MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    def generate_motivation(self, name: str | None = None) -> dict:
        model_type = Config.DEFAULT_MODEL_PROVIDER

        context = {"name": name}
        rendered_prompt = self.prompt_template.render(context)

        if model_type == "gemini":
            raw_output = self._generate_content_gemini(rendered_prompt)
        elif model_type == "openai":
            raw_output = self._generate_content_openai(rendered_prompt)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")

        # Parse the output
        quote_line = ""
        message_line = ""
        for line in raw_output.split('\n'):
            if line.startswith("Quote:"):
                quote_line = line.replace("Quote:", "").strip().strip('" ')
            elif line.startswith("Message:"):
                message_line = line.replace("Message:", "").strip().strip('" ')

        if not quote_line or not message_line:
            # Fallback for parsing issues
            if "Quote:" in raw_output and "Message:" in raw_output:
                quote_line = raw_output.split("Quote:")[1].split("\n")[0].strip().strip('" ')
                message_line = raw_output.split("Message:")[1].split("\n")[0].strip().strip('" ')
            else:
                # If parsing completely fails, return the raw output as message
                quote_line = "An inspiring thought for your day:"
                message_line = raw_output

        return {"quote": quote_line, "message": message_line}
