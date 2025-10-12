import google.generativeai as genai
from config import Config

class SummaryService:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)

    def generate_task_summary(self, tasks: dict) -> str:
        completed_tasks = tasks.get('completed', [])
        pending_tasks = tasks.get('pending', [])

        task_summary_text = ""
        if completed_tasks:
            task_summary_text += "- ✔ Finished: " + ", ".join(completed_tasks) + "\n"
        if pending_tasks:
            task_summary_text += "- 🕓 Pending: " + ", ".join(pending_tasks)
        if not completed_tasks and not pending_tasks:
            task_summary_text = "No tasks provided for today."
        return task_summary_text

    def generate_news_summary(self, news_headlines: str) -> str:
        prompt = f"""You are DailySummaryAgent, a smart assistant that summarizes news. 
Given the following news headlines, summarize them into a short, readable summary. 
Keep the tone professional, friendly, and time-efficient. Use bullet points or paragraphs as needed. 

Today's Top News Headlines:
{news_headlines}

Generated News Summary:
"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating news summary: {e}")
            return "Could not summarize news headlines at this time."

    def get_full_summary(self, tasks: dict, news_headlines: str) -> dict:
        task_summary = self.generate_task_summary(tasks)
        news_summary = self.generate_news_summary(news_headlines)
        
        return {"daily_tasks_summary": task_summary, "todays_top_news": news_summary}
