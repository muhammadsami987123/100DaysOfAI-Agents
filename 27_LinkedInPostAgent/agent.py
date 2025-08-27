import argparse
import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

from config import load_env
from openai_utils import generate_post_with_ai, enhance_post_text
from linkedin_service import LinkedInService


BASE_DIR = Path(__file__).resolve().parent
DRAFTS_DIR = BASE_DIR / "drafts"
POSTS_DIR = BASE_DIR / "posts"
LOGS_DIR = BASE_DIR / "logs"
SCHEDULE_FILE = BASE_DIR / "scheduled_posts.json"


def ensure_directories_exist() -> None:
    DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)


def load_text_from_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def save_draft(text: str) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    draft_path = DRAFTS_DIR / f"draft_{timestamp}.md"
    with open(draft_path, "w", encoding="utf-8") as f:
        f.write(text)
    return draft_path


def save_post_history(entry: dict) -> None:
    history_path = BASE_DIR / "post_history.json"
    history = []
    if history_path.exists():
        try:
            with open(history_path, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            history = []
    history.append(entry)
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def schedule_post(text: str, when: str) -> dict:
    scheduled_at = parse_time_input(when)
    item = {
        "text": text,
        "scheduled_at": scheduled_at.isoformat(),
        "status": "scheduled",
        "created_at": datetime.now().isoformat(),
    }
    data = []
    if SCHEDULE_FILE.exists():
        try:
            with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = []
    data.append(item)
    with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return item


def parse_time_input(when: str) -> datetime:
    when = when.strip().lower()
    now = datetime.now()
    if when.startswith("in "):
        parts = when.split()
        if len(parts) >= 3 and parts[0] == "in":
            try:
                amount = int(parts[1])
            except ValueError:
                raise ValueError("Invalid time amount in relative expression.")
            unit = parts[2]
            if unit.startswith("min"):
                return now + timedelta(minutes=amount)
            if unit.startswith("hour"):
                return now + timedelta(hours=amount)
            if unit.startswith("day"):
                return now + timedelta(days=amount)
            raise ValueError("Unsupported time unit. Use minutes/hours/days.")
    if ":" in when:
        try:
            hour, minute = when.split(":", 1)
            hour_i = int(hour)
            minute_i = int(minute)
            candidate = now.replace(hour=hour_i, minute=minute_i, second=0, microsecond=0)
            if candidate <= now:
                candidate = candidate + timedelta(days=1)
            return candidate
        except Exception as exc:
            raise ValueError("Invalid HH:MM time.") from exc
    raise ValueError("Time format not recognized. Use 'HH:MM' or 'in N hours'.")


def prompt_input(prompt: str) -> str:
    print(prompt)
    return input().strip()


def preview_post(text: str) -> None:
    print("\n===== Post Preview =====")
    print(text)
    print("\n========================")
    print(f"Characters: {len(text)}  Words: {len(text.split())}")


def handle_create_flow(args: argparse.Namespace) -> None:
    ensure_directories_exist()
    load_env()

    title_or_topic = prompt_input("What's the topic or title?")

    use_ai_answer = prompt_input("Do you want AI to write the post? (Y/n)") or "Y"
    use_ai = use_ai_answer.lower().startswith("y")

    if use_ai:
        tone_choice = prompt_input("Choose tone: (1) Professional (2) Casual (3) Motivational (4) Technical")
        tone_map = {
            "1": "professional",
            "2": "casual",
            "3": "motivational",
            "4": "technical",
        }
        tone = tone_map.get(tone_choice, "professional")
        base_text = generate_post_with_ai(title_or_topic, tone=tone)
    else:
        input_mode = prompt_input("Provide content via: (1) Manual paste (2) File path")
        if input_mode == "2":
            file_path = prompt_input("Enter file path (.md or .txt):")
            base_text = load_text_from_file(file_path)
        else:
            print("Paste your post content. End with an empty line:")
            lines = []
            while True:
                line = input()
                if line.strip() == "":
                    break
                lines.append(line)
            base_text = "\n".join(lines)

    enhance_answer = prompt_input("Enhance text? Add tone, hashtags, emojis? (Y/n)") or "Y"
    if enhance_answer.lower().startswith("y"):
        tone_choice = prompt_input("Tone: (1) Professional (2) Casual (3) Motivational (4) Technical")
        tone_map = {
            "1": "professional",
            "2": "casual",
            "3": "motivational",
            "4": "technical",
        }
        tone = tone_map.get(tone_choice, "professional")
        add_emojis = (prompt_input("Add emojis? (Y/n)") or "Y").lower().startswith("y")
        add_hashtags = (prompt_input("Add hashtags? (Y/n)") or "Y").lower().startswith("y")
        text = enhance_post_text(base_text, tone=tone, add_emojis=add_emojis, add_hashtags=add_hashtags)
    else:
        text = base_text

    preview_post(text)

    action = prompt_input("What do you want to do?\n(1) Post now\n(2) Save as Draft\n(3) Schedule")

    service = LinkedInService()

    if action == "1":
        ok = service.post_now(text)
        status = "posted" if ok else "failed"
        save_post_history({"status": status, "text": text, "when": datetime.now().isoformat()})
        print("Posted successfully." if ok else "Failed to post.")
    elif action == "2":
        draft_path = save_draft(text)
        save_post_history({"status": "drafted", "text": text, "path": str(draft_path), "when": datetime.now().isoformat()})
        print(f"Draft saved at {draft_path}")
    elif action == "3":
        when = prompt_input("Enter time to post (e.g., 14:00 or 'in 1 hour')")
        item = schedule_post(text, when)
        save_post_history({"status": "scheduled", "text": text, "when": item["scheduled_at"]})
        scheduled_dt = datetime.fromisoformat(item["scheduled_at"]).strftime("%I:%M %p").lstrip("0")
        print(f"Post scheduled for {scheduled_dt}. ✅")
    else:
        print("No action taken.")


def main() -> None:
    parser = argparse.ArgumentParser(description="LinkedInPostAgent - Create and manage LinkedIn posts")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("create", help="Start interactive flow to create a post")
    sub.add_parser("schedule-runner", help="Run the background scheduler loop to post scheduled items")

    args = parser.parse_args()

    ensure_directories_exist()

    if args.command == "create" or args.command is None:
        handle_create_flow(args)
        return

    if args.command == "schedule-runner":
        from scheduler import run_scheduler_loop
        run_scheduler_loop(schedule_file=SCHEDULE_FILE)
        return

    parser.print_help()


if __name__ == "__main__":
    main()


