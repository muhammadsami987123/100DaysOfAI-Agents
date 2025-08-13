import os
from typing import Dict, List, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Server Configuration
PORT = int(os.getenv("PORT", 8013))
HOST = os.getenv("HOST", "0.0.0.0")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 4000))
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.3))

# File Upload Configuration
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 10485760))  # 10MB
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

# Supported Programming Languages
SUPPORTED_LANGUAGES = {
    "python": {
        "extensions": [".py", ".pyw"],
        "keywords": ["def", "class", "import", "from", "if", "for", "while", "try", "except"],
        "best_practices": [
            "PEP 8 style guide",
            "Type hints",
            "Docstrings",
            "Error handling",
            "List comprehensions",
            "Context managers"
        ]
    },
    "javascript": {
        "extensions": [".js", ".jsx", ".ts", ".tsx"],
        "keywords": ["function", "const", "let", "var", "if", "for", "while", "try", "catch"],
        "best_practices": [
            "ES6+ features",
            "Arrow functions",
            "Template literals",
            "Destructuring",
            "Async/await",
            "Error handling"
        ]
    },
    "java": {
        "extensions": [".java"],
        "keywords": ["public", "class", "private", "protected", "static", "void", "int", "String"],
        "best_practices": [
            "Java naming conventions",
            "Access modifiers",
            "Exception handling",
            "Collections framework",
            "Stream API",
            "Lombok annotations"
        ]
    },
    "cpp": {
        "extensions": [".cpp", ".cc", ".cxx", ".h", ".hpp"],
        "keywords": ["#include", "int", "void", "class", "public", "private", "protected"],
        "best_practices": [
            "RAII principles",
            "Smart pointers",
            "STL containers",
            "Exception handling",
            "Const correctness",
            "Move semantics"
        ]
    },
    "csharp": {
        "extensions": [".cs"],
        "keywords": ["using", "namespace", "class", "public", "private", "void", "int", "string"],
        "best_practices": [
            "C# naming conventions",
            "LINQ",
            "Async/await",
            "Exception handling",
            "Properties",
            "Extension methods"
        ]
    },
    "php": {
        "extensions": [".php"],
        "keywords": ["<?php", "function", "class", "public", "private", "protected", "echo", "return"],
        "best_practices": [
            "PSR standards",
            "Composer autoloading",
            "Error handling",
            "Type declarations",
            "Namespaces",
            "Modern PHP features"
        ]
    },
    "go": {
        "extensions": [".go"],
        "keywords": ["package", "import", "func", "var", "const", "type", "struct", "interface"],
        "best_practices": [
            "Go naming conventions",
            "Error handling",
            "Interfaces",
            "Goroutines",
            "Channels",
            "Testing"
        ]
    },
    "rust": {
        "extensions": [".rs"],
        "keywords": ["fn", "let", "mut", "struct", "enum", "impl", "trait", "use"],
        "best_practices": [
            "Ownership system",
            "Error handling with Result",
            "Pattern matching",
            "Traits",
            "Cargo ecosystem",
            "Memory safety"
        ]
    },
    "swift": {
        "extensions": [".swift"],
        "keywords": ["import", "class", "struct", "func", "var", "let", "if", "for", "guard"],
        "best_practices": [
            "Swift naming conventions",
            "Optionals",
            "Protocols",
            "Extensions",
            "Error handling",
            "SwiftUI"
        ]
    },
    "kotlin": {
        "extensions": [".kt", ".kts"],
        "keywords": ["fun", "val", "var", "class", "object", "interface", "when", "if"],
        "best_practices": [
            "Kotlin idioms",
            "Null safety",
            "Extension functions",
            "Data classes",
            "Coroutines",
            "Kotlin DSL"
        ]
    }
}

# UI Languages
UI_LANGUAGES = {
    "english": {
        "name": "English",
        "code": "en"
    },
    "hindi": {
        "name": "हिंदी",
        "code": "hi"
    },
    "urdu": {
        "name": "اردو",
        "code": "ur"
    }
}

# Code Review Categories
REVIEW_CATEGORIES = {
    "syntax": {
        "name": "Syntax Issues",
        "description": "Code syntax errors and formatting problems",
        "weight": 0.2
    },
    "best_practices": {
        "name": "Best Practices",
        "description": "Coding standards and industry best practices",
        "weight": 0.25
    },
    "performance": {
        "name": "Performance",
        "description": "Code efficiency and optimization opportunities",
        "weight": 0.2
    },
    "security": {
        "name": "Security",
        "description": "Security vulnerabilities and concerns",
        "weight": 0.2
    },
    "readability": {
        "name": "Readability",
        "description": "Code clarity and maintainability",
        "weight": 0.15
    }
}

# GitHub API Configuration
GITHUB_API_URL = "https://api.github.com"
GITHUB_RAW_URL = "https://raw.githubusercontent.com"

# Error Messages
ERROR_MESSAGES = {
    "missing_api_key": "OpenAI API key is required. Please set OPENAI_API_KEY in your .env file.",
    "invalid_file": "Invalid file format. Please upload a supported code file.",
    "file_too_large": f"File too large. Maximum size is {MAX_FILE_SIZE // 1024 // 1024}MB.",
    "github_fetch_failed": "Failed to fetch code from GitHub. Please check the URL and ensure it's a public repository.",
    "code_analysis_failed": "Code analysis failed. Please try again with different code.",
    "unsupported_language": "Unsupported programming language. Please use a supported language.",
    "empty_code": "No code provided. Please enter or upload some code to review."
}

# Success Messages
SUCCESS_MESSAGES = {
    "analysis_complete": "Code analysis completed successfully!",
    "file_uploaded": "File uploaded successfully!",
    "github_fetched": "Code fetched from GitHub successfully!"
}

def get_language_from_extension(filename: str) -> str:
    """Detect programming language from file extension."""
    if not filename:
        return "unknown"
    
    extension = os.path.splitext(filename)[1].lower()
    
    for lang, config in SUPPORTED_LANGUAGES.items():
        if extension in config["extensions"]:
            return lang
    
    return "unknown"

def get_language_from_content(content: str) -> str:
    """Detect programming language from code content."""
    if not content:
        return "unknown"
    
    content_lower = content.lower()
    
    # Simple heuristics for language detection
    # Python: include common tokens even for tiny snippets (e.g., print("hi"))
    if any(keyword in content_lower for keyword in ["def ", "import ", "from ", "class ", "print(", "async def "]):
        return "python"
    # JavaScript/TypeScript: detect common patterns including console.log
    elif any(keyword in content_lower for keyword in ["function", "const ", "let ", "var ", "=>", "console.log("]):
        return "javascript"
    elif any(keyword in content_lower for keyword in ["public class", "private ", "public ", "void "]):
        return "java"
    elif any(keyword in content_lower for keyword in ["#include", "int main", "std::"]):
        return "cpp"
    elif any(keyword in content_lower for keyword in ["using ", "namespace ", "public class"]):
        return "csharp"
    elif any(keyword in content_lower for keyword in ["<?php", "function ", "echo "]):
        return "php"
    elif any(keyword in content_lower for keyword in ["package ", "func ", "import "]):
        return "go"
    elif any(keyword in content_lower for keyword in ["fn ", "let ", "mut ", "struct "]):
        return "rust"
    elif any(keyword in content_lower for keyword in ["import ", "class ", "func ", "var "]):
        return "swift"
    elif any(keyword in content_lower for keyword in ["fun ", "val ", "var ", "class "]):
        return "kotlin"
    
    return "unknown"

def validate_config() -> List[str]:
    """Validate configuration and return list of errors."""
    errors = []
    
    if not OPENAI_API_KEY:
        errors.append(ERROR_MESSAGES["missing_api_key"])
    
    return errors
