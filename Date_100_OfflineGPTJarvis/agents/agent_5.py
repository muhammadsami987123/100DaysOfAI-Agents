# agent_5.py - TextFixerAgent

from textblob import TextBlob

class TextFixerAgent:
    def fix_text(self, text):
        try:
            blob = TextBlob(text)
            corrected_text = blob.correct()
            return f"Original text: {text}\nCorrected text: {corrected_text}"
        except Exception as e:
            return f"An error occurred: {e}"
