import sys
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.status import Status
from rich.markdown import Markdown
from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text
from rich.table import Table
from rich.columns import Columns
from time import sleep
from command_explainer import CommandExplainer, detect_os


def print_banner(console: Console) -> None:
    banner_text = Text()
    banner_text.append("AICommandExplainerAgent ", style="bold cyan")
    banner_text.append("⚙️", style="bold yellow")
    banner_text.append("\n", style="bold cyan")
    banner_text.append("Smart Terminal Command Interpreter", style="dim")
    banner_text.append("\n", style="dim")
    banner_text.append("Type 'help' for commands, 'exit' to leave.", style="dim")
    
    console.print(Panel.fit(banner_text, border_style="cyan"))


def print_help(console: Console) -> None:
    help_text = """
[bold]Available Commands:[/bold]

[cyan]1. Explain Command[/cyan]
   • Enter any shell/terminal command to get a detailed explanation
   • Example: `rsync -avz folder/ user@host:/backup`

[cyan]2. Suggest Command[/cyan]
   • Type 'suggest:' followed by what you want to do
   • Example: `suggest: copy all .txt files to another folder`

[cyan]3. Quick Analysis[/cyan]
   • Type 'analyze:' followed by a command for quick breakdown
   • Example: `analyze: rm -rf /tmp/*`

[cyan]4. Help[/cyan]
   • Type 'help' to see this message

[cyan]5. Exit[/cyan]
   • Type 'exit' or 'quit' to leave

[bold yellow]Note:[/bold] The agent will automatically detect dangerous commands and provide safety warnings.
    """
    console.print(Panel(help_text, title="Help", border_style="green"))


def print_command_summary(console: Console, summary: dict, command: str) -> None:
    """Display a quick command analysis."""
    table = Table(title=f"Quick Analysis: {command}", show_header=True, header_style="bold magenta")
    table.add_column("Component", style="cyan", no_wrap=True)
    table.add_column("Details", style="white")
    
    table.add_row("Main Command", summary.get("main_command", "N/A"))
    table.add_row("Flags", ", ".join(summary.get("flags", [])) or "None")
    table.add_row("Arguments", ", ".join(summary.get("arguments", [])) or "None")
    table.add_row("Total Parts", str(summary.get("total_parts", 0)))
    
    if summary.get("is_dangerous"):
        danger_style = "bold red"
        table.add_row("⚠️  Safety", "DANGEROUS COMMAND DETECTED", style=danger_style)
        table.add_row("Dangerous Patterns", ", ".join(summary.get("dangerous_flags", [])), style=danger_style)
    else:
        table.add_row("✅ Safety", "Command appears safe")
    
    console.print(table)


def main() -> int:
    console = Console()
    print_banner(console)

    try:
        explainer = CommandExplainer()
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        console.print("Ensure you set OPENAI_API_KEY in a .env file.")
        return 1

    os_profile = detect_os()
    console.print(f"Detected OS: [bold]{os_profile['name']}[/bold] using [bold]{os_profile['shell']}[/bold]")
    console.print("\n[dim]Type 'help' to see available commands.[/dim]")

    while True:
        try:
            console.print("\n[bold green]Ready for commands…[/bold green]")
            user_input: str = Prompt.ask("[cyan]You[/cyan]")
            
            if user_input.strip().lower() in {"exit", "quit"}:
                console.print("[yellow]Goodbye! Happy coding! 🚀[/yellow]")
                break
                
            if user_input.strip().lower() == "help":
                print_help(console)
                continue
                
            if not user_input.strip():
                continue

            # Handle different input types
            if user_input.lower().startswith("suggest:"):
                # Command suggestion mode
                request = user_input[8:].strip()
                if not request:
                    console.print("[red]Please provide a description of what you want to do.[/red]")
                    continue
                
                console.print(f"[bold blue]Suggesting command for:[/bold blue] {request}")
                console.print("[bold blue]Processing…[/bold blue]")
                
                # Use non-streaming version for suggestions
                suggestion_text = explainer.suggest_command(request, os_profile)
                
                with console.status("[bold magenta]Formatting…[/bold magenta]", spinner="dots12"):
                    renderable = Markdown(suggestion_text or "(no response)")
                    sleep(0.05)
                
                console.print(Panel(renderable, title="Command Suggestion", border_style="green", expand=True))
                
            elif user_input.lower().startswith("analyze:"):
                # Quick analysis mode
                command = user_input[8:].strip()
                if not command:
                    console.print("[red]Please provide a command to analyze.[/red]")
                    continue
                
                console.print(f"[bold blue]Quick Analysis:[/bold blue] {command}")
                summary = explainer.get_command_summary(command)
                print_command_summary(console, summary, command)
                
            else:
                # Regular command explanation mode
                console.print(f"[bold blue]Explaining command:[/bold blue] {user_input}")
                console.print("[bold blue]Processing…[/bold blue]")
                
                streamed_text: str = ""
                spinner = Spinner("dots", text="Analyzing command…")
                with Live(spinner, console=console, refresh_per_second=12):
                    for token in explainer.stream_explanation(user_input, os_profile):
                        streamed_text += token
                        blocks = max(1, len(streamed_text) // 120)
                        spinner.text = f"Analyzing… [{blocks} blocks]"
                
                with console.status("[bold magenta]Formatting…[/bold magenta]", spinner="dots12"):
                    renderable = Markdown(streamed_text or "(no response)")
                    sleep(0.05)
                
                console.print(Panel(renderable, title="Command Explanation", border_style="cyan", expand=True))

        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted. Type 'exit' to quit.[/yellow]")
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
