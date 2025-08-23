import platform
import openai
import re
from typing import Dict, Optional, List, Tuple
from rich.console import Console
from rich.text import Text

from config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    TEMPERATURE,
    MAX_TOKENS,
    MAX_HISTORY_MESSAGES,
    DANGEROUS_COMMANDS,
)


def detect_os() -> Dict[str, str]:
    system = platform.system()
    if system == "Windows":
        return {"id": "windows", "name": "Windows", "shell": "PowerShell"}
    if system == "Darwin":
        return {"id": "macos", "name": "macOS", "shell": "Bash"}
    if system == "Linux":
        return {"id": "linux", "name": "Linux", "shell": "Bash"}
    return {"id": system.lower() or "unknown", "name": system or "Unknown", "shell": "Unknown"}


class CommandExplainer:
    def __init__(self, api_key: Optional[str] = None) -> None:
        api_key_to_use = api_key or OPENAI_API_KEY
        if not api_key_to_use:
            raise ValueError("Missing OpenAI API key. Set OPENAI_API_KEY in .env.")
        
        # Initialize OpenAI client with new API format
        self.client = openai.OpenAI(api_key=api_key_to_use)
        self.model = OPENAI_MODEL
        self.temperature = TEMPERATURE
        self.max_tokens = MAX_TOKENS
        self._history: list[dict] = []
        self.console = Console()

    def _build_system_prompt(self, os_profile: Dict[str, str]) -> str:
        os_id = os_profile.get("id", "windows")
        os_name = os_profile.get("name", "Windows")
        shell = os_profile.get("shell", "PowerShell")

        return (
            f"You are an AI Command Explainer Agent, specialized in explaining terminal/shell commands. "
            f"The user is on {os_name} using {shell}. "
            f"Your role is to break down commands in a clear, educational way.\n\n"
            f"Always structure your response with these sections:\n"
            f"1) **Command Overview**: Brief description of what the command does\n"
            f"2) **Flag Breakdown**: Explain each flag/option with examples\n"
            f"3) **Arguments**: Explain the arguments and their purpose\n"
            f"4) **What Happens**: Step-by-step what the command will do\n"
            f"5) **Safety Notes**: Any warnings or safer alternatives\n"
            f"6) **Examples**: 2-3 practical examples\n\n"
            f"Be concise but thorough. Use markdown formatting. "
            f"If the command is dangerous, emphasize the risks clearly. "
            f"Always suggest safer alternatives when possible."
        )

    def _check_dangerous_command(self, command: str) -> Tuple[bool, List[str]]:
        """Check if a command contains dangerous patterns."""
        command_lower = command.lower().strip()
        dangerous_flags = []
        is_dangerous = False
        
        for dangerous in DANGEROUS_COMMANDS:
            if dangerous.lower() in command_lower:
                is_dangerous = True
                dangerous_flags.append(dangerous)
        
        # Additional pattern checks
        dangerous_patterns = [
            r'rm\s+-rf', r'del\s+/[sq]', r'rmdir\s+/[sq]',
            r'chmod\s+777', r'chown\s+root', r'sudo\s+rm',
            r':\(\)\s*\{\s*:\|\:&\s*\};:', r'fork\(\)',
            r'dd\s+if=/dev/zero', r'mkfs', r'fdisk'
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, command_lower):
                is_dangerous = True
                dangerous_flags.append(f"Pattern: {pattern}")
        
        return is_dangerous, dangerous_flags

    def _build_command_prompt(self, command: str, os_profile: Dict[str, str]) -> str:
        """Build a specific prompt for command explanation."""
        is_dangerous, dangerous_flags = self._check_dangerous_command(command)
        
        prompt = f"Please explain this command: `{command}`\n\n"
        prompt += f"Operating System: {os_profile['name']}\n"
        prompt += f"Shell: {os_profile['shell']}\n\n"
        
        if is_dangerous:
            prompt += f"⚠️  WARNING: This command appears to be dangerous! "
            prompt += f"Detected dangerous patterns: {', '.join(dangerous_flags)}\n"
            prompt += "Please emphasize the risks and provide safer alternatives.\n\n"
        
        prompt += "Please provide a comprehensive explanation following the structured format."
        return prompt

    def explain_command(self, command: str, os_profile: Optional[Dict[str, str]] = None) -> str:
        """Explain a single command."""
        os_prof = os_profile or detect_os()
        system_prompt = self._build_system_prompt(os_prof)
        command_prompt = self._build_command_prompt(command, os_prof)

        messages = [{"role": "system", "content": system_prompt}]
        if self._history:
            messages.extend(self._history[-MAX_HISTORY_MESSAGES:])
        messages.append({"role": "user", "content": command_prompt})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                messages=messages,
            )
            content = response.choices[0].message.content.strip()
            
            # Save to history
            self._history.extend([
                {"role": "user", "content": command_prompt},
                {"role": "assistant", "content": content},
            ])
            return content
        except Exception as e:
            return f"Error explaining command: {str(e)}"

    def suggest_command(self, natural_request: str, os_profile: Optional[Dict[str, str]] = None) -> str:
        """Suggest a command based on natural language request."""
        os_prof = os_profile or detect_os()
        system_prompt = (
            f"You are an AI Command Suggestion Agent for {os_prof['name']} using {os_prof['shell']}. "
            "The user will describe what they want to do in natural language. "
            "Suggest the most appropriate command with explanation.\n\n"
            "Structure your response as:\n"
            "1) **Suggested Command**: The actual command to run\n"
            "2) **What It Does**: Brief explanation\n"
            "3) **Why This Command**: Why it's the best choice\n"
            "4) **Safety Notes**: Any warnings\n"
            "5) **Alternative Options**: Other ways to achieve the same goal"
        )

        messages = [{"role": "system", "content": system_prompt}]
        if self._history:
            messages.extend(self._history[-MAX_HISTORY_MESSAGES:])
        messages.append({"role": "user", "content": f"I want to: {natural_request}"})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                messages=messages,
            )
            content = response.choices[0].message.content.strip()
            
            # Save to history
            self._history.extend([
                {"role": "user", "content": f"I want to: {natural_request}"},
                {"role": "assistant", "content": content},
            ])
            return content
        except Exception as e:
            return f"Error suggesting command: {str(e)}"

    def stream_explanation(self, command: str, os_profile: Optional[Dict[str, str]] = None):
        """Stream the explanation for better CLI experience."""
        os_prof = os_profile or detect_os()
        system_prompt = self._build_system_prompt(os_prof)
        command_prompt = self._build_command_prompt(command, os_prof)

        messages = [{"role": "system", "content": system_prompt}]
        if self._history:
            messages.extend(self._history[-MAX_HISTORY_MESSAGES:])
        messages.append({"role": "user", "content": command_prompt})

        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=True,
                messages=messages,
            )
            
            collected: list[str] = []
            for chunk in stream:
                try:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        collected.append(content)
                        yield content
                except Exception:
                    continue
            
            # Save to history at the end
            if collected:
                assistant_text = "".join(collected).strip()
                self._history.extend([
                    {"role": "user", "content": command_prompt},
                    {"role": "assistant", "content": assistant_text},
                ])
        except Exception as e:
            yield f"Error explaining command: {str(e)}"

    def get_command_summary(self, command: str) -> Dict[str, str]:
        """Get a quick summary of command components."""
        is_dangerous, dangerous_flags = self._check_dangerous_command(command)
        
        # Basic command parsing
        parts = command.strip().split()
        if not parts:
            return {"error": "Empty command"}
        
        main_command = parts[0]
        flags = [part for part in parts[1:] if part.startswith('-')]
        arguments = [part for part in parts[1:] if not part.startswith('-')]
        
        return {
            "main_command": main_command,
            "flags": flags,
            "arguments": arguments,
            "is_dangerous": is_dangerous,
            "dangerous_flags": dangerous_flags,
            "total_parts": len(parts)
        }
