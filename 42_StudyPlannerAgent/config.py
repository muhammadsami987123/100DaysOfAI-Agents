"""
Configuration and setup for StudyPlannerAgent
"""

import os
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta

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
    print()
    print("📚 After setting up the API key, run:")
    print("   python main.py --web        # Start web interface")
    print("   python main.py --terminal   # Start terminal interface")
    print("   python main.py --quick \"Learn JavaScript\"  # Quick study plan generation")

class StudyConfig:
    """Configuration constants for StudyPlannerAgent"""
    
    # Learning styles
    LEARNING_STYLES = {
        "reading": {
            "name": "Reading",
            "description": "Learn through textbooks, articles, and written materials",
            "methods": ["Textbooks", "Articles", "Documentation", "Notes", "Books"],
            "time_ratio": 0.4
        },
        "practice": {
            "name": "Practice",
            "description": "Learn through hands-on exercises and practical application",
            "methods": ["Exercises", "Projects", "Coding", "Problem Solving", "Labs"],
            "time_ratio": 0.5
        },
        "videos": {
            "name": "Videos",
            "description": "Learn through video tutorials and lectures",
            "methods": ["Video Tutorials", "Online Courses", "Lectures", "Webinars", "Tutorials"],
            "time_ratio": 0.3
        },
        "mixed": {
            "name": "Mixed",
            "description": "Combination of reading, practice, and videos",
            "methods": ["Reading + Practice + Videos", "Balanced Approach", "Multi-modal Learning"],
            "time_ratio": 0.4
        }
    }
    
    # Study difficulty levels
    DIFFICULTY_LEVELS = {
        "beginner": {
            "name": "Beginner",
            "description": "No prior knowledge required",
            "pace": "slow",
            "depth": "basic",
            "time_multiplier": 1.2
        },
        "intermediate": {
            "name": "Intermediate",
            "description": "Some prior knowledge helpful",
            "pace": "moderate",
            "depth": "intermediate",
            "time_multiplier": 1.0
        },
        "advanced": {
            "name": "Advanced",
            "description": "Strong foundation required",
            "pace": "fast",
            "depth": "advanced",
            "time_multiplier": 0.8
        }
    }
    
    # Common study subjects/topics
    STUDY_SUBJECTS = {
        "programming": {
            "name": "Programming",
            "topics": ["Python", "JavaScript", "Java", "C++", "Web Development", "Data Structures", "Algorithms"],
            "estimated_hours": {"beginner": 200, "intermediate": 150, "advanced": 100}
        },
        "languages": {
            "name": "Languages",
            "topics": ["English", "Spanish", "French", "German", "Chinese", "Japanese", "IELTS", "TOEFL"],
            "estimated_hours": {"beginner": 300, "intermediate": 200, "advanced": 150}
        },
        "academic": {
            "name": "Academic",
            "topics": ["Mathematics", "Physics", "Chemistry", "Biology", "History", "Literature", "Economics"],
            "estimated_hours": {"beginner": 250, "intermediate": 180, "advanced": 120}
        },
        "certifications": {
            "name": "Certifications",
            "topics": ["AWS", "Google Cloud", "Microsoft Azure", "PMP", "CISSP", "CompTIA", "Cisco"],
            "estimated_hours": {"beginner": 120, "intermediate": 80, "advanced": 60}
        },
        "skills": {
            "name": "Skills",
            "topics": ["Public Speaking", "Writing", "Design", "Marketing", "Sales", "Leadership", "Time Management"],
            "estimated_hours": {"beginner": 100, "intermediate": 80, "advanced": 60}
        }
    }
    
    # Default study settings
    DEFAULT_LEARNING_STYLE = "mixed"
    DEFAULT_DIFFICULTY = "intermediate"
    DEFAULT_HOURS_PER_DAY = 2
    DEFAULT_DAYS_AVAILABLE = 30
    
    # GPT settings
    MAX_TOKENS = 3000
    TEMPERATURE = 0.7
    
    # File storage settings
    OUTPUT_DIR = "output"
    PLANS_DIR = "study_plans"
    PLAN_EXTENSIONS = [".md", ".json", ".pdf"]
    
    # Web interface settings
    WEB_TITLE = "StudyPlannerAgent"
    WEB_DESCRIPTION = "AI-powered personalized study planning tool"
    WEB_VERSION = "1.0.0"
    
    # Study plan generation prompts
    STUDY_PLAN_PROMPTS = {
        "base": """You are an expert educational consultant and study planner. Create a comprehensive, personalized study plan based on the following requirements:

Study Goal: {goal}
Time Available: {days_available} days
Hours per Day: {hours_per_day} hours
Learning Style: {learning_style}
Difficulty Level: {difficulty}
Subject Area: {subject}

Please create a detailed study plan that includes:

1. **Overview Section**:
   - Goal summary
   - Total study time available
   - Learning approach strategy
   - Expected outcomes

2. **Weekly Breakdown**:
   - Week-by-week progression from basics to advanced
   - Key milestones and checkpoints
   - Review and assessment points

3. **Daily Schedule Template**:
   - Daily time allocation
   - Study session structure
   - Break recommendations
   - Review and practice time

4. **Resource Recommendations**:
   - Books, courses, or materials
   - Online resources and tools
   - Practice exercises and projects
   - Assessment methods

5. **Progress Tracking**:
   - Weekly goals and objectives
   - Self-assessment criteria
   - Milestone celebrations
   - Adjustment strategies

6. **Tips and Strategies**:
   - Study techniques specific to the learning style
   - Time management advice
   - Motivation and consistency tips
   - Common pitfalls to avoid

Format the plan with:
- Clear headings and subheadings
- Bullet points for easy reading
- Time estimates for each activity
- Actionable daily tasks
- Progress checkpoints

Make the plan practical, achievable, and motivating. Focus on building a strong foundation and progressing systematically toward the goal.

Generate the study plan now:""",
        
        "quick": """Create a concise study plan for:

Goal: {goal}
Time: {days_available} days, {hours_per_day} hours/day
Style: {learning_style}
Level: {difficulty}

Include:
1. Weekly breakdown (3-4 weeks max)
2. Daily study routine
3. Key resources
4. Progress milestones

Keep it practical and actionable.""",
        
        "detailed": """Create an extremely detailed study plan for:

Goal: {goal}
Time: {days_available} days, {hours_per_day} hours/day
Style: {learning_style}
Level: {difficulty}
Subject: {subject}

Include:
1. **Comprehensive Overview** with learning objectives
2. **Detailed Weekly Plans** with specific topics and activities
3. **Daily Schedules** with exact time allocations
4. **Resource Library** with specific books, courses, and tools
5. **Assessment Strategy** with quizzes, projects, and evaluations
6. **Progress Tracking System** with metrics and milestones
7. **Study Techniques** tailored to the learning style
8. **Troubleshooting Guide** for common challenges
9. **Motivation Strategies** and reward systems
10. **Flexibility Guidelines** for schedule adjustments

Make it comprehensive, professional, and highly detailed."""
    }
    
    # Study plan templates
    PLAN_TEMPLATES = {
        "basic": {
            "name": "Basic Plan",
            "description": "Simple weekly breakdown with daily tasks",
            "sections": ["Overview", "Weekly Plan", "Daily Schedule", "Resources"]
        },
        "detailed": {
            "name": "Detailed Plan",
            "description": "Comprehensive plan with progress tracking",
            "sections": ["Overview", "Weekly Plans", "Daily Schedules", "Resources", "Assessment", "Progress Tracking", "Tips"]
        },
        "intensive": {
            "name": "Intensive Plan",
            "description": "Fast-paced plan for quick learning",
            "sections": ["Overview", "Accelerated Schedule", "Daily Intensive Sessions", "Resources", "Assessment", "Motivation"]
        }
    }
    
    # Export formats
    EXPORT_FORMATS = {
        "markdown": {
            "name": "Markdown",
            "extension": ".md",
            "description": "Human-readable format with formatting"
        },
        "json": {
            "name": "JSON",
            "extension": ".json",
            "description": "Structured data format for integration"
        },
        "pdf": {
            "name": "PDF",
            "extension": ".pdf",
            "description": "Professional document format"
        }
    }
