"""
Mock agent for testing DesktopAgentWrapper when real agents are not available
"""

import time
from typing import Dict, Any

class MockArticleRewriterAgent:
    """Mock ArticleRewriter agent for testing"""
    
    def __init__(self):
        self.name = "MockArticleRewriter"
    
    def rewrite_article(self, content: str, tone: str = "formal", language: str = "english", generate_variations: bool = True) -> Dict[str, Any]:
        """Mock rewrite functionality"""
        # Simulate processing time
        time.sleep(0.5)
        
        # Generate mock rewritten content
        rewritten_content = f"[{tone.upper()}] {content}"
        
        variations = []
        if generate_variations:
            variations = [
                f"[{tone.upper()} VARIATION 1] {content}",
                f"[{tone.upper()} VARIATION 2] {content}"
            ]
        
        return {
            "success": True,
            "rewritten_content": rewritten_content,
            "variations": variations,
            "metadata": {
                "original_length": len(content),
                "rewritten_length": len(rewritten_content),
                "tone": tone,
                "language": language,
                "word_count": len(rewritten_content.split()),
                "variations_count": len(variations)
            }
        }

class MockStoryWriterAgent:
    """Mock StoryWriter agent for testing"""
    
    def __init__(self):
        self.name = "MockStoryWriter"
    
    def generate_story(self, prompt: str, genre: str = "fantasy", tone: str = "serious", length: str = "medium", language: str = "english") -> Dict[str, Any]:
        """Mock story generation"""
        time.sleep(0.5)
        
        story_content = f"Once upon a time, in a {genre} world, there was a story about: {prompt}. The tone was {tone} and the length was {length}."
        
        return {
            "success": True,
            "story": {
                "title": f"A {genre.title()} Story",
                "content": story_content,
                "metadata": {
                    "genre": genre,
                    "tone": tone,
                    "length": length,
                    "language": language
                }
            }
        }

class MockPromptImproverAgent:
    """Mock PromptImprover agent for testing"""
    
    def __init__(self):
        self.name = "MockPromptImprover"
    
    def improve_prompt(self, raw_prompt: str, tone: str = "professional") -> Dict[str, Any]:
        """Mock prompt improvement"""
        time.sleep(0.5)
        
        improved_prompt = f"[IMPROVED - {tone.upper()}] {raw_prompt}"
        
        suggestions = [
            "Add more specific details",
            "Use clearer language",
            "Include context information"
        ]
        
        return {
            "success": True,
            "improved_prompt": improved_prompt,
            "suggestions": suggestions
        }
