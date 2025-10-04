import google.generativeai as genai
import random
from typing import Dict, Any, Optional
from config import Config

class AIQuoteGenerator:
    """AI-powered agent to generate motivational, deep, and meaningful quotes."""

    def __init__(self):
        try:
            if not Config.GOOGLE_API_KEY:
                raise ValueError("Google API key not found in configuration")

            genai.configure(api_key=Config.GOOGLE_API_KEY)
            self.client = genai.GenerativeModel(Config.GEMINI_MODEL)
            print("✅ AIQuoteGenerator initialized successfully with Google Gemini")
        except Exception as e:
            print(f"Warning: Could not initialize Google Gemini client: {e}")
            self.client = None
            print("⚠️ AIQuoteGenerator initialized without Gemini (limited functionality)")

    async def generate_quote(self, mood: str, tone: str, output_format: str) -> Dict[str, Any]:
        """
        Generate a motivational quote based on mood, tone, and output format.

        Args:
            mood (str): The desired mood or theme (e.g., Success, Positivity).
            tone (str): The desired tone for the quote (e.g., Poetic, Bold).
            output_format (str): The desired output format (e.g., Text only, Image Quote, Tweet-ready).

        Returns:
            Dict[str, Any]: A dictionary containing the generated quote, image URL (if applicable),
                            and other metadata.
        """
        try:
            if not self.client:
                return self._create_fallback_quote(mood)

            prompt = self._build_prompt(mood, tone, output_format)
            print(f"🤖 Generating quote for mood='{mood}', tone='{tone}', format='{output_format}'")
            
            response = await self.client.generate_content_async(prompt)
            quote_text = response.text.strip()

            image_url = self._get_mock_image_url(mood)
            tweet_text = self._format_for_tweet(quote_text)

            print(f"✅ Quote generated successfully (length: {len(quote_text)} characters)")

            return {
                "success": True,
                "quote": quote_text,
                "image_url": image_url,
                "tweet_ready": tweet_text,
                "error": None
            }

        except Exception as e:
            print(f"❌ AI quote generation failed: {e}")
            return {
                "success": False,
                "quote": None,
                "image_url": None,
                "tweet_ready": None,
                "error": f"Failed to generate quote: {str(e)}"
            }

    def _build_prompt(self, mood: str, tone: str, output_format: str) -> str:
        """
        Build the prompt for the Google Gemini API.
        """
        prompt = f"""
        You are AIQuoteGenerator, an intelligent agent that generates unique, original, and emotionally resonant motivational quotes.
        The user wants a quote with the following characteristics:
        - Mood/Theme: {mood}
        - Tone: {tone}
        - Output Format Preference: {output_format}

        Generate a fresh, never-repeated, and impactful quote. Make it suitable for social media, personal journals, or daily affirmations.
        Do NOT include any introductory or concluding remarks, just the quote itself. Ensure the quote is concise and powerful.
        """
        return prompt.strip()

    def _create_fallback_quote(self, mood: str) -> Dict[str, Any]:
        """Create a fallback quote if AI generation fails."""
        fallback_quotes = {
            "Success": "The only way to do great work is to love what you do. Keep pushing forward!",
            "Mindset": "Your mindset determines your future. Cultivate positivity daily.",
            "Positivity": "Choose to be optimistic, it feels better. Embrace the light within you.",
            "Hustle": "Great things come from hard work and perseverance. Never give up on your dreams.",
            "Self-Reflection": "Take time to reflect. It's the path to growth and understanding.",
            "default": "Stay inspired. Every day is a new opportunity to shine."
        }
        quote_text = fallback_quotes.get(mood, fallback_quotes["default"])
        print(f"⚠️ Using fallback quote for mood='{mood}'")
        return {
            "success": True,
            "quote": quote_text,
            "image_url": self._get_mock_image_url(mood),
            "tweet_ready": self._format_for_tweet(quote_text),
            "error": "AI service not available, showing a fallback quote."
        }

    def _get_mock_image_url(self, mood: str) -> str:
        """
        Returns a reliable random image URL using Picsum Photos.
        """
        # Use a cache-busting param to always get a new image
        cache_buster = f"t={random.randint(100000, 999999)}"
        return f"https://picsum.photos/800/600?{cache_buster}"

    def _format_for_tweet(self, quote: str) -> str:
        """
        Formats the quote to be tweet-ready (max 280 characters, adds hashtags).
        """
        hashtags = "#Motivation #Inspiration #QuoteOfTheDay"
        max_quote_length = 280 - len(hashtags) - 5 # 5 for ellipses and space

        if len(quote) > max_quote_length:
            quote = quote[:max_quote_length].rsplit(' ', 1)[0] + "..."
        
        return f"{quote}\n\n{hashtags}"
