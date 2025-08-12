"""
Document processing utilities for resume parsing
"""

import os
import json
import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

try:
    from docx import Document
except ImportError:
    Document = None

from config import ALLOWED_EXTENSIONS, ERROR_MESSAGES

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Handles document processing for resumes"""
    
    def __init__(self):
        self.supported_extensions = ALLOWED_EXTENSIONS
    
    def extract_text_from_file(self, file_path: str) -> str:
        """Extract text from PDF or DOCX file"""
        try:
            file_path = Path(file_path)
            extension = file_path.suffix.lower()
            
            if extension not in self.supported_extensions:
                raise ValueError(ERROR_MESSAGES["invalid_file"])
            
            if extension == ".pdf":
                return self._extract_from_pdf(file_path)
            elif extension in [".docx", ".doc"]:
                return self._extract_from_docx(file_path)
            else:
                raise ValueError(ERROR_MESSAGES["invalid_file"])
                
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {e}")
            raise
    
    def _extract_from_pdf(self, file_path: Path) -> str:
        """Extract text from PDF file using PyMuPDF"""
        if not fitz:
            raise ImportError("PyMuPDF is required for PDF processing")
        
        try:
            doc = fitz.open(file_path)
            text = ""
            
            for page in doc:
                text += page.get_text()
            
            doc.close()
            return text.strip()
            
        except Exception as e:
            logger.error(f"PDF extraction error: {e}")
            raise ValueError(ERROR_MESSAGES["processing_failed"])
    
    def _extract_from_docx(self, file_path: Path) -> str:
        """Extract text from DOCX file using python-docx"""
        if not Document:
            raise ImportError("python-docx is required for DOCX processing")
        
        try:
            doc = Document(file_path)
            text = ""
            
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"DOCX extraction error: {e}")
            raise ValueError(ERROR_MESSAGES["processing_failed"])
    
    def analyze_resume(self, text: str) -> Dict:
        """Analyze resume text and extract structured information"""
        try:
            # Basic text cleaning
            cleaned_text = self._clean_text(text)
            
            # Extract sections
            sections = self._extract_sections(cleaned_text)
            
            # Analyze content
            analysis = {
                "contact_info": self._extract_contact_info(cleaned_text),
                "skills": self._extract_skills(cleaned_text),
                "experience": self._extract_experience(sections.get("experience", "")),
                "education": self._extract_education(sections.get("education", "")),
                "summary": self._extract_summary(sections.get("summary", "")),
                "raw_text": cleaned_text
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Resume analysis error: {e}")
            return {"raw_text": text, "error": str(e)}
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = " ".join(text.split())
        
        # Remove special characters that might interfere with parsing
        text = text.replace("\x00", "")
        
        return text
    
    def _extract_sections(self, text: str) -> Dict[str, str]:
        """Extract different sections from resume"""
        sections = {}
        
        # Common section headers
        section_headers = [
            "experience", "work experience", "employment history",
            "education", "academic background", "qualifications",
            "skills", "technical skills", "competencies",
            "summary", "objective", "profile", "about",
            "contact", "personal information"
        ]
        
        lines = text.split("\n")
        current_section = "general"
        current_content = []
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if line is a section header
            is_header = any(header in line_lower for header in section_headers)
            
            if is_header and current_content:
                sections[current_section] = "\n".join(current_content)
                current_section = line_lower
                current_content = []
            else:
                current_content.append(line)
        
        # Add the last section
        if current_content:
            sections[current_section] = "\n".join(current_content)
        
        return sections
    
    def _extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extract contact information"""
        contact_info = {}
        
        # Email pattern
        import re
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            contact_info["email"] = emails[0]
        
        # Phone pattern
        phone_pattern = r'(\+?1?[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
        phones = re.findall(phone_pattern, text)
        if phones:
            contact_info["phone"] = "".join(phones[0])
        
        return contact_info
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume text"""
        # Common skill keywords
        skill_keywords = [
            "python", "javascript", "java", "c++", "c#", "php", "ruby", "go", "rust",
            "html", "css", "react", "angular", "vue", "node.js", "express",
            "django", "flask", "spring", "laravel", "asp.net",
            "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch",
            "aws", "azure", "gcp", "docker", "kubernetes", "jenkins",
            "git", "github", "gitlab", "jira", "agile", "scrum",
            "machine learning", "ai", "data science", "statistics",
            "project management", "leadership", "communication", "teamwork"
        ]
        
        found_skills = []
        text_lower = text.lower()
        
        for skill in skill_keywords:
            if skill in text_lower:
                found_skills.append(skill.title())
        
        return list(set(found_skills))  # Remove duplicates
    
    def _extract_experience(self, experience_text: str) -> List[Dict]:
        """Extract work experience information"""
        experiences = []
        
        if not experience_text:
            return experiences
        
        # Simple extraction - can be enhanced with more sophisticated parsing
        lines = experience_text.split("\n")
        
        for line in lines:
            line = line.strip()
            if line and len(line) > 10:  # Filter out very short lines
                experiences.append({
                    "description": line,
                    "duration": "",
                    "company": "",
                    "title": ""
                })
        
        return experiences[:5]  # Limit to 5 most recent experiences
    
    def _extract_education(self, education_text: str) -> List[Dict]:
        """Extract education information"""
        education = []
        
        if not education_text:
            return education
        
        lines = education_text.split("\n")
        
        for line in lines:
            line = line.strip()
            if line and len(line) > 5:
                education.append({
                    "description": line,
                    "degree": "",
                    "institution": "",
                    "year": ""
                })
        
        return education[:3]  # Limit to 3 most recent education entries
    
    def _extract_summary(self, summary_text: str) -> str:
        """Extract professional summary"""
        if not summary_text:
            return ""
        
        # Take first few sentences as summary
        sentences = summary_text.split(".")
        return ". ".join(sentences[:3]) + "."


class JobDescriptionProcessor:
    """Handles job description processing"""
    
    def analyze_job_description(self, text: str) -> Dict:
        """Analyze job description and extract key information"""
        try:
            cleaned_text = self._clean_text(text)
            
            analysis = {
                "required_skills": self._extract_required_skills(cleaned_text),
                "preferred_skills": self._extract_preferred_skills(cleaned_text),
                "responsibilities": self._extract_responsibilities(cleaned_text),
                "requirements": self._extract_requirements(cleaned_text),
                "company_info": self._extract_company_info(cleaned_text),
                "raw_text": cleaned_text
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Job description analysis error: {e}")
            return {"raw_text": text, "error": str(e)}
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        return " ".join(text.split())
    
    def _extract_required_skills(self, text: str) -> List[str]:
        """Extract required skills from job description"""
        # Keywords that indicate required skills
        required_indicators = ["required", "must have", "essential", "mandatory", "required skills"]
        
        skills = []
        text_lower = text.lower()
        
        # Extract skills mentioned with required indicators
        lines = text.split("\n")
        for line in lines:
            line_lower = line.lower()
            if any(indicator in line_lower for indicator in required_indicators):
                # Extract potential skills from this line
                potential_skills = self._extract_skills_from_line(line)
                skills.extend(potential_skills)
        
        return list(set(skills))
    
    def _extract_preferred_skills(self, text: str) -> List[str]:
        """Extract preferred skills from job description"""
        # Keywords that indicate preferred skills
        preferred_indicators = ["preferred", "nice to have", "bonus", "plus", "advantageous"]
        
        skills = []
        text_lower = text.lower()
        
        lines = text.split("\n")
        for line in lines:
            line_lower = line.lower()
            if any(indicator in line_lower for indicator in preferred_indicators):
                potential_skills = self._extract_skills_from_line(line)
                skills.extend(potential_skills)
        
        return list(set(skills))
    
    def _extract_skills_from_line(self, line: str) -> List[str]:
        """Extract skills from a specific line"""
        # Common technical skills
        technical_skills = [
            "python", "javascript", "java", "c++", "c#", "php", "ruby", "go", "rust",
            "html", "css", "react", "angular", "vue", "node.js", "express",
            "django", "flask", "spring", "laravel", "asp.net",
            "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch",
            "aws", "azure", "gcp", "docker", "kubernetes", "jenkins",
            "git", "github", "gitlab", "jira", "agile", "scrum",
            "machine learning", "ai", "data science", "statistics"
        ]
        
        found_skills = []
        line_lower = line.lower()
        
        for skill in technical_skills:
            if skill in line_lower:
                found_skills.append(skill.title())
        
        return found_skills
    
    def _extract_responsibilities(self, text: str) -> List[str]:
        """Extract job responsibilities"""
        responsibilities = []
        
        # Look for responsibility indicators
        responsibility_indicators = ["responsibilities", "duties", "tasks", "will be responsible"]
        
        lines = text.split("\n")
        in_responsibilities_section = False
        
        for line in lines:
            line_lower = line.lower().strip()
            
            if any(indicator in line_lower for indicator in responsibility_indicators):
                in_responsibilities_section = True
                continue
            
            if in_responsibilities_section and line.strip():
                if line.strip().startswith(("•", "-", "*", "1.", "2.", "3.")):
                    responsibilities.append(line.strip())
                elif len(line.strip()) > 20:  # Likely a responsibility
                    responsibilities.append(line.strip())
        
        return responsibilities[:10]  # Limit to 10 responsibilities
    
    def _extract_requirements(self, text: str) -> List[str]:
        """Extract job requirements"""
        requirements = []
        
        # Look for requirement indicators
        requirement_indicators = ["requirements", "qualifications", "experience", "education"]
        
        lines = text.split("\n")
        in_requirements_section = False
        
        for line in lines:
            line_lower = line.lower().strip()
            
            if any(indicator in line_lower for indicator in requirement_indicators):
                in_requirements_section = True
                continue
            
            if in_requirements_section and line.strip():
                if line.strip().startswith(("•", "-", "*", "1.", "2.", "3.")):
                    requirements.append(line.strip())
                elif len(line.strip()) > 15:  # Likely a requirement
                    requirements.append(line.strip())
        
        return requirements[:8]  # Limit to 8 requirements
    
    def _extract_company_info(self, text: str) -> Dict[str, str]:
        """Extract company information"""
        company_info = {}
        
        # Look for company name patterns
        import re
        
        # Common company indicators
        company_indicators = ["about", "company", "organization", "firm", "corporation"]
        
        lines = text.split("\n")
        for line in lines:
            line_lower = line.lower()
            if any(indicator in line_lower for indicator in company_indicators):
                # Extract potential company name
                words = line.split()
                for i, word in enumerate(words):
                    if word.lower() in ["inc", "llc", "corp", "ltd", "company"]:
                        if i > 0:
                            company_info["name"] = " ".join(words[:i+1])
                            break
        
        return company_info
