import os
import subprocess
from typing import Tuple, List, Dict, Optional
from git import Repo, RemoteProgress, GitCommandError
from rich.console import Console

from config import GITHUB_TOKEN

class ProgressPrinter(RemoteProgress):
    """Custom progress printer for Git operations."""
    def __init__(self, console: Console):
        super().__init__()
        self.console = console

    def update(self, op_code, cur_count, max_count=None, message=''):
        percent = (cur_count / max_count) * 100 if max_count else 0
        self.console.log(f"[yellow]Git Progress:[/yellow] {message} {percent:.1f}%", justify="left")

class GitHubService:
    """Handles Git operations for cloning, pulling, and getting repository information."""

    def __init__(self, console: Console):
        self.console = console

    def _get_authenticated_repo_url(self, repo_url: str) -> str:
        """Injects GitHub token into the repository URL for authentication."""
        if GITHUB_TOKEN and "github.com" in repo_url:
            # Assumes HTTPS URL like https://github.com/owner/repo.git or https://github.com/owner/repo
            if repo_url.startswith("https://"):
                parts = repo_url.split("https://")
                return f"https://oauth2:{GITHUB_TOKEN}@" + parts[1]
        return repo_url

    def clone_repository(self, repo_url: str, local_path: str, branch: Optional[str] = None) -> Tuple[bool, str]:
        """Clones a GitHub repository to a local path."""
        auth_repo_url = self._get_authenticated_repo_url(repo_url)
        try:
            if os.path.exists(local_path) and os.listdir(local_path):
                return False, f"Error: Local path '{local_path}' already exists and is not empty." # Use this message instead of the Git error message
            self.console.print(f"[blue]Cloning repository[/blue] [cyan]{repo_url}[/cyan] into [yellow]{local_path}[/yellow]...")
            Repo.clone_from(auth_repo_url, local_path, branch=branch, progress=ProgressPrinter(self.console))
            self.console.print(f"[green]Repository cloned successfully![/green]")
            return True, "Repository cloned successfully."
        except GitCommandError as e:
            if "Authentication failed" in str(e):
                return False, "Authentication failed. Please check your GITHUB_TOKEN and repository permissions."
            if "Repository not found" in str(e):
                return False, f"Repository '{repo_url}' not found or is private. Please check the URL and permissions."
            return False, f"Git clone error: {e}"
        except Exception as e:
            return False, f"An unexpected error occurred during cloning: {e}"

    def pull_repository(self, local_path: str, branch: Optional[str] = None) -> Tuple[bool, str, List[str], List[str]]:
        """Pulls the latest changes from a remote repository."""
        try:
            repo = Repo(local_path)
            # Ensure the current branch is the one we want to pull, or check out if not
            if branch and repo.active_branch.name != branch:
                self.console.print(f"[blue]Switching to branch[/blue] [cyan]{branch}[/cyan]...")
                repo.git.checkout(branch)

            # Store current head commit hash for comparison after pull
            old_head_commit = repo.head.commit.hexsha

            self.console.print(f"[blue]Pulling latest changes for branch[/blue] [cyan]{repo.active_branch.name}[/cyan]...")
            # Force fetch all remotes before pulling
            for remote in repo.remotes:
                remote.fetch(progress=ProgressPrinter(self.console))
            
            # Pull from the correct remote and branch
            pull_info = repo.remotes.origin.pull(repo.active_branch, progress=ProgressPrinter(self.console))

            # Get new head commit hash
            new_head_commit = repo.head.commit.hexsha

            if old_head_commit == new_head_commit:
                self.console.print("[green]Repository is already up to date.[/green]")
                return True, "Repository is already up to date.", [], []

            # Check for merge conflicts
            if repo.index.diff("HEAD"): # Check if there are unmerged changes
                self.console.print("[red]Merge conflict detected! Please resolve manually.[/red]")
                return False, "Merge conflict detected!", [], []

            # Get changed files and commit messages
            changed_files = []
            commit_messages = []
            for info in pull_info:
                if info.commit:
                    commit_messages.append(info.commit.message.strip())
                    # Use diff to find changed files between old and new head
                    diff_index = repo.commit(old_head_commit).diff(info.commit)
                    for diff_obj in diff_index:
                        if diff_obj.change_type in ('A', 'M', 'D', 'R', 'C'): # Added, Modified, Deleted, Renamed, Copied
                            changed_files.append(diff_obj.a_path if diff_obj.a_path else diff_obj.b_path)

            self.console.print(f"[green]Repository updated successfully![/green]")
            return True, "Repository updated successfully.", list(set(changed_files)), list(set(commit_messages)) # Use set to avoid duplicates
        except GitCommandError as e:
            if "local changes would be overwritten" in str(e):
                return False, "Local changes detected that would be overwritten. Please commit or stash them first.", [], []
            if "merge conflict" in str(e):
                 return False, "Merge conflict detected! Please resolve manually.", [], []
            return False, f"Git pull error: {e}", [], []
        except Exception as e:
            return False, f"An unexpected error occurred during pulling: {e}", [], []

    def get_repo_status(self, local_path: str) -> Tuple[bool, str]:
        """Checks if a local path is a valid Git repository."""
        try:
            _ = Repo(local_path)
            return True, "Valid Git repository."
        except Exception:
            return False, f"'{local_path}' is not a valid Git repository."

    def get_latest_commit_info(self, local_path: str) -> Tuple[Optional[str], Optional[str]]:
        """Get the latest commit hash and message from a local repository."""
        try:
            repo = Repo(local_path)
            latest_commit = repo.head.commit
            return latest_commit.hexsha, latest_commit.message.strip()
        except Exception:
            return None, None

    def get_remote_head_commit_info(self, repo_url: str, branch: str) -> Tuple[Optional[str], Optional[str]]:
        """Get the latest commit hash and message from the remote repository's head."""
        auth_repo_url = self._get_authenticated_repo_url(repo_url)
        try:
            # Use git ls-remote to get the HEAD commit hash without cloning
            # This requires git to be installed and available in PATH
            result = subprocess.run(
                ["git", "ls-remote", auth_repo_url, branch],
                capture_output=True, text=True, check=True
            )
            lines = result.stdout.strip().split('\n')
            if lines:
                for line in lines:
                    if f"refs/heads/{branch}" in line:
                        commit_hash = line.split()[0]
                        # Getting the commit message requires cloning or deeper API interaction
                        # For now, we'll just return the hash. The pull operation will give messages.
                        return commit_hash, "(Commit message not available via ls-remote)"
            return None, None
        except subprocess.CalledProcessError as e:
            if "Authentication failed" in e.stderr or "Could not read from remote repository" in e.stderr:
                self.console.print("[red]Remote access failed:[/red] Authentication or repository access error.")
                return None, "Authentication or repository access error."
            self.console.print(f"[red]Git ls-remote error:[/red] {e.stderr}")
            return None, None
        except Exception as e:
            self.console.print(f"[red]An unexpected error occurred getting remote info:[/red] {e}")
            return None, None

    def has_uncommitted_changes(self, local_path: str) -> Tuple[bool, str]:
        """Checks if the local repository has uncommitted changes."""
        try:
            repo = Repo(local_path)
            if repo.is_dirty(untracked_files=True):
                return True, "Local repository has uncommitted changes or untracked files."
            return False, "No uncommitted changes."
        except Exception as e:
            return False, f"Error checking for uncommitted changes: {e}"

    def get_unpushed_commits(self, local_path: str, remote_name: str = 'origin', branch_name: Optional[str] = None) -> List[str]:
        """Gets a list of commit messages for commits that are in the local branch but not yet pushed to the remote."""
        try:
            repo = Repo(local_path)
            if branch_name is None:
                branch_name = repo.active_branch.name
            
            local_branch = repo.heads[branch_name]
            remote_branch = repo.remotes[remote_name].refs[branch_name]

            # Find commits that are in local_branch but not in remote_branch
            unpushed_commits = list(repo.iter_commits(f'{remote_branch}..{local_branch}'))
            return [commit.message.strip() for commit in unpushed_commits]
        except Exception as e:
            self.console.print(f"[red]Error getting unpushed commits:[/red] {e}")
            return []

    def auto_commit_changes(self, local_path: str, commit_message: str = "Auto-commit before pull") -> Tuple[bool, str]:
        """Automatically stages and commits local changes, amending previous auto-commits if applicable."""
        try:
            repo = Repo(local_path)
            if repo.is_dirty(untracked_files=True):
                self.console.print("[blue]Detecting uncommitted changes. Attempting to auto-commit...[/blue]")
                repo.git.add(".")

                # Check if the last commit is an auto-commit and if it's unpushed
                latest_commit = repo.head.commit
                
                should_amend = False
                tracking_branch = repo.active_branch.tracking_branch()

                if tracking_branch:
                    # Check if the latest local commit is an auto-commit
                    if latest_commit.message.strip() == commit_message:
                        try:
                            # Compare local HEAD with the remote tracking branch's HEAD
                            upstream_latest_commit = repo.remotes[tracking_branch.remote_name].refs[tracking_branch.remote_head].commit
                            if latest_commit != upstream_latest_commit: # If local commit is different from upstream, it's unpushed
                                should_amend = True
                        except Exception as e:
                            self.console.print(f"[yellow]Warning: Could not compare with upstream branch for amending: {e}[/yellow]")
                            # Fallback to creating a new commit if comparison fails
                            should_amend = False
                
                if should_amend:
                    # Amend the last commit
                    repo.git.commit("--amend", "--no-edit")
                    self.console.print(f"[green]Successfully amended previous auto-commit: '{commit_message}'[/green]")
                    return True, "Auto-commit amended successfully."
                else:
                    # Create a new commit
                    repo.index.commit(commit_message)
                    self.console.print(f"[green]Successfully auto-committed changes: '{commit_message}'[/green]")
                    return True, "Auto-commit successful."
            return True, "No uncommitted changes to auto-commit."
        except GitCommandError as e:
            return False, f"Git auto-commit error: {e}"
        except Exception as e:
            return False, f"An unexpected error occurred during auto-commit: {e}"

    def _verify_local_path_is_repo(self, local_path: str) -> bool:
        """Internal helper to verify if the given path is a Git repo."""
        return os.path.exists(os.path.join(local_path, '.git'))

    def is_local_repo_initialized(self, local_path: str) -> bool:
        """Checks if the given local_path is an initialized Git repository."""
        return self._verify_local_path_is_repo(local_path)

    def check_local_repo_exists(self, local_path: str) -> bool:
        """Checks if the local path exists and is a directory."""
        return os.path.isdir(local_path)
