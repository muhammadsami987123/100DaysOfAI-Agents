import openai
import json

class FlashcardAgent:
    def __init__(self, openai_api_key):
        openai.api_key = openai_api_key

    def generate_flashcards(self, text, num_flashcards=5, difficulty="Medium", subject="General", language="English"):
        prompt = f"""
        You are an AI assistant specialized in creating flashcards for educational purposes.
        Generate {num_flashcards} flashcards from the following text, adhering to these specifications:

        Text: {text}
        Difficulty: {difficulty}
        Subject: {subject}
        Language: {language}

        Flashcard Styles (mix and match or choose one based on suitability):
        - Q/A format: { "type": "qa", "question": "...", "answer": "..." }
        - Fill in the blanks: { "type": "fill_in_the_blanks", "sentence": "...", "blank_word": "..." }
        - True/False: { "type": "true_false", "statement": "...", "is_true": true/false }

        Ensure flashcards are clean, clear, and structured for active recall. 
        Return the flashcards as a JSON array.
        """

        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",  # Or a more capable model if available
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that creates flashcards."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                response_format={ "type": "json_object" }
            )
            
            content = response.choices[0].message.content
            flashcards = json.loads(content)
            return flashcards.get("flashcards", flashcards) # Assuming the AI returns a dictionary with a 'flashcards' key or directly an array
        except Exception as e:
            print(f"Error generating flashcards: {e}")
            return []
