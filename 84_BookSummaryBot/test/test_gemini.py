import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

# Test prompt
test_prompt = """Summarize this book chapter text:

This is a test chapter about the importance of time management and provides practical strategies for organizing daily tasks effectively.

Summary type: concise

Respond with ONLY a JSON object in this exact format:
{
  "summary": "Your summary here",
  "key_points": ["point1", "point2", "point3"]
}

If summary_type is "bullet_points", put the bullet points in the summary field and leave key_points empty."""

try:
    response = model.generate_content(test_prompt)
    print("Raw response:")
    print(repr(response.text))
    print("\nFormatted response:")
    print(response.text)
except Exception as e:
    print(f"Error: {e}")
