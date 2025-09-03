# 🎯 AI Quiz Maker - Day 33 of #100DaysOfAI-Agents

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange.svg)](https://openai.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Transform any content into engaging quizzes with AI-powered intelligence!** 🚀

AI Quiz Maker is a powerful application that generates multiple-choice quizzes from topics, text files, URLs, or pasted content using OpenAI's advanced language models. Perfect for educators, students, content creators, and anyone who needs to create engaging assessments quickly.

## ✨ **Features**

### 🎨 **Modern Web Interface**
- **Beautiful Tailwind CSS Design** - Responsive, modern UI with smooth animations
- **Multiple Input Methods** - Topic, URL, File Upload, and Text Input
- **Real-time Validation** - Input validation with helpful error messages
- **Interactive Elements** - Drag & drop file upload, character counters, loading states

### 🤖 **AI-Powered Quiz Generation**
- **Multiple AI Models** - Support for GPT-3.5-turbo, GPT-4, and GPT-4o-mini
- **Smart Content Processing** - Intelligent parsing of various content formats
- **Customizable Difficulty** - Easy, Medium, and Hard question levels
- **Flexible Question Count** - Generate 1-50 questions per quiz

### 📚 **Content Sources**
- **Topic-based** - Generate quizzes from subject names
- **URL Fetching** - Extract content from documentation, articles, and web pages
- **File Upload** - Support for .txt, .md, .doc, .docx files
- **Text Input** - Paste any content directly

### 📤 **Export & Sharing**
- **Multiple Formats** - Markdown, JSON, and CSV export
- **Quiz History** - Save and manage previously generated quizzes
- **Statistics Dashboard** - Track your quiz generation activity
- **Easy Sharing** - Download files or copy to clipboard

### 🖥️ **Command Line Interface**
- **Interactive Mode** - User-friendly CLI with prompts
- **Batch Processing** - Generate multiple quizzes efficiently
- **Configuration Options** - Customize settings via command line
- **Cross-platform** - Works on Windows, macOS, and Linux

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.8 or higher
- OpenAI API key
- Modern web browser

### **Installation**

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/100DaysOfAI-Agents.git
   cd 100DaysOfAI-Agents/33_AIQuizMaker
   ```

2. **Install dependencies**
   ```bash
   # Windows
   install.bat
   
   # Linux/macOS
   pip install -r requirements.txt
   ```

3. **Set up environment**
   ```bash
   # Copy environment template
   cp env.example .env
   
   # Edit .env file with your OpenAI API key
   OPENAI_API_KEY=your_api_key_here
   ```

4. **Start the application**
   ```bash
   # Web UI
   start.bat  # Windows
   python server.py  # Linux/macOS
   
   # CLI
   python main.py
   ```

5. **Open your browser**
   ```
   http://localhost:5000
   ```

## 🎯 **Usage Examples**

### **Web Interface**

#### **1. Topic-based Quiz Generation**
1. Select the **"Topic"** tab
2. Enter a subject: `"Python Programming Fundamentals"`
3. Set questions: `10`, Difficulty: `Medium`
4. Click **"Generate Quiz"**
5. Review and export your quiz!

#### **2. URL Content Quiz**
1. Select the **"URL"** tab
2. Enter a URL: `https://docs.python.org/3/tutorial/`
3. Click **"Fetch Content"**
4. Review the extracted content
5. Generate quiz from the fetched content

#### **3. File Upload Quiz**
1. Select the **"File Upload"** tab
2. Drag & drop or select a text file
3. File content automatically populates
4. Configure quiz settings
5. Generate your quiz!

### **Command Line Interface**

#### **Basic Usage**
```bash
# Generate quiz from topic
python main.py --topic "Machine Learning Basics" --questions 5 --difficulty medium

# Interactive mode
python main.py --interactive

# Generate from file
python main.py --file "notes.txt" --questions 10 --difficulty hard
```

#### **Advanced CLI Options**
```bash
# Custom model and settings
python main.py \
  --topic "Data Science" \
  --questions 15 \
  --difficulty hard \
  --model gpt-4 \
  --include-answers \
  --output json

# Batch processing
python main.py --batch-file "topics.txt" --output-dir "quizzes/"
```

## 🔧 **Configuration**

### **Environment Variables**
Create a `.env` file in the project root:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# Flask Configuration
FLASK_PORT=5000
FLASK_DEBUG=True

# Quiz Settings
DEFAULT_QUESTIONS=5
DEFAULT_DIFficulty=medium
INCLUDE_ANSWERS=True

# File Paths
UPLOADS_DIR=uploads/
OUTPUTS_DIR=outputs/
QUIZES_DIR=quizzes/
```

### **Supported AI Models**
- `gpt-3.5-turbo` - Fast, cost-effective
- `gpt-4` - High quality, more expensive
- `gpt-4o-mini` - Balanced performance (default)

### **Quiz Difficulty Levels**
- **Easy** - Basic concepts, definitions
- **Medium** - Application and understanding
- **Hard** - Analysis and synthesis

## 📁 **Project Structure**

```
33_AIQuizMaker/
├── 📁 static/                 # Frontend assets
│   ├── 📄 script.js          # JavaScript functionality
│   └── 📄 style.css          # Custom styles (if needed)
├── 📁 templates/              # HTML templates
│   └── 📄 index.html         # Main web interface
├── 📁 uploads/                # Temporary file uploads
├── 📁 outputs/                # Generated quiz exports
├── 📁 quizzes/                # Saved quiz files
├── 📄 main.py                 # CLI interface
├── 📄 server.py               # Flask web server
├── 📄 quiz_generator.py       # Core quiz generation logic
├── 📄 config.py               # Configuration management
├── 📄 requirements.txt        # Python dependencies
├── 📄 install.bat            # Windows installation script
├── 📄 start.bat              # Windows startup script
├── 📄 test_installation.py   # Installation verification
└── 📄 README.md               # This file
```

## 🛠️ **Technical Architecture**

### **Backend Components**
- **Flask Web Server** - RESTful API endpoints
- **Quiz Generator** - OpenAI API integration and content processing
- **File Handler** - Document processing and validation
- **Session Management** - User quiz history and preferences

### **Frontend Components**
- **Responsive UI** - Tailwind CSS for modern design
- **Interactive Elements** - JavaScript for dynamic functionality
- **Real-time Updates** - AJAX for seamless user experience
- **Progressive Enhancement** - Works without JavaScript

### **Data Flow**
1. **Input Processing** - Validate and prepare content
2. **AI Generation** - Send to OpenAI API with structured prompts
3. **Response Parsing** - Extract quiz questions and answers
4. **Format Conversion** - Convert to desired output format
5. **Storage & Export** - Save to history and generate files

## 📊 **API Endpoints**

### **Core Endpoints**
- `POST /api/generate` - Generate quiz from content
- `POST /api/fetch-url` - Extract content from URL
- `POST /api/upload` - Handle file uploads
- `POST /api/export` - Export quiz in various formats

### **Management Endpoints**
- `GET /api/history` - Retrieve quiz history
- `GET /api/statistics` - Get usage statistics
- `POST /api/clear-history` - Clear quiz history
- `GET /api/health` - Server health check

### **Example API Usage**
```bash
# Generate quiz
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Python is a programming language",
    "questions": 5,
    "difficulty": "medium",
    "include_answers": true
  }'

# Fetch URL content
curl -X POST http://localhost:5000/api/fetch-url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/article"}'
```

## 🎨 **Customization**

### **UI Customization**
- **Color Scheme** - Modify Tailwind CSS variables
- **Layout** - Adjust component positioning and spacing
- **Animations** - Customize transitions and effects
- **Responsiveness** - Optimize for different screen sizes

### **Quiz Generation**
- **Prompt Templates** - Customize AI instructions
- **Question Types** - Add support for different formats
- **Difficulty Scaling** - Implement custom difficulty algorithms
- **Content Processing** - Add new content source types

### **Export Formats**
- **Custom Formats** - Add new export types
- **Styling** - Customize output appearance
- **Metadata** - Include additional quiz information
- **Templates** - Use custom export templates

## 🧪 **Testing**

### **Installation Testing**
```bash
python test_installation.py
```

### **Manual Testing**
1. **Web UI Testing**
   - Test all input methods
   - Verify quiz generation
   - Check export functionality
   - Test responsive design

2. **CLI Testing**
   - Test all command options
   - Verify file processing
   - Check error handling
   - Test batch operations

### **API Testing**
```bash
# Health check
curl http://localhost:5000/api/health

# Test quiz generation
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"content": "Test content", "questions": 3}'
```

## 🚨 **Troubleshooting**

### **Common Issues**

#### **1. OpenAI API Errors**
```
Error: Invalid API key
Solution: Verify your API key in .env file
```

#### **2. File Upload Issues**
```
Error: File type not supported
Solution: Use .txt, .md, .doc, or .docx files
```

#### **3. URL Fetching Problems**
```
Error: Failed to fetch URL
Solution: Check URL accessibility and internet connection
```

#### **4. Port Already in Use**
```
Error: Port 5000 is already in use
Solution: Change FLASK_PORT in .env file
```

### **Debug Mode**
Enable debug mode for detailed error information:
```env
FLASK_DEBUG=True
```

### **Logs**
Check console output for detailed error messages and debugging information.

## 📈 **Performance Tips**

### **Optimization Strategies**
- **Content Length** - Keep content under 10,000 characters for faster processing
- **Question Count** - Generate 5-15 questions for optimal performance
- **Model Selection** - Use GPT-3.5-turbo for faster, cost-effective generation
- **Caching** - Enable browser caching for static assets

### **Resource Management**
- **File Cleanup** - Temporary files are automatically removed
- **Memory Usage** - Large files are processed in chunks
- **API Rate Limits** - Respect OpenAI's rate limiting guidelines

## 🔒 **Security Considerations**

### **Data Protection**
- **API Key Security** - Never commit API keys to version control
- **Input Validation** - All user inputs are validated and sanitized
- **File Upload Security** - File types and sizes are strictly controlled
- **Session Security** - Flask sessions use secure random keys

### **Privacy**
- **Content Processing** - Content is processed locally when possible
- **API Communication** - Secure HTTPS communication with OpenAI
- **Data Retention** - Quiz history is stored in browser sessions only

## 🤝 **Contributing**

### **Development Setup**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### **Code Style**
- Follow PEP 8 Python guidelines
- Use meaningful variable names
- Add docstrings to functions
- Include type hints where appropriate

### **Testing**
- Test all new features
- Ensure backward compatibility
- Update documentation
- Verify installation process

## 📚 **Learning Resources**

### **Technologies Used**
- **Python** - [Official Documentation](https://docs.python.org/)
- **Flask** - [Flask Documentation](https://flask.palletsprojects.com/)
- **OpenAI API** - [OpenAI Documentation](https://platform.openai.com/docs/)
- **Tailwind CSS** - [Tailwind Documentation](https://tailwindcss.com/docs)

### **Related Projects**
- **Educational Tools** - Explore similar quiz generation tools
- **AI Applications** - Learn about other AI-powered applications
- **Web Development** - Improve your Flask and frontend skills

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **OpenAI** - For providing the GPT models and API
- **Flask Community** - For the excellent web framework
- **Tailwind CSS** - For the beautiful utility-first CSS framework
- **100DaysOfAI-Agents** - For the learning challenge and community

## 📞 **Support**

### **Getting Help**
- **Issues** - Report bugs and request features on GitHub
- **Discussions** - Join community discussions
- **Documentation** - Check this README and inline code comments

### **Community**
- **GitHub Discussions** - Share ideas and get help
- **Discord Server** - Join our community chat
- **Twitter** - Follow for updates and tips

---

<div align="center">

**Made with ❤️ by the AI Quiz Maker Team**

*Transform learning with AI-powered quiz generation!* 🎯✨

[![GitHub Stars](https://img.shields.io/github/stars/yourusername/100DaysOfAI-Agents?style=social)](https://github.com/yourusername/100DaysOfAI-Agents)
[![GitHub Forks](https://img.shields.io/github/forks/yourusername/100DaysOfAI-Agents?style=social)](https://github.com/yourusername/100DaysOfAI-Agents)
[![GitHub Issues](https://img.shields.io/github/issues/yourusername/100DaysOfAI-Agents)](https://github.com/yourusername/100DaysOfAI-Agents/issues)

</div>
