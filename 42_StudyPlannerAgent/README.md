# 📚 StudyPlannerAgent - Day 42 of #100DaysOfAI-Agents

<div align="center">

![StudyPlannerAgent Banner](https://img.shields.io/badge/StudyPlannerAgent-Day%2042-blue?style=for-the-badge&logo=graduation-cap&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange?style=for-the-badge&logo=openai&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20Framework-red?style=for-the-badge&logo=fastapi&logoColor=white)

**Create intelligent, personalized study plans with AI-powered planning**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎯 Examples](#-examples) • [📚 Documentation](#-documentation) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is StudyPlannerAgent?

StudyPlannerAgent is an intelligent AI-powered study planning system that creates personalized, comprehensive study plans tailored to your goals, time constraints, and learning preferences. Whether you're a student preparing for exams, a professional learning new skills, or someone looking to organize their learning journey, this agent helps you create structured, achievable study plans that maximize your learning efficiency.

### 🌟 Key Highlights

- **🎯 4 Learning Styles**: Reading, Practice, Videos, Mixed approaches
- **📊 3 Difficulty Levels**: Beginner, Intermediate, Advanced with adaptive pacing
- **📋 3 Plan Templates**: Basic, Detailed, Intensive for different needs
- **💾 3 Export Formats**: Markdown, JSON, PDF for maximum flexibility
- **🌐 Dual Interface**: Beautiful web UI + powerful terminal interface
- **⏰ Smart Scheduling**: Intelligent time allocation and progress tracking
- **🎨 Modern Design**: Vibrant coral-teal-blue theme with glassmorphism effects

## 🎯 Features

### 🚀 Core Functionality
- ✅ **AI Study Plan Generation**: Powered by OpenAI GPT-4 for intelligent planning
- ✅ **Personalized Content**: Plans tailored to your specific goals and constraints
- ✅ **Real-time Generation**: Live plan creation with progress indicators
- ✅ **Auto-save**: Plans automatically saved in multiple formats
- ✅ **Progress Tracking**: Built-in plan management and organization
- ✅ **Smart Time Management**: Intelligent scheduling based on available time

### 🎨 Learning Styles
- ✅ **📚 Reading**: Learn through textbooks, articles, and written materials
- ✅ **💻 Practice**: Hands-on exercises, projects, and practical application
- ✅ **🎥 Videos**: Video tutorials, online courses, and lectures
- ✅ **🎯 Mixed**: Balanced combination of all learning methods
- ✅ **Adaptive Pacing**: Time allocation optimized for each learning style
- ✅ **Resource Integration**: Curated learning materials and tools

### 📊 Difficulty Management
- ✅ **🌱 Beginner**: No prior knowledge required, slow-paced learning
- ✅ **📈 Intermediate**: Some prior knowledge helpful, moderate pace
- ✅ **🚀 Advanced**: Strong foundation required, fast-paced learning
- ✅ **Smart Progression**: Systematic advancement from basics to advanced
- ✅ **Time Optimization**: Difficulty-based time allocation adjustments
- ✅ **Prerequisite Mapping**: Clear learning path dependencies

### 💻 User Interfaces
- ✅ **Modern Web UI**: Beautiful, responsive interface with vibrant theme
- ✅ **Enhanced Terminal**: Interactive CLI with colors and formatting
- ✅ **Quick Generation**: Fast command-line plan creation
- ✅ **Real-time Updates**: Live progress indicators and feedback
- ✅ **Mobile Responsive**: Works seamlessly on all devices
- ✅ **Keyboard Shortcuts**: Power user features for efficiency

### 📊 Plan Management & Analytics
- ✅ **Plan Library**: Organize and manage your study plan collection
- ✅ **Export Options**: Download as Markdown, JSON, or PDF
- ✅ **Search & Filter**: Find plans by goal, subject, or date
- ✅ **Progress Tracking**: Monitor your learning journey
- ✅ **Backup & Restore**: Automatic saving and data persistence
- ✅ **Template System**: Reusable plan structures

### 🎨 Advanced Features
- ✅ **Intelligent Scheduling**: AI-optimized daily and weekly schedules
- ✅ **Resource Recommendations**: Curated learning materials and tools
- ✅ **Assessment Strategies**: Built-in progress tracking and evaluation
- ✅ **Study Techniques**: Learning methods optimized for chosen style
- ✅ **Error Handling**: Robust error management with user-friendly messages
- ✅ **Performance Optimized**: Smooth animations and efficient rendering

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.8+** installed on your system
- **OpenAI API Key** (get one from [OpenAI Platform](https://platform.openai.com/api-keys))
- **Internet connection** for AI plan generation

### ⚡ One-Click Installation

```bash
# Windows - Run the installer
install.bat

# The installer will:
# ✅ Check Python installation
# ✅ Create virtual environment
# ✅ Install all dependencies
# ✅ Set up configuration files
# ✅ Run installation tests
```

### 🔧 Manual Installation

```bash
# 1. Clone or download the project
git clone <repository-url>
cd 42_StudyPlannerAgent

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up environment
echo OPENAI_API_KEY=your_api_key_here > .env
```

### 🎯 First Run

```bash
# Option 1: Web Interface (Recommended)
python main.py --web
# Open: http://localhost:8042

# Option 2: Terminal Interface
python main.py --terminal

# Option 3: Quick Plan Generation
python main.py --quick "Learn JavaScript"
```

### 🧪 Verify Installation

```bash
# Run the test suite
python test_installation.py

# Expected output:
# ✅ Python version compatible
# ✅ All dependencies installed
# ✅ Configuration loaded
# ✅ Plan generator initialized
# ✅ Web app ready
```

## 🎯 Examples & Usage

### 🌐 Web Interface

The web interface provides a beautiful, interactive experience for study plan generation:

1. **📝 Enter Your Goal**: Describe what you want to learn in the text field
2. **⏰ Set Time Constraints**: Choose days available and hours per day
3. **🎨 Choose Learning Style**: Select your preferred learning approach
4. **📊 Set Difficulty**: Pick the appropriate difficulty level
5. **🚀 Generate**: Click "Generate Study Plan" and watch the magic happen
6. **💾 Download**: Save your plan in multiple formats

**🎯 Pro Tips:**
- Be specific about your study goal for better results
- Set realistic time constraints for achievable plans
- Try different learning styles to find what works best
- Use the detailed template for comprehensive planning

### 💻 Terminal Interface

The enhanced terminal interface offers powerful command-line functionality:

```bash
# Start the enhanced terminal
python main.py --terminal

# 🎯 Available Commands:
generate              # Interactive study plan generation
list                  # List all your saved plans with details
load <plan_id>        # Load a specific study plan
config                # View current settings and options
help                  # Show detailed help
quit                  # Exit the application

# 💡 Pro Tips:
# - Follow the interactive prompts for guided plan creation
# - Use 'g', 'l', 'c' as shortcuts for commands
# - Plans are automatically saved for easy access
```

### ⚡ Quick Generation

Generate study plans instantly from the command line:

```bash
# 🚀 Basic study plan generation
python main.py --quick "Learn JavaScript"

# 🎯 With specific options
python main.py --quick "Master Python Programming" \
  --days 60 \
  --hours 3 \
  --style practice \
  --difficulty intermediate \
  --subject "Programming" \
  --template detailed

# 📚 Academic subjects
python main.py --quick "Prepare for IELTS" --style mixed --difficulty intermediate
python main.py --quick "Learn Machine Learning" --days 90 --hours 2
python main.py --quick "AWS Certification" --template intensive
```

### 📚 Study Plan Examples

Here are some example goals to get you started:

| Subject | Goal | Expected Output |
|---------|------|----------------|
| **Programming** | "Learn JavaScript from scratch" | 30-day plan with daily coding exercises |
| **Languages** | "Prepare for IELTS exam" | Comprehensive 60-day preparation schedule |
| **Academic** | "Master Calculus for engineering" | Structured math learning with practice problems |
| **Certifications** | "AWS Solutions Architect certification" | Intensive 45-day exam preparation plan |
| **Skills** | "Learn data analysis with Python" | Project-based learning with real datasets |
| **Professional** | "Master project management" | Business skills development with practical applications |

### 🎨 Study Planning Tips

**📝 Writing Better Goals:**
- **Be Specific**: "Learn Python" vs "Master Python for data science"
- **Add Context**: "Prepare for exam" vs "Prepare for AWS certification exam"
- **Include Timeline**: "Learn JavaScript in 3 months"
- **Set Clear Objectives**: "Build 5 projects using React"

**🎭 Learning Style Selection:**
- **Reading**: Perfect for theory-heavy subjects like mathematics, philosophy
- **Practice**: Great for programming, hands-on skills, practical applications
- **Videos**: Ideal for visual learners, software tutorials, demonstrations
- **Mixed**: Best for comprehensive learning, complex subjects

**📊 Difficulty Level Guidelines:**
- **Beginner**: No prior knowledge, starting from absolute basics
- **Intermediate**: Some familiarity, building on existing knowledge
- **Advanced**: Strong foundation, focusing on mastery and specialization

## 🎭 Learning Options

### 📚 Available Learning Styles

| Style | Description | Time Ratio | Best For | Example Methods |
|-------|-------------|------------|----------|-----------------|
| **📚 Reading** | Textbooks, articles, documentation | 40% | Visual learners, theory-heavy subjects | Textbooks, research papers, documentation |
| **💻 Practice** | Hands-on exercises and projects | 50% | Kinesthetic learners, practical skills | Coding exercises, lab work, projects |
| **🎥 Videos** | Video tutorials and lectures | 30% | Auditory learners, visual demonstrations | Online courses, YouTube tutorials, webinars |
| **🎯 Mixed** | Combination of all methods | 40% | Most learners, comprehensive learning | Balanced approach with multiple resources |

### 📊 Difficulty Levels

| Level | Prerequisites | Pace | Time Multiplier | Best For |
|-------|---------------|------|-----------------|----------|
| **🌱 Beginner** | No prior knowledge required | Slow and methodical | 1.2x | First-time learners, absolute basics |
| **📈 Intermediate** | Some prior knowledge helpful | Moderate and steady | 1.0x | Building on existing knowledge |
| **🚀 Advanced** | Strong foundation required | Fast and intensive | 0.8x | Specialization, mastery, certification |

### 📋 Plan Templates

| Template | Description | Sections | Best For | Time Frame |
|----------|-------------|----------|----------|------------|
| **📋 Basic** | Simple weekly breakdown | Overview, Weekly Plan, Daily Schedule, Resources | Quick learning, simple goals | 1-4 weeks |
| **📊 Detailed** | Comprehensive with tracking | 7 detailed sections including assessment and progress tracking | Complex goals, long-term learning | 1-6 months |
| **⚡ Intensive** | Fast-paced learning | Accelerated schedule with intensive sessions | Time-constrained goals, exam preparation | 1-4 weeks |

### 🌍 Subject Areas

| Area | Examples | Estimated Hours | Best Learning Style |
|------|----------|-----------------|-------------------|
| **Programming** | Python, JavaScript, Java, Web Development | 200-400 hours | Practice + Reading |
| **Languages** | English, Spanish, French, IELTS, TOEFL | 300-600 hours | Mixed approach |
| **Academic** | Mathematics, Physics, Chemistry, Biology | 250-500 hours | Reading + Practice |
| **Certifications** | AWS, Google Cloud, Microsoft, PMP | 120-300 hours | Practice + Videos |
| **Skills** | Public Speaking, Writing, Design, Marketing | 100-200 hours | Mixed approach |

## 🏗️ Project Architecture

### 📁 File Structure

```
42_StudyPlannerAgent/
├── 📄 main.py                   # Main entry point with CLI arguments
├── ⚙️ config.py                 # Configuration and settings management
├── 🌐 web_app.py                # FastAPI web application with REST API
├── 🤖 utils/
│   └── 📄 plan_generator.py     # AI-powered study plan generation
├── 💻 cli/
│   └── 📄 studyplanner.py       # Command-line interface
├── 📋 requirements.txt          # Python dependencies
├── 🧪 test_installation.py      # Comprehensive installation test suite
├── 📦 install.bat               # Windows installation script
├── 🚀 start.bat                 # Windows startup script
├── 🎬 demo.py                   # Demo script showcasing capabilities
├── 📄 env.example               # Environment variables template
├── 🎨 templates/                # HTML templates
│   └── 📄 index.html            # Main study planning interface
├── 🎨 static/                   # Static assets
│   └── 📄 js/
│       └── 📄 app.js            # Frontend JavaScript logic
├── 📁 output/                   # Generated study plans (auto-created)
│   └── 📁 study_plans/          # Individual plan files
├── 📖 README.md                # This comprehensive documentation
└── 📄 SUMMARY.md               # Project summary and metrics
```

### 🔧 Technical Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Python 3.8+ | Core application logic |
| **AI Engine** | OpenAI GPT-4 | Study plan generation |
| **Web Framework** | FastAPI | REST API and web server |
| **Template Engine** | Jinja2 | HTML template rendering |
| **Frontend** | Vanilla JavaScript | Interactive user interface |
| **Styling** | Tailwind CSS | Modern, responsive design |
| **Data Storage** | JSON + File System | Plan persistence |
| **Server** | Uvicorn | ASGI web server |

### 🎯 Key Components

#### 🤖 StudyPlanGenerator (`utils/plan_generator.py`)
- **Core AI Logic**: Handles OpenAI API integration
- **Plan Generation**: Creates personalized study plans
- **File Management**: Saves, loads, and organizes plans
- **Export Options**: Multiple format support (MD, JSON, PDF)
- **Progress Tracking**: Plan management and statistics

#### 🌐 Web Application (`web_app.py`)
- **REST API**: Provides endpoints for all operations
- **Plan Management**: CRUD operations for study plans
- **File Downloads**: Export plans in multiple formats
- **Real-time Generation**: Live plan creation
- **Error Handling**: Robust error management

#### 💻 CLI Interface (`cli/studyplanner.py`)
- **Interactive Menu**: User-friendly terminal interface
- **Plan Generation**: Command-line plan creation
- **Plan Management**: View, load, and delete plans
- **Configuration**: Settings and preferences
- **Help System**: Comprehensive usage guide

#### 🎨 Frontend (`static/` & `templates/`)
- **Interactive UI**: Modern, responsive web interface
- **Real-time Updates**: Dynamic content updates
- **Form Validation**: Client-side input validation
- **Modal Dialogs**: Plan management and help
- **Toast Notifications**: User feedback system

## ⚙️ Configuration & Setup

### 🔑 API Key Setup

**Step 1: Get OpenAI API Key**
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign up or log in to your account
3. Navigate to "API Keys" section
4. Create a new API key
5. Copy the key (starts with `sk-`)

**Step 2: Configure the Key**

```bash
# Option 1: Environment Variable (Recommended)
# Windows
set OPENAI_API_KEY=sk-your_actual_api_key_here

# Linux/Mac
export OPENAI_API_KEY=sk-your_actual_api_key_here

# Option 2: .env File
echo OPENAI_API_KEY=sk-your_actual_api_key_here > .env

# Option 3: config.json
echo '{"openai_api_key": "sk-your_actual_api_key_here"}' > config.json
```

### 🎛️ Advanced Configuration

Edit `config.py` to customize the application:

```python
# Study Plan Generation Settings
MAX_TOKENS = 3000          # Maximum tokens per plan
TEMPERATURE = 0.7          # Creativity level (0.0-1.0)
DEFAULT_LEARNING_STYLE = "mixed"  # Default learning approach
DEFAULT_DIFFICULTY = "intermediate"  # Default difficulty level
DEFAULT_HOURS_PER_DAY = 2  # Default daily study time
DEFAULT_DAYS_AVAILABLE = 30  # Default study period

# File Storage Settings
OUTPUT_DIR = "output"      # Directory for plan files
PLANS_DIR = "study_plans"  # Subdirectory for individual plans

# Web Interface Settings
WEB_TITLE = "StudyPlannerAgent"
WEB_DESCRIPTION = "AI-powered personalized study planning tool"
WEB_VERSION = "1.0.0"
```

## 🧪 Testing & Quality Assurance

### 🔍 Installation Testing

Run the comprehensive test suite to verify everything is working:

```bash
python test_installation.py
```

**Test Coverage:**
- ✅ **Python Version**: Compatibility check (3.8+)
- ✅ **Dependencies**: All required packages installed
- ✅ **File Structure**: All necessary files present
- ✅ **Configuration**: Settings loaded correctly
- ✅ **API Integration**: OpenAI connection test
- ✅ **Plan Generator**: Core functionality test
- ✅ **Web App**: FastAPI application test
- ✅ **File System**: Directory creation and permissions

### 🚀 Performance Testing

```bash
# Test plan generation speed
python -c "
from utils.plan_generator import StudyPlanGenerator
from config import get_api_key
import time

generator = StudyPlanGenerator(get_api_key())
start = time.time()
plan = generator.generate_study_plan('Learn Python', 30, 2, 'mixed', 'intermediate')
end = time.time()
print(f'Generation time: {end-start:.2f} seconds')
print(f'Plan length: {len(plan[\"content\"])} characters')
"
```

### 🐛 Troubleshooting

**Common Issues & Solutions:**

| Issue | Cause | Solution |
|-------|-------|----------|
| **"OpenAI API key not found"** | Missing or invalid API key | Set `OPENAI_API_KEY` environment variable |
| **"Failed to generate plan"** | API quota exceeded or network issue | Check API key credits and internet connection |
| **"Module not found"** | Missing dependencies | Run `pip install -r requirements.txt` |
| **"Port already in use"** | Port 8042 is occupied | Use `--port 8000` or kill the process using the port |
| **"Permission denied"** | File system permissions | Run with appropriate permissions or change directory |
| **"PDF download failed"** | Missing reportlab package | Install with `pip install reportlab` |

### 📊 Performance Metrics

**Expected Performance:**
- **Plan Generation**: 10-30 seconds per plan
- **Web Interface Load**: <1 second
- **API Response Time**: <100ms for most operations
- **Memory Usage**: <50MB typical
- **Concurrent Users**: Supports 10+ simultaneous users

## 🔌 API Documentation

### 📚 Study Plan Generation Endpoints

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `POST` | `/api/generate` | Generate a new study plan | `{goal, days_available, hours_per_day, learning_style, difficulty, subject, template}` | `{success, plan}` |
| `GET` | `/api/plans` | Get all saved plans | - | `{success, plans, total}` |
| `GET` | `/api/plans/{id}` | Get specific plan | - | `{success, plan}` |
| `DELETE` | `/api/plans/{id}` | Delete a plan | - | `{success, message}` |

### 💾 Plan Management Endpoints

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `GET` | `/api/download/{id}/{format}` | Download plan file | - | File download |
| `GET` | `/api/config` | Get configuration options | - | `{success, config}` |
| `GET` | `/health` | Health check | - | `{status, timestamp, version}` |

### 📝 Example API Usage

```javascript
// Generate a study plan
const response = await fetch('/api/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    goal: "Learn JavaScript Programming",
    days_available: 30,
    hours_per_day: 2,
    learning_style: "mixed",
    difficulty: "intermediate",
    subject: "Programming",
    template: "detailed"
  })
});

const result = await response.json();
console.log(result.plan.goal);
```

```python
# Python API usage
import requests

response = requests.post('http://localhost:8042/api/generate', json={
    'goal': 'Master Python for Data Science',
    'days_available': 60,
    'hours_per_day': 3,
    'learning_style': 'practice',
    'difficulty': 'intermediate',
    'subject': 'Programming',
    'template': 'detailed'
})

plan = response.json()['plan']
print(f"Generated: {plan['goal']}")
```

## 💡 Best Practices & Tips

### ✍️ Writing Effective Study Goals

**🎯 Be Specific and Detailed:**
- ❌ **Vague**: "Learn programming"
- ✅ **Specific**: "Master Python for data science and machine learning"

**⏰ Include Time Context:**
- ❌ **Generic**: "Learn Spanish"
- ✅ **Time-bound**: "Learn conversational Spanish in 6 months"

**🎯 Set Clear Objectives:**
- ❌ **Unclear**: "Get better at math"
- ✅ **Specific**: "Master calculus for engineering degree"

**📚 Add Subject Context:**
- ❌ **Broad**: "Learn about AI"
- ✅ **Focused**: "Learn machine learning with Python for career transition"

### 🎨 Study Planning Strategies

**📚 Learning Style Selection:**

| Learning Style | Best For | Tips |
|----------------|----------|------|
| **Reading** | Theory-heavy subjects, academic content | Use textbooks, research papers, documentation |
| **Practice** | Hands-on skills, programming, practical applications | Focus on projects, exercises, real-world applications |
| **Videos** | Visual learners, software tutorials, demonstrations | Use online courses, YouTube, interactive tutorials |
| **Mixed** | Comprehensive learning, complex subjects | Combine multiple approaches for balanced learning |

**📊 Difficulty Level Guidelines:**

| Level | Characteristics | Time Allocation | Best For |
|-------|----------------|-----------------|----------|
| **Beginner** | No prior knowledge, slow pace | 1.2x normal time | First-time learners, absolute basics |
| **Intermediate** | Some knowledge, moderate pace | 1.0x normal time | Building on existing knowledge |
| **Advanced** | Strong foundation, fast pace | 0.8x normal time | Specialization, mastery, certification |

### 🚀 Performance Optimization

**⚡ Faster Plan Generation:**
- Use specific, focused goals for quicker processing
- Choose appropriate difficulty level
- Avoid overly complex scenarios initially

**💾 Better Organization:**
- Use descriptive goals for your plans
- Add subject context for better categorization
- Regularly export your favorite plans

**🎯 Quality Improvement:**
- Experiment with different learning styles
- Try the same goal with different settings
- Use the detailed template for comprehensive planning

## 🔮 Future Roadmap

### 🚀 Planned Features

| Feature | Status | Description |
|---------|--------|-------------|
| **Progress Tracking** | 🔄 Planned | Visual progress charts and analytics |
| **Plan Updates** | 🔄 Planned | Dynamic plan modification based on progress |
| **Collaborative Planning** | 🔄 Planned | Share and collaborate on study plans |
| **Mobile App** | 🔄 Planned | Native mobile application |
| **Calendar Integration** | 🔄 Planned | Export to Google Calendar, Outlook |
| **Resource Integration** | 🔄 Planned | Direct links to recommended resources |
| **AI Tutoring** | 🔄 Planned | Interactive AI study assistant |
| **Multi-language Support** | 🔄 Planned | Plans in multiple languages |

### 🎯 Enhancement Ideas

- **Real-time Collaboration**: Multiple users editing plans simultaneously
- **Resource Integration**: Direct links to recommended courses and materials
- **Progress Analytics**: Detailed learning analytics and insights
- **Study Groups**: Collaborative study planning and sharing
- **Adaptive Learning**: Plans that adjust based on progress and performance
- **Voice Integration**: Voice commands and audio study plans
- **AR/VR Support**: Immersive learning experiences
- **Advanced Scheduling**: Integration with calendar apps and productivity tools

## 🤝 Contributing

We welcome contributions to make StudyPlannerAgent even better!

### 🛠️ How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and test thoroughly
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### 🎯 Areas for Contribution

- **New Learning Styles**: Add custom learning approach definitions
- **Subject Libraries**: Add pre-built subject-specific plans
- **UI Improvements**: Enhance the user interface and experience
- **Performance**: Optimize plan generation speed
- **Documentation**: Improve guides and examples
- **Testing**: Add more test cases and coverage
- **Bug Fixes**: Report and fix issues

### 📋 Contribution Guidelines

- Follow the existing code style
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass
- Be respectful and constructive

## 📞 Support & Community

### 🆘 Getting Help

1. **📖 Documentation**: Check this README and code comments
2. **🧪 Test Suite**: Run `python test_installation.py`
3. **🔍 Troubleshooting**: Review the troubleshooting section
4. **📊 Logs**: Check console output for error messages
5. **🌐 API Status**: Verify OpenAI API is operational

### 🐛 Reporting Issues

When reporting issues, please include:
- **System Information**: OS, Python version, browser
- **Error Messages**: Full error output
- **Steps to Reproduce**: What you were doing when it happened
- **Expected vs Actual**: What you expected vs what happened

### 💬 Community

- **GitHub Issues**: Report bugs and request features
- **Discussions**: Ask questions and share ideas
- **Showcase**: Share your amazing study plans!

## 📄 License & Credits

### 📜 License

This project is part of the **#100DaysOfAI-Agents** challenge by **Muhammad Sami Asghar Mughal**.

**MIT License** - Feel free to use, modify, and distribute!

### 🙏 Acknowledgments

- **OpenAI** for providing the GPT-4 API
- **FastAPI** team for the excellent web framework
- **Tailwind CSS** for the beautiful styling framework
- **Python community** for amazing libraries
- **All contributors** who help improve this project

### 🌟 Inspiration

This project was inspired by the need for intelligent study planning tools that are:
- **Personalized**: Tailored to individual learning styles and goals
- **Intelligent**: AI-powered for optimal learning paths
- **Flexible**: Supporting multiple subjects and timeframes
- **Effective**: Maximizing learning efficiency and outcomes

---

<div align="center">

## 🎉 Ready to Start Learning?

**Create your perfect study plan with the power of AI!**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎯 Examples](#-examples) • [📚 Documentation](#-documentation)

---

**Made with ❤️ by the #100DaysOfAI-Agents community**

*Day 42 of 100 - Building the future of AI agents, one day at a time!*

</div>
