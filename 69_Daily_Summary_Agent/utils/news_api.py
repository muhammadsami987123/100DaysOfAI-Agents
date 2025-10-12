import google.generativeai as genai
import os
from config import Config

def fetch_news_headlines(news_preference="General"):
    genai.configure(api_key=Config.GEMINI_API_KEY)
    model = genai.GenerativeModel(Config.GEMINI_MODEL)

    prompt = f"Provide {Config.MAX_NEWS_HEADLINES} top trending news headlines in the category of {news_preference}. Focus on the headline itself, no descriptions. Return as a bulleted list."
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error fetching news: {e}")
        return "Could not fetch news headlines at this time."
