import json

# Test the JSON parsing logic with the actual Gemini response
test_response = '```json\n{\n  "summary": "This chapter emphasizes the significance of time management and offers effective strategies for daily task organization.",\n  "key_points": [\n    "Importance of time management",\n    "Organizing daily tasks",\n    "Practical strategies for effectiveness"\n  ]\n}\n```'

print("Original response:")
print(repr(test_response))

# Apply the same cleaning logic
cleaned_text = test_response.strip()

# Remove markdown code blocks
if cleaned_text.startswith('```json'):
    cleaned_text = cleaned_text[7:]
elif cleaned_text.startswith('```'):
    cleaned_text = cleaned_text[3:]

if cleaned_text.endswith('```'):
    cleaned_text = cleaned_text[:-3]

cleaned_text = cleaned_text.strip()

print("\nCleaned text:")
print(repr(cleaned_text))

# Try to find JSON object in the response
start_idx = cleaned_text.find('{')
end_idx = cleaned_text.rfind('}')

if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
    json_text = cleaned_text[start_idx:end_idx+1]
    print(f"\nExtracted JSON:")
    print(repr(json_text))
    
    try:
        parsed_content = json.loads(json_text)
        print(f"\nParsed successfully:")
        print(parsed_content)
    except json.JSONDecodeError as e:
        print(f"\nJSON parsing error: {e}")
else:
    print("\nNo JSON object found")
