import unittest
import os
import shutil
from unittest.mock import MagicMock, patch
from git import Repo, GitCommandError
from rich.console import Console

from agent import AutoUpdaterBot
from github_service import GitHubService
from config import DEFAULT_BRANCH

class TestAutoUpdaterBot(unittest.TestCase):

    def setUp(self):
        self.test_dir = "./test_repo_temp"
        self.console = Console(record=True, force_terminal=True)
        self.updater_bot = AutoUpdaterBot(self.console)
        # Ensure test directory is clean before each test
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        # Clean up test directory after each test
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    @patch.object(GitHubService, 'clone_repository')
    @patch.object(GitHubService, 'pull_repository')
    @patch.object(GitHubService, 'is_local_repo_initialized', return_value=False)
    @patch.object(GitHubService, 'check_local_repo_exists', return_value=False)
    def test_update_repository_clone_success(self, mock_check_local_repo_exists, mock_is_local_repo_initialized, mock_pull_repository, mock_clone_repository):
        mock_clone_repository.return_value = (True, "Repository cloned successfully.")
        self.updater_bot.update_repository("https://github.com/test/repo", self.test_dir)
        mock_clone_repository.assert_called_once_with("https://github.com/test/repo", self.test_dir, DEFAULT_BRANCH)
        self.assertIn("Repository cloned successfully.", self.console.export_text())

    @patch.object(GitHubService, 'clone_repository')
    @patch.object(GitHubService, 'pull_repository')
    @patch.object(GitHubService, 'is_local_repo_initialized', return_value=False)
    @patch.object(GitHubService, 'check_local_repo_exists', return_value=False)
    def test_update_repository_clone_failure(self, mock_check_local_repo_exists, mock_is_local_repo_initialized, mock_pull_repository, mock_clone_repository):
        mock_clone_repository.return_value = (False, "Cloning failed due to permissions.")
        self.updater_bot.update_repository("https://github.com/test/repo", self.test_dir)
        mock_clone_repository.assert_called_once()
        self.assertIn("Cloning failed: Cloning failed due to permissions.", self.console.export_text())

    @patch.object(GitHubService, 'pull_repository')
    @patch.object(GitHubService, 'is_local_repo_initialized', return_value=True)
    @patch.object(GitHubService, 'check_local_repo_exists', return_value=True)
    @patch.object(GitHubService, 'has_uncommitted_changes', return_value=(False, "No uncommitted changes."))
    @patch.object(GitHubService, 'get_latest_commit_info', return_value=("old_hash", "old commit"))
    @patch.object(GitHubService, 'get_remote_head_commit_info', return_value=("new_hash", "new commit"))
    @patch.object(AutoUpdaterBot, '_run_script') # Mock _run_script to prevent actual execution
    def test_update_repository_pull_success(self, mock_run_script, mock_get_remote_head_commit_info, mock_get_latest_commit_info, mock_has_uncommitted_changes, mock_check_local_repo_exists, mock_is_local_repo_initialized):
        mock_pull_repository.return_value = (True, "Repository updated successfully.", ["file1.txt", "file2.js"], ["feat: add new feature"])
        self.updater_bot.update_repository("https://github.com/test/repo", self.test_dir)
        mock_pull_repository.assert_called_once_with(self.test_dir, DEFAULT_BRANCH)
        self.assertIn("Repository updated successfully.", self.console.export_text())
        self.assertIn("Files Updated:", self.console.export_text())
        self.assertIn("Commit Messages Pulled:", self.console.export_text())

    @patch.object(GitHubService, 'pull_repository')
    @patch.object(GitHubService, 'is_local_repo_initialized', return_value=True)
    @patch.object(GitHubService, 'check_local_repo_exists', return_value=True)
    @patch.object(GitHubService, 'has_uncommitted_changes', return_value=(False, "No uncommitted changes."))
    @patch.object(GitHubService, 'get_latest_commit_info', return_value=("old_hash", "old commit"))
    @patch.object(GitHubService, 'get_remote_head_commit_info', return_value=("new_hash", "new commit"))
    @patch.object(AutoUpdaterBot, '_run_script')
    def test_update_repository_pull_failure(self, mock_run_script, mock_get_remote_head_commit_info, mock_get_latest_commit_info, mock_has_uncommitted_changes, mock_check_local_repo_exists, mock_is_local_repo_initialized):
        mock_pull_repository.return_value = (False, "Merge conflict detected!", [], [])
        self.updater_bot.update_repository("https://github.com/test/repo", self.test_dir)
        mock_pull_repository.assert_called_once()
        self.assertIn("Update failed: Merge conflict detected!", self.console.export_text())

    @patch.object(GitHubService, 'pull_repository')
    @patch.object(GitHubService, 'is_local_repo_initialized', return_value=True)
    @patch.object(GitHubService, 'check_local_repo_exists', return_value=True)
    @patch.object(GitHubService, 'has_uncommitted_changes', return_value=(True, "Local changes detected."))
    def test_update_repository_uncommitted_changes(self, mock_has_uncommitted_changes, mock_check_local_repo_exists, mock_is_local_repo_initialized, mock_pull_repository):
        self.updater_bot.update_repository("https://github.com/test/repo", self.test_dir)
        mock_pull_repository.assert_not_called()
        self.assertIn("Error: Local changes detected.", self.console.export_text())

    @patch.object(GitHubService, 'is_local_repo_initialized', return_value=True)
    @patch.object(GitHubService, 'check_local_repo_exists', return_value=True)
    @patch.object(GitHubService, 'has_uncommitted_changes', return_value=(False, ""))
    @patch.object(GitHubService, 'get_latest_commit_info', return_value=("same_hash", ""))
    @patch.object(GitHubService, 'get_remote_head_commit_info', return_value=("same_hash", ""))
    @patch.object(AutoUpdaterBot, '_run_script')
    def test_update_repository_already_up_to_date(self, mock_run_script, mock_get_remote_head_commit_info, mock_get_latest_commit_info, mock_has_uncommitted_changes, mock_check_local_repo_exists, mock_is_local_repo_initialized):
        self.updater_bot.update_repository("https://github.com/test/repo", self.test_dir)
        self.assertIn("Local repository is already up to date with remote.", self.console.export_text())

    @patch.object(GitHubService, 'pull_repository')
    @patch.object(GitHubService, 'is_local_repo_initialized', return_value=True)
    @patch.object(GitHubService, 'check_local_repo_exists', return_value=True)
    @patch.object(GitHubService, 'has_uncommitted_changes', return_value=(False, ""))
    @patch.object(GitHubService, 'get_latest_commit_info', return_value=("old_hash", ""))
    @patch.object(GitHubService, 'get_remote_head_commit_info', return_value=("new_hash", ""))
    @patch.object(AutoUpdaterBot, '_run_script', return_value=(True, "Script Output"))
    def test_update_repository_with_rebuild_and_tests(self, mock_run_script, mock_get_remote_head_commit_info, mock_get_latest_commit_info, mock_has_uncommitted_changes, mock_check_local_repo_exists, mock_is_local_repo_initialized, mock_pull_repository):
        mock_pull_repository.return_value = (True, "Updated.", [], [])
        self.updater_bot.update_repository("https://github.com/test/repo", self.test_dir, rebuild=True, run_tests=True)
        self.assertEqual(mock_run_script.call_count, 2) # Called for rebuild and run_tests
        mock_run_script.assert_any_call(self.test_dir, "rebuild")
        mock_run_script.assert_any_call(self.test_dir, "run_tests")
        self.assertIn("Starting Rebuild Process", self.console.export_text())
        self.assertIn("Starting Test Execution", self.console.export_text())

    @patch.object(GitHubService, 'pull_repository')
    @patch.object(GitHubService, 'is_local_repo_initialized', return_value=True)
    @patch.object(GitHubService, 'check_local_repo_exists', return_value=True)
    @patch.object(GitHubService, 'has_uncommitted_changes', return_value=(False, ""))
    @patch.object(GitHubService, 'get_latest_commit_info', return_value=("old_hash", ""))
    @patch.object(GitHubService, 'get_remote_head_commit_info', return_value=("new_hash", ""))
    def test_update_repository_summary_only_mode(self, mock_get_remote_head_commit_info, mock_get_latest_commit_info, mock_has_uncommitted_changes, mock_check_local_repo_exists, mock_is_local_repo_initialized, mock_pull_repository):
        self.updater_bot.update_repository("https://github.com/test/repo", self.test_dir, summary_only=True)
        mock_pull_repository.assert_not_called()
        self.assertIn("Summary Only Mode: Checking for updates without pulling.", self.console.export_text())
        self.assertIn("Potential updates available on branch", self.console.export_text())

    @patch.object(GitHubService, 'is_local_repo_initialized', return_value=False)
    @patch.object(GitHubService, 'check_local_repo_exists', return_value=True) # Exists but not a repo
    @patch.object(GitHubService, 'clone_repository')
    def test_update_repository_local_path_exists_but_not_repo(self, mock_clone_repository, mock_check_local_repo_exists, mock_is_local_repo_initialized):
        self.updater_bot.update_repository("https://github.com/test/repo", self.test_dir)
        mock_clone_repository.assert_not_called()
        self.assertIn("Error: The directory", self.console.export_text())
        self.assertIn("exists but is not a Git repository", self.console.export_text())

    # Test _run_script when .sh is present
    @patch('subprocess.run')
    def test_run_script_sh_present(self, mock_subprocess_run):
        # Create a dummy .sh file
        script_path = os.path.join(self.test_dir, "rebuild.sh")
        with open(script_path, "w") as f:
            f.write("echo Hello from rebuild.sh")
        os.chmod(script_path, 0o755) # Make it executable
        
        mock_subprocess_run.return_value = MagicMock(stdout="Script output", stderr="", returncode=0)
        success, output = self.updater_bot._run_script(self.test_dir, "rebuild")
        self.assertTrue(success)
        self.assertEqual(output, "Script output")
        mock_subprocess_run.assert_called_once_with(["bash", script_path], cwd=self.test_dir, capture_output=True, text=True, check=True)

    # Test _run_script when .bat is present
    @patch('subprocess.run')
    def test_run_script_bat_present(self, mock_subprocess_run):
        # Create a dummy .bat file
        script_path = os.path.join(self.test_dir, "rebuild.bat")
        with open(script_path, "w") as f:
            f.write("echo Hello from rebuild.bat")

        mock_subprocess_run.return_value = MagicMock(stdout="Script output", stderr="", returncode=0)
        success, output = self.updater_bot._run_script(self.test_dir, "rebuild")
        self.assertTrue(success)
        self.assertEqual(output, "Script output")
        mock_subprocess_run.assert_called_once_with([script_path], cwd=self.test_dir, capture_output=True, text=True, check=True)

    # Test _run_script when no script is found
    @patch('subprocess.run')
    def test_run_script_no_script_found(self, mock_subprocess_run):
        success, message = self.updater_bot._run_script(self.test_dir, "non_existent_script")
        self.assertFalse(success)
        self.assertIn("No non_existent_script.sh or non_existent_script.bat found", message)
        mock_subprocess_run.assert_not_called()

    @patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, 'cmd', stdout='stdout', stderr='stderr'))
    def test_run_script_failure(self, mock_subprocess_run):
        script_path = os.path.join(self.test_dir, "rebuild.sh")
        with open(script_path, "w") as f:
            f.write("exit 1")
        os.chmod(script_path, 0o755) # Make it executable
        
        success, output = self.updater_bot._run_script(self.test_dir, "rebuild")
        self.assertFalse(success)
        self.assertIn("Rebuild failed:", output)


if __name__ == '__main__':
    unittest.main()
