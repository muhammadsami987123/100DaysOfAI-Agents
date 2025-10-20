import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Configuration
    LLM_MODEL = os.getenv("LLM_MODEL", "gemini").lower()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    
    # Generation Settings
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))
    
    # Supported config formats
    SUPPORTED_FORMATS = ["json", "yaml", "toml", "js", "ts"]
    
    # Common config types
    CONFIG_TYPES = {
        "app_settings": {
            "name": "Application Settings",
            "examples": ["Node.js Express", "Django", "Flask", "React", "Vue"]
        },
        "devops": {
            "name": "DevOps & Deployment",
            "examples": ["GitHub Actions", "Docker Compose", "Kubernetes", "CI/CD"]
        },
        "linting": {
            "name": "Linting & Formatting",
            "examples": ["ESLint", "Prettier", "Stylelint", "Black", "Pylint"]
        },
        "build_tools": {
            "name": "Build Tools",
            "examples": ["Vite", "Webpack", "Babel", "Rollup", "Parcel"]
        },
        "package_managers": {
            "name": "Package Managers",
            "examples": ["package.json", "pyproject.toml", "composer.json", "requirements.txt"]
        },
        "database": {
            "name": "Database Configuration",
            "examples": ["PostgreSQL", "MongoDB", "Redis", "MySQL", "SQLite"]
        },
        "custom": {
            "name": "Custom Configuration",
            "examples": ["Custom tool configs", "Environment files", "Custom JSON/YAML"]
        }
    }
    
    # Default values for common configurations
    DEFAULT_VALUES = {
        "port": "3000",
        "host": "localhost",
        "database_url": "postgresql://localhost:5432/mydb",
        "mongodb_url": "mongodb://localhost:27017/mydb",
        "redis_url": "redis://localhost:6379",
        "api_key": "your-api-key-here",
        "secret_key": "your-secret-key-here",
        "environment": "development"
    }
    
    @classmethod
    def validate(cls):
        """Validate configuration settings"""
        if cls.LLM_MODEL == "openai":
            if not cls.OPENAI_API_KEY:
                print("Warning: OPENAI_API_KEY not found. AI features will be limited.")
                return False
        elif cls.LLM_MODEL == "gemini":
            if not cls.GEMINI_API_KEY:
                print("Warning: GEMINI_API_KEY not found. AI features will be limited.")
                return False
        else:
            print("Warning: Invalid LLM_MODEL specified. Must be 'openai' or 'gemini'.")
            return False
        return True
