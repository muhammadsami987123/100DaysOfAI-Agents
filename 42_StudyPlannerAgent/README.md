# 📚 StudyPlannerAgent - Day 42 of #100DaysOfAI-Agents

**AI-Powered Personalized Study Planning Tool**

StudyPlannerAgent is an intelligent study planning system that creates personalized, comprehensive study plans tailored to your goals, time constraints, and learning preferences. Using advanced AI technology, it helps students and learners efficiently prepare for exams, learn new skills, or manage their study routines.

---

## 🎯 Problem It Solves

Many students struggle with:
- **Poor time management** and study organization
- **Lack of structured learning paths** for complex subjects
- **Difficulty balancing** school, work, and personal life
- **Unclear progression** from basics to advanced topics
- **Inefficient study methods** that don't match their learning style

StudyPlannerAgent provides **clear, achievable plans** tailored to individual goals, time availability, and preferred learning methods.

---

## ✨ Key Features

### 🧠 AI-Powered Planning
- **GPT-4 Integration**: Advanced AI generates comprehensive study plans
- **Personalized Content**: Plans tailored to your specific goals and constraints
- **Intelligent Progression**: Systematic progression from basics to advanced topics
- **Adaptive Learning**: Plans adjust to different learning styles and difficulty levels

### 🎨 Multiple Learning Styles
- **📚 Reading**: Learn through textbooks, articles, and written materials
- **💻 Practice**: Hands-on exercises, projects, and practical application
- **🎥 Videos**: Video tutorials, online courses, and lectures
- **🎯 Mixed**: Balanced combination of all learning methods

### 📊 Flexible Difficulty Levels
- **🌱 Beginner**: No prior knowledge required, slow-paced learning
- **📈 Intermediate**: Some prior knowledge helpful, moderate pace
- **🚀 Advanced**: Strong foundation required, fast-paced learning

### 📋 Plan Templates
- **📋 Basic**: Simple weekly breakdown with daily tasks
- **📊 Detailed**: Comprehensive plan with progress tracking
- **⚡ Intensive**: Fast-paced plan for quick learning

### 💾 Multiple Export Formats
- **Markdown (.md)**: Human-readable format with formatting
- **JSON (.json)**: Structured data for integration
- **PDF (.pdf)**: Professional document format

### 🌐 Dual Interface
- **Web UI**: Beautiful, responsive web interface with real-time generation
- **CLI**: Command-line interface for quick access and automation

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

#### Option 1: Automated Installation (Windows)
```bash
# Clone or download the project
cd 42_StudyPlannerAgent

# Run the installation script
install.bat

# Start the application
start.bat
```

#### Option 2: Manual Installation
```bash
# Clone or download the project
cd 42_StudyPlannerAgent

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
# Windows:
set OPENAI_API_KEY=your_api_key_here
# Linux/Mac:
export OPENAI_API_KEY=your_api_key_here
```

### Usage

#### Web Interface (Recommended)
```bash
python main.py --web
```
Open your browser to: http://127.0.0.1:8042

#### Terminal Interface
```bash
python main.py --terminal
```

#### Quick Plan Generation
```bash
python main.py --quick "Learn JavaScript" --days 30 --hours 2 --style practice
```

---

## 📖 Detailed Usage Guide

### Web Interface

1. **Open the Web Interface**
   - Run `python main.py --web`
   - Navigate to http://127.0.0.1:8042

2. **Create a Study Plan**
   - Enter your study goal (e.g., "Learn Python", "Prepare for IELTS")
   - Set time constraints (days available, hours per day)
   - Choose your learning style
   - Select difficulty level
   - Optionally specify subject area
   - Choose a plan template
   - Click "Generate Study Plan"

3. **Manage Plans**
   - View all saved plans
   - Load existing plans
   - Download plans in different formats
   - Delete unwanted plans

### Terminal Interface

1. **Start Terminal Mode**
   ```bash
   python main.py --terminal
   ```

2. **Interactive Menu**
   - Choose from numbered options
   - Follow prompts for plan generation
   - View and manage saved plans

3. **Available Commands**
   - Generate new study plan
   - View saved plans
   - Load existing plan
   - Configuration settings
   - Help and usage guide

### Command Line Options

```bash
# Basic usage
python main.py [OPTIONS]

# Web interface (default)
python main.py --web

# Terminal interface
python main.py --terminal

# Quick plan generation
python main.py --quick "Learn JavaScript" --days 30 --hours 2

# Custom server settings
python main.py --host 0.0.0.0 --port 8080

# Quick plan with all options
python main.py --quick "Prepare for IELTS" \
  --days 60 \
  --hours 3 \
  --style mixed \
  --difficulty intermediate \
  --subject "Languages" \
  --template detailed \
  --output pdf
```

---

## 🎨 Learning Styles Explained

### 📚 Reading Style
- **Best for**: Visual learners, theory-heavy subjects
- **Methods**: Textbooks, articles, documentation, notes
- **Time allocation**: 40% of study time
- **Examples**: Learning programming concepts, academic subjects

### 💻 Practice Style
- **Best for**: Kinesthetic learners, hands-on subjects
- **Methods**: Exercises, projects, coding, problem-solving
- **Time allocation**: 50% of study time
- **Examples**: Programming, mathematics, practical skills

### 🎥 Video Style
- **Best for**: Auditory learners, visual demonstrations
- **Methods**: Video tutorials, online courses, lectures
- **Time allocation**: 30% of study time
- **Examples**: Software tutorials, language learning

### 🎯 Mixed Style
- **Best for**: Most learners, comprehensive learning
- **Methods**: Combination of reading, practice, and videos
- **Time allocation**: 40% of study time
- **Examples**: Complex subjects requiring multiple approaches

---

## 📊 Difficulty Levels

### 🌱 Beginner
- **Prerequisites**: No prior knowledge required
- **Pace**: Slow and methodical
- **Depth**: Basic concepts and fundamentals
- **Time multiplier**: 1.2x (more time allocated)
- **Examples**: First programming language, basic mathematics

### 📈 Intermediate
- **Prerequisites**: Some prior knowledge helpful
- **Pace**: Moderate and steady
- **Depth**: Intermediate concepts and applications
- **Time multiplier**: 1.0x (standard time allocation)
- **Examples**: Advanced programming, specialized skills

### 🚀 Advanced
- **Prerequisites**: Strong foundation required
- **Pace**: Fast and intensive
- **Depth**: Advanced concepts and mastery
- **Time multiplier**: 0.8x (less time, more intensive)
- **Examples**: Expert-level skills, professional certifications

---

## 📋 Plan Templates

### 📋 Basic Template
- **Overview**: Goal summary and approach
- **Weekly Plan**: Week-by-week breakdown
- **Daily Schedule**: Basic daily routine
- **Resources**: Essential materials and tools
- **Best for**: Simple goals, short timeframes

### 📊 Detailed Template
- **Comprehensive Overview**: Detailed objectives and strategy
- **Weekly Plans**: Specific topics and activities
- **Daily Schedules**: Exact time allocations
- **Resource Library**: Extensive materials and tools
- **Assessment Strategy**: Quizzes, projects, evaluations
- **Progress Tracking**: Metrics and milestones
- **Study Techniques**: Tailored learning methods
- **Troubleshooting**: Common challenges and solutions
- **Best for**: Complex goals, long-term learning

### ⚡ Intensive Template
- **Accelerated Overview**: Fast-track objectives
- **Intensive Schedule**: Compressed timeline
- **Daily Intensive Sessions**: Focused, high-intensity learning
- **Essential Resources**: Core materials only
- **Rapid Assessment**: Quick progress checks
- **Motivation Strategies**: High-energy learning techniques
- **Best for**: Time-constrained goals, exam preparation

---

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description | Required |
|----------|---------|-------------|----------|
| `OPENAI_API_KEY` | - | Your OpenAI API key for GPT-4 | ✅ Yes |
| `PORT` | `8042` | Server port number | ❌ No |
| `HOST` | `127.0.0.1` | Server host address | ❌ No |

### AI Model Settings

#### OpenAI GPT-4 (Default)
- **Model**: `gpt-4` (latest and most capable)
- **Temperature**: 0.7 (balanced creativity and consistency)
- **Max Tokens**: 3000 (sufficient for comprehensive plans)
- **Features**: Advanced reasoning, personalized content, multilingual support

### File Storage Settings
- **Output Directory**: `output/`
- **Plans Directory**: `output/study_plans/`
- **Supported Formats**: `.md`, `.json`, `.pdf`
- **Auto-backup**: Plans saved in multiple formats

---

## 📁 Project Structure

```
42_StudyPlannerAgent/
├── 📄 main.py                   # Main entry point with CLI arguments
├── ⚙️ config.py                 # Configuration and settings management
├── 🌐 web_app.py                # FastAPI web application with REST API
├── 🤖 utils/
│   └── 📄 plan_generator.py     # AI-powered study plan generation
├── 💻 cli/
│   └── 📄 studyplanner.py       # Command-line interface
├── 🎨 templates/
│   └── 📄 index.html            # Main web interface template
├── 🎨 static/
│   └── 📄 js/
│       └── 📄 app.js            # Frontend JavaScript logic
├── 📁 output/                   # Generated study plans (auto-created)
│   └── 📁 study_plans/          # Individual plan files
├── 📋 requirements.txt          # Python dependencies
├── 🚀 install.bat              # Windows installation script
├── ▶️ start.bat                # Windows startup script
└── 📖 README.md                # This comprehensive documentation
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

---

## 🎯 Key Components

### 🤖 StudyPlanGenerator (`utils/plan_generator.py`)
- **Core AI Logic**: Handles OpenAI API integration
- **Plan Generation**: Creates personalized study plans
- **File Management**: Saves, loads, and organizes plans
- **Export Options**: Multiple format support
- **Progress Tracking**: Plan management and statistics

### 🌐 Web Application (`web_app.py`)
- **REST API**: Provides endpoints for all operations
- **Plan Management**: CRUD operations for study plans
- **File Downloads**: Export plans in multiple formats
- **Real-time Generation**: Live plan creation
- **Error Handling**: Robust error management

### 💻 CLI Interface (`cli/studyplanner.py`)
- **Interactive Menu**: User-friendly terminal interface
- **Plan Generation**: Command-line plan creation
- **Plan Management**: View, load, and delete plans
- **Configuration**: Settings and preferences
- **Help System**: Comprehensive usage guide

### 🎨 Frontend (`static/` & `templates/`)
- **Interactive UI**: Modern, responsive web interface
- **Real-time Updates**: Dynamic content updates
- **Form Validation**: Client-side input validation
- **Modal Dialogs**: Plan management and help
- **Toast Notifications**: User feedback system

---

## 🧪 Testing

### Manual Testing
```bash
# Test web interface
python main.py --web
# Open browser to http://127.0.0.1:8042

# Test terminal interface
python main.py --terminal

# Test quick plan generation
python main.py --quick "Learn Python" --days 7 --hours 1
```

### API Testing
```bash
# Test plan generation
curl -X POST "http://127.0.0.1:8042/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Learn JavaScript",
    "days_available": 30,
    "hours_per_day": 2,
    "learning_style": "mixed",
    "difficulty": "intermediate",
    "subject": "Programming",
    "template": "detailed"
  }'

# Test plan listing
curl "http://127.0.0.1:8042/api/plans"

# Test health check
curl "http://127.0.0.1:8042/health"
```

---

## 💡 Tips for Best Results

### Study Goal Formulation
- **Be Specific**: "Learn Python for data analysis" vs "Learn programming"
- **Set Clear Objectives**: Define what success looks like
- **Consider Prerequisites**: Mention any prior knowledge
- **Include Context**: Specify use case or application

### Time Management
- **Be Realistic**: Set achievable daily study hours
- **Consider Constraints**: Account for work, family, other commitments
- **Plan for Breaks**: Include rest days and review periods
- **Buffer Time**: Add extra time for unexpected delays

### Learning Style Selection
- **Know Your Preferences**: Choose what works best for you
- **Experiment**: Try different styles for different subjects
- **Mix and Match**: Combine multiple approaches
- **Adapt Over Time**: Adjust based on progress and feedback

### Difficulty Level
- **Start Conservative**: Begin with lower difficulty if unsure
- **Assess Honestly**: Be realistic about your current level
- **Progressive Overload**: Increase difficulty as you improve
- **Seek Feedback**: Adjust based on plan effectiveness

---

## 🔧 Troubleshooting

### Common Issues

#### API Key Problems
```
❌ Error: OpenAI API key not found!
```
**Solution**: Set your API key using one of these methods:
```bash
# Environment variable
set OPENAI_API_KEY=your_api_key_here  # Windows
export OPENAI_API_KEY=your_api_key_here  # Linux/Mac

# .env file
echo OPENAI_API_KEY=your_api_key_here > .env
```

#### Installation Issues
```
❌ ERROR: Failed to install dependencies
```
**Solutions**:
- Check internet connection
- Update pip: `python -m pip install --upgrade pip`
- Try installing individually: `pip install openai fastapi uvicorn`

#### PDF Generation Issues
```
❌ PDF save failed: PDF generation requires reportlab package
```
**Solution**: Install reportlab for PDF support:
```bash
pip install reportlab
```

#### Port Already in Use
```
❌ Error: Port 8042 is already in use
```
**Solutions**:
- Use different port: `python main.py --port 8080`
- Kill existing process using the port
- Restart your computer

### Performance Issues

#### Slow Plan Generation
- **Check API Limits**: Ensure you haven't exceeded OpenAI rate limits
- **Reduce Plan Complexity**: Use simpler templates for faster generation
- **Check Internet**: Ensure stable internet connection
- **Monitor Usage**: Track API usage and costs

#### Memory Issues
- **Clear Old Plans**: Delete unused study plans
- **Restart Application**: Close and restart the application
- **Check System Resources**: Ensure sufficient RAM and disk space

---

## 🚀 Advanced Usage

### Custom Configuration
```python
# Modify config.py for custom settings
class StudyConfig:
    MAX_TOKENS = 4000  # Increase for longer plans
    TEMPERATURE = 0.5  # Lower for more consistent plans
    DEFAULT_HOURS_PER_DAY = 3  # Change default study time
```

### API Integration
```python
from utils.plan_generator import StudyPlanGenerator

# Initialize generator
generator = StudyPlanGenerator(api_key="your_key")

# Generate plan programmatically
plan = generator.generate_study_plan(
    goal="Learn Machine Learning",
    days_available=90,
    hours_per_day=2,
    learning_style="mixed",
    difficulty="intermediate"
)

# Save in different formats
generator.save_plan(plan, "markdown")
generator.save_plan(plan, "json")
generator.save_plan(plan, "pdf")
```

### Batch Plan Generation
```bash
# Generate multiple plans
python main.py --quick "Learn Python" --output all
python main.py --quick "Learn JavaScript" --output all
python main.py --quick "Learn React" --output all
```

---

## 📈 Future Enhancements

### Planned Features
- **📊 Progress Tracking**: Visual progress charts and analytics
- **🔄 Plan Updates**: Dynamic plan modification based on progress
- **👥 Collaborative Planning**: Share and collaborate on study plans
- **📱 Mobile App**: Native mobile application
- **🎯 Goal Tracking**: Integration with goal-setting frameworks
- **📚 Resource Integration**: Direct links to recommended resources
- **⏰ Calendar Integration**: Export to Google Calendar, Outlook
- **📊 Analytics Dashboard**: Detailed learning analytics
- **🤖 AI Tutoring**: Interactive AI study assistant
- **🌍 Multi-language Support**: Plans in multiple languages

### Community Contributions
- **🎨 UI Themes**: Customizable interface themes
- **📋 Plan Templates**: Community-contributed templates
- **🔌 Integrations**: Third-party service integrations
- **📚 Subject Libraries**: Pre-built subject-specific plans
- **🎯 Specialized Modes**: Exam prep, certification, skill development

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Development Setup
```bash
# Fork and clone the repository
git clone https://github.com/your-username/42_StudyPlannerAgent.git
cd 42_StudyPlannerAgent

# Create development environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Make your changes and test
python main.py --web
```

### Contribution Areas
- **🐛 Bug Fixes**: Report and fix issues
- **✨ New Features**: Add new functionality
- **📖 Documentation**: Improve documentation
- **🎨 UI/UX**: Enhance user interface
- **🧪 Testing**: Add tests and improve coverage
- **🔧 Performance**: Optimize performance
- **🌍 Localization**: Add multi-language support

### Pull Request Process
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit a pull request

---

## 📄 License

This project is part of the #100DaysOfAI-Agents challenge and is released under the MIT License.

---

## 🙏 Acknowledgments

- **OpenAI**: For providing the GPT-4 API that powers the AI planning
- **FastAPI**: For the excellent web framework
- **Tailwind CSS**: For the beautiful styling framework
- **#100DaysOfAI-Agents Community**: For inspiration and support

---

## 📞 Support

### Getting Help
- **📖 Documentation**: Check this README for detailed usage
- **🐛 Issues**: Report bugs on GitHub Issues
- **💬 Discussions**: Join community discussions
- **📧 Contact**: Reach out for support

### Resources
- **🎓 OpenAI Documentation**: [OpenAI API Docs](https://platform.openai.com/docs)
- **🚀 FastAPI Documentation**: [FastAPI Docs](https://fastapi.tiangolo.com/)
- **🎨 Tailwind CSS**: [Tailwind CSS Docs](https://tailwindcss.com/docs)

---

## 🎉 Success Stories

*"StudyPlannerAgent helped me create a comprehensive 3-month plan to learn Python for data science. The AI-generated plan was perfectly tailored to my schedule and learning style!"* - Sarah M.

*"I used StudyPlannerAgent to prepare for my AWS certification. The detailed plan with daily tasks and progress tracking made the difference between passing and failing."* - John D.

*"The mixed learning style approach in my JavaScript study plan was perfect. I could read theory, practice coding, and watch videos all in one cohesive plan."* - Maria L.

---

**🎓 Ready to transform your learning journey? Start with StudyPlannerAgent today!**

```bash
# Quick start
python main.py --quick "Your Study Goal Here"
```

*Happy Learning! 📚✨*
