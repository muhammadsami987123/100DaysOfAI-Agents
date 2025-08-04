"""
Configuration and setup for EmailWriterAgent
"""

import os
from typing import Optional

def get_api_key() -> Optional[str]:
    """Get OpenAI API key from environment variable or .env file"""
    # Try environment variable first
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return api_key
    
    # Try .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            return api_key
    except ImportError:
        pass
    
    return None

def setup_instructions():
    """Display setup instructions for API key"""
    print("🔧 Setup Instructions:")
    print("1. Get your OpenAI API key from: https://platform.openai.com/api-keys")
    print("2. Set the API key using one of these methods:")
    print("   Option A: Set environment variable:")
    print("     Windows: set OPENAI_API_KEY=your_api_key_here")
    print("     Linux/Mac: export OPENAI_API_KEY=your_api_key_here")
    print("   Option B: Create a .env file in the project root:")
    print("     OPENAI_API_KEY=your_api_key_here")
    print("   Option C: Create a config.json file:")
    print("     {\"openai_api_key\": \"your_api_key_here\"}")
    print()
    print("📧 After setting up the API key, run:")
    print("   python main.py --web        # Start web interface")
    print("   python main.py --terminal   # Start terminal interface")
    print("   python main.py --quick \"your prompt\"  # Quick email generation")

class EmailConfig:
    """Configuration constants for EmailWriterAgent"""
    
    # Email templates
    TEMPLATES = {
        "formal": {
            "name": "Formal Business",
            "description": "Professional business communication",
            "tone": "formal",
            "greeting": "Dear {recipient},",
            "closing": "I appreciate your time and consideration.\n\nBest regards,\n{signature}"
        },
        "casual": {
            "name": "Casual Professional",
            "description": "Friendly but professional tone",
            "tone": "casual",
            "greeting": "Hi {recipient},",
            "closing": "Looking forward to connecting with you.\n\nBest,\n{signature}"
        },
        "follow_up": {
            "name": "Follow-up",
            "description": "Follow-up after meeting or conversation",
            "tone": "professional",
            "greeting": "Hi {recipient},",
            "closing": "I look forward to hearing from you and continuing our discussion.\n\nBest regards,\n{signature}"
        },
        "thank_you": {
            "name": "Thank You",
            "description": "Express gratitude professionally",
            "tone": "appreciative",
            "greeting": "Dear {recipient},",
            "closing": "Thank you again for your time and consideration.\n\nBest regards,\n{signature}"
        },
        "meeting_request": {
            "name": "Meeting Request",
            "description": "Request for a meeting or call",
            "tone": "professional",
            "greeting": "Dear {recipient},",
            "closing": "I look forward to your response and the opportunity to connect.\n\nBest regards,\n{signature}"
        },
        "urgent": {
            "name": "Urgent",
            "description": "Time-sensitive communication",
            "tone": "urgent",
            "greeting": "Dear {recipient},",
            "closing": "I appreciate your prompt attention to this matter.\n\nBest regards,\n{signature}"
        }
    }
    
    # Default email settings
    DEFAULT_FROM = "your.email@example.com"
    DEFAULT_SIGNATURE = "Your Name\nYour Title\nYour Company"
    
    # GPT settings
    MAX_TOKENS = 1000
    TEMPERATURE = 0.7
    
    # Web interface settings
    WEB_TITLE = "EmailWriterAgent"
    WEB_DESCRIPTION = "AI-powered email composition tool"
    WEB_VERSION = "1.0.0" 