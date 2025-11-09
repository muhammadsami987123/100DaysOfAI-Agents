# 📚 EBookReaderAgent - Day 98 of #100DaysOfAI-Agents

<div align="center">

![EBookReaderAgent Banner](https://img.shields.io/badge/EBookReaderAgent-Day%2098-blue?style=for-the-badge&logo=book&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-AI-orange?style=for-the-badge&logo=ai&logoColor=white)
![CLI-First](https://img.shields.io/badge/CLI--First-Lightweight-blue?style=for-the-badge)

**CLI-first eBook reader with AI-powered summaries, key takeaways, and intelligent Q&A. Optional Streamlit UI available.**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎯 Examples](#-examples) • [📚 Documentation](#-documentation) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is EBookReaderAgent?

EBookReaderAgent is a **CLI-first** intelligent AI-powered eBook reader and analyzer that processes PDF and ePub files, extracts their content, and provides quick summaries, key points, and chapter-wise breakdowns to help users understand books faster. 

**⚙️ Design Philosophy:**
- **CLI-First**: Lightweight, fast, and flexible for automation and integration
- **Optional UI**: Streamlit interface available for interactive use
- **Flexible**: Works standalone or can be integrated into other tools

Whether you're a student studying textbooks, a professional reading technical books, or a book lover wanting to quickly grasp the essence of a book, this agent helps you read smarter, not harder.

### 🌟 Key Highlights

- **📄 Multi-Format Support**: Reads both PDF and ePub files seamlessly
- **🤖 AI-Powered Summaries**: Chapter-wise summaries using Gemini 2.0 Flash or GPT-4
- **💡 Key Takeaways**: Automatically extracts top insights and lessons
- **💬 Important Quotes**: Highlights memorable and impactful quotes
- **❓ Q&A System**: Ask questions about book content and get AI-powered answers
- **⏱️ Reading Time**: Calculates estimated reading time
- **📑 Chapter Segmentation**: Automatically identifies and segments chapters
- **🖥️ CLI-First**: Fast command-line interface for quick operations
- **🎨 Optional UI**: Beautiful Streamlit interface for interactive use

## 🎯 Features

### 🚀 Core Functionality
- ✅ **PDF & ePub Support**: Parse and extract content from both formats
- ✅ **URL Support**: Download and analyze books from public URLs
- ✅ **AI Summarization**: Chapter-wise summaries powered by Gemini/OpenAI
- ✅ **Key Takeaways**: Extract top 10+ key insights automatically
- ✅ **Quote Extraction**: Find important and memorable quotes
- ✅ **Q&A System**: Ask questions about specific chapters or entire book
- ✅ **Reading Time Calculator**: Estimate time to read the book
- ✅ **Chapter Navigation**: Easy chapter selection and viewing
- ✅ **Full Book Analysis**: Complete analysis with all features

### 📄 File Processing
- ✅ **PDF Parsing**: Uses PyMuPDF for high-quality text extraction
- ✅ **ePub Parsing**: Uses ebooklib and BeautifulSoup for structured content
- ✅ **URL Download**: Automatically downloads books from public URLs
- ✅ **Chapter Detection**: Automatic chapter segmentation with pattern recognition
- ✅ **Metadata Extraction**: Title, author, page count, word count
- ✅ **Large File Support**: Handles files up to 50MB
- ✅ **Error Handling**: Graceful handling of corrupted or malformed files
- ✅ **Temp File Management**: Automatic cleanup of downloaded files

### 🤖 AI-Powered Features
- ✅ **Smart Summaries**: Context-aware chapter summaries (500 words)
- ✅ **Intelligent Takeaways**: Extracts actionable insights and lessons
- ✅ **Quote Selection**: Identifies meaningful, impactful quotes
- ✅ **Contextual Q&A**: Answers questions based on book content
- ✅ **Multi-LLM Support**: Gemini 2.0 Flash (default) or GPT-4
- ✅ **Prompt Templates**: Customizable prompts for different use cases

### 💻 User Interface
- ✅ **Modern Web UI**: Dark-themed, responsive design
- ✅ **Drag & Drop**: Easy file upload with visual feedback
- ✅ **Chapter List**: Interactive chapter navigation
- ✅ **Real-time Processing**: Live status updates during analysis
- ✅ **Mobile Responsive**: Works on all device sizes
- ✅ **Loading Indicators**: Clear feedback during processing

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.8+** installed on your system
- **Gemini API Key** (get one free from [Google AI Studio](https://makersuite.google.com/app/apikey)) or **OpenAI API Key**
- **Internet connection** for AI analysis

### ⚡ Installation

```bash
# 1. Navigate to project directory
cd 98_EBookReaderAgent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API key (create .env file)
echo GEMINI_API_KEY=your_api_key_here > .env
# OR for OpenAI:
# echo OPENAI_API_KEY=your_api_key_here > .env
# echo DEFAULT_LLM=openai > .env

# That's it! Ready to run.
```

### 🎯 First Run (CLI)

```bash
# Basic usage - analyze a book
python main.py book.pdf --analyze

# Get key takeaways
python main.py book.pdf --takeaways

# Summarize a specific chapter
python main.py book.pdf --chapter 1

# Ask a question
python main.py book.pdf --question "What is the main theme?"

# Get quotes and save to file
python main.py book.pdf --quotes --output quotes.json
```

### 🎨 Optional: Start Streamlit UI

```bash
# Install Streamlit (if not already installed)
pip install streamlit

# Start Streamlit UI
python main.py --streamlit

# Opens automatically at: http://localhost:8501
```

### 🌐 Optional: Start FastAPI Web Interface

```bash
# Install FastAPI dependencies (if not already installed)
pip install fastapi uvicorn

# Start FastAPI web interface
python main.py --web

# Navigate to: http://localhost:8000
```

### 🧪 Test with Sample Book

```bash
# CLI Example
python main.py your_book.pdf --info
python main.py your_book.pdf --takeaways --output takeaways.txt

# Or use Streamlit UI
python main.py --streamlit
# Then upload your book through the web interface
```

## 🎯 Examples & Usage

### 🖥️ CLI Usage (Primary Interface)

The CLI is the default and most efficient way to use EBookReaderAgent:

**Basic Commands:**
```bash
# Show book information (local file)
python main.py book.pdf --info

# Load book from URL
python main.py https://example.com/book.pdf --info

# Full book analysis
python main.py book.pdf --analyze

# Get key takeaways (10 by default)
python main.py book.pdf --takeaways

# Get key takeaways from URL
python main.py https://example.com/book.pdf --takeaways

# Get key takeaways (custom number)
python main.py book.pdf --takeaways --num-takeaways 15

# Summarize all chapters
python main.py book.pdf --summarize

# Summarize specific chapter
python main.py book.pdf --chapter 3

# Extract quotes
python main.py book.pdf --quotes --num-quotes 10

# Ask a question
python main.py book.pdf --question "What is the main theme?"

# Ask question about specific chapter
python main.py book.pdf --question "Explain backpropagation" --question-chapter 2

# Save output to file
python main.py book.pdf --takeaways --output takeaways.json
python main.py book.pdf --chapter 1 --output chapter1_summary.txt

# Use different LLM
python main.py book.pdf --takeaways --llm openai
```

**🎯 Pro Tips:**
- Start with `--info` to see book structure
- Use `--takeaways` for quick overview
- Use `--chapter N` for detailed chapter understanding
- Save outputs with `--output` for later reference
- Combine multiple actions in one command

### 🎨 Streamlit UI (Optional)

For interactive use, the Streamlit UI provides:

1. **📤 Upload Book**: Drag & drop PDF or ePub file
2. **📖 View Book Info**: See title, author, pages, chapters, reading time
3. **📑 Browse Chapters**: Click on any chapter to get its summary
4. **⚡ Quick Actions**: 
   - Summarize all chapters
   - Get key takeaways
   - Extract important quotes
   - Full book analysis
5. **❓ Ask Questions**: Type questions about the book content
6. **📊 Review Results**: View summaries, takeaways, quotes, and answers

**Start Streamlit UI:**
```bash
python main.py --streamlit
```

### 🌐 FastAPI Web Interface (Optional)

For a more traditional web interface:

```bash
python main.py --web
# Navigate to: http://localhost:8000
```

### 📝 Example Workflows

**Scenario 1: Quick Overview (CLI)**
```bash
# Get quick overview of a book (local file)
python main.py DeepLearningForEveryone.pdf --takeaways --output insights.txt

# Or from URL
python main.py https://example.com/DeepLearningForEveryone.pdf --takeaways --output insights.txt
```

**Scenario 2: Detailed Study (CLI)**
```bash
# 1. Check book structure
python main.py DeepLearningForEveryone.pdf --info

# 2. Get all chapter summaries
python main.py DeepLearningForEveryone.pdf --summarize --output summaries.txt

# 3. Deep dive into specific chapter
python main.py DeepLearningForEveryone.pdf --chapter 2 --output chapter2.txt

# 4. Ask specific questions
python main.py DeepLearningForEveryone.pdf --question "Explain backpropagation" --question-chapter 2

# 5. Extract quotes for notes
python main.py DeepLearningForEveryone.pdf --quotes --num-quotes 10 --output quotes.txt
```

**Scenario 3: Interactive Study (Streamlit UI)**
```bash
# Start UI
python main.py --streamlit

# Then in the browser:
# 1. Upload DeepLearningForEveryone.pdf OR enter URL
# 2. View book info: 340 pages, 8 chapters, ~12 hours reading time
# 3. Click "Get Key Takeaways" → Get top 10 insights
# 4. Click on Chapter 2 → Get detailed summary
# 5. Ask: "Explain backpropagation in simple terms"
# 6. Extract quotes for your notes
```

### 🔧 Programmatic Usage

The agent can be used programmatically in your own scripts:

```python
from agent import EBookReaderAgent
from utils.llm_service import LLMService

# Initialize agent
agent = EBookReaderAgent()

# Load a book
result = agent.load_book("path/to/book.pdf")
if result['success']:
    # Get book info
    book_info = agent.get_book_info()
    
    # Summarize a chapter
    summary = agent.summarize_chapter(1)
    
    # Get key takeaways
    takeaways = agent.get_key_takeaways(10)
    
    # Ask a question
    answer = agent.ask_question("What is the main theme?", chapter_number=1)
    
    # Get quotes
    quotes = agent.get_important_quotes(num_quotes=5)
    
    # Full analysis
    analysis = agent.analyze_book(
        include_summaries=True,
        include_takeaways=True,
        include_quotes=True
    )
```

## 📚 Documentation

### 📁 Project Structure

```
98_EBookReaderAgent/
├── agent.py              # Main EBookReaderAgent class
├── config.py             # Configuration and settings
├── main.py               # CLI entry point (primary interface)
├── streamlit_app.py      # Streamlit UI (optional)
├── web_app.py            # FastAPI web application (optional)
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── .gitignore           # Git ignore rules
├── utils/
│   ├── __init__.py
│   ├── book_parser.py   # PDF/ePub parsing logic
│   └── llm_service.py    # LLM integration (Gemini/OpenAI)
├── prompts/
│   ├── chapter_summary_prompt.txt
│   ├── key_takeaways_prompt.txt
│   ├── question_prompt.txt
│   └── quotes_prompt.txt
├── templates/           # FastAPI web UI templates (optional)
│   └── index.html
├── static/              # FastAPI web UI assets (optional)
│   ├── style.css
│   └── script.js
├── uploads/             # Uploaded book files
└── outputs/             # Generated outputs
```

### 🔧 Configuration

Create a `.env` file in the project root:

```env
# Required: At least one API key
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Optional: LLM selection (default: gemini)
DEFAULT_LLM=gemini

# Optional: Model selection
GEMINI_MODEL=gemini-2.0-flash-exp
OPENAI_MODEL=gpt-4o
```

### 📊 API Endpoints

The web application provides the following endpoints:

- `GET /` - Web interface
- `POST /api/upload` - Upload and parse book file
- `GET /api/book-info` - Get book information
- `POST /api/summarize-chapter` - Summarize a specific chapter
- `POST /api/summarize-all` - Summarize all chapters
- `POST /api/key-takeaways` - Get key takeaways
- `POST /api/ask-question` - Ask a question about the book
- `POST /api/get-quotes` - Extract important quotes
- `POST /api/analyze` - Full book analysis
- `POST /api/set-llm` - Switch between Gemini/OpenAI
- `GET /api/status` - Get current status

### 🎨 Customization

#### Custom Prompts

Edit prompt templates in the `prompts/` directory:

- `chapter_summary_prompt.txt` - Chapter summarization
- `key_takeaways_prompt.txt` - Key takeaways extraction
- `question_prompt.txt` - Q&A system
- `quotes_prompt.txt` - Quote extraction

#### Reading Speed

Adjust reading speed in `config.py`:

```python
WORDS_PER_MINUTE = 200  # Change to your reading speed
```

## 🛠️ Technical Details

### 📦 Dependencies

- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **PyMuPDF**: PDF parsing
- **ebooklib**: ePub parsing
- **beautifulsoup4**: HTML parsing for ePub
- **google-generativeai**: Gemini API
- **openai**: OpenAI API
- **python-dotenv**: Environment variable management

### 🔍 How It Works

1. **File Upload**: User uploads PDF or ePub file
2. **Parsing**: BookParser extracts text and segments chapters
3. **Metadata Extraction**: Title, author, pages, word count
4. **AI Processing**: LLM service generates summaries, takeaways, quotes
5. **Results Display**: Formatted results shown in web UI

### 📈 Performance

- **PDF Parsing**: ~1000 pages/second
- **ePub Parsing**: ~500 chapters/second
- **AI Summarization**: ~10-30 seconds per chapter (depends on LLM)
- **File Size Limit**: 50MB (configurable)

## 🎓 Use Cases

### 📚 Academic
- **Textbook Analysis**: Quickly understand complex textbooks
- **Research Papers**: Extract key points from academic papers
- **Study Notes**: Generate summaries for exam preparation

### 💼 Professional
- **Technical Books**: Understand programming/technical concepts faster
- **Business Books**: Extract actionable insights and strategies
- **Training Materials**: Process corporate training documents

### 📖 Personal
- **Book Reviews**: Get quick overviews before reading
- **Reading Lists**: Decide which books to prioritize
- **Note Taking**: Extract quotes and key points automatically

## 🐛 Troubleshooting

### Common Issues

**Issue: "PyMuPDF not installed"**
```bash
pip install PyMuPDF
```

**Issue: "ebooklib not installed"**
```bash
pip install ebooklib beautifulsoup4
```

**Issue: "API key not found"**
- Check `.env` file exists
- Verify API key is correct
- Ensure no extra spaces in `.env` file

**Issue: "File too large"**
- Increase `MAX_FILE_SIZE` in `config.py`
- Or split the book into smaller files

**Issue: "Chapter detection failed"**
- Some books may not have clear chapter markers
- The parser will create a single "Full Book" chapter
- You can still get summaries and takeaways

## 🤝 Contributing

Contributions are welcome! Here are some ways to contribute:

1. **Report Bugs**: Open an issue with detailed information
2. **Suggest Features**: Share your ideas for improvements
3. **Submit PRs**: Fix bugs or add new features
4. **Improve Documentation**: Help make the docs better
5. **Share Use Cases**: Tell us how you're using the agent

## 📝 License

This project is part of the #100DaysOfAI-Agents challenge. Feel free to use, modify, and distribute.

## 🙏 Acknowledgments

- Built as part of #100DaysOfAI-Agents challenge
- Uses Google Gemini and OpenAI for AI capabilities
- Inspired by the need for faster, smarter reading

## 📞 Support

- **Issues**: Open an issue on GitHub
- **Questions**: Check the documentation first
- **Feature Requests**: Open an issue with the "enhancement" label

---

<div align="center">

**Made with ❤️ as part of #100DaysOfAI-Agents**

[⬆ Back to Top](#-ebookreaderagent---day-98-of-100daysofa-agents)

</div>

