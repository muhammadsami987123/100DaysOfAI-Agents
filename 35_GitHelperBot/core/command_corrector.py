"""
Command corrector for detecting and fixing Git command typos
"""

import difflib
from typing import Optional, Dict, List


class CommandCorrector:
    """Handles Git command typo detection and correction"""
    
    def __init__(self):
        self.git_commands = self._load_git_commands()
        self.common_typos = self._load_common_typos()
    
    def _load_git_commands(self) -> List[str]:
        """Load list of common Git commands"""
        return [
            'add', 'branch', 'checkout', 'clone', 'commit', 'diff', 'fetch',
            'init', 'log', 'merge', 'pull', 'push', 'rebase', 'reset',
            'revert', 'status', 'stash', 'tag', 'remote', 'config', 'show',
            'blame', 'grep', 'ls-files', 'ls-tree', 'cat-file', 'rev-parse',
            'describe', 'archive', 'bundle', 'clean', 'gc', 'fsck', 'reflog',
            'shortlog', 'submodule', 'worktree', 'switch', 'restore'
        ]
    
    def _load_common_typos(self) -> Dict[str, str]:
        """Load common Git command typos and their corrections"""
        return {
            'cmomit': 'commit',
            'comit': 'commit',
            'commmit': 'commit',
            'chekout': 'checkout',
            'checkot': 'checkout',
            'checout': 'checkout',
            'brnch': 'branch',
            'branhc': 'branch',
            'brnach': 'branch',
            'stauts': 'status',
            'statis': 'status',
            'stash': 'stash',
            'stahs': 'stash',
            'pul': 'pull',
            'pus': 'push',
            'pushe': 'push',
            'merg': 'merge',
            'mergge': 'merge',
            'rebas': 'rebase',
            'rebasee': 'rebase',
            'resett': 'reset',
            'resete': 'reset',
            'revertt': 'revert',
            'reverte': 'revert',
            'remot': 'remote',
            'remotee': 'remote',
            'confg': 'config',
            'confgi': 'config',
            'configg': 'config',
            'initi': 'init',
            'initt': 'init',
            'clon': 'clone',
            'clonne': 'clone',
            'fetcc': 'fetch',
            'fetchh': 'fetch',
            'dif': 'diff',
            'difff': 'diff',
            'lo': 'log',
            'logg': 'log',
            'sho': 'show',
            'showw': 'show',
            'blam': 'blame',
            'blamee': 'blame',
            'gre': 'grep',
            'grepp': 'grep',
            'ls-file': 'ls-files',
            'ls-filess': 'ls-files',
            'ls-tre': 'ls-tree',
            'ls-treee': 'ls-tree',
            'cat-fil': 'cat-file',
            'cat-filee': 'cat-file',
            'rev-pars': 'rev-parse',
            'rev-parsee': 'rev-parse',
            'describ': 'describe',
            'describee': 'describe',
            'archiv': 'archive',
            'archivee': 'archive',
            'bundl': 'bundle',
            'bundlee': 'bundle',
            'clea': 'clean',
            'cleann': 'clean',
            'g': 'gc',
            'gcc': 'gc',
            'fsckk': 'fsck',
            'reflog': 'reflog',
            'reflogg': 'reflog',
            'shortlo': 'shortlog',
            'shortlogg': 'shortlog',
            'submodul': 'submodule',
            'submodulee': 'submodule',
            'worktre': 'worktree',
            'worktreee': 'worktree',
            'switc': 'switch',
            'switchh': 'switch',
            'restor': 'restore',
            'restoree': 'restore'
        }
    
    def correct_command(self, command: str) -> Optional[str]:
        """
        Correct Git command typos
        
        Args:
            command: The Git command to correct
            
        Returns:
            Corrected command if typos found, None otherwise
        """
        if not command.startswith('git '):
            return None
        
        parts = command.split()
        if len(parts) < 2:
            return None
        
        git_command = parts[1]
        corrected_command = None
        
        # Check for exact typo matches first
        if git_command in self.common_typos:
            corrected_command = self.common_typos[git_command]
        else:
            # Use fuzzy matching for other typos
            matches = difflib.get_close_matches(
                git_command, 
                self.git_commands, 
                n=1, 
                cutoff=0.6
            )
            if matches:
                corrected_command = matches[0]
        
        if corrected_command and corrected_command != git_command:
            # Reconstruct the full command
            parts[1] = corrected_command
            return ' '.join(parts)
        
        return None
    
    def get_suggestions(self, command: str, max_suggestions: int = 3) -> List[str]:
        """
        Get multiple suggestions for a command
        
        Args:
            command: The Git command to get suggestions for
            max_suggestions: Maximum number of suggestions to return
            
        Returns:
            List of suggested commands
        """
        if not command.startswith('git '):
            return []
        
        parts = command.split()
        if len(parts) < 2:
            return []
        
        git_command = parts[1]
        suggestions = []
        
        # Get fuzzy matches
        matches = difflib.get_close_matches(
            git_command, 
            self.git_commands, 
            n=max_suggestions, 
            cutoff=0.5
        )
        
        for match in matches:
            if match != git_command:
                parts[1] = match
                suggestions.append(' '.join(parts))
        
        return suggestions
    
    def get_usage_examples(self, command: str) -> List[str]:
        """Get usage examples for common Git commands"""
        if not command.startswith('git '):
            return []
        
        parts = command.split()
        if len(parts) < 2:
            return []
        
        git_command = parts[1]
        
        usage_examples = {
            'clone': [
                'git clone https://github.com/user/repo.git',
                'git clone https://github.com/user/repo.git my-project',
                'git clone --branch main https://github.com/user/repo.git'
            ],
            'add': [
                'git add .',
                'git add filename.txt',
                'git add src/',
                'git add -A'
            ],
            'commit': [
                'git commit -m "Your commit message"',
                'git commit -am "Add and commit all changes"',
                'git commit --amend -m "Updated commit message"'
            ],
            'push': [
                'git push origin main',
                'git push -u origin main',
                'git push origin feature-branch'
            ],
            'pull': [
                'git pull origin main',
                'git pull --rebase origin main',
                'git pull origin feature-branch'
            ],
            'checkout': [
                'git checkout main',
                'git checkout -b new-branch',
                'git checkout feature-branch'
            ],
            'branch': [
                'git branch',
                'git branch -a',
                'git branch new-branch',
                'git branch -d old-branch'
            ],
            'merge': [
                'git merge feature-branch',
                'git merge origin/main',
                'git merge --no-ff feature-branch'
            ],
            'rebase': [
                'git rebase main',
                'git rebase -i HEAD~3',
                'git rebase origin/main'
            ],
            'reset': [
                'git reset HEAD~1',
                'git reset --soft HEAD~1',
                'git reset --hard HEAD~1'
            ],
            'stash': [
                'git stash',
                'git stash push -m "Work in progress"',
                'git stash pop',
                'git stash list'
            ]
        }
        
        return usage_examples.get(git_command, [])
