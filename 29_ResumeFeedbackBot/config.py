import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration settings for ResumeFeedbackBot"""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4')
    OPENAI_MAX_TOKENS = int(os.getenv('OPENAI_MAX_TOKENS', '4000'))
    OPENAI_TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'resume-feedback-bot-secret-key-2024')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    HOST = os.getenv('HOST', '127.0.0.1')
    PORT = int(os.getenv('PORT', '5000'))
    
    # File Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}
    
    # Output Configuration
    OUTPUT_FOLDER = 'outputs'
    LOGS_FOLDER = 'logs'
    
    # Resume Analysis Configuration
    RESUME_SECTIONS = [
        'summary', 'experience', 'education', 'skills', 
        'projects', 'certifications', 'languages', 'interests'
    ]
    
    # Portfolio Analysis Configuration
    PORTFOLIO_ANALYSIS_DEPTH = 3  # Number of pages to analyze
    
    # Rating System Configuration
    RATING_CRITERIA = [
        'clarity', 'relevance', 'professionalism', 'structure',
        'grammar', 'achievements', 'skills_alignment', 'overall_impact'
    ]
    
    # Job Role Matching
    DEFAULT_INDUSTRIES = [
        'Technology', 'Healthcare', 'Finance', 'Education', 
        'Marketing', 'Sales', 'Engineering', 'Design', 
        'Consulting', 'Non-profit', 'Government', 'Other'
    ]
    
    # AI Prompt Templates
    RESUME_ANALYSIS_PROMPT = """
    You are an expert resume reviewer with 15+ years of experience in HR and recruitment.
    Analyze the following resume and provide detailed, actionable feedback.
    
    Resume Content:
    {resume_text}
    
    Target Job Role: {target_role}
    Industry: {industry}
    
    Please provide feedback in the following JSON format:
    {{
        "overall_score": 8.5,
        "scores": {{
            "clarity": 8,
            "relevance": 9,
            "professionalism": 8,
            "structure": 7,
            "grammar": 9,
            "achievements": 8,
            "skills_alignment": 9,
            "overall_impact": 8
        }},
        "strengths": [
            "Clear and concise summary",
            "Quantified achievements in experience section"
        ],
        "weaknesses": [
            "Missing specific metrics in some achievements",
            "Skills section could be more targeted"
        ],
        "suggestions": [
            "Add specific numbers to quantify achievements",
            "Reorganize skills by relevance to target role"
        ],
        "section_analysis": {{
            "summary": {{
                "score": 8,
                "feedback": "Good overview but could be more specific",
                "suggestions": ["Add target role", "Include key achievements"]
            }},
            "experience": {{
                "score": 8,
                "feedback": "Well-structured with good achievements",
                "suggestions": ["Add more metrics", "Use action verbs"]
            }}
        }},
        "improved_summary": "Experienced software engineer with 5+ years...",
        "improved_experience": [
            "Led development team of 8 engineers...",
            "Increased system performance by 40%..."
        ]
    }}
    """
    
    PORTFOLIO_ANALYSIS_PROMPT = """
    You are an expert web designer and UX consultant.
    Analyze the following portfolio website and provide detailed feedback.
    
    Portfolio URL: {portfolio_url}
    Website Content: {website_content}
    
    Please provide feedback in the following JSON format:
    {{
        "overall_score": 8.0,
        "scores": {{
            "design": 8,
            "usability": 7,
            "content": 9,
            "performance": 8,
            "mobile_responsiveness": 7,
            "professionalism": 8
        }},
        "strengths": [
            "Clean and modern design",
            "Clear project showcases"
        ],
        "weaknesses": [
            "Slow loading times",
            "Limited mobile optimization"
        ],
        "suggestions": [
            "Optimize images for faster loading",
            "Improve mobile navigation"
        ],
        "technical_recommendations": [
            "Compress images",
            "Add lazy loading",
            "Improve CSS for mobile"
        ]
    }}
    """
    
    @staticmethod
    def validate_config():
        """Validate configuration settings"""
        errors = []
        
        if not Config.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is required")
        
        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER)
        
        if not os.path.exists(Config.OUTPUT_FOLDER):
            os.makedirs(Config.OUTPUT_FOLDER)
        
        if not os.path.exists(Config.LOGS_FOLDER):
            os.makedirs(Config.LOGS_FOLDER)
        
        return errors
