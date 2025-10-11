import os
import google.generativeai as genai
from gtts import gTTS
import base64

class MeditationBot:
    def __init__(self):
        self.meditation_types = ["relaxation", "focus", "sleep", "stress relief"]
        self.time_options = [2, 5, 10]
        self.background_sounds = ["none", "forest_stream", "ocean_waves", "gentle_rain"]
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")

        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel('models/gemini-2.0-flash')
        else:
            self.model = None
            print("Warning: GEMINI_API_KEY is not set. LLM functionality will be limited or unavailable.")

    def greet(self):
        return "Hello there. I am MeditationBot, your calm and supportive guide for short, focused meditation sessions. How may I assist you today?"

    def ask_for_meditation_type(self):
        return f"What type of meditation do you need? You can choose from: {', '.join(self.meditation_types)}."

    def ask_for_time_option(self):
        return f"How long would you like your session to be? I can offer {', '.join(map(str, self.time_options))} minutes."

    def start_meditation(self, meditation_type, duration):
        if not self.model:
            return ["I am sorry, I cannot generate a meditation script at this time. My LLM functionality is not available."]
        
        prompt = f"You are MeditationBot — a calm, supportive guide for short, focused meditation sessions. Your job is to guide users through meditations based on their needs. Generate a {duration}-minute meditation script for {meditation_type}. The meditation should be designed to help the user with {meditation_type}. Include a variety of calming instructions, breathing exercises (e.g., deep breaths, belly breathing), body scan elements, and vivid natural imagery (e.g., a serene lake, a peaceful forest, a gentle breeze). Keep the tone consistently soothing, gentle, and mindful throughout the session. Incorporate gentle pauses. Each instruction should be a short, distinct sentence or phrase. End with a calming conclusion, such as \"Take this calm with you.\" Keep pacing slow and intentional. Output the script as a list of distinct sentences/instructions, with each element of the list being a separate instruction or a peaceful phrase."
        
        try:
            response = self.model.generate_content(prompt)
            script = response.text.strip().split('\n')
            script = [line.strip() for line in script if line.strip()]
            return script
        except Exception as e:
            print(f"Error generating meditation script with LLM: {e}")
            return ["I am sorry, I encountered an error while trying to generate your meditation. Please try again later."]

    def generate_tts_script(self, text):
        if not self.gemini_api_key:
            return None
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            # Save the audio to a BytesIO object or a temporary file
            # For simplicity, we'll return a base64 encoded string
            from io import BytesIO
            fp = BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            audio_base64 = base64.b64encode(fp.read()).decode('utf-8')
            return audio_base64
        except Exception as e:
            print(f"Error generating TTS: {e}")
            return None

    def get_supported_languages(self):
        return ["English"] # Placeholder

    def get_breathing_animation_data(self):
        # Placeholder for UI integration
        return {}
