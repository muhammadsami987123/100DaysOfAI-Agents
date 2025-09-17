# 📊 TextAnalyzerAgent - Day 46 of #100DaysOfAI-Agents

<div align="center">

![TextAnalyzerAgent Banner](https://img.shields.io/badge/TextAnalyzerAgent-Day%2046-blue?style=for-the-badge&logo=analyzer&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-API-orange?style=for-the-badge&logo=google&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-lightgray?style=for-the-badge&logo=flask&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-UI%20Framework-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)

**Analyze the tone and sentiment of any given text to improve communication**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎭 Examples](#-examples) • [📚 Documentation](#-documentation) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is TextAnalyzerAgent?

TextAnalyzerAgent is an intelligent AI-powered tool designed to analyze the tone and sentiment of text, providing valuable insights for various applications. From social media management to customer support, this agent helps users understand the emotional context and overall tone of written content, facilitating clearer and more effective communication.

### 🌟 Key Highlights

-   **🎯 Tone Analysis**: Identifies various tones (e.g., formal, informal, optimistic, concerned, neutral).
-   **❤️ Sentiment Analysis**: Determines sentiment (e.g., positive, negative, neutral, mixed).
-   **📝 Concise Summary**: Provides a brief overview of the analysis.
-   **⚙️ Modular & Structured**: Responses are easy to integrate into other systems.
-   **🌐 Modern Web UI**: Features a responsive, animated web interface with light/dark mode.
-   **⚡ Fast & Efficient**: Utilizes Google Gemini API for quick analysis.
-   **📈 Error Handling**: Robust error handling on both frontend and backend.

## 🎯 Features

### 🚀 Core Functionality

-   ✅ **AI-Powered Analysis**: Leverages Google Gemini for accurate tone and sentiment detection.
-   ✅ **Structured Output**: Delivers analysis in a consistent, easy-to-parse format.
-   ✅ **Real-time Feedback**: Provides instant analysis results in the web UI.
-   ✅ **Input Validation**: Ensures valid text input before processing.
-   ✅ **API Key Integration**: Securely manages Gemini API key via environment variables.

### 💻 User Interface

-   ✅ **Modern Web UI**: Built with Flask and Tailwind CSS for a sleek, responsive design.
-   ✅ **Light/Dark Mode**: User-friendly theme toggle with preference saving.
-   ✅ **Interactive Input**: Textarea with floating labels and clear focus states.
-   ✅ **Dynamic Status**: Real-time feedback on analysis progress and errors.
-   ✅ **Animated Elements**: Smooth transitions and loading indicators for a better UX.

### 📊 Applications

-   **Social Media Managers**: Tone check before posting to maintain brand voice.
-   **Writers & Editors**: Validate style and tone consistency in articles, blogs, etc.
-   **Customer Support Teams**: Sentiment review of complaints and feedback for improved service.
-   **Mental Health Apps**: Detect negative sentiment patterns in user input for early intervention.
-   **Journalists & Researchers**: Analyze public opinion and media sentiment.

## 🚀 Quick Start

### 📋 Prerequisites

-   **Python 3.8+** installed on your system
-   **Node.js & npm/yarn** (for Tailwind CSS setup)
-   **Google Gemini API Key** (get one from [Google AI Studio](https://aistudio.google.com/app/apikey))
-   **Internet connection** for AI analysis

### ⚡ One-Click Installation (Windows)

Navigate to the `46_TextAnalyzerAgent` directory and run:

```bash
.\install.bat
```

The installer will:
-   ✅ Create a Python virtual environment
-   ✅ Install Python dependencies (`pip install -r requirements.txt`)
-   ✅ Install Node.js dependencies (`npm install` for Tailwind CSS)
-   ✅ Build Tailwind CSS (`npm run build`)

### 🔧 Manual Installation

```bash
# 1. Clone or download the project
git clone <repository-url>
cd 46_TextAnalyzerAgent

# 2. Create Python virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 4. Install Python dependencies
pip install -r requirements.txt

# 5. Install Node.js dependencies (for Tailwind CSS)
npm install

# 6. Build Tailwind CSS
npm run build

# 7. Configure API Key
echo GEMINI_API_KEY="your_api_key_here" > .env
```

### 🎯 First Run

To run the web application, execute the `start.bat` file from the `46_TextAnalyzerAgent` directory:

```bash
.\start.bat
```

This script will:
-   ✅ Activate the Python virtual environment
-   ✅ Start the Tailwind CSS watcher in a separate console
-   ✅ Run the Flask web application

Open your web browser and navigate to `http://127.0.0.1:5000/` to access the Text Analyzer Agent.

## 🎭 Examples & Usage

### 🌐 Web Interface

The web interface provides an intuitive way to analyze text:

1.  **📝 Enter Your Text**: Type or paste the text you want to analyze into the input area.
2.  **🚀 Analyze**: Click the "Analyze Text" button.
3.  **📊 View Results**: The analysis summary, tone, and sentiment will be displayed.
4.  **☀️/🌙 Toggle Theme**: Use the button at the top right to switch between light and dark modes.

**🎯 Pro Tips:**
-   Ensure your `GEMINI_API_KEY` is correctly set in the `.env` file.
-   Observe the status indicator and loading animation for real-time feedback.

### 💡 Example Scenarios

Here are some examples of how the Text Analyzer Agent processes text:

#### Example 1: Positive Sentiment

**Input Text:**
"I am absolutely thrilled with the results! This is the best product I have ever used. Highly recommend to everyone!"

**Expected Output Structure:**
```
Summary: The text expresses strong satisfaction and enthusiasm.
Tone: Enthusiastic, Highly Positive, Recommending
Sentiment: Positive
```

#### Example 2: Negative Sentiment with Concern

**Input Text:**
"I am very disappointed with the recent changes. The new features are confusing and have made the user experience much worse. I hope this gets fixed soon."

**Expected Output Structure:**
```
Summary: The text conveys disappointment and concern regarding recent negative changes.
Tone: Disappointed, Concerned, Critical
Sentiment: Negative
```

#### Example 3: Neutral/Informative Tone

**Input Text:**
"The quarterly report indicates a slight increase in revenue compared to the previous quarter, with stable operational costs."

**Expected Output Structure:**
```
Summary: The text presents factual information about financial performance.
Tone: Formal, Informative, Objective, Neutral
Sentiment: Neutral
```

#### Example 4: Mixed Sentiment

**Input Text:**
"While the initial setup was a bit challenging, the performance after configuration has been outstanding. I appreciate the effort, but documentation could be improved."

**Expected Output Structure:**
```
Summary: The text shows appreciation for good performance but highlights issues with initial setup and documentation.
Tone: Appreciative, Critical, Constructive
Sentiment: Mixed
```

## 🏗️ Project Architecture

### 📁 File Structure

```
46_TextAnalyzerAgent/
├── 📄 main.py                   # Main entry point for running the Flask app
├── ⚙️ config.py                 # Configuration settings (API keys, etc.)
├── 🤖 text_analyzer_agent.py    # Core AI text analysis logic using Google Gemini
├── 🌐 web_app.py                # Flask web application with routes and API endpoints
├── 📋 requirements.txt          # Python dependencies
├── 📦 install.bat               # Windows installation script
├── 🚀 start.bat                 # Windows startup script
├── 📄 README.md                 # This comprehensive documentation
├── 📄 package.json              # Node.js dependencies for Tailwind CSS
├── ⚙️ tailwind.config.js        # Tailwind CSS configuration
├── 🎨 static/                   # Static assets (CSS, JavaScript)
│   ├── css/
│   │   ├── input.css           # Tailwind CSS input file
│   │   └── output.css          # Tailwind CSS compiled output file
│   └── js/
│       └── script.js           # Frontend JavaScript logic
└── 📚 templates/                # HTML templates
    └── index.html              # Main web interface page
```

### 🔧 Technical Stack

| Component        | Technology           | Purpose                                    |
|------------------|----------------------|--------------------------------------------|
| **Backend**      | Python 3.8+          | Core application logic                     |
| **AI Engine**    | Google Gemini API    | Tone and sentiment analysis                |
| **Web Framework**| Flask                | Web application and API server             |
| **Template Engine**| Jinja2               | HTML template rendering                    |
| **Frontend**     | Tailwind CSS         | Modern, responsive UI styling              |
| **Frontend Logic**| Vanilla JavaScript   | Interactive user interface and state management |
| **Environment**  | python-dotenv        | Environment variable management            |

### 🎯 Key Components

#### 🤖 TextAnalyzerAgent (`text_analyzer_agent.py`)
-   **Core AI Logic**: Handles Google Gemini API integration.
-   **Text Analysis**: Performs tone and sentiment analysis.
-   **Structured Output**: Ensures consistent analysis results.

#### 🌐 Web Application (`web_app.py`)
-   **Flask Routes**: Manages web routes and API endpoints (`/` for UI, `/analyze` for API).
-   **Frontend Integration**: Renders HTML templates and serves static assets.
-   **Error Handling**: Provides robust server-side error logging.

#### 🎨 Frontend (`static/`, `templates/`)
-   **Modern UI**: Responsive design with Tailwind CSS.
-   **Dark Mode**: Theme toggle for user preference.
-   **Interactive Elements**: Input field with floating labels, dynamic buttons.
-   **Visual Feedback**: Loading indicators and clear status messages.

#### ⚙️ Configuration (`config.py`)
-   **Settings Management**: Centralized application configuration.
-   **API Key Management**: Secure handling of the Google Gemini API key.

## ⚙️ Configuration & Setup

### 🔑 API Key Setup

**Step 1: Get Google Gemini API Key**
1.  Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2.  Sign up or log in to your Google account.
3.  Navigate to the "Get API Key" section.
4.  Create a new API key.
5.  Copy the generated API key.

**Step 2: Configure the Key**

Create a `.env` file in the `46_TextAnalyzerAgent` directory with the following content:

```
GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY_HERE"
```

Replace `YOUR_ACTUAL_GEMINI_API_KEY_HERE` with the API key you obtained from Google AI Studio.

### 🎛️ Advanced Configuration

Edit `config.py` to customize application settings:

```python
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
```

## 🧪 Testing & Quality Assurance

### 🔍 Verification Steps

1.  **Run the application:** Follow the [Quick Start](#-quick-start) instructions.
2.  **Open in browser:** Navigate to `http://127.0.0.1:5000/`.
3.  **Test UI elements:** Verify light/dark mode toggle, input field focus, and button hover effects.
4.  **Perform analysis:** Enter text and click "Analyze Text". Check if results are displayed correctly.
5.  **Check console for errors:** Monitor your browser's developer console (`F12`) and the backend terminal for any error messages during interaction.

### 🐛 Troubleshooting

**Common Issues & Solutions:**

| Issue                                  | Cause                                | Solution                                                              |
|----------------------------------------|--------------------------------------|-----------------------------------------------------------------------|
| **"GEMINI_API_KEY is not set" warning** | `.env` file missing, misspelled key, or not restarted | Ensure `.env` is in `46_TextAnalyzerAgent`, key is correct, restart app. |
| **Analysis results not showing**      | Frontend parsing issue or backend API error | Check browser console logs for `Fetch response` and `Parsed data` to debug frontend parsing, or check backend terminal for `web_app.py` errors. |
| **UI not styled correctly**            | Tailwind CSS not built or linked     | Run `npm install` then `npm run build` from `46_TextAnalyzerAgent` directory. Ensure `output.css` is correctly linked in `index.html`. |
| **`npm` command not found**            | Node.js/npm not installed            | Install Node.js from [nodejs.org](https://nodejs.org/).                  |
| **Port already in use**                | Another process is using port 5000   | Identify and terminate the process using the port, or change Flask port. |

## 🔮 Future Roadmap

### 🚀 Planned Enhancements

-   **Sentiment Scoring**: Provide a numerical sentiment score in addition to categorical sentiment.
-   **Detailed Tone Breakdown**: Offer more granular insights into specific tone components.
-   **Text Highlighting**: Visually highlight parts of the text corresponding to specific tones/sentiments.
-   **Input History**: Allow users to review previous analysis requests.
-   **API Rate Limiting**: Implement rate limiting for API calls to prevent abuse.
-   **Dockerization**: Package the application in a Docker container for easier deployment.

## 🤝 Contributing

We welcome contributions to make TextAnalyzerAgent even better!

### 🛠️ How to Contribute

1.  **Fork the repository**.
2.  **Create a feature branch**: `git checkout -b feature/your-feature-name`.
3.  **Make your changes** and test thoroughly.
4.  **Commit your changes**: `git commit -m 'Add your feature'`.
5.  **Push to the branch**: `git push origin feature/your-feature-name`.
6.  **Open a Pull Request**.

### 🎯 Areas for Contribution

-   **UI/UX Improvements**: Enhance the user interface and experience.
-   **New Analysis Features**: Integrate additional text analysis capabilities.
-   **Performance Optimization**: Improve speed and efficiency.
-   **Documentation**: Enhance guides and examples.
-   **Bug Fixes**: Report and fix issues.

## 📞 Support & Community

### 🆘 Getting Help

1.  **Documentation**: Refer to this `README.md`.
2.  **Troubleshooting**: Check the troubleshooting section above.
3.  **GitHub Issues**: Report bugs or suggest features on the GitHub repository.

### 💬 Community

-   **GitHub Issues**: For bug reports and feature requests.
-   **Discussions**: For general questions and ideas.

## 📄 License & Credits

### 📜 License

This project is part of the **#100DaysOfAI-Agents** challenge by **Muhammad Sami Asghar Mughal**.

**MIT License** - Feel free to use, modify, and distribute!

### 🙏 Acknowledgments

-   **Google Gemini API** for powerful text analysis capabilities.
-   **Flask** for the robust web framework.
-   **Tailwind CSS** for a beautiful and responsive UI.
-   **Python community** for amazing libraries.
-   **All contributors** who help improve this project.

### 🌟 Inspiration

This project was inspired by the need for tools that can provide quick and accurate insights into text, facilitating better communication and understanding across various domains.

---

<div align="center">

## 🎉 Ready to Analyze Text?

**Understand the hidden meanings in your text with the power of AI!**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎭 Examples](#-examples) • [📚 Documentation](#-documentation)

---

**Made with ❤️ by the #100DaysOfAI-Agents community**

*Day 46 of 100 - Building the future of AI agents, one day at a time!*

</div>
