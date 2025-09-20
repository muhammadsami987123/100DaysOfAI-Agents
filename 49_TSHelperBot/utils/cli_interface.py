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
        """Print enhanced welcome message for TSHelperBot"""
        header = """
╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                   🌐 TSHelperBot - AI-Powered JS/TS Assistant                              ║
║                                           Your Intelligent JavaScript/TypeScript Companion                    ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
        """

        self.console.print(header, style="bold blue")

        features = [
            ("🧠", "AI Code Generation", "Create JS/TS code from descriptions"),
            ("🔍", "Code Explanation", "Understand existing JS/TS code"),
            ("♻️", "Code Refactoring", "Optimize and clean up JS/TS code"),
            ("↔️", "Code Conversion", "Convert between JS and TS"),
            ("🐞", "Code Debugging", "Identify and fix errors in JS/TS"),
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
            ("generate \"a function to validate an email\"", "I'll create the JS/TS code for you"),
            ("explain \"function greet() { console.log(\\\"Hello!\\\"); }\"", "I'll break down the code's purpose"),
            ("refactor \"const add = (a, b) => { return a + b; }\"", "I'll suggest improvements"),
            ("convert \"const x: number = 5;\" --to js", "I'll convert it to JavaScript"),
            ("debug \"function sum(a, b) { return a  b; }\"", "I'll find and fix the error"),
            ("generate \"responsive header\" --save header.ts", "I'll save the TS to a file")
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

    def print_code_output(self, output: str, language: str = "ts") -> None:
        """Print code content with syntax highlighting"""
        if not output:
            return
        syntax = Syntax(output, language, theme="monokai", line_numbers=True, word_wrap=True)
        self.console.print(Panel(syntax, title=f"Generated {language.upper()} Code", border_style="magenta", highlight=True))

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
            ("1", "Generate Code", "Create JS/TS code from a description"),
            ("2", "Explain Code", "Understand existing JS/TS code"),
            ("3", "Refactor Code", "Optimize and clean up JS/TS code"),
            ("4", "Convert JS ↔ TS", "Convert code between JavaScript and TypeScript"),
            ("5", "Debug Code", "Identify and fix errors in JS/TS code"),
            ("6", "Save Output", "Save generated code to a file (after generation)"),
            ("7", "Help", "Show help information"),
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
            "\n[bold]Select an option (0-7) or type a command",
            default=""
        )
        return choice

    def confirm_action(self, message: str) -> bool:
        """Ask for confirmation"""
        return Confirm.ask(message, default=False)

    def print_help(self) -> None:
        """Print help information"""
        help_text = """
# TSHelperBot Help

## Commands
- **Generate Code**: `generate <description>` (e.g., `generate \"a function to validate an email\"`)
- **Explain Code**: `explain <code_snippet>` (e.g., `explain \"const x = 5;\"`)
- **Refactor Code**: `refactor <code_snippet>` (e.g., `refactor \"function add(a,b){return a+b}\"`)
- **Convert Code**: `convert <code_snippet> --to <js|ts>` (e.g., `convert \"let x = 5;\" --to ts`)
- **Debug Code**: `debug <code_snippet>` (e.g., `debug \"function sum(a, b) { return a  b; }\"`)
- **Specify Language**: Add `--lang <js|ts>` (default is 'ts' for generate, detected for explain/refactor/debug)
- **Save output**: Add `--save <filename.js|ts>` to `generate` or other commands
- **Minimal markup**: Add `--minimal` for concise code/explanations
- **Exit**: `exit`, `quit`, or `q`

## Examples
```bash
# Generate a simple function in TypeScript
python agent.py --generate \"a function to fetch data from an API\" --lang ts

# Explain a JavaScript snippet
python agent.py --explain \"const add = (x, y) => x + y;\" --lang js

# Refactor a TypeScript class
python agent.py --refactor \"class MyClass { constructor(name) { this.name = name; } }\" --lang ts

# Convert JS to TS and save
python agent.py --convert \"function multiply(a, b) { return a * b; }\" --to ts --save multiply.ts

# Debug a JS function with a simulated error
python agent.py --debug \"function divide(a, b) { return a / c; }\" --error \"ReferenceError: c is not defined\" --lang js

# Generate and save minimal JS
python agent.py --generate \"a simple counter component\" --lang js --minimal --save counter.js
```

## Safety Features
- Output is validated for basic code structure (future)
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
**TSHelperBot v1.0.0**
- Python: {sys.version.split()[0]}
- Platform: {platform.system()} {platform.release()}
- Terminal: {sys.stdout.encoding}
        """

        self.console.print(Panel(
            info_text,
            title="Version Info",
            border_style="blue"
        ))
