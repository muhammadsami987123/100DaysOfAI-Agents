
import argparse
import json
import os
import re
from docx import Document
from pypdf import PdfReader
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Generative AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash-001')

class ResumeParserAgent:
    def __init__(self):
        self.resume_text = ""
        self.parsed_data = {}

    def greet_user(self):
        print("Hello! I am ResumeParserAgent, your AI HR assistant.")
        print("My job is to extract, structure, and summarize candidate information from resumes.")
        print("I support multiple formats like .pdf, .docx, and .txt.")
        print("\nPlease upload a resume file to begin parsing, or paste the resume text directly.")
        print("Enter 'file <path_to_file>' or 'text <your_resume_text>':")

    def get_input(self):
        user_input = input("> ").strip()
        if user_input.startswith("file "):
            file_path = user_input.split(" ", 1)[1]
            self.resume_text = self._read_file(file_path)
        elif user_input.startswith("text "):
            self.resume_text = user_input.split(" ", 1)[1]
        else:
            print("Invalid input. Please start with 'file ' or 'text '.")
            self.get_input()

    def _read_file(self, file_path):
        if not os.path.exists(file_path):
            print(f"Error: File not found at {file_path}")
            return ""

        _, file_extension = os.path.splitext(file_path)
        file_extension = file_extension.lower()

        if file_extension == ".pdf":
            return self._read_pdf(file_path)
        elif file_extension == ".docx":
            return self._read_docx(file_path)
        elif file_extension == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            print(f"Error: Unsupported file type: {file_extension}")
            return ""

    def _read_pdf(self, file_path):
        text = ""
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                text += page.extract_text() or ""
        except Exception as e:
            print(f"Error reading PDF: {e}")
        return text

    def _read_docx(self, file_path):
        text = ""
        try:
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            print(f"Error reading DOCX: {e}")
        return text

    def parse_resume(self):
        if not self.resume_text:
            print("No resume text to parse.")
            return

        prompt = f"""
        Extract the following information from the resume text below and return it as a clean JSON object.
        If a field is not found, use an empty string or empty array as appropriate.

        Resume Text:
        ---
        {self.resume_text}
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
            response = model.generate_content(prompt)
            # Attempt to extract JSON from the response text
            json_match = re.search(r"```json\n([\s\S]*?)\n```", response.text)
            if json_match:
                json_string = json_match.group(1)
                self.parsed_data = json.loads(json_string)
            else:
                # If no code block, try to parse the entire response as JSON
                self.parsed_data = json.loads(response.text)
        except Exception as e:
            print(f"Error parsing resume with AI model: {e}")
            self.parsed_data = {"error": str(e), "raw_response": response.text if response else "No response"}

    def summarize_resume(self):
        if not self.resume_text:
            return "No resume text to summarize."
        prompt = f"Summarize the following resume in 3-5 lines:\n\n{self.resume_text}"
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error summarizing resume: {e}"

    def extract_skills_only(self):
        if not self.resume_text:
            return "No resume text to extract skills from."
        prompt = f"Extract only the technical and soft skills from the following resume and list them as a JSON array:\n\n{self.resume_text}"
        try:
            response = model.generate_content(prompt)
            # Attempt to extract JSON array from the response text
            json_match = re.search(r"\[([\s\S]*?)\]", response.text)
            if json_match:
                skills_list_str = "[" + json_match.group(0) + "]" # Ensure it's a valid JSON array string
                return json.dumps(json.loads(skills_list_str), indent=2)
            else:
                # If no code block, try to parse the entire response as JSON
                return json.dumps(json.loads(response.text), indent=2)
        except Exception as e:
            return f"Error extracting skills: {e}"

    def validate_fields(self):
        missing_fields = []
        key_fields = ["full_name", "email", "phone_number"]
        for field in key_fields:
            if not self.parsed_data.get(field):
                missing_fields.append(field)
        if missing_fields:
            return f"Missing key fields: {', '.join(missing_fields)}"
        else:
            return "All key fields are present."

    def save_json_output(self, filename="resume_parsed.json"):
        if self.parsed_data:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.parsed_data, f, indent=4)
            print(f"Parsed data saved to {filename}")
        else:
            print("No data to save.")

def main():
    parser = argparse.ArgumentParser(description="ResumeParserAgent - CLI-based AI HR Assistant")
    parser.add_argument("--summary", action="store_true", help="Summarize the resume in 3-5 lines.")
    parser.add_argument("--skills-only", action="store_true", help="Extract only technical and soft skills.")
    parser.add_argument("--json", action="store_true", help="Save parsed output as resume_parsed.json.")
    parser.add_argument("--validate", action="store_true", help="Check if key fields are missing.")

    args = parser.parse_args()

    agent = ResumeParserAgent()
    agent.greet_user()
    agent.get_input()

    if not agent.resume_text:
        print("No resume content provided. Exiting.")
        return

    if args.summary:
        print("\n--- Resume Summary ---")
        print(agent.summarize_resume())
    elif args.skills_only:
        print("\n--- Skills Only ---")
        print(agent.extract_skills_only())
    else:
        agent.parse_resume()
        if agent.parsed_data:
            print("\n--- Parsed Resume Data ---")
            print(json.dumps(agent.parsed_data, indent=4))

            if args.json:
                agent.save_json_output()
            if args.validate:
                print("\n--- Validation Result ---")
                print(agent.validate_fields())
        else:
            print("Failed to parse resume.")

if __name__ == "__main__":
    main()
