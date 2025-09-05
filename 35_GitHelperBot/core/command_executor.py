"""
Command executor for safely running Git commands
"""

import subprocess
import shlex
from typing import Dict, List, Optional


class CommandExecutor:
    """Handles safe execution of Git commands"""
    
    def __init__(self):
        self.dangerous_commands = self._load_dangerous_commands()
        self.safe_commands = self._load_safe_commands()
    
    def _load_dangerous_commands(self) -> List[str]:
        """Load list of potentially dangerous Git commands"""
        return [
            'git reset --hard',
            'git clean -fd',
            'git push --force',
            'git push -f',
            'git rebase --onto',
            'git filter-branch',
            'git gc --aggressive',
            'git reflog expire',
            'git prune',
            'git remote remove',
            'git branch -D',
            'git tag -d'
        ]
    
    def _load_safe_commands(self) -> List[str]:
        """Load list of safe Git commands"""
        return [
            'git status',
            'git log',
            'git diff',
            'git show',
            'git branch',
            'git remote -v',
            'git config --list',
            'git help',
            'git --version',
            'git init',
            'git clone',
            'git add',
            'git commit',
            'git push',
            'git pull',
            'git fetch',
            'git merge',
            'git checkout',
            'git switch',
            'git restore',
            'git stash',
            'git tag',
            'git blame',
            'git grep',
            'git ls-files',
            'git ls-tree',
            'git cat-file',
            'git rev-parse',
            'git describe',
            'git archive',
            'git shortlog',
            'git submodule',
            'git worktree'
        ]
    
    def execute_command(self, command: str) -> Dict[str, any]:
        """
        Execute a Git command safely
        
        Args:
            command: The Git command to execute
            
        Returns:
            Dictionary with success status, output, and error information
        """
        if not command.startswith('git '):
            return {
                'success': False,
                'error': 'Not a Git command',
                'output': None
            }
        
        # Check if command is dangerous
        if self._is_dangerous_command(command):
            return {
                'success': False,
                'error': 'Command is potentially dangerous and blocked for safety',
                'output': None
            }
        
        try:
            # Parse command safely
            parts = shlex.split(command)
            
            # Execute command
            result = subprocess.run(
                parts,
                capture_output=True,
                text=True,
                timeout=30,  # 30 second timeout
                cwd='.'  # Run in current directory
            )
            
            # Check if it's a help/usage message (common when missing arguments)
            is_help_message = any(keyword in result.stderr.lower() if result.stderr else False 
                                for keyword in ['usage:', 'fatal:', 'error:'])
            
            return {
                'success': result.returncode == 0,
                'output': result.stdout if result.stdout else None,
                'error': result.stderr if result.stderr else None,
                'return_code': result.returncode,
                'is_help_message': is_help_message
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Command timed out after 30 seconds',
                'output': None
            }
        except FileNotFoundError:
            return {
                'success': False,
                'error': 'Git not found. Please ensure Git is installed and in PATH',
                'output': None
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Execution error: {str(e)}',
                'output': None
            }
    
    def _is_dangerous_command(self, command: str) -> bool:
        """Check if a command is potentially dangerous"""
        command_lower = command.lower()
        
        # Check for dangerous patterns
        dangerous_patterns = [
            '--force',
            '--hard',
            '--delete',
            '--remove',
            '--prune',
            '--aggressive',
            '--expire',
            'filter-branch'
        ]
        
        for pattern in dangerous_patterns:
            if pattern in command_lower:
                return True
        
        # Check for specific dangerous commands
        for dangerous_cmd in self.dangerous_commands:
            if command.startswith(dangerous_cmd):
                return True
        
        return False
    
    def validate_command(self, command: str) -> Dict[str, any]:
        """
        Validate a Git command without executing it
        
        Args:
            command: The Git command to validate
            
        Returns:
            Dictionary with validation results
        """
        if not command.startswith('git '):
            return {
                'valid': False,
                'error': 'Not a Git command',
                'warning': None
            }
        
        # Check if command is dangerous
        if self._is_dangerous_command(command):
            return {
                'valid': True,
                'error': None,
                'warning': 'This command is potentially dangerous. Proceed with caution.'
            }
        
        # Check if command is in safe list
        parts = command.split()
        if len(parts) >= 2:
            base_command = f"git {parts[1]}"
            if base_command in self.safe_commands:
                return {
                    'valid': True,
                    'error': None,
                    'warning': None
                }
        
        return {
            'valid': True,
            'error': None,
            'warning': 'Command not in safe list. Please verify before executing.'
        }
    
    def get_command_help(self, command: str) -> Optional[str]:
        """
        Get help for a Git command
        
        Args:
            command: The Git command to get help for
            
        Returns:
            Help text or None if not available
        """
        if not command.startswith('git '):
            return None
        
        try:
            # Extract the base command
            parts = command.split()
            if len(parts) < 2:
                return None
            
            base_command = parts[1]
            help_command = f"git help {base_command}"
            
            result = subprocess.run(
                shlex.split(help_command),
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return result.stdout
            else:
                return None
                
        except Exception:
            return None
