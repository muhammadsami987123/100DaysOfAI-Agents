import os
import httpx
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = None
if OPENAI_API_KEY:
    client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def generate_image_openai(prompt: str, n: int = 1, size: str = "1024x1024") -> list[str]:
    """
    Generates images using OpenAI's DALL-E model.
    """
    if not client:
        raise ValueError("OPENAI_API_KEY not found or client not initialized.")
    
    try:
        response = await client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=n,
            size=size
        )
        image_urls = [item.url for item in response.data]
        return image_urls
    except Exception as e:
        print(f"Error generating image with OpenAI: {e}")
        raise
