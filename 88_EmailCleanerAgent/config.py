from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GMAIL_CLIENT_SECRET_FILE = "client_secret.json"
    GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
    GMAIL_CREDENTIALS_FILE = "gmail_credentials.json"
