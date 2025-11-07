"""LLM Service for BookmarkManager - Handles both Gemini and OpenAI"""
from typing import Dict, Any, Optional
from config import Config
import json
import os


class LLMService:
    def __init__(self):
        self.gemini_api_key = Config.GEMINI_API_KEY
        self.openai_api_key = Config.OPENAI_API_KEY
        self.default_llm = Config.DEFAULT_LLM
        self.prompts_dir = "./prompts"
        os.makedirs(self.prompts_dir, exist_ok=True)
        
    def set_llm(self, llm_choice: str):
        """Set the LLM to use for this session"""
        if llm_choice in ["gemini", "openai"]:
            self.default_llm = llm_choice
        else:
            self.default_llm = Config.DEFAULT_LLM

    def _read_template(self, filename: str) -> str:
        """Read a prompt template from the prompts directory"""
        template_path = os.path.join(self.prompts_dir, filename)
        try:
            if os.path.exists(template_path):
                with open(template_path, "r") as f:
                    return f.read()
            else:
                # Return empty string if file doesn't exist
                return ""
        except Exception as e:
            print(f"Error reading template {filename}: {e}")
            return ""

    def generate_content(self, prompt: str, use_llm: Optional[str] = None) -> Dict[str, Any]:
        """Generate content using the specified LLM"""
        llm_choice = use_llm or self.default_llm
        
        try:
            if llm_choice == "gemini":
                return self._generate_with_gemini(prompt)
            elif llm_choice == "openai":
                return self._generate_with_openai(prompt)
            else:
                return {"error": f"Unknown LLM: {llm_choice}"}
        except Exception as e:
            print(f"Error generating content: {e}")
            return {"error": str(e)}

    def _generate_with_gemini(self, prompt: str) -> Dict[str, Any]:
        """Generate content using Google Gemini API"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.gemini_api_key)
            model = genai.GenerativeModel(Config.GEMINI_MODEL)
            response = model.generate_content(prompt)
            
            return {
                "content": response.text,
                "model": Config.GEMINI_MODEL,
                "success": True
            }
        except Exception as e:
            print(f"Gemini API Error: {e}")
            return {
                "error": str(e),
                "model": Config.GEMINI_MODEL,
                "success": False
            }

    def _generate_with_openai(self, prompt: str) -> Dict[str, Any]:
        """Generate content using OpenAI API"""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_api_key)
            response = client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            return {
                "content": response.choices[0].message.content,
                "model": Config.OPENAI_MODEL,
                "success": True
            }
        except Exception as e:
            print(f"OpenAI API Error: {e}")
            return {
                "error": str(e),
                "model": Config.OPENAI_MODEL,
                "success": False
            }

