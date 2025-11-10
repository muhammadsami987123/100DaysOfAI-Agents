# 🤖 FormFillerBot - Day 99 of #100DaysOfAI-Agents

<div align="center">

![FormFillerBot Banner](https://img.shields.io/badge/FormFillerBot-Day%2099-blue?style=for-the-badge&logo=google&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20Framework-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-API-blue?style=for-the-badge&logo=google&logoColor=white)
![OpenAI GPT-4](https://img.shields.io/badge/OpenAI_GPT--4-API-orange?style=for-the-badge&logo=openai&logoColor=white)

**Your AI-powered auto-fill assistant for web forms using locally stored data!**

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [🎭 Examples](#-examples) • [🏗️ Project Architecture](#️-project-architecture) • [⚙️ Configuration](#️-configuration--setup) • [🧪 Testing](#-testing--quality-assurance) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is FormFillerBot?

FormFillerBot is an AI-assisted auto-fill system that detects form fields on any website, maps them to stored user data using an LLM (Google Gemini or OpenAI GPT-4), and provides intelligent fill suggestions. All user data is stored locally on your device, ensuring complete privacy and security.

### 🌟 Key Highlights

- **🔒 Privacy-First**: All data is stored locally on your device. No cloud storage unless you explicitly choose it.
- **🤖 AI-Powered Field Detection**: Uses GPT-4.1 or Gemini 2.0-flash to understand form fields and map them to your data.
- **📝 Comprehensive Data Management**: Store personal info, professional details, education, and custom fields.
- **🎨 Modern Web Interface**: Clean, responsive UI with dark/light mode for managing data and analyzing forms.
- **⚙️ Configurable LLMs**: Easily switch between Gemini and OpenAI models via the UI.
- **🔍 Smart Field Mapping**: Handles variations like "Your Full Name," "Applicant Name," "First + Last Name," etc.

## 🎯 Features

### 🚀 Core Functionality
- ✅ **Local Data Storage**: Store user information securely on your device (name, email, phone, social links, job details).
- ✅ **AI-Powered Form Analysis**: Uses LLM to understand form fields and map them to stored data.
- ✅ **Intelligent Field Matching**: Handles field name variations and context to provide accurate mappings.
- ✅ **Fill Suggestions**: Get confidence-scored suggestions for each form field.
- ✅ **Data Management**: Edit, update, and manage your local data through a web interface.
- ✅ **LLM Selection**: Choose between Google Gemini and OpenAI GPT-4 for form analysis.

### 🎨 User Experience
- ✅ **Modern Dashboard UI**: Intuitive layout for data management and form analysis.
- ✅ **Dark/Light Mode**: User-friendly theme toggle for comfortable viewing.
- ✅ **Tabbed Interface**: Separate tabs for data management and form analysis.
- ✅ **Visual Feedback**: Clear success/error messages and loading indicators.
- ✅ **Responsive Design**: Works seamlessly on desktop and mobile devices.

### 📊 Management & Integration
- ✅ **Centralized Configuration**: Uses a `Config` class and `.env` file for easy management of API keys and settings.
- ✅ **Modular Codebase**: Organized Python files for clear separation of concerns.
- ✅ **JSON Data Storage**: Simple, human-readable JSON format for user data.

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.8+** installed on your system.
- **Google Gemini API Key** (get one from [Google AI Studio](https://aistudio.google.com/app/apikey)).
- **OpenAI API Key** (get one from [OpenAI](https://platform.openai.com/account/api-keys)) (optional, if you want to use GPT-4).
- **Internet connection** for AI form analysis.

### 🔧 Manual Installation

```bash
# 1. Navigate to the agent's directory
cd 99_FormFillerBot

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment (Windows)
venv\Scripts\activate
# On Linux/Mac, use: source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up environment variables
# Create a .env file in the 99_FormFillerBot directory:
echo GEMINI_API_KEY=your_gemini_api_key_here > .env
echo OPENAI_API_KEY=your_openai_api_key_here >> .env
echo DEFAULT_LLM=gemini >> .env
# Replace 'your_gemini_api_key_here' and 'your_openai_api_key_here' with your actual API keys.
```

### 🎯 First Run (Web UI - Recommended)

```bash
# 1. Navigate to the agent's directory (if not already there)
cd 99_FormFillerBot

# 2. Run the application
python main.py

# 3. Then, open your web browser and navigate to:
# http://127.0.0.1:8000
```

## 🎭 Examples & Usage

### 🌐 Web Interface

#### 1. **Manage Your Data**
   - Navigate to the "Manage Data" tab
   - Fill in your personal information, professional details, and education
   - Click "Save Data" to store your information locally
   - All data is saved to `./data/user_data.json`

#### 2. **Analyze a Form**
   - Navigate to the "Analyze Form" tab
   - Paste form field information in JSON format:
     ```json
     [
       {
         "id": "email",
         "name": "email",
         "type": "email",
         "label": "Email Address",
         "placeholder": "your@email.com"
       },
       {
         "id": "name",
         "name": "full_name",
         "type": "text",
         "label": "Full Name"
       },
       {
         "id": "phone",
         "name": "phone_number",
         "type": "tel",
         "label": "Phone Number"
       }
     ]
     ```
   - Optionally paste form HTML for additional context
   - Select your preferred AI model (Gemini or OpenAI)
   - Click "Analyze Form" to get fill suggestions

#### 3. **Review Fill Suggestions**
   - View field mappings with confidence levels (high, medium, low)
   - See suggested values from your stored data
   - Review the reasoning for each mapping
   - Use the suggestions to fill forms manually or via browser extension

### 📝 Example Form Field JSON

```json
[
  {
    "id": "first_name",
    "name": "first_name",
    "type": "text",
    "label": "First Name",
    "placeholder": "Enter your first name"
  },
  {
    "id": "last_name",
    "name": "last_name",
    "type": "text",
    "label": "Last Name",
    "placeholder": "Enter your last name"
  },
  {
    "id": "email",
    "name": "email",
    "type": "email",
    "label": "Email Address",
    "placeholder": "your@email.com"
  },
  {
    "id": "phone",
    "name": "phone",
    "type": "tel",
    "label": "Phone Number",
    "placeholder": "(555) 123-4567"
  },
  {
    "id": "linkedin",
    "name": "linkedin_url",
    "type": "url",
    "label": "LinkedIn Profile",
    "placeholder": "https://linkedin.com/in/yourprofile"
  }
]
```

### 🔍 Example Analysis Result

```json
{
  "success": true,
  "field_mappings": [
    {
      "field_id": "email",
      "field_name": "email",
      "field_type": "email",
      "suggested_value": "user@example.com",
      "confidence": "high",
      "data_source": "personal_info.email",
      "reasoning": "Email field clearly maps to personal_info.email"
    },
    {
      "field_id": "name",
      "field_name": "full_name",
      "field_type": "text",
      "suggested_value": "John Doe",
      "confidence": "medium",
      "data_source": "personal_info.full_name",
      "reasoning": "Name field likely refers to full name, but could also be first+last"
    }
  ]
}
```

## 🏗️ Project Architecture

### 📁 Directory Structure

```
99_FormFillerBot/
│
├── agent.py                 # Main FormFillerBot agent logic
├── config.py                # Configuration settings
├── web_app.py               # FastAPI web application
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore file
├── README.md               # This file
│
├── data/                   # Local data storage (created automatically)
│   └── user_data.json      # User data file
│
├── utils/                  # Utility modules
│   ├── __init__.py
│   └── llm_service.py      # LLM service for Gemini and OpenAI
│
├── templates/              # HTML templates
│   └── index.html          # Main web interface
│
├── static/                 # Static files
│   └── main.css            # Custom styles
│
└── prompts/                # Prompt templates
    └── field_mapping_prompt.txt  # Prompt for field mapping
```

### 🔧 Key Components

#### 1. **FormFillerBot Agent** (`agent.py`)
   - Manages local user data (CRUD operations)
   - Analyzes form fields using LLM
   - Maps form fields to user data
   - Provides fill suggestions with confidence scores

#### 2. **Web Application** (`web_app.py`)
   - FastAPI routes for data management
   - Form analysis endpoints
   - JSON API for programmatic access
   - HTML interface for user interaction

#### 3. **LLM Service** (`utils/llm_service.py`)
   - Integration with Google Gemini API
   - Integration with OpenAI API
   - JSON response parsing
   - Error handling and fallbacks

#### 4. **Configuration** (`config.py`)
   - Environment variable management
   - API key configuration
   - Data directory settings
   - LLM model selection

### 🔄 Workflow

1. **Data Management**:
   - User enters data via web interface
   - Data is saved to `./data/user_data.json`
   - All data remains local on the device

2. **Form Analysis**:
   - User provides form field information (JSON)
   - FormFillerBot sends fields and user data to LLM
   - LLM analyzes fields and maps them to user data
   - Results are returned with confidence scores

3. **Fill Suggestions**:
   - User reviews field mappings
   - Suggested values are displayed
   - User can use suggestions to fill forms manually or via extension

## ⚙️ Configuration & Setup

### 🔑 Environment Variables

Create a `.env` file in the project root:

```env
# LLM API Keys
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# LLM Configuration
DEFAULT_LLM=gemini
GEMINI_MODEL=gemini-2.0-flash
OPENAI_MODEL=gpt-4.1

# Data Storage
DATA_DIR=./data
```

### 📊 Data Structure

User data is stored in JSON format:

```json
{
  "personal_info": {
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1-555-123-4567",
    "date_of_birth": "1990-01-01",
    "address": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip_code": "10001",
    "country": "USA"
  },
  "professional": {
    "job_title": "Software Engineer",
    "company": "Tech Corp",
    "linkedin": "https://linkedin.com/in/johndoe",
    "github": "https://github.com/johndoe",
    "portfolio": "https://johndoe.dev"
  },
  "education": {
    "degree": "Bachelor of Science",
    "university": "State University",
    "graduation_year": "2012"
  },
  "custom_fields": {}
}
```

## 🧪 Testing & Quality Assurance

### 🧪 Manual Testing

1. **Data Management**:
   - Add personal information
   - Update professional details
   - Save and verify data persistence
   - Check data file location (`./data/user_data.json`)

2. **Form Analysis**:
   - Provide form field JSON
   - Analyze form with different LLM models
   - Verify field mappings
   - Check confidence scores

3. **Error Handling**:
   - Test with missing API keys
   - Test with invalid JSON
   - Test with empty form fields
   - Verify error messages

### 🔍 API Testing

You can test the API endpoints using curl or Postman:

```bash
# Get user data
curl http://localhost:8000/api/user-data

# Update user data
curl -X POST http://localhost:8000/api/update-data \
  -F "data_updates={\"personal_info\":{\"email\":\"test@example.com\"}}" \
  -F "llm_choice=gemini"

# Analyze form
curl -X POST http://localhost:8000/api/analyze-form \
  -F "form_fields=[{\"id\":\"email\",\"name\":\"email\",\"type\":\"email\",\"label\":\"Email\"}]" \
  -F "form_html=" \
  -F "llm_choice=gemini"
```

## 🚧 Future Enhancements

### 🔮 Planned Features

- [ ] **Browser Extension**: Chrome/Firefox extension for direct form filling
- [ ] **Auto-Fill Templates**: Save and reuse form fill templates
- [ ] **Field Detection**: Automatic form field detection from HTML
- [ ] **Multi-Profile Support**: Manage multiple user profiles
- [ ] **Export/Import**: Export and import user data
- [ ] **Form History**: Track and manage filled forms
- [ ] **Custom Field Mappings**: User-defined field mapping rules
- [ ] **Privacy Mode**: Temporary data storage for one-time forms

### 🌐 Browser Extension Roadmap

1. **Content Script**: Inject into web pages to detect forms
2. **Field Detection**: Automatically extract form fields from DOM
3. **Fill Button**: Add "Fill Form" button to forms
4. **Preview Mode**: Show fill preview before applying
5. **Confirmation Dialog**: Confirm before filling sensitive fields

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### 📝 Contribution Guidelines

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is part of the #100DaysOfAI-Agents challenge and is open source.

## 🙏 Acknowledgments

- **Google Gemini API** for powerful AI capabilities
- **OpenAI** for GPT-4 integration
- **FastAPI** for the web framework
- **Tailwind CSS** for beautiful UI components

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](../../issues) page
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

## 🎉 Conclusion

FormFillerBot is a powerful, privacy-focused tool for auto-filling web forms using AI. With local data storage and intelligent field mapping, it provides a secure and efficient way to manage form filling tasks.

**Happy Form Filling! 🚀**

---

<div align="center"> 

**Made with ❤️ for #100DaysOfAI-Agents**

[⬆ Back to Top](#-formfillerbot---day-99-of-100daysofa-agents)

</div>

