import google.generativeai as genai
from config import GEMINI_API_KEY
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from agent import GeminiRecipeAgent
import speech_recognition as sr
from PIL import Image
import io
import argparse

genai.configure(api_key=GEMINI_API_KEY)
recipe_agent = GeminiRecipeAgent(api_key=GEMINI_API_KEY)

class RecipeRequest(BaseModel):
    ingredients: str
    filters: dict | None = None

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "Welcome to FoodRecipeBot!"})

@app.post("/recipes")
async def get_recipes(recipe_request: RecipeRequest):
    recipes = recipe_agent.generate_recipes(recipe_request.ingredients, recipe_request.filters)
    return recipes

@app.post("/voice-to-text")
async def voice_to_text(audio: UploadFile = File(...)):
    r = sr.Recognizer()
    with sr.AudioFile(audio.file) as source:
        audio_data = r.record(source)
    try:
        transcription = r.recognize_google(audio_data)
        return {"transcription": transcription}
    except sr.UnknownValueError:
        return {"transcription": None, "error": "Google Speech Recognition could not understand audio"}
    except sr.RequestError as e:
        return {"transcription": None, "error": f"Could not request results from Google Speech Recognition service; {e}"}

@app.post("/upload-image-for-ingredients")
async def upload_image_for_ingredients(image: UploadFile = File(...)):
    try:
        image_data = await image.read()
        pil_image = Image.open(io.BytesIO(image_data))
        
        vision_model = genai.GenerativeModel('gemini-pro-vision')
        prompt = "Identify all ingredients visible in this image. List them as a comma-separated string, e.g., 'chicken, rice, broccoli'. If no ingredients are found, return an empty string."
        
        response = vision_model.generate_content([prompt, pil_image])
        ingredients_text = response.text.strip()
        ingredients_list = [item.strip() for item in ingredients_text.split(',') if item.strip()]

        return {"ingredients": ingredients_list}
    except Exception as e:
        print(f"Error processing image: {e}")
        return {"ingredients": [], "error": f"Error processing image: {e}"}

def cli_app():
    print("\n--- FoodRecipeBot CLI ---")
    ingredients = input("Enter your ingredients (comma-separated): ")
    
    print("Apply filters? (y/n): ")
    apply_filters_input = input().lower()
    filters = {}
    if apply_filters_input == 'y':
        filters['vegetarian'] = input("Vegetarian? (y/n): ").lower() == 'y'
        filters['vegan'] = input("Vegan? (y/n): ").lower() == 'y'
        filters['gluten_free'] = input("Gluten-free? (y/n): ").lower() == 'y'
        filters['quick_meal'] = input("Quick meal? (y/n): ").lower() == 'y'
        meal_type = input("Meal type (breakfast, lunch, dinner, dessert, or leave empty for any): ").lower()
        if meal_type in ['breakfast', 'lunch', 'dinner', 'dessert']:
            filters['meal_type'] = meal_type
        else:
            filters['meal_type'] = None

    print("Generating recipes...")
    recipes = recipe_agent.generate_recipes(ingredients, filters)

    if recipes:
        for i, recipe in enumerate(recipes):
            print(f"\n--- Recipe {i+1}: {recipe.get('title', 'No Title')} ---")
            print(f"Description: {recipe.get('description', 'No description.')}")
            if recipe.get('calories'):
                print(f"Calories: {recipe['calories']}")
            if recipe.get('prep_time'):
                print(f"Preparation Time: {recipe['prep_time']} minutes")
            print("Ingredients:")
            for ing in recipe.get('ingredients', []):
                print(f"  - {ing}")
            print("Instructions:")
            for j, step in enumerate(recipe.get('instructions', [])):
                print(f"  {j+1}. {step}")
    else:
        print("No recipes found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FoodRecipeBot - AI Cooking Assistant")
    parser.add_argument("--cli", action="store_true", help="Run in command-line interface mode")
    args = parser.parse_args()

    if args.cli:
        cli_app()
    else:
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
