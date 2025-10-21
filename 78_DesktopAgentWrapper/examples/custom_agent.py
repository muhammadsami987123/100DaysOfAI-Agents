"""
Example of creating a custom agent wrapper
"""

from typing import Dict, Any
from agents.agent_base import BaseAgent

class CustomAgentWrapper(BaseAgent):
    """Example custom agent wrapper"""
    
    def __init__(self):
        # Import your custom agent class here
        from your_module import YourCustomAgent
        
        super().__init__(
            agent_class=YourCustomAgent,
            agent_name="Custom Agent",
            description="Your custom AI agent description"
        )
    
    def get_ui_config(self) -> Dict[str, Any]:
        """Define UI configuration for your custom agent"""
        return {
            "inputs": [
                {
                    "name": "input_text",
                    "type": "textarea",
                    "label": "Input Text",
                    "placeholder": "Enter your text here...",
                    "required": True
                },
                {
                    "name": "option",
                    "type": "dropdown",
                    "label": "Option",
                    "options": [
                        {"value": "option1", "label": "Option 1"},
                        {"value": "option2", "label": "Option 2"}
                    ],
                    "default": "option1"
                }
            ],
            "outputs": [
                {
                    "name": "result",
                    "type": "text",
                    "label": "Result"
                }
            ],
            "ui_config": {
                "window_title": "Custom Agent - Desktop",
                "window_size": (1000, 700),
                "show_sidebar": True,
                "enable_export": True
            }
        }
    
    def process(self, **inputs) -> Dict[str, Any]:
        """Process inputs using your custom agent"""
        if not self.agent_instance:
            return {
                "success": False,
                "error": "Agent not initialized"
            }
        
        try:
            # Extract inputs
            input_text = inputs.get("input_text", "").strip()
            option = inputs.get("option", "option1")
            
            if not input_text:
                return {
                    "success": False,
                    "error": "No input text provided"
                }
            
            # Call your custom agent
            result = self.agent_instance.process(
                text=input_text,
                option=option
            )
            
            return {
                "success": True,
                "result": result
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Processing error: {str(e)}"
            }
    
    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        """Validate inputs for your custom agent"""
        input_text = inputs.get("input_text", "").strip()
        return len(input_text) > 0
