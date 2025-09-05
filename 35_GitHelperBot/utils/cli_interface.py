"""
CLI interface utilities for rich terminal output
"""

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
        """Print enhanced welcome message"""
        # Create a beautiful header
        header = """
╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                    🤖 GitHelperBot - AI-Powered Git Assistant                              ║
║                                           Your Intelligent Git Companion                                    ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
        """
        
        self.console.print(header, style="bold blue")
        
        # Create feature cards
        features = [
            ("✅", "Typo Correction", "Fix common Git command typos"),
            ("🧠", "AI Explanations", "Get detailed command explanations"),
            ("⚡", "Safe Execution", "Execute commands with safety checks"),
            ("📄", "File Generation", "Create .gitignore and README files"),
            ("🔍", "Natural Language", "Ask questions in plain English"),
            ("🛡️", "Safety First", "Block dangerous commands")
        ]
        
        # Create a table for features
        table = Table(show_header=False, box=ROUNDED, padding=(0, 1))
        table.add_column("Icon", style="cyan", width=3)
        table.add_column("Feature", style="bold white", width=20)
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
        
        # Quick examples
        examples = [
            ("git cmomit -m \"message\"", "I'll suggest the correct spelling"),
            ("how to squash commits?", "I'll explain the process step-by-step"),
            ("git status", "I'll explain and ask if you want to execute"),
            ("generate gitignore", "I'll create a .gitignore file for you")
        ]
        
        example_table = Table(show_header=False, box=ROUNDED, padding=(0, 1))
        example_table.add_column("Command", style="yellow", width=30)
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
        
        # Quick start info
        self.console.print("\n")
        self.console.print(Panel(
            "[bold green]Type 'exit' or 'quit' to leave. Let's get started! 🚀[/bold green]",
            box=HEAVY,
            border_style="green"
        ))
    
    def print_header(self, message: str) -> None:
        """Print a header message"""
        self.console.print(f"\n[bold blue]{message}[/bold blue]")
        self.console.print("─" * len(message))
    
    def print_success(self, message: str) -> None:
        """Print a success message"""
        self.console.print(f"[green]✅ {message}[/green]")
    
    def print_warning(self, message: str) -> None:
        """Print a warning message"""
        self.console.print(f"[yellow]⚠️  {message}[/yellow]")
    
    def print_error(self, message: str) -> None:
        """Print an error message"""
        self.console.print(f"[red]❌ {message}[/red]")
    
    def print_info(self, message: str) -> None:
        """Print an info message"""
        self.console.print(f"[blue]ℹ️  {message}[/blue]")
    
    def print_markdown(self, content: str) -> None:
        """Print markdown content"""
        self.console.print(Markdown(content))
    
    def print_output(self, output: str) -> None:
        """Print command output with syntax highlighting"""
        if not output:
            return
        
        # Try to detect if it's Git output and apply appropriate syntax
        if any(keyword in output.lower() for keyword in ['commit', 'branch', 'diff', 'status']):
            syntax = Syntax(output, "bash", theme="monokai", line_numbers=False)
        else:
            syntax = Syntax(output, "text", theme="monokai", line_numbers=False)
        
        self.console.print(syntax)
    
    def get_user_input(self, prompt: str, default: str = "") -> str:
        """Get user input with a prompt"""
        return Prompt.ask(prompt, default=default)
    
    def get_user_choice(self, prompt: str, choices: List[str]) -> str:
        """Get user choice from a list of options"""
        while True:
            choice = Prompt.ask(prompt, default="n").lower()
            if choice in choices:
                return choice
            self.print_error(f"Invalid choice. Please choose from: {', '.join(choices)}")
    
    def show_suggestion_menu(self, suggestions: List[str], title: str = "Suggestions") -> Optional[str]:
        """Show an interactive suggestion menu"""
        if not suggestions:
            return None
        
        self.console.print(f"\n[bold cyan]📋 {title}[/bold cyan]")
        
        # Create a table for suggestions
        table = Table(show_header=True, box=ROUNDED, padding=(0, 1))
        table.add_column("#", style="cyan", width=3)
        table.add_column("Command", style="yellow", width=50)
        table.add_column("Action", style="dim white", width=20)
        
        for i, suggestion in enumerate(suggestions, 1):
            action = "Execute" if suggestion.startswith("git ") else "Use"
            table.add_row(str(i), suggestion, action)
        
        self.console.print(table)
        
        # Get user selection
        while True:
            try:
                choice = IntPrompt.ask(
                    f"\n[bold]Select a command (1-{len(suggestions)}) or press Enter to cancel",
                    default=0
                )
                
                if choice == 0:
                    return None
                elif 1 <= choice <= len(suggestions):
                    return suggestions[choice - 1]
                else:
                    self.print_error(f"Please enter a number between 1 and {len(suggestions)}")
            except KeyboardInterrupt:
                return None
            except Exception:
                self.print_error("Invalid input. Please enter a number.")
    
    def show_quick_actions(self) -> Optional[str]:
        """Show quick action menu"""
        actions = [
            ("1", "git status", "Check repository status"),
            ("2", "git add .", "Stage all changes"),
            ("3", "git commit -m \"message\"", "Commit changes"),
            ("4", "git push origin main", "Push to remote"),
            ("5", "git pull origin main", "Pull from remote"),
            ("6", "git branch", "List branches"),
            ("7", "git log --oneline -5", "Show recent commits"),
            ("8", "generate gitignore", "Create .gitignore file"),
            ("9", "generate readme", "Create README.md file"),
            ("h", "history", "Show command history"),
            ("f", "favorites", "Show favorite commands"),
            ("0", "help", "Show help information")
        ]
        
        self.console.print("\n[bold cyan]⚡ Quick Actions[/bold cyan]")
        
        table = Table(show_header=True, box=ROUNDED, padding=(0, 1))
        table.add_column("Key", style="cyan", width=3)
        table.add_column("Command", style="yellow", width=40)
        table.add_column("Description", style="dim white", width=30)
        
        for key, cmd, desc in actions:
            table.add_row(key, cmd, desc)
        
        self.console.print(table)
        
        choice = Prompt.ask(
            "\n[bold]Press a key for quick action or type a command",
            default=""
        )
        
        # Handle quick action selection
        if choice.isdigit() and 0 <= int(choice) <= 9:
            selected_action = actions[int(choice)]
            if selected_action[1] == "help":
                self.print_help()
                return None
            else:
                return selected_action[1]
        elif choice.lower() == "h":
            return "history"
        elif choice.lower() == "f":
            return "favorites"
        
        return choice if choice else None
    
    def confirm_action(self, message: str) -> bool:
        """Ask for confirmation"""
        return Confirm.ask(message, default=False)
    
    def print_command_suggestions(self, command: str, suggestions: List[str]) -> None:
        """Print command suggestions"""
        self.print_warning(f"Did you mean one of these?")
        
        for i, suggestion in enumerate(suggestions, 1):
            self.console.print(f"  {i}. [cyan]{suggestion}[/cyan]")
        
        self.console.print()
    
    def print_dangerous_command_warning(self, command: str) -> None:
        """Print warning for dangerous commands"""
        warning_text = f"""
[bold red]⚠️  DANGEROUS COMMAND DETECTED ⚠️[/bold red]

Command: [yellow]{command}[/yellow]

This command can cause data loss or irreversible changes.
Please make sure you understand what this command does before proceeding.

[bold]Are you absolutely sure you want to execute this?[/bold]
        """
        
        self.console.print(Panel(
            warning_text,
            title="Safety Warning",
            border_style="red"
        ))
    
    def print_help(self) -> None:
        """Print help information"""
        help_text = """
# GitHelperBot Help

## Commands
- **Git commands**: Type any Git command (e.g., `git status`)
- **Natural language**: Ask questions (e.g., "how to merge branches?")
- **Generate files**: `generate gitignore` or `generate readme`
- **Exit**: `exit`, `quit`, or `q`

## Examples
```bash
# Correct typos
git cmomit -m "message"

# Get explanations
git rebase -i HEAD~3

# Ask questions
how to create a new branch?

# Generate files
generate gitignore
```

## Safety Features
- Commands are validated before execution
- Dangerous commands require extra confirmation
- All commands can be cancelled
- Safe execution with timeouts
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
**GitHelperBot v1.0.0**
- Python: {sys.version.split()[0]}
- Platform: {platform.system()} {platform.release()}
- Terminal: {sys.stdout.encoding}
        """
        
        self.console.print(Panel(
            info_text,
            title="Version Info",
            border_style="blue"
        ))
    
    def show_command_history(self, history_data: List[Dict[str, Any]], limit: int = 10) -> Optional[str]:
        """Show command history with selection"""
        if not history_data:
            self.print_info("No command history found.")
            return None
        
        self.console.print(f"\n[bold cyan]📜 Command History (Last {min(limit, len(history_data))} commands)[/bold cyan]")
        
        table = Table(show_header=True, box=ROUNDED, padding=(0, 1))
        table.add_column("#", style="cyan", width=3)
        table.add_column("Command", style="yellow", width=50)
        table.add_column("Status", style="white", width=10)
        table.add_column("Time", style="dim white", width=15)
        
        for i, entry in enumerate(history_data[:limit], 1):
            status = "✅" if entry.get("success", False) else "❌"
            timestamp = entry.get("timestamp", "")
            if timestamp:
                from datetime import datetime
                try:
                    dt = datetime.fromisoformat(timestamp)
                    time_str = dt.strftime("%H:%M:%S")
                except:
                    time_str = timestamp[:8]
            else:
                time_str = "Unknown"
            
            table.add_row(str(i), entry["command"], status, time_str)
        
        self.console.print(table)
        
        # Get user selection
        while True:
            try:
                choice = IntPrompt.ask(
                    f"\n[bold]Select a command (1-{min(limit, len(history_data))}) or press Enter to cancel",
                    default=0
                )
                
                if choice == 0:
                    return None
                elif 1 <= choice <= min(limit, len(history_data)):
                    return history_data[choice - 1]["command"]
                else:
                    self.print_error(f"Please enter a number between 1 and {min(limit, len(history_data))}")
            except KeyboardInterrupt:
                return None
            except Exception:
                self.print_error("Invalid input. Please enter a number.")
    
    def show_favorites(self, favorites: List[Dict[str, Any]]) -> Optional[str]:
        """Show favorite commands with selection"""
        if not favorites:
            self.print_info("No favorite commands found.")
            return None
        
        self.console.print(f"\n[bold cyan]⭐ Favorite Commands ({len(favorites)} commands)[/bold cyan]")
        
        table = Table(show_header=True, box=ROUNDED, padding=(0, 1))
        table.add_column("#", style="cyan", width=3)
        table.add_column("Command", style="yellow", width=50)
        table.add_column("Status", style="white", width=10)
        table.add_column("Usage", style="dim white", width=10)
        
        for i, entry in enumerate(favorites, 1):
            status = "✅" if entry.get("success", False) else "❌"
            usage_count = entry.get("usage_count", 1)
            
            table.add_row(str(i), entry["command"], status, str(usage_count))
        
        self.console.print(table)
        
        # Get user selection
        while True:
            try:
                choice = IntPrompt.ask(
                    f"\n[bold]Select a command (1-{len(favorites)}) or press Enter to cancel",
                    default=0
                )
                
                if choice == 0:
                    return None
                elif 1 <= choice <= len(favorites):
                    return favorites[choice - 1]["command"]
                else:
                    self.print_error(f"Please enter a number between 1 and {len(favorites)}")
            except KeyboardInterrupt:
                return None
            except Exception:
                self.print_error("Invalid input. Please enter a number.")
    
    def show_command_stats(self, stats: Dict[str, Any]) -> None:
        """Show command usage statistics"""
        self.console.print("\n[bold cyan]📊 Command Statistics[/bold cyan]")
        
        stats_table = Table(show_header=False, box=ROUNDED, padding=(0, 1))
        stats_table.add_column("Metric", style="bold white", width=20)
        stats_table.add_column("Value", style="cyan", width=15)
        
        stats_table.add_row("Total Commands", str(stats.get("total", 0)))
        stats_table.add_row("Success Rate", f"{stats.get('success_rate', 0)}%")
        
        self.console.print(stats_table)
        
        if stats.get("most_used"):
            self.console.print("\n[bold]Most Used Commands:[/bold]")
            for cmd, count in stats["most_used"]:
                self.console.print(f"  {cmd}: {count} times")
