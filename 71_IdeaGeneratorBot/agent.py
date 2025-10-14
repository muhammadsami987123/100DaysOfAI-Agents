import os
import re
from typing import List, Dict
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def build_system_prompt(topic: str, num_ideas: int = 5) -> str:
    return f"""You are IdeaGeneratorBot, an AI brainstorming assistant that generates structured, creative, and ranked ideas for any topic.\n \
User topic: {topic}\n \
Instructions:\n- Generate exactly {num_ideas} unique ideas relevant to the given topic (apps, startups, AI projects, or content).\n- For each idea, provide:\n  * Title (catchy)\n  * Description (1–2 sentences)\n  * Why It Works: GPT-style reasoning\n  * Audience\n  * Rank: (High, Medium, or Low)\n- Rank ideas by originality, feasibility, and user impact.\n- Avoid generic or repeated ideas.\n\nFormat:\nIdea 1: <Title>\nDescription: <description>\nWhy It Works: <reasoning>\nAudience: <audience>\nRank: <High/Medium/Low>\n\n(Repeat for all ideas, no extra text, just the formatted list.)"""

def parse_gemini_output(text: str) -> List[Dict]:
    ideas = []
    # Use regex to robustly match all idea chunks from large output
    ideas_chunks = re.findall(r'(Idea\s*\d+:.*?)(?=Idea\s*\d+:|\Z)', text, flags=re.DOTALL)
    for chunk in ideas_chunks:
        idea = {}
        lines = [l.strip() for l in chunk.strip().split('\n') if l.strip()]
        for line in lines:
            if line.lower().startswith("idea"):
                # Can be "Idea N: Title" or just "Idea N:" or "Idea N Title"
                sp = line.split(':', 1)
                idea["title"] = sp[1].strip() if len(sp) > 1 else sp[0].strip()
            elif line.startswith("Description:"):
                idea["description"] = line[len("Description:"):].strip()
            elif line.startswith("Why It Works:"):
                idea["why"] = line[len("Why It Works:"):].strip()
            elif line.startswith("Audience:"):
                idea["audience"] = line[len("Audience:"):].strip()
            elif line.startswith("Rank:"):
                idea["rank"] = line[len("Rank:"):].strip()
        if idea.get("title"):
            ideas.append(idea)
    return ideas

def generate_ideas(topic: str, num_ideas: int = 5) -> List[Dict]:
    if not GEMINI_API_KEY:
        return [{"title": "Error: No Gemini API Key", "description": "Set GEMINI_API_KEY in .env", "why": "", "audience": "", "rank": "Low"}]
    genai.configure(api_key=GEMINI_API_KEY)
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        prompt = build_system_prompt(topic, num_ideas=num_ideas)
        response = model.generate_content(prompt)
        print("GEMINI RAW RESPONSE:", response.text)
        return parse_gemini_output(response.text or "")
    except Exception as e:
        print("GEMINI API ERROR:", e)
        return [{
            "title": "Gemini API Error", 
            "description": str(e), 
            "why": "", "audience": "", "rank": "Low"
        }]
