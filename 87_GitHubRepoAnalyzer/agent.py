"""
GitHubRepoAnalyzer Agent
- Accepts GitHub repo URL
- Fetches file tree, README, key files via GitHub API
- Summarizes repo using LLM (Gemini or GPT-4.1)
- Returns structured analysis
"""

import os
import json
import httpx

GITHUB_API_URL = "https://api.github.com/repos/"


from utils.llm_service import LLMService
from typing import Dict, Any, Optional

class GitHubRepoAnalyzer:
    def __init__(self, llm_service: Optional[LLMService] = None, storage_file: str = "repo_analysis.json"):
        self.llm = llm_service or LLMService()
        self.storage_file = storage_file
        self.analysis_cache = self._load_cache()

    def _load_cache(self) -> Dict[str, Any]:
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_cache(self) -> None:
        with open(self.storage_file, "w", encoding="utf-8") as f:
            json.dump(self.analysis_cache, f, indent=2)

    async def fetch_repo_data(self, repo_url: str) -> Dict[str, Any]:
        import re
        match = re.search(r"github.com/([^/]+)/([^/]+)", repo_url)
        if not match:
            raise ValueError("Invalid GitHub repo URL")
        owner, repo = match.group(1), match.group(2)
        async with httpx.AsyncClient() as client:
            tree_url = f"{GITHUB_API_URL}{owner}/{repo}/git/trees/main?recursive=1"
            tree_resp = await client.get(tree_url)
            tree = tree_resp.json().get("tree", [])
            readme_url = f"{GITHUB_API_URL}{owner}/{repo}/readme"
            readme_resp = await client.get(readme_url, headers={"Accept": "application/vnd.github.v3.raw"})
            readme = readme_resp.text if readme_resp.status_code == 200 else ""
            key_files = {}
            for file in tree:
                path = file.get("path", "")
                if path.lower() in ["main.py", "app.js", "index.js", "app.py"]:
                    file_url = f"{GITHUB_API_URL}{owner}/{repo}/contents/{path}"
                    file_resp = await client.get(file_url, headers={"Accept": "application/vnd.github.v3.raw"})
                    key_files[path] = file_resp.text if file_resp.status_code == 200 else ""
            return {
                "owner": owner,
                "repo": repo,
                "tree": tree,
                "readme": readme,
                "key_files": key_files
            }

    async def analyze_repo(self, repo_url: str, llm_choice: str = "gemini") -> str:
        repo_data = await self.fetch_repo_data(repo_url)
        summary = self.llm.generate_content(repo_data, llm_choice)
        self.analysis_cache[repo_url] = summary
        self._save_cache()
        return summary
