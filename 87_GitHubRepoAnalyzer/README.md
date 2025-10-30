# 🔍 GitHubRepoAnalyzer - Day 87 of #100DaysOfAI-Agents

<div align="center">

![GitHubRepoAnalyzer Banner](https://img.shields.io/badge/GitHubRepoAnalyzer-Day%2087-blue?style=for-the-badge&logo=github&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![Gemini](https://img.shields.io/badge/Google-Gemini--Pro-orange?style=for-the-badge&logo=google&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20Framework-red?style=for-the-badge&logo=fastapi&logoColor=white)

**Analyze GitHub repositories with AI-powered insights and beautiful glassmorphism UI**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎨 UI Elements](#-ui-elements) • [📚 Documentation](#-documentation) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is GitHubRepoAnalyzer?

GitHubRepoAnalyzer is a modern web application that leverages AI to provide comprehensive analysis of GitHub repositories. With its stunning glassmorphism UI and powerful AI backend, it helps developers, project managers, and open-source enthusiasts understand repositories at a glance. Get instant insights about code structure, documentation quality, and actionable improvements.

### 🌟 Key Highlights

- **🎨 Beautiful Glass UI**: Modern, responsive interface with glassmorphism effects
- **🤖 Dual AI Models**: Choose between Gemini Pro and GPT-4.1
- **⚡ Real-time Analysis**: Instant repository insights
- **📊 Smart Suggestions**: AI-powered improvement recommendations
- **💾 Export Options**: Download or copy analysis results
- **🌐 Web-based**: No installation needed, runs in browser
- **🔄 Interactive UI**: Smooth animations and visual feedback

## 🎯 Features

### 🚀 Core Functionality
- ✅ **AI Repository Analysis**: Powered by Google Gemini and OpenAI
- ✅ **Smart Pattern Detection**: Identifies code patterns and structure
- ✅ **Documentation Review**: Evaluates README and docs quality
- ✅ **Interactive Results**: Copy, download, and share insights
- ✅ **Progress Tracking**: Visual feedback during analysis
- ✅ **Error Handling**: Graceful error management

### 🎨 UI Elements
- ✅ **Glassmorphism Design**: Modern, translucent interface
- ✅ **Animated Effects**: Smooth transitions and interactions
- ✅ **Loading States**: Beautiful loading animations
- ✅ **Responsive Layout**: Works on all screen sizes
- ✅ **Dark Theme**: Easy on the eyes
- ✅ **Interactive Buttons**: Copy and download with effects

### 💻 Technical Features
- ✅ **FastAPI Backend**: High-performance API server
- ✅ **Static File Caching**: Optimized resource loading
- ✅ **CORS Support**: Cross-origin resource sharing
- ✅ **Gzip Compression**: Faster content delivery
- ✅ **Error Boundaries**: Robust error handling
- ✅ **Development Mode**: Hot-reloading for development

### 📊 Analysis Capabilities
- ✅ **Code Structure**: Repository organization analysis
- ✅ **Documentation Quality**: README and docs evaluation
- ✅ **Best Practices**: Compliance with standards
- ✅ **Action Items**: Suggested improvements
- ✅ **Quick Stats**: Repository statistics
- ✅ **Export Options**: Multiple export formats

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.8+** installed on your system
- **Google API Key** for Gemini Pro
- **OpenAI API Key** (optional, for GPT-4.1)
- **Internet connection** for repository analysis

### ⚡ Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/GitHubRepoAnalyzer.git
cd 87_GitHubRepoAnalyzer

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create .env file with your API keys:
GOOGLE_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key  # Optional

# Start the application
uvicorn web_app:app --reload
```

### 🌐 Usage

1. Open your browser and navigate to `http://localhost:8000`
2. Enter a GitHub repository URL
3. Select your preferred LLM model (Gemini or GPT-4.1)
4. Click Analyze and wait for the results
5. Use the Copy or Download buttons to save the analysis

## 🎨 UI Elements

### Glassmorphism Effects
- **Translucent Cards**: Beautiful glass-like containers
- **Gradient Backgrounds**: Smooth color transitions
- **Animated Blobs**: Dynamic background elements
- **Interactive Buttons**: Smooth hover and click effects
- **Loading States**: Elegant loading animations

### Interactive Features
- **Copy Button**: One-click copying with success animation
- **Download Button**: Easy export with visual feedback
- **Model Selection**: Switch between AI models
- **Loading Overlay**: Visual progress indicator
- **Error Messages**: Clear error notifications

## 📚 Documentation

Detailed documentation for developers is available in the `/docs` folder:

- **Installation Guide**: Complete setup instructions
- **API Reference**: Backend API documentation
- **UI Components**: Frontend component guide
- **Configuration**: Environment variables and settings
- **Troubleshooting**: Common issues and solutions

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
Created with ♥ as part of #100DaysOfAI-Agents

[⬆ Back to Top](#-githubrepofanalyzer---day-87-of-100daysofai-agents)
</div>
- LLM selection: Gemini (default) or GPT-4.1

## Usage
1. Enter a public GitHub repo URL
2. Select LLM (optional)
3. Click "Analyze Repository"
4. View and copy/download the summary

## Tech Stack
- Frontend: HTML + TailwindCSS
- Backend: Python + FastAPI
- LLMs: Gemini 2.0-flash (default), GPT-4.1 (optional)
- GitHub API integration

---

Follows the agent structure and conventions from Day 85/86.