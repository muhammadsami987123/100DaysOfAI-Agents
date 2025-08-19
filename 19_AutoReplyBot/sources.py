import json
import os
from typing import Dict, Iterable, List, Optional

from config import (
    INBOX_JSON_PATH,
    CHAT_JSON_PATH,
    OUTBOX_JSON_PATH,
)
from config import GMAIL_ENABLED, GMAIL_QUERY, GMAIL_MAX_RESULTS
from gmail_service import fetch_inbox as gmail_fetch_inbox
from gmail_service import send_email as gmail_send_email


class Message:
    def __init__(self, message_id: str, sender: str, recipient: str, subject: str, content: str, channel: str, timestamp: str, thread_id: Optional[str] = None):
        self.id = message_id
        self.sender = sender
        self.recipient = recipient
        self.subject = subject
        self.content = content
        self.channel = channel  # email | chat
        self.timestamp = timestamp
        self.thread_id = thread_id or message_id

    def to_dict(self) -> Dict[str, str]:
        return {
            "id": self.id,
            "sender": self.sender,
            "recipient": self.recipient,
            "subject": self.subject,
            "content": self.content,
            "channel": self.channel,
            "timestamp": self.timestamp,
            "thread_id": self.thread_id,
        }


def _read_json(path: str) -> List[Dict]:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                return data
            if isinstance(data, dict) and "messages" in data and isinstance(data["messages"], list):
                return data["messages"]
            return []
        except json.JSONDecodeError:
            return []


def load_inbox_messages() -> List[Message]:
    if GMAIL_ENABLED:
        records = gmail_fetch_inbox(query=GMAIL_QUERY, max_results=GMAIL_MAX_RESULTS)
    else:
        records = _read_json(INBOX_JSON_PATH)
    messages: List[Message] = []
    for r in records:
        messages.append(
            Message(
                message_id=str(r.get("id") or r.get("message_id") or r.get("timestamp")),
                sender=str(r.get("from") or r.get("sender") or "unknown"),
                recipient=str(r.get("to") or r.get("recipient") or "me@example.com"),
                subject=str(r.get("subject") or "(no subject)"),
                content=str(r.get("body") or r.get("content") or ""),
                channel="email",
                timestamp=str(r.get("timestamp") or ""),
                thread_id=str(r.get("thread_id") or r.get("conversation_id") or r.get("id") or ""),
            )
        )
    return messages


def load_chat_messages() -> List[Message]:
    records = _read_json(CHAT_JSON_PATH)
    messages: List[Message] = []
    for r in records:
        messages.append(
            Message(
                message_id=str(r.get("id") or r.get("message_id") or r.get("timestamp")),
                sender=str(r.get("from") or r.get("sender") or "unknown"),
                recipient=str(r.get("to") or r.get("recipient") or "me"),
                subject=str(r.get("subject") or r.get("topic") or "(chat)"),
                content=str(r.get("text") or r.get("body") or r.get("content") or ""),
                channel="chat",
                timestamp=str(r.get("timestamp") or ""),
                thread_id=str(r.get("thread_id") or r.get("conversation_id") or r.get("id") or ""),
            )
        )
    return messages


def append_outbox(record: Dict) -> None:
    os.makedirs(os.path.dirname(OUTBOX_JSON_PATH), exist_ok=True)
    existing: List[Dict] = _read_json(OUTBOX_JSON_PATH)
    existing.append(record)
    with open(OUTBOX_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)


def send_reply(recipient: str, subject: str, body: str, thread_id: Optional[str] = None) -> Optional[str]:
    if GMAIL_ENABLED:
        try:
            return gmail_send_email(recipient, subject, body, thread_id=thread_id)
        except Exception:
            return None
    # For JSON mode, we only append to outbox and do not truly send
    return None


