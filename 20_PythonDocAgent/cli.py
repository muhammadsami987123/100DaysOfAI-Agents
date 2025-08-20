from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.markdown import Markdown
from rich.live import Live
from rich.spinner import Spinner
from time import sleep

from ai_agent import OpenAIClient
from config import SUPPORTED_LANGUAGES, get_language_config, load_settings, validate_config
from content_fetcher import FetchedContent, fetch_from_url, read_file, normalize_inline, extract_code_blocks
from doc_analyzer import (
    ConversationMemory,
    SYSTEM_PROMPT,
    build_explain_prompt,
    build_summary_prompt,
    build_walkthrough_prompt,
)


console = Console()


def print_banner() -> None:
    console.print(Panel.fit("PythonDocAgent - Day 20 of #100DaysOfAI-Agents\nAnalyze, explain, and summarize Python code/docs", title="🤖 PythonDocAgent", subtitle="OpenAI + Rich CLI"))


def copy_to_clipboard(text: str) -> bool:
    try:
        import pyperclip
        pyperclip.copy(text)
        return True
    except Exception:
        return False


def show_code_blocks(md_text: str) -> None:
    blocks = extract_code_blocks(md_text)
    if not blocks:
        return
    console.print("\n[bold]Detected code blocks:[/bold]")
    for idx, (lang, body) in enumerate(blocks, start=1):
        syntax = Syntax(body, (lang or "python"), theme="monokai", line_numbers=True)
        console.print(Panel(syntax, title=f"Block {idx} ({lang or 'python'})"))


def render_markdown_panel(text: str, title: str = "PythonDocAgent") -> None:
    renderable = Markdown(text or "(no response)")
    console.print(Panel(renderable, title=title, border_style="cyan", expand=True))


def handle_streaming_to_console(stream_gen, language_cfg):
    output_chunks: list[str] = []
    console.print("[bold blue]Processing…[/bold blue]")
    spinner = Spinner("dots", text="Calling OpenAI…")
    with Live(spinner, console=console, refresh_per_second=12):
        for chunk in stream_gen:
            output_chunks.append(chunk)
            # Show approximate progress blocks
            merged = "".join(output_chunks)
            blocks = max(1, len(merged) // 120)
            spinner.text = f"Generating… [{blocks} blocks]"
    with console.status("[bold magenta]Formatting…[/bold magenta]", spinner="dots12"):
        sleep(0.05)
    console.print("[bold magenta]Responding…[/bold magenta]")
    final = "".join(output_chunks)
    render_markdown_panel(final, title="PythonDocAgent")
    return final


def build_messages(memory: ConversationMemory, user_content: str) -> list[dict]:
    messages = memory.to_messages()
    messages.append({"role": "user", "content": user_content})
    return messages


def command_explain(content: FetchedContent, lang: str, client: OpenAIClient, memory: ConversationMemory) -> str:
    lcfg = get_language_config(lang)
    console.print(lcfg["analyzing"]) 
    prompt = build_explain_prompt(lang, content.title, content.text)
    messages = build_messages(memory, prompt)
    if client.settings.stream:
        streamed = handle_streaming_to_console(client.stream_chat(SYSTEM_PROMPT, messages), lcfg)
        memory.add("user", prompt)
        memory.add("assistant", streamed)
        return streamed
    else:
        console.print("[bold blue]Processing…[/bold blue]")
        result = client.complete_chat(SYSTEM_PROMPT, messages)
        with console.status("[bold magenta]Formatting…[/bold magenta]", spinner="dots12"):
            sleep(0.05)
        console.print("[bold magenta]Responding…[/bold magenta]")
        render_markdown_panel(result)
        memory.add("user", prompt)
        memory.add("assistant", result)
        return result


def command_summary(content: FetchedContent, lang: str, client: OpenAIClient, memory: ConversationMemory) -> str:
    lcfg = get_language_config(lang)
    console.print(lcfg["analyzing"]) 
    prompt = build_summary_prompt(lang, content.title, content.text)
    messages = build_messages(memory, prompt)
    if client.settings.stream:
        streamed = handle_streaming_to_console(client.stream_chat(SYSTEM_PROMPT, messages), lcfg)
        memory.add("user", prompt)
        memory.add("assistant", streamed)
        return streamed
    else:
        console.print("[bold blue]Processing…[/bold blue]")
        result = client.complete_chat(SYSTEM_PROMPT, messages)
        with console.status("[bold magenta]Formatting…[/bold magenta]", spinner="dots12"):
            sleep(0.05)
        console.print("[bold magenta]Responding…[/bold magenta]")
        render_markdown_panel(result)
        memory.add("user", prompt)
        memory.add("assistant", result)
        return result


def command_walkthrough(content: FetchedContent, lang: str, client: OpenAIClient, memory: ConversationMemory, line_from: int, line_to: int) -> str:
    lcfg = get_language_config(lang)
    console.print(lcfg["analyzing"]) 
    prompt = build_walkthrough_prompt(lang, content.title, content.text, line_from, line_to)
    messages = build_messages(memory, prompt)
    if client.settings.stream:
        streamed = handle_streaming_to_console(client.stream_chat(SYSTEM_PROMPT, messages), lcfg)
        memory.add("user", prompt)
        memory.add("assistant", streamed)
        return streamed
    else:
        console.print("[bold blue]Processing…[/bold blue]")
        result = client.complete_chat(SYSTEM_PROMPT, messages)
        with console.status("[bold magenta]Formatting…[/bold magenta]", spinner="dots12"):
            sleep(0.05)
        console.print("[bold magenta]Responding…[/bold magenta]")
        render_markdown_panel(result)
        memory.add("user", prompt)
        memory.add("assistant", result)
        return result


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="PythonDocAgent - Explain/summarize Python code or docs via OpenAI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python main.py --url https://docs.python.org/3/library/itertools.html --explain\n"
            "  python main.py --file my_module.py --summary\n"
            "  python main.py --inline 'def add(x,y): return x+y' --walk 1 20\n"
            "  python main.py --url https://github.com/psf/requests --lang hi --explain\n"
        ),
    )

    src = parser.add_mutually_exclusive_group(required=False)
    src.add_argument("--url", "-u", help="Public URL to fetch and analyze")
    src.add_argument("--file", "-f", help="Local file path to analyze")
    src.add_argument("--inline", "-i", help="Inline code or text to analyze")

    mode = parser.add_mutually_exclusive_group(required=False)
    mode.add_argument("--explain", action="store_true", help="Explain code/docs and suggest improvements")
    mode.add_argument("--summary", action="store_true", help="Summarize section-wise")
    mode.add_argument("--walk", nargs=2, metavar=("FROM", "TO"), help="Line-by-line walkthrough between two line numbers")
    mode.add_argument("--chat", action="store_true", help="Interactive chat mode with memory")

    parser.add_argument("--lang", "-l", choices=list(SUPPORTED_LANGUAGES.keys()), default="en", help="Language for the response")
    parser.add_argument("--copy", action="store_true", help="Copy the final answer to clipboard if possible")
    parser.add_argument("--show-code", action="store_true", help="Render detected code blocks with syntax highlighting")
    return parser.parse_args(argv)


def load_content(args: argparse.Namespace) -> FetchedContent:
    if args.url:
        console.print(get_language_config(args.lang)["fetching"]) 
        return fetch_from_url(args.url)
    if args.file:
        return read_file(args.file)
    if args.inline:
        return normalize_inline("Inline", args.inline)
    # default empty content for chat mode
    return normalize_inline("Chat", "")


def main(argv: Optional[list[str]] = None) -> int:
    print_banner()

    errors = validate_config()
    if errors:
        for e in errors:
            console.print(f"[red]❌ {e}[/red]")
        return 1

    settings = load_settings()
    lang = settings.default_language

    args = parse_args(argv)
    if args.lang:
        lang = args.lang

    # Sensible defaults:
    # - If no mode provided and no source -> default to chat mode
    # - If no mode provided but a source exists -> default to explain mode
    has_source = bool(args.url or args.file or args.inline)
    if not (args.chat or args.explain or args.summary or args.walk):
        if has_source:
            args.explain = True
        else:
            args.chat = True

    content = load_content(args)
    client = OpenAIClient()
    memory = ConversationMemory(max_turns=settings.history_max_turns)

    if args.chat:
        console.print("[bold]Interactive chat. Type 'exit' to quit.[/bold]")
        while True:
            try:
                console.print("[bold green]Listening…[/bold green]")
                user = console.input("[cyan]You[/cyan]: ")
            except (EOFError, KeyboardInterrupt):
                break
            if not user or user.strip().lower() in {"exit", "quit"}:
                break
            messages = memory.to_messages() + [{"role": "user", "content": user}]
            if client.settings.stream:
                output = handle_streaming_to_console(client.stream_chat(SYSTEM_PROMPT, messages), get_language_config(lang))
            else:
                console.print("[bold blue]Processing…[/bold blue]")
                output = client.complete_chat(SYSTEM_PROMPT, messages)
                with console.status("[bold magenta]Formatting…[/bold magenta]", spinner="dots12"):
                    sleep(0.05)
                console.print("[bold magenta]Responding…[/bold magenta]")
                render_markdown_panel(output)
            memory.add("user", user)
            memory.add("assistant", output)
        return 0
    elif args.explain:
        result = command_explain(content, lang, client, memory)
    elif args.summary:
        result = command_summary(content, lang, client, memory)
    elif args.walk:
        from_line = int(args.walk[0])
        to_line = int(args.walk[1])
        result = command_walkthrough(content, lang, client, memory, from_line, to_line)
    else:
        # Fallback safety: start chat
        console.print("[bold]Interactive chat. Type 'exit' to quit.[/bold]")
        while True:
            try:
                user = console.input("[cyan]> [/cyan]")
            except (EOFError, KeyboardInterrupt):
                break
            if not user or user.strip().lower() in {"exit", "quit"}:
                break
            messages = memory.to_messages() + [{"role": "user", "content": user}]
            if client.settings.stream:
                output = handle_streaming_to_console(client.stream_chat(SYSTEM_PROMPT, messages), get_language_config(lang))
            else:
                output = client.complete_chat(SYSTEM_PROMPT, messages)
                console.print(output)
            memory.add("user", user)
            memory.add("assistant", output)
        return 0

    if args.show_code:
        show_code_blocks(result)

    if args.copy and copy_to_clipboard(result):
        console.print(get_language_config(lang)["copied"]) 

    return 0


if __name__ == "__main__":
    sys.exit(main())


