import google.generativeai as genai
import os
from openai import OpenAI
from typing import Dict, Any, Optional
import json
from config import Config

class LLMService:
    def __init__(self):
        self.gemini_client = None
        self.openai_client = None
        self.current_llm = Config.DEFAULT_LLM
        self._init_clients()

    def _init_clients(self) -> None:
        if Config.GEMINI_API_KEY:
            try:
                genai.configure(api_key=Config.GEMINI_API_KEY)
                self.gemini_client = genai.GenerativeModel(Config.GEMINI_MODEL)
            except Exception as e:
                print(f"Failed to initialize Gemini client: {e}")
                self.gemini_client = None
        else:
            print("GEMINI_API_KEY not found. Gemini client not initialized.")

        if Config.OPENAI_API_KEY:
            try:
                self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
            except Exception as e:
                print(f"Failed to initialize OpenAI client: {e}")
                self.openai_client = None
        else:
            print("OPENAI_API_KEY not found. OpenAI client not initialized.")

    def set_llm(self, llm_choice: str) -> None:
        if llm_choice == "gemini" and self.gemini_client:
            self.current_llm = "gemini"
            print(f"Switched to Gemini LLM")
        elif llm_choice == "openai" and self.openai_client:
            self.current_llm = "openai"
            print(f"Switched to OpenAI LLM")
        else:
            print(f"Warning: Selected LLM '{llm_choice}' is not available. Using current LLM: {self.current_llm}")

    def _read_template(self, template_name: str) -> str:
        template_path = os.path.join(os.path.dirname(__file__), "..", "prompts", template_name)
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Template file not found: {template_path}")
            return ""

    def generate_content(self, prompt: str, parse_json: bool = True) -> Dict[str, Any]:
        """Generate content from LLM. If parse_json is True, attempts to parse JSON from response."""
        try:
            if self.current_llm == "gemini":
                if not self.gemini_client:
                    raise ValueError("Gemini client not initialized.")
                response = self.gemini_client.generate_content(prompt)
                response_text = response.text
                print(f"Gemini response: {repr(response_text[:200])}...")
                
                if not response_text or len(response_text.strip()) < 10:
                    print("Warning: Gemini returned empty or very short response")
                    return {"error": "No response generated from Gemini API"}
                
                if parse_json:
                    return self._parse_json_response(response_text)
                else:
                    return {"response": response_text}
                    
            elif self.current_llm == "openai":
                if not self.openai_client:
                    raise ValueError("OpenAI client not initialized.")
                response = self.openai_client.chat.completions.create(
                    model=Config.OPENAI_MODEL,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                response_text = response.choices[0].message.content
                print(f"OpenAI response: {repr(response_text[:200])}...")
                
                if parse_json:
                    return self._parse_json_response(response_text)
                else:
                    return {"response": response_text}
            else:
                print("Warning: No LLM client is set or initialized.")
                return {"error": "No LLM client available"}
        except Exception as e:
            print(f"Error generating content with {self.current_llm}: {e}")
            import traceback
            traceback.print_exc()
            return {"error": f"Error generating content: {str(e)}"}

    def _parse_json_response(self, text: str) -> Dict[str, Any]:
        """Parse JSON from LLM response text."""
        try:
            cleaned_text = text.strip()
            
            # Remove markdown code blocks
            if cleaned_text.startswith('```json'):
                cleaned_text = cleaned_text[7:]
            elif cleaned_text.startswith('```'):
                cleaned_text = cleaned_text[3:]
            
            if cleaned_text.endswith('```'):
                cleaned_text = cleaned_text[:-3]
            
            cleaned_text = cleaned_text.strip()
            
            # Try to find JSON object in the response
            start_idx = cleaned_text.find('{')
            end_idx = cleaned_text.rfind('}')
            
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                json_text = cleaned_text[start_idx:end_idx+1]
                print(f"Attempting to parse JSON: {repr(json_text[:200])}...")
                parsed_content = json.loads(json_text)
                return parsed_content
            else:
                print("Warning: No JSON object found in response")
                return {"response": cleaned_text, "raw": True}
                
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Raw response: {text[:500]}")
            return {"response": text, "raw": True, "parse_error": str(e)}

