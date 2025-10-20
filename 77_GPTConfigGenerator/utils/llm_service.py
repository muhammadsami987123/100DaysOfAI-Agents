import os
import json
import yaml
import re
from typing import Optional, Dict, Any, List
from config import Config

class LLMService:
    def __init__(self):
        self.model_choice = Config.LLM_MODEL.lower()
        self.openai_client = None
        self.gemini_model = None
        self._init_clients()

    def _init_clients(self) -> None:
        """Initialize AI clients based on configuration"""
        if self.model_choice == "openai" and Config.OPENAI_API_KEY:
            try:
                from openai import OpenAI
                self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
            except Exception as e:
                print(f"Error initializing OpenAI client: {e}")
                self.openai_client = None
        elif self.model_choice == "gemini" and Config.GEMINI_API_KEY:
            try:
                import google.generativeai as genai
                genai.configure(api_key=Config.GEMINI_API_KEY)
                self.gemini_model = genai.GenerativeModel(Config.GEMINI_MODEL)
            except Exception as e:
                print(f"Error initializing Gemini client: {e}")
                self.gemini_model = None

    def _build_config_prompt(self, user_request: str, config_type: str = "auto", format: str = "json") -> str:
        """Build the prompt for config generation"""
        prompt = f"""You are GPTConfigGenerator, a specialized AI agent that generates structured configuration files from natural language instructions.

User Request: {user_request}

Instructions:
1. Generate a valid {format.upper()} configuration file based on the user's request
2. Use proper syntax, indentation, and formatting for {format.upper()}
3. Add helpful inline comments where appropriate
4. Use sensible default values for common settings
5. If specific values are not mentioned, use placeholder values like "your-api-key" or "localhost"
6. Ensure the configuration is production-ready and follows best practices

Config Type: {config_type}
Output Format: {format.upper()}

Important Guidelines:
- Always return valid {format.upper()} syntax
- Include all necessary fields for the requested configuration
- Add comments explaining complex or important settings
- Use appropriate data types (strings, numbers, booleans, arrays, objects)
- Follow naming conventions for the specific technology/framework

Return ONLY the configuration file content, no additional text or explanations."""
        
        return prompt

    def _clean_config_output(self, text: str, format: str) -> str:
        """Clean and validate the generated configuration"""
        # Remove markdown code blocks if present
        text = re.sub(r'```(?:json|yaml|toml|js|ts)?\s*\n?', '', text, flags=re.IGNORECASE)
        text = re.sub(r'```\s*$', '', text)
        
        # Remove any leading/trailing whitespace
        text = text.strip()
        
        # Try to validate JSON if format is json
        if format.lower() == "json":
            try:
                json.loads(text)
            except json.JSONDecodeError:
                # Try to fix common JSON issues
                text = self._fix_json_issues(text)
        
        return text

    def _fix_json_issues(self, text: str) -> str:
        """Attempt to fix common JSON issues"""
        # Fix trailing commas
        text = re.sub(r',(\s*[}\]])', r'\1', text)
        
        # Fix single quotes to double quotes
        text = re.sub(r"'([^']*)'", r'"\1"', text)
        
        # Fix unquoted keys
        text = re.sub(r'(\w+):', r'"\1":', text)
        
        return text

    def generate_config(self, user_request: str, config_type: str = "auto", format: str = "json") -> Dict[str, Any]:
        """Generate configuration file based on user request"""
        prompt = self._build_config_prompt(user_request, config_type, format)
        
        try:
            if self.model_choice == "openai" and self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model=Config.OPENAI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a configuration file generator. Always return valid, properly formatted configuration files."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=Config.TEMPERATURE,
                    max_tokens=Config.MAX_TOKENS
                )
                content = response.choices[0].message.content
                
            elif self.model_choice == "gemini" and self.gemini_model:
                response = self.gemini_model.generate_content(prompt)
                content = response.text
                
            else:
                return self._get_fallback_config(user_request, format)
            
            # Clean and validate the output
            clean_content = self._clean_config_output(content, format)
            
            return {
                "success": True,
                "config_content": clean_content,
                "format": format,
                "config_type": config_type,
                "user_request": user_request
            }
            
        except Exception as e:
            print(f"Error generating config: {e}")
            return self._get_fallback_config(user_request, format)

    def _get_fallback_config(self, user_request: str, format: str) -> Dict[str, Any]:
        """Provide a practical fallback configuration when AI is unavailable.

        This returns success=True so the UI can still display the generated
        configuration while also including a note about fallback mode.
        """
        request_lower = user_request.lower()

        # Minimal heuristics for useful fallbacks
        if format.lower() == "json":
            # If the user mentions fields like name/age/sex/class, generate a simple JSON structure
            if any(k in request_lower for k in ["student", "name", "age", "sex", "class"]):
                fallback_obj = {
                    "students": [
                        {
                            "name": "John Doe",
                            "age": 18,
                            "sex": "Male",
                            "class": "10-A",
                            "higher": False
                        }
                    ]
                }
                return {
                    "success": True,
                    "config_content": json.dumps(fallback_obj, indent=2),
                    "format": "json",
                    "config_type": "database",
                    "user_request": user_request,
                    "note": "Returned local fallback as AI service is unavailable."
                }

            # Generic app settings JSON
            fallback_obj = {
                "name": "my-app",
                "version": "1.0.0",
                "port": 3000,
                "host": "localhost",
                "environment": "development",
                "database": {"url": "your-database-url-here"},
                "api": {"key": "your-api-key-here"}
            }
            return {
                "success": True,
                "config_content": json.dumps(fallback_obj, indent=2),
                "format": "json",
                "config_type": "app_settings",
                "user_request": user_request,
                "note": "Returned local fallback as AI service is unavailable."
            }

        if format.lower() == "yaml":
            # Simple docker-compose fallback
            docker_compose = (
                "version: '3.8'\n"
                "services:\n"
                "  app:\n"
                "    image: node:latest\n"
                "    ports:\n"
                "      - '3000:3000'\n"
                "    environment:\n"
                "      - NODE_ENV=development\n"
                "    volumes:\n"
                "      - .:/app\n"
                "    working_dir: /app\n"
                "    command: npm start\n"
            )
            return {
                "success": True,
                "config_content": docker_compose,
                "format": "yaml",
                "config_type": "docker_compose",
                "user_request": user_request,
                "note": "Returned local fallback as AI service is unavailable."
            }

        # Last-resort plain text fallback
        return {
            "success": True,
            "config_content": "{}" if format.lower() == "json" else "# Fallback configuration",
            "format": format,
            "config_type": "custom",
            "user_request": user_request,
            "note": "Returned local fallback as AI service is unavailable."
        }

    def explain_config(self, config_content: str, format: str) -> Dict[str, Any]:
        """Explain a configuration file in natural language"""
        prompt = f"""You are GPTConfigGenerator. Explain the following {format.upper()} configuration file in clear, natural language.

Configuration:
{config_content}

Instructions:
1. Explain what this configuration does
2. Describe each section and key settings
3. Mention any important considerations or best practices
4. Keep the explanation concise but informative

Return a clear explanation in paragraph form."""

        try:
            if self.model_choice == "openai" and self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model=Config.OPENAI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a configuration file expert. Explain configurations clearly and helpfully."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )
                explanation = response.choices[0].message.content
                
            elif self.model_choice == "gemini" and self.gemini_model:
                response = self.gemini_model.generate_content(prompt)
                explanation = response.text
                
            else:
                explanation = f"This appears to be a {format.upper()} configuration file. Please review the settings and adjust as needed for your specific use case."
            
            return {
                "success": True,
                "explanation": explanation.strip()
            }
            
        except Exception as e:
            return {
                "success": False,
                "explanation": f"This appears to be a {format.upper()} configuration file. Please review the settings and adjust as needed for your specific use case.",
                "error": str(e)
            }
