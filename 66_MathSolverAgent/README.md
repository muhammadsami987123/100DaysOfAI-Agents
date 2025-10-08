# MathSolverAgent

## Day 66 Challenge — AI Agent Series

### Task
Solve math equations step-by-step with clear logic and explanation.

### Purpose
To assist users with solving mathematical problems by breaking them into clear, understandable steps — making learning interactive and helpful, not just result-based.

### Features
- **Web UI:** Intuitive web interface for input and output.
- **Step-by-step solutions:** Provides detailed explanations for each step.
- **Supports diverse topics:** Arithmetic, Algebra, Geometry, Calculus, Word problems.
- **LaTeX support:** Handles LaTeX input/output for mathematical expressions.
- **Visual graph descriptions:** Describes applicable visual graphs.
- **Multilingual support:** Accepts English or Urdu input.
- **Structured output:** Returns responses in a clean, organized format.
- **Streaming mode:** Uses Google Gemini API in streaming mode for real-time explanations.

### Setup
1. Navigate to the `66_MathSolverAgent` directory.
2. Run `install.bat` (Windows) to set up the virtual environment and install dependencies.
3. Create a `.env` file in the `66_MathSolverAgent` directory and add your Google Gemini API key:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

### Usage
1. Run `install.bat` once to set up the environment and build the frontend.
2. Run `start.bat` (Windows) from the `66_MathSolverAgent` directory to launch the backend server.
3. Open your web browser and navigate to `http://localhost:8000`. The UI will be accessible directly.
4. Enter your math problem in the input box and click "Solve Problem".
5. If you make changes to the frontend (`mathmate-ui` files), you'll need to rebuild and recopy them:
   a. Navigate to `66_MathSolverAgent\mathmate-ui`.
   b. Run `npm run build`.
   c. Navigate back to `66_MathSolverAgent`.
   d. Run `xcopy /E /I /Y mathmate-ui\dist static\assets`.
   e. Restart the backend server (`start.bat`).

### Example Input (via Web UI):
`Solve 3x² - 12x = 0`

### Example Output (via Web UI):
(Displayed step-by-step in the browser, followed by the final answer)

### Project Structure
```
66_MathSolverAgent/
├── main.py                 # FastAPI application to serve the UI and API
├── config.py               # Configuration settings (API keys, host, port)
├── math_agent.py           # Core logic for solving math problems using Gemini API
├── requirements.txt        # Python dependencies
├── install.bat             # Windows installation script
├── start.bat               # Windows startup script
├── static/
│   └── assets/             # Frontend build files (HTML, CSS, JS)
└── README.md               # Project documentation
```
