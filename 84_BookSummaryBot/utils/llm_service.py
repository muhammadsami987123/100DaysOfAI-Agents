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
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.gemini_client = genai.GenerativeModel(Config.GEMINI_MODEL)
        else:
            print("GEMINI_API_KEY not found. Gemini client not initialized.")

        if Config.OPENAI_API_KEY:
            self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
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
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()

    def generate_content(self, prompt: str) -> Dict[str, Any]:
        try:
            if self.current_llm == "gemini":
                if not self.gemini_client:
                    raise ValueError("Gemini client not initialized.")
                response = self.gemini_client.generate_content(prompt)
                summary_text = response.text
                print(f"Gemini response: {repr(summary_text)}")  # Debug output with repr to see exact characters
                
                # Check if response is empty or too short
                if not summary_text or len(summary_text.strip()) < 10:
                    print("Warning: Gemini returned empty or very short response")
                    return {"summary": "No response generated from Gemini API", "key_points": []}
                
                # Attempt to parse as JSON if it looks like it
                try:
                    # Clean up the response text
                    cleaned_text = summary_text.strip()
                    
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
                        print(f"Attempting to parse JSON: {repr(json_text)}")
                        parsed_content = json.loads(json_text)
                        
                        # Validate the parsed content has required fields
                        if isinstance(parsed_content, dict) and "summary" in parsed_content:
                            return parsed_content
                        else:
                            print("Warning: Parsed JSON missing required fields")
                            return {"summary": cleaned_text, "key_points": []}
                    else:
                        # If no JSON found, return the text as summary
                        print("Warning: No JSON object found in response")
                        return {"summary": cleaned_text, "key_points": []}
                        
                except json.JSONDecodeError as e:
                    print(f"JSON parsing error: {e}")
                    print(f"Raw response: {summary_text}")
                    # Create a fallback response with the raw text as summary
                    fallback_summary = summary_text.strip() if summary_text.strip() else "No summary generated"
                    return {"summary": fallback_summary, "key_points": []}
            elif self.current_llm == "openai":
                if not self.openai_client:
                    raise ValueError("OpenAI client not initialized.")
                response = self.openai_client.chat.completions.create(
                    model=Config.OPENAI_MODEL,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                summary_text = response.choices[0].message.content
                print(f"OpenAI response: {summary_text}")  # Debug output
                
                try:
                    # Clean up the response text
                    cleaned_text = summary_text.strip()
                    
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
                        parsed_content = json.loads(json_text)
                        return parsed_content
                    else:
                        # If no JSON found, return the text as summary
                        return {"summary": cleaned_text, "key_points": []}
                        
                except json.JSONDecodeError as e:
                    print(f"JSON parsing error: {e}")
                    print(f"Raw response: {summary_text}")
                    # Create a fallback response with the raw text as summary
                    fallback_summary = summary_text.strip() if summary_text.strip() else "No summary generated"
                    return {"summary": fallback_summary, "key_points": []}
            else:
                print("Warning: No LLM client is set or initialized.")
                return {"summary": "No LLM client available", "key_points": []}
        except Exception as e:
            print(f"Error generating content with {self.current_llm}: {e}")
            print(f"Exception type: {type(e)}")
            import traceback
            traceback.print_exc()
            # Return a fallback response instead of raising an exception
            return {"summary": f"Error generating summary: {str(e)}", "key_points": []}
