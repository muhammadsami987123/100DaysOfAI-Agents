import argparse
import sys
import os
import logging
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.text import Text
from typing import Optional

from agent import AutoUpdaterBot
from config import DEFAULT_BRANCH, LOG_LEVEL

# Configure logging
logging.basicConfig(level=LOG_LEVEL, format='%(levelname)s: %(message)s')

class CLIInterface:
    """Handles CLI interactions and displays messages using rich."""
    def __init__(self, console: Console):
        self.console = console

    def print_welcome(self) -> None:
        """Prints a welcome message for AutoUpdaterBot."""
        header = """
╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                  🔄 AutoUpdaterBot - AI-Powered GitHub Updater                                ║
║                                      Your Intelligent Local Repository Synchronization Companion                 ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
        """
        self.console.print(header, style="bold blue")
        self.console.print(Panel(
            "[bold green]Welcome to AutoUpdaterBot! I help you keep your local GitHub repositories up-to-date.[/bold green]",
            border_style="green",
            padding=(1, 2)
        ))

    def get_user_input(self, prompt_message: str, default: Optional[str] = None) -> str:
        """Gets user input with a rich prompt."""
        return Prompt.ask(f"[bold yellow]{prompt_message}[/bold yellow]", default=default or "")

    def confirm_action(self, message: str, default: bool = False) -> bool:
        """Asks for user confirmation with a rich prompt."""
        return Confirm.ask(f"[bold cyan]{message}[/bold cyan]", default=default)

    def show_help(self) -> None:
        """Displays help information."""
        self.console.print(Panel(
            Text("AutoUpdaterBot Help", justify="center", style="bold blue"),
            border_style="blue"
        ))
        self.console.print("""
[bold]Usage:[/bold] python cli.py [OPTIONS]

[bold underline]Options:[/bold underline] 
  --repo <url>         GitHub repository URL
  --local-path <path>  Local directory path
  --branch <name>      Optional: Branch name (default: main)
  --rebuild            Optional: Run rebuild script (rebuild.sh/rebuild.bat)
  --run-tests          Optional: Run tests script (run_tests.sh/run_tests.bat)
  --summary-only       Optional: Show changes summary without performing actual pull/update
  --auto-commit        Optional: Automatically commit local changes before pulling
  --help               Show this help message

[bold underline]Interactive Mode:[/bold underline]
Run without arguments: `python cli.py` to be prompted for inputs.
        """
        )

def main() -> int:
    console = Console()
    cli_interface = CLIInterface(console)
    updater_bot = AutoUpdaterBot(console)

    parser = argparse.ArgumentParser(description="AutoUpdaterBot - CLI for updating GitHub repositories.")
    parser.add_argument('--repo', type=str, help='GitHub repository URL (e.g., https://github.com/user/repo)')
    parser.add_argument('--local-path', type=str, help='Local directory where the repo is or will be cloned')
    parser.add_argument('--branch', type=str, default=DEFAULT_BRANCH, help=f'Branch name (default: {DEFAULT_BRANCH})')
    parser.add_argument('--rebuild', action='store_true', help='Execute rebuild.sh/rebuild.bat after update')
    parser.add_argument('--run-tests', action='store_true', help='Execute run_tests.sh/run_tests.bat after update')
    parser.add_argument('--summary-only', action='store_true', help='Show changes summary without actual pull/update')
    parser.add_argument('--auto-commit', action='store_true', help='Automatically commit local changes before pulling')
    # Removed --help/-h as argparse provides it by default

    args = parser.parse_args()

    if len(sys.argv) == 1: # No arguments provided, enter interactive mode
        cli_interface.print_welcome()
        repo_url = cli_interface.get_user_input("Enter GitHub repository URL:")
        local_path = cli_interface.get_user_input("Enter target local folder:")
        branch = cli_interface.get_user_input(f"Enter branch name (default: {DEFAULT_BRANCH}):", default=DEFAULT_BRANCH)
        rebuild = cli_interface.confirm_action("Run rebuild script after update?")
        run_tests = cli_interface.confirm_action("Run tests after update?")
        summary_only = cli_interface.confirm_action("Show summary only (no actual pull/update)?")
        auto_commit = cli_interface.confirm_action("Automatically commit local changes before pulling?")

        if not repo_url or not local_path:
            cli_interface.console.print("[red]Error: Repository URL and local path are required.[/red]")
            return 1

    else: # Arguments provided, run in non-interactive mode
        if not args.repo or not args.local_path:
            parser.print_help()
            return 1
        repo_url = args.repo
        local_path = args.local_path
        branch = args.branch
        rebuild = args.rebuild
        run_tests = args.run_tests
        summary_only = args.summary_only
        auto_commit = args.auto_commit

    try:
        updater_bot.update_repository(repo_url, local_path, branch, rebuild, run_tests, summary_only, auto_commit)
    except Exception as e:
        cli_interface.console.print(f"[red]An unexpected error occurred:[/red] {e}")
        logging.error(f"Unexpected error in main: {e}", exc_info=True)
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
