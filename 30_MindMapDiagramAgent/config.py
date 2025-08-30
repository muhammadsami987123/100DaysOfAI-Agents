import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for MindMapDiagramAgent"""
    
    def __init__(self):
        # OpenAI Configuration
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "4000"))
        self.OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
        
        # Server Configuration
        self.HOST = os.getenv("HOST", "127.0.0.1")
        self.PORT = int(os.getenv("PORT", "8030"))
        self.DEBUG = os.getenv("DEBUG", "true").lower() == "true"
        
        # Mind Map Configuration
        self.MAX_INPUT_LENGTH = int(os.getenv("MAX_INPUT_LENGTH", "10000"))
        self.MAX_DEPTH_LEVELS = int(os.getenv("MAX_DEPTH_LEVELS", "5"))
        self.DEFAULT_DEPTH_LEVELS = int(os.getenv("DEFAULT_DEPTH_LEVELS", "3"))
        
        # Export Configuration
        self.EXPORT_QUALITY = int(os.getenv("EXPORT_QUALITY", "90"))
        self.EXPORT_WIDTH = int(os.getenv("EXPORT_WIDTH", "1920"))
        self.EXPORT_HEIGHT = int(os.getenv("EXPORT_HEIGHT", "1080"))
        
        # File Storage
        self.UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
        self.EXPORT_DIR = os.getenv("EXPORT_DIR", "exports")
        self.TEMP_DIR = os.getenv("TEMP_DIR", "temp")
        
        # Session Configuration
        self.SESSION_TIMEOUT = int(os.getenv("SESSION_TIMEOUT", "3600"))  # 1 hour
        self.MAX_SESSIONS_PER_USER = int(os.getenv("MAX_SESSIONS_PER_USER", "10"))
        
        # AI Processing Configuration
        self.CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "2000"))
        self.OVERLAP_SIZE = int(os.getenv("OVERLAP_SIZE", "200"))
        self.MAX_NODES = int(os.getenv("MAX_NODES", "100"))
        
        # Validation
        self._validate_config()
    
    def _validate_config(self):
        """Validate configuration settings"""
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required. Please set it in your .env file.")
        
        if self.PORT < 1 or self.PORT > 65535:
            raise ValueError("PORT must be between 1 and 65535")
        
        if self.MAX_INPUT_LENGTH < 100:
            raise ValueError("MAX_INPUT_LENGTH must be at least 100 characters")
        
        if self.MAX_DEPTH_LEVELS < 1 or self.MAX_DEPTH_LEVELS > 10:
            raise ValueError("MAX_DEPTH_LEVELS must be between 1 and 10")
    
    def get_openai_config(self) -> dict:
        """Get OpenAI configuration as dictionary"""
        return {
            "api_key": self.OPENAI_API_KEY,
            "model": self.OPENAI_MODEL,
            "max_tokens": self.OPENAI_MAX_TOKENS,
            "temperature": self.OPENAI_TEMPERATURE
        }
    
    def get_export_config(self) -> dict:
        """Get export configuration as dictionary"""
        return {
            "quality": self.EXPORT_QUALITY,
            "width": self.EXPORT_WIDTH,
            "height": self.EXPORT_HEIGHT
        }
    
    def get_processing_config(self) -> dict:
        """Get AI processing configuration as dictionary"""
        return {
            "chunk_size": self.CHUNK_SIZE,
            "overlap_size": self.OVERLAP_SIZE,
            "max_nodes": self.MAX_NODES,
            "max_depth": self.MAX_DEPTH_LEVELS
        }

# Default themes for diagrams
DEFAULT_THEMES = {
    "light": {
        "name": "Light",
        "background": "#ffffff",
        "text": "#333333",
        "primary": "#3b82f6",
        "secondary": "#6b7280",
        "accent": "#f59e0b"
    },
    "dark": {
        "name": "Dark",
        "background": "#1f2937",
        "text": "#f9fafb",
        "primary": "#60a5fa",
        "secondary": "#9ca3af",
        "accent": "#fbbf24"
    },
    "blue": {
        "name": "Blue",
        "background": "#eff6ff",
        "text": "#1e40af",
        "primary": "#3b82f6",
        "secondary": "#60a5fa",
        "accent": "#0ea5e9"
    },
    "green": {
        "name": "Green",
        "background": "#f0fdf4",
        "text": "#166534",
        "primary": "#22c55e",
        "secondary": "#4ade80",
        "accent": "#10b981"
    },
    "purple": {
        "name": "Purple",
        "background": "#faf5ff",
        "text": "#7c3aed",
        "primary": "#8b5cf6",
        "secondary": "#a78bfa",
        "accent": "#a855f7"
    }
}

# Diagram type configurations
DIAGRAM_TYPES = {
    "mindmap": {
        "name": "Mind Map",
        "description": "Hierarchical diagram showing relationships between concepts",
        "icon": "🧠",
        "mermaid_type": "mindmap"
    },
    "flowchart": {
        "name": "Flowchart",
        "description": "Process flow diagram showing steps and decisions",
        "icon": "📊",
        "mermaid_type": "flowchart"
    },
    "orgchart": {
        "name": "Organization Chart",
        "description": "Hierarchical structure showing organizational relationships",
        "icon": "🏢",
        "mermaid_type": "graph"
    },
    "network": {
        "name": "Network Diagram",
        "description": "Network of interconnected nodes and relationships",
        "icon": "🌐",
        "mermaid_type": "graph"
    }
}

# Export formats
EXPORT_FORMATS = {
    "png": {
        "name": "PNG Image",
        "extension": ".png",
        "mime_type": "image/png",
        "description": "High-quality raster image"
    },
    "svg": {
        "name": "SVG Vector",
        "extension": ".svg",
        "mime_type": "image/svg+xml",
        "description": "Scalable vector graphics"
    },
    "pdf": {
        "name": "PDF Document",
        "extension": ".pdf",
        "mime_type": "application/pdf",
        "description": "Portable document format"
    },
    "json": {
        "name": "JSON Data",
        "extension": ".json",
        "mime_type": "application/json",
        "description": "Structured data format"
    }
}
