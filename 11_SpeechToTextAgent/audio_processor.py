import os
import tempfile
from pathlib import Path
from typing import Optional, Tuple
import logging

from pydub import AudioSegment
from moviepy.editor import VideoFileClip
from config import SUPPORTED_AUDIO_FORMATS, SUPPORTED_VIDEO_FORMATS, MAX_FILE_SIZE

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AudioProcessingError(Exception):
    """Custom exception for audio processing errors."""
    pass


def validate_file(file_path: str, file_size: int) -> Tuple[bool, str]:
    """
    Validate uploaded file for size and format.
    
    Args:
        file_path: Path to the uploaded file
        file_size: Size of the file in bytes
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if file_size > MAX_FILE_SIZE:
        return False, f"File size ({file_size / 1024 / 1024:.1f}MB) exceeds maximum allowed size (25MB)"
    
    file_extension = Path(file_path).suffix.lower()
    
    if file_extension in SUPPORTED_AUDIO_FORMATS:
        return True, ""
    elif file_extension in SUPPORTED_VIDEO_FORMATS:
        return True, ""
    else:
        supported_formats = list(SUPPORTED_AUDIO_FORMATS) + list(SUPPORTED_VIDEO_FORMATS)
        return False, f"Unsupported file format. Supported formats: {', '.join(supported_formats)}"


def extract_audio_from_video(video_path: str) -> str:
    """
    Extract audio from video file.
    
    Args:
        video_path: Path to the video file
        
    Returns:
        Path to the extracted audio file
    """
    try:
        logger.info(f"Extracting audio from video: {video_path}")
        
        # Create a temporary file for the audio
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            temp_audio_path = temp_audio.name
        
        # Load video and extract audio
        video = VideoFileClip(video_path)
        audio = video.audio
        
        if audio is None:
            raise AudioProcessingError("No audio track found in the video file")
        
        # Write audio to temporary file
        audio.write_audiofile(temp_audio_path, verbose=False, logger=None)
        
        # Close video to free up resources
        video.close()
        audio.close()
        
        logger.info(f"Audio extracted successfully to: {temp_audio_path}")
        return temp_audio_path
        
    except Exception as e:
        logger.error(f"Error extracting audio from video: {e}")
        raise AudioProcessingError(f"Failed to extract audio from video: {str(e)}")


def convert_audio_to_wav(audio_path: str) -> str:
    """
    Convert audio file to WAV format for better compatibility with Whisper.
    
    Args:
        audio_path: Path to the audio file
        
    Returns:
        Path to the converted WAV file
    """
    try:
        logger.info(f"Converting audio to WAV: {audio_path}")
        
        # Create a temporary WAV file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
            temp_wav_path = temp_wav.name
        
        # Load audio and convert to WAV
        audio = AudioSegment.from_file(audio_path)
        
        # Export as WAV with specific parameters for Whisper
        audio.export(
            temp_wav_path,
            format="wav",
            parameters=["-ar", "16000", "-ac", "1"]  # 16kHz mono for optimal Whisper performance
        )
        
        logger.info(f"Audio converted to WAV successfully: {temp_wav_path}")
        return temp_wav_path
        
    except Exception as e:
        logger.error(f"Error converting audio to WAV: {e}")
        raise AudioProcessingError(f"Failed to convert audio to WAV: {str(e)}")


def process_media_file(file_path: str, file_size: int) -> str:
    """
    Process uploaded media file and prepare it for transcription.
    
    Args:
        file_path: Path to the uploaded file
        file_size: Size of the file in bytes
        
    Returns:
        Path to the processed audio file ready for transcription
    """
    try:
        # Validate file
        is_valid, error_message = validate_file(file_path, file_size)
        if not is_valid:
            raise AudioProcessingError(error_message)
        
        file_extension = Path(file_path).suffix.lower()
        
        # If it's a video file, extract audio first
        if file_extension in SUPPORTED_VIDEO_FORMATS:
            logger.info("Processing video file - extracting audio")
            audio_path = extract_audio_from_video(file_path)
        else:
            # It's an audio file, use it directly
            audio_path = file_path
        
        # Convert to WAV format for optimal Whisper performance
        wav_path = convert_audio_to_wav(audio_path)
        
        # Clean up intermediate audio file if it was extracted from video
        if file_extension in SUPPORTED_VIDEO_FORMATS and audio_path != file_path:
            try:
                os.unlink(audio_path)
                logger.info("Cleaned up intermediate audio file")
            except Exception as e:
                logger.warning(f"Failed to clean up intermediate file: {e}")
        
        return wav_path
        
    except Exception as e:
        logger.error(f"Error processing media file: {e}")
        raise AudioProcessingError(f"Failed to process media file: {str(e)}")


def cleanup_temp_files(*file_paths: str) -> None:
    """
    Clean up temporary files.
    
    Args:
        *file_paths: Variable number of file paths to delete
    """
    for file_path in file_paths:
        try:
            if file_path and os.path.exists(file_path):
                os.unlink(file_path)
                logger.info(f"Cleaned up temporary file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to clean up file {file_path}: {e}")


def get_file_info(file_path: str) -> dict:
    """
    Get information about the uploaded file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Dictionary containing file information
    """
    try:
        path = Path(file_path)
        file_size = os.path.getsize(file_path)
        
        return {
            "filename": path.name,
            "extension": path.suffix.lower(),
            "size_mb": round(file_size / 1024 / 1024, 2),
            "is_video": path.suffix.lower() in SUPPORTED_VIDEO_FORMATS,
            "is_audio": path.suffix.lower() in SUPPORTED_AUDIO_FORMATS
        }
    except Exception as e:
        logger.error(f"Error getting file info: {e}")
        return {}
