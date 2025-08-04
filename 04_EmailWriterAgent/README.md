# 🤖 EmailWriterAgent - Day 4 of #100DaysOfAI-Agents

<div align="center">

![EmailWriterAgent](https://img.shields.io/badge/EmailWriterAgent-AI%20Powered-blue?style=for-the-badge&logo=openai)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20Framework-red?style=for-the-badge&logo=fastapi)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT%20API-purple?style=for-the-badge&logo=openai)

**Transform your ideas into professional emails with AI-powered assistance**

[Features](#-features) • [Quick Start](#-quick-start) • [Usage](#-usage) • [Templates](#-templates) • [API](#-api) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [📧 Usage](#-usage)
- [🎨 Templates](#-templates)
- [🛠️ Configuration](#-configuration)
- [🔧 API Reference](#-api-reference)
- [📁 Project Structure](#-project-structure)
- [🎯 Use Cases](#-use-cases)
- [🔒 Security & Privacy](#-security--privacy)
- [🐛 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🌟 Overview

EmailWriterAgent is an intelligent email composition tool that leverages OpenAI's GPT technology to help you write professional, contextually appropriate emails from simple natural language prompts. Whether you need a formal business email, a casual follow-up, or an urgent communication, this tool adapts to your needs with smart personalization and multiple templates.

### Key Benefits

- **⚡ Speed**: Generate professional emails in seconds, not minutes
- **🎯 Accuracy**: Context-aware content that matches your specific situation
- **🎨 Flexibility**: Multiple templates and tone options for every scenario
- **💡 Intelligence**: Smart extraction of dates, names, and context from your prompts
- **🔄 Iteration**: Easy editing and regeneration for perfect results

---

## ✨ Features

### 🤖 AI-Powered Generation
- **Natural Language Processing**: Describe your email in plain English
- **Context Awareness**: Automatically extracts dates, times, locations, and names
- **Smart Personalization**: Uses recipient names naturally throughout the email
- **Professional Polish**: Generates compelling subject lines and appropriate closings

### 📧 Email Templates
- **6 Built-in Templates**: Formal, Casual, Follow-up, Thank You, Meeting Request, Urgent
- **Customizable Tone**: Override template defaults with specific tone preferences
- **Dynamic Content**: Templates adapt to your specific situation and context

### 🖥️ Multiple Interfaces
- **Web Interface**: Beautiful, responsive UI with real-time preview and inline editing
- **Terminal Interface**: Command-line tool for quick email generation
- **Quick Mode**: Generate emails directly from command line arguments

### 🛠️ Advanced Features
- **Inline Editing**: Edit generated emails directly in the preview area
- **Email History**: Track and reuse previous email prompts
- **Export Options**: Copy to clipboard or download as text files
- **Template Management**: Visual template selection and customization
- **Real-time Preview**: See your email as it's being generated

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (3.9+ recommended)
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))
- **Internet Connection** (for API calls)

### Installation

1. **Navigate to the project directory:**
   ```bash
   cd 04_EmailWriterAgent
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key:**

   **Option A: Environment Variable (Recommended)**
   ```bash
   # Windows (Command Prompt)
   set OPENAI_API_KEY=your_api_key_here
   
   # Windows (PowerShell)
   $env:OPENAI_API_KEY="your_api_key_here"
   
   # Linux/Mac
   export OPENAI_API_KEY=your_api_key_here
   ```

   **Option B: .env file**
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

   **Option C: Direct in code (Not recommended for production)**
   ```python
   # In config.py
   OPENAI_API_KEY = "your_api_key_here"
   ```

### First Run

#### Web Interface (Recommended)
```bash
python main.py --web
```
Then open your browser to `http://127.0.0.1:8004`

#### Terminal Interface
```bash
python main.py --terminal
```

#### Quick Email Generation
```bash
python main.py --quick "meeting tomorrow at 2pm"
```

---

## 📧 Usage

### Web Interface

1. **Start the web server:**
   ```bash
   python main.py --web
   ```

2. **Open your browser** to `http://127.0.0.1:8004`

3. **Compose your email:**
   - Enter your prompt (e.g., "meeting tomorrow at 2pm")
   - Select a template from the sidebar
   - Optionally customize tone, recipient, sender, and signature
   - Click "Generate Email"

4. **Review and edit:**
   - Preview the generated email
   - Click "Edit Email" to make inline changes
   - Use "Copy Email" or "Download" to save your work
   - Click "Regenerate" for variations

### Terminal Interface

```bash
# Start terminal mode
python main.py --terminal

# Available commands:
📧 EmailWriterAgent> write meeting tomorrow at 2pm
📧 EmailWriterAgent> templates
📧 EmailWriterAgent> history
📧 EmailWriterAgent> help
📧 EmailWriterAgent> quit
```

### Quick Commands

```bash
# Generate a formal email
python main.py --quick "thank you for the interview"

# Generate a follow-up email
python main.py --quick "follow up on project proposal"

# Generate a meeting request
python main.py --quick "schedule a call next week"

# Generate an urgent email
python main.py --quick "urgent: server down, need immediate assistance"
```

### Advanced Usage

```bash
# Custom port
python main.py --web --port 8005

# Custom host
python main.py --web --host 0.0.0.0

# Quick email with specific template
python main.py --quick "meeting request" --template formal
```

---

## 🎨 Templates

| Template | Description | Tone | Best For |
|----------|-------------|------|----------|
| **Formal Business** | Professional business communication | Formal | Client communications, official announcements |
| **Casual Professional** | Friendly but professional tone | Casual | Team updates, internal communications |
| **Follow-up** | Follow-up after meeting or conversation | Professional | Post-meeting summaries, action item reminders |
| **Thank You** | Express gratitude professionally | Appreciative | Interview follow-ups, gift acknowledgments |
| **Meeting Request** | Request for a meeting or call | Professional | Scheduling calls, booking appointments |
| **Urgent** | Time-sensitive communication | Urgent | Critical issues, emergency notifications |

### Template Examples

#### Formal Business
```
Subject: Follow-up on Q4 Project Proposal Discussion

Dear John,

I hope this email finds you well. I wanted to follow up on our discussion regarding the Q4 project proposal we reviewed during our meeting on Monday, October 15th.

As we discussed, the implementation timeline and resource allocation need to be finalized by the end of this week to ensure we meet our Q4 objectives. I've prepared the detailed breakdown you requested and would appreciate your feedback.

I look forward to hearing from you and continuing our discussion.

Best regards,
Sarah Johnson
Senior Project Manager
```

#### Casual Professional
```
Subject: Quick update on the new feature rollout

Hi team,

Just wanted to give you a heads up that we're planning to roll out the new dashboard feature next Tuesday. The testing phase has been going really well, and we're confident it will improve user experience significantly.

Let me know if you have any questions or concerns before we go live!

Best,
Mike
```

---

## 🛠️ Configuration

### Customizing Defaults

Edit `config.py` to customize:

```python
class EmailConfig:
    # Default email settings
    DEFAULT_FROM = "your.email@example.com"
    DEFAULT_SIGNATURE = "Your Name\nYour Title\nYour Company"
    
    # GPT settings
    MAX_TOKENS = 1000
    TEMPERATURE = 0.7
```

### Adding New Templates

Add new templates to the `TEMPLATES` dictionary in `config.py`:

```python
TEMPLATES = {
    # ... existing templates ...
    "custom_template": {
        "name": "Custom Template",
        "description": "Your custom template description",
        "tone": "professional",
        "greeting": "Dear {recipient},",
        "closing": "Best regards,\n{signature}"
    }
}
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `EMAILWRITER_PORT` | Web server port | 8004 |
| `EMAILWRITER_HOST` | Web server host | 127.0.0.1 |

---

## 🔧 API Reference

### Web API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main web interface |
| `/api/generate-email` | POST | Generate email |
| `/api/templates` | GET | Get available templates |
| `/api/history` | GET | Get email history |
| `/api/health` | GET | Health check |

### Request Format

```json
{
    "prompt": "meeting tomorrow at 2pm",
    "template": "formal",
    "recipient": "john@example.com",
    "sender": "your.email@example.com",
    "signature": "Your Name\nYour Title",
    "tone": "professional"
}
```

### Response Format

```json
{
    "success": true,
    "email": {
        "subject": "Meeting Tomorrow at 2:00 PM",
        "to": "john@example.com",
        "from": "your.email@example.com",
        "body": "Dear John,\n\nI hope this email finds you well..."
    }
}
```

### Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--web` | Start web interface | False |
| `--terminal` | Start terminal interface | False |
| `--quick` | Generate quick email | None |
| `--host` | Web server host | 127.0.0.1 |
| `--port` | Web server port | 8004 |

---

## 📁 Project Structure

```
04_EmailWriterAgent/
├── 📄 main.py                 # Main entry point and CLI
├── 🤖 email_agent.py          # Core EmailAgent class
├── 🌐 web_app.py              # FastAPI web application
├── ⚙️ config.py               # Configuration and templates
├── 📋 requirements.txt        # Python dependencies
├── 📖 README.md              # This documentation
├── 🧪 test_*.py              # Test scripts
├── 📁 templates/             # HTML templates
│   └── 📄 index.html        # Main web interface
└── 📁 static/               # Static files
    ├── 🎨 css/
    │   └── style.css        # CSS styles
    └── ⚡ js/
        └── app.js           # JavaScript functionality
```

### Key Files

- **`main.py`**: Entry point with CLI argument parsing
- **`email_agent.py`**: Core AI email generation logic
- **`web_app.py`**: FastAPI web server implementation
- **`config.py`**: Configuration, templates, and API key management
- **`templates/index.html`**: Main web interface template
- **`static/css/style.css`**: Modern, responsive styling
- **`static/js/app.js`**: Interactive web functionality

---

## 🎯 Use Cases

### 💼 Business Communication

| Scenario | Template | Example Prompt |
|----------|----------|----------------|
| **Meeting Requests** | Meeting Request | "schedule a call with the marketing team next week" |
| **Project Updates** | Formal Business | "update on Q4 project status and timeline" |
| **Client Communications** | Formal Business | "proposal for new website redesign project" |
| **Team Announcements** | Casual Professional | "announcement about new office policy starting Monday" |

### 🤝 Professional Networking

| Scenario | Template | Example Prompt |
|----------|----------|----------------|
| **Interview Follow-ups** | Thank You | "thank you for the interview last week" |
| **Networking Outreach** | Casual Professional | "connect with industry professional met at conference" |
| **Professional Introductions** | Formal Business | "introduction to potential business partner" |
| **Reference Requests** | Formal Business | "request for professional reference for job application" |

### 📧 Personal Communication

| Scenario | Template | Example Prompt |
|----------|----------|----------------|
| **Formal Invitations** | Formal Business | "invitation to company holiday party" |
| **Apology Letters** | Formal Business | "apology for missing the meeting yesterday" |
| **Congratulatory Messages** | Thank You | "congratulations on the promotion" |
| **Request Letters** | Formal Business | "request for time off next month" |

---

## 🔒 Security & Privacy

### Data Protection

- **🔐 API Key Security**: API keys are stored securely using environment variables
- **📝 No Permanent Storage**: Email content is not stored permanently
- **🔒 Encrypted Communication**: All communication with OpenAI is encrypted
- **👤 Privacy First**: No personal data is logged or stored

### Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** for sensitive data
3. **Regularly rotate** your OpenAI API keys
4. **Monitor API usage** to control costs
5. **Review generated content** before sending

### API Usage

- **Cost Control**: Each email generation uses approximately 100-200 tokens
- **Rate Limits**: Respect OpenAI's rate limits
- **Error Handling**: Graceful handling of API failures
- **Fallback Options**: Terminal mode available if web interface fails

---

## 🐛 Troubleshooting

### Common Issues

#### ❌ "OpenAI API key not found"
**Solution:**
```bash
# Check if API key is set
echo $OPENAI_API_KEY

# Set API key (Linux/Mac)
export OPENAI_API_KEY=your_api_key_here

# Set API key (Windows)
set OPENAI_API_KEY=your_api_key_here
```

#### ❌ "Failed to generate email"
**Solutions:**
1. Check your internet connection
2. Verify your OpenAI API key is valid
3. Ensure you have sufficient API credits
4. Try the terminal interface for debugging

#### ❌ "Web interface not loading"
**Solutions:**
```bash
# Check if port is available
netstat -an | grep 8004

# Try different port
python main.py --web --port 8005

# Check dependencies
pip install -r requirements.txt
```

#### ❌ "Module not found errors"
**Solution:**
```bash
# Install dependencies
pip install -r requirements.txt

# Or install individually
pip install openai fastapi uvicorn jinja2 colorama pydantic
```

### Debug Mode

```bash
# Run with verbose output
python main.py --web --debug

# Check API health
curl http://127.0.0.1:8004/api/health
```

### Getting Help

1. **Check the terminal output** for detailed error messages
2. **Verify your OpenAI API key** is working with a simple test
3. **Try the terminal interface** for debugging
4. **Check the `/api/health` endpoint** for service status
5. **Review the logs** for specific error details

---

## 🤝 Contributing

This project is part of the **#100DaysOfAI-Agents** challenge. We welcome contributions!

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Areas for Contribution

- **🐛 Bug Fixes**: Report and fix bugs
- **✨ New Features**: Add new email templates or features
- **📚 Documentation**: Improve README, add examples
- **🎨 UI/UX**: Enhance the web interface
- **🧪 Testing**: Add more test coverage
- **🔧 Configuration**: Improve configuration options

### Development Setup

```bash
# Clone the repository
git clone <repository-url>
cd 04_EmailWriterAgent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
python test_installation.py
python test_improvements.py
python test_inline_editing.py
```

### Code Style

- Follow **PEP 8** Python style guidelines
- Use **type hints** for function parameters
- Add **docstrings** for all functions
- Write **comprehensive tests**
- Keep **commit messages** clear and descriptive

---

## 📄 License

This project is part of the **#100DaysOfAI-Agents** challenge by [Muhammad Sami Asghar Mughal](https://github.com/your-username).

### License Terms

- **Open Source**: This project is open source and available under the MIT License
- **Educational Use**: Free to use for educational and personal purposes
- **Commercial Use**: Contact the author for commercial licensing
- **Attribution**: Please credit the original author when using this code

---

## 🙏 Acknowledgments

### Open Source Libraries
- **[OpenAI](https://openai.com/)** - GPT API for intelligent email generation
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern web framework for the API
- **[Uvicorn](https://www.uvicorn.org/)** - Lightning-fast ASGI server
- **[Jinja2](https://jinja.palletsprojects.com/)** - Template engine for web interface
- **[Colorama](https://pypi.org/project/colorama/)** - Cross-platform colored terminal output

### Community
- **AI Community** - For inspiration and support
- **Open Source Contributors** - For the amazing tools that make this possible
- **Beta Testers** - For valuable feedback and bug reports

### Special Thanks
- **OpenAI Team** - For making powerful AI accessible
- **FastAPI Community** - For the excellent documentation and support
- **#100DaysOfAI-Agents** - For the motivation to build amazing AI tools

---

<div align="center">

**Happy email writing! 📧✨**

[⬆️ Back to Top](#-emailwriteragent---day-4-of-100daysofai-agents)

</div> 
**Happy email writing! 📧✨** 