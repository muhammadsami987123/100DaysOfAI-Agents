# 🍽️ FoodRecipeBot - Day 67 of #100DaysOfAI-Agents

<div align="center">

![FoodRecipeBot Banner](https://img.shields.io/badge/FoodRecipeBot-Day%2067-blue?style=for-the-badge&logo=utensils&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-API-orange?style=for-the-badge&logo=google&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20Framework-red?style=for-the-badge&logo=fastapi&logoColor=white)

**Transform your ingredients into delightful recipes with AI-powered suggestions!**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎭 Examples](#-examples-usage) • [🏗️ Architecture](#-project-architecture) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is FoodRecipeBot?

FoodRecipeBot is an intelligent AI cooking assistant designed to revolutionize your kitchen experience. It leverages advanced AI to provide personalized recipe suggestions based on the ingredients you already possess. This agent helps users efficiently plan meals, significantly reduce food waste, and discover a world of healthy, creative culinary options tailored to their unique preferences.

### 🌟 Key Highlights

-   **🍳 Flexible Input Methods**: Seamlessly input your ingredients via a typed list, voice-to-text (speech recognition), or by uploading an image (powered by Google Gemini Vision API).
-   **🥗 Intelligent Recipe Suggestions**: Receive 1-5 highly relevant and detailed recipe suggestions, each featuring a clear title, brief description, comprehensive ingredient list (with missing items highlighted), and step-by-step instructions.
-   **🌶️ Advanced Filtering**: Precisely refine your recipe search using various filters, including dietary needs (Vegetarian, Vegan, Gluten-free), meal quickness (Quick meals), and specific meal types (Breakfast, Lunch, Dinner, Dessert).
-   **⏱️ Optional Recipe Details**: Gain additional insights with optional information such as estimated preparation time and calorie counts for each suggested recipe.
-   **💬 Interactive Support**: Engage in future chat-based follow-up questions and request real-time modifications to generated recipes.
-   **💻 Dual Interface**: Choose between a modern, professional web-based User Interface (UI) and a robust, functional terminal-based application for quick interactions.
-   **💾 Recipe Management**: Easily download your generated recipe suggestions as a structured JSON file for offline access or future reference.

## 🎯 Features

### 🚀 Core Functionality

-   ✅ **AI-Powered Recipe Generation**: Utilizes the Google Gemini API to generate innovative and contextually appropriate recipe ideas.
-   ✅ **Multi-Modal Ingredient Input**: Supports diverse input formats—text, spoken word, and visual data—to cater to all user preferences.
-   ✅ **Dynamic Recipe Filtering**: Enables users to apply multiple filters to obtain highly customized recipe results.
-   ✅ **Comprehensive Recipe Display**: Presents each recipe in an easy-to-read format, detailing every step and ingredient.
-   ✅ **Intuitive Missing Ingredient Highlighting**: Clearly indicates which ingredients are not part of the user's initial input, aiding in meal planning.
-   ✅ **Adaptive User Interface**: Ensures a consistent and optimized user experience across various devices with a responsive design.

### ⚙️ Input & Output Methods

| Method               | Description                                            | Technology Used           |
|----------------------|--------------------------------------------------------|---------------------------|
| **Typed List**       | Direct text entry of ingredients.                      | HTML `<textarea>`         |
| **Voice-to-Text**    | Speech input transcribed into a text list of ingredients. | `SpeechRecognition` (Python) |
| **Image Upload**     | Image analysis to identify visible ingredients.      | Google Gemini Vision API, `Pillow` (Python) |
| **Structured Output**| Recipes delivered in a standardized, machine-readable format. | JSON                      |
| **Recipe Download**  | Option to save generated recipes locally.              | JavaScript Blob API       |

### 🎨 UI/UX Enhancements

| Feature                  | Description                                              | Styling & Implementation               |
|--------------------------|----------------------------------------------------------|----------------------------------------|
| **Modern Web UI**        | Clean, professional, white-based theme with minimal design. | Tailwind CSS, Custom CSS             |
| **Loader Button**        | Visual feedback (spinner) during API calls and processing. | HTML, Tailwind CSS, Custom CSS, JavaScript |
| **Three-Column Layout**  | Recipe suggestions displayed in a responsive grid for visual appeal. | Tailwind CSS Grid                      |
| **Intuitive Icons**      | Visual cues for key information like ingredients and cook time. | Font Awesome, Tailwind CSS             |
| **Enhanced Form Elements**| Modern styling for text areas, checkboxes, and select dropdowns. | Tailwind CSS                           |

## 🚀 Quick Start

Follow these steps to set up and run the FoodRecipeBot on your local machine.

### 📋 Prerequisites

-   **Python 3.8+**: Ensure Python is installed and accessible via your PATH.
-   **Google Gemini API Key**: Obtain your API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
-   **Microphone**: Required for utilizing the voice input feature.
-   **Internet Connection**: Essential for AI processing (Gemini API) and speech recognition.

### ⚡ Installation

```bash
# 1. Navigate to the project directory
cd 67_FoodRecipeBot

# 2. Create and activate a Python virtual environment (recommended)
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 3. Install required Python dependencies
pip install -r requirements.txt

# Note for Windows users regarding Pyaudio (for SpeechRecognition):
# If `pip install pyaudio` fails, you might need to install it via pipwin:
# pip install pipwin
# pipwin install pyaudio
```

### 🔑 Configuration

1.  **Generate your Google Gemini API Key**:
    *   Visit the [Google AI Studio](https://aistudio.google.com/app/apikey) and create a new API key if you don't already have one.

2.  **Set the API Key as an Environment Variable**:
    *   Create a file named `.env` in the root directory of `67_FoodRecipeBot` (at the same level as `main.py`).
    *   Add the following line, replacing `YOUR_GEMINI_API_KEY` with your actual key:
    ```
    GEMINI_API_KEY='YOUR_GEMINI_API_KEY'
    ```
    *   This ensures your API key is loaded securely without being hardcoded.

### 🎯 First Run

#### 🌐 Option 1: Web Interface (Recommended)

1.  Ensure your virtual environment is active and you are in the `67_FoodRecipeBot` directory.
2.  Start the FastAPI server:
    ```bash
    uvicorn main:app --reload
    ```
    (The `--reload` flag enables automatic server restarts on code changes, useful during development.)
3.  Open your web browser and navigate to: `http://127.0.0.1:8000`

#### 💻 Option 2: Terminal Interface

1.  Ensure your virtual environment is active and you are in the `67_FoodRecipeBot` directory.
2.  Run the application in CLI mode:
    ```bash
    python main.py --cli
    ```
3.  Follow the interactive prompts in your terminal to input ingredients and apply filters. Recipes will be displayed directly.

## 🎭 Examples & Usage

### 🌐 Web Interface Walkthrough

The web interface provides a rich, interactive experience for recipe generation:

1.  **📝 Input Ingredients**: Use the text area to type a list of ingredients you have (e.g., "chicken, tomatoes, pasta, basil").
2.  **🎤 Voice Input**: Click the "🎤 Voice Input" button to use your microphone. Speak your ingredients clearly, and the system will transcribe them automatically.
3.  **📸 Image Upload**: Click "Choose File" to upload an image of your ingredients. The Gemini Vision API will analyze the image and populate the ingredient list.
4.  **⚙️ Apply Filters**: Select desired dietary filters (e.g., Vegetarian, Vegan) and choose a specific Meal Type (e.g., Breakfast, Dinner) to narrow down suggestions.
5.  **🚀 Get Recipes**: Click the "<i class="fas fa-search"></i> Get Recipes" button. A loader will appear, indicating that recipes are being generated.
6.  **📊 View Results**: Relevant recipe suggestions will be displayed in a clean, three-column card layout.
7.  **💾 Download Recipes**: After recipes are displayed, a "<i class="fas fa-download"></i> Download Recipes" button will appear, allowing you to save all generated recipes as a JSON file.

### 💻 Terminal Interface Guide

For quick, text-based interactions, the terminal interface is efficient:

```bash
python main.py --cli
```

Upon execution, you will be prompted to:
-   Enter your ingredients (e.g., `eggs, milk, flour`)
-   Choose whether to apply filters (`y/n`)
-   If filters are applied, you'll be guided through options for vegetarian, vegan, gluten-free, quick meal, and meal type.

The generated recipes, including titles, descriptions, ingredients, instructions, calories, and prep time, will be presented directly in your terminal.

## 🏗️ Project Architecture

### 📁 File Structure

```
67_FoodRecipeBot/
├── 📄 main.py                   # Main application entry point, FastAPI server setup, CLI handler
├── ⚙️ config.py                 # Centralized configuration management, Gemini API key loading
├── 🤖 agent.py                 # Core AI logic: Google Gemini API integration for recipe generation and image analysis
├── 📋 requirements.txt          # Specifies all Python dependencies for easy installation
├── 📚 templates/                # Contains HTML templates for the web user interface
│   └── index.html              # The main web page for interacting with the FoodRecipeBot
├── 🎨 static/                   # Directory for static assets like JavaScript and CSS
│   └── js/
│       └── script.js           # Frontend JavaScript logic for UI interactivity and API calls
├── 📄 README.md                # This comprehensive project documentation
└── 📄 .env                     # Stores environment variables, including the sensitive Gemini API key
```

### 🔧 Technical Stack

| Component            | Technology                | Purpose                                                         |
|----------------------|---------------------------|-----------------------------------------------------------------|
| **Backend Framework**| Python 3.8+, FastAPI      | Provides a robust and high-performance foundation for the API and web server. |
| **AI Engine**        | Google Gemini API         | Powers intelligent recipe generation and advanced image recognition. |
| **Speech-to-Text**   | `SpeechRecognition` (Python)| Transcribes spoken audio into text for ingredient input.         |
| **Image Processing** | `Pillow` (Python)         | Facilitates handling and preparation of image files for the Gemini Vision API. |
| **Web Frontend**     | HTML5, Tailwind CSS       | Delivers a modern, visually appealing, and responsive user interface. |
| **Client-side Logic**| Vanilla JavaScript        | Manages all interactive elements, dynamic content updates, and asynchronous API communication. |
| **Environment Mgmt.**| `python-dotenv`           | Securely loads environment variables to manage sensitive information like API keys. |
| **ASGI Server**      | `Uvicorn`                 | A lightning-fast ASGI server that runs the FastAPI application. |
| **Templating Engine**| `Jinja2`                  | Renders dynamic HTML content for the web interface.             |
| **Data Validation**  | `Pydantic`                | Ensures data integrity for API requests and responses.          |

## 🛠️ Troubleshooting

### Common Issues & Solutions

| Issue                                                | Probable Cause                                                      | Solution                                                                                                                               |
|------------------------------------------------------|---------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| `RuntimeError: Directory 'static' does not exist`      | The path for static or template files in `main.py` is incorrect relative to the execution directory. | Ensure `app.mount("/static", StaticFiles(directory="static"))` and `Jinja2Templates(directory="templates")` use correct relative paths. |
| `Error fetching recipes.` (on frontend)             | Issues with API response parsing, or unexpected data format from Gemini. | Check the terminal logs for the exact Gemini API response. Verify `agent.py`'s JSON parsing logic and ingredient key standardization. |
| `Error: Could not decode JSON from Gemini API response.`| Gemini API output contains non-standard JSON, extra text, or formatting. | `agent.py` includes robust regex-based JSON extraction. Review the raw Gemini response in terminal logs for anomalies.                    |
| `No module named 'pyaudio'`                          | `pyaudio` (a dependency for `SpeechRecognition` on some systems) is not installed. | On Windows, install `pipwin` (`pip install pipwin`) then use it to install `pyaudio` (`pipwin install pyaudio`).                     |
| `Google Gemini API Key not found`                    | The `GEMINI_API_KEY` environment variable is missing or incorrect. | Verify that a `.env` file exists in the `67_FoodRecipeBot` directory with `GEMINI_API_KEY='YOUR_KEY'`, or set it as a system environment variable. |
| Unformatted UI / Incorrect styles on web page       | Tailwind CSS is not loading or its classes are misapplied.          | Confirm the Tailwind CDN link in `index.html` is correct. Inspect browser developer tools for CSS loading errors and check class names in `index.html` and `script.js`. |

### Performance Optimization Tips

-   **Concise Ingredient Input**: Provide clear and to-the-point ingredient lists to optimize AI processing time.
-   **Targeted Filters**: Utilize the available filters effectively to narrow down recipe suggestions, improving relevance and reducing generation load.
-   **Stable Internet Connection**: A reliable internet connection is crucial for seamless communication with the Google Gemini API, ensuring optimal performance.

## 🔮 Future Enhancements

-   **Interactive Chat-based Modifications**: Implement a dynamic chat interface allowing users to refine recipes or ask follow-up questions.
-   **Advanced Image Recognition**: Further enhance the accuracy and scope of ingredient detection from diverse image inputs.
-   **User Accounts & Personalization**: Introduce user registration, allowing for saved favorite recipes, personalized meal plans, and cooking history.
-   **Detailed Nutritional Information**: Expand on optional recipe details to include comprehensive nutritional breakdowns (e.g., carbs, protein, fats).
-   **Recipe Scaling**: Add functionality to adjust recipe quantities based on desired serving sizes.
-   **Automated Shopping List Generation**: Enable users to generate a shopping list directly from selected recipes.

## 🤝 Contributing

We welcome and encourage contributions to enhance the FoodRecipeBot. If you have valuable suggestions, discover bugs, or wish to contribute code, please follow these guidelines:

1.  **Fork the repository** on GitHub.
2.  **Create a dedicated feature branch**: For example, `git checkout -b feature/add-new-filter`.
3.  **Implement your changes** and ensure they are thoroughly tested.
4.  **Commit your changes** with a clear and descriptive message: `git commit -m 'feat: Add new filtering option for recipes'`.
5.  **Push your branch** to your forked repository: `git push origin feature/add-new-filter`.
6.  **Open a Pull Request** against the main repository, providing a detailed description of your contributions.

## 📄 License

This project is proudly open-sourced under the **MIT License**.

---

<div align="center">

**Made with ❤️ by Muhammad Sami Asghar Mughal as part of the #100DaysOfAI-Agents challenge**

*Day 67 of 100 - Cooking up AI innovation, one recipe at a time!* 

</div>
