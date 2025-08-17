import openai
from typing import Dict, List, Optional
from config import (
    OPENAI_API_KEY, OPENAI_MODEL, MAX_TOKENS, TEMPERATURE,
    get_language_config, ERROR_MESSAGES
)


class AISummarizer:
    """AI service for generating repository summaries using OpenAI GPT."""
    
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError(ERROR_MESSAGES["missing_api_key"])
        
        self.api_key = OPENAI_API_KEY
        self.model = OPENAI_MODEL
        self.max_tokens = MAX_TOKENS
        self.temperature = TEMPERATURE
    
    def generate_summary(self, repo_data: Dict, language: str = "en") -> str:
        """Generate a comprehensive repository summary using AI."""
        try:
            # Get language configuration
            lang_config = get_language_config(language)
            
            # Prepare the prompt
            prompt = self._build_prompt(repo_data, language)
            
            # Generate summary using OpenAI
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt(language)
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            summary = response.choices[0].message.content.strip()
            return summary
            
        except Exception as e:
            if "OpenAI" in str(e) or "API" in str(e):
                raise ValueError(f"OpenAI API error: {str(e)}")
            else:
                raise ValueError(f"Summary generation failed: {str(e)}")
    
    def _get_system_prompt(self, language: str) -> str:
        """Get the system prompt based on language."""
        if language == "ur":
            return """آپ ایک ماہر AI اسسٹنٹ ہیں جو GitHub repositories کا گہرا اور تفصیلی تجزیہ کرتے ہیں۔

آپ کا کام ہے:
1. Repository کی مکمل تفہیم حاصل کرنا
2. Project کی اہمیت اور مقصد کو واضح کرنا
3. Technical details کو سادہ زبان میں بیان کرنا
4. Practical insights فراہم کرنا

آپ کا output ہونا چاہیے:
1. **Project Overview** – project کا مقصد، اہمیت، اور بنیادی functionality (4-5 لائنیں)
2. **Key Features & Capabilities** – detailed bullet points میں main features
3. **Technology Stack** – تمام detected technologies، frameworks، اور tools کی comprehensive list
4. **Architecture & Structure** – project کی organization، patterns، اور design approach
5. **Setup & Usage** – step-by-step installation اور usage instructions
6. **Code Quality Insights** – project structure، best practices، اور potential improvements
7. **Recommendations** – missing elements، improvements، اور best practices

ہمیشہ detailed، informative، اور actionable insights فراہم کریں۔"""
        
        elif language == "hi":
            return """आप एक विशेषज्ञ AI सहायक हैं जो GitHub repositories का गहरा और विस्तृत विश्लेषण करते हैं।

आपका काम है:
1. Repository की पूरी समझ प्राप्त करना
2. Project की महत्वपूर्णता और उद्देश्य को स्पष्ट करना
3. Technical details को सरल भाषा में बताना
4. Practical insights प्रदान करना

आपका output होना चाहिए:
1. **Project Overview** – project का उद्देश्य, महत्व, और मूल functionality (4-5 पंक्तियों में)
2. **Key Features & Capabilities** – detailed bullet points में main features
3. **Technology Stack** – सभी detected technologies, frameworks, और tools की comprehensive list
4. **Architecture & Structure** – project की organization, patterns, और design approach
5. **Setup & Usage** – step-by-step installation और usage instructions
6. **Code Quality Insights** – project structure, best practices, और potential improvements
7. **Recommendations** – missing elements, improvements, और best practices

हमेशा detailed, informative, और actionable insights प्रदान करें।"""
        
        else:  # English (default)
            return """You are an expert AI assistant specializing in deep and comprehensive GitHub repository analysis.

Your role is to:
1. Gain complete understanding of the repository
2. Clarify the project's purpose, significance, and core functionality
3. Explain technical details in simple, accessible language
4. Provide practical insights and actionable recommendations

Your output must include:
1. **Project Overview** – Purpose, significance, and core functionality (4-5 lines)
2. **Key Features & Capabilities** – Detailed bullet points of main features
3. **Technology Stack** – Comprehensive list of all detected technologies, frameworks, and tools
4. **Architecture & Structure** – Project organization, patterns, and design approach
5. **Setup & Usage** – Step-by-step installation and usage instructions
6. **Code Quality Insights** – Project structure, best practices, and potential improvements
7. **Recommendations** – Missing elements, improvements, and best practices

Always provide detailed, informative, and actionable insights. Focus on practical value and real-world applicability."""
    
    def _build_prompt(self, repo_data: Dict, language: str) -> str:
        """Build the user prompt for the AI model."""
        repo_info = repo_data['repository_info']
        files = repo_data['files']
        file_contents = repo_data['file_contents']
        technologies = repo_data.get('technologies', [])
        structure_analysis = repo_data.get('structure_analysis', {})
        
        # Extract key information
        repo_name = repo_info.get('name', 'Unknown')
        description = repo_info.get('description', 'No description available')
        language_detected = repo_info.get('language', 'Unknown')
        stars = repo_info.get('stargazers_count', 0)
        forks = repo_info.get('forks_count', 0)
        created_at = repo_info.get('created_at', 'Unknown')
        updated_at = repo_info.get('updated_at', 'Unknown')
        topics = repo_info.get('topics', [])
        homepage = repo_info.get('homepage', '')
        license_info = repo_info.get('license', {})
        
        # Get README content if available
        readme_content = ""
        for file_path, content_info in file_contents.items():
            if content_info['name'].lower().startswith('readme'):
                readme_content = content_info['content']
                break
        
        # Get key configuration files with better analysis
        config_files = {}
        main_files = {}
        source_files = {}
        
        for file_path, content_info in file_contents.items():
            file_name = content_info['name']
            
            # Configuration files
            if file_path in ['package.json', 'requirements.txt', 'pom.xml', 'build.gradle', 
                           'Cargo.toml', 'Gemfile', 'composer.json', 'setup.py', 
                           'pyproject.toml', 'Dockerfile', 'docker-compose.yml', 'go.mod',
                           'package-lock.json', 'yarn.lock', 'composer.lock']:
                config_files[file_path] = content_info['content']
            
            # Main entry points
            elif file_name in ['main.py', 'app.py', 'index.py', 'index.js', 'index.ts', 
                             'index.html', 'main.go', 'main.rs', 'main.java']:
                main_files[file_path] = content_info['content']
            
            # Source files (first 500 chars for context)
            elif any(file_name.endswith(ext) for ext in ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs']):
                source_files[file_path] = content_info['content'][:500]
        
        # Build comprehensive prompt
        prompt_parts = [
            f"=== REPOSITORY ANALYSIS REQUEST ===",
            f"",
            f"Repository: {repo_name}",
            f"Description: {description}",
            f"Primary Language: {language_detected}",
            f"Stars: {stars:,}, Forks: {forks:,}",
            f"Created: {created_at}, Last Updated: {updated_at}",
            f"Topics: {', '.join(topics) if topics else 'None'}",
            f"Homepage: {homepage if homepage else 'None'}",
            f"License: {license_info.get('name', 'None') if license_info else 'None'}",
            f"",
            f"=== DETECTED TECHNOLOGIES ===",
            f"Technologies: {', '.join(technologies) if technologies else 'None detected'}",
            f"Build System: {structure_analysis.get('build_system', 'Unknown')}",
            f"Package Manager: {structure_analysis.get('package_manager', 'Unknown')}",
            f"",
            f"=== PROJECT STRUCTURE ANALYSIS ===",
            f"Has README: {structure_analysis.get('has_readme', False)}",
            f"Has License: {structure_analysis.get('has_license', False)}",
            f"Has Docker: {structure_analysis.get('has_docker', False)}",
            f"Has Tests: {structure_analysis.get('has_tests', False)}",
            f"Has Documentation: {structure_analysis.get('has_docs', False)}",
            f"Has CI/CD: {structure_analysis.get('has_ci_cd', False)}",
            f"",
            f"=== REPOSITORY STRUCTURE ===",
            self._format_file_structure(files),
            f""
        ]
        
        if readme_content:
            prompt_parts.extend([
                f"=== README CONTENT ===",
                readme_content[:3000] + ("..." if len(readme_content) > 3000 else ""),
                f""
            ])
        
        if config_files:
            prompt_parts.append("=== CONFIGURATION FILES ===")
            for file_name, content in config_files.items():
                prompt_parts.append(f"📄 {file_name}:")
                prompt_parts.append(content[:1500] + ("..." if len(content) > 1500 else ""))
                prompt_parts.append("")
        
        if main_files:
            prompt_parts.append("=== MAIN ENTRY POINTS ===")
            for file_name, content in main_files.items():
                prompt_parts.append(f"🚀 {file_name}:")
                prompt_parts.append(content[:1000] + ("..." if len(content) > 1000 else ""))
                prompt_parts.append("")
        
        if source_files:
            prompt_parts.append("=== SOURCE CODE SAMPLES ===")
            for file_name, content in source_files.items():
                prompt_parts.append(f"💻 {file_name}:")
                prompt_parts.append(content + ("..." if len(content) >= 500 else ""))
                prompt_parts.append("")
        
        # Add analysis instructions
        lang_config = get_language_config(language)
        prompt_parts.extend([
            f"=== ANALYSIS INSTRUCTIONS ===",
            f"Based on the above information, provide a comprehensive analysis including:",
            f"1. What this project does and why it's useful",
            f"2. Key features and capabilities",
            f"3. Technology stack and dependencies",
            f"4. Project architecture and structure",
            f"5. How to set up and use the project",
            f"6. Code quality insights and patterns",
            f"7. Recommendations for improvements",
            f"",
            f"Provide detailed, practical insights that would help a developer understand and work with this project.",
            f"",
            f"Language: {lang_config['name']} ({language.upper()})"
        ])
        
        return "\n".join(prompt_parts)
    
    def _format_file_structure(self, files: List[Dict]) -> str:
        """Format file structure for the prompt."""
        if not files:
            return "No files found"
        
        # Group by directory with better organization
        structure = {}
        file_types = {
            'config': [],
            'source': [],
            'docs': [],
            'assets': [],
            'other': []
        }
        
        for file in files:
            path_parts = file['path'].split('/')
            file_name = file['name']
            
            # Categorize files
            if any(file_name.endswith(ext) for ext in ['.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.env']):
                file_types['config'].append(file)
            elif any(file_name.endswith(ext) for ext in ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs', '.php', '.rb']):
                file_types['source'].append(file)
            elif any(file_name.endswith(ext) for ext in ['.md', '.txt', '.rst', '.adoc']):
                file_types['docs'].append(file)
            elif any(file_name.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.css', '.scss', '.less']):
                file_types['assets'].append(file)
            else:
                file_types['other'].append(file)
            
            # Build directory structure
            if len(path_parts) == 1:
                if 'root' not in structure:
                    structure['root'] = []
                structure['root'].append(file_name)
            else:
                dir_path = '/'.join(path_parts[:-1])
                if dir_path not in structure:
                    structure[dir_path] = []
                structure[dir_path].append(path_parts[-1])
        
        lines = []
        
        # Add file type summary
        lines.append("📊 File Type Summary:")
        for file_type, file_list in file_types.items():
            if file_list:
                lines.append(f"  {file_type.title()}: {len(file_list)} files")
        lines.append("")
        
        # Add directory structure
        lines.append("📁 Directory Structure:")
        for path, files_list in sorted(structure.items()):
            if path == 'root':
                lines.append("Root Directory:")
            else:
                lines.append(f"{path}/")
            
            for file_name in sorted(files_list):
                lines.append(f"  📄 {file_name}")
            lines.append("")
        
        return '\n'.join(lines)
    
    def get_model_info(self) -> Dict:
        """Get information about the AI model being used."""
        return {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }
