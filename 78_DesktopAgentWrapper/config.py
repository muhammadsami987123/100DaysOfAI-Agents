"""
Configuration and settings for DesktopAgentWrapper
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for DesktopAgentWrapper"""
    
    # Application Configuration
    APP_NAME = "DesktopAgentWrapper"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "Universal desktop GUI for AI agents"
    
    # API Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # UI Configuration
    DEFAULT_THEME = os.getenv("APP_THEME", "dark")
    WINDOW_SIZE = (1200, 800)
    MIN_WINDOW_SIZE = (800, 600)
    
    # Agent Configuration
    DEFAULT_AGENT = os.getenv("DEFAULT_AGENT", "ArticleRewriter")
    AUTO_SAVE = os.getenv("AUTO_SAVE", "true").lower() == "true"
    SESSION_TIMEOUT = int(os.getenv("SESSION_TIMEOUT", "3600"))
    
    # File Paths
    ASSETS_DIR = "assets"
    AGENTS_DIR = "agents"
    SESSIONS_DIR = "sessions"
    LOGS_DIR = "logs"
    EXPORTS_DIR = "exports"
    
    # UI Themes
    THEMES = {
        "dark": {
            "primary_color": "#3b82f6",
            "secondary_color": "#1e40af", 
            "background_color": "#0f172a",
            "surface_color": "#1e293b",
            "text_color": "#f8fafc",
            "accent_color": "#f59e0b",
            "success_color": "#10b981",
            "error_color": "#ef4444",
            "warning_color": "#f59e0b"
        },
        "light": {
            "primary_color": "#3b82f6",
            "secondary_color": "#1e40af",
            "background_color": "#ffffff",
            "surface_color": "#f8fafc",
            "text_color": "#1e293b",
            "accent_color": "#f59e0b",
            "success_color": "#10b981",
            "error_color": "#ef4444",
            "warning_color": "#f59e0b"
        }
    }
    
    # Supported Agent Types
    AGENT_TYPES = {
        "text_processing": {
            "name": "Text Processing",
            "description": "Agents that process and transform text content",
            "icon": "📝",
            "agents": ["ArticleRewriter", "PromptImprover", "TextAnalyzer", "StoryWriter"]
        },
        "ai_assistant": {
            "name": "AI Assistant", 
            "description": "General-purpose AI assistants and helpers",
            "icon": "🤖",
            "agents": ["DevHelper", "TerminalHelper", "CodeReviewer", "GitHelper"]
        },
        "data_processing": {
            "name": "Data Processing",
            "description": "Agents that analyze and process data",
            "icon": "📊",
            "agents": ["PDFQAAgent", "ResumeParser", "InvestmentAdvisor", "StudyPlanner"]
        },
        "creative": {
            "name": "Creative",
            "description": "Agents for creative tasks and content generation",
            "icon": "🎨",
            "agents": ["ImageCaptionBot", "MoodMusicAgent", "IdeaGenerator", "ComicWriter"]
        }
    }
    
    # Export Formats
    EXPORT_FORMATS = {
        "txt": {
            "name": "Text File",
            "extension": ".txt",
            "description": "Plain text format"
        },
        "json": {
            "name": "JSON File", 
            "extension": ".json",
            "description": "Structured JSON format"
        },
        "html": {
            "name": "HTML File",
            "extension": ".html", 
            "description": "HTML format with styling"
        },
        "pdf": {
            "name": "PDF File",
            "extension": ".pdf",
            "description": "PDF document format"
        }
    }
    
    # UI Component Defaults
    UI_DEFAULTS = {
        "show_progress_bar": True,
        "enable_export": True,
        "auto_save_interval": 300,
        "max_history_items": 50,
        "show_sidebar": True,
        "enable_notifications": True
    }
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration"""
        # Check if required directories exist
        required_dirs = [cls.ASSETS_DIR, cls.AGENTS_DIR, cls.SESSIONS_DIR, cls.LOGS_DIR, cls.EXPORTS_DIR]
        for dir_path in required_dirs:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
        
        return True
    
    @classmethod
    def get_theme_colors(cls, theme: str = None) -> Dict[str, str]:
        """Get theme colors"""
        theme = theme or cls.DEFAULT_THEME
        return cls.THEMES.get(theme, cls.THEMES["dark"])
    
    @classmethod
    def get_agent_type(cls, agent_name: str) -> Optional[str]:
        """Get agent type for a given agent name"""
        for agent_type, config in cls.AGENT_TYPES.items():
            if agent_name in config["agents"]:
                return agent_type
        return None
