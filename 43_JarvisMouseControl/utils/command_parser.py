"""
Command parser for JarvisMouseControl
Handles natural language processing and command recognition in multiple languages
"""

import json
import re
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import openai
from config import CONFIG, get_api_key

class CommandParser:
    """Parses voice and text commands into mouse actions"""
    
    def __init__(self, language: str = "en"):
        """Initialize command parser with specified language"""
        self.language = language
        self.translations = self._load_translations()
        self.api_key = get_api_key()
        
        # Initialize OpenAI client if API key is available
        if self.api_key:
            openai.api_key = self.api_key
    
    def _load_translations(self) -> Dict[str, Any]:
        """Load translations from JSON file"""
        try:
            with open(CONFIG.TRANSLATIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️  Translations file not found: {CONFIG.TRANSLATIONS_FILE}")
            return {}
        except json.JSONDecodeError as e:
            print(f"⚠️  Error loading translations: {e}")
            return {}
    
    def parse_command(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Parse a command text into mouse action
        
        Args:
            text: The command text to parse
            
        Returns:
            Dictionary with action details or None if not recognized
        """
        if not text or not text.strip():
            return None
        
        text = text.strip().lower()
        
        # Try local pattern matching first
        local_result = self._parse_local_patterns(text)
        if local_result:
            return local_result
        
        # Try OpenAI parsing if available
        if self.api_key:
            openai_result = self._parse_with_openai(text)
            if openai_result:
                return openai_result
        
        return None
    
    def _parse_local_patterns(self, text: str) -> Optional[Dict[str, Any]]:
        """Parse command using local pattern matching"""
        commands = self.translations.get("commands", {})
        
        # Check each command type
        for action, languages in commands.items():
            if self.language in languages:
                patterns = languages[self.language]
                for pattern in patterns:
                    if self._text_matches_pattern(text, pattern):
                        return self._create_action_dict(action, text)
        
        return None
    
    def _text_matches_pattern(self, text: str, pattern: str) -> bool:
        """Check if text matches a command pattern"""
        # Simple word-based matching
        text_words = set(text.split())
        pattern_words = set(pattern.split())
        
        # Check if all pattern words are in text
        return pattern_words.issubset(text_words)
    
    def _create_action_dict(self, action: str, original_text: str) -> Dict[str, Any]:
        """Create action dictionary from parsed command"""
        # Extract modifiers (small, medium, large)
        distance = self._extract_distance_modifier(original_text)
        
        return {
            "action": action,
            "original_text": original_text,
            "distance": distance,
            "confidence": 0.9,  # High confidence for pattern matching
            "method": "pattern"
        }
    
    def _extract_distance_modifier(self, text: str) -> str:
        """Extract distance modifier from text"""
        modifiers = self.translations.get("modifiers", {})
        
        for modifier, languages in modifiers.items():
            if self.language in languages:
                patterns = languages[self.language]
                for pattern in patterns:
                    if pattern in text:
                        return modifier
        
        return "medium"  # Default distance
    
    def _parse_with_openai(self, text: str) -> Optional[Dict[str, Any]]:
        """Parse command using OpenAI for better understanding"""
        try:
            prompt = self._create_openai_prompt(text)
            
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=CONFIG.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": prompt["system"]},
                    {"role": "user", "content": prompt["user"]}
                ],
                max_tokens=CONFIG.OPENAI_MAX_TOKENS,
                temperature=CONFIG.OPENAI_TEMPERATURE
            )
            
            result_text = response.choices[0].message.content.strip()
            return self._parse_openai_response(result_text, text)
            
        except Exception as e:
            print(f"⚠️  OpenAI parsing error: {e}")
            return None
    
    def _create_openai_prompt(self, text: str) -> Dict[str, str]:
        """Create OpenAI prompt for command parsing"""
        language_name = CONFIG.LANGUAGE_NAMES.get(self.language, "English")
        
        system_prompt = f"""You are a voice command interpreter for a mouse control system. 
        The user is speaking in {language_name} and wants to control their computer mouse.
        
        Available actions:
        - move_up: Move mouse cursor up
        - move_down: Move mouse cursor down  
        - move_left: Move mouse cursor left
        - move_right: Move mouse cursor right
        - click: Left click
        - double_click: Double click
        - right_click: Right click
        - scroll_up: Scroll up
        - scroll_down: Scroll down
        - drag: Drag and drop
        - stop: Stop/quit the system
        
        Distance modifiers:
        - small: Small movement (50px)
        - medium: Medium movement (100px) 
        - large: Large movement (200px)
        
        Respond with JSON format:
        {{"action": "action_name", "distance": "small|medium|large", "confidence": 0.0-1.0}}"""
        
        user_prompt = f"Parse this {language_name} command: '{text}'"
        
        return {
            "system": system_prompt,
            "user": user_prompt
        }
    
    def _parse_openai_response(self, response: str, original_text: str) -> Optional[Dict[str, Any]]:
        """Parse OpenAI response into action dictionary"""
        try:
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                
                # Validate action
                valid_actions = list(CONFIG.MOUSE_ACTIONS.keys())
                if result.get("action") in valid_actions:
                    return {
                        "action": result["action"],
                        "original_text": original_text,
                        "distance": result.get("distance", "medium"),
                        "confidence": result.get("confidence", 0.8),
                        "method": "openai"
                    }
        except (json.JSONDecodeError, KeyError) as e:
            print(f"⚠️  Error parsing OpenAI response: {e}")
        
        return None
    
    def get_feedback_message(self, message_key: str, **kwargs) -> str:
        """Get localized feedback message"""
        feedback = self.translations.get("feedback", {})
        language_feedback = feedback.get(self.language, feedback.get("en", {}))
        
        message = language_feedback.get(message_key, f"Message not found: {message_key}")
        
        # Format message with kwargs
        try:
            return message.format(**kwargs)
        except KeyError:
            return message
    
    def set_language(self, language: str):
        """Change the parser language"""
        if language in CONFIG.SUPPORTED_LANGUAGES:
            self.language = language
            return True
        return False
    
    def get_supported_commands(self) -> List[str]:
        """Get list of supported commands for current language"""
        commands = self.translations.get("commands", {})
        language_commands = []
        
        for action, languages in commands.items():
            if self.language in languages:
                language_commands.extend(languages[self.language])
        
        return language_commands
    
    def get_help_text(self) -> str:
        """Get help text for current language"""
        return self.get_feedback_message("help")
    
    def is_stop_command(self, text: str) -> bool:
        """Check if text is a stop command"""
        stop_commands = self.translations.get("commands", {}).get("stop", {})
        if self.language in stop_commands:
            patterns = stop_commands[self.language]
            for pattern in patterns:
                if self._text_matches_pattern(text.lower(), pattern):
                    return True
        return False
