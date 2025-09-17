import google.generativeai as genai
from config import Config

class TextAnalyzerAgent:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash-001')

    def analyze_text(self, text):
        prompt = f"""
        Analyze the tone and sentiment of the following text.
        Provide a concise summary of the analysis, then detail the tone and sentiment.
        The output should be structured as follows:

        Summary: [Concise summary of the analysis]
        Tone: [Identified tone(s), e.g., Formal, Informal, Optimistic, Concerned, Neutral]
        Sentiment: [Identified sentiment, e.g., Positive, Negative, Neutral, Mixed]

        Text:
        "{text}"
        """
        try:
            response = self.model.generate_content(prompt)
            if response and response.text:
                return response.text
            else:
                return "Summary: Analysis failed. No text response from API.\nTone: N/A\nSentiment: N/A"
        except Exception as e:
            return f"Summary: Analysis encountered an error. ({str(e)})\nTone: N/A\nSentiment: N/A"
