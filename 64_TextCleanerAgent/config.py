import os

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "supersecretkey") # Fallback for development
    UPLOAD_FOLDER = 'uploads' # Folder to temporarily store uploaded files
    ALLOWED_EXTENSIONS = {'txt', 'docx'}
