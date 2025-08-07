from langdetect import detect
import openai
import os

def detect_language(text):
    try:
        return detect(text)
    except Exception:
        return None

def translate_text(text, source_lang, target_lang):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set.")
    client = openai.OpenAI()
    prompt = f"""
Translate the following text from '{source_lang}' to '{target_lang}'.
If the text is already in '{target_lang}', return it as is.
Text:
{text}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2048,
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"Error translating text: {e}")
