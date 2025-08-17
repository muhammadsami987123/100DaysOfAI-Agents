import os
from typing import Dict, List, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 6000))  # Increased from 4000 to 6000
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.2))  # Reduced from 0.3 to 0.2 for more focused output

# GitHub API Configuration
GITHUB_API_URL = "https://api.github.com"
GITHUB_RAW_URL = "https://raw.githubusercontent.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Optional, for higher rate limits

# Repository Analysis Configuration
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 1024 * 1024))  # 1MB per file
MAX_FILES_TO_ANALYZE = int(os.getenv("MAX_FILES_TO_ANALYZE", 50))
SUPPORTED_FILE_EXTENSIONS = [
    # Configuration files
    ".py", ".js", ".ts", ".java", ".cpp", ".c", ".cs", ".php", ".go", ".rs", ".swift", ".kt",
    ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".env", ".gitignore",
    # Documentation
    ".md", ".txt", ".rst", ".adoc",
    # Build files
    ".py", ".js", ".ts", ".java", ".cpp", ".c", ".cs", ".php", ".go", ".rs", ".swift", ".kt",
    "requirements.txt", "package.json", "pom.xml", "build.gradle", "Cargo.toml", "Gemfile",
    "composer.json", "nuget.config", "Dockerfile", "docker-compose.yml", ".dockerignore",
    # Source files
    ".py", ".js", ".ts", ".jsx", ".tsx", ".vue", ".svelte", ".java", ".cpp", ".c", ".h", ".hpp",
    ".cs", ".php", ".go", ".rs", ".swift", ".kt", ".scala", ".rb", ".pl", ".sh", ".bat",
    ".sql", ".html", ".css", ".scss", ".sass", ".less"
]

# Key files to prioritize for analysis
PRIORITY_FILES = [
    "README.md", "README.txt", "README.rst", "README.adoc",
    "main.py", "app.py", "index.py", "index.js", "index.ts", "index.html",
    "package.json", "requirements.txt", "pom.xml", "build.gradle",
    "Cargo.toml", "Gemfile", "composer.json", "setup.py", "pyproject.toml",
    "Dockerfile", "docker-compose.yml", ".gitignore", "LICENSE", "CHANGELOG.md"
]

# Language Support
SUPPORTED_LANGUAGES = {
    "en": {
        "name": "English",
        "code": "en",
        "analyzing": "Analyzing repository...",
        "fetching": "Fetching repository data...",
        "processing": "Processing files...",
        "generating": "Generating summary...",
        "complete": "Analysis complete!",
        "error": "Error occurred",
        "private_repo": "Repository is private. Cannot analyze.",
        "invalid_url": "Invalid GitHub URL provided.",
        "no_readme": "No README file found in repository.",
        "fetch_failed": "Failed to fetch repository data.",
        "saving": "Saving summary to file...",
        "saved": "Summary saved successfully!"
    },
    "ur": {
        "name": "اردو",
        "code": "ur",
        "analyzing": "ریپوزٹری کا تجزیہ کر رہا ہے...",
        "fetching": "ریپوزٹری ڈیٹا حاصل کر رہا ہے...",
        "processing": "فائلیں پروسیس کر رہا ہے...",
        "generating": "خلاصہ تیار کر رہا ہے...",
        "complete": "تجزیہ مکمل ہو گیا!",
        "error": "خرابی آئی",
        "private_repo": "ریپوزٹری نجی ہے۔ تجزیہ نہیں کر سکتا۔",
        "invalid_url": "غلط GitHub URL دی گئی ہے۔",
        "no_readme": "ریپوزٹری میں کوئی README فائل نہیں ملی۔",
        "fetch_failed": "ریپوزٹری ڈیٹا حاصل کرنے میں ناکام۔",
        "saving": "خلاصہ فائل میں محفوظ کر رہا ہے...",
        "saved": "خلاصہ کامیابی سے محفوظ ہو گیا!"
    },
    "hi": {
        "name": "हिंदी",
        "code": "hi",
        "analyzing": "रिपॉजिटरी का विश्लेषण कर रहा है...",
        "fetching": "रिपॉजिटरी डेटा प्राप्त कर रहा है...",
        "processing": "फाइलें प्रोसेस कर रहा है...",
        "generating": "सारांश तैयार कर रहा है...",
        "complete": "विश्लेषण पूरा हो गया!",
        "error": "त्रुटि आई",
        "private_repo": "रिपॉजिटरी निजी है। विश्लेषण नहीं कर सकता।",
        "invalid_url": "गलत GitHub URL दी गई है।",
        "no_readme": "रिपॉजिटरी में कोई README फाइल नहीं मिली।",
        "fetch_failed": "रिपॉजिटरी डेटा प्राप्त करने में असफल।",
        "saving": "सारांश फाइल में सहेज रहा है...",
        "saved": "सारांश सफलतापूर्वक सहेजा गया!"
    }
}

# Error Messages
ERROR_MESSAGES = {
    "missing_api_key": "OpenAI API key is required. Please set OPENAI_API_KEY in your .env file.",
    "invalid_github_url": "Invalid GitHub URL. Please provide a valid GitHub repository URL.",
    "private_repository": "Cannot analyze private repositories. Please ensure the repository is public.",
    "repository_not_found": "Repository not found. Please check the URL and ensure the repository exists.",
    "rate_limit_exceeded": "GitHub API rate limit exceeded. Please try again later.",
    "fetch_failed": "Failed to fetch repository data. Please check your internet connection and try again.",
    "no_files_found": "No analyzable files found in the repository.",
    "file_too_large": "Some files are too large to analyze. Analysis may be incomplete.",
    "analysis_failed": "Repository analysis failed. Please try again with a different repository."
}

# Success Messages
SUCCESS_MESSAGES = {
    "analysis_started": "Repository analysis started successfully!",
    "files_fetched": "Repository files fetched successfully!",
    "summary_generated": "Repository summary generated successfully!",
    "file_saved": "Summary saved to file successfully!"
}

def validate_config() -> List[str]:
    """Validate configuration and return list of errors."""
    errors = []
    
    if not OPENAI_API_KEY:
        errors.append(ERROR_MESSAGES["missing_api_key"])
    
    return errors

def get_language_config(lang_code: str) -> Dict[str, str]:
    """Get language configuration for the specified language code."""
    return SUPPORTED_LANGUAGES.get(lang_code.lower(), SUPPORTED_LANGUAGES["en"])

def is_supported_file(filename: str) -> bool:
    """Check if a file is supported for analysis."""
    if not filename:
        return False
    
    # Check exact matches first (for files without extensions)
    if filename in PRIORITY_FILES:
        return True
    
    # Check file extensions
    extension = os.path.splitext(filename)[1].lower()
    return extension in SUPPORTED_FILE_EXTENSIONS or filename in SUPPORTED_FILE_EXTENSIONS
