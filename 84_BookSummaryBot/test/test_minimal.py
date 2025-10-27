import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

# Very simple test
simple_prompt = "Please respond with this JSON: {\"summary\": \"test summary\", \"key_points\": [\"point1\"]}"

print("Testing with simple prompt:")
print(f"Prompt: {simple_prompt}")

try:
    response = model.generate_content(simple_prompt)
    print(f"Response: {repr(response.text)}")
    print(f"Response length: {len(response.text)}")
    
    # Try to parse as JSON with our cleaning logic
    import json
    try:
        # Clean up the response text
        cleaned_text = response.text.strip()
        
        # Remove markdown code blocks
        if cleaned_text.startswith('```json'):
            cleaned_text = cleaned_text[7:]
        elif cleaned_text.startswith('```'):
            cleaned_text = cleaned_text[3:]
        
        if cleaned_text.endswith('```'):
            cleaned_text = cleaned_text[:-3]
        
        cleaned_text = cleaned_text.strip()
        print(f"Cleaned text: {repr(cleaned_text)}")
        
        # Try to find JSON object in the response
        start_idx = cleaned_text.find('{')
        end_idx = cleaned_text.rfind('}')
        
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            json_text = cleaned_text[start_idx:end_idx+1]
            print(f"Extracted JSON: {repr(json_text)}")
            parsed = json.loads(json_text)
            print(f"Parsed successfully: {parsed}")
        else:
            print("No JSON object found")
            
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
