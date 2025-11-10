from typing import Dict, Any, Optional, List
from utils.llm_service import LLMService
from config import Config
import os
import json
from pathlib import Path


class FormFillerBot:
    def __init__(self, llm_service: Optional[LLMService] = None):
        self.llm_service = llm_service or LLMService()
        self.data_file = Config.DATA_FILE
        self._ensure_data_directory()

    def _ensure_data_directory(self):
        """Ensure data directory exists."""
        data_dir = os.path.dirname(self.data_file)
        if data_dir:
            os.makedirs(data_dir, exist_ok=True)
        
        # Initialize data file if it doesn't exist
        if not os.path.exists(self.data_file):
            self._save_user_data(self._get_default_data())

    def _get_default_data(self) -> Dict[str, Any]:
        """Get default user data structure."""
        return {
            "personal_info": {
                "first_name": "",
                "last_name": "",
                "full_name": "",
                "email": "",
                "phone": "",
                "date_of_birth": "",
                "address": "",
                "city": "",
                "state": "",
                "zip_code": "",
                "country": ""
            },
            "professional": {
                "job_title": "",
                "company": "",
                "linkedin": "",
                "github": "",
                "portfolio": "",
                "resume_url": ""
            },
            "education": {
                "degree": "",
                "university": "",
                "graduation_year": ""
            },
            "custom_fields": {}
        }

    def _load_user_data(self) -> Dict[str, Any]:
        """Load user data from local file."""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Merge with default to ensure all fields exist
                    default = self._get_default_data()
                    return self._merge_data(default, data)
            else:
                return self._get_default_data()
        except Exception as e:
            print(f"Error loading user data: {e}")
            return self._get_default_data()

    def _merge_data(self, default: Dict, user_data: Dict) -> Dict:
        """Merge user data with default structure."""
        merged = default.copy()
        for key, value in user_data.items():
            if isinstance(value, dict) and key in merged and isinstance(merged[key], dict):
                merged[key].update(value)
            else:
                merged[key] = value
        return merged

    def _save_user_data(self, data: Dict[str, Any]):
        """Save user data to local file."""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving user data: {e}")
            return False

    def get_user_data(self) -> Dict[str, Any]:
        """Get all user data."""
        return self._load_user_data()

    def update_user_data(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update user data with new values."""
        current_data = self._load_user_data()
        
        # Deep update
        for category, values in updates.items():
            if category in current_data and isinstance(current_data[category], dict):
                current_data[category].update(values)
            else:
                current_data[category] = values
        
        if self._save_user_data(current_data):
            return {"success": True, "data": current_data}
        else:
            return {"success": False, "error": "Failed to save data"}

    def analyze_form_fields(self, form_html: str, form_fields: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze form fields and map them to user data using LLM.
        
        Args:
            form_html: HTML content of the form (for context)
            form_fields: List of form field information with id, name, type, label, placeholder, etc.
        
        Returns:
            Dict with field mappings and suggested values
        """
        user_data = self._load_user_data()
        
        # Prepare field information for LLM
        fields_info = json.dumps(form_fields, indent=2)
        user_data_json = json.dumps(user_data, indent=2)
        
        # Read prompt template
        prompt_template = self.llm_service._read_template("field_mapping_prompt.txt")
        
        if not prompt_template:
            # Fallback prompt if template doesn't exist
            prompt_template = """You are FormFillerBot, an AI that maps form fields to user data.

Form Fields to Analyze:
{fields_info}

Available User Data:
{user_data}

Task: For each form field, determine what data it's asking for and map it to the appropriate field in the user data.

Return a JSON object with this structure:
{{
    "field_mappings": [
        {{
            "field_id": "field identifier",
            "field_name": "field name",
            "suggested_value": "value from user data",
            "confidence": "high|medium|low",
            "data_source": "personal_info.email|personal_info.first_name|etc.",
            "reasoning": "brief explanation"
        }}
    ]
}}

Only include fields that have a match. Use high confidence only when you're very sure."""
        
        # Format prompt
        prompt = prompt_template.replace("{fields_info}", fields_info)
        prompt = prompt.replace("{user_data}", user_data_json)
        
        # Get LLM response
        result = self.llm_service.generate_content(prompt, parse_json=True)
        
        if "error" in result:
            return {"error": result["error"], "field_mappings": []}
        
        # Extract field mappings
        if "field_mappings" in result:
            return {
                "success": True,
                "field_mappings": result["field_mappings"],
                "user_data": user_data
            }
        elif "response" in result:
            # Try to extract JSON from raw response
            try:
                if isinstance(result["response"], str):
                    # Try to parse again
                    parsed = self.llm_service._parse_json_response(result["response"])
                    if "field_mappings" in parsed:
                        return {
                            "success": True,
                            "field_mappings": parsed["field_mappings"],
                            "user_data": user_data
                        }
            except:
                pass
            
            return {
                "success": False,
                "error": "Could not parse field mappings from LLM response",
                "raw_response": result.get("response", "")
            }
        else:
            return {
                "success": False,
                "error": "Unexpected response format from LLM",
                "result": result
            }

    def extract_form_fields(self, form_html: str) -> List[Dict[str, Any]]:
        """
        Extract form field information from HTML.
        This is a simplified version - in a real browser extension, this would be done client-side.
        
        Args:
            form_html: HTML content containing form fields
        
        Returns:
            List of field information dictionaries
        """
        # This is a basic implementation
        # In a real scenario, this would use BeautifulSoup or similar to parse HTML
        # For now, we'll return a structure that the frontend can populate
        return []

    def get_fill_suggestions(self, form_fields: List[Dict[str, Any]], form_html: str = "") -> Dict[str, Any]:
        """
        Get fill suggestions for form fields.
        
        Args:
            form_fields: List of form field information
            form_html: Optional HTML context
        
        Returns:
            Dict with field mappings and values
        """
        return self.analyze_form_fields(form_html, form_fields)

