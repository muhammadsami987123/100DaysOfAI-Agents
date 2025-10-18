"""
Core ArticleRewriter agent functionality for AI-powered content rewriting
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from openai import OpenAI

from config import Config

class ArticleRewriterAgent:
    """Main agent class for article rewriting and management"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the ArticleRewriterAgent with API key"""
        self.model_choice = Config.LLM_MODEL.lower()
        self.openai_client = None
        self.gemini_client = None
        self.gemini_model = None
        self.outputs_dir = Path(Config.OUTPUTS_DIR)
        
        # Create directories if they don't exist
        self.outputs_dir.mkdir(exist_ok=True)
        
        # Initialize clients based on configuration
        self._init_clients()
    
    def _init_clients(self):
        """Initialize AI clients based on configuration"""
        if self.model_choice == "gemini" and Config.GEMINI_API_KEY:
            try:
                import google.generativeai as genai
                genai.configure(api_key=Config.GEMINI_API_KEY)
                self.gemini_model = genai.GenerativeModel(Config.GEMINI_MODEL)
                self.gemini_client = genai
                print("✅ ArticleRewriterAgent initialized with Gemini")
            except Exception as e:
                print(f"❌ Error initializing Gemini client: {e}")
                self.gemini_client = None
                self.gemini_model = None
        
        if self.model_choice == "openai" and Config.OPENAI_API_KEY:
            try:
                self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
                print("✅ ArticleRewriterAgent initialized with OpenAI")
            except Exception as e:
                print(f"❌ Error initializing OpenAI client: {e}")
                self.openai_client = None
        
        # If no valid client, try fallback
        if not self.gemini_client and not self.openai_client:
            if Config.OPENAI_API_KEY:
                try:
                    self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
                    print("✅ ArticleRewriterAgent initialized with OpenAI (fallback)")
                except Exception as e:
                    print(f"❌ Error initializing OpenAI fallback: {e}")
            elif Config.GEMINI_API_KEY:
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=Config.GEMINI_API_KEY)
                    self.gemini_model = genai.GenerativeModel(Config.GEMINI_MODEL)
                    self.gemini_client = genai
                    print("✅ ArticleRewriterAgent initialized with Gemini (fallback)")
                except Exception as e:
                    print(f"❌ Error initializing Gemini fallback: {e}")
            else:
                print("⚠️ Warning: No valid API keys provided. AI features will be limited.")
    
    def rewrite_article(
        self, 
        content: str, 
        tone: str = "formal",
        language: str = "english",
        generate_variations: bool = True
    ) -> Dict[str, Any]:
        """
        Rewrite article content in the specified tone and language
        
        Args:
            content: Original article content to rewrite
            tone: Target tone for rewriting (formal, casual, professional, etc.)
            language: Target language for rewriting
            generate_variations: Whether to generate multiple variations
            
        Returns:
            Dict containing rewritten content and metadata
        """
        if not self.gemini_client and not self.openai_client:
            return self._create_fallback_response(content, tone, language)
        
        if not content.strip():
            return {
                "success": False,
                "error": "No content provided for rewriting",
                "rewritten_content": "",
                "variations": [],
                "metadata": {}
            }
        
        try:
            # Generate main rewritten content
            rewritten_content = self._generate_rewritten_content(content, tone, language)
            
            # Generate variations if requested
            variations = []
            if generate_variations:
                variations = self._generate_variations(content, tone, language)
            
            # Create metadata
            metadata = {
                "original_length": len(content),
                "rewritten_length": len(rewritten_content),
                "tone": tone,
                "language": language,
                "timestamp": datetime.now().isoformat(),
                "word_count": len(rewritten_content.split()),
                "variations_count": len(variations)
            }
            
            return {
                "success": True,
                "rewritten_content": rewritten_content,
                "variations": variations,
                "metadata": metadata,
                "error": None
            }
            
        except Exception as e:
            print(f"❌ Error rewriting article: {e}")
            return {
                "success": False,
                "error": f"Failed to rewrite article: {str(e)}",
                "rewritten_content": "",
                "variations": [],
                "metadata": {}
            }
    
    def _generate_rewritten_content(self, content: str, tone: str, language: str) -> str:
        """Generate the main rewritten content using Gemini or OpenAI"""
        prompt = self._build_rewrite_prompt(content, tone, language)
        
        # Try Gemini first if available
        if self.gemini_model:
            try:
                response = self.gemini_model.generate_content(prompt)
                return response.text.strip()
            except Exception as e:
                print(f"❌ Error generating rewritten content with Gemini: {e}")
        
        # Try OpenAI if available
        if self.openai_client:
            try:
                response = self.openai_client.chat.completions.create(
                    model=Config.OPENAI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are an expert content rewriter who can adapt any text to different tones and styles while preserving the original meaning and key information."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=Config.MAX_TOKENS,
                    temperature=Config.TEMPERATURE
                )
                
                return response.choices[0].message.content.strip()
                
            except Exception as e:
                print(f"❌ Error generating rewritten content with OpenAI: {e}")
        
        # Fallback if both fail
        return self._create_fallback_rewrite(content, tone)
    
    def _generate_variations(self, content: str, tone: str, language: str) -> List[str]:
        """Generate 2-3 variations of the rewritten content"""
        variations = []
        
        # Get alternative tones for variations
        alternative_tones = self._get_alternative_tones(tone)
        
        for alt_tone in alternative_tones[:2]:  # Limit to 2 variations
            try:
                prompt = self._build_rewrite_prompt(content, alt_tone, language)
                variation = None
                
                # Try Gemini first if available
                if self.gemini_model:
                    try:
                        response = self.gemini_model.generate_content(prompt)
                        variation = response.text.strip()
                    except Exception as e:
                        print(f"❌ Error generating variation with Gemini: {e}")
                
                # Try OpenAI if Gemini failed or not available
                if not variation and self.openai_client:
                    try:
                        response = self.openai_client.chat.completions.create(
                            model=Config.OPENAI_MODEL,
                            messages=[
                                {"role": "system", "content": "You are an expert content rewriter who can adapt any text to different tones and styles while preserving the original meaning and key information."},
                                {"role": "user", "content": prompt}
                            ],
                            max_tokens=Config.MAX_TOKENS,
                            temperature=Config.TEMPERATURE
                        )
                        
                        variation = response.choices[0].message.content.strip()
                    except Exception as e:
                        print(f"❌ Error generating variation with OpenAI: {e}")
                
                if variation and variation != content:
                    variations.append(variation)
                    
            except Exception as e:
                print(f"❌ Error generating variation with tone {alt_tone}: {e}")
                continue
        
        return variations
    
    def _build_rewrite_prompt(self, content: str, tone: str, language: str) -> str:
        """Build the prompt for rewriting content"""
        tone_info = Config.TONES.get(tone, {})
        tone_name = tone_info.get("name", tone.title())
        tone_description = tone_info.get("description", "")
        
        language_info = Config.LANGUAGES.get(language, {})
        language_name = language_info.get("name", language.title())
        
        prompt = f"""Rewrite the following content in a {tone_name.lower()} tone and in {language_name}.

Target Tone: {tone_name}
Description: {tone_description}
Language: {language_name}

Instructions:
1. Maintain the original meaning and key information
2. Adapt the writing style to match the {tone_name.lower()} tone
3. Ensure the content flows naturally and is engaging
4. Keep the same structure and organization
5. Write in {language_name}
6. Make it appropriate for the target tone while preserving all important details

Original Content:
{content}

Rewritten Content:"""
        
        return prompt
    
    def _get_alternative_tones(self, primary_tone: str) -> List[str]:
        """Get alternative tones for generating variations"""
        all_tones = list(Config.TONES.keys())
        if primary_tone in all_tones:
            all_tones.remove(primary_tone)
        
        # Return a curated list of complementary tones
        tone_mapping = {
            "formal": ["professional", "casual"],
            "casual": ["witty", "simplified"],
            "professional": ["formal", "persuasive"],
            "witty": ["casual", "poetic"],
            "poetic": ["witty", "persuasive"],
            "persuasive": ["professional", "casual"],
            "simplified": ["casual", "professional"]
        }
        
        return tone_mapping.get(primary_tone, all_tones[:2])
    
    def _create_fallback_response(self, content: str, tone: str, language: str) -> Dict[str, Any]:
        """Create a fallback response when AI is not available"""
        fallback_content = self._create_fallback_rewrite(content, tone)
        
        return {
            "success": True,
            "rewritten_content": fallback_content,
            "variations": [
                f"[Variation 1] {fallback_content}",
                f"[Variation 2] {fallback_content}"
            ],
            "metadata": {
                "original_length": len(content),
                "rewritten_length": len(fallback_content),
                "tone": tone,
                "language": language,
                "timestamp": datetime.now().isoformat(),
                "word_count": len(fallback_content.split()),
                "variations_count": 2,
                "fallback": True
            },
            "error": None
        }
    
    def _create_fallback_rewrite(self, content: str, tone: str) -> str:
        """Create a simple fallback rewrite when AI is not available"""
        tone_prefixes = {
            "formal": "It is important to note that",
            "casual": "So here's the thing,",
            "professional": "From a business perspective,",
            "witty": "Well, well, well,",
            "poetic": "In the realm of words,",
            "persuasive": "You should definitely know that",
            "simplified": "Simply put,"
        }
        
        prefix = tone_prefixes.get(tone, "Here's the content:")
        return f"{prefix} {content}"
    
    def save_rewrite(self, rewrite_data: Dict[str, Any], format: str = "txt") -> Optional[str]:
        """Save rewritten content to file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            tone = rewrite_data.get("metadata", {}).get("tone", "unknown")
            filename = f"rewrite_{tone}_{timestamp}.{format}"
            filepath = self.outputs_dir / filename
            
            content = rewrite_data.get("rewritten_content", "")
            if not content:
                return None
            
            with open(filepath, 'w', encoding='utf-8') as f:
                if format == "md":
                    f.write(f"# Rewritten Article\n\n")
                    f.write(f"**Tone:** {tone.title()}\n")
                    f.write(f"**Language:** {rewrite_data.get('metadata', {}).get('language', 'unknown').title()}\n")
                    f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    f.write("---\n\n")
                    f.write(content)
                    
                    # Add variations if available
                    variations = rewrite_data.get("variations", [])
                    if variations:
                        f.write("\n\n## Variations\n\n")
                        for i, variation in enumerate(variations, 1):
                            f.write(f"### Variation {i}\n\n")
                            f.write(f"{variation}\n\n")
                else:
                    f.write(f"Rewritten Article - {tone.title()}\n")
                    f.write(f"Language: {rewrite_data.get('metadata', {}).get('language', 'unknown').title()}\n")
                    f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(content)
                    
                    # Add variations if available
                    variations = rewrite_data.get("variations", [])
                    if variations:
                        f.write("\n\n" + "=" * 50 + "\n")
                        f.write("VARIATIONS\n")
                        f.write("=" * 50 + "\n\n")
                        for i, variation in enumerate(variations, 1):
                            f.write(f"VARIATION {i}:\n")
                            f.write("-" * 20 + "\n")
                            f.write(f"{variation}\n\n")
            
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Error saving rewrite: {e}")
            return None
    
    def get_available_tones(self) -> Dict[str, Dict[str, str]]:
        """Get available tones for rewriting"""
        return Config.TONES
    
    def get_available_languages(self) -> Dict[str, Dict[str, str]]:
        """Get available languages for rewriting"""
        return Config.LANGUAGES
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about saved rewrites"""
        try:
            files = list(self.outputs_dir.glob("rewrite_*"))
            return {
                "total_rewrites": len(files),
                "outputs_directory": str(self.outputs_dir),
                "available_formats": Config.OUTPUT_EXTENSIONS
            }
        except Exception as e:
            return {"error": f"Failed to get stats: {e}"}
