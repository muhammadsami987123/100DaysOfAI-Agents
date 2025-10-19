import sys
import platform
import os # Added for os.path.exists and os.getenv
from typing import Dict, Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.status import Status
from rich.markdown import Markdown
from rich.live import Live
from rich.spinner import Spinner
from time import sleep

from config import Config
from agents.terminal_helper_agent import TerminalHelperAgent # Import the actual agent

def detect_os() -> Dict[str, str]:
    system = platform.system()
    shell = Config.DEFAULT_SHELL
    if system == "Windows":
        shell = "powershell"
    elif system == "Darwin":
        # Check for zsh or bash
        if os.path.exists("/bin/zsh") and os.getenv("SHELL") == "/bin/zsh":
            shell = "zsh"
        else:
            shell = "bash"
    elif system == "Linux":
        # Check for zsh or bash
        if os.path.exists("/bin/zsh") and os.getenv("SHELL") == "/bin/zsh":
            shell = "zsh"
        else:
            shell = "bash"
        
    return {"id": system.lower() or "unknown", "name": system or "Unknown", "shell": shell}


def print_banner(console: Console) -> None:
    console.print(Panel.fit(
        "[bold cyan]💻 TerminalHelperAI[/bold cyan] — Learn & Use Terminal Commands Easily\n"
        "[dim]Type 'exit' or 'quit' to leave.[/dim]",
        border_style="blue"
    ))


def main() -> int:
    console = Console()
    print_banner(console)

    os_profile = detect_os()

    try:
        agent = TerminalHelperAgent() # Use the actual agent
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        console.print("Ensure you set OPENAI_API_KEY or GEMINI_API_KEY in a .env file.") # Updated message
        return 1

    # os_profile = detect_os() # Moved up
    console.print(f"Detected OS: [bold]{os_profile['name']}[/bold] (Shell: [bold]{os_profile['shell']}[/bold])")

    while True:
        try:
            console.print("\n[bold green]Listening…[/bold green]")
            user_input: str = Prompt.ask("[cyan]You[/cyan]")
            if user_input.strip().lower() in {"exit", "quit"}:
                console.print("[yellow]Goodbye![/yellow]")
                break
            if not user_input.strip():
                continue

            # Placeholder for streaming logic
            console.print("[bold blue]Processing…[/bold blue]")
            streamed_text: str = ""
            spinner = Spinner("dots", text="Generating response…")
            with Live(spinner, console=console, refresh_per_second=12):
                for token in agent.stream(user_input, os_profile): # Use agent's stream method
                    streamed_text += token
                    spinner.text = f"Generating… [{len(streamed_text)} chars]"
                
            with console.status("[bold magenta]Formatting…[/bold magenta]", spinner="dots12"):
                renderable = Markdown(streamed_text or "(no response)")
                sleep(0.05)

            console.print("[bold magenta]Response Ready…[/bold magenta]")
            console.print(Panel(renderable, title="TerminalHelperAI", border_style="green", expand=True))

        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted.[/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
