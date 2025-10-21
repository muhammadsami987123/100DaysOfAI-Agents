"""
PromptImprover agent wrapper for DesktopAgentWrapper
"""

import sys
import os
from typing import Dict, Any
from .agent_base import BaseAgent

# Add the PromptImprover path to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '72_PromptImproverAgent'))

try:
    from agent import PromptImproverAgent
except ImportError:
    # Fallback if PromptImprover is not available
    from .mock_agent import MockPromptImproverAgent
    PromptImproverAgent = MockPromptImproverAgent

class PromptImproverWrapper(BaseAgent):
    """Wrapper for PromptImprover agent"""
    
    def __init__(self):
        super().__init__(
            agent_class=PromptImproverAgent,
            agent_name="PromptImprover",
            description="AI-powered prompt optimization and enhancement tool"
        )
        
        # Available tones for prompt improvement
        self.tones = {
            "professional": {"name": "Professional", "description": "Formal and business-appropriate"},
            "casual": {"name": "Casual", "description": "Conversational and friendly"},
            "technical": {"name": "Technical", "description": "Precise and detailed"},
            "creative": {"name": "Creative", "description": "Imaginative and expressive"},
            "persuasive": {"name": "Persuasive", "description": "Convincing and compelling"},
            "educational": {"name": "Educational", "description": "Clear and instructional"}
        }
    
    def get_ui_config(self) -> Dict[str, Any]:
        """Get UI configuration for PromptImprover"""
        return {
            "inputs": [
                {
                    "name": "raw_prompt",
                    "type": "textarea",
                    "label": "Original Prompt",
                    "placeholder": "Enter your original prompt here...",
                    "required": True
                },
                {
                    "name": "tone",
                    "type": "dropdown",
                    "label": "Improvement Tone",
                    "options": [{"value": key, "label": config["name"]} for key, config in self.tones.items()],
                    "default": "professional"
                }
            ],
            "outputs": [
                {
                    "name": "improved_prompt",
                    "type": "text",
                    "label": "Improved Prompt"
                },
                {
                    "name": "suggestions",
                    "type": "list",
                    "label": "Improvement Suggestions"
                }
            ],
            "ui_config": {
                "window_title": "PromptImprover - Desktop",
                "window_size": (1200, 800),
                "show_sidebar": True,
                "enable_export": True
            }
        }
    
    def process(self, **inputs) -> Dict[str, Any]:
        """Process prompt improvement"""
        if not self.agent_instance:
            return {
                "success": False,
                "error": "Agent not initialized"
            }
        
        try:
            # Validate inputs
            if not self.validate_inputs(inputs):
                return {
                    "success": False,
                    "error": "Invalid inputs"
                }
            
            # Extract parameters
            raw_prompt = inputs.get("raw_prompt", "").strip()
            tone = inputs.get("tone", "professional")
            
            if not raw_prompt:
                return {
                    "success": False,
                    "error": "No prompt provided for improvement"
                }
            
            # Call the agent
            result = self.agent_instance.improve_prompt(
                raw_prompt=raw_prompt,
                tone=tone
            )
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Processing error: {str(e)}"
            }
    
    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        """Validate PromptImprover inputs"""
        raw_prompt = inputs.get("raw_prompt", "").strip()
        tone = inputs.get("tone", "")
        
        if not raw_prompt:
            return False
        
        if tone not in self.tones:
            return False
        
        return True
    
    def format_output(self, result: Any) -> str:
        """Format PromptImprover output"""
        if isinstance(result, dict):
            if result.get("success", True):
                improved_prompt = result.get("improved_prompt", "")
                suggestions = result.get("suggestions", [])
                
                output = f"# Improved Prompt\n\n"
                output += f"{improved_prompt}\n\n"
                
                if suggestions:
                    output += "## Improvement Suggestions\n\n"
                    for i, suggestion in enumerate(suggestions, 1):
                        output += f"{i}. {suggestion}\n"
                
                return output
            else:
                return f"Error: {result.get('error', 'Unknown error')}"
        
        return str(result)
