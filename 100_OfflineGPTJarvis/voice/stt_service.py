# stt_service.py

import speech_recognition as sr

class STTService:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self):
        with sr.Microphone() as source:
            print("Listening for your command...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            command = self.recognizer.recognize_whisper(audio, language="english")
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            print(f"Could not request results from the speech recognition service; {e}")
            return None
