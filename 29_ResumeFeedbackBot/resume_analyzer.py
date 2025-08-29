import os
import json
import logging
from typing import Dict, List, Optional, Tuple
import PyPDF2
from docx import Document
import openai
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResumeAnalyzer:
    """Handles resume parsing and AI analysis"""
    
    def __init__(self):
        """Initialize the resume analyzer"""
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    def extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from DOCX: {e}")
            raise Exception(f"Failed to extract text from DOCX: {str(e)}")
    
    def extract_text_from_file(self, file_path: str) -> str:
        """Extract text from supported file formats"""
        file_extension = file_path.lower().split('.')[-1]
        
        if file_extension == 'pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_extension in ['docx', 'doc']:
            return self.extract_text_from_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    def analyze_resume(self, resume_text: str, target_role: str = "", industry: str = "") -> Dict:
        """Analyze resume using AI and return detailed feedback"""
        try:
            # Prepare the prompt
            prompt = Config.RESUME_ANALYSIS_PROMPT.format(
                resume_text=resume_text,
                target_role=target_role or "General",
                industry=industry or "General"
            )
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert resume reviewer and career consultant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=Config.OPENAI_MAX_TOKENS,
                temperature=Config.OPENAI_TEMPERATURE
            )
            
            # Parse the response
            content = response.choices[0].message.content
            
            # Try to extract JSON from the response
            try:
                # Find JSON in the response
                start_idx = content.find('{')
                end_idx = content.rfind('}') + 1
                json_str = content[start_idx:end_idx]
                analysis = json.loads(json_str)
            except json.JSONDecodeError:
                # If JSON parsing fails, create a structured response
                analysis = self._create_fallback_analysis(content, resume_text)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing resume: {e}")
            return self._create_error_analysis(str(e))
    
    def _create_fallback_analysis(self, content: str, resume_text: str) -> Dict:
        """Create a fallback analysis when JSON parsing fails"""
        return {
            "overall_score": 7.0,
            "scores": {
                "clarity": 7,
                "relevance": 7,
                "professionalism": 7,
                "structure": 7,
                "grammar": 7,
                "achievements": 7,
                "skills_alignment": 7,
                "overall_impact": 7
            },
            "strengths": ["Resume submitted successfully"],
            "weaknesses": ["AI analysis encountered issues"],
            "suggestions": ["Please review the raw feedback below"],
            "section_analysis": {
                "summary": {
                    "score": 7,
                    "feedback": "Analysis in progress",
                    "suggestions": ["Review content manually"]
                }
            },
            "raw_feedback": content,
            "resume_length": len(resume_text),
            "word_count": len(resume_text.split())
        }
    
    def _create_error_analysis(self, error_message: str) -> Dict:
        """Create an error analysis when AI analysis fails"""
        return {
            "overall_score": 0.0,
            "scores": {
                "clarity": 0,
                "relevance": 0,
                "professionalism": 0,
                "structure": 0,
                "grammar": 0,
                "achievements": 0,
                "skills_alignment": 0,
                "overall_impact": 0
            },
            "strengths": [],
            "weaknesses": [f"Analysis failed: {error_message}"],
            "suggestions": ["Please try again or contact support"],
            "error": True,
            "error_message": error_message
        }
    
    def generate_improved_version(self, resume_text: str, analysis: Dict) -> Dict:
        """Generate an improved version of the resume based on analysis"""
        try:
            prompt = f"""
            Based on the following resume analysis, generate an improved version of the resume.
            
            Original Resume:
            {resume_text}
            
            Analysis:
            {json.dumps(analysis, indent=2)}
            
            Please provide an improved version that addresses the weaknesses and incorporates the suggestions.
            Return the response in JSON format:
            {{
                "improved_resume": "Complete improved resume text",
                "key_improvements": [
                    "List of key improvements made"
                ],
                "summary_changes": "Improved summary section",
                "experience_changes": "Improved experience descriptions"
            }}
            """
            
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert resume writer and career consultant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=Config.OPENAI_MAX_TOKENS,
                temperature=Config.OPENAI_TEMPERATURE
            )
            
            content = response.choices[0].message.content
            
            try:
                start_idx = content.find('{')
                end_idx = content.rfind('}') + 1
                json_str = content[start_idx:end_idx]
                improvements = json.loads(json_str)
            except json.JSONDecodeError:
                improvements = {
                    "improved_resume": content,
                    "key_improvements": ["AI-generated improvements"],
                    "summary_changes": "See improved resume above",
                    "experience_changes": "See improved resume above"
                }
            
            return improvements
            
        except Exception as e:
            logger.error(f"Error generating improved version: {e}")
            return {
                "improved_resume": resume_text,
                "key_improvements": ["Could not generate improvements"],
                "error": True,
                "error_message": str(e)
            }
    
    def save_analysis(self, analysis: Dict, filename: str) -> str:
        """Save analysis results to a JSON file"""
        try:
            output_path = os.path.join(Config.OUTPUT_FOLDER, f"{filename}_analysis.json")
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            return output_path
        except Exception as e:
            logger.error(f"Error saving analysis: {e}")
            raise Exception(f"Failed to save analysis: {str(e)}")
    
    def get_analysis_summary(self, analysis: Dict) -> Dict:
        """Extract key summary information from analysis"""
        return {
            "overall_score": analysis.get("overall_score", 0),
            "top_strengths": analysis.get("strengths", [])[:3],
            "top_weaknesses": analysis.get("weaknesses", [])[:3],
            "key_suggestions": analysis.get("suggestions", [])[:3],
            "has_error": analysis.get("error", False)
        }
