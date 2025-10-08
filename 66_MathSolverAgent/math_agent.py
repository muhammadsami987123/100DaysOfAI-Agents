import google.generativeai as genai
import traceback
from config import Config

class MathSolverAgent:
    def __init__(self):
        Config.validate()
        # Debug print the API key (partially masked)
        if Config.GEMINI_API_KEY:
            print(f"DEBUG: Gemini API Key loaded: {Config.GEMINI_API_KEY[:5]}...{Config.GEMINI_API_KEY[-5:]}")
        else:
            print("DEBUG: Gemini API Key is not set in config.py")

        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(model_name="gemini-2.0-flash-001")

    def solve_math_problem(self, problem: str):
        """
        Solves a math problem step-by-step using the Google Gemini API in streaming mode.
        """
        
        generation_config = {
            "temperature": 0.7,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]

        self.model = genai.GenerativeModel(model_name="gemini-2.0-flash-001",
                                      generation_config=generation_config,
                                      safety_settings=safety_settings)

        prompt_parts = [
            "You are MathSolverAgent, an AI chatbot that solves math problems step-by-step with clear logic and explanation. ",
            "You should:\n",
            "- Accept input as text (equations, expressions, word problems)\n",
            "- Return step-by-step solution with explanation\n",
            "- Support topics like: Arithmetic, Algebra, Geometry, Calculus, Word problems\n",
            "- Handle LaTeX input/output if needed\n",
            "- Return final answer at the end\n",
            "- Show visual graph description (if applicable)\n",
            "- Allow English or Urdu input\n",
            "- Return responses in a structured, clean format.\n",
            "Solve the following math problem:\n",
            f"Problem: {problem}\n",
            "Please provide the solution step-by-step, followed by the final answer. If a visual graph is applicable, describe it."
        ]
        
        steps = []
        final_answer = ""
        graph_description = ""

        try:
            response = self.model.generate_content(prompt_parts, stream=True)
            for chunk in response:
                text = chunk.text
                if "Step" in text and ":" in text:
                    steps.append(text)
                elif "Final Answer:" in text:
                    final_answer = text.replace("Final Answer:", "").strip()
                elif "Graph:" in text:
                    graph_description = text.replace("Graph:", "").strip()
                else:
                    if text.strip(): 
                        steps.append(text.strip())

        except Exception as e:
            print(f"ERROR: Exception during Gemini API call: {e}")
            traceback.print_exc()
            steps = [f"Error: {e}. Could not solve the problem. Please check your API key and problem statement."]
            final_answer = "Error"

        return {"steps": steps, "final_answer": final_answer, "graph_description": graph_description}
