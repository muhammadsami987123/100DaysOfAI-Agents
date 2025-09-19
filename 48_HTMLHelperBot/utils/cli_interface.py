import sys
from typing import List, Optional, Dict, Any
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.text import Text
from rich.syntax import Syntax
from rich.table import Table
from rich.columns import Columns
from rich.align import Align
from rich.box import ROUNDED, DOUBLE, HEAVY
from rich import print as rprint

class CLIInterface:
    """Handles CLI interface and rich output formatting"""

    def __init__(self):
        self.console = Console()

    def print_welcome(self) -> None:
        """Print enhanced welcome message for HTMLHelperBot"""
        header = """
╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                   🌐 HTMLHelperBot - AI-Powered HTML Assistant                              ║
║                                           Your Intelligent HTML Companion                                   ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
        """

        self.console.print(header, style="bold blue")

        features = [
            ("🧠", "AI HTML Generation", "Create HTML from descriptions"),
            ("🔍", "HTML Explanation", "Understand existing HTML code"),
            ("⚡", "Optimized Output", "Generate clean, semantic, accessible HTML"),
            ("📄", "File Saving", "Save generated HTML to .html files"),
            ("🎨", "Rich UI", "Beautiful terminal interface"),
            ("🌐", "Accessibility & SEO", "Adhere to best practices")
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
            ("generate \"responsive pricing table\"", "I'll create the HTML for you"),
            ("explain \"<p>Hello</p>\"", "I'll break down the tag's purpose and usage"),
            ("generate \"simple page\" --save index.html", "I'll save the HTML to a file")
        ]

        example_table = Table(show_header=False, box=ROUNDED, padding=(0, 1))
        example_table.add_column("Command", style="yellow", width=40)
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
            "[bold green]Type 'exit' or 'quit' to leave. Let's get started! 🚀[/bold green]",
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

    def print_markdown(self, content: str) -> None:
        """Print markdown content"""
        self.console.print(Panel(Markdown(content), title="Details", border_style="dim"))

    def print_html_output(self, output: str) -> None:
        """Print HTML content with syntax highlighting"""
        if not output:
            return
        syntax = Syntax(output, "html", theme="monokai", line_numbers=True, word_wrap=True)
        self.console.print(Panel(syntax, title="Generated HTML", border_style="magenta", highlight=True))

    def copy_to_clipboard(self, text: str) -> None:
        """Copies text to the clipboard."""
        try:
            import pyperclip
            pyperclip.copy(text)
            self.print_success("Content copied to clipboard!")
        except pyperclip.PyperclipException as e:
            self.print_error(f"Failed to copy to clipboard: {e}. Please install xclip or xsel for Linux.")

    def get_user_input(self, prompt: str, default: str = "") -> str:
        """Get user input with a prompt"""
        return self.console.input(f"\n[bold green]{prompt} [/bold green][dim]({default})[/dim]: ") or default

    def get_user_choice(self, prompt: str, choices: List[str]) -> str:
        """Get user choice from a list of options"""
        while True:
            choice = Prompt.ask(prompt, default="n").lower()
            if choice in choices:
                return choice
            self.print_error(f"Invalid choice. Please choose from: {', '.join(choices)}")

    def show_main_menu(self) -> str:
        """Show main menu with options"""
        menu_options = [
            ("1", "Generate HTML", "Create HTML from a description"),
            ("2", "Explain HTML", "Understand existing HTML code"),
            ("3", "Save Output", "Save generated HTML to a file (after generation)"),
            ("4", "Chat with Bot", "Engage in a conversation about HTML"),
            ("5", "Help", "Show help information"),
            ("0", "Exit", "Leave the application")
        ]

        self.console.print("\n[bold cyan]📋 Main Menu[/bold cyan]")

        table = Table(show_header=True, box=ROUNDED, padding=(0, 1))
        table.add_column("Key", style="cyan", width=3)
        table.add_column("Option", style="bold white", width=30)
        table.add_column("Description", style="dim white", width=40)

        for key, option, desc in menu_options:
            table.add_row(key, option, desc)

        self.console.print(table)

        choice = self.get_user_input(
            "\n[bold]Select an option (0-5) or type a command",
            default=""
        )
        return choice

    def confirm_action(self, message: str) -> bool:
        """Ask for confirmation"""
        return Confirm.ask(message, default=False)

    def print_help(self) -> None:
        """Print help information"""
        help_text = """
# HTMLHelperBot Help

## Commands
- **Generate HTML**: `generate <description>` (e.g., `generate "a responsive header"`)
- **Explain HTML**: `explain <html_code>` (e.g., `explain "<div>"`)
- **Save output**: Add `--save <filename.html>` to `generate` command
- **Specify HTML version**: Add `--version html5` (default)
- **Minimal markup**: Add `--minimal` for concise HTML
- **Exit**: `exit`, `quit`, or `q`

## Examples
```bash
# Generate a simple form
python main.py --generate "a login form with username and password fields"

# Explain a specific tag
python main.py --explain "<article>"

# Generate and save HTML
python main.py --generate "a hero section" --save hero.html
```

## Safety Features
- Output is validated for basic HTML structure (future)
- Saving files requires user confirmation
- API calls have timeouts
- Clear error messages
        """

        self.console.print(Panel(
            Markdown(help_text),
            title="Help",
            border_style="green"
        ))

    def print_version_info(self) -> None:
        """Print version and system information"""
        import platform
        import sys

        info_text = f"""
**HTMLHelperBot v1.0.0**
- Python: {sys.version.split()[0]}
- Platform: {platform.system()} {platform.release()}
- Terminal: {sys.stdout.encoding}
        """

        self.console.print(Panel(
            info_text,
            title="Version Info",
            border_style="blue"
        ))
