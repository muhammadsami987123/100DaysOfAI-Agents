import json
import os
from typing import Dict, Any, Optional
import pandas as pd
import io
import re # Added for regex-like extraction

from backend.config import Config

# Dynamically import LLM clients
try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

class CSVAnalyzerAgent:
    def __init__(self):
        self.model_choice = Config.LLM_MODEL.lower()
        self.openai_client = None
        self.gemini_model = None
        self._init_clients()

    def _init_clients(self):
        if self.model_choice == 'gemini' and Config.GEMINI_API_KEY:
            if genai:
                try:
                    genai.configure(api_key=Config.GEMINI_API_KEY)
                    self.gemini_model = genai.GenerativeModel('gemini-2.0-flash') # Using flash for speed
                except Exception as e:
                    print(f"Error initializing Gemini client: {e}")
                    self.gemini_model = None
            else:
                print("Warning: google-generativeai not installed.")
        
        if self.model_choice == 'openai' and Config.OPENAI_API_KEY:
            if OpenAI:
                try:
                    self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
                except Exception as e:
                    print(f"Error initializing OpenAI client: {e}")
                    self.openai_client = None
            else:
                print("Warning: openai library not installed.")

        # Fallback if preferred model not available
        if not self.gemini_model and not self.openai_client:
            if Config.GEMINI_API_KEY and genai:
                try:
                    genai.configure(api_key=Config.GEMINI_API_KEY)
                    self.gemini_model = genai.GenerativeModel('gemini-2.0-flash')
                    print("Falling back to Gemini.")
                except Exception:
                    pass
            if not self.gemini_model and Config.OPENAI_API_KEY and OpenAI:
                try:
                    self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
                    print("Falling back to OpenAI.")
                except Exception:
                    pass
        
        if not self.gemini_model and not self.openai_client:
            print("CRITICAL ERROR: No LLM client initialized. Please check API keys and installations.")

    def _generate_response_with_llm(self, prompt: str) -> Optional[str]:
        if self.gemini_model:
            try:
                response = self.gemini_model.generate_content(prompt)
                return response.text
            except Exception as e:
                print(f"Gemini API error: {e}")
        
        if self.openai_client:
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful data analysis assistant."}, 
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"OpenAI API error: {e}")
        
        return "I am unable to generate a response at this moment. Please check my configuration."

    def analyze_csv(self, df: pd.DataFrame, user_question: str) -> Dict[str, Any]:
        # Capture df.info() output
        buffer = io.StringIO()
        df.info(buf=buffer, verbose=True, show_counts=True)
        df_info_str = buffer.getvalue()
        
        # Initial prompt to guide the LLM
        initial_prompt = (
            f"You are CSVAnalyzerBot. A user has uploaded a CSV file. "
            f"The DataFrame head is:\n{df.head().to_markdown(index=False)}\n"
            f"The DataFrame info is:\n{df_info_str.splitlines()[-3]}\n" # Use splitlines() for robustness
            f"And column names are:\n{df.columns.tolist()}\n"
            f"The user's question is: '{user_question}'.\n\n"
            f"Based on the data and the question, provide a detailed natural language answer. "
            f"If a numerical answer, summary, or specific data extraction is requested, provide it. "
            f"If a visualization would be helpful, suggest a type of chart (e.g., 'bar chart', 'line chart', 'scatter plot') and the columns to use for X and Y axes (and optionally color/grouping). "
            f"For example: {{ \"response\": \"Here is the average salary.\", \"chart_suggestion\": {{ \"type\": \"bar chart\", \"x\": \"Department\", \"y\": \"Average Salary\" }} }}\n\n"
            f"Your response MUST be in JSON format with two keys: 'response' (string) and 'chart_suggestion' (object or null). "
            f"The 'chart_suggestion' object should contain 'type', 'x', 'y', and optionally 'color'. "
            f"If no chart is suitable, set 'chart_suggestion' to null. "
            f"CRITICAL: The 'response' field MUST be a clear, concise, and user-friendly natural language answer to the user's question. Do NOT include any JSON syntax or formatting directly in the 'response' field. Focus on explaining the data in an accessible way." 
        )

        llm_output = self._generate_response_with_llm(initial_prompt)
        
        # Post-process LLM output to ensure clean JSON or plain text
        cleaned_output = llm_output.strip()
        if cleaned_output.startswith('json '):
            cleaned_output = cleaned_output[len('json '):].strip()

        try:
            parsed_output = json.loads(cleaned_output)
            response_text = parsed_output.get("response", "I could not generate a clear natural language response from the AI.")
            chart_suggestion = parsed_output.get("chart_suggestion", None)
            
            # Final check to ensure response_text doesn't contain any JSON artifacts
            if isinstance(response_text, str) and response_text.startswith('{') and '"response":' in response_text:
                try:
                    temp_parsed_res = json.loads(response_text)
                    response_text = temp_parsed_res.get("response", "I could not generate a clear natural language response.")
                except json.JSONDecodeError:
                    pass # Keep original response_text if it's not valid JSON

            return {"response": response_text.strip(), "chart_suggestion": chart_suggestion}
        except json.JSONDecodeError:
            # If JSON decoding fails completely, try to extract response from a raw string
            response_text = cleaned_output # Default to full output
            if '"response":' in cleaned_output:
                try:
                    # More robust regex-like extraction for malformed JSON strings
                    match = re.search(r'"response":\s*"([^"]*)"', cleaned_output)
                    if match:
                        response_text = match.group(1)
                except Exception:
                    pass

            return {"response": response_text.strip(), "chart_suggestion": None}
