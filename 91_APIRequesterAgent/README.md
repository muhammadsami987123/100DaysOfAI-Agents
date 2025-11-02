# 🌐 APIRequesterAgent - Day 91 of #100DaysOfAI-Agents

<div align="center">

![APIRequesterAgent Banner](https://img.shields.io/badge/APIRequesterAgent-Day%2091-blue?style=for-the-badge&logo=globe&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20Framework-red?style=for-the-badge&logo=fastapi&logoColor=white)
![Gemini](https://img.shields.io/badge/Google_Gemini-2.0--flash-blueviolet?style=for-the-badge&logo=google&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4.1-orange?style=for-the-badge&logo=openai&logoColor=white)

**Send GET/POST/PUT/DELETE API calls with ease and get formatted responses.**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎭 Examples](#-examples) • [📚 Documentation](#-documentation) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is APIRequesterAgent?

APIRequesterAgent is a smart AI-powered tool that allows users to send various HTTP requests (GET, POST, PUT, DELETE) to any API endpoint through a simple, intuitive web interface. It's designed to mimic the functionality of tools like Postman, providing formatted responses, status codes, and response times, along with an optional history of previous requests.

### 🌟 Key Highlights

- **🌐 All HTTP Methods**: Supports GET, POST, PUT, DELETE requests.
- **📝 Customizable Requests**: Easily add headers and JSON body/payload.
- **📊 Formatted Responses**: Pretty-prints JSON responses, displays status code and response time.
- **💾 Request History**: Saves previous requests for quick re-use.
- **🛡️ Robust Error Handling**: Gracefully manages invalid URLs, timeouts, and JSON errors.
- **💻 Dual LLM Support**: Default Gemini 2.0-flash, with optional OpenAI GPT-4.1 (for future enhancements).
- **🎨 Responsive UI**: Clean, modern, and fully responsive frontend with TailwindCSS.

## 🎯 Features

### 🚀 Core Functionality
- ✅ **API Request Sending**: Execute GET, POST, PUT, DELETE requests to any URL.
- ✅ **Dynamic Input**: User-friendly input fields for URL, method, headers, and body.
- ✅ **JSON Handling**: Automatically parses and pretty-prints JSON responses.
- ✅ **Performance Metrics**: Displays HTTP status code and response time.
- ✅ **Request History**: Stores and allows re-use of past requests.
- ✅ **Error Management**: Catches and displays common API request errors.

### 💻 User Interface
- ✅ **Modern Web UI**: Built with HTML and TailwindCSS for a sleek look.
- ✅ **Input Fields**: Dedicated areas for URL, Method (dropdown), Headers (JSON), Body (JSON).
- ✅ **Output Panel**: Clearly displays the formatted API response.
- ✅ **History Panel**: Shows a list of previous requests with details.
- ✅ **LLM Selector**: Dropdown to choose between Gemini and OpenAI (for future AI-driven request generation/analysis).
- ✅ **Responsive Design**: Optimized for various screen sizes.

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.8+** installed on your system.
- **OpenAI API Key** (optional, for GPT-4.1) (get one from [OpenAI Platform](https://platform.openai.com/api-keys))
- **Google Gemini API Key** (optional, for Gemini 2.0-flash) (get one from [Google AI Studio](https://aistudio.google.com/app/apikey))
- **Internet connection** for API calls.

### 🔧 Manual Installation

```bash
# 1. Clone or download the project
git clone <repository-url>
cd 91_APIRequesterAgent

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows
venc\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up environment variables
# Create a .env file in the project root with your API keys (if using LLMs)
# .env content example:
# GEMINI_API_KEY="your_gemini_api_key_here"
# OPENAI_API_KEY="your_openai_api_key_here"
# DEFAULT_LLM="gemini"
# HISTORY_FILE="request_history.json"
```

### 🎯 First Run

```bash
# Start the FastAPI web application
python main.py

# Open your web browser and navigate to:
# http://127.0.0.1:9000
```

## 🎭 Examples & Usage

### 🌐 Web Interface

The web interface provides an interactive experience for sending API requests:

1.  **📝 Enter API URL**: Input the endpoint you wish to call.
2.  **↔️ Select Method**: Choose between GET, POST, PUT, or DELETE.
3.  **➕ Add Headers**: Provide headers in JSON format (e.g., `{"Content-Type": "application/json"}`).
4.  **📦 Add Body**: For POST/PUT requests, enter the JSON payload.
5.  **🚀 Send Request**: Click the "Send Request" button.
6.  **📊 View Response**: The output panel will display the formatted JSON response, status code, and response time.
7.  **📜 Check History**: Review previous requests in the history panel.

**🎯 Pro Tips:**
- Ensure your JSON inputs for Headers and Body are valid.
- Use the history panel to quickly re-send or modify past requests.

### 🧪 Example Input & Output

**Example Request:**
- URL: `https://jsonplaceholder.typicode.com/posts`
- Method: `POST`
- Headers: `{"Content-Type": "application/json"}`
- Body: `{"title": "foo", "body": "bar", "userId": 1}`

**Expected Output (Response Panel):**
```json
{
  "title": "foo",
  "body": "bar",
  "userId": 1,
  "id": 101
}
```
Status Code: `201`
Response Time: `~150ms` (will vary)

## 🏗️ Project Architecture

### 📁 File Structure

```
91_APIRequesterAgent/
├── 📄 main.py                   # Main entry point for the FastAPI application
├── ⚙️ config.py                 # Configuration and settings management
├── 🤖 agent.py                 # Core API request logic and history management
├── 🌐 web_app.py                # FastAPI web application with routes and templating
├── 📋 requirements.txt          # Python dependencies
├── 📚 templates/                # HTML templates
│   └── index.html              # Main interface for sending requests
├── 🎨 static/                   # Static assets
│   └── main.css                # TailwindCSS and custom styles
├── 💡 utils/                    # Utility functions
│   └── llm_service.py          # LLM integration (Gemini/OpenAI) for future enhancements
├── 📄 .env                      # Environment variables for API keys and settings
├── 📄 .gitignore                # Specifies intentionally untracked files to ignore
├── 📄 README.md                 # This comprehensive documentation
└── 📜 request_history.json      # Stores history of API requests (auto-created)
```

### 🔧 Technical Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Python 3.8+ | Core application logic |
| **Web Framework** | FastAPI | REST API and web server |
| **HTTP Client** | `requests` | Sending HTTP requests |
| **Template Engine** | Jinja2 | HTML template rendering |
| **Frontend** | HTML, TailwindCSS | Modern, responsive design |
| **LLMs** | Google Gemini, OpenAI GPT-4.1 | AI integration for future features |
| **Data Storage** | JSON File System | Request history persistence |
| **Server** | Uvicorn | ASGI web server |

### 🎯 Key Components

#### 🤖 APIRequesterAgent (`agent.py`)
- **Request Execution**: Handles sending HTTP requests (GET, POST, PUT, DELETE).
- **Response Processing**: Extracts status code, response time, and JSON body.
- **History Management**: Saves and retrieves request/response history.
- **Error Handling**: Manages network, timeout, and JSON parsing errors.

#### 🌐 Web Application (`web_app.py`)
- **FastAPI Routes**: Defines endpoints for the main page and API request submission.
- **Template Rendering**: Uses Jinja2 to render the `index.html` with dynamic data.
- **Form Processing**: Handles user input from the web form.
- **LLM Integration**: Interfaces with `LLMService` for AI model selection.

#### 🎨 Frontend (`templates/index.html`, `static/main.css`)
- **Interactive UI**: Provides input fields, buttons, and display panels.
- **Responsive Design**: Ensures usability across devices.
- **Theme Toggle**: Dark/light mode switching.

#### 💡 LLMService (`utils/llm_service.py`)
- **LLM Abstraction**: Provides a unified interface for Gemini and OpenAI models.
- **Model Selection**: Allows switching between configured LLMs.
- **Content Generation**: (Currently for future enhancements) Can be used for AI-driven request generation or response analysis.

#### ⚙️ Configuration (`config.py`)
- **Environment Variables**: Loads API keys and other settings from `.env`.
- **LLM Defaults**: Sets default LLM and model names.
- **History File**: Defines the path for storing request history.

## ⚙️ Configuration & Setup

### 🔑 API Key Setup

**Step 1: Get API Keys (Optional for core functionality)**
- **Google Gemini**: Visit [Google AI Studio](https://aistudio.google.com/app/apikey) to get your `GEMINI_API_KEY`.
- **OpenAI**: Visit [OpenAI Platform](https://platform.openai.com/api-keys) to get your `OPENAI_API_KEY`.

**Step 2: Configure the Keys**

Create a `.env` file in the root of the `91_APIRequesterAgent` directory and add your API keys:

```
GEMINI_API_KEY="your_gemini_api_key_here"
OPENAI_API_KEY="your_openai_api_key_here"
DEFAULT_LLM="gemini" # or "openai"
HISTORY_FILE="request_history.json"
```

### 🎛️ Advanced Configuration

Edit `config.py` to customize application settings:

```python
# ...existing code...

class Config:
    # ...existing code...
    GEMINI_MODEL = _strip(os.getenv("GEMINI_MODEL", "gemini-2.0-flash"))
    OPENAI_MODEL = _strip(os.getenv("OPENAI_MODEL", "gpt-4.1"))
    HISTORY_FILE = _strip(os.getenv("HISTORY_FILE", "request_history.json"))
```

## 🧪 Testing & Quality Assurance

(Note: Detailed testing instructions and scripts are not yet provided but can be added based on project needs.)

### 🐛 Troubleshooting

**Common Issues & Solutions:**

| Issue | Cause | Solution |
|-------|-------|----------|
| **"Module not found"** | Missing dependencies | Run `pip install -r requirements.txt` |
| **"Port already in use"** | Default port 9000 is occupied | Change the `PORT` environment variable or modify `main.py` |
| **"Invalid JSON in Headers or Body"** | Malformed JSON input | Ensure headers and body are valid JSON strings |
| **"Request timed out"** | API endpoint is slow or unresponsive | Check the API endpoint's status or increase timeout in `agent.py` |
| **"Connection error"** | Network issue or invalid URL | Verify internet connection and URL correctness |

### 🔒 Security Considerations

- **API Key Security**: Never commit API keys directly to version control. Use `.env` and `.gitignore`.
- **Input Validation**: User inputs are handled to prevent common vulnerabilities.
- **Local Storage**: Request history is stored locally in `request_history.json`.
