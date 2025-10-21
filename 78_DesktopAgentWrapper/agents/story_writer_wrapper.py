"""
StoryWriter agent wrapper for DesktopAgentWrapper
"""

import sys
import os
from typing import Dict, Any
from .agent_base import BaseAgent

# Add the StoryWriter path to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '36_StoryWriterAgent'))

try:
    from story_agent import StoryAgent
    from config import StoryConfig
except ImportError:
    # Fallback if StoryWriter is not available
    from .mock_agent import MockStoryWriterAgent
    StoryAgent = MockStoryWriterAgent
    StoryConfig = None

class StoryWriterWrapper(BaseAgent):
    """Wrapper for StoryWriter agent"""
    
    def __init__(self):
        super().__init__(
            agent_class=StoryAgent,
            agent_name="StoryWriter",
            description="AI-powered creative story generation tool"
        )
        
        # Initialize configuration
        if StoryConfig:
            self.genres = StoryConfig.GENRES
            self.tones = StoryConfig.TONES
            self.lengths = StoryConfig.LENGTHS
            self.languages = StoryConfig.LANGUAGES
        else:
            # Fallback configuration
            self.genres = {
                "fantasy": {"name": "Fantasy", "description": "Magical worlds and mythical creatures"},
                "sci-fi": {"name": "Science Fiction", "description": "Futuristic technology and space exploration"},
                "mystery": {"name": "Mystery", "description": "Puzzles and investigations"},
                "romance": {"name": "Romance", "description": "Love stories and relationships"},
                "horror": {"name": "Horror", "description": "Scary and supernatural elements"},
                "children": {"name": "Children's Story", "description": "Kid-friendly stories"}
            }
            
            self.tones = {
                "serious": {"name": "Serious", "description": "Thoughtful and profound"},
                "funny": {"name": "Funny", "description": "Humorous and light-hearted"},
                "inspirational": {"name": "Inspirational", "description": "Uplifting and motivational"},
                "dramatic": {"name": "Dramatic", "description": "Intense and emotional"}
            }
            
            self.lengths = {
                "short": {"name": "Short", "description": "1-2 paragraphs (100-300 words)"},
                "medium": {"name": "Medium", "description": "3-5 paragraphs (300-600 words)"},
                "long": {"name": "Long", "description": "7+ paragraphs (600+ words)"}
            }
            
            self.languages = {
                "english": {"name": "English", "description": "Generate stories in English"},
                "urdu": {"name": "Urdu", "description": "Generate stories in Urdu (اردو)"},
                "arabic": {"name": "Arabic", "description": "Generate stories in Arabic (العربية)"},
                "spanish": {"name": "Spanish", "description": "Generate stories in Spanish (Español)"},
                "french": {"name": "French", "description": "Generate stories in French (Français)"},
                "german": {"name": "German", "description": "Generate stories in German (Deutsch)"}
            }
    
    def get_ui_config(self) -> Dict[str, Any]:
        """Get UI configuration for StoryWriter"""
        return {
            "inputs": [
                {
                    "name": "prompt",
                    "type": "textarea",
                    "label": "Story Prompt",
                    "placeholder": "Enter your story idea, characters, or plot...",
                    "required": True
                },
                {
                    "name": "genre",
                    "type": "dropdown",
                    "label": "Genre",
                    "options": [{"value": key, "label": config["name"]} for key, config in self.genres.items()],
                    "default": "fantasy"
                },
                {
                    "name": "tone",
                    "type": "dropdown",
                    "label": "Tone",
                    "options": [{"value": key, "label": config["name"]} for key, config in self.tones.items()],
                    "default": "serious"
                },
                {
                    "name": "length",
                    "type": "dropdown",
                    "label": "Length",
                    "options": [{"value": key, "label": config["name"]} for key, config in self.lengths.items()],
                    "default": "medium"
                },
                {
                    "name": "language",
                    "type": "dropdown",
                    "label": "Language",
                    "options": [{"value": key, "label": config["name"]} for key, config in self.languages.items()],
                    "default": "english"
                }
            ],
            "outputs": [
                {
                    "name": "story",
                    "type": "text",
                    "label": "Generated Story"
                }
            ],
            "ui_config": {
                "window_title": "StoryWriter - Desktop",
                "window_size": (1200, 800),
                "show_sidebar": True,
                "enable_export": True
            }
        }
    
    def process(self, **inputs) -> Dict[str, Any]:
        """Process story generation"""
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
            prompt = inputs.get("prompt", "").strip()
            genre = inputs.get("genre", "fantasy")
            tone = inputs.get("tone", "serious")
            length = inputs.get("length", "medium")
            language = inputs.get("language", "english")
            
            if not prompt:
                return {
                    "success": False,
                    "error": "No story prompt provided"
                }
            
            # Call the agent
            result = self.agent_instance.generate_story(
                prompt=prompt,
                genre=genre,
                tone=tone,
                length=length,
                language=language
            )
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Processing error: {str(e)}"
            }
    
    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        """Validate StoryWriter inputs"""
        prompt = inputs.get("prompt", "").strip()
        genre = inputs.get("genre", "")
        tone = inputs.get("tone", "")
        length = inputs.get("length", "")
        language = inputs.get("language", "")
        
        if not prompt:
            return False
        
        if genre not in self.genres:
            return False
            
        if tone not in self.tones:
            return False
            
        if length not in self.lengths:
            return False
            
        if language not in self.languages:
            return False
        
        return True
    
    def format_output(self, result: Any) -> str:
        """Format StoryWriter output"""
        if isinstance(result, dict):
            if result.get("success", True):
                story = result.get("story", {})
                if isinstance(story, dict):
                    title = story.get("title", "Untitled Story")
                    content = story.get("content", "")
                    
                    output = f"# {title}\n\n"
                    output += content
                    
                    # Add metadata if available
                    metadata = story.get("metadata", {})
                    if metadata:
                        output += "\n\n" + "="*50 + "\n"
                        output += "STORY METADATA\n"
                        output += "="*50 + "\n\n"
                        
                        for key, value in metadata.items():
                            output += f"**{key.title()}**: {value}\n"
                    
                    return output
                else:
                    return str(story)
            else:
                return f"Error: {result.get('error', 'Unknown error')}"
        
        return str(result)
