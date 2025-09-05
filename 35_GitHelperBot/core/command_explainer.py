"""
Command explainer using OpenAI GPT for Git command explanations
"""

import re
from typing import Optional
from config.openai_config import OpenAIConfig


class CommandExplainer:
    """Handles Git command explanations using OpenAI GPT"""
    
    def __init__(self, config: OpenAIConfig):
        self.config = config
        self.client = config.get_client()
    
    def explain_command(self, command: str) -> str:
        """
        Explain a Git command using GPT
        
        Args:
            command: The Git command to explain
            
        Returns:
            Markdown-formatted explanation
        """
        if not self.config.is_available():
            return self._fallback_explanation(command)
        
        try:
            prompt = self._create_command_prompt(command)
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return self._fallback_explanation(command)
    
    def explain_query(self, query: str) -> str:
        """
        Explain a natural language query about Git
        
        Args:
            query: Natural language query
            
        Returns:
            Markdown-formatted explanation with commands
        """
        if not self.config.is_available():
            return self._fallback_query_explanation(query)
        
        try:
            prompt = self._create_query_prompt(query)
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return self._fallback_query_explanation(query)
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for Git explanations"""
        return """You are a Git expert assistant. Your job is to explain Git commands and concepts clearly and concisely.

Guidelines:
1. Always format your responses in clean Markdown
2. Use code blocks with bash syntax for commands
3. Explain what each command does and when to use it
4. Include practical examples when helpful
5. Be concise but comprehensive
6. Use emojis sparingly and appropriately
7. Structure explanations with clear headings

Format examples like this:
### Command Name
Brief description of what the command does.

```bash
git command --options
```

**Explanation:** Detailed explanation of the command and its options.

**When to use:** Specific use cases and scenarios."""
    
    def _create_command_prompt(self, command: str) -> str:
        """Create prompt for command explanation"""
        return f"""Please explain this Git command in detail:

Command: {command}

Provide:
1. What the command does
2. What each option/flag means
3. Common use cases
4. Any warnings or best practices
5. Example usage if helpful

Format the response in clean Markdown with proper code blocks."""
    
    def _create_query_prompt(self, query: str) -> str:
        """Create prompt for natural language query"""
        return f"""The user is asking about Git: "{query}"

Please provide:
1. A clear explanation of the concept or task
2. The specific Git commands needed
3. Step-by-step instructions if applicable
4. Examples and use cases
5. Any important warnings or considerations

Format the response in clean Markdown with proper code blocks and clear structure."""
    
    def _fallback_explanation(self, command: str) -> str:
        """Fallback explanation when OpenAI is not available"""
        # Basic explanations for common commands
        explanations = {
            'git add': """### Git Add
Adds files to the staging area for the next commit.

```bash
git add <file>
git add .  # Add all files
git add -A # Add all files including deletions
```

**Explanation:** The `git add` command stages changes for commit. Files must be staged before they can be committed.

**When to use:** Before committing changes to include them in the next commit.""",
            
            'git commit': """### Git Commit
Creates a new commit with staged changes.

```bash
git commit -m "Your commit message"
git commit -am "Add and commit all changes"
```

**Explanation:** The `git commit` command creates a snapshot of your staged changes with a descriptive message.

**When to use:** After staging changes to save them to the repository history.""",
            
            'git push': """### Git Push
Uploads local commits to a remote repository.

```bash
git push origin main
git push -u origin main  # Set upstream branch
```

**Explanation:** The `git push` command sends your local commits to the remote repository.

**When to use:** After committing changes locally to share them with others.""",
            
            'git pull': """### Git Pull
Downloads and merges changes from a remote repository.

```bash
git pull origin main
git pull --rebase  # Use rebase instead of merge
```

**Explanation:** The `git pull` command fetches changes from remote and merges them into your current branch.

**When to use:** Before starting work or when you want to get the latest changes."""
        }
        
        # Try to find a matching explanation
        for key, explanation in explanations.items():
            if command.startswith(key):
                return explanation
        
        return f"""### Git Command Explanation
Command: `{command}`

**Note:** Detailed explanation not available offline. 
This appears to be a Git command. For full explanations, please set up your OpenAI API key.

**Common Git Commands:**
- `git add` - Stage changes
- `git commit` - Create a commit
- `git push` - Upload to remote
- `git pull` - Download from remote
- `git status` - Check repository status
- `git log` - View commit history"""
    
    def _fallback_query_explanation(self, query: str) -> str:
        """Fallback explanation for natural language queries"""
        return f"""### Git Help
Query: "{query}"

**Note:** AI-powered explanations not available offline. 
Please set up your OpenAI API key for detailed explanations.

**Common Git Tasks:**
- **Initialize repository:** `git init`
- **Clone repository:** `git clone <url>`
- **Check status:** `git status`
- **Add files:** `git add <file>`
- **Commit changes:** `git commit -m "message"`
- **Push changes:** `git push origin main`
- **Pull changes:** `git pull origin main`
- **Create branch:** `git checkout -b <branch-name>`
- **Switch branch:** `git checkout <branch-name>`
- **Merge branch:** `git merge <branch-name>`

For more help, visit: https://git-scm.com/docs"""
