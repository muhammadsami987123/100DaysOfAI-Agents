# Quick Setup Guide - GPTConfigGenerator

## 🚀 Quick Start (5 minutes)

### 1. Install Dependencies
```bash
# Windows
install.bat

# Manual
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Key
```bash
# Copy example environment file
copy env.example .env

# Edit .env and add your API key
LLM_MODEL=openai
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Start the Application
```bash
# Windows
start.bat

# Manual
python main.py
```

### 4. Open Browser
Navigate to: `http://127.0.0.1:8000`

## 🧪 Test Installation
```bash
python test_installation.py
```

## 🎯 Example Usage

### Web Interface
1. Go to `http://127.0.0.1:8000`
2. Enter: "Create a JSON config for Express app with port 3000"
3. Click "Generate Configuration"
4. Copy or download the result

### CLI Interface
```bash
python cli.py "Create docker-compose.yml with PostgreSQL and Redis"
python cli.py --explain config.json --format json
python cli.py --convert config.json --from json --to yaml
```

### Demo
```bash
python demo.py
```

## 🔧 Configuration

### Environment Variables (.env)
```
LLM_MODEL=openai                    # or gemini
OPENAI_API_KEY=your_key_here        # Required for OpenAI
GEMINI_API_KEY=your_key_here        # Required for Gemini
TEMPERATURE=0.3                     # AI creativity (0.0-1.0)
MAX_TOKENS=2000                     # Max response length
```

### Supported Formats
- JSON
- YAML
- TOML
- JavaScript
- TypeScript

### Configuration Types
- Application Settings (Node.js, Django, Flask, etc.)
- DevOps (Docker, Kubernetes, GitHub Actions)
- Linting (ESLint, Prettier, Stylelint)
- Build Tools (Vite, Webpack, Babel)
- Package Managers (package.json, pyproject.toml)
- Database (PostgreSQL, MongoDB, Redis)
- Custom configurations

## 🐛 Troubleshooting

### Common Issues
1. **API Key Error**: Make sure your API key is set in `.env`
2. **Module Not Found**: Run `pip install -r requirements.txt`
3. **Port in Use**: Kill existing process or change port in `main.py`

### Get Help
- Run `python test_installation.py` to diagnose issues
- Check the full README.md for detailed documentation
- Ensure Python 3.8+ is installed

## 🎉 Ready to Use!

You're all set! Start generating configuration files from natural language descriptions.
