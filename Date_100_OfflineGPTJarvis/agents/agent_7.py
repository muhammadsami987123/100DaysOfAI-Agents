# agent_7.py - GitHelperAgent

import git

class GitHelperAgent:
    def __init__(self, repo_path="."):
        try:
            self.repo = git.Repo(repo_path)
        except git.InvalidGitRepositoryError:
            self.repo = None

    def get_status(self):
        if not self.repo:
            return "Not a git repository."
        
        status = self.repo.git.status()
        return status

    def add_all(self):
        if not self.repo:
            return "Not a git repository."
        
        self.repo.git.add(A=True)
        return "All files added to the staging area."

    def commit(self, message):
        if not self.repo:
            return "Not a git repository."
        
        self.repo.git.commit(m=message)
        return f"Committed with message: {message}"
