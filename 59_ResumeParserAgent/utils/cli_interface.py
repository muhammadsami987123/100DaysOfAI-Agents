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
import json

class CLIInterface:
    """Handles CLI interface and rich output formatting"""

    def __init__(self):
        self.console = Console()

    def print_welcome(self) -> None:
        """Print enhanced welcome message for ResumeParserAgent"""
        header = """
╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                   📄 ResumeParserAgent - AI HR Assistant                                    ║
║                                      Your Intelligent Resume Companion                                     ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
        """

        self.console.print(header, style="bold blue")

        features = [
            ("🧠", "AI Resume Parsing", "Extract structured information"),
            ("🔍", "Multi-format Support", "PDF, DOCX, and TXT files"),
            ("✅", "Structured JSON Output", "Clean JSON with labeled fields"),
            ("📝", "Resume Summaries", "3-5 line summaries"),
            ("💡", "Skills Extraction", "Technical and soft skills"),
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
            ("file my_resume.pdf", "I'll parse your PDF resume"),
            ("text 'John Doe...'", "I'll process your pasted resume text"),
            ("python main.py --summary", "I'll summarize a resume"),
            ("python main.py --skills-only", "I'll extract only skills"),
            ("python main.py --json", "I'll save parsed data to JSON"),
            ("python main.py --validate", "I'll validate key fields")
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
            "[bold green]Enter 'file <path_to_file>' or 'text <your_resume_text>'. Type 'exit' or 'quit' to leave. Let's get started! 🚀[/bold green]",
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

    def print_markdown(self, content: str, title: str = "Details") -> None:
        """Print markdown content"""
        self.console.print(Panel(Markdown(content), title=title, border_style="dim"))

    def print_json_output(self, output: Dict[str, Any], title: str = "JSON Output") -> None:
        """Print JSON content with syntax highlighting"""
        if not output:
            return
        json_string = json.dumps(output, indent=4)
        syntax = Syntax(json_string, "json", theme="monokai", line_numbers=True, word_wrap=True)
        self.console.print(Panel(syntax, title=title, border_style="magenta", highlight=True))

    def get_user_input(self, prompt: str, default: str = "") -> str:
        """Get user input with a prompt"""
        return self.console.input(f"\n[bold green]{prompt} [/bold green][dim]({default})[/dim]: ") or default

    def get_multiline_user_input(self, prompt: str, delimiter: str = "END") -> str:
        """
        Get multi-line user input until a specific delimiter is entered.
        """
        self.console.print(f"\n[bold green]{prompt} [/bold green][dim](Type '{delimiter}' on a new line to finish):[/dim]")
        lines = []
        while True:
            try:
                line = self.console.input("> ")
                if line.strip().upper() == delimiter:
                    break
                lines.append(line)
            except EOFError: # Handles Ctrl+D on Unix or Ctrl+Z on Windows
                break
            except KeyboardInterrupt:
                self.console.print("[yellow]Input cancelled.[/yellow]")
                return ""
        return "\n".join(lines)

    def confirm_action(self, message: str) -> bool:
        """Ask for confirmation"""
        return Confirm.ask(message, default=False)

    def print_help(self) -> None:
        """Print help information"""
        help_text = """
# ResumeParserAgent Help

## Commands
- **Parse File**: `file <path_to_file>` (e.g., `file my_resume.pdf`)
- **Paste Text**: `text <your_resume_text>` (e.g., `text 'John Doe...'`)
- **Summarize**: Add `--summary` to parse command
- **Skills Only**: Add `--skills-only` to parse command
- **Save to JSON**: Add `--json` to parse command
- **Validate Fields**: Add `--validate` to parse command
- **Exit**: `exit`, `quit`, or `q`

## Examples
```bash
# Parse a PDF resume and get full output
python main.py --file my_resume.pdf

# Paste resume text and get a summary
python main.py --text 'John Doe...' --summary

# Parse a DOCX, extract skills only, and save to JSON
python main.py --file my_resume.docx --skills-only --json

# Parse a TXT file and validate key fields
python main.py --file my_resume.txt --validate
```

## Safety Features
- Saving files requires user confirmation
- API calls have timeouts
- Clear error messages
        """

        self.console.print(Panel(
            Markdown(help_text),
            title="Help",
            border_style="green"
        ))
