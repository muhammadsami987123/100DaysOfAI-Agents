# 🌍 LocationInfoAgent - Day 61 of #100DaysOfAI-Agents

<div align="center">

![LocationInfoAgent Banner](https://img.shields.io/badge/LocationInfoAgent-Day%2061-blue?style=for-the-badge&logo=globe&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-orange?style=for-the-badge&logo=openai&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20Framework-red?style=for-the-badge&logo=fastapi&logoColor=white)

**Your AI-powered assistant to explore any place with voice capabilities**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🌐 APIs](#-api-documentation) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is LocationInfoAgent?

LocationInfoAgent is an intelligent AI-powered assistant designed to provide comprehensive, voice-enabled information about any location you wish to explore. Whether it's a bustling city, a serene country, a famous landmark, or an entire region, this agent delivers current facts, cultural insights, language details, key attractions, and visual context.

### 🌟 Key Highlights

-   **🌍 Global Coverage**: Get information for cities, countries, landmarks, and regions worldwide.
-   **🤖 AI-Powered Insights**: Uses OpenAI (GPT-4o-mini) to generate natural, conversational location reports.
-   **🔊 Voice Output**: Hear detailed information spoken aloud with customizable Text-to-Speech (TTS).
-   **🗺️ Interactive Maps**: Integrates Google Maps for visual context and navigation.
-   **📸 Image Gallery**: Displays relevant images of the explored location.
-   **⚡ Fast & Responsive**: Built with FastAPI for a high-performance backend and modern frontend.
-   **🎨 Modern UI**: Clean, high-contrast black-and-white theme with responsive design.

## 🎯 Features

### 🚀 Core Functionality
-   ✅ **AI-Enhanced Responses**: Generates detailed, natural language reports about locations.
-   ✅ **Geocoding**: Accurately finds geographical coordinates for input locations.
-   ✅ **Live Data Fetching**: Integrates with Wikipedia API for factual content.
-   ✅ **Interactive Map Embeds**: Displays Google Maps with the location pinned.
-   ✅ **Dynamic Image Galleries**: Fetches and showcases images from Unsplash.
-   ✅ **Text-to-Speech Output**: Converts AI-generated text into spoken words using multiple TTS engines.
-   ✅ **Voice Control**: Option to enable/disable voice output and stop ongoing speech.

### 💻 User Interface
-   ✅ **Intuitive Web UI**: Modern, clean, and responsive design for easy interaction.
-   ✅ **Loading Indicators**: Provides clear visual feedback during API calls.
-   ✅ **Error Handling**: Displays user-friendly messages for network issues or invalid inputs.
-   ✅ **Placeholder Typing Effect**: Engaging input field with dynamic placeholders.

## 📦 Installation

### 📋 Prerequisites

-   **Python 3.8+** installed on your system.
-   **Internet connection** for AI and external API data fetching.

### 🔑 How to Generate API Keys

To unlock the full functionality of the LocationInfoAgent, you'll need API keys from the following services:

#### 1. OpenAI API Key (Required for AI features)

1.  **Visit OpenAI Platform**: Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2.  **Sign Up or Log In**: Create an account or log in.
3.  **Create New Secret Key**: Click on "Create new secret key".
4.  **Copy the Key**: Copy the generated key (it starts with `sk-`).
5.  **Add to .env**: Add this key to your `.env` file:
    ```env
    OPENAI_API_KEY=your_openai_api_key_here
    ```

#### 2. Google Maps API Key (Optional, for Map Embeds)

1.  **Go to Google Cloud Console**: Navigate to [console.cloud.google.com](https://console.cloud.google.com/)
2.  **Create a Project**: Select an existing project or create a new one.
3.  **Enable APIs**: Search for and enable the following APIs:
    *   `Maps Embed API`
    *   `Geocoding API` (recommended for accurate location finding)
    *   `Places API` (optional, for richer place data)
4.  **Create Credentials**: Go to "APIs & Services" > "Credentials", click "+ CREATE CREDENTIALS" and select "API key".
5.  **Copy the Key**: Copy the generated API key.
6.  **Restrict the Key (Important!)**: Edit the API key, go to "Application restrictions", choose "HTTP referrers (web sites)", and add your domain(s). For local development, add `http://localhost:8000/*`.
7.  **Add to .env**: Add this key to your `.env` file:
    ```env
    GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
    ```

#### 3. Unsplash API Key (Optional, for Image Gallery)

1.  **Go to Unsplash Developers**: Visit [unsplash.com/developers](https://unsplash.com/developers)
2.  **Sign Up or Log In**: Create an account or log in.
3.  **Create a New Application**: Go to "Your Apps" or "New Application", agree to the guidelines, and provide an application name/description.
4.  **Copy the Access Key**: Once the application is created, copy the "Access Key" (this is your API key).
5.  **Add to .env**: Add this key to your `.env` file:
    ```env
    IMAGE_SEARCH_API_KEY=your_unsplash_access_key_here
    ```

### ⚡ One-Click Installation (Windows)

```bash
# Windows - Run the installer
install.bat

# The installer will:
# ✅ Check Python installation
# ✅ Create virtual environment
# ✅ Install all dependencies
# ✅ Create .env file template
# ✅ Run installation tests
```

### 🔧 Manual Installation

```bash
# 1. Navigate to the project directory
cd 61_LocationInfoAgent

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windowsenv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up environment variables (manually create .env file with your keys)
# See 'How to Generate API Keys' section above
```

### 🎯 First Run

```bash
# Option 1: Web Interface (Recommended)
# Windows
start.bat
# Linux/Mac
source venv/bin/activate
python main.py

# Open your browser to:
# http://localhost:8000
```

### 🧪 Verify Installation

```bash
# Run the test suite
python test_installation.py

# Expected output:
# ✅ Python version compatible
# ✅ All dependencies installed
# ✅ Configuration loaded
# ✅ API keys checked
# ✅ Service modules placeholder (will pass for now)
# ✅ Web app ready
```

## 🎯 Usage

### 🌐 Web Interface

The web interface provides an intuitive experience for exploring locations:

1.  **📝 Enter a Location**: Type a city, country, landmark, or region into the input field.
2.  **🔊 Toggle Voice Output**: Check/uncheck the "Enable Voice Output" box to control spoken responses.
3.  **🚀 Explore**: Click "Explore" or press Enter to fetch information.
4.  **👁️ View Results**: See a detailed AI-generated report, an embedded map, and an image gallery.

## 🏗️ Project Architecture

### 📁 File Structure

```
61_LocationInfoAgent/
├── 📄 main.py                 # FastAPI application entry point, API routes
├── ⚙️ config.py               # Configuration and environment variables
├── 🤖 location_agent.py       # Core AI logic, orchestrates data fetching and AI response generation
├── 🌐 location_service.py     # Handles external API calls (geocoding, Wikipedia, Google Maps, Unsplash)
├── 🔊 tts_service.py          # Manages Text-to-Speech functionality (OpenAI TTS, pyttsx3, gTTS)
├── 📋 requirements.txt        # Python dependencies for the project
├── 📖 README.md               # This comprehensive documentation
├── 📦 install.bat             # Windows script for environment setup and dependency installation
├── 🚀 start.bat               # Windows script to activate environment and run the application
├── 🧪 test_installation.py    # Script to verify correct setup and functionality
├── 📚 templates/              # HTML templates for the web interface
│   └── index.html            # Main HTML page for the LocationInfoAgent UI
└── 🎨 static/                 # Static assets like JavaScript and CSS files
    └── js/
        └── app.js            # Frontend JavaScript for interactivity and API calls
```

### 🔧 Technical Stack

| Component          | Technology          | Purpose                                        |
| :----------------- | :------------------ | :--------------------------------------------- |
| **Backend Framework** | FastAPI           | Building high-performance async API endpoints |
| **AI Engine**      | OpenAI GPT-4o-mini  | Natural language understanding and generation   |
| **Web Scraping**   | BeautifulSoup4, lxml | Extracting structured data from web pages (e.g., Wikipedia) |
| **HTTP Client**    | httpx, requests     | Asynchronous and synchronous API requests       |
| **Text-to-Speech** | OpenAI TTS, pyttsx3, gTTS | Converting text into natural-sounding speech |
| **Configuration**  | python-dotenv       | Managing environment variables                 |
| **Template Engine**| Jinja2              | Rendering dynamic HTML content                  |
| **Frontend**       | HTML5, Tailwind CSS, Vanilla JS | Modern, responsive, interactive user interface |
| **Web Server**     | Uvicorn             | ASGI server for FastAPI application             |

### 🎯 Key Components

#### 🤖 LocationInfoAgent (`location_agent.py`)
-   **AI Orchestration**: Directs interactions between location services, TTS, and OpenAI.
-   **Response Enhancement**: Uses AI to generate structured, engaging, and voice-friendly location reports.
-   **Voice Integration**: Triggers TTS service for spoken output.

#### 🌐 LocationService (`location_service.py`)
-   **Geocoding**: Converts location names into precise latitude and longitude coordinates.
-   **Data Retrieval**: Fetches comprehensive factual data from sources like Wikipedia.
-   **Map Generation**: Creates embeddable Google Maps URLs.
-   **Image Fetching**: Retrieves relevant images from Unsplash or other sources.

#### 🔊 TTSService (`tts_service.py`)
-   **Multi-Engine Support**: Provides text-to-speech using OpenAI TTS, pyttsx3, and gTTS.
-   **Asynchronous Playback**: Ensures voice output doesn't block the UI.
-   **Voice Control**: Allows stopping ongoing speech.

#### 📄 FastAPI Application (`main.py`)
-   **API Endpoints**: Defines the routes for `explore`, `voice/stop`, `health`, etc.
-   **Request/Response Handling**: Validates and processes incoming requests and formats responses.
-   **Static File & Template Serving**: Manages the delivery of frontend assets.

#### 🎨 Frontend (`static/js/app.js` and `templates/index.html`)
-   **User Input**: Captures location queries and voice preferences.
-   **Dynamic Display**: Renders AI responses, maps, and image galleries dynamically.
-   **Loading States**: Manages UI feedback during asynchronous operations.
-   **Interactive Elements**: Handles button clicks, form submissions, and voice toggles.

## 🐛 Troubleshooting

### Common Issues

1.  **API Key Errors**: Ensure `OPENAI_API_KEY`, `GOOGLE_MAPS_API_KEY`, and `IMAGE_SEARCH_API_KEY` are correctly set in your `.env` file.
2.  **Location Not Found**: Check spelling or try adding country (e.g., "Paris, France").
3.  **Voice Not Working**: Verify `TTS_ENABLED=True` in `.env`, check system audio drivers, or try `TTS_ENGINE=gtts`.
4.  **Map Not Loading**: Confirm `GOOGLE_MAPS_API_KEY` is valid, and the "Maps Embed API" is enabled in Google Cloud Console. Check browser console for errors.
5.  **Images Not Loading**: Confirm `IMAGE_SEARCH_API_KEY` is valid for Unsplash (or your chosen service) and check browser console for errors.
6.  **Network Errors**: Check internet connection and firewall settings. Ensure external APIs are accessible.
7.  **Port Already in Use**: Change the `PORT` in your `.env` file (e.g., `PORT=8001`).

### Debug Mode
Enable debug mode by setting `DEBUG=True` in your `.env` file for detailed logging.

## 🔮 Future Roadmap

### 🚀 Planned Features

-   **Contextual Tips**: AI-generated travel tips based on location info.
-   **Historical Data**: Option to retrieve historical facts or events.
-   **User Preferences**: Personalize recommendations based on user interests.
-   **Multi-language Support**: Expand TTS and AI response languages.
-   **Voice Input**: Implement speech-to-text for hands-free interaction.
-   **More Data Sources**: Integrate with additional APIs (e.g., Google Places, weather).
-   **Caching Mechanism**: Implement server-side caching for faster responses.

## 🤝 Contributing

We welcome contributions to make LocationInfoAgent even better!

### 🛠️ How to Contribute

1.  **Fork the repository**.
2.  **Create a feature branch**: `git checkout -b feature/your-feature-name`.
3.  **Make your changes** and test thoroughly.
4.  **Commit your changes**: `git commit -m 'Add your concise commit message'`.
5.  **Push to the branch**: `git push origin feature/your-feature-name`.
6.  **Open a Pull Request** to the main branch.

### 🎯 Areas for Contribution

-   **New Data Sources**: Integrate new APIs for more diverse information.
-   **UI/UX Improvements**: Enhance the frontend design and user experience.
-   **Performance Optimization**: Improve speed and efficiency of data fetching/processing.
-   **Bug Fixes**: Identify and resolve issues.
-   **Documentation**: Improve existing guides and examples.

## 📞 Support & Community

### 🆘 Getting Help

1.  **📖 Documentation**: Refer to this README for comprehensive information.
2.  **🧪 Test Suite**: Run `python test_installation.py` to verify your setup.
3.  **🔍 Troubleshooting**: Check the Troubleshooting section for common issues.
4.  **📊 Logs**: Review server console output for detailed error messages.

### 🐛 Reporting Issues

When reporting issues, please include:

-   **System Information**: OS, Python version, browser, etc.
-   **Error Messages**: Full traceback or relevant error text.
-   **Steps to Reproduce**: Clear steps to trigger the issue.
-   **Expected vs Actual**: Describe what you expected to happen versus what actually occurred.

## 📄 License & Credits

### 📜 License

This project is part of the **#100DaysOfAI-Agents** challenge by **Muhammad Sami Asghar Mughal**.

**MIT License** - Feel free to use, modify, and distribute!

### 🙏 Acknowledgments

-   **OpenAI** for providing advanced AI models and TTS capabilities.
-   **Google Maps Platform** for interactive mapping services.
-   **Unsplash** for high-quality, free-to-use images.
-   **FastAPI** team for the modern, high-performance web framework.
-   **Tailwind CSS** for simplifying UI development and styling.
-   **Python community** for the rich ecosystem of libraries.

---

**Built with ❤️ for Day 61 of 100 Days of AI Agents**

*Explore the world with AI-powered insights and natural voice interaction!*
