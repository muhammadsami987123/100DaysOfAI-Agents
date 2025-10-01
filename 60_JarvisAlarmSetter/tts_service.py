import pyttsx3
from gtts import gTTS
import os

class TTSService:
    def __init__(self):
        self.engine = pyttsx3.init()
        # You can configure voice properties here
        # voices = self.engine.getProperty('voices')
        # self.engine.setProperty('voice', voices[0].id) # Example: set to a female voice

    def speak(self, text, save_audio=False, filename="response.mp3"):
        print(f"Speaking: {text}")
        if save_audio:
            # Using gTTS for higher quality audio synthesis and saving to file
            tts = gTTS(text=text, lang='en')
            tts.save(filename)
            os.system(f"start {filename}") # For Windows, use 'afplay' on macOS, 'xdg-open' on Linux
        else:
            # Using pyttsx3 for local, faster speech (though often lower quality)
            self.engine.say(text)
            self.engine.runAndWait()
