# 📝 GPTNotepad - Smart Notepad with Auto Summaries | Day 79 of #100DaysOfAI-Agents


<div align="center">

![AI Models](https://img.shields.io/badge/AI-Gemini%202.0%20%7C%20OpenAI-orange?style=for-the-badge&logo=google&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8%2B-green?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20Framework-teal?style=for-the-badge&logo=fastapi&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-UI-blue?style=for-the-badge&logo=tailwindcss)

**Your intelligent notepad that summarizes your thoughts, meetings, and ideas instantly!**

</div>

---

## ✨ What is GPTNotepad?

GPTNotepad is an intelligent web-based notepad application that allows users to write free-form notes, upload files, or provide URLs, and automatically generates concise, bullet-point summaries and full extracted notes using either Google Gemini (default) or OpenAI's GPT models. It's perfect for quickly distilling key information from various sources like journal entries, meeting logs, task lists, brainstorming sessions, documents, or web pages.

### 🌟 Key Highlights

-   **🧠 AI-Powered Summarization**: Leverages Google Gemini (default) or OpenAI GPT for accurate and concise summaries (3-6 bullet points).
-   **⚙️ Dual LLM Support**: Configurable to use Google Gemini 2.0 Flash (default) or OpenAI GPT models with intelligent fallback.
-   **📝 Multi-Modal Input**: Seamlessly input notes via manual text entry, file upload (.txt, .pdf, .docx), or public URL.
-   **💡 Dual Output Panes**: Simultaneously view a concise **Summary** (left) and the **Full Extracted Notes** (right).
-   **🚀 Enhanced UI/UX**: Professional, clean, and user-friendly web interface with a deep black theme, gold accents, glassmorphic cards, and responsive design.
-   **💾 Copy & Download**: Easily copy the summary or notes to clipboard, or download them as `.txt` files.
-   **⚡ Live Feedback**: Includes a loading spinner and toast notifications for user actions and AI processing.
-   **⚙️ Easy Setup**: Simple environment variable configuration for your API keys.

---

## 💡 Real-World Problem Solved

GPTNotepad addresses the growing need for efficient information processing and knowledge management in both personal and professional contexts. It helps users:

-   **Overcome Information Overload**: Quickly condense lengthy articles, meeting notes, or documents into digestible summaries.
-   **Boost Productivity**: Reduce time spent on manual summarization, allowing focus on high-value tasks.
-   **Enhance Learning & Retention**: Distill key concepts from educational materials or research papers.
-   **Streamline Content Creation**: Rapidly generate summaries for reports, presentations, or social media.
-   **Centralize Data**: Process information from various sources (manual, files, web) in one intuitive platform.

---

## 🎯 Features

### Frontend (HTML + Tailwind CSS + Vanilla JS)

-   ✅ **Two-Pane Layout**: Summary on the left, editable notes/input on the right, always visible.
-   ✅ **Multi-Input Tabs**: Easily switch between "Manual" text input, "File" upload, and "URL" input.
-   ✅ **Editable Notes Area**: Manually type or edit extracted notes in the right pane.
-   ✅ **"Summarize" Button**: Initiates the AI summarization process.
-   ✅ **Copy & Download Buttons**: Dedicated buttons to copy or download content from both Summary and Notes panes.
-   ✅ **Loading Spinner & Toasts**: Visual feedback for ongoing processes and user actions.
-   ✅ **Advanced Dark Mode**: A deep black theme with elegant gold and white highlights, consistent with preferred UI examples.
-   ✅ **Responsive Design**: Optimal viewing and interaction across various devices.

### Backend (Python + FastAPI + Dual LLM Support)

-   ✅ **FastAPI Endpoint**: A robust `/summarize` endpoint to handle all input types (text, file, URL).
-   ✅ **OpenAI/Gemini Integration**: Uses `openai` SDK and `google.generativeai` for summarization.
-   ✅ **Intelligent LLM Fallback**: Prioritizes Gemini (default) and falls back to OpenAI if the primary is unavailable or not configured.
-   ✅ **File Content Extraction**: Extracts text from `.txt`, `.pdf` (using `PyPDF2`), and `.docx` (using `python-docx`) files.
-   ✅ **URL Content Extraction**: Fetches and extracts main textual content from public web pages (using `requests` and `BeautifulSoup4`).
-   ✅ **Structured Output**: Always returns both a clean bullet-point summary and the full extracted/processed notes.
-   ✅ **Strict Prompt Logic**: Ensures summaries are 3-6 bullet points, focused, and neutral in tone.
-   ✅ **Error Handling**: Gracefully handles missing API keys, content extraction failures, and summarization errors.

### Prompt Logic

-   ✅ **Concise Output**: Returns only clean bullet-point output.
-   ✅ **No Extra Info**: Strictly avoids adding or assuming information not present in the note.
-   ✅ **Professional Tone**: Maintains a professional, neutral tone as per instructions.

---

## 🚀 Quick Start

### 📋 Prerequisites

-   **Python 3.8+** installed on your system.
-   **Google Gemini API Key** (from [Google AI Studio](https://aistudio.google.com/app/apikey)) **OR** **OpenAI API Key** (from [OpenAI Platform](https://platform.openai.com/api-keys)).
-   **Internet connection** for AI summarization.

### ⚡ Installation

```bash
# 1. Navigate to the project directory
cd 79_GPTNotepad

# 2. Run the one-click installation script (Windows)
# This will create a virtual environment and install all dependencies.
install.bat

# --- OR ---

# 2. Manual Installation (macOS/Linux or if install.bat has issues)
# Create and activate a virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 3. Install Python dependencies
pip install -r requirements.txt
```

### 🔑 API Key Setup

1.  **Obtain API Keys**:
    *   For **Google Gemini**: Visit [Google AI Studio](https://aistudio.google.com/app/apikey) and create a new API key.
    *   For **OpenAI GPT**: Visit [OpenAI Platform](https://platform.openai.com/api-keys) and create a new API key.
2.  **Configure `.env` File**:
    *   Create a file named `.env` in the root directory of `79_GPTNotepad/` (at the same level as `main.py`).
    *   Add your API keys and configure the preferred LLM model. **Gemini is the default model.**

    ```dotenv
    # Required: Set your preferred LLM model ("gemini" or "openai"). Gemini is default.
    LLM_MODEL=gemini 

    # Optional: Google Gemini API Key and Model (used if LLM_MODEL=gemini)
    GEMINI_API_KEY=your_google_gemini_api_key_here
    GEMINI_MODEL=gemini-2.0-flash # Or another Gemini model like gemini-1.5-pro

    # Optional: OpenAI API Key and Model (used if LLM_MODEL=openai or as fallback)
    OPENAI_API_KEY=your_openai_api_key_here
    OPENAI_MODEL=gpt-3.5-turbo    # Or another GPT model like gpt-4o-mini
    
    # Server settings (optional)
    HOST=0.0.0.0
    PORT=8000
    DEBUG=True
    ```

### 🎯 First Run

1.  **Start the FastAPI application** from the `79_GPTNotepad/` directory:
    ```bash
    # On Windows (uses start.bat which activates venv and runs main.py)
    start.bat

    # On macOS/Linux (after activating venv manually)
    source venv/bin/activate
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```
2.  **Open your web browser** and navigate to: [http://localhost:8000](http://localhost:8000)

---

## 💡 Usage Examples

The GPTNotepad provides a sleek, interactive web interface:

1.  **📝 Manual Input**:
    *   Select the `✍️ Manual` tab.
    *   Type or paste your notes directly into the editable text area on the right pane.
    *   Click `Summarize`. The summary will appear on the left, and your full notes will remain on the right.
2.  **📄 File Upload**:
    *   Select the `📄 File` tab.
    *   Click "Choose File" and upload a `.txt`, `.pdf`, or `.docx` document.
    *   Click `Summarize`. The agent will extract content, summarize it, and display both outputs.
3.  **🌐 URL Input**:
    *   Select the `🌐 URL` tab.
    *   Paste a public web page URL (e.g., `https://en.wikipedia.org/wiki/Artificial_intelligence`) into the input field.
    *   Click `Summarize`. The agent will fetch the web page, extract main content, and provide the summary and notes.
4.  **Copy & Download**:
    *   Use the `📋 Copy` buttons to quickly copy the content of either the Summary or Notes pane.
    *   Use the `⬇️ Download` buttons to save the content as a `.txt` file.
5.  **Dark Mode**: Toggle the `🌙`/`☀️` button in the header to switch between the dark and light themes.

---

## 🏗️ Project Architecture

### 📁 File Structure

```
79_GPTNotepad/
  ├── main.py                # Main FastAPI application entry point, API routes, static files
  ├── config.py              # Centralized configuration (API keys, models, server settings)
  ├── agents/
  │   └── agent.py           # Core AI logic: LLM integration, text extraction (files/URLs), summarization
  ├── frontend/
  │   └── index.html         # Main web UI (HTML, inline Tailwind CSS, inline JavaScript for interactivity)
  ├── prompts/
  │   └── summarizer_prompt.txt # AI prompt template for summarization tasks
  ├── .env                   # Environment variables (for API keys and other settings)
  ├── requirements.txt       # Python dependencies
  ├── install.bat            # Windows one-click installation script (creates venv, installs deps)
  ├── start.bat              # Windows one-click startup script (activates venv, runs main.py)
  └── test_gptnotepad.py     # Pytest script for API backend testing
```

### 🔧 Technical Stack

| Component            | Technology                | Purpose                                                                |
| :------------------- | :------------------------ | :--------------------------------------------------------------------- |
| **Backend Framework**| Python 3.8+, FastAPI      | Robust, high-performance API and web server.                           |
| **AI Engine**        | Google Gemini API, OpenAI API | Powers intelligent summarization with dual-model support.              |
| **Text Extraction**  | `PyPDF2`, `python-docx`, `requests`, `BeautifulSoup4` | Extracts text from various document types and web pages.               |
| **Web Frontend**     | HTML5, Tailwind CSS       | Modern, responsive, and aesthetically pleasing user interface with custom animations. |
| **Client-side Logic**| Vanilla JavaScript        | Manages UI interactivity, dynamic content updates, and API calls.      |
| **Environment Mgmt.**| `python-dotenv`           | Securely loads environment variables.                                  |
| **ASGI Server**      | `Uvicorn`                 | Lightning-fast ASGI server for FastAPI.                                |
| **Data Validation**  | `Pydantic`                | Ensures data integrity for API requests.                               |
| **Testing**          | `pytest`, `fastapi.testclient` | Comprehensive unit and integration testing for backend logic.          |

### 🎯 Key Components

#### 🧠 `agents/agent.py` - The AI Brain

-   **LLM Integration**: Initializes and manages API clients for both Google Gemini and OpenAI.
-   **Intelligent Fallback**: Attempts summarization with Gemini first, then falls back to OpenAI if configured.
-   **Content Extraction**: Contains methods to read and extract plain text from `.txt`, `.pdf`, `.docx` files, and public web pages.
-   **Summarization Logic**: Formats the prompt and interacts with the chosen LLM to generate concise summaries (3-6 bullet points) and returns full extracted notes.

#### 🌐 `main.py` - The FastAPI Server

-   **Application Entry**: Initializes the FastAPI application and mounts static files (`frontend/`).
-   **API Endpoints**: Defines the `/` route to serve `index.html` and the `/summarize` POST endpoint.
-   **Input Handling**: Processes incoming requests, prioritizing file uploads, then URLs, then manual text.
-   **Agent Orchestration**: Calls the `GPTSummarizerAgent` for content extraction and summarization.
-   **Response Formatting**: Returns JSON containing both the `summary` (list of strings) and `notes` (full string).

#### 🎨 `frontend/index.html` - The User Interface

-   **Single-File Frontend**: Contains all HTML structure, Tailwind CSS configuration, custom CSS styles, and JavaScript logic.
-   **Dynamic Layout**: Implements the two-pane interface and input mode switching.
-   **User Interaction**: Handles form submissions, button clicks, theme toggling, and displays AI responses.
-   **Visual Feedback**: Manages loading spinners, toast notifications, and error messages.
-   **Modern Aesthetics**: Utilizes Tailwind CSS with custom styling for a sleek, dark-themed, glassmorphic design.

---

## ⚙️ Configuration & Setup

### Environment Variables

-   `LLM_MODEL`: (`string`, default: "gemini") - Specifies the primary LLM to use. Options: `gemini`, `openai`.
-   `GEMINI_API_KEY`: (`string`, required if `LLM_MODEL=gemini`) - Your Google Gemini API key.
-   `GEMINI_MODEL`: (`string`, default: "gemini-2.0-flash") - The specific Gemini model to use.
-   `OPENAI_API_KEY`: (`string`, required if `LLM_MODEL=openai` or as a fallback) - Your OpenAI API key.
-   `OPENAI_MODEL`: (`string`, default: "gpt-3.5-turbo") - The specific OpenAI GPT model to use.
-   `HOST`: (`string`, default: "0.0.0.0") - The host address for the FastAPI server.
-   `PORT`: (`int`, default: 8000) - The port for the FastAPI server.
-   `DEBUG`: (`boolean`, default: `True`) - Enables/disables debug mode for FastAPI.

---

## 🧪 Testing & Quality Assurance

### 🔍 API Backend Testing

To ensure the backend API is functioning correctly for all input types and edge cases, a `pytest` suite is included.

```bash
# Navigate to the project directory
cd 79_GPTNotepad

# Run all backend tests
pytest test_gptnotepad.py
```

**Test Coverage:**
-   ✅ **Manual Note Input**: Verifies summarization and notes generation for direct text input.
-   ✅ **.txt File Upload**: Confirms correct text extraction and AI processing for plain text files.
-   ✅ **.pdf File Upload**: Tests PDF text extraction and subsequent summarization.
-   ✅ **URL Content Extraction**: Validates fetching and processing of content from public URLs.
-   ✅ **Dual Output**: Ensures the API always returns both a `summary` and `notes`.
-   ✅ **Error Handling**: Checks graceful responses for empty inputs or API failures.

---

## 🐛 Troubleshooting

### Common Issues & Solutions

| Issue                                    | Probable Cause                                                      | Solution                                                                                                                               |
| :--------------------------------------- | :------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------- |
| `API Key not found` (Gemini/OpenAI)      | Missing or incorrect `GEMINI_API_KEY` or `OPENAI_API_KEY` in `.env`.| Verify `.env` file exists in the root directory and contains correct API keys for the chosen `LLM_MODEL`.                              |
| `Failed to generate summary`             | LLM API quota exceeded, invalid model, or network issue.            | Check your API key credits, chosen `LLM_MODEL`, and internet connection. Review backend logs for specific API errors.                 |
| `Failed to extract text from ...`        | Unsupported file type, malformed file, or inaccessible URL.       | Ensure file is `.txt`, `.pdf`, or `.docx`. Check URL for public accessibility and correctness. Inspect backend logs for extraction errors. |
| `ModuleNotFoundError`                    | Missing Python dependencies.                                        | Run `pip install -r requirements.txt` after activating your virtual environment.                                                       |
| `Port 8000 already in use`               | Another application is using `http://localhost:8000`.               | Change the `PORT` in `config.py` to an available port (e.g., `8001`) or terminate the conflicting process.                            |
| Unformatted UI / Incorrect styles        | Tailwind CSS not loading or classes misapplied (less likely with inline CSS). | Ensure Tailwind CDN is correctly linked in `index.html`. Inspect browser developer tools for any CSS loading errors.                     |
| `pdfplumber` or `python-docx` related errors | Missing system dependencies for PDF/DOCX processing (rare).       | Ensure necessary system libraries for `PyPDF2` (minimal, usually fine) or `python-docx` are met. Check library specific documentation. |

---

## 🔮 Future Roadmap

### 🚀 Planned Enhancements

-   **Note Persistence**: Implement local storage or a small database (e.g., SQLite) to save user notes and summaries across sessions.
-   **Categorization/Tagging**: Allow users to categorize or tag notes for better organization and searchability.
-   **Export Options**: Expand download options to include `.md` (Markdown) format or combined `.html` output.
-   **Summary Refinement**: Add UI elements to allow users to provide feedback on summaries for iterative improvement.
-   **Custom Prompt Settings**: Provide advanced users with the option to customize the summarization prompt.
-   **Multi-language Support**: Implement language detection and summarization in multiple languages.
-   **Image-to-Text for Notes**: Integrate OCR (Optical Character Recognition) for images containing text to convert them into editable notes.

---

## 🤝 Contributing

We welcome and encourage contributions to enhance GPTNotepad! If you have valuable suggestions, discover bugs, or wish to contribute code, please follow these guidelines:

1.  **Fork the repository** on GitHub.
2.  **Create a dedicated feature branch**: `git checkout -b feature/add-new-export-option`.
3.  **Implement your changes** and ensure they are thoroughly tested.
4.  **Commit your changes** with a clear and descriptive message: `git commit -m 'feat: Add Markdown export for summaries'`.
5.  **Push your branch** to your forked repository: `git push origin feature/add-new-export-option`.
6.  **Open a Pull Request** against the main repository, providing a detailed description of your contributions.

---

## 📄 License & Credits

This project is proudly open-sourced under the **MIT License**.

### 🙏 Acknowledgments

-   **Google Gemini** for the powerful Gemini models.
-   **OpenAI** for the powerful GPT models.
-   **FastAPI** for providing a robust and easy-to-use web framework.
-   **Tailwind CSS** for simplifying UI development and enabling beautiful designs.
-   **PyPDF2**, **python-docx**, **requests**, and **BeautifulSoup4** for robust content extraction.

---

<div align="center">

## 🎉 Ready to Smarten Up Your Notes?

**Start summarizing your thoughts with AI today!**

</div>
