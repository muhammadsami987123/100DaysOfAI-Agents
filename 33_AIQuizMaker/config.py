#!/usr/bin/env python3
"""
Configuration file for AI Quiz Maker

This file manages API keys, configuration settings, and environment variables.
You can either:
1. Set your OpenAI API key in this file directly
2. Use environment variables
3. Use a .env file in your home directory
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file in home directory
home_dir = os.path.expanduser("~")
env_file = os.path.join(home_dir, ".env")
if os.path.exists(env_file):
    load_dotenv(env_file)

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')

# Flask Configuration
FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

# Quiz Configuration
DEFAULT_QUESTIONS = int(os.getenv('DEFAULT_QUESTIONS', 5))
DEFAULT_DIFFICULTY = os.getenv('DEFAULT_DIFFICULTY', 'medium')
DEFAULT_FORMAT = os.getenv('DEFAULT_FORMAT', 'md')

# Supported formats and difficulties
SUPPORTED_FORMATS = ['md', 'json', 'csv']
SUPPORTED_DIFFICULTIES = ['easy', 'medium', 'hard']

# File paths
UPLOADS_DIR = os.path.join(os.path.dirname(__file__), 'uploads')
OUTPUTS_DIR = os.path.join(os.path.dirname(__file__), 'outputs')
QUIZES_DIR = os.path.join(os.path.dirname(__file__), 'quizzes')

# Create directories if they don't exist
for directory in [UPLOADS_DIR, OUTPUTS_DIR, QUIZES_DIR]:
    os.makedirs(directory, exist_ok=True)

def get_api_key():
    """Get the OpenAI API key from various sources."""
    # First check if it's set in this file
    if 'OPENAI_API_KEY' in globals() and OPENAI_API_KEY:
        return OPENAI_API_KEY
    
    # Then check environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        return api_key
    
    return None

def validate_config():
    """Validate the configuration and return any issues."""
    issues = []
    
    if not get_api_key():
        issues.append("OpenAI API key not found")
    
    if OPENAI_MODEL not in ['gpt-3.5-turbo', 'gpt-4', 'gpt-4o-mini']:
        issues.append(f"Unsupported OpenAI model: {OPENAI_MODEL}")
    
    if DEFAULT_DIFFICULTY not in SUPPORTED_DIFFICULTIES:
        issues.append(f"Unsupported difficulty: {DEFAULT_DIFFICULTY}")
    
    if DEFAULT_FORMAT not in SUPPORTED_FORMATS:
        issues.append(f"Unsupported format: {DEFAULT_FORMAT}")
    
    return issues

def setup_instructions():
    """Print setup instructions."""
    print("🔧 AI Quiz Maker Setup Instructions:")
    print("=" * 50)
    print()
    print("To set up your OpenAI API key, choose one of these methods:")
    print()
    print("1. Create a .env file in your home directory:")
    print(f"   Create file: {os.path.expanduser('~')}/.env")
    print("   Add this line: OPENAI_API_KEY=your_actual_api_key_here")
    print()
    print("2. Set environment variable:")
    print("   Windows: set OPENAI_API_KEY=your_actual_api_key_here")
    print("   macOS/Linux: export OPENAI_API_KEY=your_actual_api_key_here")
    print()
    print("3. Pass as command line argument:")
    print("   python main.py --api-key your_actual_api_key_here")
    print()
    print("4. Edit this config.py file (not recommended for security)")
    print()
    print("Get your API key from: https://platform.openai.com/api-keys")
    print()
    print("💡 Quick Setup (Windows):")
    print("   set OPENAI_API_KEY=your_api_key_here")
    print("   python main.py")
    print()
    print("💡 Quick Setup (macOS/Linux):")
    print("   export OPENAI_API_KEY=your_api_key_here")
    print("   python main.py")
    print()
    print("🔧 Configuration Options:")
    print(f"   Default Questions: {DEFAULT_QUESTIONS}")
    print(f"   Default Difficulty: {DEFAULT_DIFFICULTY}")
    print(f"   Default Format: {DEFAULT_FORMAT}")
    print(f"   OpenAI Model: {OPENAI_MODEL}")
    print(f"   Flask Port: {FLASK_PORT}")
    print(f"   Flask Debug: {FLASK_DEBUG}")
    print("=" * 50)

def get_quiz_prompt_template():
    """Get the quiz generation prompt template."""
    return """You are an expert quiz creator. Create a {num_questions} question multiple choice quiz about the following topic/content.

Topic/Content: {content}

Requirements:
- Difficulty: {difficulty}
- Number of questions: {num_questions}
- Each question should have 4 options (A, B, C, D)
- Only one correct answer per question
- Include the correct answer for each question
- Make questions engaging and educational
- Vary question types (concepts, examples, scenarios)
- Ensure all options are plausible but only one is correct

IMPORTANT: Follow this EXACT format for each question:

1. [Question text here]
   A) [Option A text here]
   B) [Option B text here]
   C) [Option C text here]
   D) [Option D text here]
   Answer: [A, B, C, or D]

2. [Question text here]
   A) [Option A text here]
   B) [Option B text here]
   C) [Option C text here]
   D) [Option D text here]
   Answer: [A, B, C, or D]

Continue this pattern for all {num_questions} questions. Do not add any extra text, explanations, or formatting beyond the questions and answers."""

def get_quiz_validation_prompt():
    """Get the prompt for validating quiz format."""
    return """You are a quiz validator. Review the following quiz and ensure it meets these requirements:

1. Exactly {num_questions} questions
2. Each question has exactly 4 options (A, B, C, D)
3. Each question has a clear answer marked
4. Questions are appropriate for {difficulty} difficulty
5. All options are plausible but only one is correct

If the quiz meets all requirements, return "VALID" followed by the quiz.
If there are issues, return "INVALID" followed by a corrected version.

Quiz to validate:
{quiz_content}"""

if __name__ == "__main__":
    # Test configuration
    print("🔧 Testing AI Quiz Maker Configuration...")
    issues = validate_config()
    
    if issues:
        print("❌ Configuration issues found:")
        for issue in issues:
            print(f"   - {issue}")
        print()
        setup_instructions()
    else:
        print("✅ Configuration is valid!")
        print(f"   API Key: {'✅ Set' if get_api_key() else '❌ Not set'}")
        print(f"   Model: {OPENAI_MODEL}")
        print(f"   Port: {FLASK_PORT}")
        print(f"   Debug: {FLASK_DEBUG}")
