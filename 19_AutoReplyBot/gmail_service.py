from __future__ import annotations

import base64
import email
from email.message import EmailMessage
from typing import Dict, List, Optional
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import (
    GMAIL_CREDENTIALS_FILE,
    GMAIL_TOKEN_FILE,
    GMAIL_USER,
    GMAIL_QUERY,
    GMAIL_MAX_RESULTS,
)


# If modifying these scopes, delete token.json.
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]


def _get_service():
    creds: Optional[Credentials] = None
    if os.path.exists(GMAIL_TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(GMAIL_TOKEN_FILE, SCOPES)
    # If creds exist but scopes are insufficient, force a new auth flow
    if creds and getattr(creds, "scopes", None):
        existing_scopes = set(creds.scopes or [])
        required_scopes = set(SCOPES)
        if not required_scopes.issubset(existing_scopes):
            creds = None
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(GMAIL_CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(GMAIL_TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    service = build("gmail", "v1", credentials=creds)
    return service


def list_messages(query: Optional[str] = None, max_results: Optional[int] = None) -> List[Dict]:
    service = _get_service()
    try:
        results = service.users().messages().list(
            userId=GMAIL_USER,
            q=query or GMAIL_QUERY,
            maxResults=max_results or GMAIL_MAX_RESULTS,
        ).execute()
        return results.get("messages", [])
    except HttpError:
        return []


def get_message_detail(message_id: str) -> Dict:
    service = _get_service()
    msg = service.users().messages().get(userId=GMAIL_USER, id=message_id, format="full").execute()
    return msg


def _parse_email_payload(msg: Dict) -> Dict[str, str]:
    headers = {h["name"].lower(): h["value"] for h in msg.get("payload", {}).get("headers", [])}
    subject = headers.get("subject", "(no subject)")
    sender = headers.get("from", "unknown")
    to = headers.get("to", "me@example.com")

    body_text = ""
    payload = msg.get("payload", {})
    if payload.get("body", {}).get("data"):
        body_text = base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="ignore")
    else:
        for part in payload.get("parts", []) or []:
            if part.get("mimeType") == "text/plain" and part.get("body", {}).get("data"):
                body_text = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="ignore")
                break

    return {
        "subject": subject,
        "from": sender,
        "to": to,
        "body": body_text,
    }


def fetch_inbox(query: Optional[str] = None, max_results: Optional[int] = None) -> List[Dict[str, str]]:
    messages = []
    for item in list_messages(query=query, max_results=max_results):
        msg = get_message_detail(item["id"])
        parsed = _parse_email_payload(msg)
        parsed["id"] = msg.get("id")
        parsed["thread_id"] = msg.get("threadId")
        parsed["timestamp"] = msg.get("internalDate")
        messages.append(parsed)
    return messages


def send_email(to_address: str, subject: str, body: str, thread_id: Optional[str] = None) -> Optional[str]:
    service = _get_service()
    message = EmailMessage()
    message["To"] = to_address
    message["Subject"] = subject
    message.set_content(body)
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {"raw": encoded_message}
    if thread_id:
        create_message["threadId"] = thread_id
    sent = service.users().messages().send(userId=GMAIL_USER, body=create_message).execute()
    return sent.get("id")


