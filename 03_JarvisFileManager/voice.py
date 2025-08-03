import speech_recognition as sr
import pyttsx3
from agent import process_command

def listen_and_respond(listen_only=False, command_text=None):
    recognizer = sr.Recognizer()
    if listen_only:
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="en-US")
            return text
        except Exception:
            return None
    else:
        if command_text is None:
            return "No command to process."
        response = process_command(command_text)
        speak(response)
        return response

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()