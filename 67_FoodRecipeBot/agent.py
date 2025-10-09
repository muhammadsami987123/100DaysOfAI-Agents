import google.generativeai as genai
import json
import re

class GeminiRecipeAgent:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-001')

    def generate_recipes(self, ingredients: str, filters: dict = None, num_recipes: int = 3):
        prompt = f"""Generate {num_recipes} recipes based on the following ingredients: {ingredients}.\n
Each recipe should include a title (label this 'title'), a brief description, a list of ingredients (label this 'ingredients' and ensure it is an array of strings, e.g., ["1 cup rice", "2 mushrooms"]), and step-by-step instructions. Also include 'calories' and 'prep_time' (estimated preparation time in minutes). If an ingredient is missing from the user's provided list, highlight it in the ingredients list.

Apply the following filters if provided: {filters}.

Respond only with a JSON array of objects, where each object represents a recipe. Wrap the JSON in a markdown code block like this:
```json
[{{"title": "..."}}]
```"""
        
        # Add filtering logic based on the 'filters' dictionary
        if filters:
            filter_str = ", ".join([f"{k}: {v}" for k, v in filters.items() if v])
            if filter_str:
                prompt += f"\nFilters: {filter_str}"

        response = self.model.generate_content(prompt)
        
        recipes = []
        # Attempt to extract JSON from a markdown code block if direct parsing fails
        try:
            recipes = json.loads(response.text)
        except json.JSONDecodeError:
            # Try to find JSON within a markdown code block, being more flexible
            match = re.search(r'.*?```json\n([\s\S]*?)\n```.*?', response.text, re.DOTALL)
            if match:
                json_string = match.group(1)
                try:
                    recipes = json.loads(json_string)
                except json.JSONDecodeError:
                    print("Error: Could not decode JSON from extracted markdown code block.")
                    print(json_string)
            else:
                print("Error: No JSON markdown code block found in Gemini API response.")
            
            print("Original Gemini API response:")
            print(response.text)

        # Standardize ingredient keys and format
        for recipe in recipes:
            # Rename 'recipe_title' to 'title' if present
            if 'recipe_title' in recipe:
                recipe['title'] = recipe.pop('recipe_title')
            
            # Standardize 'ingredients_needed' to 'ingredients'
            if 'ingredients_needed' in recipe:
                recipe['ingredients'] = recipe.pop('ingredients_needed')
            
            # Ensure 'ingredients' is a list of strings
            if 'ingredients' in recipe and isinstance(recipe['ingredients'], dict):
                recipe['ingredients'] = [f"{value}" for key, value in recipe['ingredients'].items()]
            
            print(f"Processed ingredients for {recipe.get('title', 'unknown')}: {recipe.get('ingredients')}")
        
        return recipes
