# 🤖 FormFillerBot - Day 99 of #100DaysOfAI-Agents

<div align="center">

![FormFillerBot Banner](https://img.shields.io/badge/FormFillerBot-Day%2099-blue?style=for-the-badge&logo=google&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20Framework-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-API-blue?style=for-the-badge&logo=google&logoColor=white)
![OpenAI GPT-4](https://img.shields.io/badge/OpenAI_GPT--4-API-orange?style=for-the-badge&logo=openai&logoColor=white)

**Your AI-powered auto-fill assistant for web forms using locally stored data!**

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [🎭 Examples](#-examples) • [📚 Documentation](#-documentation) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is FormFillerBot?

FormFillerBot is an intelligent AI-powered assistant designed to streamline the process of filling out web forms. It leverages advanced Large Language Models (LLMs) like Google Gemini and OpenAI GPT-4 to intelligently detect form fields on any website, map them to your securely stored local data, and provide accurate fill suggestions. With a strong emphasis on privacy, all your personal information is kept on your device, giving you complete control and peace of mind.

### 🌟 Key Highlights

- **🔒 Privacy-First**: All user data is stored locally on your device, ensuring no sensitive information leaves your system without your explicit consent.
- **🤖 AI-Powered Field Detection**: Utilizes cutting-edge LLMs (Google Gemini or OpenAI GPT-4) to understand the context of form fields and accurately map them to your data.
- **📝 Comprehensive Data Management**: Easily store and manage various categories of personal, professional, and educational information, along with custom fields.
- **🎨 Modern Web Interface**: Features a clean, intuitive, and responsive user interface with dark/light mode, making data management and form analysis a breeze.
- **⚙️ Configurable LLMs**: Seamlessly switch between Google Gemini and OpenAI models directly from the UI to leverage your preferred AI.
- **🔍 Smart Field Mapping**: Intelligently handles diverse field naming conventions (e.g., "Your Full Name," "Applicant Name," "First + Last Name") to provide precise suggestions.

## 🎯 Features

### 🚀 Core Functionality
- ✅ **Local Data Storage**: Securely store personal, professional, and educational data on your device in a structured JSON format.
- ✅ **AI-Powered Form Analysis**: Employs LLMs to interpret form fields and suggest relevant data from your local storage.
- ✅ **Intelligent Field Matching**: Advanced algorithms and LLM capabilities ensure accurate mapping even with varied field labels.
- ✅ **Confidence-Scored Suggestions**: Provides fill suggestions with confidence levels (high, medium, low) to guide your choices.
- ✅ **Data Management UI**: A user-friendly web interface for adding, editing, and reviewing your stored data.
- ✅ **LLM Selection**: Choose between Google Gemini and OpenAI models for form analysis based on your preference and API access.

### 🎨 User Experience
- ✅ **Intuitive Dashboard**: A modern, responsive web UI for managing data and analyzing forms.
- ✅ **Dark/Light Mode**: Toggle between themes for optimal viewing comfort.
- ✅ **Tabbed Navigation**: Easily switch between "Manage Data" and "Analyze Form" sections.
- ✅ **Clear Feedback**: Instant success/error messages and loading indicators for a smooth experience.
- ✅ **Responsive Design**: Optimized for seamless use across desktop and mobile devices.

### 📊 Management & Integration
- ✅ **Centralized Configuration**: Utilizes a `Config` class and `.env` file for easy management of API keys, default LLMs, and data paths.
- ✅ **Modular Codebase**: Well-organized Python files ensure clear separation of concerns, making the project easy to understand and extend.
- ✅ **JSON Data Storage**: User data is stored in human-readable JSON files, facilitating easy inspection and backup.

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.8+** installed on your system.
- **Google Gemini API Key** (obtainable from [Google AI Studio](https://aistudio.google.com/app/apikey)).
- **OpenAI API Key** (optional, if you plan to use GPT-4, available from [OpenAI Platform](https://platform.openai.com/account/api-keys)).
- **Internet connection** is required for AI form analysis.

### 🔧 Manual Installation

```bash
# 1. Navigate to the agent's directory
cd 99_FormFillerBot

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the virtual environment (Windows)
venv\Scripts\activate
# On Linux/Mac, use: source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up environment variables
# Create a .env file in the 99_FormFillerBot directory with your API keys:
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

# 3. Open your web browser and navigate to:
# http://127.0.0.1:8000
```

## 🎭 Examples & Usage

### 🌐 Web Interface

The web interface provides an interactive way to manage your data and analyze forms:

#### 1. **Manage Your Data**
   - Navigate to the "Manage Data" tab.
   - Fill in your personal, professional, and educational information using the provided forms.
   - Click "Save Data" to securely store your information locally.
   - All data is saved to `./data/user_data.json` within your project directory.

#### 2. **Analyze a Form**
   - Switch to the "Analyze Form" tab.
   - Paste the form field information in JSON format (e.g., extracted from a web page's HTML).
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
       }
     ]
     ```
   - Optionally, paste the full form HTML for additional context, which can improve LLM accuracy.
   - Select your preferred AI model (Gemini or OpenAI) for the analysis.
   - Click "Analyze Form" to receive intelligent fill suggestions.

#### 3. **Review Fill Suggestions**
   - The analysis results will display a list of suggested mappings.
   - Each mapping includes the suggested value from your stored data, a confidence level (high, medium, low), the data source, and a brief reasoning for the match.
   - Use these suggestions to manually fill out forms or integrate with browser extensions for automated filling.

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

## 📚 Documentation

### 📁 File Structure

```
99_FormFillerBot/
│
├── 📄 agent.py                 # Core FormFillerBot logic for data management and form analysis
├── ⚙️ config.py                # Configuration settings for API keys, LLMs, and data paths
├── 🌐 web_app.py               # FastAPI application defining API routes and serving the UI
├── 📄 main.py                  # Application entry point, starts the FastAPI server
├── 📋 requirements.txt         # Python dependencies required for the project
├── 🚫 .gitignore               # Specifies intentionally untracked files to ignore
├── 📄 README.md                # This documentation file
│
├── 🗄️ data/                   # Directory for local data storage (auto-created if not exists)
│   └── user_data.json      # JSON file containing the user's stored data
│
├── 🛠️ utils/                  # Utility modules
│   ├── __init__.py         # Initializes the utils package
│   └── llm_service.py      # Handles interactions with Google Gemini and OpenAI APIs
│
├── 🖼️ templates/              # HTML templates for the web interface
│   └── index.html          # Main web page template
│
├── 🎨 static/                 # Static assets for the web interface
│   └── main.css            # Custom CSS styles for the UI
│
└── 💬 prompts/                # Directory for LLM prompt templates
    └── field_mapping_prompt.txt  # Template for the form field mapping prompt
```

### 🔧 Technical Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Python 3.8+ | Core application logic and API development |
| **AI Engine** | Google Gemini, OpenAI GPT-4 | Intelligent form field analysis and data mapping |
| **Web Framework** | FastAPI | High-performance web framework for API and UI serving |
| **Template Engine** | Jinja2 | Renders dynamic HTML content for the web interface |
| **Frontend** | HTML, CSS, JavaScript | Interactive user interface with modern styling |
| **Data Storage** | JSON (local file system) | Secure and private storage of user data |
| **Server** | Uvicorn | ASGI web server for running the FastAPI application |
| **Environment** | python-dotenv | Manages environment variables for configuration |

### 🎯 Key Components

#### 🤖 FormFillerBot Agent (`agent.py`)
- **Data Management**: Provides CRUD (Create, Read, Update, Delete) operations for local user data.
- **Form Analysis**: Orchestrates the process of sending form field information and user data to the LLM.
- **Field Mapping**: Interprets LLM responses to map form fields to appropriate user data fields.
- **Suggestion Generation**: Compiles and returns fill suggestions with confidence scores.

#### 🌐 Web Application (`web_app.py`)
- **FastAPI Routes**: Defines API endpoints for fetching/updating user data and analyzing forms.
- **HTML Interface**: Serves the `index.html` template, providing the user-facing dashboard.
- **Request Handling**: Processes incoming HTTP requests, including form submissions and API calls.

#### 💡 LLM Service (`utils/llm_service.py`)
- **API Integration**: Manages connections and requests to both Google Gemini and OpenAI APIs.
- **Model Selection**: Allows dynamic switching between configured LLM providers.
- **Prompt Management**: Reads and formats prompt templates for LLM interactions.
- **Response Parsing**: Handles parsing of LLM responses, including JSON extraction and error handling.

#### ⚙️ Configuration (`config.py`)
- **Environment Variables**: Loads API keys and other settings from a `.env` file.
- **LLM Settings**: Configures default LLM, model names, and data directory paths.
- **Data File Path**: Defines the location for `user_data.json`.

## ⚙️ Configuration & Setup

### 🔑 API Key Setup

**Step 1: Obtain API Keys**
- **Google Gemini**: Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
- **OpenAI**: Get your API key from [OpenAI Platform](https://platform.openai.com/account/api-keys).

**Step 2: Configure the Keys**
Create a `.env` file in the root directory of `99_FormFillerBot` and add your API keys:

```env
# LLM API Keys
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# LLM Configuration
DEFAULT_LLM=gemini # Can be 'gemini' or 'openai'
GEMINI_MODEL=gemini-2.0-flash
OPENAI_MODEL=gpt-4.1 # Or gpt-3.5-turbo, etc.

# Data Storage
DATA_DIR=./data # Directory where user_data.json will be stored
```
**Important**: Replace `your_gemini_api_key_here` and `your_openai_api_key_here` with your actual API keys. Never commit your `.env` file to version control.

### 🎛️ Advanced Configuration

You can customize default settings by modifying `config.py` or the `.env` file:

```python
# config.py snippet
class Config:
    GEMINI_API_KEY = _strip(os.getenv("GEMINI_API_KEY"))
    OPENAI_API_KEY = _strip(os.getenv("OPENAI_API_KEY"))
    DEFAULT_LLM = _strip(os.getenv("DEFAULT_LLM", "gemini")) # Default LLM to use
    GEMINI_MODEL = _strip(os.getenv("GEMINI_MODEL", "gemini-2.0-flash")) # Specific Gemini model
    OPENAI_MODEL = _strip(os.getenv("OPENAI_MODEL", "gpt-4.1")) # Specific OpenAI model
    DATA_DIR = _strip(os.getenv("DATA_DIR")) or "./data" # Directory for user data
    DATA_FILE = os.path.join(DATA_DIR, "user_data.json") # Full path to user data file
```

### 📊 Data Structure

User data is stored in `user_data.json` with the following structure:

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
    "portfolio": "https://johndoe.dev",
    "resume_url": ""
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

### 🔍 Manual Testing

1. **Data Management**:
   - Access the "Manage Data" tab.
   - Fill in various personal, professional, and educational fields.
   - Click "Save Data" and verify that the `user_data.json` file is created/updated correctly in the `./data` directory.
   - Reload the page to ensure data persists.
   - Test with empty fields and ensure they are saved as empty strings.

2. **Form Analysis**:
   - Switch to the "Analyze Form" tab.
   - Provide a sample JSON of form fields (e.g., from the examples above).
   - Experiment with different LLM models (Gemini/OpenAI) if both API keys are configured.
   - Click "Analyze Form" and review the generated `field_mappings`.
   - Verify that suggested values, confidence levels, and reasoning are accurate based on your stored data.
   - Test with form fields that have no corresponding data to ensure they are correctly omitted or marked as low confidence.

3. **Error Handling**:
   - Test the application with missing or invalid API keys (by removing them from `.env`).
   - Provide malformed JSON in the "Form Fields" textarea.
   - Observe error messages in the UI and console for clarity and helpfulness.

### 🚀 API Testing

You can interact with the backend API directly using tools like `curl` or Postman/Insomnia.

```bash
# Get user data
curl -X POST http://localhost:8000/api/user-data

# Update user data (example: update email)
curl -X POST http://localhost:8000/api/update-data \
  -F "data_updates={"personal_info":{"email":"new.email@example.com"}}" \
  -F "llm_choice=gemini"

# Analyze form fields
curl -X POST http://localhost:8000/api/analyze-form \
  -F "form_fields=[{"id":"email","name":"email","type":"email","label":"Email"}]" \
  -F "form_html=<form><label>Your Name</label><input type='text' name='full_name'></form>" \
  -F "llm_choice=gemini"
```

### 🐛 Troubleshooting

**Common Issues & Solutions:**

| Issue | Cause | Solution |
|---|---|---|
| **"API Key not found"** | Missing or incorrect API key in `.env` | Ensure `GEMINI_API_KEY` and/or `OPENAI_API_KEY` are correctly set in your `.env` file. |
| **"Failed to generate content"** | LLM API error, rate limit, or network issue | Check your internet connection, API key validity, and LLM provider's status. |
| **"ModuleNotFoundError"** | Missing Python dependencies | Run `pip install -r requirements.txt` to install all required packages. |
| **"Port already in use"** | Port 8000 (default for FastAPI) is occupied | Close other applications using port 8000 or change the port in `main.py` (e.g., `uvicorn.run(app, host="0.0.0.0", port=8001)`). |
| **"JSON parsing error"** | Malformed JSON input for form fields | Ensure the JSON you provide in the "Form Fields" textarea is valid. |
| **"Data directory not found"** | Issues with creating `./data` directory | Check file system permissions for the project directory. |

### 🔒 Security Considerations

- **API Key Security**: Never hardcode API keys directly into your code. Always use environment variables or a `.env` file and ensure `.env` is in your `.gitignore`.
- **Local Data Storage**: All user data is stored locally, minimizing privacy risks associated with cloud storage. However, ensure your local machine is secure.
- **Input Validation**: The application performs basic input validation, but users should be cautious about the data they input, especially when providing form HTML.
- **LLM Interaction**: While LLMs are powerful, they can sometimes produce unexpected outputs. The system is designed to handle common LLM response formats.

## 📚 API Documentation

FormFillerBot exposes a simple RESTful API for programmatic interaction.

### 📚 Data Management Endpoints

| Method | Endpoint | Description | Request Body (Form Data) | Response (JSON) |
|---|---|---|---|---|
| `POST` | `/api/user-data` | Retrieves all stored user data. | None | `{ "success": true, "data": {...} }` |
| `POST` | `/api/update-data` | Updates specific fields in user data. | `data_updates` (JSON string), `llm_choice` (string) | `{ "success": true, "data": {...} }` |

### 🔍 Form Analysis Endpoints

| Method | Endpoint | Description | Request Body (Form Data) | Response (JSON) |
|---|---|---|---|---|
| `POST` | `/api/analyze-form` | Analyzes form fields and provides fill suggestions. | `form_fields` (JSON string), `form_html` (string, optional), `llm_choice` (string) | `{ "success": true, "field_mappings": [...] }` |

### 📝 Example API Usage (JavaScript Fetch)

```javascript
// Example: Fetch user data
fetch('/api/user-data', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
})
.then(response => response.json())
.then(data => console.log('User Data:', data))
.catch(error => console.error('Error fetching user data:', error));

// Example: Update user's email
const updateData = new FormData();
updateData.append('data_updates', JSON.stringify({
    personal_info: { email: 'new.email@example.com' }
}));
updateData.append('llm_choice', 'gemini');

fetch('/api/update-data', {
    method: 'POST',
    body: updateData
})
.then(response => response.json())
.then(result => console.log('Update Result:', result))
.catch(error => console.error('Error updating data:', error));

// Example: Analyze a form
const analyzeFormData = new FormData();
analyzeFormData.append('form_fields', JSON.stringify([
    { id: 'name', name: 'full_name', type: 'text', label: 'Your Name' },
    { id: 'email', name: 'email_address', type: 'email', label: 'Email' }
]));
analyzeFormData.append('form_html', '<form><label>Your Name</label><input type="text" name="full_name"></form>');
analyzeFormData.append('llm_choice', 'openai');

fetch('/api/analyze-form', {
    method: 'POST',
    body: analyzeFormData
})
.then(response => response.json())
.then(result => console.log('Analysis Result:', result))
.catch(error => console.error('Error analyzing form:', error));
```

## 💡 Best Practices & Tips

### ✍️ Optimizing Form Field Input

**🎯 Be Specific with Field Details:**
- Provide as much detail as possible in the `form_fields` JSON (e.g., `id`, `name`, `type`, `label`, `placeholder`). The more context the LLM has, the better the mapping.

**📚 Include Form HTML (Optional but Recommended):**
- If available, providing the full `form_html` can significantly improve the LLM's understanding of the form's structure and context, leading to more accurate suggestions.

**🔄 Handle Variations:**
- The LLM is designed to handle variations, but clear and consistent input helps. For example, if a field is "E-mail Address", ensure your `label` reflects this.

### 🎨 Data Management Strategies

**💾 Keep Your Data Up-to-Date:**
- Regularly review and update your `user_data.json` via the "Manage Data" tab to ensure the most current information is available for form filling.

**🔒 Protect Your `user_data.json`:**
- Since all your sensitive data is stored in `user_data.json`, ensure this file is protected on your local system. Avoid sharing it or storing it in insecure locations.

**🎯 Use Custom Fields for Unique Data:**
- If you frequently encounter specific fields not covered by `personal_info`, `professional`, or `education`, consider adding them to the `custom_fields` section in your `user_data.json` for future mapping.

### 🚀 Performance Optimization

**⚡ Choose the Right LLM:**
- Experiment with both Gemini and OpenAI models to see which provides better performance and accuracy for your specific use cases.
- Consider the cost implications of each API if you are making many requests.

**📊 Monitor API Usage:**
- Keep an eye on your API usage for both Gemini and OpenAI to avoid unexpected charges or hitting rate limits.

## 🔮 Future Roadmap

### 🚀 Planned Features

| Feature | Status | Description |
|---|---|---|
| **Browser Extension** | 🔄 Planned | Develop a Chrome/Firefox extension for direct, in-browser form filling. |
| **Auto-Fill Templates** | 🔄 Planned | Allow users to save and reuse specific form fill templates for recurring forms. |
| **Advanced Field Detection** | 🔄 Planned | Implement more sophisticated client-side logic for automatic form field extraction from HTML. |
| **Multi-Profile Support** | 🔄 Planned | Enable managing and switching between multiple user data profiles. |
| **Export/Import Data** | 🔄 Planned | Functionality to easily export and import `user_data.json` for backup and migration. |
| **Form History** | 🔄 Planned | Track and manage previously filled forms and their analysis results. |
| **Custom Field Mapping Rules** | 🔄 Planned | Allow users to define their own custom rules for mapping specific form fields to data. |
| **Privacy Mode Enhancements** | 🔄 Planned | Options for temporary data storage or "incognito" filling for one-time forms. |

### 🎯 Enhancement Ideas

- **AI-Powered Data Extraction**: Automatically extract data from documents (e.g., PDFs, images) to populate `user_data.json`.
- **Voice-Controlled Filling**: Integrate speech-to-text for voice commands to fill forms.
- **Integration with Password Managers**: Securely pull data from existing password managers.
- **Cross-Device Sync**: (Optional, with user consent) Encrypted synchronization of `user_data.json` across devices.
- **User Feedback Loop**: Implement a system for users to provide feedback on mapping accuracy to improve the LLM's performance over time.

## 🤝 Contributing

We welcome contributions to enhance FormFillerBot! Your ideas and code can help make this tool even more powerful and user-friendly.

### 🛠️ How to Contribute

1. **Fork the repository** on GitHub.
2. **Create a new branch** for your feature or bug fix: `git checkout -b feature/your-feature-name`.
3. **Make your changes** and ensure they adhere to the existing code style.
4. **Test your changes** thoroughly.
5. **Commit your changes** with a clear and concise message: `git commit -m 'feat: Add new feature X'`.
6. **Push your branch** to your forked repository: `git push origin feature/your-feature-name`.
7. **Open a Pull Request** to the main repository, describing your changes and their benefits.

### 🎯 Areas for Contribution

- **Frontend Improvements**: Enhance the UI/UX, add new visual components, or refine existing ones.
- **LLM Prompt Engineering**: Optimize existing prompts or create new ones for better mapping accuracy.
- **New Features**: Implement any of the planned features from the roadmap or suggest new ones.
- **Testing**: Write unit or integration tests to improve code reliability.
- **Documentation**: Improve existing documentation or add new guides.
- **Bug Fixes**: Identify and resolve any issues.

### 📋 Contribution Guidelines

- Follow the existing Python and JavaScript code style.
- Ensure all new features are accompanied by appropriate documentation updates.
- Be mindful of privacy and security best practices, especially concerning user data.
- All contributions should aim to improve the core functionality or user experience.

## 📄 License & Credits

### 📜 License

This project is part of the **#100DaysOfAI-Agents** challenge and is open-sourced under the **MIT License**. Feel free to use, modify, and distribute it.

### 🙏 Acknowledgments

- **Google Gemini API** for providing powerful AI capabilities.
- **OpenAI** for the advanced GPT-4 model integration.
- **FastAPI** for the robust and efficient web framework.
- **Jinja2** for flexible templating.
- **Tailwind CSS** for the utility-first CSS framework used in the UI.
- **All contributors** who help improve this project.

### 🌟 Inspiration

FormFillerBot was inspired by the need for a privacy-focused, AI-driven solution to automate the tedious task of filling out web forms, making digital interactions smoother and more efficient.

---

<div align="center">

## 🎉 Ready to Simplify Your Form Filling?

**Let AI handle the tedious forms, so you can focus on what matters!**

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [🎭 Examples](#-examples) • [📚 Documentation](#-documentation)

---

**Made with ❤️ for #100DaysOfAI-Agents**

*Day 99 of 100 - Building intelligent agents for a smarter future!*

</div>