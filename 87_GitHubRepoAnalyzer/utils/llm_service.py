"""
LLM Service abstraction for Gemini and OpenAI GPT-4.1
"""

import os
import json
from config import Config

try:
    import google.generativeai as genai
    HAS_GENAI = True
except Exception:
    genai = None
    HAS_GENAI = False

try:
    from openai import OpenAI
    HAS_OPENAI = True
except Exception:
    OpenAI = None
    HAS_OPENAI = False

class LLMService:
    """LLMService supporting Gemini and OpenAI, with model switching."""
    def __init__(self):
        self.current_llm = Config.DEFAULT_LLM_MODEL
        self.gemini_client = None
        self.openai_client = None
        self._init_clients()

    def _init_clients(self):
        if HAS_GENAI and Config.GEMINI_API_KEY:
            try:
                genai.configure(api_key=Config.GEMINI_API_KEY)
                self.gemini_client = genai.GenerativeModel("gemini-2.0-flash")
            except Exception as e:
                print(f"Failed to initialize Gemini client: {e}")
                self.gemini_client = None
        if HAS_OPENAI and Config.OPENAI_API_KEY:
            try:
                self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
            except Exception as e:
                print(f"Failed to initialize OpenAI client: {e}")
                self.openai_client = None

    def set_llm(self, model: str):
        if model in ["gemini", "openai"]:
            self.current_llm = model

    def generate_content(self, repo_data, model: str = None):
        model = model or self.current_llm
        prompt = self._build_prompt(repo_data)
        if model == "gemini" and self.gemini_client:
            try:
                response = self.gemini_client.generate_content([prompt])
                return response.text if hasattr(response, "text") else str(response)
            except Exception as e:
                return f"Gemini error: {e}"
        elif model == "openai" and self.openai_client:
            try:
                completion = self.openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}]
                )
                return completion.choices[0].message.content
            except Exception as e:
                return f"OpenAI error: {e}"
        # Fallback: return a simple summary
        return self._fallback_summary(repo_data)

    def _build_prompt(self, repo_data):
        owner = repo_data.get("owner", "")
        repo = repo_data.get("repo", "")
        readme = repo_data.get("readme", "")
        tree = repo_data.get("tree", [])
        key_files = repo_data.get("key_files", {})
        prompt = f"Analyze the following GitHub repository and summarize its purpose, tech stack, key files, and structure.\n\n"
        prompt += f"Repository: {owner}/{repo}\n\n"
        prompt += f"README:\n{readme[:500]}...\n\n" if readme else "README: Not found\n\n"
        prompt += "Key Files:\n"
        for k, v in key_files.items():
            prompt += f"- {k}: {len(v)} chars\n"
        prompt += "\nFile/Folder Structure:\n"
        for file in tree[:20]:
            prompt += f"- {file.get('path', '')}\n"
        prompt += "...\n"
        return prompt

    def _fallback_summary(self, repo_data):
        owner = repo_data.get("owner", "")
        repo = repo_data.get("repo", "")
        readme = repo_data.get("readme", "")
        tree = repo_data.get("tree", [])
        key_files = repo_data.get("key_files", {})
        summary = f"Repository: {owner}/{repo}\n\n"
        summary += f"README:\n{readme[:500]}...\n\n" if readme else "README: Not found\n\n"
        summary += "Key Files:\n"
        for k, v in key_files.items():
            summary += f"- {k}: {len(v)} chars\n"
        summary += "\nFile/Folder Structure:\n"
        for file in tree[:20]:
            summary += f"- {file.get('path', '')}\n"
        summary += "...\n\n(No LLM API key set: This is a fallback summary.)"
        return summary
