# ⚙️ GPTConfigGenerator - Day 77 of #100DaysOfAI-Agents

<div align="center">

![GPTConfigGenerator Banner](https://img.shields.io/badge/GPTConfigGenerator-Day%2077-blue?style=for-the-badge&logo=json&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20Framework-red?style=for-the-badge&logo=fastapi&logoColor=white)
![AI](https://img.shields.io/badge/AI-OpenAI%20%7C%20Gemini-purple?style=for-the-badge)

**Instantly Generate JSON/YAML/TOML Configs with GPT from Natural Language**

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [🎯 Usage Examples](#-usage-examples) • [🌐 Web Interface](#-web-interface) • [🔌 API Reference](#-api-reference) • [⚙️ Configuration](#-configuration) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is GPTConfigGenerator?

GPTConfigGenerator is an intelligent AI-powered tool that transforms simple natural language instructions into clean, structured configuration files. Whether you need JSON configs for Node.js apps, YAML files for Docker Compose, or TOML files for Python projects, this agent generates production-ready configurations instantly.

### 🌟 Key Highlights

- **🧠 AI-Powered Generation**: Uses OpenAI GPT-4o-mini or Google Gemini for intelligent config generation
- **📁 Multiple Formats**: Supports JSON, YAML, TOML, JavaScript, and TypeScript configurations
- **🎯 Smart Detection**: Auto-detects configuration type and format from your description
- **✨ Clean Output**: Generates properly formatted, commented, and production-ready configs
- **🌐 Modern Web UI**: Beautiful, responsive interface with real-time generation
- **🔧 Validation & Conversion**: Built-in config validation and format conversion tools
- **📝 Explanations**: Get natural language explanations of generated configurations

---

## 🎯 Features

### 🚀 Core Functionality

- ✅ **Natural Language to Config**: Convert plain English descriptions into structured configs
- ✅ **Multiple Format Support**: JSON, YAML, TOML, JavaScript, TypeScript
- ✅ **Smart Type Detection**: Auto-detects app settings, DevOps, linting, build tools, etc.
- ✅ **Format Conversion**: Convert configurations between different formats
- ✅ **Config Validation**: Validate syntax and structure of configuration files
- ✅ **Inline Comments**: Adds helpful comments explaining complex settings
- ✅ **Sensible Defaults**: Uses production-ready default values and best practices

### 🎨 User Experience

- ✅ **Modern Web Interface**: Clean, responsive design with Tailwind CSS
- ✅ **Real-time Generation**: Instant config generation with loading indicators
- ✅ **Example Templates**: Pre-built examples for common configuration types
- ✅ **Copy & Download**: Easy copying to clipboard and file downloads
- ✅ **Error Handling**: Clear error messages and fallback configurations
- ✅ **Mobile Responsive**: Works seamlessly on desktop and mobile devices

### 🔧 Advanced Capabilities

- ✅ **Dual AI Support**: Choose between OpenAI and Google Gemini models
- ✅ **Config Explanations**: Get natural language explanations of any config
- ✅ **Type-specific Generation**: Tailored configs for different technologies
- ✅ **Best Practices**: Follows industry standards and security guidelines
- ✅ **Extensible**: Easy to add new config types and formats

---

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.8+** installed on your system
- **OpenAI API Key** or **Google Gemini API Key**
- **Internet connection** for AI-powered generation

### ⚡ Installation

1. **Navigate to the project directory:**
   ```bash
   cd 77_GPTConfigGenerator
   ```

2. **Run the installation script:**
   ```bash
   # Windows
   install.bat
   
   # Manual installation
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   pip install -r requirements.txt
   ```

3. **Configure your API key:**
   ```bash
   # Copy the example environment file
   copy env.example .env
   
   # Edit .env and add your API key
   LLM_MODEL=openai  # or gemini
   OPENAI_API_KEY=your_openai_api_key_here
   # OR
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Start the application:**
   ```bash
   # Windows
   start.bat
   
   # Manual start
   python main.py
   ```

5. **Open your browser:**
   Navigate to `http://127.0.0.1:8000`

---

## 🎯 Usage Examples

### 🌐 Web Interface

The intuitive web interface allows you to:

1. **Describe your needs** in natural language
2. **Select configuration type** (or let it auto-detect)
3. **Choose output format** (JSON, YAML, TOML, etc.)
4. **Generate configuration** with one click
5. **Copy or download** the generated config

### 💡 Example Requests

#### Docker Compose Configuration
```
"Create a docker-compose.yml file with PostgreSQL and Redis services"
```

#### Prettier Configuration
```
"Generate a .prettierrc JSON config using 2-space tabs, no semicolons"
```

#### Vite Configuration
```
"Create a vite.config.js file with React and Tailwind CSS"
```

#### GitHub Actions
```
"Give me a GitHub Actions YAML that runs tests on push and pull request"
```

#### Express.js App Config
```
"Create a JSON config for a Node.js Express app with port 3000 and MongoDB"
```

#### ESLint Configuration
```
"Generate an ESLint config for React TypeScript project with strict rules"
```

---

## 🌐 Web Interface

### 🎨 Interface Features

- **Clean Design**: Modern, professional interface with intuitive navigation
- **Real-time Generation**: Watch configurations generate in real-time
- **Example Templates**: Click on examples to quickly try different config types
- **Format Selection**: Choose from JSON, YAML, TOML, JavaScript, TypeScript
- **Type Detection**: Auto-detect configuration type or manually select
- **Copy & Download**: Easy copying to clipboard and file downloads
- **Error Handling**: Clear error messages and helpful suggestions
- **Mobile Responsive**: Works perfectly on all device sizes

### 🔧 Interface Sections

1. **Input Section**: Describe your configuration needs
2. **Options Panel**: Select type and format preferences
3. **Output Section**: View generated configuration
4. **Explanation Panel**: Get natural language explanations
5. **Examples Gallery**: Try pre-built configuration templates

---

## 🔌 API Reference

### 📡 Endpoints

#### Generate Configuration
```http
POST /api/generate
Content-Type: application/json

{
  "user_request": "Create a JSON config for Express app",
  "config_type": "app_settings",
  "format": "json"
}
```

#### Explain Configuration
```http
POST /api/explain
Content-Type: application/json

{
  "config_content": "{\"port\": 3000, \"host\": \"localhost\"}",
  "format": "json"
}
```

#### Convert Configuration
```http
POST /api/convert
Content-Type: application/json

{
  "config_content": "{\"port\": 3000}",
  "from_format": "json",
  "to_format": "yaml"
}
```

#### Validate Configuration
```http
POST /api/validate
Content-Type: application/json

{
  "config_content": "{\"port\": 3000}",
  "format": "json"
}
```

#### Get Supported Formats
```http
GET /api/formats
```

#### Get Configuration Types
```http
GET /api/config-types
```

#### Get Suggestions
```http
GET /api/suggestions?config_type=app_settings&format=json
```

---

## ⚙️ Configuration

### 🔑 Environment Variables

| Variable | Default | Description | Required |
|----------|---------|-------------|----------|
| `LLM_MODEL` | `openai` | AI model to use: `openai` or `gemini` | ✅ |
| `OPENAI_API_KEY` | — | Your OpenAI API key | conditional ✅ |
| `OPENAI_MODEL` | `gpt-4o-mini` | OpenAI model to use | ❌ |
| `GEMINI_API_KEY` | — | Your Google Gemini API key | conditional ✅ |
| `GEMINI_MODEL` | `gemini-2.0-flash` | Gemini model to use | ❌ |
| `TEMPERATURE` | `0.3` | AI creativity level (0.0-1.0) | ❌ |
| `MAX_TOKENS` | `2000` | Maximum tokens for AI response | ❌ |

### 🎛️ Configuration Types

The agent supports various configuration types:

- **App Settings**: Node.js, Django, Flask, React, Vue configurations
- **DevOps**: Docker Compose, Kubernetes, GitHub Actions, CI/CD
- **Linting**: ESLint, Prettier, Stylelint, Black, Pylint
- **Build Tools**: Vite, Webpack, Babel, Rollup, Parcel
- **Package Managers**: package.json, pyproject.toml, composer.json
- **Database**: PostgreSQL, MongoDB, Redis, MySQL configurations
- **Custom**: Any custom configuration based on description

### 📁 Supported Formats

- **JSON**: Standard JSON configuration files
- **YAML**: YAML configuration files with proper indentation
- **TOML**: TOML configuration files for Python projects
- **JavaScript**: JavaScript configuration files with exports
- **TypeScript**: TypeScript configuration files with types

---

## 🏗️ Project Structure

```
77_GPTConfigGenerator/
├── main.py                    # FastAPI application entry point
├── agent.py                   # Main GPTConfigGenerator agent class
├── config.py                  # Configuration and settings
├── utils/
│   ├── __init__.py
│   └── llm_service.py         # LLM integration (OpenAI/Gemini)
├── templates/
│   └── index.html             # Web interface template
├── requirements.txt           # Python dependencies
├── env.example               # Environment variables template
├── install.bat               # Windows installation script
├── start.bat                 # Windows startup script
└── README.md                 # This documentation
```

### 🔧 Key Components

- **`main.py`**: FastAPI web server with REST API endpoints
- **`agent.py`**: Core agent logic for config generation and processing
- **`utils/llm_service.py`**: AI model integration and prompt engineering
- **`config.py`**: Application configuration and supported formats
- **`templates/index.html`**: Modern web interface with Tailwind CSS

---

## 🧪 Testing & Quality Assurance

### 🔍 Manual Testing

1. **Installation Test**: Run `install.bat` and verify all dependencies install
2. **API Key Test**: Ensure your API key is properly configured
3. **Generation Test**: Try generating different types of configurations
4. **Format Test**: Test all supported output formats
5. **Validation Test**: Test config validation and conversion features

### 🚀 Functional Testing

- ✅ **Config Generation**: Generate configs for different technologies
- ✅ **Format Support**: Test JSON, YAML, TOML, JS, TS outputs
- ✅ **Type Detection**: Verify auto-detection of config types
- ✅ **Error Handling**: Test error scenarios and fallback configs
- ✅ **Web Interface**: Test all UI interactions and responsiveness

---

## 🐛 Troubleshooting

### Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| **"API key not found"** | Missing or invalid API key | Check `.env` file and ensure API key is set |
| **"Module not found"** | Missing dependencies | Run `pip install -r requirements.txt` |
| **"Port already in use"** | Port 8000 is occupied | Kill existing process or change port in `main.py` |
| **"Invalid JSON"** | Malformed configuration | Check the generated config syntax |
| **"Generation failed"** | AI service error | Check internet connection and API key validity |

### 🔧 Debug Mode

Enable debug mode by setting environment variable:
```bash
set DEBUG=true  # Windows
export DEBUG=true  # Linux/Mac
```

---

## 🔮 Future Roadmap

### 🚀 Planned Features

| Feature | Status | Description |
|---------|--------|-------------|
| **Config Templates** | 🔄 Planned | Pre-built templates for common configurations |
| **Batch Generation** | 🔄 Planned | Generate multiple configs at once |
| **Config Comparison** | 🔄 Planned | Compare different configuration versions |
| **Schema Validation** | 🔄 Planned | Validate configs against JSON schemas |
| **Config History** | 🔄 Planned | Save and manage generated configurations |
| **Custom Prompts** | 🔄 Planned | Allow custom AI prompts for specific needs |
| **Config Optimization** | 🔄 Planned | Optimize configs for performance and security |
| **Multi-language Support** | 🔄 Planned | Support for more configuration languages |

### 🎯 Enhancement Ideas

- **Config Templates**: Pre-built templates for popular frameworks
- **Smart Suggestions**: AI-powered suggestions for improving configs
- **Security Analysis**: Check configurations for security best practices
- **Performance Optimization**: Optimize configs for better performance
- **Documentation Generation**: Auto-generate documentation from configs

---

## 🤝 Contributing

We welcome contributions to make GPTConfigGenerator even more powerful!

### 🛠️ How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes** and test thoroughly
4. **Commit your changes**: `git commit -m 'feat: Add amazing new feature'`
5. **Push to the branch**: `git push origin feature/your-feature-name`
6. **Open a Pull Request**

### 🎯 Areas for Contribution

- **New Config Types**: Add support for new configuration types
- **Format Support**: Add support for additional file formats
- **UI Improvements**: Enhance the web interface
- **API Enhancements**: Improve API endpoints and responses
- **Documentation**: Improve documentation and examples
- **Testing**: Add comprehensive test coverage
- **Performance**: Optimize generation speed and accuracy

### 📋 Contribution Guidelines

- Follow the existing code style and naming conventions
- Add type hints and docstrings for new functions
- Test your changes thoroughly
- Update documentation as needed
- Ensure all tests pass before submitting

---

## 📞 Support & Community

### 🆘 Getting Help

1. **📖 Documentation**: Refer to this README for comprehensive information
2. **🐛 Issues**: Check the troubleshooting section for common issues
3. **💬 Discussions**: Join GitHub discussions for questions and ideas
4. **🔍 Search**: Search existing issues before creating new ones

### 🐛 Reporting Issues

When reporting issues, please include:

- **System Information**: OS, Python version, browser
- **Error Messages**: Complete error traceback if applicable
- **Steps to Reproduce**: Clear steps to reproduce the issue
- **Expected vs Actual**: What you expected vs what happened

---

## 📄 License & Credits

### 📜 License

This project is part of the **#100DaysOfAI-Agents** challenge by **Muhammad Sami Asghar Mughal**.

**MIT License** - Feel free to use, modify, and distribute!

### 🙏 Acknowledgments

- **OpenAI** for providing powerful GPT models
- **Google Gemini** for innovative AI capabilities
- **FastAPI** for the excellent web framework
- **Tailwind CSS** for beautiful UI components
- **Python community** for the rich ecosystem of libraries
- **All contributors** who help improve this project

### 🌟 Inspiration

This project was inspired by the need for developers to quickly generate configuration files without memorizing complex syntax. GPTConfigGenerator makes configuration generation:

- **Fast**: Generate configs in seconds with natural language
- **Accurate**: AI-powered generation ensures correct syntax and structure
- **Flexible**: Support for multiple formats and configuration types
- **User-Friendly**: Simple interface that anyone can use

---

<div align="center">

## 🎉 Ready to Generate Configs?

**Transform your natural language into structured configurations instantly!**

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [🎯 Usage Examples](#-usage-examples) • [🌐 Web Interface](#-web-interface)

---

**Made with ❤️ by Muhammad Sami Asghar Mughal for Day 77 of #100DaysOfAI-Agents**

*Building the future of AI agents, one day at a time!*

</div>
