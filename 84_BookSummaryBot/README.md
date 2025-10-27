# 📚 BookSummaryBot - Day 84 of #100DaysOfAI-Agents

<div align="center">

![BookSummaryBot Banner](https://img.shields.io/badge/BookSummaryBot-Day%2084-blue?style=for-the-badge&logo=google&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20Framework-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-API-blue?style=for-the-badge&logo=google&logoColor=white)
![OpenAI GPT-4](https://img.shields.io/badge/OpenAI_GPT--4-API-orange?style=for-the-badge&logo=openai&logoColor=white)

**Your AI assistant for concise book chapter summaries from text, files, or URLs!**

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [🎭 Examples](#-examples) • [🏗️ Project Architecture](#-project-architecture) • [⚙️ Configuration](#-configuration--setup) • [🧪 Testing](#-testing--quality-assurance) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is BookSummaryBot?

BookSummaryBot is a smart assistant designed to help users quickly grasp the core ideas of book chapters. It accepts chapter content as pasted text, uploaded files (.txt or .pdf), or a public URL, and then generates a concise, clear summary. Users can choose between Google Gemini 2.0-flash (default) or OpenAI GPT-4.1 for summarization.

### 🌟 Key Highlights

- **📖 Multi-Input Support**: Summarize from pasted text, .txt files, .pdf files, or public URLs.
- **💡 AI-Powered Summarization**: Utilizes Google Gemini 2.0-flash (default) or OpenAI GPT-4.1 to generate high-quality summaries.
- **📝 Concise & Structured Output**: Provides summaries in 1-3 paragraphs or 5-7 bullet points, optionally with key themes, characters, or events.
- **🎨 Modern UI**: Features a clean, responsive, and intuitive web interface with dark/light mode, inspired by leading dashboard designs.
- **⚙️ Configurable LLMs**: Easily switch between Gemini and OpenAI models via the UI.
- **📥 Output Management**: Copy and download buttons for generated summaries and key points.

## 🎯 Features

### 🚀 Core Functionality
- ✅ **AI-Powered Summary Generation**: Integrates with Google Gemini API and OpenAI API for intelligent content summarization.
- ✅ **Flexible Input Methods**: Accepts direct text input, file uploads (TXT, PDF), and URL fetching.
- ✅ **Summarization Options**: Generates summaries as concise paragraphs or bullet points.
- ✅ **Key Information Extraction**: Optionally extracts key themes, main characters, or significant events.
- ✅ **LLM Selection**: Allows users to choose their preferred LLM for summarization.

### 🎨 User Experience
- ✅ **Modern Dashboard UI**: Intuitive layout for inputs and outputs, with a focus on ease of use.
- ✅ **Dark/Light Mode**: User-friendly theme toggle for comfortable viewing in any lighting condition.
- ✅ **Clear Input Guidance**: Enhanced labels and hints for all input methods.
- ✅ **Visual Feedback**: Loading spinner and error message display for smooth interaction.
- ✅ **Initial Welcome Screen**: Engaging welcome message with guidance for new users.

### 📊 Management & Integration
- ✅ **Centralized Configuration**: Uses a `Config` class and `.env` file for easy management of API keys and settings.
- ✅ **Modular Codebase**: Organized Python files for clear separation of concerns (FastAPI app, agent logic, LLM service, utilities).

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.8+** installed on your system.
- **Google Gemini API Key** (get one from [Google AI Studio](https://aistudio.google.com/app/apikey)).
- **OpenAI API Key** (get one from [OpenAI](https://platform.openai.com/account/api-keys)) (optional, if you want to use GPT-4).
- **Internet connection** for AI summarization and URL fetching.

### 🔧 Manual Installation

   ```bash
# 1. Navigate to the agent's directory
cd 84_BookSummaryBot

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment (Windows)
venc\Scripts\activate
# On Linux/Mac, use: source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up environment variables
# Create a .env file in the 84_BookSummaryBot directory:
echo GEMINI_API_KEY=your_gemini_api_key_here > .env
echo OPENAI_API_KEY=your_openai_api_key_here >> .env
# Replace 'your_gemini_api_key_here' and 'your_openai_api_key_here' with your actual API keys.
# You can also set DEFAULT_LLM="openai" to use OpenAI by default.
```

### 🎯 First Run (Web UI - Recommended)

   ```bash
# 1. Navigate to the agent's directory (if not already there)
cd 84_BookSummaryBot

# 2. Run the application
python main.py

# 3. Then, open your web browser and navigate to:
# http://127.0.0.1:8000
```

## 🎭 Examples & Usage

### 🌐 Web Interface

The intuitive web interface allows you to easily get your book chapter summary:

1.  **Provide Chapter Content**: Paste text into the textarea, upload a `.txt` or `.pdf` file, or enter a public URL to the chapter.
2.  **Choose LLM**: Select your preferred language model (Gemini 2.0-flash or OpenAI GPT-4).
3.  **Summarize Chapter**: Click "Summarize Chapter" to receive your personalized summary.
4.  **Manage Output**: Use the "Copy" and "Download" buttons to save the summary and key points.

### 💡 Example Scenario:

-   **Study Session**: Quickly summarize a dense chapter from a textbook by pasting its content or uploading the PDF, then easily copy the key points for your notes.
-   **Book Review**: Get a quick overview of a chapter from an online book to understand its main arguments before writing a review.

## 🏗️ Project Architecture

### 📁 File Structure

```
84_BookSummaryBot/
├── main.py                 # Entry point to run the FastAPI web application
├── web_app.py              # FastAPI web application with API routes
├── config.py               # Configuration settings for API keys, models, etc.
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (e.g., GEMINI_API_KEY, OPENAI_API_KEY)
├── README.md               # This comprehensive documentation
├── templates/
│   └── index.html          # HTML template for the UI (dashboard layout)
├── static/
│   └── main.css            # Custom CSS for styling (dark mode, etc.)
├── uploads/                # Directory for temporary file uploads
├── utils/
│   └── llm_service.py      # Handles interactions with different LLMs (Gemini, OpenAI)
└── prompts/
    └── summary_prompt.txt  # Prompt template for chapter summarization
```

### 🔧 Technical Stack

| Component          | Technology          | Purpose                                  |
|--------------------|---------------------|------------------------------------------|
| **Backend**        | Python 3.8+         | Core application logic                   |
| **Web Framework**  | FastAPI             | High-performance web server and API      |
| **Template Engine**| Jinja2              | HTML template rendering                  |
| **LLMs**           | Google Gemini API, OpenAI API | News fetching and summary generation     |
| **Frontend**       | HTML5, CSS3, JavaScript | Modern, responsive UI with interactive elements |
| **Styling**        | Tailwind CSS        | Responsive design and aesthetic enhancements |
| **File Handling**  | `aiofiles`, `PyPDF2`, `httpx` | Asynchronous file I/O, PDF parsing, HTTP requests |
| **Environment**    | `python-dotenv`     | Environment variable management          |

### 🎯 Key Components

#### 🤖 BookSummaryAgent (`agent.py`)
- **Orchestration**: Manages the flow from user input to summary generation.
- **Summarization Logic**: Calls the `LLMService` to generate summaries.

#### 🌐 Web Application (`web_app.py`)
- **FastAPI Routes**: Handles `/` (UI) and `/summarize` (API) endpoints.
- **Input Processing**: Manages text input, file uploads (TXT/PDF), and URL fetching.
- **Output Rendering**: Displays the generated summaries and key points.

#### 🧠 LLM Service Utility (`utils/llm_service.py`)
- **LLM Integration**: Interfaces with Google Gemini and OpenAI APIs.
- **Model Selection**: Allows dynamic switching between configured LLMs.
- **Prompt Management**: Reads and formats prompt templates for LLM interaction.

#### ⚙️ Configuration (`config.py`)
- **Centralized Settings**: Defines API keys, default LLM, model names, and other configurable parameters.

## ⚙️ Configuration & Setup

### 🔑 API Key Setup

**Step 1: Get Google Gemini API Key**
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign up or log in to your Google account.
3. Create a new API key.
4. Copy the generated API key (starts with `AIza...`).

**Step 2: Get OpenAI API Key (Optional)**
1. Visit [OpenAI Platform](https://platform.openai.com/account/api-keys)
2. Sign up or log in to your OpenAI account.
3. Create a new secret key.
4. Copy the generated API key (starts with `sk-...`).

**Step 3: Configure the Keys**

Create a `.env` file in the `84_BookSummaryBot` directory with your API keys:

```
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
DEFAULT_LLM=gemini # or openai
```

*   **Important**: Do NOT commit your `.env` file to version control. Ensure your `.gitignore` file includes `.env`.

### 🎛️ Advanced Configuration

Edit `config.py` to customize application settings:

```python
# LLM Model Settings
DEFAULT_LLM = "gemini"  # "gemini" or "openai"
GEMINI_MODEL = "gemini-1.5-flash"  # Or another suitable Gemini model
OPENAI_MODEL = "gpt-4" # Or another suitable OpenAI model

# File Upload Settings
UPLOAD_DIR = "./uploads" # Directory to save temporary uploaded files
```

## 🧪 Testing & Quality Assurance

### 🔍 Installation Testing

After following the "Manual Installation" steps, verify the following:

-   ✅ Python virtual environment is created and activated.
-   ✅ All dependencies listed in `requirements.txt` are installed without errors.
-   ✅ `.env` file is created with your `GEMINI_API_KEY` (and `OPENAI_API_KEY` if used).
-   ✅ The `uploads` directory is created in the project root.

### 🚀 Functional Testing

1.  **Launch the Web UI**: Run `python main.py` and navigate to `http://127.0.0.1:8000`.
2.  **Test Text Input**: Paste a sample chapter text and click "Summarize Chapter". Verify that the "Chapter Summary" section is populated.
3.  **Test File Upload**: Upload a `.txt` file and a `.pdf` file. Ensure summaries are generated correctly.
4.  **Test URL Fetching**: Enter a public URL to a text document or a chapter. Verify summarization.
5.  **Test LLM Switching**: Switch between "Gemini 2.0-flash" and "OpenAI GPT-4" and ensure summaries are generated by the selected model.
6.  **Test Output Actions**: Use the "Copy" and "Download" buttons for both summary and key points to ensure they function correctly.
7.  **Test Dark/Light Mode**: Toggle the theme switch and ensure all UI elements adapt correctly.
8.  **Test Error Handling**: Try submitting without any content, with an unsupported file type, or with an invalid URL to see appropriate error messages.

### 🐛 Troubleshooting

**Common Issues & Solutions:**

| Issue                                   | Cause                               | Solution                                         |
|-----------------------------------------|-------------------------------------|--------------------------------------------------|
| **"API key not found"**               | Missing or invalid API Key          | Ensure `.env` file is correct or API key is set as environment variable. |
| **"Error fetching URL"**              | Network issue or invalid URL        | Check your internet connection or the URL provided. |
| **"Error processing file"**           | Permissions or file content issue   | Ensure the `uploads` directory is writable; check file integrity. |
| **"Error generating summary"**        | LLM API issue or invalid prompt     | Check API keys; simplify content or adjust prompt. |
| **"Port already in use"**             | FastAPI default port (8000) is occupied | Restart your system or use a different port (modify `main.py`). |

## 🔮 Future Roadmap

### 🚀 Planned Features

| Feature                        | Status     | Description                                     |
|--------------------------------|------------|-------------------------------------------------|
| **Summary Length Control**     | 🔄 Planned | Allow users to specify desired summary length (e.g., short, medium, long). |
| **Batch Summarization**        | 🔄 Planned | Enable summarization of multiple chapters or documents at once. |
| **Book-level Summaries**       | 🔄 Planned | Generate summaries for entire books (if feasible with LLM context windows). |
| **Chapter Outline Generation** | 🔄 Planned | Generate a detailed outline or table of contents for a chapter. |
| **Enhanced File Support**      | 🔄 Planned | Add support for more file types like .docx, .epub. |

### 🎯 Enhancement Ideas

-   **Tone Customization**: Allow users to specify the desired tone of the summary.
-   **Contextual Summarization**: Implement a way to provide overall book context for more accurate chapter summaries.
-   **User Authentication**: Implement secure user accounts for saving summaries.
-   **Notification System**: Implement notifications for when a summary is ready.

## 🤝 Contributing

We welcome contributions to make BookSummaryBot even better!

### 🛠️ How to Contribute

1.  **Fork the repository**.f
2.  **Create a feature branch**: `git checkout -b feature/your-feature-name`.
3.  **Make your changes** and test thoroughly.
4.  **Commit your changes**: `git commit -m 'feat: Add amazing new summarization feature'`.
5.  **Push to the branch**: `git push origin feature/your-feature-name`.
6.  **Open a Pull Request** with a clear description of your changes.

### 🎯 Areas for Contribution

-   **UI/UX Improvements**: Further enhance the user interface and experience.
-   **Backend Optimizations**: Improve the efficiency and speed of summary generation and file handling.
-   **New Integrations**: Add support for more LLMs or content sources.
-   **Error Handling**: Make error messages even more user-friendly and robust.
-   **Testing**: Expand unit and integration tests.

### 📋 Contribution Guidelines

-   Follow the existing code style and naming conventions.
-   Add unit tests for new functionality.
-   Update documentation (README.md) as needed.
-   Ensure all automated tests pass.
-   Be respectful and constructive in all interactions.

## 📞 Support & Community

### 🆘 Getting Help

1.  **📖 Documentation**: Refer to this README for comprehensive information.
2.  **🐛 Troubleshooting**: Check the troubleshooting section for common issues.
3.  **📊 Console Logs**: Review your terminal output for any error messages or warnings.
4.  **🌐 Internet Connection**: Ensure you have a stable internet connection for API calls.

### 🐛 Reporting Issues

When reporting issues via GitHub Issues, please include:

-   **System Information**: Your OS, Python version, and browser used.
-   **Full Error Messages**: Copy and paste the complete error traceback if applicable.
-   **Steps to Reproduce**: A clear, concise description of how to reproduce the bug.
-   **Expected vs. Actual Behavior**: What you expected to happen versus what actually occurred.

### 💬 Community

-   **GitHub Issues**: For bug reports and feature requests.
-   **GitHub Discussions**: For general questions, ideas, and sharing your experience.

## 📄 License & Credits

### 📜 License

This project is part of the **#100DaysOfAI-Agents** challenge by **Muhammad Sami Asghar Mughal**.

**MIT License** - Feel free to use, modify, and distribute the code for personal and commercial purposes.

### 🙏 Acknowledgments

-   **Google Gemini API** for powerful AI capabilities.
-   **OpenAI API** for advanced language models.
-   **FastAPI** for the high-performance web framework.
-   **Tailwind CSS** and **Font Awesome** for UI components and icons.
-   **`aiofiles` and `PyPDF2`** for robust file handling.
-   **The Python community** for a rich ecosystem of libraries.
-   **All contributors** who help improve this project.

### 🌟 Inspiration

This project was inspired by the need for a versatile and intelligent tool to streamline the process of understanding and summarizing book chapters, offering flexibility in input methods and LLM choices.

---

<div align="center">

## 🎉 Ready to Summarize Your Next Chapter?

**Get concise, AI-powered summaries of your book chapters with ease!**

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [🎭 Examples](#-examples) • [🏗️ Project Architecture](#-project-architecture)

---

**Made with ❤️ by Muhammad Sami Asghar Mughal for Day 84 of #100DaysOfAI-Agents**

</div>
