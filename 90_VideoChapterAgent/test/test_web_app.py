import pytest
from fastapi.testclient import TestClient
from web_app import app
from unittest.mock import patch, MagicMock
import os
from config import UPLOAD_DIR, CHAPTERS_DIR, TRANSCRIPTS_DIR

client = TestClient(app)

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

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "Video Chapter Agent" in response.text

@patch('web_app.VideoChapterAgent')
def test_upload_video(MockVideoChapterAgent):
    mock_agent_instance = MockVideoChapterAgent.return_value
    mock_agent_instance.process_video.return_value = (
        "test_video.mp4",
        [{"title": "Intro", "start": "00:00:00", "end": "00:00:10"}],
        "This is a test transcript."
    )

    # Create a dummy file for upload
    dummy_file_path = os.path.join(UPLOAD_DIR, "test_upload.mp4")
    with open(dummy_file_path, "w") as f:
        f.write("dummy video content")

    with open(dummy_file_path, "rb") as f:
        response = client.post(
            "/upload/",
            files={"video_file": ("test_upload.mp4", f, "video/mp4")},
            data={"llm_model": "gemini-pro"}
        )

    assert response.status_code == 200
    json_response = response.json()
    assert json_response["video_filename"] == "test_video.mp4"
    assert len(json_response["chapters"]) == 1
    assert json_response["transcript"] == "This is a test transcript."
    MockVideoChapterAgent.return_value.process_video.assert_called_once()

@patch('web_app.FileResponse')
def test_download_chapter(MockFileResponse):
    # Create a dummy chapter file
    chapter_file_path = os.path.join(CHAPTERS_DIR, "test_video_chapter_1.mp4")
    with open(chapter_file_path, "w") as f:
        f.write("dummy chapter content")

    response = client.get(f"/download/chapter/{os.path.basename(chapter_file_path)}")
    assert response.status_code == 200
    MockFileResponse.assert_called_once_with(chapter_file_path, media_type="video/mp4")

@patch('web_app.FileResponse')
def test_download_transcript(MockFileResponse):
    # Create a dummy transcript file
    transcript_file_path = os.path.join(TRANSCRIPTS_DIR, "test_video.txt")
    with open(transcript_file_path, "w") as f:
        f.write("dummy transcript content")

    response = client.get(f"/download/transcript/{os.path.basename(transcript_file_path)}")
    assert response.status_code == 200
    MockFileResponse.assert_called_once_with(transcript_file_path, media_type="text/plain")
