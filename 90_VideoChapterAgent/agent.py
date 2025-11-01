import os
import json
from pydub import AudioSegment
import speech_recognition as sr
import ffmpeg
from utils.llm_service import LLMService
from config import PROMPTS_DIR, UPLOAD_DIR, CHAPTERS_DIR, TRANSCRIPTS_DIR

class VideoChapterAgent:
    def __init__(self, llm_type: str = "gemini"):
        self.llm_service = LLMService(llm_type)
        self.chapter_prompt_path = os.path.join(PROMPTS_DIR, "chapter_prompt.txt")

    def _load_prompt(self, prompt_path: str) -> str:
        with open(prompt_path, "r") as f:
            return f.read()

    def _extract_audio(self, video_path: str, audio_output_path: str):
        ffmpeg.input(video_path).output(audio_output_path).run(overwrite_output=True)

    def _transcribe_audio(self, audio_path: str) -> str:
        r = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio = r.record(source)  # read the entire audio file
        try:
            return r.recognize_google(audio)
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Speech recognition service error; {e}"

    def _generate_chapters_from_transcript(self, transcript: str, llm_model: str) -> list:
        prompt_template = self._load_prompt(self.chapter_prompt_path)
        prompt = prompt_template.replace("{transcript}", transcript)
        response_text = self.llm_service.generate_content(prompt, llm_model)

        chapters = []
        # Parse the LLM response. Assuming it's line-by-line as in the prompt example.
        # Example format: Chapter 1: Introduction (00:00:00-00:02:15)
        for line in response_text.split('\n'):
            if line.strip().startswith("Chapter"):
                try:
                    parts = line.split(": ", 1)
                    title_and_time = parts[1].strip()
                    title_match = title_and_time.split(" (")[0]
                    time_match = title_and_time.split(" (")[1].strip(")")
                    start_time_str, end_time_str = time_match.split("-")

                    chapters.append({"title": title_match, "start": start_time_str, "end": end_time_str})
                except IndexError:
                    print(f"Warning: Could not parse chapter line: {line}")
        return chapters

    def _format_timestamp(self, seconds: float) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02}:{minutes:02}:{secs:02}"

    def _split_video_into_chapters(self, video_path: str, chapters: list):
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        output_dir = os.path.join(CHAPTERS_DIR, base_name)
        os.makedirs(output_dir, exist_ok=True)

        chapter_files = []
        for i, chapter in enumerate(chapters):
            start_time_str = chapter["start"]
            end_time_str = chapter["end"]
            title = chapter["title"]
            output_path = os.path.join(output_dir, f"{base_name}_chapter_{i+1}.mp4")

            # Convert HH:MM:SS to seconds for ffmpeg
            start_seconds = sum(x * int(t) for x, t in zip([3600, 60, 1], start_time_str.split(':')))
            end_seconds = sum(x * int(t) for x, t in zip([3600, 60, 1], end_time_str.split(':')))

            try:
                ffmpeg.input(video_path, ss=start_seconds, to=end_seconds).output(output_path).run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
                chapter_files.append(os.path.basename(output_path))
                print(f"Split chapter: {title} from {start_time_str} to {end_time_str}")
            except ffmpeg.Error as e:
                print(f"Error splitting chapter {title}: {e.stderr.decode()}")
                # Optionally, log the error and continue or re-raise

        return chapter_files

    def process_video(self, video_path: str, llm_model: str):
        video_filename = os.path.basename(video_path)
        base_name = os.path.splitext(video_filename)[0]
        audio_output_path = os.path.join(TRANSCRIPTS_DIR, f"{base_name}.wav")
        transcript_file_path = os.path.join(TRANSCRIPTS_DIR, f"{base_name}.txt")

        # Ensure directories exist
        os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)
        os.makedirs(CHAPTERS_DIR, exist_ok=True)

        # Extract audio
        self._extract_audio(video_path, audio_output_path)

        # Transcribe audio
        transcript = self._transcribe_audio(audio_output_path)
        with open(transcript_file_path, "w") as f:
            f.write(transcript)

        # Generate chapters
        chapters = self._generate_chapters_from_transcript(transcript, llm_model)

        # Split video into chapters
        chapter_files = self._split_video_into_chapters(video_path, chapters)

        return {"video_filename": video_filename, "transcript": transcript, "chapters": chapters, "chapter_files": chapter_files}

