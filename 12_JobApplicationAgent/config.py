"""
Configuration settings for JobApplicationAgent
"""

import os
from typing import Dict, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Server Configuration
PORT = int(os.getenv("PORT", 8012))
HOST = os.getenv("HOST", "0.0.0.0")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "4000"))

# File Upload Configuration
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 10485760))  # 10MB
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc"}
UPLOAD_FOLDER = "uploads"

# Language Configuration
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")

# Supported Languages
SUPPORTED_LANGUAGES: Dict[str, str] = {
    "en": "English",
    "hi": "Hindi",
    "ur": "Urdu",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "ar": "Arabic",
    "pt": "Portuguese",
    "it": "Italian",
    "ru": "Russian",
    "nl": "Dutch",
    "sv": "Swedish",
    "no": "Norwegian",
    "da": "Danish",
    "fi": "Finnish",
    "pl": "Polish",
    "tr": "Turkish"
}

# Cover Letter Length Options
COVER_LETTER_LENGTHS = {
    "short": "Short (150-200 words)",
    "medium": "Medium (250-350 words)",
    "long": "Long (400-500 words)"
}

# Document Generation Settings
RESUME_TEMPLATES = {
    "professional": "Professional",
    "modern": "Modern",
    "creative": "Creative",
    "minimal": "Minimal"
}

# Additional Document Types
ADDITIONAL_DOCUMENTS = {
    "personal_statement": "Personal Statement",
    "reference_page": "Reference Page",
    "thank_you_note": "Thank You Note",
    "motivation_letter": "Motivation Letter",
    "linkedin_bio": "LinkedIn Bio"
}

# AI Prompt Templates
PROMPT_TEMPLATES = {
    "resume_analysis": """
    Analyze the following resume and extract key information:
    - Skills (technical and soft skills)
    - Work experience with achievements
    - Education and certifications
    - Contact information
    - Professional summary
    
    Resume content:
    {resume_content}
    
    Please provide a structured analysis in JSON format.
    """,
    
    "job_analysis": """
    Analyze the following job description and extract key information:
    - Required skills and qualifications
    - Preferred experience
    - Job responsibilities
    - Company information
    - Industry and role type
    
    Job description:
    {job_description}
    
    Please provide a structured analysis in JSON format.
    """,
    
    "customized_resume": """
    Create a customized resume based on the original resume and job requirements.
    
    Original Resume Analysis:
    {resume_analysis}
    
    Job Requirements Analysis:
    {job_analysis}
    
    Instructions:
    1. Tailor the resume to match the job requirements
    2. Highlight relevant skills and experiences
    3. Use action verbs and quantifiable achievements
    4. Maintain professional formatting
    5. Ensure ATS compatibility
    6. Language: {language}
    
    Generate a professional, customized resume.
    """,
    
    "cover_letter": """
    Create a personalized cover letter based on the resume and job description.
    
    Resume Analysis:
    {resume_analysis}
    
    Job Analysis:
    {job_analysis}
    
    Instructions:
    1. Address the hiring manager professionally
    2. Explain why you're interested in the position
    3. Highlight relevant skills and experiences
    4. Show enthusiasm for the company
    5. Include a call to action
    6. Length: {length}
    7. Language: {language}
    
    Generate a compelling, personalized cover letter.
    """,
    
    "personal_statement": """
    Create a personal statement based on the resume and job description.
    
    Resume Analysis:
    {resume_analysis}
    
    Job Analysis:
    {job_analysis}
    
    Instructions:
    1. Write a compelling personal statement that showcases your unique value proposition
    2. Connect your background to the job requirements
    3. Demonstrate your passion and motivation for the role
    4. Include specific examples of achievements and growth
    5. Keep it concise and impactful (300-500 words)
    6. Language: {language}
    
    Generate a compelling personal statement.
    """,
    
    "reference_page": """
    Create a professional reference page based on the resume.
    
    Resume Analysis:
    {resume_analysis}
    
    Job Analysis:
    {job_analysis}
    
    Instructions:
    1. Create a professional reference page with 3-5 references
    2. Include name, title, company, email, and phone for each reference
    3. Select references who can speak to relevant skills and experiences
    4. Ensure references align with the job requirements
    5. Use professional formatting
    6. Language: {language}
    
    Generate a professional reference page.
    """,
    
    "thank_you_note": """
    Create a thank you note for after an interview.
    
    Resume Analysis:
    {resume_analysis}
    
    Job Analysis:
    {job_analysis}
    
    Instructions:
    1. Write a professional thank you note for after an interview
    2. Express gratitude for the opportunity
    3. Reiterate your interest in the position
    4. Mention specific points from the interview
    5. Keep it concise and professional (150-200 words)
    6. Language: {language}
    
    Generate a professional thank you note.
    """,
    
    "motivation_letter": """
    Create a motivation letter based on the resume and job description.
    
    Resume Analysis:
    {resume_analysis}
    
    Job Analysis:
    {job_analysis}
    
    Instructions:
    1. Write a motivation letter explaining why you want this specific role
    2. Connect your personal and professional goals to the position
    3. Demonstrate your understanding of the company and role
    4. Show enthusiasm and commitment
    5. Include specific examples of relevant experience
    6. Length: {length}
    7. Language: {language}
    
    Generate a compelling motivation letter.
    """,
    
    "linkedin_bio": """
    Create a LinkedIn bio based on the resume and job description.
    
    Resume Analysis:
    {resume_analysis}
    
    Job Analysis:
    {job_analysis}
    
    Instructions:
    1. Create a professional LinkedIn bio that aligns with the target role
    2. Include a compelling headline
    3. Write an engaging summary section
    4. Highlight key skills and achievements
    5. Use relevant keywords for the industry
    6. Keep it concise and professional
    7. Language: {language}
    
    Generate a professional LinkedIn bio.
    """,
    
    "fit_analysis": """
    Analyze the fit between the candidate's resume and the job requirements.
    
    Resume Analysis:
    {resume_analysis}
    
    Job Analysis:
    {job_analysis}
    
    Instructions:
    1. Calculate overall match percentage (0-100)
    2. Identify key strengths that match the job
    3. Identify areas where the candidate could improve
    4. Provide specific recommendations
    5. Language: {language}
    
    Provide analysis in JSON format with:
    - match_percentage (integer)
    - key_strengths (list of strings)
    - gap_areas (list of strings)
    - recommendations (list of strings)
    """
}

# Error Messages
ERROR_MESSAGES = {
    "no_api_key": "OpenAI API key not found. Please set OPENAI_API_KEY in your .env file.",
    "invalid_file": "Invalid file format. Please upload a PDF or DOCX file.",
    "file_too_large": f"File too large. Maximum size is {MAX_FILE_SIZE // 1024 // 1024}MB.",
    "upload_failed": "File upload failed. Please try again.",
    "processing_failed": "Document processing failed. Please check your file and try again.",
    "generation_failed": "Application generation failed. Please try again.",
    "invalid_language": "Unsupported language selected.",
    "missing_resume": "Please upload a resume file.",
    "missing_job_description": "Please enter a job description."
}

# Success Messages
SUCCESS_MESSAGES = {
    "upload_success": "Resume uploaded successfully!",
    "generation_success": "Application generated successfully!",
    "download_success": "Document downloaded successfully!"
}

# Validation Rules
VALIDATION_RULES = {
    "min_job_description_length": 50,
    "max_job_description_length": 10000,
    "min_resume_length": 100,
    "max_resume_length": 50000
}

# File Paths
TEMPLATE_DIR = "templates"
STATIC_DIR = "static"
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

# Create necessary directories
for directory in [UPLOAD_DIR, OUTPUT_DIR]:
    os.makedirs(directory, exist_ok=True)

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "job_agent.log"

# Security Settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Performance Settings
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 300))  # 5 minutes
MAX_CONCURRENT_REQUESTS = int(os.getenv("MAX_CONCURRENT_REQUESTS", 10))

# Feature Flags
ENABLE_VOICE_INPUT = os.getenv("ENABLE_VOICE_INPUT", "False").lower() == "true"
ENABLE_URL_PROCESSING = os.getenv("ENABLE_URL_PROCESSING", "False").lower() == "true"
ENABLE_HISTORY = os.getenv("ENABLE_HISTORY", "False").lower() == "true"
