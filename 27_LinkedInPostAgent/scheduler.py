import json
import time
from datetime import datetime
from pathlib import Path

from linkedin_service import LinkedInService


def run_scheduler_loop(schedule_file: Path) -> None:
    service = LinkedInService()
    print("Scheduler running... Press Ctrl+C to stop.")
    while True:
        try:
            if schedule_file.exists():
                with open(schedule_file, "r", encoding="utf-8") as f:
                    items = json.load(f)
            else:
                items = []

            changed = False
            now = datetime.now()
            for item in items:
                if item.get("status") == "scheduled":
                    scheduled_at = datetime.fromisoformat(item["scheduled_at"])
                    if now >= scheduled_at:
                        ok = service.post_now(item["text"])
                        item["status"] = "posted" if ok else "failed"
                        item["posted_at"] = datetime.now().isoformat()
                        changed = True

            if changed:
                with open(schedule_file, "w", encoding="utf-8") as f:
                    json.dump(items, f, ensure_ascii=False, indent=2)

            time.sleep(15)
        except KeyboardInterrupt:
            print("Scheduler stopped.")
            break


