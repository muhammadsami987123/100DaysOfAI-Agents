from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from config import Config
from utils.news_api import fetch_news_headlines
from utils.summary_service import SummaryService
from utils.tts_utils import generate_audio

load_dotenv()

class DailySummaryAgent:
    def __init__(self):
        self.summary_service = SummaryService()

    def get_daily_summary(self, user_tasks: dict, news_preference: str):
        # Fetch news
        news_headlines = fetch_news_headlines(news_preference)

        # Generate full summary text
        summaries = self.summary_service.get_full_summary(user_tasks, news_headlines)
        full_summary_text = f"Your Daily Tasks Summary:\n{summaries['daily_tasks_summary']}\n\nToday’s Top News:\n{summaries['todays_top_news']}"

        # Generate audio
        audio_path = generate_audio(full_summary_text)

        return {
            "daily_tasks_summary": summaries['daily_tasks_summary'],
            "todays_top_news": summaries['todays_top_news'],
            "audio_path": audio_path,
            "full_summary_text": full_summary_text # Include for TTS
        }

app = Flask(__name__)
daily_summary_agent = DailySummaryAgent()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize_day():
    user_tasks = request.json.get('tasks', {})
    news_preference = request.json.get('news_preference', Config.DEFAULT_NEWS_PREFERENCE)

    summary_data = daily_summary_agent.get_daily_summary(user_tasks, news_preference)

    return jsonify({
        "daily_tasks_summary": summary_data["daily_tasks_summary"],
        "todays_top_news": summary_data["todays_top_news"],
        "audio_path": summary_data["audio_path"]
    })
