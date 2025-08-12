"""
Main AI agent for job application generation
"""

import json
import logging
from typing import Dict, List, Optional, Any
import openai
from openai import OpenAI

from config import (
    OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE, OPENAI_MAX_TOKENS,
    PROMPT_TEMPLATES, ERROR_MESSAGES, SUPPORTED_LANGUAGES, ADDITIONAL_DOCUMENTS
)
from document_processor import DocumentProcessor, JobDescriptionProcessor
from url_extractor import JobURLExtractor

logger = logging.getLogger(__name__)


class JobApplicationAgent:
    """Main AI agent for generating job applications"""
    
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError(ERROR_MESSAGES["no_api_key"])
        
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.document_processor = DocumentProcessor()
        self.job_processor = JobDescriptionProcessor()
        self.url_extractor = JobURLExtractor()
        
    def generate_application(
        self,
        resume_file_path: str,
        job_description: str,
        language: str = "en",
        cover_letter_length: str = "medium",
        additional_documents: List[str] = None
    ) -> Dict[str, Any]:
        """Generate complete job application package"""
        try:
            # Validate inputs
            self._validate_inputs(resume_file_path, job_description, language)
            
            # Process resume
            logger.info("Processing resume...")
            resume_text = self.document_processor.extract_text_from_file(resume_file_path)
            resume_analysis = self.document_processor.analyze_resume(resume_text)
            
            # Process job description
            logger.info("Processing job description...")
            job_analysis = self.job_processor.analyze_job_description(job_description)
            
            # Generate customized resume
            logger.info("Generating customized resume...")
            customized_resume = self._generate_customized_resume(
                resume_analysis, job_analysis, language
            )
            
            # Generate cover letter
            logger.info("Generating cover letter...")
            cover_letter = self._generate_cover_letter(
                resume_analysis, job_analysis, language, cover_letter_length
            )
            
            # Generate additional documents
            additional_content = {}
            if additional_documents:
                logger.info("Generating additional documents...")
                for doc_type in additional_documents:
                    if doc_type in ADDITIONAL_DOCUMENTS:
                        try:
                            content = self._generate_additional_document(
                                doc_type, resume_analysis, job_analysis, language, cover_letter_length
                            )
                            additional_content[doc_type] = content
                        except Exception as e:
                            logger.error(f"Failed to generate {doc_type}: {e}")
                            additional_content[doc_type] = f"Error generating {ADDITIONAL_DOCUMENTS[doc_type]}: {str(e)}"
            
            # Generate fit analysis
            logger.info("Generating fit analysis...")
            fit_summary = self._generate_fit_analysis(
                resume_analysis, job_analysis, language
            )
            
            return {
                "success": True,
                "data": {
                    "customized_resume": customized_resume,
                    "cover_letter": cover_letter,
                    "additional_documents": additional_content,
                    "fit_summary": fit_summary,
                    "resume_analysis": resume_analysis,
                    "job_analysis": job_analysis
                }
            }
            
        except Exception as e:
            logger.error(f"Application generation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def extract_job_from_url(self, url: str) -> Dict[str, Any]:
        """Extract job description from URL"""
        try:
            result = self.url_extractor.extract_job_description(url)
            return result
        except Exception as e:
            logger.error(f"URL extraction failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _validate_inputs(self, resume_file_path: str, job_description: str, language: str):
        """Validate input parameters"""
        if not resume_file_path:
            raise ValueError(ERROR_MESSAGES["missing_resume"])
        
        if not job_description or len(job_description.strip()) < 50:
            raise ValueError(ERROR_MESSAGES["missing_job_description"])
        
        if language not in SUPPORTED_LANGUAGES:
            raise ValueError(ERROR_MESSAGES["invalid_language"])
    
    def _generate_customized_resume(
        self,
        resume_analysis: Dict,
        job_analysis: Dict,
        language: str
    ) -> str:
        """Generate customized resume using AI"""
        try:
            prompt = PROMPT_TEMPLATES["customized_resume"].format(
                resume_analysis=json.dumps(resume_analysis, indent=2),
                job_analysis=json.dumps(job_analysis, indent=2),
                language=SUPPORTED_LANGUAGES.get(language, "English")
            )
            
            response = self._call_openai(prompt, "Generate a professional, customized resume")
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Resume generation failed: {e}")
            raise ValueError("Failed to generate customized resume")
    
    def _generate_cover_letter(
        self,
        resume_analysis: Dict,
        job_analysis: Dict,
        language: str,
        length: str
    ) -> str:
        """Generate personalized cover letter using AI"""
        try:
            # Map length to word count
            length_mapping = {
                "short": "150-200 words",
                "medium": "250-350 words", 
                "long": "400-500 words"
            }
            
            word_count = length_mapping.get(length, "250-350 words")
            
            prompt = PROMPT_TEMPLATES["cover_letter"].format(
                resume_analysis=json.dumps(resume_analysis, indent=2),
                job_analysis=json.dumps(job_analysis, indent=2),
                length=word_count,
                language=SUPPORTED_LANGUAGES.get(language, "English")
            )
            
            response = self._call_openai(prompt, "Generate a compelling, personalized cover letter")
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Cover letter generation failed: {e}")
            raise ValueError("Failed to generate cover letter")
    
    def _generate_additional_document(
        self,
        doc_type: str,
        resume_analysis: Dict,
        job_analysis: Dict,
        language: str,
        length: str
    ) -> str:
        """Generate additional document using AI"""
        try:
            if doc_type not in PROMPT_TEMPLATES:
                raise ValueError(f"Unsupported document type: {doc_type}")
            
            # Map length to word count for motivation letter
            length_mapping = {
                "short": "150-200 words",
                "medium": "250-350 words", 
                "long": "400-500 words"
            }
            word_count = length_mapping.get(length, "250-350 words")
            
            prompt = PROMPT_TEMPLATES[doc_type].format(
                resume_analysis=json.dumps(resume_analysis, indent=2),
                job_analysis=json.dumps(job_analysis, indent=2),
                length=word_count,
                language=SUPPORTED_LANGUAGES.get(language, "English")
            )
            
            system_message = f"Generate a professional {ADDITIONAL_DOCUMENTS[doc_type].lower()}"
            response = self._call_openai(prompt, system_message)
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"{doc_type} generation failed: {e}")
            raise ValueError(f"Failed to generate {ADDITIONAL_DOCUMENTS[doc_type]}")
    
    def _generate_fit_analysis(
        self,
        resume_analysis: Dict,
        job_analysis: Dict,
        language: str
    ) -> Dict[str, Any]:
        """Generate job fit analysis using AI"""
        try:
            prompt = PROMPT_TEMPLATES["fit_analysis"].format(
                resume_analysis=json.dumps(resume_analysis, indent=2),
                job_analysis=json.dumps(job_analysis, indent=2),
                language=SUPPORTED_LANGUAGES.get(language, "English")
            )
            
            response = self._call_openai(prompt, "Analyze job fit and provide structured analysis")
            
            # Parse JSON response
            try:
                fit_data = json.loads(response)
                return fit_data
            except json.JSONDecodeError:
                # Fallback to structured parsing if JSON parsing fails
                return self._parse_fit_analysis_fallback(response)
                
        except Exception as e:
            logger.error(f"Fit analysis generation failed: {e}")
            return self._generate_default_fit_analysis(resume_analysis, job_analysis)
    
    def _call_openai(self, prompt: str, system_message: str) -> str:
        """Make API call to OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                temperature=OPENAI_TEMPERATURE,
                max_tokens=OPENAI_MAX_TOKENS
            )
            
            return response.choices[0].message.content
            
        except openai.APIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise ValueError(f"AI service error: {e}")
        except Exception as e:
            logger.error(f"OpenAI call failed: {e}")
            raise ValueError("Failed to generate content")
    
    def _parse_fit_analysis_fallback(self, response: str) -> Dict[str, Any]:
        """Fallback parsing for fit analysis when JSON parsing fails"""
        try:
            # Extract match percentage
            import re
            match_pattern = r'(\d+)%'
            match_match = re.search(match_pattern, response)
            match_percentage = int(match_match.group(1)) if match_match else 75
            
            # Extract key strengths (look for bullet points or numbered lists)
            strengths = []
            lines = response.split('\n')
            for line in lines:
                if line.strip().startswith(('•', '-', '*', '1.', '2.', '3.')):
                    strength = line.strip().lstrip('•-*1234567890. ')
                    if strength and len(strength) > 5:
                        strengths.append(strength)
            
            # Extract gap areas
            gap_areas = []
            if "gap" in response.lower() or "improve" in response.lower():
                gap_section = response.lower().split("gap")[-1] if "gap" in response.lower() else ""
                gap_lines = gap_section.split('\n')
                for line in gap_lines:
                    if line.strip().startswith(('•', '-', '*')):
                        gap = line.strip().lstrip('•-* ')
                        if gap and len(gap) > 5:
                            gap_areas.append(gap)
            
            # Generate recommendations
            recommendations = [
                "Review and customize the generated content before submission",
                "Highlight relevant achievements and experiences",
                "Ensure all contact information is current and professional"
            ]
            
            return {
                "match_percentage": match_percentage,
                "key_strengths": strengths[:5] if strengths else ["Strong technical background", "Relevant experience"],
                "gap_areas": gap_areas[:3] if gap_areas else ["Consider adding more specific achievements"],
                "recommendations": recommendations
            }
            
        except Exception as e:
            logger.error(f"Fallback parsing failed: {e}")
            return self._generate_default_fit_analysis({}, {})
    
    def _generate_default_fit_analysis(self, resume_analysis: Dict, job_analysis: Dict) -> Dict[str, Any]:
        """Generate default fit analysis when AI generation fails"""
        # Calculate basic match percentage based on skills overlap
        resume_skills = set(resume_analysis.get("skills", []))
        job_required_skills = set(job_analysis.get("required_skills", []))
        job_preferred_skills = set(job_analysis.get("preferred_skills", []))
        
        all_job_skills = job_required_skills.union(job_preferred_skills)
        
        if all_job_skills:
            match_percentage = min(100, int((len(resume_skills.intersection(all_job_skills)) / len(all_job_skills)) * 100))
        else:
            match_percentage = 75
        
        return {
            "match_percentage": match_percentage,
            "key_strengths": list(resume_skills)[:5] if resume_skills else ["Strong technical background"],
            "gap_areas": list(all_job_skills - resume_skills)[:3] if all_job_skills else ["Consider adding more specific skills"],
            "recommendations": [
                "Review and customize the generated content before submission",
                "Highlight relevant achievements and experiences",
                "Ensure all contact information is current and professional"
            ]
        }
    
    def analyze_resume_only(self, resume_file_path: str) -> Dict[str, Any]:
        """Analyze resume without job description"""
        try:
            resume_text = self.document_processor.extract_text_from_file(resume_file_path)
            analysis = self.document_processor.analyze_resume(resume_text)
            
            return {
                "success": True,
                "data": analysis
            }
            
        except Exception as e:
            logger.error(f"Resume analysis failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def analyze_job_only(self, job_description: str) -> Dict[str, Any]:
        """Analyze job description without resume"""
        try:
            analysis = self.job_processor.analyze_job_description(job_description)
            
            return {
                "success": True,
                "data": analysis
            }
            
        except Exception as e:
            logger.error(f"Job analysis failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported languages"""
        return SUPPORTED_LANGUAGES
    
    def get_cover_letter_lengths(self) -> Dict[str, str]:
        """Get available cover letter length options"""
        return {
            "short": "Short (150-200 words)",
            "medium": "Medium (250-350 words)",
            "long": "Long (400-500 words)"
        }
    
    def get_additional_documents(self) -> Dict[str, str]:
        """Get available additional document types"""
        return ADDITIONAL_DOCUMENTS
    
    def get_supported_job_sites(self) -> Dict[str, str]:
        """Get list of supported job sites for URL extraction"""
        return self.url_extractor.get_supported_sites()
