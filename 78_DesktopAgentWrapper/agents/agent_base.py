"""
Base agent wrapper class for DesktopAgentWrapper
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Base class for all agent wrappers"""
    
    def __init__(self, agent_class, agent_name: str, description: str = ""):
        """
        Initialize the base agent wrapper
        
        Args:
            agent_class: The original agent class
            agent_name: Display name for the agent
            description: Description of the agent
        """
        self.agent_class = agent_class
        self.agent_name = agent_name
        self.description = description
        self.agent_instance = None
        
    def initialize(self) -> bool:
        """Initialize the agent instance"""
        try:
            self.agent_instance = self.agent_class()
            logger.info(f"Initialized agent: {self.agent_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize agent {self.agent_name}: {e}")
            return False
    
    @abstractmethod
    def get_ui_config(self) -> Dict[str, Any]:
        """
        Get UI configuration for the agent
        
        Returns:
            Dictionary containing UI configuration
        """
        pass
    
    @abstractmethod
    def process(self, **inputs) -> Dict[str, Any]:
        """
        Process inputs using the agent
        
        Args:
            **inputs: Input parameters
            
        Returns:
            Dictionary containing processing results
        """
        pass
    
    def get_agent_info(self) -> Dict[str, str]:
        """Get agent information"""
        return {
            "name": self.agent_name,
            "description": self.description,
            "class": self.agent_class.__name__
        }
    
    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        """
        Validate input parameters
        
        Args:
            inputs: Input parameters to validate
            
        Returns:
            True if inputs are valid, False otherwise
        """
        return True
    
    def format_output(self, result: Any) -> str:
        """
        Format the output for display
        
        Args:
            result: Raw result from agent
            
        Returns:
            Formatted string for display
        """
        if isinstance(result, dict):
            if result.get("success", True):
                return result.get("result", result.get("rewritten_content", str(result)))
            else:
                return f"Error: {result.get('error', 'Unknown error')}"
        return str(result)
