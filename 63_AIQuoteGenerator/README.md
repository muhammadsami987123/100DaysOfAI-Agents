
# 🌟 AIQuoteGenerator — Day 63 of the Agent Creation Challenge

<div align="center">

![AIQuoteGenerator Banner](https://img.shields.io/badge/AIQuoteGenerator-Day%2063-blueviolet?style=for-the-badge&logo=sparkfun&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-API-orange?style=for-the-badge&logo=google&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20Framework-red?style=for-the-badge&logo=fastapi&logoColor=white)

**Your daily spark, one quote at a time — generate inspirational quotes with AI.**

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [💡 Usage](#-usage) • [🛠️ Technology Stack](#-technology-stack) • [📦 Installation](#-installation) • [⚙️ Configuration](#-configuration) • [🐛 Troubleshooting](#-troubleshooting) • [🤝 Contributing](#-contributing) • [📄 License](#-license)

</div>

---

## ✨ What is AIQuoteGenerator?

AIQuoteGenerator is a UI-based intelligent agent designed to generate powerful, motivational, deep, and meaningful quotes using Google's Gemini AI. It provides a modern, aesthetic user interface where users can select a mood or theme, choose a tone, and define the output format (text only, image quote, or tweet-ready) to get a fresh dose of inspiration daily.

### 🌟 Key Highlights

- **🧠 AI-Powered Quote Generation**: Utilizes Google Gemini API for high-quality, context-aware quotes.
- **🎨 Premium UI/UX**: Modern black theme with elegant gold and white highlights, 3D effects, and fully responsive design for a sleek, engaging experience.
- **✨ Customizable Inspiration**: Select mood/theme (Success, Mindset, Positivity, Hustle, Self-Reflection), and tone (Poetic, Bold, Simple, Deep).
- **🖼️ Dynamic Image Backgrounds**: When 'Image Quote' is selected, quotes are beautifully overlaid on random aesthetic image backgrounds from Picsum Photos, enhancing visual impact.
- **📝 Flexible Output**: Generate quotes as plain text, image quotes (downloadable as combined PNG), or tweet-ready formats.
- **💾 Interactive Options**: Copy (with visual feedback), Download (as text or image), and Share buttons (with visual feedback) for generated quotes.
- **🚀 Fast & Engaging**: Includes a "Crafting inspiration..." loading animation for a realistic feel, and smooth navigation with a responsive navbar.
- **Never Repeated**: Ensures fresh, unique quotes with each generation.

## 💡 Real-World Problem Solved

This agent addresses several real-world needs:

- **Content Creation**: Helps social media managers and content creators publish fresh, high-quality inspirational posts effortlessly, including visually appealing image quotes.
- **Mental Wellness**: Promotes mental wellness, motivation, and positive mindset building through daily affirmations and inspiring visuals.
- **Empowering Non-Writers**: Enables individuals without writing experience to express impactful thoughts and share wisdom through professionally presented quotes.
- **Habit Building**: Encourages habit formation through consistent exposure to motivational content for personal growth.

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.8+** installed on your system
- **Google Gemini API Key** (get one from [Google AI Studio](https://aistudio.google.com/app/apikey))
- **Internet connection** for AI quote generation and image backgrounds.

### ⚡ One-Click Installation (Windows)

```bash
# Navigate to the project directory
cd 63_AIQuoteGenerator

# Run the installation script
install.bat

# The installer will:
# ✅ Check Python installation
# ✅ Create a virtual environment
# ✅ Install all Python dependencies (including html2canvas for image download)
# ✅ Set up a .env file template
# ✅ Run installation tests
```

### 🔧 Manual Installation

```bash
# 1. Clone or download the project
git clone <repository-url>
cd 63_AIQuoteGenerator

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux (use 'source' instead of 'call')
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up environment variables
echo GEMINI_API_KEY=your_gemini_api_key_here > .env
```

### 🎯 First Run

```bash
# Option 1: Start the Web Interface (Recommended)
python main.py
# Open your browser to: http://localhost:8000
```

### 🧪 Verify Installation

```bash
# Run the test suite
python test_installation.py

# Expected output:
# ✅ Python version compatible
# ✅ All dependencies installed
# ✅ Configuration loaded
# ✅ AI agent initialized
# ✅ Web app ready
```

## 💡 Usage

### Navigating the UI
- **Home**: Returns to the main quote generation form.
- **Contact**: Scrolls smoothly to the contact form section at the bottom of the page.
- **About**: Opens a modal window with information about the 100 Days of AI Agents challenge.

### Generating Quotes
1.  **Select Mood/Theme**: Choose an inspirational category (e.g., Success, Mindset).
2.  **Choose Tone**: Pick the desired style (e.g., Poetic, Bold).
3.  **Output Format**: Select:
    -   <span class="font-bold">Text only</span>: Displays just the quote text.
    -   <span class="font-bold">Image Quote</span>: Displays the quote overlaid on a dynamically generated image background from Picsum Photos. The entire visual can be downloaded as a PNG.
    -   <span class="font-bold">Tweet-ready</span>: Formats the quote for Twitter, including relevant hashtags.
4.  **Click "Generate Quote"**: Watch as AI crafts your personalized inspiration.

### Interacting with Generated Quotes
-   **Copy**: Click to copy the quote text to your clipboard. You'll see a gold glow effect and a "Copied!" tooltip.
-   **Download**: If 'Image Quote' format is selected, clicking this button will download the displayed quote (text + background image) as a PNG file. For 'Text only' and 'Tweet-ready', it will simply copy the text.
-   **Share**: For 'Tweet-ready' format, this button will open a new Twitter window with the pre-formatted tweet. For other formats, it will provide a similar visual feedback as copy, indicating it's ready to share.

## ✨ Features

- **AI-Powered Quote Generation**: Leverages Google Gemini for generating fresh, unique, and context-aware motivational quotes.
- **Premium UI/UX**: Modern black theme with elegant gold and white highlights, 3D glassmorphism effects, and a fully responsive design across all devices.
- **Customizable Inspiration**: Users can choose from various moods/themes (e.g., Success, Mindset, Positivity, Hustle, Self-Reflection) and tones (Poetic, Bold, Simple, Deep).
- **Dynamic Image Backgrounds**: When 'Image Quote' output is selected, the quote is displayed aesthetically over a unique, randomly generated image from [Picsum Photos](https://picsum.photos/). The quote text is optimized for readability with appropriate styling.
- **Flexible Output Formats**: Supports plain text quotes, visually rich image quotes (which can be downloaded as a single PNG file), and ready-to-post tweet formats.
- **Interactive Elements**: Features intuitive Copy, Download, and Share buttons with subtle animations and tooltips for enhanced user feedback.
- **Responsive Navbar**: A sleek, sticky top navigation bar with 'Home', 'Contact' (smooth scroll), and 'About the Challenge' (modal dialog) links, adapting seamlessly to mobile and desktop screens.
- **Loading Animation**: A captivating "Crafting inspiration..." animation provides a realistic and engaging user experience during quote generation.
- **Error Handling**: Robust error management ensures graceful fallbacks and user-friendly messages for any issues.
- **Daily Affirmations**: Designed to encourage a positive daily routine by providing new, inspiring quotes at your fingertips.

## 🛠️ Technology Stack

### Frontend
-   **HTML5**: Semantic markup for content structure.
-   **Tailwind CSS**: Utility-first CSS framework for rapid and responsive UI development.
-   **Vanilla JavaScript**: Interactive elements, dynamic content updates, and client-side logic.
-   **html2canvas**: A JavaScript library used for accurately rendering and downloading the DOM as an image (specifically for the 'Image Quote' download feature).

### Backend
-   **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.8+.
-   **Python 3.8+**: The core language for backend logic and AI integration.
-   **Google Gemini API**: For generating advanced, context-aware quotes.
-   **Python-dotenv**: Manages environment variables for secure API key handling.

### APIs & Services
-   **Google Gemini API**: The primary AI engine for high-quality quote generation.
-   **Picsum Photos**: Provides reliable, random image backgrounds for visually rich quote overlays.

## 🏗️ Project Structure

```
63_AIQuoteGenerator/
├── main.py                 # FastAPI application entry point
├── config.py               # Configuration and environment variables
├── ai_agent.py             # Google Gemini integration and AI logic
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── install.bat             # Windows installation script
├── start.bat               # Windows startup script
├── test_installation.py    # Installation verification script
├── templates/
│   └── index.html          # Main HTML template for the UI
└── static/
    ├── js/
    │   └── app.js          # Frontend JavaScript for interactivity
    └── css/
        └── style.css       # Frontend CSS for custom styles (if any, beyond Tailwind)
```

## ⚙️ Configuration

### Environment Variables

-   `GOOGLE_API_KEY`: Your Google Gemini API key (required).
-   `GEMINI_MODEL`: The Gemini model to use (default: `gemini-pro`).
-   `APP_TITLE`: Application title (default: "AIQuoteGenerator").
-   `APP_DESCRIPTION`: Application description.
-   `HOST`: Server host (default: "0.0.0.0").
-   `PORT`: Server port (default: 8000).
-   `DEBUG`: Debug mode (default: True).

### API Key Setup

**Step 1: Get Google Gemini API Key**
1.  Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2.  Sign up or log in to your Google account.
3.  Create a new API key.
4.  Copy the generated API key.

**Step 2: Configure the Key**

Create a `.env` file in the `63_AIQuoteGenerator` directory with your API key:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

## 🐛 Troubleshooting

### Common Issues

1.  **`Google API Key not found`**: Ensure `GOOGLE_API_KEY` is correctly set in your `.env` file.
2.  **`ModuleNotFoundError`**: Run `pip install -r requirements.txt` to install all dependencies.
3.  **`Port Already in Use`**: Change the `PORT` in `config.py` to an available port.
4.  **`Network Error`**: Verify your internet connection and ensure Google Gemini API is accessible, and Picsum Photos is reachable.

### Debug Mode

Set `DEBUG = True` in `config.py` for more verbose logging and detailed error messages.

## 🤝 Contributing

This project is part of the 100 Days of AI Agents challenge. Contributions are welcome!

-   Report bugs and issues.
-   Suggest new features.
-   Submit pull requests.

## 📄 License

This project is open-source and available under the MIT License.

---

<div align="center">

**Your daily spark, one quote at a time.**

*Experience the power of AI to inspire and uplift!*

</div>
