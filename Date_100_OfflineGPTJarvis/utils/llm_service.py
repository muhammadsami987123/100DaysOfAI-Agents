# llm_service.py

from gpt4all import GPT4All

class LLMService:
    def __init__(self, model_name="orca-mini-3b-gguf2-q4_0.gguf"):
        # You might need to download the model if it's not available locally.
        # GPT4All will attempt to download it if not found.
        self.model = GPT4All(model_name)

    def generate_response(self, prompt):
        with self.model.chat_session():
            response = self.model.generate(prompt=prompt, temp=0)
            return response
