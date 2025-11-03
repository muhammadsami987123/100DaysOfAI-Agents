import speech_recognition as sr
import pygame
import os
import random
from pydub import AudioSegment
from pydub.playback import play
from config import Config
from utils.llm_service import LLMService

class JarvisMusicController:
    def __init__(self):
        pygame.mixer.init()
        self.recognizer = sr.Recognizer()
        self.llm_service = LLMService()
        self.music_files = self._load_music_files()
        self.current_song_index = 0
        self.is_playing = False
        self.current_playback = None # To hold the pydub playback object

    def _load_music_files(self):
        music_path = Config.MUSIC_DIR
        if not os.path.exists(music_path):
            os.makedirs(music_path)
            print(f"Created music directory: {music_path}. Please add music files here.")
            return []

        files = []
        for root, _, filenames in os.walk(music_path):
            for filename in filenames:
                if any(filename.endswith(ext) for ext in Config.SUPPORTED_AUDIO_FORMATS):
                    files.append(os.path.join(root, filename))
        return files

    def _get_song_name(self, file_path):
        return os.path.basename(file_path).split('.')[0]

    def _play_song(self, index=None):
        if not self.music_files:
            print("No music files found. Please add songs to the 'music' directory.")
            return

        if index is not None:
            self.current_song_index = index
        elif self.current_playback is None: # If no song is currently loaded, play the first one or a random one
            self.current_song_index = random.randint(0, len(self.music_files) - 1)

        song_path = self.music_files[self.current_song_index]
        print(f"Now playing: \"{self._get_song_name(song_path)}\"")

        try:
            # Stop any currently playing pydub audio
            if self.current_playback and self.current_playback.is_playing():
                self.current_playback.stop()

            audio = AudioSegment.from_file(song_path)
            self.current_playback = play(audio) # Play in a non-blocking way
            self.is_playing = True
        except Exception as e:
            print(f"Error playing song {self._get_song_name(song_path)}: {e}")
            self.is_playing = False

    def _pause_song(self):
        if self.is_playing and self.current_playback:
            self.current_playback.pause()
            self.is_playing = False
            print("Playback paused.")

    def _unpause_song(self):
        if not self.is_playing and self.current_playback:
            self.current_playback.play()
            self.is_playing = True
            print(f"Resuming: \"{self._get_song_name(self.music_files[self.current_song_index])}\"")

    def _stop_song(self):
        if self.current_playback:
            self.current_playback.stop()
            self.is_playing = False
            self.current_playback = None
            print("Playback stopped.")

    def _next_song(self):
        if not self.music_files:
            print("No music files to skip.")
            return
        self._stop_song()
        self.current_song_index = (self.current_song_index + 1) % len(self.music_files)
        self._play_song(self.current_song_index)
        print(f"Skipped to: \"{self._get_song_name(self.music_files[self.current_song_index])}\"")

    def _previous_song(self):
        if not self.music_files:
            print("No music files to go back to.")
            return
        self._stop_song()
        self.current_song_index = (self.current_song_index - 1 + len(self.music_files)) % len(self.music_files)
        self._play_song(self.current_song_index)
        print(f"Going back to: \"{self._get_song_name(self.music_files[self.current_song_index])}\"")

    def listen_for_command(self):
        with sr.Microphone() as source:
            print("> Listening for command...")
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                command = self.recognizer.recognize_google(audio)
                print(f"User: {command}")
                return command
            except sr.UnknownValueError:
                print("Could not understand audio")
                return ""
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                return ""
            except Exception as e:
                print(f"An error occurred during voice recognition: {e}")
                return ""

    def process_command(self, command: str):
        if not command:
            return

        # First, try direct keyword matching
        command_lower = command.lower()
        if "play" in command_lower:
            if not self.is_playing:
                self._play_song()
            else:
                self._unpause_song()
        elif "pause" in command_lower:
            self._pause_song()
        elif "next" in command_lower or "skip" in command_lower:
            self._next_song()
        elif "previous" in command_lower or "back" in command_lower:
            self._previous_song()
        elif "stop" in command_lower:
            self._stop_song()
        else:
            # If no direct match, use LLM for interpretation
            interpreted_command = self.llm_service.interpret_command(command)
            if "play" in interpreted_command:
                if not self.is_playing:
                    self._play_song()
                else:
                    self._unpause_song()
            elif "pause" in interpreted_command:
                self._pause_song()
            elif "next" in interpreted_command or "skip" in interpreted_command:
                self._next_song()
            elif "previous" in interpreted_command or "back" in interpreted_command:
                self._previous_song()
            elif "stop" in interpreted_command:
                self._stop_song()
            else:
                print(f"Unrecognized command: {command}")

