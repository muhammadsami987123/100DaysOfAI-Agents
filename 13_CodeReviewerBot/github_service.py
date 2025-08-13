import re
import requests
from typing import Optional, Tuple, Dict, Any
from urllib.parse import urlparse, unquote

from config import GITHUB_API_URL, GITHUB_RAW_URL, ERROR_MESSAGES


class GitHubService:
    """Service for fetching code from GitHub repositories."""
    
    def __init__(self):
        self.api_url = GITHUB_API_URL
        self.raw_url = GITHUB_RAW_URL
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CodeReviewerBot/1.0',
            'Accept': 'application/vnd.github.v3.raw'
        })
    
    def extract_github_info(self, url: str) -> Optional[Dict[str, str]]:
        """
        Extract repository and file information from GitHub URL.
        
        Args:
            url: GitHub URL (file or repository)
        
        Returns:
            Dictionary with owner, repo, path, and branch information
        """
        try:
            parsed = urlparse(url)
            
            # Handle different GitHub URL formats
            if parsed.netloc not in ['github.com', 'www.github.com']:
                return None
            
            path_parts = parsed.path.strip('/').split('/')
            
            if len(path_parts) < 2:
                return None
            
            owner = path_parts[0]
            repo = path_parts[1]
            
            # Check if it's a file URL
            if len(path_parts) >= 4 and path_parts[2] == 'blob':
                branch = path_parts[3]
                file_path = '/'.join(path_parts[4:])
                return {
                    'owner': owner,
                    'repo': repo,
                    'branch': branch,
                    'path': file_path,
                    'type': 'file'
                }
            
            # Check if it's a repository URL
            elif len(path_parts) == 2:
                return {
                    'owner': owner,
                    'repo': repo,
                    'type': 'repo'
                }
            
            return None
            
        except Exception:
            return None
    
    def fetch_file_content(self, owner: str, repo: str, path: str, branch: str = "main") -> Tuple[Optional[str], Optional[str]]:
        """
        Fetch file content from GitHub.
        
        Args:
            owner: Repository owner
            repo: Repository name
            path: File path in repository
            branch: Branch name (default: main)
        
        Returns:
            Tuple of (content, filename) or (None, None) if failed
        """
        try:
            # Try main branch first, then master
            branches_to_try = [branch, "main", "master"]
            
            for branch_name in branches_to_try:
                url = f"{self.raw_url}/{owner}/{repo}/{branch_name}/{path}"
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    filename = path.split('/')[-1]
                    return response.text, filename
            
            return None, None
            
        except Exception as e:
            print(f"Error fetching file content: {e}")
            return None, None
    
    def fetch_repository_files(self, owner: str, repo: str, branch: str = "main") -> Optional[Dict[str, str]]:
        """
        Fetch all code files from a repository.
        
        Args:
            owner: Repository owner
            repo: Repository name
            branch: Branch name (default: main)
        
        Returns:
            Dictionary mapping filenames to content, or None if failed
        """
        try:
            # Get repository tree
            api_url = f"{self.api_url}/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
            response = self.session.get(api_url, timeout=10)
            
            if response.status_code != 200:
                return None
            
            tree_data = response.json()
            files = {}
            
            # Supported file extensions
            supported_extensions = {'.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.cc', '.cxx', 
                                  '.h', '.hpp', '.cs', '.php', '.go', '.rs', '.swift', '.kt', '.kts'}
            
            for item in tree_data.get('tree', []):
                if item['type'] == 'blob':
                    file_path = item['path']
                    extension = '.' + file_path.split('.')[-1].lower() if '.' in file_path else ''
                    
                    if extension in supported_extensions:
                        content, filename = self.fetch_file_content(owner, repo, file_path, branch)
                        if content:
                            files[filename] = content
            
            return files if files else None
            
        except Exception as e:
            print(f"Error fetching repository files: {e}")
            return None
    
    def fetch_from_url(self, url: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Fetch code from GitHub URL.
        
        Args:
            url: GitHub URL (file or repository)
        
        Returns:
            Tuple of (content, filename, language) or (None, None, None) if failed
        """
        github_info = self.extract_github_info(url)
        
        if not github_info:
            return None, None, None
        
        try:
            if github_info['type'] == 'file':
                # Fetch single file
                content, filename = self.fetch_file_content(
                    github_info['owner'],
                    github_info['repo'],
                    github_info['path'],
                    github_info.get('branch', 'main')
                )
                
                if content:
                    language = self._detect_language_from_filename(filename)
                    return content, filename, language
                
            elif github_info['type'] == 'repo':
                # Fetch repository files
                files = self.fetch_repository_files(
                    github_info['owner'],
                    github_info['repo']
                )
                
                if files:
                    # Return the first file found
                    filename = list(files.keys())[0]
                    content = files[filename]
                    language = self._detect_language_from_filename(filename)
                    return content, filename, language
            
            return None, None, None
            
        except Exception as e:
            print(f"Error fetching from GitHub URL: {e}")
            return None, None, None
    
    def _detect_language_from_filename(self, filename: str) -> str:
        """Detect programming language from filename."""
        if not filename:
            return "unknown"
        
        extension = '.' + filename.split('.')[-1].lower() if '.' in filename else ''
        
        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'javascript',
            '.tsx': 'javascript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.cc': 'cpp',
            '.cxx': 'cpp',
            '.h': 'cpp',
            '.hpp': 'cpp',
            '.cs': 'csharp',
            '.php': 'php',
            '.go': 'go',
            '.rs': 'rust',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.kts': 'kotlin'
        }
        
        return language_map.get(extension, "unknown")
    
    def validate_github_url(self, url: str) -> bool:
        """Validate if the URL is a valid GitHub URL."""
        github_info = self.extract_github_info(url)
        return github_info is not None
    
    def get_repository_info(self, owner: str, repo: str) -> Optional[Dict[str, Any]]:
        """
        Get basic repository information.
        
        Args:
            owner: Repository owner
            repo: Repository name
        
        Returns:
            Repository information or None if failed
        """
        try:
            api_url = f"{self.api_url}/repos/{owner}/{repo}"
            response = self.session.get(api_url, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            
            return None
            
        except Exception as e:
            print(f"Error fetching repository info: {e}")
            return None
    
    def is_public_repository(self, owner: str, repo: str) -> bool:
        """
        Check if a repository is public.
        
        Args:
            owner: Repository owner
            repo: Repository name
        
        Returns:
            True if repository is public, False otherwise
        """
        repo_info = self.get_repository_info(owner, repo)
        return repo_info is not None and not repo_info.get('private', True)
