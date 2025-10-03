import os
import subprocess
from typing import List, Tuple, Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax

from github_service import GitHubService
from config import DEFAULT_BRANCH

class AutoUpdaterBot:
    """Main AutoUpdaterBot class for managing repository updates."""

    def __init__(self, console: Console):
        self.console = console
        self.github_service = GitHubService(console)

    def _run_script(self, local_path: str, script_name: str) -> Tuple[bool, str]:
        """Helper to run a shell script (e.g., rebuild or test)."""
        script_path_sh = os.path.join(local_path, f"{script_name}.sh")
        script_path_bat = os.path.join(local_path, f"{script_name}.bat")

        if os.path.exists(script_path_sh):
            self.console.print(f"[blue]Executing {script_name}.sh...[/blue]")
            command = ["bash", script_path_sh]
        elif os.path.exists(script_path_bat):
            self.console.print(f"[blue]Executing {script_name}.bat...[/blue]")
            command = [script_path_bat]
        else:
            return False, f"No {script_name}.sh or {script_name}.bat found in {local_path}"

        try:
            result = subprocess.run(command, cwd=local_path, capture_output=True, text=True, check=True)
            self.console.print(Panel(Syntax(result.stdout, "bash", theme="monokai", line_numbers=True), title=f"[green]{script_name.capitalize()} Output[/green]"))
            if result.stderr:
                self.console.print(Panel(Syntax(result.stderr, "bash", theme="monokai", line_numbers=True), title=f"[yellow]{script_name.capitalize()} Warnings/Errors[/yellow]", border_style="yellow"))
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            self.console.print(Panel(Syntax(e.stdout + e.stderr, "bash", theme="monokai", line_numbers=True), title=f"[red]{script_name.capitalize()} Failed[/red]", border_style="red"))
            return False, f"{script_name.capitalize()} failed: {e}"
        except Exception as e:
            return False, f"An unexpected error occurred during {script_name}: {e}"

    def update_repository(self, repo_url: str, local_path: str, branch: str = DEFAULT_BRANCH, 
                          rebuild: bool = False, run_tests: bool = False, summary_only: bool = False, 
                          auto_commit: bool = False) -> None:
        """Orchestrates the update process for a GitHub repository."""
        self.console.print(Panel(
            Text("🔄 Starting AutoUpdaterBot Process", justify="center", style="bold magenta"),
            border_style="magenta"
        ))

        # Step 1: Check if local repository exists and is valid
        is_repo_initialized = self.github_service.is_local_repo_initialized(local_path)
        local_repo_exists = self.github_service.check_local_repo_exists(local_path)

        if local_repo_exists and not is_repo_initialized:
            self.console.print(f"[red]Error:[/red] The directory '{local_path}' exists but is not a Git repository. Please remove it or provide a different path.")
            return
        
        if is_repo_initialized:
            status_ok, status_message = self.github_service.has_uncommitted_changes(local_path)
            if status_ok:
                if auto_commit:
                    self.console.print("[blue]Auto-commit enabled. Attempting to commit local changes...[/blue]")
                    commit_success, commit_msg = self.github_service.auto_commit_changes(local_path)
                    if not commit_success:
                        self.console.print(f"[red]Auto-commit failed:[/red] {commit_msg}")
                        return
                    self.console.print(f"[green]{commit_msg}[/green]")
                else:
                    self.console.print(f"[red]Error:[/red] {status_message} Please commit or stash your changes before updating, or enable --auto-commit.")
                    return

            # Step 2: Get remote and local commit info for comparison
            local_head_hash, _ = self.github_service.get_latest_commit_info(local_path)
            remote_head_hash, _ = self.github_service.get_remote_head_commit_info(repo_url, branch)

            if local_head_hash == remote_head_hash:
                self.console.print("[green]Local repository is already up to date with remote.[/green]")
                # Still show summary if requested, even if no new commits
                if summary_only:
                    self._display_summary([], [], "Repository already up to date.")
                return
            
            if summary_only:
                self.console.print("[yellow]Summary Only Mode: Checking for updates without pulling.[/yellow]")
                self._display_summary([], [], f"Potential updates available on branch '{branch}'.")
                return
            
            # Step 3: Pull changes
            success, message, changed_files, commit_messages = self.github_service.pull_repository(local_path, branch)
            if not success:
                self.console.print(f"[red]Update failed:[/red] {message}")
                return
            self._display_summary(changed_files, commit_messages, message)

        else: # Local repository does not exist, so clone it
            if summary_only:
                self.console.print("[yellow]Summary Only Mode: No local repository found. Would clone if not in summary-only mode.[/yellow]")
                return

            self.console.print(f"[blue]Local path '{local_path}' does not exist or is not a repository. Attempting to clone...[/blue]")
            success, message = self.github_service.clone_repository(repo_url, local_path, branch)
            if not success:
                self.console.print(f"[red]Cloning failed:[/red] {message}")
                return
            self._display_summary([], [], message)

        # Step 4: Optional Post-Update Actions
        if rebuild:
            self.console.print("\n" + "="*40)
            self.console.print(Text("📦 Starting Rebuild Process", justify="center", style="bold cyan"))
            self.console.print("="*40)
            rebuild_success, rebuild_output = self._run_script(local_path, "rebuild")
            if not rebuild_success:
                self.console.print(f"[red]Rebuild failed![/red]")

        if run_tests:
            self.console.print("\n" + "="*40)
            self.console.print(Text("🧪 Starting Test Execution", justify="center", style="bold green"))
            self.console.print("="*40)
            test_success, test_output = self._run_script(local_path, "run_tests")
            if not test_success:
                self.console.print(f"[red]Tests failed![/red]")

        self.console.print(Panel(
            Text("✅ AutoUpdaterBot Process Complete", justify="center", style="bold green"),
            border_style="green"
        ))

    def _display_summary(self, changed_files: List[str], commit_messages: List[str], status_message: str) -> None:
        """Displays a formatted summary of the update."""
        self.console.print(Panel(
            Text("📊 Update Summary", justify="center", style="bold blue"),
            border_style="blue"
        ))
        self.console.print(f"[bold]Status:[/bold] {status_message}")

        if changed_files:
            self.console.print("\n[bold underline]Files Updated:[/bold underline]")
            for file in changed_files:
                self.console.print(f" - [yellow]{file}[/yellow]")
        else:
            self.console.print("\n[dim]No files updated in this operation.[/dim]")

        if commit_messages:
            self.console.print("\n[bold underline]Commit Messages Pulled:[/bold underline]")
            for message in commit_messages:
                self.console.print(f" - [cyan]{message}[/cyan]")
        else:
            self.console.print("\n[dim]No new commit messages pulled.[/dim]")
