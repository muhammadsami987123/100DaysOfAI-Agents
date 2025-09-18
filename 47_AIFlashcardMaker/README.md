# 📚 AIFlashcardMaker - Day 47 of #100DaysOfAI-Agents

<div align="center">

![AIFlashcardMaker Banner](https://img.shields.io/badge/AIFlashcardMaker-Day%2047-blue?style=for-the-badge&logo=book&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5--turbo-orange?style=for-the-badge&logo=openai&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-red?style=for-the-badge&logo=flask&logoColor=white)

**Convert raw educational notes, PDFs, or manual text input into structured flashcards that follow active recall principles.**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎭 Examples](#-examples) • [📚 Documentation](#-documentation) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is AIFlashcardMaker?

AIFlashcardMaker is an intelligent AI-powered study assistant designed to streamline the creation of effective learning materials. It takes your raw educational notes, PDFs, or direct text input and transforms them into structured flashcards, optimized for active recall and spaced repetition.

### 🌟 Key Highlights

- **📝 Flexible Input**: Upload PDFs, paste raw text, or type notes directly.
- **💡 Multiple Flashcard Styles**: Generate Q/A, Fill-in-the-Blanks, and True/False flashcards.
- **🗣️ Multilingual Support**: Flashcards in English, Urdu, and Hindi.
- **📈 Customizable Difficulty**: Tailor flashcards to Easy, Medium, or Advanced levels.
- **🧠 Subject Contextualization**: Optimize flashcard generation based on subject (e.g., Math, Biology, History).
- **💾 Export Options**: Download flashcards in Markdown, JSON, CSV, and potentially Anki-compatible formats.
- **🖥️ Modern UI**: Clean, responsive, and interactive web interface built with TailwindCSS.

## 🎯 Features

### 🚀 Core Functionality
- ✅ **AI Flashcard Generation**: Powered by OpenAI's GPT models for high-quality content.
- ✅ **Document Parsing**: Extracts text from PDF and TXT files.
- ✅ **Interactive Flashcards**: Collapsible cards for active recall.
- ✅ **Customizable Generation**: Control the number, difficulty, subject, and language of flashcards.

### 🎭 Flashcard Styles
- ✅ **Q/A Format**: Classic question and answer style.
- ✅ **Fill-in-the-Blanks**: Sentences with missing key terms for recall practice.
- ✅ **True/False Statements**: Evaluate the accuracy of provided statements.

### 💻 User Interface (UI)
- ✅ **Input Panel**: Dedicated sections for text input, file upload, and AI options.
- ✅ **Output Panel**: Displays generated flashcards interactively.
- ✅ **Download Buttons**: Easy export to popular formats.
- ✅ **Responsive Design**: Seamless experience across devices with TailwindCSS.

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.8+** installed on your system.
- **OpenAI API Key** (get one from [OpenAI Platform](https://platform.openai.com/api-keys)).
- **Internet connection** for AI flashcard generation.

### 🔧 Installation

```bash
# 1. Navigate to the project directory
cd 47_AIFlashcardMaker

# 2. (Optional) Create and activate a virtual environment
python -m venv venv
# Windows
vvenv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variable
# Create a .env file in the project root with your OpenAI API key
echo OPENAI_API_KEY=sk-your_actual_api_key_here > .env
# Replace 'sk-your_actual_api_key_here' with your actual OpenAI API key
```

### 🎯 First Run

```bash
# Start the Flask web application
python main.py

# Open your web browser and navigate to:
# http://127.0.0.1:5000
```

## 🎭 Examples & Usage

### 🌐 Web Interface

The web interface provides an intuitive experience for generating flashcards:

1.  **📝 Provide Input**: Paste raw notes, type directly, or upload a PDF/TXT file.
2.  **🎛️ Customize AI Options**: Select the number of flashcards, difficulty, subject context, and language.
3.  **🚀 Generate Flashcards**: Click "Generate Flashcards" to see the AI-powered output.
4.  **💡 Interactive Review**: Click on questions to reveal answers for active recall.
5.  **💾 Export & Save**: Download your flashcards in Markdown, JSON, or CSV format.

## 🏗️ Project Architecture

### 📁 File Structure

```
47_AIFlashcardMaker/
├── 📄 main.py                   # Main entry point for the Flask app
├── ⚙️ config.py                 # Configuration settings (API keys, upload folder)
├── 🤖 flashcard_agent.py        # Core AI logic for flashcard generation
├── 🌐 web_app.py                # Flask web application, routing, file handling
├── 📋 requirements.txt          # Python dependencies (Flask, PyMuPDF, OpenAI)
├── 📚 templates/                # HTML templates
│   └── index.html              # Main user interface
├── 🎨 static/                   # Static assets
│   ├── css/
│   │   └── style.css           # TailwindCSS for styling
│   └── js/
│       └── app.js              # Frontend interactivity and download logic
├── 📄 README.md                # This comprehensive documentation
├── 📄 .env                     # Environment variables (e.g., OPENAI_API_KEY)
└── 📂 uploads/                 # Temporarily stores uploaded files
```

### 🔧 Technical Stack

| Component       | Technology          | Purpose                                  |
| :-------------- | :------------------ | :--------------------------------------- |
| **Backend**     | Python 3.8+, Flask  | Core application logic, web server       |
| **AI Engine**   | OpenAI GPT-3.5-turbo| Flashcard generation                     |
| **PDF Parsing** | PyMuPDF             | Extracts text from PDF documents         |
| **Frontend**    | HTML5, JavaScript   | Interactive user interface               |
| **Styling**     | TailwindCSS         | Modern, responsive design                |
| **Data Format** | JSON                | API communication and flashcard structure|

### 🎯 Key Components

#### 🤖 FlashcardAgent (`flashcard_agent.py`)
- **Core AI Logic**: Integrates with OpenAI API to generate flashcards.
- **Flashcard Styles**: Crafts Q/A, Fill-in-the-Blanks, and True/False cards.
- **Prompt Engineering**: Dynamically constructs prompts based on user options.

#### 🌐 Web Application (`web_app.py`)
- **Flask App**: Manages routes (`/`, `/generate`).
- **File Handling**: Securely uploads and processes PDF/TXT files.
- **Text Extraction**: Calls parsing functions for uploaded documents.
- **API Integration**: Connects frontend requests to the `FlashcardAgent`.
- **Error Handling**: Provides user-friendly error responses.

#### 🎨 Frontend (`static/`, `templates/`)
- **`index.html`**: The main UI with input forms, AI options, and output display.
- **`style.css`**: Utilizes TailwindCSS for a modern and responsive look.
- **`app.js`**: Handles form submissions, displays interactive flashcards, and manages download functionalities (Markdown, JSON, CSV).

#### ⚙️ Configuration (`config.py`)
- **API Key Management**: Securely loads OpenAI API key.
- **File Upload Settings**: Defines allowed file extensions and upload folder.
- **Application Secrets**: Stores `SECRET_KEY` for Flask session management.

## ⚙️ Configuration & Setup

### 🔑 API Key Setup

**Step 1: Get OpenAI API Key**
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign up or log in to your account
3. Navigate to "API Keys" section
4. Create a new API key
5. Copy the key (starts with `sk-`)

**Step 2: Configure the Key**

Create a `.env` file in the root of the `47_AIFlashcardMaker` directory and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your_actual_api_key_here
```

**Important**: Replace `sk-your_actual_api_key_here` with your actual key. Do not share your API key publicly or commit it to version control.

### 🎛️ Advanced Configuration

Edit `config.py` to customize application settings:

```python
# config.py
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_secret_key'
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'pdf', 'txt'}
```

## 🧪 Testing & Quality Assurance

### 🔍 Verification Steps

1.  **Run Application**: Ensure `python main.py` starts without errors.
2.  **UI Interaction**: Verify all input fields, selectors, and buttons are functional.
3.  **Flashcard Generation**: Test with sample text and PDF/TXT files.
4.  **Interactive Cards**: Confirm flashcards toggle visibility correctly.
5.  **Download Functionality**: Verify Markdown, JSON, and CSV downloads work and contain correct data.
6.  **Error Handling**: Test with invalid inputs (e.g., no text, unsupported file types).

### 🐛 Troubleshooting

**Common Issues & Solutions:**

| Issue                               | Cause                           | Solution                                                                |
| :---------------------------------- | :------------------------------ | :---------------------------------------------------------------------- |
| **Flashcards not appearing**        | Frontend JS error, Backend API error, No content extracted, OpenAI error | Check browser console, server logs, API key, input content.             |
| **Download buttons not working**    | Frontend JS error               | Check browser console for errors in `app.js` download functions.        |
| **"OpenAI API key not found"**      | Missing or invalid API key      | Ensure `OPENAI_API_KEY` is set in `.env` file.                          |
| **"Module not found"**              | Missing dependencies            | Run `pip install -r requirements.txt`.                                  |
| **"Error extracting text from PDF"**| Corrupted PDF, PyMuPDF issue    | Try a different PDF, ensure `pymupdf` is installed correctly.           |

## 🔮 Future Roadmap

### 🚀 Planned Features

- **Anki-compatible Export**: Add direct export in a format compatible with Anki.
- **Image/Multimedia Flashcards**: Support for generating flashcards with images or audio.
- **Advanced AI Models**: Integration with newer or specialized AI models for better flashcard quality.
- **User Accounts & Persistence**: Allow users to save and manage their flashcards across sessions.
- **Spaced Repetition System**: Implement a basic SRS to optimize learning.

## 🤝 Contributing

We welcome contributions! Please refer to the GitHub repository for guidelines on how to contribute, report issues, or suggest new features.

## 📞 Support & Community

For questions, issues, or discussions, please visit the GitHub repository.

## 📄 License & Credits

This project is part of the **#100DaysOfAI-Agents** challenge by **Muhammad Sami Asghar Mughal**.

**MIT License** - Feel free to use, modify, and distribute!

---

<div align="center">

## 🎉 Ready to Master Your Studies?

**Transform your learning experience with AI-powered flashcards!**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎭 Examples](#-examples) • [📚 Documentation](#-documentation)

---

**Made with ❤️ by the #100DaysOfAI-Agents community**

*Day 47 of 100 - Building the future of AI agents, one day at a time!*

</div>
