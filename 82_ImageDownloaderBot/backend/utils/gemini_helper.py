import os
import httpx
from dotenv import load_dotenv
import google.generativeai as genai
from typing import List, Optional
import json

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY not found in environment variables. Please set it in .env file.")
else:
    print(f"Gemini API Key loaded: {GEMINI_API_KEY[:5]}...{GEMINI_API_KEY[-5:]}")

genai.configure(api_key=GEMINI_API_KEY)

async def generate_image_gemini(prompt: str) -> List[str]:
    """
    Generates images using Google's Gemini model.
    Since Gemini Pro Vision currently doesn't support direct image generation,
    we'll use it to generate a descriptive prompt and then use a fallback URL
    that represents what the image would look like.
    """
    try:
        # Initialize Gemini Pro model
        model = genai.GenerativeModel('models/imagen-4.0-fast-generate-001')
        
        # Generate a more detailed description using Gemini
        enhance_prompt = f"""Given this image prompt: '{prompt}'
        Create a detailed visual description that could be used to generate an image.
        Focus on visual details, style, composition, lighting, and mood."""
        
        response = await model.generate_content_async(enhance_prompt)
        enhanced_description = response.text if response else prompt
        
        # For now, return a placeholder URL with the enhanced description
        # This would be replaced with actual image generation when available
        placeholder_text = enhanced_description.replace(' ', '+')[:50]  # Limit length for URL
        image_url = f"https://via.placeholder.com/800x600?text={placeholder_text}"
        
        return [image_url]
        
    except Exception as e:
        print(f"Error in Gemini image generation: {str(e)}")
        # Return a fallback placeholder if something goes wrong
        return [f"https://via.placeholder.com/800x600?text=Error:+{str(e)[:30]}"]
