import os
import tempfile
import logging
from pathlib import Path
from typing import Optional, Tuple

import yt_dlp
from config import MAX_FILE_SIZE

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class YouTubeProcessingError(Exception):
    """Custom exception for YouTube processing errors."""
    pass


def validate_youtube_url(url: str) -> Tuple[bool, str]:
    """
    Validate YouTube URL format.
    
    Args:
        url: YouTube URL to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not url or not url.strip():
        return False, "YouTube URL is required"
    
    url = url.strip()
    
    # Check if it's a valid YouTube URL
    youtube_patterns = [
        "youtube.com/watch",
        "youtu.be/",
        "youtube.com/embed/",
        "youtube.com/v/",
        "youtube.com/shorts/"
    ]
    
    if not any(pattern in url for pattern in youtube_patterns):
        return False, "Invalid YouTube URL format"
    
    return True, ""


def download_youtube_audio(url: str) -> Tuple[str, dict]:
    """
    Download audio from YouTube video.
    
    Args:
        url: YouTube video URL
        
    Returns:
        Tuple of (audio_file_path, video_info)
    """
    try:
        logger.info(f"Downloading audio from YouTube: {url}")
        
        # Create a temporary directory for downloads
        with tempfile.TemporaryDirectory() as temp_dir:
            # Configure yt-dlp options
            ydl_opts = {
                'format': 'bestaudio/best',  # Best audio quality
                'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav',
                    'preferredquality': '192',
                }],
                'quiet': True,
                'no_warnings': True,
                'extractaudio': True,
                'audioformat': 'wav',
                'audioquality': '0',  # Best quality
                'writesubtitles': False,
                'writeautomaticsub': False,
                'ignoreerrors': False,
                'no_check_certificate': True,
                'prefer_ffmpeg': True,
            }
            
            # Download the video
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Get video info first
                video_info = ydl.extract_info(url, download=False)
                
                # Check video duration (limit to reasonable length)
                duration = video_info.get('duration', 0)
                if duration > 3600:  # 1 hour limit
                    raise YouTubeProcessingError("Video is too long (maximum 1 hour allowed)")
                
                # Download the audio
                ydl.download([url])
            
            # Find the downloaded audio file
            audio_files = list(Path(temp_dir).glob("*.wav"))
            if not audio_files:
                raise YouTubeProcessingError("No audio file was downloaded")
            
            # Get the first (and should be only) audio file
            audio_file = audio_files[0]
            
            # Check file size
            file_size = audio_file.stat().st_size
            if file_size > MAX_FILE_SIZE:
                raise YouTubeProcessingError(f"Downloaded audio file is too large ({file_size / 1024 / 1024:.1f}MB)")
            
            # Copy to a new temporary file (since temp_dir will be deleted)
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
                temp_audio_path = temp_audio.name
            
            # Read and write the file content
            with open(audio_file, 'rb') as src, open(temp_audio_path, 'wb') as dst:
                dst.write(src.read())
            
            logger.info(f"YouTube audio downloaded successfully: {temp_audio_path}")
            
            # Prepare video info for return
            clean_info = {
                'title': video_info.get('title', 'Unknown'),
                'duration': video_info.get('duration', 0),
                'uploader': video_info.get('uploader', 'Unknown'),
                'view_count': video_info.get('view_count', 0),
                'upload_date': video_info.get('upload_date', 'Unknown'),
                'description': video_info.get('description', '')[:200] + '...' if video_info.get('description', '') else '',
                'thumbnail': video_info.get('thumbnail', ''),
                'webpage_url': video_info.get('webpage_url', url)
            }
            
            return temp_audio_path, clean_info
            
    except yt_dlp.DownloadError as e:
        logger.error(f"YouTube download error: {e}")
        raise YouTubeProcessingError(f"Failed to download YouTube video: {str(e)}")
    except Exception as e:
        logger.error(f"Error processing YouTube video: {e}")
        raise YouTubeProcessingError(f"Failed to process YouTube video: {str(e)}")


def get_youtube_video_info(url: str) -> dict:
    """
    Get information about a YouTube video without downloading.
    
    Args:
        url: YouTube video URL
        
    Returns:
        Dictionary containing video information
    """
    try:
        logger.info(f"Getting YouTube video info: {url}")
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(url, download=False)
            
            return {
                'title': video_info.get('title', 'Unknown'),
                'duration': video_info.get('duration', 0),
                'uploader': video_info.get('uploader', 'Unknown'),
                'view_count': video_info.get('view_count', 0),
                'upload_date': video_info.get('upload_date', 'Unknown'),
                'description': video_info.get('description', '')[:200] + '...' if video_info.get('description', '') else '',
                'thumbnail': video_info.get('thumbnail', ''),
                'webpage_url': video_info.get('webpage_url', url),
                'is_valid': True
            }
            
    except Exception as e:
        logger.error(f"Error getting YouTube video info: {e}")
        return {
            'is_valid': False,
            'error': str(e)
        }


def format_duration(seconds: int) -> str:
    """
    Format duration in seconds to human-readable format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        remaining_seconds = seconds % 60
        return f"{hours}h {minutes}m {remaining_seconds}s"


def is_youtube_url(url: str) -> bool:
    """
    Check if a URL is a YouTube URL.
    
    Args:
        url: URL to check
        
    Returns:
        True if it's a YouTube URL, False otherwise
    """
    if not url:
        return False
    
    url = url.strip().lower()
    return any(pattern in url for pattern in [
        "youtube.com/watch",
        "youtu.be/",
        "youtube.com/embed/",
        "youtube.com/v/",
        "youtube.com/shorts/"
    ])
