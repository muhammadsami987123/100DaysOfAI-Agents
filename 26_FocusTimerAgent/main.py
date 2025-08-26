from __future__ import annotations

import argparse
import os
import sys
import threading
from typing import Optional

# Support running as a module or as a script
try:
    from .config import CONFIG
    from .timer import PomodoroTimer, read_status, write_command, read_history
    from .ai_agent import coach_message
except Exception:  # pragma: no cover
    from config import CONFIG  # type: ignore
    from timer import PomodoroTimer, read_status, write_command, read_history  # type: ignore
    from ai_agent import coach_message  # type: ignore


def _start_timer(args: argparse.Namespace) -> None:
    work = args.work or CONFIG.default_work_minutes
    short_break = args.break_minutes or CONFIG.default_short_break_minutes
    long_break = args.long or CONFIG.default_long_break_minutes
    cycles = args.cycles or CONFIG.cycles_before_long_break
    voice = not args.mute

    timer = PomodoroTimer(
        work_minutes=work,
        short_break_minutes=short_break,
        long_break_minutes=long_break,
        cycles_before_long=cycles,
        voice_enabled=voice,
    )
    timer.run()


def _print_status() -> None:
    status = read_status()
    mode = status.get("mode", "idle")
    remaining = status.get("session_seconds_remaining", 0)
    minutes = remaining // 60
    seconds = remaining % 60
    paused = status.get("is_paused", False)
    cycle = status.get("current_cycle", 0)
    voice = status.get("voice_enabled", True)
    print(f"Mode: {mode} | Remaining: {minutes:02d}:{seconds:02d} | Cycle: {cycle} | Paused: {paused} | Voice: {voice}")


def _print_history() -> None:
    hist = read_history()
    if not hist:
        print("No history yet.")
        return
    for day, data in sorted(hist.items()):
        print(f"{day}: {data.get('completed_focus_sessions', 0)} focus sessions")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="focus-timer",
        description="FocusTimerAgent - Pomodoro Timer with TTS",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_start = sub.add_parser("start", help="Start the Pomodoro timer")
    p_start.add_argument("--work", type=int, dest="work", help="Work minutes")
    p_start.add_argument("--break", type=int, dest="break_minutes", help="Short break minutes")
    p_start.add_argument("--long", type=int, dest="long", help="Long break minutes")
    p_start.add_argument("--cycles", type=int, dest="cycles", help="Cycles before long break")
    p_start.add_argument("--mute", action="store_true", help="Start with voice reminders muted")
    p_start.set_defaults(func=_start_timer)

    p_pause = sub.add_parser("pause", help="Pause the current session")
    p_pause.set_defaults(func=lambda *_: write_command("pause"))

    p_resume = sub.add_parser("resume", help="Resume the current session")
    p_resume.set_defaults(func=lambda *_: write_command("resume"))

    p_stop = sub.add_parser("stop", help="Stop the timer")
    p_stop.set_defaults(func=lambda *_: write_command("stop"))

    p_status = sub.add_parser("status", help="Show current timer status")
    p_status.set_defaults(func=lambda *_: _print_status())

    p_history = sub.add_parser("history", help="Show daily completed sessions")
    p_history.set_defaults(func=lambda *_: _print_history())

    p_mute = sub.add_parser("mute", help="Mute voice reminders")
    p_mute.set_defaults(func=lambda *_: write_command("mute"))

    p_unmute = sub.add_parser("unmute", help="Unmute voice reminders")
    p_unmute.set_defaults(func=lambda *_: write_command("unmute"))

    p_coach = sub.add_parser("coach", help="Ask the coach for a motivational tip")
    p_coach.add_argument("--context", type=str, default="mid-session", help="e.g., starting focus, mid-session, struggling, ending soon")
    p_coach.add_argument("--mood", type=str, default="neutral", help="e.g., energized, tired, distracted")
    p_coach.add_argument("--minutes-left", type=int, dest="minutes_left", default=None)
    p_coach.set_defaults(func=lambda args: print(coach_message(args.context, args.mood, args.minutes_left)))

    return parser


def main(argv: Optional[list[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    func = getattr(args, "func", None)
    if func is None:
        parser.print_help()
        return
    func(args)


if __name__ == "__main__":
    main()


