import pygame
import speech_recognition as sr
from app_uninstaller_agent import AppUninstallerAgent
from config import GREETING_MESSAGE, VOICE_INPUT_TIMEOUT, VOICE_INPUT_PHRASE_TIME_LIMIT

def init_pygame_mixer():
    """Initializes pygame mixer for audio playback."""
    pygame.mixer.init()

def play_audio(file_path):
    """Plays an audio file."""
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10) # Wait for the music to finish playing

def main():
    init_pygame_mixer()
    agent = AppUninstallerAgent()
    agent.speak(GREETING_MESSAGE)

    while True:
        print("Listening for command...")
        command = agent.listen_for_command()

        if command:
            print(f"Command received: {command}")
            agent.process_command(command)
        else:
            print("No command received or command not understood.")

if __name__ == "__main__":
    main()
