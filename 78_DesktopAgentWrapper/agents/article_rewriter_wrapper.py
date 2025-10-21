"""
ArticleRewriter agent wrapper for DesktopAgentWrapper
"""

import sys
import os
from typing import Dict, Any
from .agent_base import BaseAgent

# Add the ArticleRewriter path to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '75_ArticleRewriter'))

try:
    from agents.article_rewriter_agent import ArticleRewriterAgent
    from config import Config as ArticleRewriterConfig
except ImportError:
    # Fallback if ArticleRewriter is not available
    from .mock_agent import MockArticleRewriterAgent
    ArticleRewriterAgent = MockArticleRewriterAgent
    ArticleRewriterConfig = None

class ArticleRewriterWrapper(BaseAgent):
    """Wrapper for ArticleRewriter agent"""
    
    def __init__(self):
        super().__init__(
            agent_class=ArticleRewriterAgent,
            agent_name="ArticleRewriter",
            description="AI-powered content rewriting tool with multiple tone options"
        )
        
        # Initialize configuration
        if ArticleRewriterConfig:
            self.tones = ArticleRewriterConfig.TONES
            self.languages = ArticleRewriterConfig.LANGUAGES
        else:
            # Fallback configuration
            self.tones = {
                "formal": {"name": "Formal", "description": "Professional, academic tone"},
                "casual": {"name": "Casual", "description": "Conversational, friendly tone"},
                "professional": {"name": "Professional", "description": "Business-focused tone"},
                "witty": {"name": "Witty", "description": "Humorous, engaging tone"},
                "poetic": {"name": "Poetic", "description": "Artistic, flowing tone"},
                "persuasive": {"name": "Persuasive", "description": "Convincing, sales-oriented tone"},
                "simplified": {"name": "Simplified", "description": "Clear, easy-to-understand tone"}
            }
            
            self.languages = {
                "english": {"name": "English", "description": "Rewrite in English"},
                "urdu": {"name": "Urdu", "description": "Rewrite in Urdu (اردو)"},
                "spanish": {"name": "Spanish", "description": "Rewrite in Spanish (Español)"},
                "french": {"name": "French", "description": "Rewrite in French (Français)"},
                "german": {"name": "German", "description": "Rewrite in German (Deutsch)"},
                "arabic": {"name": "Arabic", "description": "Rewrite in Arabic (العربية)"}
            }
    
    def get_ui_config(self) -> Dict[str, Any]:
        """Get UI configuration for ArticleRewriter"""
        return {
            "inputs": [
                {
                    "name": "content",
                    "type": "textarea",
                    "label": "Content to Rewrite",
                    "placeholder": "Enter your article, blog post, or any text content here...",
                    "required": True
                },
                {
                    "name": "tone",
                    "type": "dropdown",
                    "label": "Writing Tone",
                    "options": [{"value": key, "label": config["name"]} for key, config in self.tones.items()],
                    "default": "formal"
                },
                {
                    "name": "language",
                    "type": "dropdown", 
                    "label": "Target Language",
                    "options": [{"value": key, "label": config["name"]} for key, config in self.languages.items()],
                    "default": "english"
                },
                {
                    "name": "generate_variations",
                    "type": "checkbox",
                    "label": "Generate Variations",
                    "default": True
                }
            ],
            "outputs": [
                {
                    "name": "rewritten_content",
                    "type": "text",
                    "label": "Rewritten Content"
                },
                {
                    "name": "variations",
                    "type": "list",
                    "label": "Variations"
                }
            ],
            "ui_config": {
                "window_title": "ArticleRewriter - Desktop",
                "window_size": (1200, 800),
                "show_sidebar": True,
                "enable_export": True
            }
        }
    
    def process(self, **inputs) -> Dict[str, Any]:
        """Process content rewriting"""
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
            content = inputs.get("content", "").strip()
            tone = inputs.get("tone", "formal")
            language = inputs.get("language", "english")
            generate_variations = inputs.get("generate_variations", True)
            
            if not content:
                return {
                    "success": False,
                    "error": "No content provided for rewriting"
                }
            
            # Call the agent
            result = self.agent_instance.rewrite_article(
                content=content,
                tone=tone,
                language=language,
                generate_variations=generate_variations
            )
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Processing error: {str(e)}"
            }
    
    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        """Validate ArticleRewriter inputs"""
        content = inputs.get("content", "").strip()
        tone = inputs.get("tone", "")
        language = inputs.get("language", "")
        
        if not content:
            return False
        
        if tone not in self.tones:
            return False
            
        if language not in self.languages:
            return False
        
        return True
    
    def format_output(self, result: Any) -> str:
        """Format ArticleRewriter output"""
        if isinstance(result, dict):
            if result.get("success", True):
                output = result.get("rewritten_content", "")
                
                # Add variations if available
                variations = result.get("variations", [])
                if variations:
                    output += "\n\n" + "="*50 + "\n"
                    output += "VARIATIONS\n"
                    output += "="*50 + "\n\n"
                    
                    for i, variation in enumerate(variations, 1):
                        output += f"VARIATION {i}:\n"
                        output += "-" * 20 + "\n"
                        output += f"{variation}\n\n"
                
                return output
            else:
                return f"Error: {result.get('error', 'Unknown error')}"
        
        return str(result)
