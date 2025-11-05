from typing import Dict, Any, Optional, List
from utils.llm_service import LLMService
from config import Config
import os
import json
import shutil
from pathlib import Path


class AIProjectStarterAgent:
    def __init__(self, llm_service: Optional[LLMService] = None):
        self.llm_service = llm_service or LLMService()

    def generate_project_structure(
        self,
        project_name: str,
        project_type: str,
        llm_preference: str = "gemini",
        features: List[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a complete project structure based on user parameters.
        
        Args:
            project_name: Name of the project
            project_type: Type of project (chatbot, cli, api, web_app, etc.)
            llm_preference: Preferred LLM (gemini or openai)
            features: List of optional features (logging, file_storage, frontend, etc.)
        
        Returns:
            Dict with project structure details and file contents
        """
        features = features or []
        
        # Normalize project name for folder/file names
        folder_name = project_name.lower().replace(" ", "_").replace("-", "_")
        
        # Generate project structure
        structure = self._generate_folder_structure(project_type, features)
        
        # Generate boilerplate code
        boilerplate = self._generate_boilerplate_code(
            project_name, folder_name, project_type, llm_preference, features
        )
        
        # Generate README
        readme_content = self._generate_readme(
            project_name, project_type, llm_preference, features
        )
        
        # Generate .env template
        env_template = self._generate_env_template(llm_preference)
        
        # Generate .gitignore
        gitignore_content = self._generate_gitignore()
        
        return {
            "project_name": project_name,
            "folder_name": folder_name,
            "structure": structure,
            "boilerplate": boilerplate,
            "readme": readme_content,
            "env_template": env_template,
            "gitignore": gitignore_content,
            "requirements": self._generate_requirements(project_type, features)
        }

    def _generate_folder_structure(self, project_type: str, features: List[str]) -> Dict[str, Any]:
        """Generate folder structure based on project type and features."""
        base_structure = {
            "": ["main.py", "config.py", "requirements.txt", "README.md", ".env", ".gitignore"]
        }
        
        # Add utils folder (standard for all projects)
        base_structure["utils"] = ["__init__.py", "llm_service.py"]
        
        # Add prompts folder (standard for all projects)
        base_structure["prompts"] = []
        
        # Project type specific folders
        if project_type in ["web_app", "api", "chatbot"]:
            base_structure["templates"] = []
            base_structure["static"] = []
            if "file_storage" in features or "file_upload" in features:
                base_structure["uploads"] = []
        
        if project_type == "cli":
            base_structure["cli"] = []
        
        # Feature specific folders
        if "logging" in features:
            base_structure["logs"] = []
        
        if "file_storage" in features or "json_storage" in features:
            if "storage" not in base_structure:
                base_structure["storage"] = []
        
        return base_structure

    def _generate_boilerplate_code(
        self,
        project_name: str,
        folder_name: str,
        project_type: str,
        llm_preference: str,
        features: List[str]
    ) -> Dict[str, str]:
        """Generate boilerplate code files."""
        boilerplate = {}
        
        # Generate config.py
        boilerplate["config.py"] = self._generate_config_py(llm_preference)
        
        # Generate main.py
        boilerplate["main.py"] = self._generate_main_py(project_name, project_type)
        
        # Generate agent.py
        boilerplate["agent.py"] = self._generate_agent_py(project_name, folder_name)
        
        # Generate web_app.py if needed
        if project_type in ["web_app", "api", "chatbot"]:
            boilerplate["web_app.py"] = self._generate_web_app_py(project_name)
        
        # Generate utils/llm_service.py
        boilerplate["utils/llm_service.py"] = self._get_llm_service_template()
        
        # Generate utils/__init__.py
        boilerplate["utils/__init__.py"] = ""
        
        # Generate prompt template
        boilerplate["prompts/main_prompt.txt"] = self._generate_main_prompt_template()
        
        return boilerplate

    def _generate_config_py(self, llm_preference: str) -> str:
        """Generate config.py content."""
        return f'''import os
from dotenv import load_dotenv

load_dotenv()


def _strip(val: str | None) -> str | None:
    if val is None:
        return None
    # Remove surrounding whitespace and surrounding quotes if present
    v = val.strip()
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        v = v[1:-1]
    return v


class Config:
    GEMINI_API_KEY = _strip(os.getenv("GEMINI_API_KEY"))
    OPENAI_API_KEY = _strip(os.getenv("OPENAI_API_KEY"))
    DEFAULT_LLM = _strip(os.getenv("DEFAULT_LLM", "{llm_preference}"))
    GEMINI_MODEL = _strip(os.getenv("GEMINI_MODEL", "gemini-2.0-flash"))
    OPENAI_MODEL = _strip(os.getenv("OPENAI_MODEL", "gpt-4.1"))
    UPLOAD_DIR = _strip(os.getenv("UPLOAD_DIR", "./uploads"))
'''

    def _generate_main_py(self, project_name: str, project_type: str) -> str:
        """Generate main.py based on project type."""
        if project_type in ["web_app", "api", "chatbot"]:
            return '''import uvicorn
from web_app import app
from config import Config
import os

if __name__ == '__main__':
    # Ensure required directories exist
    os.makedirs(Config.UPLOAD_DIR, exist_ok=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
        elif project_type == "cli":
            class_name = "".join(word.capitalize() for word in project_name.replace("-", "_").replace(" ", "_").split("_")) + "Agent"
            return f'''from agent import {class_name}
from config import Config
from utils.llm_service import LLMService

if __name__ == '__main__':
    agent = {class_name}(llm_service=LLMService())
    # Add your CLI logic here
    print("CLI Agent started!")
'''
        else:
            class_name = "".join(word.capitalize() for word in project_name.replace("-", "_").replace(" ", "_").split("_")) + "Agent"
            return f'''from agent import {class_name}
from config import Config

if __name__ == '__main__':
    agent = {class_name}()
    # Add your main logic here
    print("Agent started!")
'''

    def _generate_agent_py(self, project_name: str, folder_name: str) -> str:
        """Generate agent.py content."""
        class_name = "".join(word.capitalize() for word in project_name.replace("-", "_").replace(" ", "_").split("_")) + "Agent"
        
        return f'''from typing import Dict, Any, Optional
from utils.llm_service import LLMService


class {class_name}:
    def __init__(self, llm_service: Optional[LLMService] = None):
        self.llm_service = llm_service or LLMService()

    def process(self, user_input: str) -> Dict[str, Any]:
        """Main processing method - customize based on your needs."""
        prompt_template = self.llm_service._read_template("main_prompt.txt")
        formatted_prompt = prompt_template.replace("{{user_input}}", user_input)
        
        result = self.llm_service.generate_content(formatted_prompt)
        return result
'''

    def _generate_web_app_py(self, project_name: str) -> str:
        """Generate web_app.py for FastAPI."""
        class_name = "".join(word.capitalize() for word in project_name.replace("-", "_").replace(" ", "_").split("_")) + "Agent"
        
        return f'''from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from agent import {class_name}
from config import Config
from utils.llm_service import LLMService

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

agent = {class_name}(llm_service=LLMService())


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html", {{"request": request, "default_llm": Config.DEFAULT_LLM}}
    )


@app.post("/process", response_class=HTMLResponse)
async def process_route(
    request: Request,
    user_input: str = Form(...),
    llm_choice: str = Form(Config.DEFAULT_LLM),
):
    error_message = None
    result = None
    
    try:
        agent.llm_service.set_llm(llm_choice)
        result = agent.process(user_input)
    except Exception as e:
        error_message = str(e)
        result = {{"summary": "", "message": ""}}

    return templates.TemplateResponse(
        "index.html",
        {{
            "request": request,
            "result": result,
            "error_message": error_message,
            "default_llm": Config.DEFAULT_LLM,
            "selected_llm": llm_choice,
        }},
    )
'''

    def _get_llm_service_template(self) -> str:
        """Return the LLM service template (same as our utils/llm_service.py)."""
        # Read from our own llm_service.py
        service_path = os.path.join(os.path.dirname(__file__), "..", "utils", "llm_service.py")
        try:
            with open(service_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            # Fallback template
            return '''import os
import json
from typing import Dict, Any
from config import Config

try:
    import google.generativeai as genai
    HAS_GENAI = True
except Exception:
    genai = None
    HAS_GENAI = False

try:
    from openai import OpenAI
    HAS_OPENAI = True
except Exception:
    OpenAI = None
    HAS_OPENAI = False


class LLMService:
    """Simple LLM wrapper that attempts to use Gemini by default and OpenAI as optional."""
    
    def __init__(self):
        self.current_llm = Config.DEFAULT_LLM
        self.gemini_client = None
        self.openai_client = None
        self._init_clients()

    def _init_clients(self):
        if HAS_GENAI and Config.GEMINI_API_KEY:
            try:
                genai.configure(api_key=Config.GEMINI_API_KEY)
                self.gemini_client = genai.GenerativeModel(Config.GEMINI_MODEL)
            except Exception as e:
                print(f"Failed to initialize Gemini client: {e}")
                self.gemini_client = None

        if HAS_OPENAI and Config.OPENAI_API_KEY:
            try:
                self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
            except Exception as e:
                print(f"Failed to initialize OpenAI client: {e}")
                self.openai_client = None

    def set_llm(self, llm_choice: str) -> None:
        if llm_choice in ("gemini", "openai"):
            self.current_llm = llm_choice

    def _read_template(self, template_name: str) -> str:
        template_path = os.path.join(os.path.dirname(__file__), "..", "prompts", template_name)
        try:
            with open(template_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""

    def generate_content(self, prompt: str) -> Dict[str, Any]:
        try:
            if self.current_llm == "gemini" and self.gemini_client:
                response = self.gemini_client.generate_content(prompt)
                text = getattr(response, "text", str(response))
                return self._parse_text_response(text)

            if self.current_llm == "openai" and self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model=Config.OPENAI_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                )
                text = response.choices[0].message.content
                return self._parse_text_response(text)

            return {"summary": "", "message": "No LLM configured"}

        except Exception as e:
            return {"summary": f"Error: {e}", "message": ""}

    def _parse_text_response(self, text: str) -> Dict[str, Any]:
        cleaned = text.strip()
        try:
            start = cleaned.find("{")
            end = cleaned.rfind("}")
            if start != -1 and end != -1 and end > start:
                json_text = cleaned[start:end+1]
                parsed = json.loads(json_text)
                return parsed
        except Exception:
            pass
        return {"summary": cleaned, "message": ""}
'''

    def _generate_main_prompt_template(self) -> str:
        """Generate a basic prompt template."""
        return '''You are a helpful AI assistant. Process the following user input:

{{user_input}}

Provide a helpful and accurate response.
'''

    def _generate_readme(
        self,
        project_name: str,
        project_type: str,
        llm_preference: str,
        features: List[str]
    ) -> str:
        """Generate README.md content."""
        features_list = "\n".join([f"- ✅ {f}" for f in features]) if features else "- ✅ Basic functionality"
        
        return f'''# {project_name}

## Overview

This is a GPT-based {project_type} project scaffolded by AIProjectStarter.

## Features

{features_list}

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your API keys:
```
GEMINI_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key
DEFAULT_LLM={llm_preference}
```

3. Run the project:
```bash
python main.py
```

## Project Structure

- `agent.py` - Main agent logic
- `config.py` - Configuration settings
- `main.py` - Entry point
- `utils/` - Utility functions including LLM service
- `prompts/` - Prompt templates
'''

    def _generate_env_template(self, llm_preference: str) -> str:
        """Generate .env template."""
        return f'''# LLM API Keys
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# LLM Configuration
DEFAULT_LLM={llm_preference}
GEMINI_MODEL=gemini-2.0-flash
OPENAI_MODEL=gpt-4.1

# Other Settings
UPLOAD_DIR=./uploads
'''

    def _generate_gitignore(self) -> str:
        """Generate .gitignore content."""
        return '''# Environment variables
.env

# Python bytecode
__pycache__/
*.pyc
*.pyo

# Virtual environment
venv/
env/

# Uploads directory
uploads/

# Logs
logs/
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
'''

    def _generate_requirements(self, project_type: str, features: List[str]) -> str:
        """Generate requirements.txt based on project type and features."""
        base_requirements = [
            "fastapi",
            "uvicorn[standard]",
            "jinja2",
            "python-dotenv",
            "google-generativeai",
            "openai"
        ]
        
        if project_type in ["web_app", "api"]:
            base_requirements.append("python-multipart")
        
        if "file_upload" in features:
            base_requirements.append("aiofiles")
        
        return "\n".join(base_requirements)

    def scaffold_project(
        self,
        project_name: str,
        project_type: str,
        llm_preference: str = "gemini",
        features: List[str] = None,
        output_dir: str = None
    ) -> Dict[str, Any]:
        """
        Actually create the project files on disk.
        
        Args:
            project_name: Name of the project
            project_type: Type of project
            llm_preference: Preferred LLM
            features: List of optional features
            output_dir: Directory where to create the project (default: Downloads folder)
        
        Returns:
            Dict with success status and project path
        """
        features = features or []
        output_dir = output_dir or Config.DEFAULT_OUTPUT_DIR
        
        # Generate project structure
        project_data = self.generate_project_structure(
            project_name, project_type, llm_preference, features
        )
        
        folder_name = project_data["folder_name"]
        project_path = os.path.join(output_dir, folder_name)
        
        try:
            # Create project directory
            os.makedirs(project_path, exist_ok=True)
            
            # Create folder structure
            for folder, files in project_data["structure"].items():
                folder_path = os.path.join(project_path, folder) if folder else project_path
                os.makedirs(folder_path, exist_ok=True)
                
                # Create empty files for folders
                if not files:
                    # Create __init__.py for empty Python packages
                    if folder in ["utils", "cli"]:
                        init_file = os.path.join(folder_path, "__init__.py")
                        with open(init_file, "w", encoding="utf-8") as f:
                            f.write("")
            
            # Write boilerplate files
            for file_path, content in project_data["boilerplate"].items():
                full_path = os.path.join(project_path, file_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(content)
            
            # Write README
            readme_path = os.path.join(project_path, "README.md")
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(project_data["readme"])
            
            # Write .env template
            env_path = os.path.join(project_path, ".env.example")
            with open(env_path, "w", encoding="utf-8") as f:
                f.write(project_data["env_template"])
            
            # Write .gitignore
            gitignore_path = os.path.join(project_path, ".gitignore")
            with open(gitignore_path, "w", encoding="utf-8") as f:
                f.write(project_data["gitignore"])
            
            # Write requirements.txt
            requirements_path = os.path.join(project_path, "requirements.txt")
            with open(requirements_path, "w", encoding="utf-8") as f:
                f.write(project_data["requirements"])
            
            return {
                "success": True,
                "project_path": project_path,
                "message": f"Project '{project_name}' successfully created at {project_path}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to create project: {str(e)}"
            }

