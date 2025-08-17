import re
import requests
import json
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse
from config import (
    GITHUB_API_URL, GITHUB_RAW_URL, GITHUB_TOKEN, 
    MAX_FILE_SIZE, MAX_FILES_TO_ANALYZE, PRIORITY_FILES,
    is_supported_file, ERROR_MESSAGES
)


class GitHubService:
    """Service for interacting with GitHub API and fetching repository data."""
    
    def __init__(self):
        self.session = requests.Session()
        if GITHUB_TOKEN:
            self.session.headers.update({
                'Authorization': f'token {GITHUB_TOKEN}',
                'Accept': 'application/vnd.github.v3+json'
            })
        else:
            self.session.headers.update({
                'Accept': 'application/vnd.github.v3+json'
            })
    
    def parse_github_url(self, url: str) -> Optional[Tuple[str, str]]:
        """Parse GitHub URL to extract owner and repository name."""
        # Handle various GitHub URL formats
        patterns = [
            r'https?://github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$',
            r'https?://github\.com/([^/]+)/([^/]+?)(?:/.*)?$',
            r'git@github\.com:([^/]+)/([^/]+?)(?:\.git)?$'
        ]
        
        for pattern in patterns:
            match = re.match(pattern, url.strip())
            if match:
                owner, repo = match.groups()
                # Remove any trailing slashes or .git
                repo = repo.rstrip('/').replace('.git', '')
                return owner, repo
        
        return None
    
    def get_repository_info(self, owner: str, repo: str) -> Dict:
        """Get basic repository information."""
        url = f"{GITHUB_API_URL}/repos/{owner}/{repo}"
        response = self.session.get(url)
        
        if response.status_code == 404:
            raise ValueError(ERROR_MESSAGES["repository_not_found"])
        elif response.status_code == 403:
            raise ValueError(ERROR_MESSAGES["private_repository"])
        elif response.status_code != 200:
            raise ValueError(ERROR_MESSAGES["fetch_failed"])
        
        return response.json()
    
    def get_repository_structure(self, owner: str, repo: str, path: str = "") -> List[Dict]:
        """Get repository file structure."""
        url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/contents/{path}"
        response = self.session.get(url)
        
        if response.status_code != 200:
            return []
        
        contents = response.json()
        if not isinstance(contents, list):
            return []
        
        files = []
        for item in contents:
            if item['type'] == 'file':
                files.append({
                    'name': item['name'],
                    'path': item['path'],
                    'size': item['size'],
                    'download_url': item['download_url']
                })
            elif item['type'] == 'dir':
                # Recursively get subdirectory contents
                sub_files = self.get_repository_structure(owner, repo, item['path'])
                files.extend(sub_files)
        
        return files
    
    def get_file_content(self, download_url: str) -> Optional[str]:
        """Get file content from GitHub."""
        try:
            response = self.session.get(download_url)
            if response.status_code == 200:
                content = response.text
                # Check file size
                if len(content.encode('utf-8')) > MAX_FILE_SIZE:
                    return None
                return content
        except Exception:
            pass
        return None
    
    def analyze_repository(self, github_url: str) -> Dict:
        """Main method to analyze a GitHub repository."""
        # Parse URL
        parsed = self.parse_github_url(github_url)
        if not parsed:
            raise ValueError(ERROR_MESSAGES["invalid_github_url"])
        
        owner, repo = parsed
        
        # Get repository info
        repo_info = self.get_repository_info(owner, repo)
        
        # Get file structure
        files = self.get_repository_structure(owner, repo)
        
        # Filter and prioritize files
        analyzable_files = []
        for file in files:
            if is_supported_file(file['name']):
                analyzable_files.append(file)
        
        # Sort by priority (README files first, then priority files, then others)
        def get_file_priority(file_info):
            name = file_info['name']
            if name.lower().startswith('readme'):
                return 0
            elif name in PRIORITY_FILES:
                return 1
            else:
                return 2
        
        analyzable_files.sort(key=get_file_priority)
        
        # Limit the number of files to analyze
        if len(analyzable_files) > MAX_FILES_TO_ANALYZE:
            analyzable_files = analyzable_files[:MAX_FILES_TO_ANALYZE]
        
        # Fetch content for priority files
        file_contents = {}
        for file in analyzable_files:
            if file['download_url']:
                content = self.get_file_content(file['download_url'])
                if content:
                    file_contents[file['path']] = {
                        'name': file['name'],
                        'size': file['size'],
                        'content': content
                    }
        
        # Extract technologies
        technologies = self.extract_key_technologies(analyzable_files, file_contents)
        
        # Analyze project structure
        structure_analysis = self.analyze_project_structure(analyzable_files)
        
        return {
            'repository_info': repo_info,
            'files': analyzable_files,
            'file_contents': file_contents,
            'total_files': len(files),
            'analyzable_files': len(analyzable_files),
            'technologies': technologies,
            'structure_analysis': structure_analysis
        }
    
    def analyze_project_structure(self, files: List[Dict]) -> Dict:
        """Analyze the project structure and patterns."""
        analysis = {
            'has_readme': False,
            'has_license': False,
            'has_docker': False,
            'has_tests': False,
            'has_docs': False,
            'has_ci_cd': False,
            'main_language': None,
            'framework_detected': None,
            'build_system': None,
            'package_manager': None
        }
        
        # Check for key files
        for file in files:
            name = file['name'].lower()
            path = file['path'].lower()
            
            if name.startswith('readme'):
                analysis['has_readme'] = True
            elif name in ['license', 'license.txt', 'license.md']:
                analysis['has_license'] = True
            elif name in ['dockerfile', 'docker-compose.yml', 'docker-compose.yaml']:
                analysis['has_docker'] = True
            elif 'test' in path or 'spec' in path or 'tests' in path:
                analysis['has_tests'] = True
            elif 'docs' in path or 'documentation' in path:
                analysis['has_docs'] = True
            elif '.github' in path or 'ci' in path or 'cd' in path:
                analysis['has_ci_cd'] = True
        
        # Detect main language and framework
        language_counts = {}
        for file in files:
            ext = file['name'].split('.')[-1].lower()
            if ext in ['py', 'js', 'ts', 'java', 'cpp', 'c', 'go', 'rs', 'php', 'rb']:
                language_counts[ext] = language_counts.get(ext, 0) + 1
        
        if language_counts:
            analysis['main_language'] = max(language_counts, key=language_counts.get)
        
        # Detect framework and build system
        for file in files:
            name = file['name'].lower()
            if name == 'package.json':
                analysis['package_manager'] = 'npm'
            elif name == 'requirements.txt':
                analysis['build_system'] = 'pip'
            elif name == 'pom.xml':
                analysis['build_system'] = 'maven'
            elif name == 'build.gradle':
                analysis['build_system'] = 'gradle'
            elif name == 'cargo.toml':
                analysis['build_system'] = 'cargo'
            elif name == 'go.mod':
                analysis['build_system'] = 'go modules'
        
        return analysis
    
    def get_folder_structure_text(self, files: List[Dict]) -> str:
        """Convert file structure to readable text format."""
        if not files:
            return "No files found"
        
        # Group files by directory
        structure = {}
        for file in files:
            path_parts = file['path'].split('/')
            if len(path_parts) == 1:
                # Root level file
                if 'root' not in structure:
                    structure['root'] = []
                structure['root'].append(file['name'])
            else:
                # File in subdirectory
                dir_path = '/'.join(path_parts[:-1])
                if dir_path not in structure:
                    structure[dir_path] = []
                structure[dir_path].append(path_parts[-1])
        
        # Format the structure
        lines = []
        for path, files_list in sorted(structure.items()):
            if path == 'root':
                lines.append("📁 Root Directory:")
            else:
                lines.append(f"📁 {path}/")
            
            for file_name in sorted(files_list):
                lines.append(f"  📄 {file_name}")
            lines.append("")
        
        return '\n'.join(lines)
    
    def extract_key_technologies(self, files: List[Dict], file_contents: Dict) -> List[str]:
        """Extract key technologies from repository files."""
        technologies = set()
        
        # Check for common technology indicators
        tech_indicators = {
            'Python': ['.py', 'requirements.txt', 'setup.py', 'pyproject.toml'],
            'JavaScript/Node.js': ['.js', '.ts', '.jsx', '.tsx', 'package.json', 'yarn.lock'],
            'Java': ['.java', 'pom.xml', 'build.gradle', '.gradle'],
            'C++': ['.cpp', '.cc', '.cxx', '.h', '.hpp', 'CMakeLists.txt'],
            'C#': ['.cs', '.csproj', '.sln', 'packages.config'],
            'PHP': ['.php', 'composer.json', 'composer.lock'],
            'Go': ['.go', 'go.mod', 'go.sum'],
            'Rust': ['.rs', 'Cargo.toml', 'Cargo.lock'],
            'Swift': ['.swift', 'Package.swift'],
            'Kotlin': ['.kt', '.kts', 'build.gradle.kts'],
            'Ruby': ['.rb', 'Gemfile', 'Gemfile.lock'],
            'Docker': ['Dockerfile', 'docker-compose.yml', '.dockerignore'],
            'React': ['.jsx', '.tsx', 'react', 'react-dom'],
            'Vue': ['.vue', 'vue.config.js'],
            'Angular': ['angular.json', 'angular-cli.json'],
            'Flask': ['flask', 'app.py'],
            'Django': ['django', 'manage.py', 'settings.py'],
            'FastAPI': ['fastapi', 'main.py'],
            'Express': ['express', 'app.js', 'server.js']
        }
        
        for tech, indicators in tech_indicators.items():
            for file in files:
                if any(indicator in file['name'].lower() for indicator in indicators):
                    technologies.add(tech)
                    break
        
        # Check file contents for additional indicators
        for file_path, content_info in file_contents.items():
            content = content_info['content'].lower()
            
            # Check for framework mentions
            if 'react' in content and 'react-dom' in content:
                technologies.add('React')
            if 'vue' in content and ('vue.config' in content or 'vue-router' in content):
                technologies.add('Vue')
            if 'angular' in content:
                technologies.add('Angular')
            if 'flask' in content:
                technologies.add('Flask')
            if 'django' in content:
                technologies.add('Django')
            if 'fastapi' in content:
                technologies.add('FastAPI')
            if 'express' in content:
                technologies.add('Express')
            if 'spring' in content:
                technologies.add('Spring')
            if 'laravel' in content:
                technologies.add('Laravel')
        
        return sorted(list(technologies))
