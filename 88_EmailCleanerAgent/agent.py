import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from utils.llm_service import LLMService
from config import Config

class EmailCleanerAgent:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
        self.gmail_service = self._get_gmail_service()

    def _get_gmail_service(self):
        creds = None
        if os.path.exists(Config.GMAIL_CREDENTIALS_FILE):
            creds = Credentials.from_authorized_user_file(Config.GMAIL_CREDENTIALS_FILE, Config.GMAIL_SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(Config.GMAIL_CLIENT_SECRET_FILE, Config.GMAIL_SCOPES)
                creds = flow.run_local_server(port=0)
            with open(Config.GMAIL_CREDENTIALS_FILE, 'w') as token:
                token.write(creds.to_json())
        return build('gmail', 'v1', credentials=creds)

    def fetch_emails(self, max_results=50):
        results = self.gmail_service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=max_results).execute()
        messages = results.get('messages', [])
        emails = []
        for message in messages:
            msg = self.gmail_service.users().messages().get(userId='me', id=message['id']).execute()
            email_data = {
                'id': msg['id'],
                'snippet': msg['snippet'],
                'subject': next(header['value'] for header in msg['payload']['headers'] if header['name'] == 'Subject')
            }
            emails.append(email_data)
        return emails

    def analyze_and_classify_emails(self, emails):
        # This is a simplified analysis. In a real app, you'd use the LLM.
        classified_emails = []
        for email in emails:
            if "newsletter" in email['snippet'].lower() or "promotion" in email['snippet'].lower():
                classification = "Promotional"
            elif "unsubscribe" in email['snippet'].lower():
                classification = "Spam"
            else:
                classification = "Important"
            
            email['classification'] = classification
            classified_emails.append(email)
        return classified_emails

    def delete_email(self, email_id):
        self.gmail_service.users().messages().trash(userId='me', id=email_id).execute()

    def archive_email(self, email_id):
        self.gmail_service.users().messages().modify(userId='me', id=email_id, body={'removeLabelIds': ['INBOX']}).execute()
