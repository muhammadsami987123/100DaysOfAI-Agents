import os
import json
from typing import Dict, Any, Optional, List
from utils.llm_service import LLMService
from config import Config

class GPTConfigGenerator:
    """Main GPTConfigGenerator agent class for generating configuration files"""
    
    def __init__(self, llm_service: Optional[LLMService] = None):
        self.llm_service = llm_service or LLMService()
        self.config = Config()
        
    def generate_config(self, user_request: str, config_type: str = "auto", format: str = "json") -> Dict[str, Any]:
        """
        Generate a configuration file based on user request
        
        Args:
            user_request: Natural language description of desired config
            config_type: Type of configuration (app_settings, devops, etc.)
            format: Output format (json, yaml, toml, js, ts)
            
        Returns:
            Dictionary containing generated config and metadata
        """
        # Detect format from request if not specified
        if format == "auto":
            format = self._detect_format(user_request)
        
        # Detect config type from request if not specified
        if config_type == "auto":
            config_type = self._detect_config_type(user_request)
        
        # Generate the configuration
        result = self.llm_service.generate_config(user_request, config_type, format)
        
        # Add additional metadata
        result["detected_format"] = format
        result["detected_type"] = config_type
        
        return result
    
    def explain_config(self, config_content: str, format: str) -> Dict[str, Any]:
        """
        Explain a configuration file in natural language
        
        Args:
            config_content: The configuration file content
            format: Format of the configuration (json, yaml, etc.)
            
        Returns:
            Dictionary containing explanation
        """
        return self.llm_service.explain_config(config_content, format)
    
    def convert_config(self, config_content: str, from_format: str, to_format: str) -> Dict[str, Any]:
        """
        Convert configuration between different formats
        
        Args:
            config_content: Original configuration content
            from_format: Source format
            to_format: Target format
            
        Returns:
            Dictionary containing converted configuration
        """
        try:
            # Parse the original configuration
            parsed_config = self._parse_config(config_content, from_format)
            
            # Convert to target format
            converted_content = self._serialize_config(parsed_config, to_format)
            
            return {
                "success": True,
                "original_format": from_format,
                "target_format": to_format,
                "converted_content": converted_content
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to convert configuration: {str(e)}",
                "original_format": from_format,
                "target_format": to_format
            }
    
    def validate_config(self, config_content: str, format: str) -> Dict[str, Any]:
        """
        Validate a configuration file
        
        Args:
            config_content: Configuration content to validate
            format: Format of the configuration
            
        Returns:
            Dictionary containing validation results
        """
        try:
            parsed_config = self._parse_config(config_content, format)
            
            return {
                "success": True,
                "valid": True,
                "format": format,
                "parsed_config": parsed_config
            }
            
        except Exception as e:
            return {
                "success": True,
                "valid": False,
                "format": format,
                "error": str(e)
            }
    
    def get_suggestions(self, config_type: str, format: str) -> List[str]:
        """
        Get configuration suggestions for a given type and format
        
        Args:
            config_type: Type of configuration
            format: Format of the configuration
            
        Returns:
            List of suggestion strings
        """
        suggestions = []
        
        if config_type in self.config.CONFIG_TYPES:
            config_info = self.config.CONFIG_TYPES[config_type]
            suggestions.append(f"Generate a {format.upper()} configuration for {config_info['name']}")
            
            for example in config_info['examples']:
                suggestions.append(f"Create a {format.upper()} config for {example}")
        
        return suggestions
    
    def _detect_format(self, user_request: str) -> str:
        """Detect the desired format from user request"""
        request_lower = user_request.lower()
        
        if any(word in request_lower for word in ["yaml", "yml"]):
            return "yaml"
        elif any(word in request_lower for word in ["toml"]):
            return "toml"
        elif any(word in request_lower for word in ["typescript", "ts"]):
            return "ts"
        elif any(word in request_lower for word in ["javascript", "js"]):
            return "js"
        else:
            return "json"  # Default to JSON
    
    def _detect_config_type(self, user_request: str) -> str:
        """Detect the configuration type from user request"""
        request_lower = user_request.lower()
        
        # Check for specific config types
        if any(word in request_lower for word in ["docker", "compose", "kubernetes", "k8s"]):
            return "devops"
        elif any(word in request_lower for word in ["eslint", "prettier", "stylelint", "black", "pylint"]):
            return "linting"
        elif any(word in request_lower for word in ["vite", "webpack", "babel", "rollup", "parcel"]):
            return "build_tools"
        elif any(word in request_lower for word in ["package.json", "pyproject.toml", "composer.json"]):
            return "package_managers"
        elif any(word in request_lower for word in ["postgresql", "mongodb", "redis", "mysql", "database"]):
            return "database"
        elif any(word in request_lower for word in ["express", "django", "flask", "react", "vue", "node"]):
            return "app_settings"
        else:
            return "custom"
    
    def _parse_config(self, content: str, format: str) -> Dict[str, Any]:
        """Parse configuration content based on format"""
        if format.lower() == "json":
            return json.loads(content)
        elif format.lower() == "yaml":
            import yaml
            return yaml.safe_load(content)
        elif format.lower() == "toml":
            import toml
            return toml.loads(content)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _serialize_config(self, config: Dict[str, Any], format: str) -> str:
        """Serialize configuration to specified format"""
        if format.lower() == "json":
            return json.dumps(config, indent=2)
        elif format.lower() == "yaml":
            import yaml
            return yaml.dump(config, default_flow_style=False, indent=2)
        elif format.lower() == "toml":
            import toml
            return toml.dumps(config)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported configuration formats"""
        return self.config.SUPPORTED_FORMATS
    
    def get_config_types(self) -> Dict[str, Dict[str, str]]:
        """Get available configuration types"""
        return self.config.CONFIG_TYPES
    
    def get_default_values(self) -> Dict[str, str]:
        """Get default configuration values"""
        return self.config.DEFAULT_VALUES
