import json
import re
import google.generativeai as genai
from typing import Dict, Any, List, Optional

class ResumeExtractor:
    def __init__(self, gemini_config):
        self.gemini_config = gemini_config
        genai.configure(api_key=self.gemini_config.api_key)
        self.model = genai.GenerativeModel(self.gemini_config.get_model_name())

    def parse_resume(self, resume_text: str) -> Dict[str, Any]:
        if not resume_text:
            return {"error": "No resume text provided for parsing."}

        prompt = f"""
        Extract the following information from the resume text below and return it as a clean JSON object.
        If a field is not found, use an empty string or empty array as appropriate.

        Resume Text:
        ---
        {resume_text}
        ---

        Extract:
        - Full Name
        - Email
        - Phone Number
        - LinkedIn/GitHub (provide URLs if available)
        - Education (list of objects with Institute, Degree, Years)
        - Work Experience (list of objects with Job Title, Company, Duration)
        - Skills (Technical and Soft Skills, as a list)
        - Certifications / Projects (as a list if available)

        Example JSON structure:
        {{
            "full_name": "",
            "email": "",
            "phone_number": "",
            "linkedin_github": [],
            "education": [
                {{"institute": "", "degree": "", "years": ""}}
            ],
            "work_experience": [
                {{"job_title": "", "company": "", "duration": ""}}
            ],
            "skills": [],
            "certifications_projects": []
        }}
        """
        try:
            response = self.model.generate_content(prompt)
            json_match = re.search(r"```json\n([\s\S]*?)\n```", response.text)
            if json_match:
                json_string = json_match.group(1)
                return json.loads(json_string)
            else:
                return json.loads(response.text)
        except Exception as e:
            return {"error": str(e), "raw_response": response.text if response else "No response"}

    def summarize_resume(self, resume_text: str) -> str:
        if not resume_text:
            return "No resume text to summarize."
        prompt = f"Summarize the following resume in 3-5 lines:\n\n{resume_text}"
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error summarizing resume: {e}"

    def extract_skills_only(self, resume_text: str) -> Optional[List[str]]:
        if not resume_text:
            return None
        prompt = f"Extract only the technical and soft skills from the following resume and list them as a JSON array:\n\n{resume_text}"
        try:
            response = self.model.generate_content(prompt)
            json_match = re.search(r"\[([\s\S]*?)\]", response.text)
            if json_match:
                # Ensure it's a valid JSON array string by wrapping in brackets if needed
                skills_list_str = json_match.group(0)
                return json.loads(skills_list_str)
            else:
                return json.loads(response.text)
        except Exception as e:
            print(f"Error extracting skills: {e}")
            return None
