import openai
import os
import json

def generate_summary(text, output_lang):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set.")
    client = openai.OpenAI()
    prompt = f"""
You are an expert multilingual summarizer. Generate a complete, detailed, and rich summary that reflects the full length and depth of the video content, not just a brief summary.
Extract:
1. Key actionable takeaways (with sentiment: Positive/Negative/Neutral for each)
2. Memorable quotes (verbatim)
3. Important statistics or data points
Summarize in '{output_lang}'.
Format your response as JSON with keys: takeaways (list of objects with 'text' and 'sentiment'), quotes (list), statistics (list).
Text:
{text}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2048,
            temperature=0.4,
        )
        content = response.choices[0].message.content
        start = content.find('{')
        end = content.rfind('}') + 1
        if start != -1 and end != -1:
            json_str = content[start:end]
            data = json.loads(json_str)
            return data
        else:
            raise RuntimeError("Could not parse OpenAI response.\nRaw response:\n" + content)
    except Exception as e:
        raise RuntimeError(f"Error extracting insights with OpenAI: {e}")
