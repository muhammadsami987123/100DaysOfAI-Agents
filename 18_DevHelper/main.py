import sys
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.status import Status
from rich.markdown import Markdown
from rich.live import Live
from rich.spinner import Spinner
from time import sleep
from assistant import DeveloperAssistant, detect_os


def print_banner(console: Console) -> None:
    console.print(Panel.fit("[bold cyan]DevHelper CLI Bot[/bold cyan] — Ask development questions in English, Urdu, or Hindi\n[dim]Type 'exit' or 'quit' to leave.[/dim]"))


def main() -> int:
    console = Console()
    print_banner(console)

    try:
        assistant = DeveloperAssistant()
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        console.print("Ensure you set OPENAI_API_KEY in a .env file.")
        return 1

    os_profile = detect_os()
    console.print(f"Detected OS: [bold]{os_profile['name']}[/bold]")

    while True:
        try:
            console.print("\n[bold green]Listening…[/bold green]")
            user_input: str = Prompt.ask("[cyan]You[/cyan]")
            if user_input.strip().lower() in {"exit", "quit"}:
                console.print("[yellow]Goodbye![/yellow]")
                break
            if not user_input.strip():
                continue

            # Stream the AI output with a dynamic loader
            console.print("[bold blue]Processing…[/bold blue]")
            streamed_text: str = ""
            spinner = Spinner("dots", text="Calling OpenAI…")
            with Live(spinner, console=console, refresh_per_second=12):
                for token in assistant.stream(user_input, os_profile):
                    streamed_text += token
                    # Show approximate token count block-wise for a blocky feel
                    blocks = max(1, len(streamed_text) // 120)
                    spinner.text = f"Generating… [{blocks} blocks]"

            # Brief formatting loader for nicer UX
            with console.status("[bold magenta]Formatting…[/bold magenta]", spinner="dots12"):
                renderable = Markdown(streamed_text or "(no response)")
                sleep(0.05)

            console.print("[bold magenta]Responding…[/bold magenta]")
            console.print(Panel(renderable, title="DevHelper", border_style="cyan", expand=True))

        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted.[/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
