from typing import Dict, Any, List, Optional
from utils.llm_service import LLMService
from config import Config
import json
import os
from datetime import datetime


class CustomPromptAgent:
    def __init__(self, llm_service: Optional[LLMService] = None):
        self.llm_service = llm_service or LLMService()
        self.templates_dir = Config.TEMPLATES_DIR
        os.makedirs(self.templates_dir, exist_ok=True)

    def build_prompt(
        self,
        role: str = "",
        task: str = "",
        output_format: str = "",
        tone: str = "",
        target_audience: str = "",
        additional_context: str = ""
    ) -> Dict[str, Any]:
        """
        Build a prompt from user inputs.
        
        Args:
            role: The role of the AI (e.g., "Marketing Copywriter", "Developer")
            task: The task to perform (e.g., "Write product description", "Generate code")
            output_format: Desired format (e.g., "Bullet points", "Paragraph", "JSON")
            tone: Tone of the output (e.g., "Friendly", "Formal", "Informative")
            target_audience: Target audience (e.g., "Startup founders", "Developers")
            additional_context: Any additional context or requirements
        
        Returns:
            Dict with the generated prompt and metadata
        """
        prompt_parts = []
        
        # Build role section
        if role:
            prompt_parts.append(f"You are a {role.lower()}.")
        
        # Build task section
        if task:
            prompt_parts.append(f"Your task is to {task.lower()}.")
        
        # Build tone section
        if tone:
            tone_descriptors = []
            for t in tone.split(","):
                t = t.strip()
                if t:
                    tone_descriptors.append(t.lower())
            if tone_descriptors:
                prompt_parts.append(f"Use a {', '.join(tone_descriptors)} tone.")
        
        # Build target audience section
        if target_audience:
            prompt_parts.append(f"Target your response to {target_audience.lower()}.")
        
        # Build output format section
        if output_format:
            prompt_parts.append(f"Format your response as {output_format.lower()}.")
        
        # Add additional context
        if additional_context:
            prompt_parts.append(f"Additional context: {additional_context}")
        
        # Combine all parts
        final_prompt = " ".join(prompt_parts)
        
        # If no parts were added, return a default prompt
        if not final_prompt.strip():
            final_prompt = "You are a helpful AI assistant. Please provide a clear and useful response."
        
        return {
            "prompt": final_prompt,
            "metadata": {
                "role": role,
                "task": task,
                "output_format": output_format,
                "tone": tone,
                "target_audience": target_audience,
                "additional_context": additional_context,
                "created_at": datetime.now().isoformat()
            }
        }

    def save_template(self, template_name: str, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Save a prompt template to disk.
        
        Args:
            template_name: Name of the template
            prompt_data: Dict containing prompt and metadata
        
        Returns:
            Dict with success status and message
        """
        try:
            # Sanitize template name
            safe_name = "".join(c for c in template_name if c.isalnum() or c in (' ', '-', '_')).strip()
            if not safe_name:
                safe_name = f"template_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            template_file = os.path.join(self.templates_dir, f"{safe_name}.json")
            
            # Add template name and timestamp
            template_data = {
                "name": safe_name,
                "prompt": prompt_data.get("prompt", ""),
                "metadata": prompt_data.get("metadata", {}),
                "saved_at": datetime.now().isoformat()
            }
            
            with open(template_file, "w", encoding="utf-8") as f:
                json.dump(template_data, f, indent=2)
            
            return {
                "success": True,
                "message": f"Template '{safe_name}' saved successfully",
                "template_name": safe_name
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error saving template: {str(e)}",
                "template_name": None
            }

    def load_template(self, template_name: str) -> Dict[str, Any]:
        """
        Load a prompt template from disk.
        
        Args:
            template_name: Name of the template to load
        
        Returns:
            Dict with template data or error message
        """
        try:
            template_file = os.path.join(self.templates_dir, f"{template_name}.json")
            
            if not os.path.exists(template_file):
                return {
                    "success": False,
                    "message": f"Template '{template_name}' not found"
                }
            
            with open(template_file, "r", encoding="utf-8") as f:
                template_data = json.load(f)
            
            return {
                "success": True,
                "template": template_data
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error loading template: {str(e)}"
            }

    def list_templates(self) -> List[Dict[str, Any]]:
        """
        List all saved templates.
        
        Returns:
            List of template metadata dicts
        """
        templates = []
        try:
            if not os.path.exists(self.templates_dir):
                return templates
            
            for filename in os.listdir(self.templates_dir):
                if filename.endswith(".json"):
                    template_name = filename[:-5]  # Remove .json extension
                    template_data = self.load_template(template_name)
                    if template_data.get("success"):
                        templates.append({
                            "name": template_name,
                            "metadata": template_data["template"].get("metadata", {}),
                            "saved_at": template_data["template"].get("saved_at", "")
                        })
        except Exception as e:
            print(f"Error listing templates: {e}")
        
        return templates

    def delete_template(self, template_name: str) -> Dict[str, Any]:
        """
        Delete a saved template.
        
        Args:
            template_name: Name of the template to delete
        
        Returns:
            Dict with success status and message
        """
        try:
            template_file = os.path.join(self.templates_dir, f"{template_name}.json")
            
            if not os.path.exists(template_file):
                return {
                    "success": False,
                    "message": f"Template '{template_name}' not found"
                }
            
            os.remove(template_file)
            
            return {
                "success": True,
                "message": f"Template '{template_name}' deleted successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error deleting template: {str(e)}"
            }

    def enhance_prompt(self, base_prompt: str, enhancement_type: str = "general") -> Dict[str, Any]:
        """
        Use LLM to enhance a prompt with better structure and clarity.
        
        Args:
            base_prompt: The base prompt to enhance
            enhancement_type: Type of enhancement (general, technical, creative, etc.)
        
        Returns:
            Dict with enhanced prompt
        """
        if not base_prompt or not base_prompt.strip():
            return {
                "success": False,
                "error": "Base prompt cannot be empty",
                "enhanced_prompt": base_prompt
            }
        
        enhancement_instructions = {
            "general": "Make it clear, concise, and effective",
            "technical": "Focus on precision, technical accuracy, and detailed specifications",
            "creative": "Add creative flourishes, storytelling elements, and engaging language",
            "strategic": "Emphasize business value, strategic thinking, and measurable outcomes",
            "educational": "Add learning objectives, structured guidance, and explanatory elements"
        }
        
        enhancement_focus = enhancement_instructions.get(enhancement_type, enhancement_instructions["general"])
        
        enhancement_prompt = f"""You are an expert AI prompt engineer. Your task is to improve the following prompt to make it more effective for AI models like GPT and Gemini.

Enhancement focus: {enhancement_focus}

Original prompt:
"{base_prompt}"

Please provide an improved version that:
1. Is more specific and actionable
2. Has clear instructions and expected outcomes
3. Includes appropriate context
4. Defines the output format

Return ONLY the improved prompt text, without any introduction or commentary."""

        try:
            result = self.llm_service.generate_content(enhancement_prompt)
            
            # Handle different response formats
            enhanced = result.get("summary") or result.get("message") or ""
            
            # If still empty, use original
            if not enhanced:
                enhanced = base_prompt
            
            return {
                "success": True,
                "original_prompt": base_prompt,
                "enhanced_prompt": enhanced.strip()
            }
        except Exception as e:
            print(f"Enhancement error: {e}")
            return {
                "success": False,
                "error": f"Enhancement failed: {str(e)}",
                "original_prompt": base_prompt,
                "enhanced_prompt": base_prompt
            }

