# 🔍 CodeReviewerBot - Day 13 of #100DaysOfAI-Agents

An intelligent AI-powered code review agent that provides professional-grade feedback on your code, just like a senior developer would. Features comprehensive analysis, multi-language support, and actionable suggestions for code improvement.

---

## ✨ What's Included

- **Multi-Input Support**: 
  - Direct code pasting with syntax highlighting
  - File upload (.py, .js, .java, .cpp, .cs, .php, .go, .rs, .swift, .kt)
  - GitHub URL integration for public repositories
- **AI-Powered Analysis**: 
  - Comprehensive code review using OpenAI GPT-4
  - Syntax error detection and suggestions
  - Best practices recommendations
  - Performance optimization tips
  - Security vulnerability identification
  - Readability and maintainability assessment
- **Multi-Language Support**: 
  - **Programming Languages**: Python, JavaScript, Java, C++, C#, PHP, Go, Rust, Swift, Kotlin
  - **UI Languages**: English, Hindi, Urdu
- **Structured Feedback**: 
  - Categorized issues (syntax, best practices, performance, security, readability)
  - Severity levels (critical, high, medium, low)
  - Line-specific suggestions with code snippets
  - Refactored code generation
  - Downloadable improved code
- **Modern Web Interface**: 
  - Beautiful glassmorphism design with Tailwind CSS
  - CodeMirror editor with syntax highlighting
  - Responsive layout for all devices
  - Interactive tabs for different feedback types
  - Real-time GitHub URL validation
  - Drag-and-drop file upload
- **Professional Features**: 
  - Code quality scoring (readability, performance, security, etc.)
  - Code statistics and complexity analysis
  - Session-based processing (no data saved)
  - Comprehensive error handling

---

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.8+)
- **AI Engine**: OpenAI GPT-4 for intelligent code analysis
- **Frontend**: HTML + Tailwind CSS + Vanilla JavaScript
- **Code Editor**: CodeMirror with syntax highlighting
- **GitHub Integration**: GitHub API for repository access
- **Server**: Uvicorn ASGI server
- **Configuration**: `python-dotenv` for environment variables

---

## 🚀 Quick Start

### 1. Clone and Navigate
```bash
cd 13_CodeReviewerBot
```

### 2. Install Dependencies
```bash
# Windows (PowerShell)
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# macOS/Linux
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Environment

**Option A: Automatic Setup (Recommended)**
```bash
python setup.py
```

**Option B: Manual Setup**
Create a `.env` file in the project directory:
```env
OPENAI_API_KEY=sk-your-openai-api-key-here
PORT=8013
MAX_FILE_SIZE=10485760
# Recommended model settings
# For larger files, prefer a model with a big context window
# Examples: gpt-4-turbo, gpt-4-1106-preview
OPENAI_MODEL=gpt-4-turbo
# Upper bound for completion tokens (the app will auto-clamp safely)
MAX_TOKENS=4000
TEMPERATURE=0.3
```

**Getting Your OpenAI API Key:**
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

**Important:** The application requires a valid OpenAI API key to function. Without it, you'll see "Code review failed" errors.

Tip: If you plan to analyze longer files, set `OPENAI_MODEL` to a variant with a larger context window (e.g., `gpt-4-turbo`). The backend automatically sizes responses to avoid context overflow.

### 4. Run the Application
```bash
# Windows (PowerShell)
python server.py

# macOS/Linux
python server.py
```

### 5. Open in Browser
Navigate to `http://localhost:8013` to access the web interface.

---

## 💡 Using the App

### Input Methods

#### 📝 Paste Code
- Click the "Paste Code" card
- Use the CodeMirror editor with syntax highlighting
- Auto-detection of programming language
- Manual language selection available

#### 📁 Upload File
- Click the "Upload File" card
- Drag and drop or click to select files
- Supports: `.py`, `.js`, `.jsx`, `.ts`, `.tsx`, `.java`, `.cpp`, `.cc`, `.cxx`, `.h`, `.hpp`, `.cs`, `.php`, `.go`, `.rs`, `.swift`, `.kt`, `.kts`
- Automatic language detection from file extension

#### 🔗 GitHub URL
- Click the "GitHub URL" card
- Paste GitHub repository or file URLs
- Supports:
  - Individual files: `https://github.com/user/repo/blob/main/file.py`
  - Repositories: `https://github.com/user/repo` (fetches first code file)
- Real-time URL validation

### Review Results

#### 📊 Summary Dashboard
- **Issue Counts**: Total, Critical, High, Medium, Low
- **Quality Scores**: Readability, Code Quality, Performance, Best Practices, Security
- **Code Statistics**: Lines, functions, classes, complexity

#### 🔍 Issues Tab
- Categorized issues with severity levels
- Line-specific suggestions
- Code snippets for context
- Actionable improvement recommendations

#### 💡 Suggestions Tab
- General improvement suggestions
- Best practices recommendations
- Code optimization tips

#### 🔧 Refactored Code Tab
- Improved version of your code
- Syntax highlighting
- Download functionality
- Preserves original logic while improving structure

#### 📈 Summary Tab
- Overall assessment
- Code complexity analysis
- Detailed recommendations

---

## 🧩 API Endpoints

### Main Review Endpoint
```
POST /api/review
```

**Request Parameters:**
- `code` (optional): Direct code input
- `language` (optional): Programming language
- `ui_language`: UI language (english, hindi, urdu)
- `file` (optional): Uploaded code file
- `github_url` (optional): GitHub repository/file URL

**Response:**
```json
{
  "success": true,
  "message": "Code analysis completed successfully!",
  "data": {
    "language": "python",
    "filename": "example.py",
    "issues": [...],
    "suggestions": [...],
    "refactored_code": "...",
    "scores": {...},
    "summary": "...",
    "statistics": {...},
    "timestamp": "..."
  }
}
```

### GitHub Validation
```
POST /api/validate-github
```

### Supported Languages
```
GET /api/languages
```

### Health Check
```
GET /api/health
```

### Quick cURL examples

```bash
# Paste code directly
curl -s -X POST http://localhost:8013/api/review \
  -F ui_language=english \
  -F language=python \
  -F code='def hello():\n    print("hi")'

# Upload a file
curl -s -X POST http://localhost:8013/api/review \
  -F ui_language=english \
  -F file=@path/to/your.py
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | Required | Your OpenAI API key for GPT-4 |
| `PORT` | `8013` | Server port number |
| `HOST` | `0.0.0.0` | Server host address |
| `MAX_FILE_SIZE` | `10485760` | Maximum file upload size (10MB) |
| `OPENAI_MODEL` | `gpt-4` | OpenAI model to use |
| `MAX_TOKENS` | `4000` | Maximum tokens for AI response |
| `TEMPERATURE` | `0.3` | AI response creativity (0-1) |

### Supported Programming Languages

| Language | Extensions | Best Practices Focus |
|----------|------------|---------------------|
| **Python** | `.py`, `.pyw` | PEP 8, type hints, docstrings, error handling |
| **JavaScript** | `.js`, `.jsx`, `.ts`, `.tsx` | ES6+, arrow functions, async/await, error handling |
| **Java** | `.java` | Naming conventions, access modifiers, exception handling |
| **C++** | `.cpp`, `.cc`, `.cxx`, `.h`, `.hpp` | RAII, smart pointers, STL, const correctness |
| **C#** | `.cs` | Naming conventions, LINQ, async/await, properties |
| **PHP** | `.php` | PSR standards, namespaces, type declarations |
| **Go** | `.go` | Naming conventions, error handling, interfaces |
| **Rust** | `.rs` | Ownership system, error handling, traits |
| **Swift** | `.swift` | Naming conventions, optionals, protocols |
| **Kotlin** | `.kt`, `.kts` | Kotlin idioms, null safety, coroutines |

---

## 📁 Project Structure

```
13_CodeReviewerBot/
├── server.py                 # FastAPI application and routes
├── code_review_service.py    # AI-powered code review logic
├── github_service.py         # GitHub API integration
├── config.py                 # Configuration and constants
├── requirements.txt          # Python dependencies
├── templates/
│   └── index.html           # Modern web interface
├── static/
│   └── js/
│       └── app.js           # Frontend JavaScript logic
├── uploads/                  # File upload directory
├── outputs/                  # Generated files directory
├── install.bat              # Windows installation script
├── start.bat                # Windows startup script
└── README.md                # This file
```

---

## 🎨 UI Features

### Design Elements
- **Glassmorphism**: Semi-transparent cards with backdrop blur
- **Gradient Backgrounds**: Beautiful blue-to-purple gradients
- **Interactive Cards**: Clickable input method selection
- **CodeMirror Integration**: Professional code editor with syntax highlighting
- **Responsive Layout**: Works perfectly on desktop, tablet, and mobile

### User Experience
- **Intuitive Navigation**: Clear visual hierarchy and intuitive controls
- **Real-time Feedback**: Loading states, error messages, and success indicators
- **Accessibility**: Proper labels, focus states, and keyboard navigation
- **Modern Icons**: Font Awesome icons throughout the interface
- **Smooth Animations**: Fade-in animations and hover transitions

---

## 🧪 Testing Examples

### Python Code Review
```python
def calculate_factorial(n):
    if n == 0:
        return 1
    else:
        return n * calculate_factorial(n-1)

result = calculate_factorial(5)
print(result)
```

**Expected Feedback:**
- Missing type hints
- No error handling for negative numbers
- Recursive approach could cause stack overflow
- Missing docstring
- Variable naming could be improved

### JavaScript Code Review
```javascript
function getData() {
    fetch('/api/data')
        .then(response => response.json())
        .then(data => {
            console.log(data);
        });
}
```

**Expected Feedback:**
- Missing error handling
- No async/await usage
- Missing loading states
- No input validation
- Hardcoded URL

### GitHub Integration
- **File URL**: `https://github.com/username/repo/blob/main/src/main.py`
- **Repository URL**: `https://github.com/username/repo`

---

## 🐛 Troubleshooting

### Common Issues

#### 1. "OpenAI API key not found"
- Ensure you've created a `.env` file with your API key
- Check that the key starts with `sk-` and is valid
- Verify you have sufficient OpenAI API credits

#### 2. "Invalid file format" errors
- Check that uploaded files have supported extensions
- Ensure files are text-based code files (not binaries)
- Verify file size is under 10MB

#### 3. "GitHub fetch failed" errors
- Ensure the GitHub URL is from a public repository
- Check that the URL format is correct
- Verify the repository/file exists and is accessible

#### 4. "Code analysis failed" errors
- Check your internet connection
- Verify your OpenAI API key is valid and has sufficient credits
- Try with smaller code snippets first
- Check server logs for detailed error messages

#### 5. "Code review failed" errors in the web interface
- **Most common cause**: Missing or invalid OpenAI API key
- Run `python setup.py` to configure your API key
- Check that your `.env` file exists and contains a valid API key
- Ensure you have sufficient OpenAI API credits

#### 6. "context_length_exceeded" or "maximum context length is ... tokens"
This means the combined prompt (instructions + your code) is bigger than the model's context window.

- Reduce the file size or analyze in smaller parts
- Prefer a model with a larger context window (e.g., set `OPENAI_MODEL=gpt-4-turbo` in `.env`)
- Keep `MAX_TOKENS` reasonable; the app auto-clamps but very large values are unnecessary
- The backend now estimates prompt size and returns a friendly error before sending oversized requests

### PowerShell Issues (Windows)
If you encounter `&&` syntax errors in PowerShell:
```powershell
# Use this instead:
cd 13_CodeReviewerBot; python server.py

# Or run commands separately:
cd 13_CodeReviewerBot
python server.py
```

---

## 🔮 Future Enhancements

Potential improvements for future versions:
- **Batch Processing**: Review multiple files at once
- **Custom Rules**: User-defined code review rules
- **Integration**: GitHub Actions, GitLab CI, VS Code extension
- **Advanced Analysis**: Cyclomatic complexity, code smells detection
- **Team Features**: Shared review history, team standards
- **Export Formats**: PDF reports, JUnit XML, SARIF
- **Performance**: Caching, incremental analysis
- **Security**: Advanced vulnerability scanning
- **Mobile App**: Native mobile applications
- **API Rate Limiting**: Better handling of API quotas

---

## 📝 License

This project is part of the #100DaysOfAI-Agents challenge by Muhammad Sami Asghar Mughal.

---

## 🤝 Contributing

Feel free to contribute to this project by:
- Reporting bugs and issues
- Suggesting new features and improvements
- Improving documentation and code quality
- Adding support for new programming languages
- Enhancing the user interface and experience
- Adding new code analysis capabilities

---

## 🙏 Acknowledgments

- **OpenAI**: For providing the GPT-4 models and API
- **GitHub**: For the GitHub API and repository access
- **FastAPI**: For the modern, fast web framework
- **Tailwind CSS**: For the beautiful, responsive design system
- **CodeMirror**: For the professional code editor
- **Font Awesome**: For the comprehensive icon library

---

**Happy Code Reviewing! 🎉**

*Get professional code feedback instantly with AI-powered analysis.*

---

## 📊 Performance Metrics

### Code Analysis Capabilities
- **Response Time**: 5-15 seconds for typical code reviews
- **File Size Limit**: 10MB per file
- **Supported Languages**: 10+ programming languages
- **Analysis Depth**: Syntax, best practices, performance, security, readability
- **Accuracy**: High-quality feedback comparable to senior developers

### System Requirements
- **Python**: 3.8 or higher
- **RAM**: 512MB minimum, 2GB recommended
- **Storage**: 100MB for application + temporary files
- **Network**: Internet connection for OpenAI API access
- **Browser**: Modern browser with JavaScript enabled

---

**Transform your code quality with AI-powered insights! 🚀**

---

## ❓ FAQ

- Why did uploading a file show a huge token number in the error?
  - Older models return "context length exceeded" with confusing numbers if `max_tokens` is large. The app now auto-sizes requests and surfaces a clear message. If you still hit this, switch to a larger-context model like `gpt-4-turbo` or split your code.

- Which model should I use?
  - For most reviews: `gpt-4-turbo`. For very small snippets, classic `gpt-4` works. Avoid models that do not support structured JSON responses if you rely on the most detailed output.
