import os
import httpx
import aiofiles
import uuid
import base64
from datetime import datetime
from typing import Optional
import re
from urllib.parse import urlparse

IMAGE_DIR = "./downloaded_images"
os.makedirs(IMAGE_DIR, exist_ok=True)

def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def get_file_extension(url: str) -> str:
    """Extract file extension from URL or default to png"""
    if url.startswith('data:image/'):
        # Extract extension from base64 image
        mime_match = re.match(r'data:image/(\w+);base64,', url)
        return mime_match.group(1) if mime_match else 'png'
    
    # Extract extension from URL
    ext_match = re.search(r'\.([a-zA-Z0-9]+)(?:\?.*)?$', url)
    if ext_match and len(ext_match.group(1)) <= 5:
        return ext_match.group(1).lower()
    return 'png'

async def save_generated_image(image_url: str, prompt: str) -> Optional[str]:
    """
    Downloads an image from a URL and saves it locally.
    Returns the file path if successful, None otherwise.
    """
    try:
        if not is_valid_url(image_url):
            raise ValueError("Invalid image URL provided")

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(image_url)
            response.raise_for_status()

            # Verify content type is an image
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                raise ValueError(f"Invalid content type: {content_type}")

        file_name = f"generated_{uuid.uuid4()}.{get_file_extension(image_url)}"
        file_path = os.path.join(IMAGE_DIR, file_name)

        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(response.content)
        
        return file_path

    except httpx.TimeoutException:
        print(f"Timeout downloading image from {image_url}")
        return None
    except httpx.HTTPStatusError as e:
        print(f"HTTP error downloading image from {image_url}: {e}")
        return None
    except Exception as e:
        print(f"Error saving generated image from {image_url}: {e}")
        return None

async def download_image_from_url(url: str) -> Optional[str]:
    """
    Downloads an image from a given URL or base64 string and saves it locally.
    Returns the file path if successful, None otherwise.
    """
    try:
        if url.startswith('data:image/'):
            # Handle base64 image
            try:
                header, encoded = url.split(",", 1)
                file_extension = get_file_extension(url)
                data = base64.b64decode(encoded)
                
                file_name = f"downloaded_{uuid.uuid4()}.{file_extension}"
                file_path = os.path.join(IMAGE_DIR, file_name)
                
                async with aiofiles.open(file_path, 'wb') as f:
                    await f.write(data)
                return file_path
            except Exception as e:
                print(f"Error processing base64 image: {e}")
                return None
        
        else:
            # Handle URL
            if not is_valid_url(url):
                raise ValueError("Invalid URL provided")

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url)
                response.raise_for_status()

                # Verify content type is an image
                content_type = response.headers.get('content-type', '')
                if not content_type.startswith('image/'):
                    raise ValueError(f"Invalid content type: {content_type}")

            file_name = f"downloaded_{uuid.uuid4()}.{get_file_extension(url)}"
            file_path = os.path.join(IMAGE_DIR, file_name)

            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(response.content)
            
            return file_path

    except httpx.TimeoutException:
        print(f"Timeout downloading image from {url}")
        return None
    except httpx.HTTPStatusError as e:
        print(f"HTTP error downloading image from {url}: {e}")
        return None
    except Exception as e:
        print(f"Error downloading image from {url}: {e}")
        return None
