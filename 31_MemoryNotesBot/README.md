# 🧠 MemoryNotesBot - AI-Powered Personal Memory Assistant

<div align="center">

![MemoryNotesBot Logo](https://img.shields.io/badge/MemoryNotesBot-AI%20Assistant-blue?style=for-the-badge&logo=brain)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange?style=for-the-badge&logo=openai)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Day 31 of 100 Days of AI Agents**

*A local-first AI-powered memory assistant that mimics human memory by storing, categorizing, and recalling contextual information. Perfect for productivity, project management, and personal organization.*

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [🔧 Installation](#-installation) • [🐛 Troubleshooting](#-troubleshooting) • [📖 Usage Guide](#-usage-guide)

</div>

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [🔧 Installation](#-installation)
- [📖 Usage Guide](#-usage-guide)
- [🎯 Real-World Use Cases](#-real-world-use-cases)
- [🏗️ Architecture](#-architecture)
- [🔧 Configuration](#-configuration)
- [🐛 Troubleshooting](#-troubleshooting)
- [📱 Web Interface Guide](#-web-interface-guide)
- [🎤 Voice Commands](#-voice-commands)
- [🔍 Search Capabilities](#-search-capabilities)
- [📊 Memory Types](#-memory-types)
- [🚀 Advanced Usage](#-advanced-usage)
- [🧪 Testing](#-testing)
- [🔒 Security & Privacy](#-security--privacy)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## ✨ Features

### 🧠 Core Memory Management
- **💾 Save Notes**: Natural language input like "Remember my GitHub token is ghp_123..."
- **🔍 Recall Information**: Query like "What is my GitHub token?" or "Do I have any notes about JavaScript?"
- **🏷️ Memory Types**: Short-term, long-term, reminders, passwords, ideas, tasks, contacts, projects
- **⚡ Priority Levels**: Low, medium, high, critical
- **🤖 Smart Categorization**: Automatic tagging and categorization using AI
- **⏰ Expiration**: Set time-based expiration for temporary memories

### 🤖 AI Enhancement
- **🧠 OpenAI Integration**: Intelligent memory analysis and enhancement
- **🏷️ Auto-tagging**: AI suggests relevant tags and categories
- **⚡ Priority Assessment**: AI determines importance and urgency
- **🔍 Search Enhancement**: Improved search with AI suggestions
- **📝 Memory Summarization**: AI-generated summaries of memory collections

### 🎤 Voice Support
- **🎙️ Speech-to-Text**: Voice input for hands-free operation
- **🔊 Text-to-Speech**: Audio feedback and responses
- **🎯 Voice Commands**: Natural language voice interactions
- **🧪 Voice Testing**: Built-in voice system diagnostics

### 💻 Multiple Interfaces
- **🖥️ CLI Interface**: Rich terminal interface with Typer and Rich
- **🌐 Web Interface**: Modern, responsive web UI with Tailwind CSS
- **🔌 API Endpoints**: RESTful API for integration with other tools

### 📊 Advanced Features
- **🔍 Search & Filter**: Advanced search with tags, categories, and memory types
- **📤 Export Options**: Export memories in JSON, Markdown, or CSV formats
- **📈 Statistics**: Comprehensive memory analytics and insights
- **📜 History Tracking**: Full audit trail of memory operations
- **🧹 Auto-cleanup**: Automatic expiration of short-term memories

---

## 🚀 Quick Start

### Prerequisites
- **🐍 Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **🔑 OpenAI API key** (optional, for AI features) - [Get API Key](https://platform.openai.com/api-keys)
- **🎤 Microphone and speakers** (for voice features)

### ⚡ 5-Minute Setup

1. **📥 Clone and Install**
   ```bash
   git clone <repository-url>
   cd 31_MemoryNotesBot
   pip install -r requirements.txt
   ```

2. **⚙️ Configure Environment**
   ```bash
   copy env.example .env
   # Edit .env and add your OpenAI API key
   ```

3. **🎯 Run Demo Mode**
   ```bash
   python main.py --demo
   ```

4. **🚀 Start Using**
   ```bash
   # Web Interface (Recommended)
   python main.py --web
   
   # Command Line Interface
   python main.py --cli
   ```

5. **🌐 Open Web Interface**
   - Navigate to: `http://localhost:5000`
   - Start saving and recalling memories!

---

## 🔧 Installation

### Method 1: Quick Install (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd 31_MemoryNotesBot

# Install dependencies
pip install -r requirements.txt

# Setup environment
copy env.example .env

# Run installation test
python test_installation.py

# Start with demo data
python main.py --demo
```

### Method 2: Manual Installation

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create directories
mkdir data
mkdir data/exports

# 4. Setup environment
copy env.example .env
# Edit .env with your OpenAI API key

# 5. Test installation
python test_installation.py
```

### Method 3: Using Installation Script

```bash
# Windows
install.bat

# Linux/Mac
chmod +x install.sh
./install.sh
```

---

## 📖 Usage Guide

### 🌐 Web Interface (Recommended)

The web interface provides the most user-friendly experience:

```bash
python main.py --web
```

**Key Features:**
- **💾 Save Memory**: Type natural language and let AI enhance it
- **🔍 Recall**: Search through all your memories with AI-powered search
- **📊 Statistics**: View memory analytics and insights
- **📤 Export**: Download memories in various formats
- **🎤 Voice Test**: Test voice input/output capabilities

### 💻 Command Line Interface

For power users and automation:

```bash
python main.py --cli
```

**Quick Commands:**
```bash
# Save a memory
python main.py save "Remember my GitHub token is ghp_123..."

# Search memories
python main.py search "GitHub token"

# Show statistics
python main.py stats
```

### 🎤 Voice Interface

For hands-free operation:

```bash
python main.py --cli
# Then select option 8 for Voice Interface
```

**Voice Commands:**
- "Remember [content]" - Save new memory
- "What is [query]?" - Search for information
- "Show me recent" - Display recent memories
- "Help" - Show available commands

---

## 🎯 Real-World Use Cases

| Problem | Solution | Example |
|---------|----------|---------|
| **🔑 Forgetful about passwords** | Save credentials securely | "Remember my GitHub token is ghp_123..." |
| **📅 Miss important deadlines** | Set reminders with AI categorization | "Project deadline for website redesign is March 15th" |
| **💡 Lose great ideas** | Capture ideas with auto-tagging | "Great idea: Create a mobile app for tracking daily habits" |
| **📞 Forget contact info** | Store contacts with smart categorization | "Bank support number: 1-800-123-4567, available 24/7" |
| **🧠 Mental clutter** | Offload thoughts to searchable storage | "Remember to buy groceries: milk, bread, eggs" |
| **📚 Learning notes** | Organize study materials | "Python virtual environment activation: source venv/bin/activate" |

### 🎯 Productivity Tips

1. **🏷️ Use Consistent Tags**: Create a tagging system (work, personal, project, etc.)
2. **⚡ Set Priorities**: Use critical priority for important information
3. **⏰ Use Expiration**: Set expiry for temporary notes
4. **🔍 Regular Searches**: Search your memories regularly to rediscover information
5. **📊 Review Statistics**: Check memory analytics to understand your patterns

---

## 🏗️ Architecture

```
MemoryNotesBot/
├── 🧠 models.py          # Data models and validation
├── 💾 memory_store.py    # Core storage and management
├── 🤖 ai_service.py      # OpenAI integration and AI features
├── 🎤 voice_service.py   # Speech recognition and synthesis
├── 💻 cli.py            # Command-line interface
├── 🌐 web_app.py        # Flask web application
├── 🚀 main.py           # Main entry point
├── ⚙️ config.py         # Configuration management
├── 📁 data/             # Memory storage
│   ├── memories.json    # Memory data
│   ├── history.json     # Operation history
│   └── exports/         # Export files
└── 📁 static/           # Web assets
    └── app.js          # Frontend JavaScript
```

### 🔧 Key Components

- **MemoryStore**: JSON-based storage with automatic cleanup
- **AIService**: OpenAI integration for intelligent enhancement
- **VoiceService**: Speech recognition and text-to-speech
- **CLI Interface**: Rich terminal interface with Typer
- **Web Interface**: Modern web UI with Alpine.js and Tailwind

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# Application Configuration
DEBUG=False
HOST=127.0.0.1
PORT=5000

# Voice Configuration
ENABLE_VOICE=True
VOICE_TIMEOUT=5

# Memory Configuration
MAX_MEMORIES=10000
SHORT_TERM_EXPIRY_HOURS=24

# Data Directory (optional, defaults to ./data)
# DATA_DIR=./data
```

### Configuration Options

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key for AI features | - | Yes (for AI) |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4o-mini` | No |
| `HOST` | Web server host | `127.0.0.1` | No |
| `PORT` | Web server port | `5000` | No |
| `ENABLE_VOICE` | Enable voice features | `True` | No |
| `MAX_MEMORIES` | Maximum memories to store | `10000` | No |

### Data Storage

- **💾 Memories**: `./data/memories.json`
- **📜 History**: `./data/history.json`
- **📤 Exports**: `./data/exports/`
- **📝 Logs**: `memory_bot.log`

---

## 🐛 Troubleshooting

### ❌ Common Issues & Solutions

#### 1. **Installation Problems**

**Problem**: `ModuleNotFoundError: No module named 'openai'`
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Problem**: `PermissionError` on Windows
```bash
# Solution: Run as Administrator or use virtual environment
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### 2. **OpenAI API Issues**

**Problem**: `AI service not available`
```bash
# Solution: Check your API key
1. Verify OPENAI_API_KEY in .env file
2. Test API key: https://platform.openai.com/api-keys
3. Ensure sufficient credits
```

**Problem**: `Rate limit exceeded`
```bash
# Solution: Wait and retry
- OpenAI has rate limits
- Wait 1-2 minutes between requests
- Consider upgrading API plan
```

#### 3. **Voice Issues**

**Problem**: `No microphone detected`
```bash
# Solution: Check audio setup
1. Verify microphone permissions
2. Test microphone in system settings
3. Install audio drivers
4. Run: python -c "import speech_recognition; print('OK')"
```

**Problem**: `TTS engine not available`
```bash
# Solution: Install TTS dependencies
pip install pyttsx3
# On Windows, also install:
pip install comtypes
```

#### 4. **Web Interface Issues**

**Problem**: `Port 5000 already in use`
```bash
# Solution: Use different port
python main.py --web --port 8080
```

**Problem**: `Web interface not loading`
```bash
# Solution: Check dependencies
pip install flask flask-cors
python test_installation.py
```

#### 5. **Memory Storage Issues**

**Problem**: `Memory validation error`
```bash
# Solution: Check data format
1. Backup data/memories.json
2. Delete corrupted file
3. Restart application
```

**Problem**: `Storage full`
```bash
# Solution: Clean up old memories
1. Use cleanup feature in web interface
2. Delete old exports in data/exports/
3. Increase MAX_MEMORIES in config
```

### 🔧 Advanced Troubleshooting

#### Debug Mode
```bash
# Enable debug logging
export DEBUG=True
python main.py --web
```

#### Check System Requirements
```bash
# Test Python version
python --version  # Should be 3.8+

# Test dependencies
python test_installation.py
```

#### Reset Application
```bash
# Backup and reset
cp data/memories.json data/memories.json.backup
rm data/memories.json data/history.json
python main.py --demo
```

### 📞 Getting Help

1. **🔍 Check Logs**: Look at `memory_bot.log` for detailed errors
2. **🧪 Run Tests**: Execute `python test_installation.py`
3. **📖 Read Docs**: Check this README and inline code comments
4. **🐛 Report Issues**: Create an issue with error details

---

## 📱 Web Interface Guide

### 🎯 Main Features

#### 1. **💾 Save Memory Tab**
- **Natural Language Input**: Type like you're talking to a person
- **AI Enhancement**: Click "AI Enhance" for automatic categorization
- **Manual Options**: Set memory type, priority, tags, and expiration
- **Auto-save**: Drafts are automatically saved

#### 2. **🔍 Recall Tab**
- **Smart Search**: AI-enhanced search with suggestions
- **Filters**: Filter by tags, categories, memory types
- **Results**: Ranked by relevance with detailed information
- **Quick Actions**: Edit or delete memories directly

#### 3. **🗑️ Forget Tab**
- **Safe Deletion**: Search before deleting
- **Bulk Operations**: Delete multiple memories
- **Confirmation**: Always asks for confirmation

#### 4. **📜 History Tab**
- **Recent Memories**: Latest additions
- **Frequent Access**: Most used memories
- **Tagged Memories**: Grouped by tags
- **Statistics**: Memory analytics

### 🎨 UI Features

- **🎨 Modern Design**: Clean, responsive interface
- **📱 Mobile Friendly**: Works on all devices
- **⚡ Real-time Updates**: Instant feedback
- **⌨️ Keyboard Shortcuts**: 
  - `Ctrl+S`: Save memory
  - `Ctrl+K`: Focus search
  - `Ctrl+N`: New memory
- **🔔 Notifications**: Success/error messages
- **🔄 Auto-refresh**: Automatic data updates

### 🎯 Pro Tips

1. **🏷️ Use AI Enhancement**: Let AI categorize your memories automatically
2. **🔍 Search Regularly**: Rediscover forgotten information
3. **📊 Check Statistics**: Understand your memory patterns
4. **📤 Export Regularly**: Backup important memories
5. **🎤 Test Voice**: Ensure voice features work for hands-free use

---

## 🎤 Voice Commands

### 🎯 Supported Commands

| Command | Action | Example |
|---------|--------|---------|
| **"Remember [content]"** | Save new memory | "Remember my GitHub token is abc123" |
| **"What is [query]?"** | Search for information | "What is my GitHub token?" |
| **"Show me recent"** | Display recent memories | "Show me recent" |
| **"Show me tagged with [tag]"** | Filter by tag | "Show me tagged with work" |
| **"Delete [query]"** | Remove memories | "Delete my old password" |
| **"Help"** | Show available commands | "Help" |

### 🎤 Voice Setup

1. **🎙️ Test Microphone**
   ```bash
   # In web interface, click "Voice Test"
   # Or in CLI, select Voice Interface
   ```

2. **🔊 Test Speakers**
   ```bash
   # Voice test will speak back to you
   # Ensure speakers are working
   ```

3. **⚙️ Adjust Settings**
   ```bash
   # In .env file:
   ENABLE_VOICE=True
   VOICE_TIMEOUT=5
   ```

### 🎯 Voice Tips

- **🎤 Clear Speech**: Speak clearly and at normal pace
- **🔇 Quiet Environment**: Minimize background noise
- **⏱️ Timeout**: Commands have 5-second timeout
- **🔄 Retry**: If not understood, try rephrasing
- **🎯 Short Commands**: Keep commands concise

---

## 🔍 Search Capabilities

### 🔍 Search Methods

#### 1. **Semantic Search**
- **AI-Enhanced**: Understands context and meaning
- **Related Terms**: Suggests related search terms
- **Fuzzy Matching**: Finds memories even with typos

#### 2. **Filtered Search**
- **Tag Filtering**: Filter by specific tags
- **Category Filtering**: Filter by memory category
- **Type Filtering**: Filter by memory type
- **Priority Filtering**: Filter by importance level

#### 3. **Advanced Search**
- **Relevance Scoring**: Results ranked by relevance
- **Context Awareness**: Understands search intent
- **Search History**: Remembers previous searches

### 🔍 Search Examples

```bash
# Basic search
"GitHub token"

# Tag-based search
"work project deadline"

# Category search
"personal contact information"

# Type search
"password credentials"
```

### 🎯 Search Tips

1. **🔍 Use Keywords**: Focus on important words
2. **🏷️ Use Tags**: Search by specific tags
3. **📅 Consider Time**: Recent memories rank higher
4. **⚡ Use AI Enhancement**: Let AI improve your search
5. **🔄 Refine Results**: Use filters to narrow down

---

## 📊 Memory Types

| Type | Description | Use Case | Example |
|------|-------------|----------|---------|
| **📝 Short-term** | Temporary, expires soon | Daily reminders, temporary notes | "Remember to buy milk today" |
| **🧠 Long-term** | Permanent storage | Important information, passwords | "My GitHub token is abc123" |
| **⏰ Reminder** | Time-sensitive actions | Appointments, deadlines | "Dentist appointment Friday 3 PM" |
| **🔑 Password** | Credentials and secrets | API keys, passwords | "WiFi password: mynetwork123" |
| **💡 Idea** | Creative thoughts | Brainstorming, concepts | "App idea: habit tracker" |
| **✅ Task** | Actionable items | To-dos, project tasks | "Call Sarah about project" |
| **👥 Contact** | People and organizations | Phone numbers, addresses | "Bank support: 1-800-123-4567" |
| **📋 Project** | Work-related information | Project details, notes | "Website redesign deadline March 15" |

### 🎯 Memory Type Tips

1. **🔑 Passwords**: Use password type for sensitive data
2. **⏰ Reminders**: Set expiration for time-sensitive items
3. **💡 Ideas**: Use idea type for creative thoughts
4. **📋 Projects**: Group related information with project type
5. **👥 Contacts**: Use contact type for people and organizations

---

## 🚀 Advanced Usage

### 🔌 API Integration

```python
import requests

# Save a memory
response = requests.post('http://localhost:5000/api/memories', json={
    'content': 'Remember to buy groceries',
    'tags': ['shopping', 'personal'],
    'category': 'personal'
})

# Search memories
response = requests.post('http://localhost:5000/api/memories/search', json={
    'query': 'groceries'
})

# Get statistics
response = requests.get('http://localhost:5000/api/statistics')
```

### 🔧 Custom Memory Types

```python
from models import MemoryType

# Create custom memory type
class CustomMemoryType(MemoryType):
    CUSTOM = "custom"

# Use in memory creation
memory = memory_store.add_memory(
    content="Custom content",
    memory_type="custom"
)
```

### 📊 Data Export

```bash
# Export all memories
curl -X POST http://localhost:5000/api/export \
  -H "Content-Type: application/json" \
  -d '{"format": "json"}'

# Export filtered memories
curl -X POST http://localhost:5000/api/export \
  -H "Content-Type: application/json" \
  -d '{"format": "markdown", "tags": ["work"]}'
```

### 🔄 Automation

```bash
# Save memory from command line
python main.py save "Daily standup at 9 AM"

# Search and export
python main.py search "standup" | python main.py export --format json

# Backup script
#!/bin/bash
python main.py export --format json > backup_$(date +%Y%m%d).json
```

---

## 🧪 Testing

### 🧪 Voice Testing

```bash
# Test voice input/output
python main.py --web
# Click "Voice Test" button in web interface
```

### 🧪 Demo Mode

```bash
# Run with sample data
python main.py --demo
```

### 🧪 Installation Test

```bash
# Comprehensive system test
python test_installation.py
```

### 🧪 API Testing

```bash
# Test API endpoints
curl http://localhost:5000/api/health
curl http://localhost:5000/api/statistics
```

### 🧪 Performance Testing

```bash
# Test with large dataset
python -c "
from memory_store import MemoryStore
store = MemoryStore()
for i in range(1000):
    store.add_memory(f'Test memory {i}', tags=['test'])
print('Performance test completed')
"
```

---

## 🔒 Security & Privacy

### 🔐 Security Features

- **🔒 Local Storage**: All data stored locally on your machine
- **☁️ No Cloud Sync**: Your memories never leave your device
- **🔑 Optional AI**: OpenAI integration is completely optional
- **📤 Data Export**: Full control over your data
- **🗑️ Secure Deletion**: Memories are permanently deleted

### 🔒 Privacy Best Practices

1. **🔑 Secure API Keys**: Keep OpenAI API key private
2. **📁 Secure Storage**: Protect your data directory
3. **🔄 Regular Backups**: Export important memories regularly
4. **🗑️ Clean Deletion**: Use forget feature for sensitive data
5. **🔒 Environment Variables**: Use .env for sensitive configuration

### 🔒 Data Protection

```bash
# Secure your data directory
chmod 700 data/
chmod 600 data/*.json

# Backup important memories
python main.py export --format json > secure_backup.json
```

---

## 🤝 Contributing

### 🚀 How to Contribute

1. **🔱 Fork the repository**
2. **🌿 Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **💻 Make your changes**
4. **🧪 Add tests if applicable**
5. **📝 Update documentation**
6. **🔀 Submit a pull request**

### 🎯 Contribution Areas

- **🐛 Bug Fixes**: Report and fix bugs
- **✨ New Features**: Add new functionality
- **📖 Documentation**: Improve README and docs
- **🎨 UI/UX**: Enhance web interface
- **🧪 Testing**: Add tests and improve coverage
- **🔧 Performance**: Optimize code and performance

### 📋 Development Setup

```bash
# Clone repository
git clone <repository-url>
cd 31_MemoryNotesBot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
python test_installation.py
pytest tests/

# Format code
black .
flake8 .
```

### 📝 Code Style

- **🐍 Python**: Follow PEP 8 guidelines
- **🎨 JavaScript**: Use ESLint and Prettier
- **📖 Documentation**: Use clear, concise comments
- **🧪 Testing**: Write tests for new features
- **📝 Commits**: Use conventional commit messages

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 📜 License Summary

- **✅ Commercial Use**: Allowed
- **✅ Modification**: Allowed
- **✅ Distribution**: Allowed
- **✅ Private Use**: Allowed
- **❌ Liability**: Limited
- **❌ Warranty**: None

---

## 🙏 Acknowledgments

- **🤖 OpenAI** for AI capabilities and GPT models
- **🐍 Typer** for CLI framework and user experience
- **🎨 Rich** for beautiful terminal output
- **🎨 Tailwind CSS** for modern web design
- **⚡ Alpine.js** for reactive web components
- **🎤 SpeechRecognition** for voice input capabilities
- **🔊 pyttsx3** for text-to-speech functionality

### 📚 Resources

- **📖 OpenAI Documentation**: [https://platform.openai.com/docs](https://platform.openai.com/docs)
- **🐍 Python Documentation**: [https://docs.python.org](https://docs.python.org)
- **🎨 Tailwind CSS**: [https://tailwindcss.com](https://tailwindcss.com)
- **⚡ Alpine.js**: [https://alpinejs.dev](https://alpinejs.dev)

---

## 📞 Support

### 🆘 Getting Help

- **🐛 Issues**: Create an issue on GitHub
- **📖 Documentation**: Check this README and inline code comments
- **💬 Community**: Join our discussions
- **📧 Email**: Contact maintainers directly

### 📋 Support Checklist

Before asking for help, please check:

- [ ] **📖 Read the README** thoroughly
- [ ] **🧪 Run installation test** (`python test_installation.py`)
- [ ] **🔍 Check troubleshooting section**
- [ ] **📝 Search existing issues**
- [ ] **📋 Provide error details** and system information

### 🎯 Quick Help Commands

```bash
# Check system status
python test_installation.py

# View logs
tail -f memory_bot.log

# Reset application
python main.py --demo

# Get help
python main.py --help
```

---

<div align="center">

**Built with ❤️ for the 100 Days of AI Agents challenge**

*Transform your digital memory with AI-powered organization and recall!*

[⬆️ Back to Top](#-memorynotesbot---ai-powered-personal-memory-assistant)

</div>
