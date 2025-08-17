# 🔍 RepoSummarizerAgent - Day 17 of #100DaysOfAI-Agents

An intelligent AI-powered CLI agent that analyzes GitHub repositories and provides **comprehensive, detailed summaries** using OpenAI GPT. Features multi-language support (English, Hindi, Urdu), intelligent file analysis, advanced technology detection, and export capabilities.

**🎯 NEW: Enhanced Summary Quality** - Significantly improved analysis with better prompts, technology detection, and comprehensive insights!

---

## ✨ What's Included

- **🔍 Intelligent Repository Analysis**: 
  - README.md content analysis and interpretation
  - Project folder structure mapping and visualization
  - Key configuration file detection (package.json, requirements.txt, etc.)
  - **Advanced technology stack identification and categorization**
  - **Project structure analysis (tests, CI/CD, documentation, etc.)**
- **🤖 AI-Powered Summarization**: 
  - OpenAI GPT integration for intelligent analysis
  - **Comprehensive project overview with detailed insights**
  - **Key features and capabilities with practical analysis**
  - **Technology stack and framework detection with explanations**
  - **Setup and installation guidance with step-by-step instructions**
  - **Code structure explanation with architectural insights**
  - **Actionable improvement suggestions and best practices**
- **🌍 Multi-Language Support**: 
  - **English** (default) - Professional technical summaries with enhanced detail
  - **Hindi** (हिंदी) - हिंदी में विस्तृत तकनीकी विश्लेषण
  - **Urdu** (اردو) - اردو میں تفصیلی تکنیکی تجزیہ
- **💾 Output Options**: 
  - Clean, formatted CLI display with progress indicators
  - File export capability (.txt format)
  - **Structured summary format with comprehensive sections**
- **⚡ Performance Features**: 
  - Progress indicators and spinners
  - Comprehensive error handling
  - GitHub API rate limit management
  - File size optimization and limits
  - Recursive directory traversal
  - **Enhanced token management (6000 tokens)**
  - **Optimized temperature settings for better quality**

---

## 🛠️ Tech Stack

- **Backend**: Python 3.8+ with CLI interface
- **AI Engine**: OpenAI GPT-4 for intelligent repository analysis
- **GitHub Integration**: GitHub REST API for repository access
- **Language Processing**: Multi-language support with localized prompts
- **Configuration**: `python-dotenv` for environment variables
- **HTTP Client**: `requests` library for API communication
- **CLI Framework**: Native `argparse` with custom formatting

---

## 🚀 Quick Start

### 1. Clone and Navigate
```bash
cd 17_RepoSummarizerAgent
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
GITHUB_TOKEN=your_github_token_here  # Optional, for higher rate limits
OPENAI_MODEL=gpt-4  # or gpt-4-turbo, gpt-3.5-turbo
MAX_TOKENS=6000  # Increased for better summaries
TEMPERATURE=0.2  # Optimized for focused output
MAX_FILE_SIZE=1048576
MAX_FILES_TO_ANALYZE=50
```

**Getting Your OpenAI API Key:**
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Generate a new API key
4. Copy and paste it into your `.env` file

**Getting Your GitHub Token (Optional):**
1. Go to [GitHub Settings > Tokens](https://github.com/settings/tokens)
2. Generate a new token with `public_repo` scope
3. Copy and paste it into your `.env` file

### 4. Test Installation
```bash
python test_installation.py
```

### 5. Test Improved Summaries
```bash
python test_improved_summary.py
```

### 6. Start Analyzing!
```bash
# Basic analysis
python main.py --url https://github.com/user/repository

# Analysis in Hindi
python main.py --url https://github.com/user/repository --lang hi

# Analysis in Urdu with file export
python main.py --url https://github.com/user/repository --lang ur --save
```

---

## 📖 Usage Examples

### Basic Repository Analysis
```bash
python main.py --url https://github.com/tiangolo/fastapi
```

### Multi-Language Support
```bash
# English (default)
python main.py --url https://github.com/facebook/react

# Hindi
python main.py --url https://github.com/facebook/react --lang hi

# Urdu
python main.py --url https://github.com/facebook/react --lang ur
```

### Save Output to File
```bash
# Save English summary
python main.py --url https://github.com/django/django --save

# Save Hindi summary
python main.py --url https://github.com/django/django --lang hi --save
```

### Get Help
```bash
python main.py --help
```

---

## 🎯 What It Analyzes

### Repository Information
- **Basic Details**: Name, description, language, stars, forks
- **Timeline**: Creation date, last update
- **Statistics**: File count, size, contributors

### File Structure Analysis
- **Directory Mapping**: Complete folder hierarchy
- **File Prioritization**: README files, configuration files, source code
- **Smart Filtering**: Focus on relevant files for analysis

### Content Analysis
- **README.md**: Project description, features, setup instructions
- **Configuration Files**: Dependencies, build tools, frameworks
- **Source Code**: Language detection, project structure
- **Documentation**: Additional markdown files, guides

### AI-Generated Summary
1. **Project Overview**: What the project does (3-4 lines)
2. **Key Features**: Main capabilities and functionality
3. **Technologies Used**: Languages, frameworks, tools detected
4. **Setup/Installation**: How to run or install the project
5. **Code Structure**: Project organization explanation
6. **Suggestions**: Improvement tips and best practices

---

## 🌍 Language Support Details

### English (en)
- Professional technical summaries
- Standard software development terminology
- Clear, concise explanations

### Hindi (hi)
- हिंदी में तकनीकी विश्लेषण
- सॉफ्टवेयर विकास की शब्दावली
- सरल और स्पष्ट विवरण

### Urdu (ur)
- اردو میں تکنیکی تجزیہ
- سافٹ ویئر ڈویلپمنٹ کی اصطلاحات
- آسان اور واضح تفصیلات

---

## 🔧 Configuration Options

### Environment Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | Required | Your OpenAI API key |
| `GITHUB_TOKEN` | Optional | GitHub personal access token |
| `OPENAI_MODEL` | `gpt-4` | AI model to use |
| `MAX_TOKENS` | `4000` | Maximum tokens for AI response |
| `TEMPERATURE` | `0.3` | AI creativity level (0-1) |
| `MAX_FILE_SIZE` | `1048576` | Maximum file size to analyze (1MB) |
| `MAX_FILES_TO_ANALYZE` | `50` | Maximum files to process |

### Command Line Options
| Option | Short | Description |
|--------|-------|-------------|
| `--url` | `-u` | GitHub repository URL (required) |
| `--lang` | `-l` | Output language: en, hi, ur |
| `--save` | `-s` | Save summary to text file |
| `--version` | `-v` | Show version information |
| `--help` | `-h` | Show help message |

---

## 📁 Project Structure

```
17_RepoSummarizerAgent/
├── config.py              # Configuration and settings
├── github_service.py      # GitHub API integration
├── ai_summarizer.py       # OpenAI GPT integration
├── main.py                # Main CLI application
├── demo.py                # Interactive demo script
├── test_installation.py   # Installation testing
├── setup.py               # Environment setup wizard
├── requirements.txt       # Python dependencies
├── install.bat            # Windows installation script
├── start.bat              # Windows startup script
├── README.md              # This file
└── .env                   # Environment variables (create this)
```

---

## 🚨 Error Handling

### Common Issues and Solutions

**OpenAI API Key Missing**
```
❌ OpenAI API key is required. Please set OPENAI_API_KEY in your .env file.
```
**Solution**: Run `python setup.py` or manually create `.env` file

**Invalid GitHub URL**
```
❌ Invalid GitHub URL. Please provide a valid GitHub repository URL.
```
**Solution**: Ensure URL follows format: `https://github.com/owner/repository`

**Private Repository**
```
❌ Cannot analyze private repositories. Please ensure the repository is public.
```
**Solution**: Use a public repository or ensure you have proper access

**Rate Limit Exceeded**
```
❌ GitHub API rate limit exceeded. Please try again later.
```
**Solution**: Add GitHub token to `.env` file or wait for rate limit reset

**Repository Not Found**
```
❌ Repository not found. Please check the URL and ensure the repository exists.
```
**Solution**: Verify the repository URL and ensure it's accessible

---

## 🧪 Testing

### Run Installation Tests
```bash
python test_installation.py
```

### Test with Demo Repositories
```bash
python demo.py
```

### Manual Testing
```bash
# Test with a simple repository
python main.py --url https://github.com/octocat/Hello-World

# Test language support
python main.py --url https://github.com/octocat/Hello-World --lang hi

# Test file export
python main.py --url https://github.com/octocat/Hello-World --save
```

---

## 🔮 Future Enhancements

- **Web Interface**: Browser-based repository analysis
- **Batch Processing**: Analyze multiple repositories at once
- **Custom Prompts**: User-defined analysis criteria
- **Export Formats**: JSON, Markdown, PDF output
- **Integration**: GitHub Actions, CI/CD pipeline support
- **Advanced Analysis**: Code quality metrics, security scanning
- **Collaboration**: Share and compare repository analyses

---

## 🤝 Contributing

This project is part of the #100DaysOfAI-Agents challenge. Contributions are welcome!

### How to Contribute
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Development Setup
```bash
# Clone and setup
git clone <your-fork>
cd 17_RepoSummarizerAgent
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Run tests
python test_installation.py
python demo.py
```

---

## 📄 License

This project is part of the #100DaysOfAI-Agents challenge and is open source.

---

## 🙏 Acknowledgments

- **OpenAI** for providing the GPT API
- **GitHub** for the comprehensive REST API
- **Python Community** for excellent libraries and tools
- **#100DaysOfAI-Agents** community for inspiration and support

---

## 📞 Support

If you encounter any issues or have questions:

1. **Check the error handling section** above
2. **Run the test script**: `python test_installation.py`
3. **Try the demo**: `python demo.py`
4. **Review the configuration**: Ensure your `.env` file is correct

---

## 🎉 Success Stories

Share your repository analysis results with the community! Tag us with `#100DaysOfAI-Agents` and `#RepoSummarizerAgent`.

---

**Happy Repository Analysis! 🚀🔍**
