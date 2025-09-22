import sys
from typing import List, Optional, Dict, Any
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.text import Text
from rich.syntax import Syntax
from rich.table import Table
from rich.box import ROUNDED, HEAVY
from rich import print as rprint
import click
import pyperclip

class CLIInterface:
    """Handles CLI interface and rich output formatting"""

    def __init__(self):
        self.console = Console()

    def print_welcome(self) -> None:
        """Print enhanced welcome message for AIComicWriter"""
        header = """
╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                    🎨 AIComicWriter - AI-Powered Comic Script Generator                     ║
║                                          Your Creative Comic Script Companion                                 ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
        """

        self.console.print(header, style="bold blue")

        features = [
            ("✍️", "Generate Comic", "Create comic scripts from prompts"),
            ("💡", "Random Idea", "Get fresh, creative comic ideas"),
            ("📝", "Refactor Draft", "Improve pacing, humor, and visual structure"),
            ("🌟", "Customizable", "Flags for tone, panels, and format"),
            ("💾", "Export Script", "Save generated scripts to files"),
            ("🎨", "Rich UI", "Beautiful terminal interface")
        ]

        table = Table(show_header=False, box=ROUNDED, padding=(0, 1))
        table.add_column("Icon", style="cyan", width=3)
        table.add_column("Feature", style="bold white", width=25)
        table.add_column("Description", style="dim white", width=40)

        for icon, feature, description in features:
            table.add_row(icon, feature, description)

        self.console.print("\n")
        self.console.print(Panel(
            table,
            title="🚀 What I Can Do",
            border_style="green",
            padding=(1, 2)
        ))

        examples = [
            ("main.py generate --topic \"cat takeover\" --tone funny", "I'll create a funny comic script"),
            ("main.py random", "I'll suggest a random comic idea"),
            ("main.py refactor", "I'll help improve your comic draft"),
            ("main.py generate --topic \"space adventure\" --panels 8 --save comic.md", "I'll save your script to a file")
        ]

        example_table = Table(show_header=False, box=ROUNDED, padding=(0, 1))
        example_table.add_column("Command", style="yellow", width=60)
        example_table.add_column("→", style="dim", width=3)
        example_table.add_column("Action", style="dim white", width=40)

        for cmd, action in examples:
            example_table.add_row(cmd, "→", action)

        self.console.print("\n")
        self.console.print(Panel(
            example_table,
            title="💡 Quick Examples",
            border_style="yellow",
            padding=(1, 2)
        ))

        self.console.print("\n")
        self.console.print(Panel(
            "[bold green]Type 'python main.py --help' for more options. Let's get started! 🚀[/bold green]",
            box=HEAVY,
            border_style="green"
        ))

    def print_header(self, message: str) -> None:
        """Print a header message"""
        self.console.print(Panel(
            Text(message, justify="left", style="bold blue"),
            padding=(0, 2),
            border_style="blue",
            title_align="left"
        ))

    def print_success(self, message: str) -> None:
        """Print a success message"""
        self.console.print(Panel(f"[green]✅ {message}[/green]", border_style="green"))

    def print_warning(self, message: str) -> None:
        """Print a warning message"""
        self.console.print(Panel(f"[yellow]⚠️  {message}[/yellow]", border_style="yellow"))

    def print_error(self, message: str) -> None:
        """Print an error message"""
        self.console.print(Panel(f"[red]❌ {message}[/red]", border_style="red"))

    def print_info(self, message: str) -> None:
        """Print an info message"""
        self.console.print(Panel(f"[blue]ℹ️  {message}[/blue]", border_style="blue"))

    def print_markdown(self, content: str, title: str = "Output") -> None:
        """Print markdown content"""
        self.console.print(Panel(Markdown(content), title=title, border_style="dim"))

    def print_comic_script(self, content: str, title: str = "Generated Comic Script", format: str = "markdown") -> None:
        """Print comic script content, optionally with syntax highlighting for markdown"""
        if not content:
            return
        if format == "markdown":
            self.console.print(Panel(Markdown(content), title=title, border_style="magenta", highlight=True))
        else:
            self.console.print(Panel(content, title=title, border_style="magenta", highlight=True))

    def copy_to_clipboard(self, text: str) -> None:
        """Copies text to the clipboard."""
        try:
            pyperclip.copy(text)
            self.print_success("Content copied to clipboard!")
        except pyperclip.PyperclipException as e:
            self.print_error(f"Failed to copy to clipboard: {e}. Please ensure you have xclip or xsel installed for Linux.")

    def get_user_input(self, prompt_message: str, default: str = "") -> str:
        """Get user input with a prompt"""
        return Prompt.ask(f"[bold green]{prompt_message}[/bold green]", default=default)

    def confirm_action(self, message: str) -> bool:
        """Ask for confirmation"""
        return Confirm.ask(message, default=False)

    def show_main_menu(self) -> str:
        """Show main menu with options"""
        menu_options = [
            ("1", "Generate Comic from Prompt", "Create a new comic script based on your ideas."),
            ("2", "Suggest a Random Comic Idea", "Get a fresh, creative comic concept."),
            ("3", "Refactor My Comic Draft", "Improve an existing comic draft for pacing, humor, or structure."),
            ("4", "View Help", "Show detailed command and flag information."), # Added Help option
            ("0", "Exit", "Exit the AIComicWriter application.")
        ]

        self.console.print("\n[bold cyan]📋 Main Menu[/bold cyan]")

        table = Table(show_header=True, box=ROUNDED, padding=(0, 1))
        table.add_column("Key", style="cyan", width=3)
        table.add_column("Option", style="bold white", width=35)
        table.add_column("Description", style="dim white", width=50)

        for key, option, desc in menu_options:
            table.add_row(key, option, desc)

        self.console.print(table)

        choice = self.get_user_input(
            "[bold]Select an option (0-4) or type 'exit' to quit", # Updated range
            default=""
        )
        return choice

    def print_help(self) -> None:
        """Print help information"""
        help_text = """
# AIComicWriter Help

## Commands
- **Generate Comic**: `python main.py generate --topic "<topic>" --characters "<chars>" --tone <tone> --panels <num> [--save <filename>]`
- **Suggest Random Idea**: `python main.py random [--save <filename>]`
- **Refactor Draft**: `python main.py refactor [--save <filename>]`

## Flags
- `--tone <funny|dramatic|dark|action|sci-fi|fantasy>`: Specify the tone (default: `funny`).
- `--panels <number>`: Set the number of panels (default: `6`).
- `--format <markdown|text>`: Choose output format (default: `markdown`).
- `--save <filename.md/.txt>`: Export the comic script to a file.

## Examples
```bash
# Generate a funny comic about a cat taking over the world
python main.py generate --topic "A cat that wants to take over the world" --characters "Mr. Whiskers, Dave" --tone funny --panels 6

# Get a random comic idea
python main.py random --save my_idea.md

# Refactor a comic draft (you will be prompted to paste the draft)
python main.py refactor
```
        """

        self.console.print(Panel(
            Markdown(help_text),
            title="Help",
            border_style="green"
        ))
