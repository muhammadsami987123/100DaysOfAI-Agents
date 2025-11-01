import pytest
import os
from unittest.mock import MagicMock, patch
from agent import VideoChapterAgent
from config import UPLOAD_DIR, CHAPTERS_DIR, TRANSCRIPTS_DIR

# Ensure test directories exist and are clean
@pytest.fixture(scope="module", autouse=True)
def setup_test_environment():
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(CHAPTERS_DIR, exist_ok=True)
    os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)
    # Clean up any previous test files
    for d in [UPLOAD_DIR, CHAPTERS_DIR, TRANSCRIPTS_DIR]:
        for f in os.listdir(d):
            os.remove(os.path.join(d, f))
    yield
    # Teardown: clean up after tests
    for d in [UPLOAD_DIR, CHAPTERS_DIR, TRANSCRIPTS_DIR]:
        for f in os.listdir(d):
            os.remove(os.path.join(d, f))

@pytest.fixture
def agent():
    # Mock LLMService for agent tests
    with patch('agent.LLMService') as MockLLMService:
        mock_llm_service_instance = MockLLMService.return_value
        mock_llm_service_instance.generate_chapters.return_value = [
            {"title": "Introduction", "start": "00:00:00", "end": "00:00:10"},
            {"title": "Main Topic", "start": "00:00:11", "end": "00:00:20"}
        ]
        # Mock the transcribe_audio method to return a dummy transcript
        with patch('agent.VideoChapterAgent._transcribe_audio', return_value="This is a test transcript."):
            return VideoChapterAgent()

# Mock pydub and ffmpeg for file operations
@patch('agent.AudioSegment.from_file')
@patch('agent.AudioSegment.export')
@patch('agent.ffmpeg_extract_subclip')
def test_process_video(mock_ffmpeg_extract_subclip, mock_export, mock_from_file, agent):
    # Create a dummy video file for testing
    dummy_video_path = os.path.join(UPLOAD_DIR, "dummy_video.mp4")
    with open(dummy_video_path, "w") as f:
        f.write("dummy video content")

    # Mock AudioSegment instance and its properties
    mock_audio_segment = MagicMock()
    mock_audio_segment.duration_seconds = 20 # Simulate a 20-second video
    mock_from_file.return_value = mock_audio_segment

    video_path, chapters, transcript = agent.process_video(dummy_video_path, "gemini-pro")

    assert video_path == os.path.basename(dummy_video_path)
    assert len(chapters) == 2
    assert chapters[0]["title"] == "Introduction"
    assert transcript == "This is a test transcript."
    mock_ffmpeg_extract_subclip.assert_called()
    mock_export.assert_called()

def test_generate_chapters_from_transcript(agent):
    transcript = "This is a test transcript for chapter generation."
    chapters = agent._generate_chapters_from_transcript(transcript, "gemini-pro")
    assert len(chapters) == 2
    assert chapters[0]["title"] == "Introduction"

def test_split_video_into_chapters(agent):
    dummy_video_path = os.path.join(UPLOAD_DIR, "dummy_video_split.mp4")
    with open(dummy_video_path, "w") as f:
        f.write("dummy video content")

    chapters_data = [
        {"title": "Intro", "start": "00:00:00", "end": "00:00:05"},
        {"title": "Outro", "start": "00:00:06", "end": "00:00:10"}
    ]

    # Mock AudioSegment instance and its properties
    mock_audio_segment = MagicMock()
    mock_audio_segment.duration_seconds = 10 # Simulate a 10-second video
    with patch('agent.AudioSegment.from_file', return_value=mock_audio_segment):
        with patch('agent.ffmpeg_extract_subclip') as mock_ffmpeg_extract_subclip:
            chapter_files = agent._split_video_into_chapters(dummy_video_path, chapters_data)
            assert len(chapter_files) == 2
            mock_ffmpeg_extract_subclip.assert_called()

def test_format_timestamp():
    from agent import _format_timestamp
    assert _format_timestamp(65) == "00:01:05"
    assert _format_timestamp(3600) == "01:00:00"
    assert _format_timestamp(0) == "00:00:00"

# Test for transcription (mocking actual transcription service)
@patch('agent.AudioSegment.from_file')
@patch('agent.AudioSegment.export')
@patch('agent.sr.Recognizer')
def test_transcribe_audio(mock_recognizer, mock_export, mock_from_file, agent):
    mock_audio_segment = MagicMock()
    mock_from_file.return_value = mock_audio_segment

    mock_recognizer_instance = mock_recognizer.return_value
    mock_recognizer_instance.record.return_value = MagicMock()
    mock_recognizer_instance.recognize_google.return_value = "Mocked transcript."

    audio_file_path = os.path.join(UPLOAD_DIR, "dummy_audio.wav")
    with open(audio_file_path, "w") as f:
        f.write("dummy audio content")

    transcript = agent._transcribe_audio(audio_file_path)
    assert transcript == "Mocked transcript."
    mock_export.assert_called_once()
    mock_recognizer_instance.recognize_google.assert_called_once()
