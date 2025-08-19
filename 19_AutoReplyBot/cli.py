import argparse
import sys
import time
from typing import Optional, List
import pyperclip
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.live import Live
from rich.spinner import Spinner

from config import (
    OPENAI_API_KEY,
    DEFAULT_TONE,
    DEFAULT_LANGUAGE,
    STREAMING,
    AUTO_MODE_DELAY_SECONDS,
    GMAIL_ENABLED,
)
from agent import AutoReplyBot
from sources import load_inbox_messages, load_chat_messages, append_outbox, Message, send_reply


def build_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AutoReplyBot — Email/Chat Auto-Responder")
    parser.add_argument("--mode", choices=["manual", "auto"], default="manual", help="Run in manual or auto mode")
    parser.add_argument("--tone", default=DEFAULT_TONE, help="Reply tone: formal, friendly, technical, concise")
    parser.add_argument("--lang", default=DEFAULT_LANGUAGE, help="Preferred language or 'auto'")
    parser.add_argument("--source", choices=["email", "chat", "both", "gmail"], default="both", help="Which source to read from")
    parser.add_argument("--max", type=int, default=50, help="Max messages to process")
    parser.add_argument("--no-stream", action="store_true", help="Disable streaming even if enabled")
    parser.add_argument("--send", action="store_true", help="Actually send replies (Gmail only)")
    return parser.parse_args()


def render_copy_hint(console: Console, text: str) -> None:
    console.print("[dim]Tip: Type 'copy' to copy to clipboard. Output is also saved to outbox.json.[/dim]")


def show_status(console: Console, status: str) -> None:
    console.print(f"[cyan]{status}[/cyan]")


def manual_flow(bot: AutoReplyBot, message: Message, tone: str, lang: str, console: Console, streaming: bool, args_send: bool) -> None:
    show_status(console, "Reading message…")
    console.print(Panel.fit(f"From: {message.sender}\nTo: {message.recipient}\nSubject: {message.subject}\n\n{message.content}", title=f"{message.channel.upper()} Message"))

    show_status(console, "Generating reply…")
    if streaming:
        spinner = Spinner("dots", text="Calling OpenAI…")
        reply_text = ""
        with Live(spinner, console=console, refresh_per_second=12):
            for token in bot.stream_reply(message, tone=tone, language=lang):
                reply_text += token
                spinner.text = f"Generating… ({len(reply_text)//50} blocks)"
    else:
        reply_text = bot.generate_reply(message, tone=tone, language=lang)

    console.print(Panel(reply_text, title="Suggested Reply", border_style="green"))
    render_copy_hint(console, reply_text)

    action = Prompt.ask("Type 'copy' to copy, or press Enter to continue", default="")
    if action.strip().lower() == "copy":
        try:
            pyperclip.copy(reply_text)
            console.print("[green]Copied to clipboard.[/green]")
        except Exception as e:
            console.print(f"[yellow]Copy failed:[/yellow] {e}")

    edited = Prompt.ask("Edit reply? (leave blank to keep)", default="")
    final_text = edited if edited.strip() else reply_text
    if args_send:
        if not GMAIL_ENABLED:
            console.print("[yellow]Gmail sending is disabled (GMAIL_ENABLED=false). Not sent.[/yellow]")
        else:
            sent_id = send_reply(message.sender, f"Re: {message.subject}", final_text, thread_id=message.thread_id)
            if sent_id:
                console.print(f"[green]Sent via Gmail:[/green] {sent_id}")
            else:
                console.print("[yellow]Failed to send via Gmail. Saved to outbox (not sent).[/yellow]")
    else:
        console.print("[yellow]Send disabled. Use --send to actually send via Gmail.[/yellow]")
    show_status(console, "Reply saved ✔")
    append_outbox({
        "thread_id": message.thread_id,
        "in_reply_to": message.id,
        "channel": message.channel,
        "reply": final_text,
        "timestamp": time.time(),
    })


def auto_flow(bot: AutoReplyBot, message: Message, tone: str, lang: str, console: Console, streaming: bool, args_send: bool) -> None:
    allowed, reason = bot.classify_for_auto_mode(message)
    if not allowed:
        console.print(f"[yellow]Skipping message[/yellow] — {reason}")
        return
    show_status(console, "Reading message…")
    show_status(console, "Generating reply…")
    if streaming:
        spinner = Spinner("dots", text="Calling OpenAI…")
        reply_text = ""
        with Live(spinner, console=console, refresh_per_second=12):
            for token in bot.stream_reply(message, tone=tone, language=lang):
                reply_text += token
                spinner.text = f"Generating… ({len(reply_text)//50} blocks)"
    else:
        reply_text = bot.generate_reply(message, tone=tone, language=lang)
    if args_send:
        if not GMAIL_ENABLED:
            console.print("[yellow]Gmail sending is disabled (GMAIL_ENABLED=false). Not sent.[/yellow]")
        else:
            sent_id = send_reply(message.sender, f"Re: {message.subject}", reply_text, thread_id=message.thread_id)
            if sent_id:
                console.print(f"[green]Sent via Gmail:[/green] {sent_id}")
            else:
                console.print("[yellow]Failed to send via Gmail. Saved to outbox (not sent).[/yellow]")
    else:
        console.print("[yellow]Send disabled. Use --send to actually send via Gmail.[/yellow]")
    show_status(console, "Reply saved ✔")
    append_outbox({
        "thread_id": message.thread_id,
        "in_reply_to": message.id,
        "channel": message.channel,
        "reply": reply_text,
        "timestamp": time.time(),
    })
    time.sleep(AUTO_MODE_DELAY_SECONDS)


def render_message_list(console: Console, items: List[Message]) -> None:
    table = Table(show_lines=False)
    table.add_column("#", justify="right", style="dim", width=3)
    table.add_column("Channel", style="cyan", width=8)
    table.add_column("From", style="magenta")
    table.add_column("Subject/Preview", style="white")
    table.add_column("When", style="dim", width=20)
    for idx, m in enumerate(items):
        subject = m.subject if m.channel == "email" else (m.subject or "(chat)")
        preview = (m.content[:80] + "…") if len(m.content) > 80 else m.content
        table.add_row(str(idx + 1), m.channel, m.sender, f"{subject} — {preview}", m.timestamp)
    console.print(table)


def manual_compose(bot: AutoReplyBot, message: Message, tone: str, lang: str, console: Console, streaming: bool) -> (str, str):
    show_status(console, "Reading message…")
    console.print(Panel.fit(
        f"From: {message.sender}\nTo: {message.recipient}\nSubject: {message.subject}\n\n{message.content}",
        title=f"{message.channel.upper()} Message"
    ))

    show_status(console, "Generating reply…")
    if streaming:
        spinner = Spinner("dots", text="Calling OpenAI…")
        reply_text = ""
        with Live(spinner, console=console, refresh_per_second=12):
            for token in bot.stream_reply(message, tone=tone, language=lang):
                reply_text += token
                spinner.text = f"Generating… ({len(reply_text)//50} blocks)"
    else:
        reply_text = bot.generate_reply(message, tone=tone, language=lang)

    console.print(Panel(reply_text, title="Suggested Reply", border_style="green"))
    render_copy_hint(console, reply_text)

    action = Prompt.ask("Type 'copy' to copy, or press Enter to continue", default="")
    if action.strip().lower() == "copy":
        try:
            pyperclip.copy(reply_text)
            console.print("[green]Copied to clipboard.[/green]")
        except Exception as e:
            console.print(f"[yellow]Copy failed:[/yellow] {e}")

    edited = Prompt.ask("Edit reply? (leave blank to keep)", default="")
    final_text = edited if edited.strip() else reply_text

    next_action = Prompt.ask("Action", choices=["send", "back", "exit"], default="send")
    return final_text, next_action


def interactive_manual_session(bot: AutoReplyBot, messages: List[Message], tone: str, lang: str, console: Console, streaming: bool, args_send: bool) -> None:
    working: List[Message] = list(messages)
    while True:
        console.print(Panel.fit("Select a message to reply, or ignore items you don't want.", title="Inbox"))
        if not working:
            console.print("[green]No more messages to process.[/green]")
            break
        render_message_list(console, working)
        cmd = Prompt.ask("Enter number to open, 'ignore N' to remove, or 'q' to exit", default="")
        cmd_str = cmd.strip().lower()
        if cmd_str in {"q", "quit", "exit"}:
            break
        if cmd_str.startswith("ignore "):
            try:
                n = int(cmd_str.split()[1])
                if 1 <= n <= len(working):
                    removed = working.pop(n - 1)
                    console.print(f"[yellow]Ignored:[/yellow] {removed.subject or removed.content[:30]}")
                else:
                    console.print("[red]Invalid index.[/red]")
            except ValueError:
                console.print("[red]Usage: ignore N[/red]")
            continue
        try:
            n = int(cmd_str)
        except ValueError:
            console.print("[yellow]Please enter a valid command or number.[/yellow]")
            continue
        if not (1 <= n <= len(working)):
            console.print("[red]Invalid index.[/red]")
            continue
        message = working[n - 1]
        final_text, pre_action = manual_compose(bot, message, tone, lang, console, streaming)
        if pre_action == "exit":
            break
        if pre_action == "back":
            console.print("[cyan]Back to list.[/cyan]")
            continue

        if args_send:
            if not GMAIL_ENABLED:
                console.print("[yellow]Gmail sending is disabled (GMAIL_ENABLED=false). Not sent.[/yellow]")
            else:
                sent_id = send_reply(message.sender, f"Re: {message.subject}", final_text, thread_id=message.thread_id)
                if sent_id:
                    console.print(f"[green]Sent via Gmail:[/green] {sent_id}")
                else:
                    console.print("[yellow]Failed to send via Gmail. Saved to outbox (not sent).[/yellow]")
        else:
            console.print("[yellow]Send disabled. Use --send to actually send via Gmail.[/yellow]")
        append_outbox({
            "thread_id": message.thread_id,
            "in_reply_to": message.id,
            "channel": message.channel,
            "reply": final_text,
            "timestamp": time.time(),
        })
        show_status(console, "Reply saved ✔")

        post_action = Prompt.ask("Next", choices=["back", "exit"], default="back")
        working.pop(n - 1)
        if post_action == "exit":
            break

def main() -> int:
    console = Console()
    args = build_args()

    bot = None
    inbox: List[Message] = []
    chats: List[Message] = []
    init_error: Optional[Exception] = None

    spinner = Spinner("dots", text="Starting AutoReplyBot…")
    with Live(spinner, console=console, refresh_per_second=12):
        try:
            bot = AutoReplyBot()
        except Exception as e:
            init_error = e
        streaming = False if args.no_stream else STREAMING
        tone = args.tone
        lang = args.lang
        spinner.text = "Loading messages…"
        try:
            if args.source == "gmail":
                inbox = load_inbox_messages()
                chats = []
            else:
                inbox = load_inbox_messages() if args.source in {"email", "both"} else []
                chats = load_chat_messages() if args.source in {"chat", "both"} else []
        except Exception as e:
            if init_error is None:
                init_error = e
    if init_error and bot is None:
        console.print(f"[red]Error:[/red] {init_error}")
        console.print("Ensure you set OPENAI_API_KEY in a .env file.")
        return 1

    messages = (inbox + chats)[: args.max]

    if not messages:
        console.print("[yellow]No messages found in sources. Add JSON to data folder.[/yellow]")
        return 0

    console.print(Panel.fit(f"AutoReplyBot — Mode: {args.mode} | Tone: {args.tone} | Language: {args.lang} | Streaming: {False if args.no_stream else STREAMING} | Gmail: {'ON' if GMAIL_ENABLED else 'OFF'}", title="AutoReplyBot"))

    if args.mode == "manual":
        interactive_manual_session(bot, messages, args.tone, args.lang, console, False if args.no_stream else STREAMING, args.send)
    else:
        for msg in messages:
            auto_flow(bot, msg, args.tone, args.lang, console, False if args.no_stream else STREAMING, args.send)

    console.print("[green]Done.[/green]")
    return 0


if __name__ == "__main__":
    sys.exit(main())


