# 📊 CSVAnalyzerBot - Day 81 of #100DaysOfAI-Agents

<div align="center">

![CSVAnalyzerBot Banner](https://img.shields.io/badge/CSVAnalyzerBot-Day%2081-blue?style=for-the-badge&logo=microsoftexcel&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-green?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20Framework-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![AI Models](https://img.shields.io/badge/AI-Gemini%202.0%20Flash%20%7C%20OpenAI%20GPT--4o--mini-orange?style=for-the-badge&logo=google&logoColor=white)

**Analyze your CSV files with natural language and get smart insights and visualizations!**

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [💻 Web Interface](#-web-interface) • [🔌 API](#-api) • [⚙️ Configuration](#%EF%B8%8F-configuration) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is CSVAnalyzerBot?

CSVAnalyzerBot is an intelligent AI-powered agent that enables users to upload a CSV file and interact with their data using natural language. It provides insightful responses, data summaries, and even suggests relevant charts to visualize the data, making data analysis accessible and intuitive.

### 🌟 Key Highlights

- **Natural Language Queries**: Ask questions about your CSV data in plain English.
- **AI-Powered Insights**: Get smart summaries, statistical information, and data extractions powered by Gemini 2.0 Flash or OpenAI GPT-4o-mini.
- **Dynamic Chart Suggestions**: The AI suggests appropriate chart types (e.g., bar, line, scatter) and the columns to visualize.
- **Interactive Web Interface**: A user-friendly chat-like interface for seamless interaction and file uploads.
- **Downloadable Summaries**: Option to download a comprehensive summary of the analyzed data.

---

## 🎯 Features

### 🚀 Core Functionality
- ✅ **CSV File Upload**: Easily upload your CSV datasets.
- ✅ **Natural Language Processing**: Understands and responds to user questions about the data.
- ✅ **Data Analysis**: Performs basic statistical analysis, aggregation, and data retrieval using `pandas`.
- ✅ **AI Integration**: Leverages Gemini 2.0 Flash (default) or OpenAI GPT-4o-mini for intelligent responses.
- ✅ **Chart Recommendations**: Provides suggestions for data visualizations.
- ✅ **Download Options**: Download generated summaries.

### 💻 Web Interface (Frontend)
- ✅ **Intuitive Design**: Clean and responsive HTML + TailwindCSS interface.
- ✅ **File Upload Component**: Simple drag-and-drop or click-to-upload for CSV files.
- ✅ **Chat-like Interaction**: Familiar chat bubbles for user questions and bot responses.
- ✅ **Dynamic Content Display**: Shows AI responses, and potentially rendered charts.
- ✅ **LLM Toggle**: Switch between Gemini and OpenAI models.

---

## 🚀 Quick Start

### 📋 Prerequisites

- Python 3.9+
- Gemini API Key (from [Google AI Studio](https://aistudio.google.com/app/apikey)) OR OpenAI API Key (from [OpenAI Platform](https://platform.openai.com/api-keys))

### ⚡ Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd 81_CsvAnalyzerBot
   ```

2. **Create a virtual environment and activate it:**
   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory (`81_CsvAnalyzerBot/`) with your API keys and configuration:
   ```env
   # Choose your preferred LLM model: "gemini" or "openai"
   LLM_MODEL=gemini

   # Gemini Configuration
   GEMINI_API_KEY=your_gemini_api_key_here

   # OpenAI Configuration
   OPENAI_API_KEY=your_openai_api_key_here

   # Server Configuration
   DEBUG=True
   HOST=0.0.0.0
   PORT=8000
   ```
   Replace `your_gemini_api_key_here` and `your_openai_api_key_here` with your actual API keys. If you only want to use one, you can leave the other blank, but set `LLM_MODEL` accordingly.

### 🎯 Run the Application

```bash
# From the 81_CsvAnalyzerBot/ directory
python -m uvicorn backend.main:app --reload
```

Open your browser and navigate to `http://localhost:8000`.

### 🧪 Verify Installation

```bash
# Run the test suite (you might need to create this test_installation.py file)
python test_installation.py

# Expected output:
# ✅ Python version compatible
# ✅ All dependencies installed
# ✅ Configuration loaded
# ✅ CSV processor initialized
# ✅ Web app ready
```

---

## 💻 Web Interface

The web interface provides a beautiful, interactive experience for data analysis:

1.  **📊 Upload Your CSV**: Easily upload your `.csv` files using drag-and-drop or click-to-upload.
2.  **💬 Ask Questions**: Interact with your data using natural language in the chat window.
3.  **💡 Get Insights**: Receive smart summaries, statistical information, and data extractions.
4.  **📈 View Charts**: See AI-suggested charts to visualize your data.
5.  **⬇️ Download Summary**: Download a comprehensive summary of the analyzed data.

**🎯 Pro Tips:**
- Use clear and specific questions for better results.
- Experiment with different types of questions (e.g., "What is the average age?", "Show me a chart of sales by region").
- Toggle between Gemini and OpenAI models in the navigation bar to compare responses.

### 📝 Example Usage

```
# Example Question 1:
"What is the average price of products?"

# Expected AI Response:
"The average price of products is $X.XX."

# Example Question 2:
"Show me a bar chart of sales by category."

# Expected AI Response:
"Here is a bar chart showing sales by category. [Chart Image/URL]"
```

---

## 🔌 API

### Endpoints

- **`POST /uploadfile/`**
  - **Description**: Upload a CSV file.
  - **Request Body**: `file: UploadFile` (the CSV file).
  - **Response**: `{ "message": "...", "filename": "...", "file_id": "..." }`

- **`POST /analyze/`**
  - **Description**: Send a natural language question for data analysis.
  - **Request Body**: `{ "question": "string", "file_id": "string" }`
  - **Response**: `{ "response": "string", "chart_suggestion": { "type": "string", "x": "string", "y": "string", "color": "string" | null } | null, "chart_url": "string" | null }`

- **`GET /charts/{filename}`**
  - **Description**: Retrieve a generated chart image.
  - **Response**: `FileResponse` (image file).

- **`GET /download-summary/?file_id={file_id}`**
  - **Description**: Download a text summary of the uploaded CSV.
  - **Response**: `FileResponse` (text file).

---

## ⚙️ Configuration

All configurations are managed via the `.env` file and `backend/config.py`.

- `LLM_MODEL`: Specifies the preferred LLM (`gemini` or `openai`).
- `GEMINI_API_KEY`: Your Google Gemini API key.
- `OPENAI_API_KEY`: Your OpenAI API key.
- `DEBUG`: Set to `True` for development, `False` for production.
- `HOST`: The host address for the FastAPI application (default: `0.0.0.0`).
- `PORT`: The port for the FastAPI application (default: `8000`).

### 🔑 API Key Setup

**Step 1: Get API Keys**
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey) to get your Gemini API Key.
2. Visit [OpenAI Platform](https://platform.openai.com/api-keys) to get your OpenAI API Key.
3. Sign up or log in to your accounts and create new API keys.

**Step 2: Configure the Keys**

```bash
# Create a .env file in the root directory (81_CsvAnalyzerBot/)
echo LLM_MODEL=gemini > .env
echo GEMINI_API_KEY=your_gemini_api_key_here >> .env
echo OPENAI_API_KEY=your_openai_api_key_here >> .env
echo DEBUG=True >> .env
echo HOST=0.0.0.0 >> .env
echo PORT=8000 >> .env
```
Replace `your_gemini_api_key_here` and `your_openai_api_key_here` with your actual API keys. If you only want to use one, you can leave the other blank, but set `LLM_MODEL` accordingly.

### 🎛️ Advanced Configuration

Edit `backend/config.py` to customize the application:

```python
# API Settings
LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini") # "gemini" or "openai"
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

# Server Settings
DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", "8000"))

# Directory Settings
UPLOAD_DIR: str = "uploads"
CHART_DIR: str = "charts"
SUMMARY_DIR: str = "summaries"
```

---

## 🏗️ Project Structure

```
81_CsvAnalyzerBot/
├── backend/
│   ├── agent.py               # LLM logic for data analysis and chart suggestions
│   ├── config.py              # Configuration settings for API keys, paths, etc.
│   ├── csv_processor.py       # Handles CSV loading, parsing, and data manipulation with pandas
│   └── main.py                # FastAPI application entry point, routes, and main logic
├── frontend/
│   ├── index.html             # Main web interface (HTML, TailwindCSS, JavaScript)
│   └── static/                # Static assets for the frontend (e.g., app.js, main.css - if added)
├── uploads/                   # Directory to store uploaded CSV files
├── charts/                    # Directory to store generated chart images
├── requirements.txt           # Python dependencies
├── .env.example               # Example environment variables file
└── README.md                  # Project documentation
```

---

## 🧪 Testing & Quality Assurance

### 🔍 Installation Testing

Run the comprehensive test suite to verify everything is working:

```bash
python test_installation.py
```

**Test Coverage:**
- ✅ **Python Version**: Compatibility check (3.9+)
- ✅ **Dependencies**: All required packages installed
- ✅ **File Structure**: All necessary files present (e.g., `backend/`, `frontend/`, `uploads/`, `charts/`)
- ✅ **Configuration**: Settings loaded correctly from `.env` and `config.py`
- ✅ **API Integration**: Test connection to selected LLM (Gemini or OpenAI)
- ✅ **CSV Processor**: Core functionality test (e.g., loading CSV, basic analysis)
- ✅ **Web App**: FastAPI application test (e.g., endpoint accessibility)
- ✅ **File System**: Directory creation and permissions for `uploads/` and `charts/`

### 🚀 Performance Testing

```bash
# Test data processing and API response speed (example, actual implementation might vary)
python -c ""
# ... (add Python code to test performance, similar to 36_StoryWriterAgent)
# Example: Measure time to upload, analyze, and generate a chart for a sample CSV
"""

### 🐛 Troubleshooting

**Common Issues & Solutions:**

| Issue | Cause | Solution |
|-------|-------|----------|
| **"API key not found"** | Missing or invalid API key | Set `GEMINI_API_KEY` or `OPENAI_API_KEY` environment variable |
| **"Failed to analyze CSV"** | LLM API quota exceeded or network issue | Check API key credits and internet connection |
| **"Module not found"** | Missing dependencies | Run `pip install -r requirements.txt` |
| **"Port already in use"** | Port 8000 is occupied | Change `PORT` in `.env` or kill the process using the port |
| **"Permission denied"** | File system permissions | Run with appropriate permissions or change directory |

### 📊 Performance Metrics

**Expected Performance:**
- **CSV Upload & Initial Summary**: < 1 second (for small to medium files)
- **Data Analysis & Chart Suggestion**: 2-5 seconds (depending on LLM response time and data complexity)
- **Web Interface Load**: <1 second
- **API Response Time**: <200ms for most operations (excluding LLM calls)
- **Memory Usage**: <100MB typical (can vary with large CSVs)
- **Concurrent Users**: Supports 5+ simultaneous users

### 🔒 Security Considerations

- **API Key Security**: Never commit API keys to version control. Use `.env` file.
- **File Upload Security**: Implement robust validation for uploaded CSV files to prevent malicious content.
- **Local Storage**: Uploaded CSVs and generated charts are stored locally.
- **Input Validation**: All user inputs (natural language queries) are sanitized before processing.
- **Error Handling**: Sensitive information is not exposed in error messages.

---

## 🔌 API Documentation

### 📚 Core Endpoints

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `POST` | `/uploadfile/` | Upload a CSV file | `file: UploadFile` | `{ "message", "filename", "file_id" }` |
| `POST` | `/analyze/` | Analyze data with natural language | `{ "question", "file_id" }` | `{ "response", "chart_suggestion", "chart_url" }` |
| `GET` | `/charts/{filename}` | Retrieve a generated chart image | - | `FileResponse` (image file) |
| `GET` | `/download-summary/?file_id={file_id}` | Download a text summary | - | `FileResponse` (text file) |

### 📝 Example API Usage

```python
import requests

BASE_URL = "http://localhost:8000"

# Example 1: Upload a CSV file
with open("sample.csv", "rb") as f:
    files = { "file": ("sample.csv", f, "text/csv") }
    response = requests.post(f"{BASE_URL}/uploadfile/", files=files)
    upload_result = response.json()
    print(f"Upload Result: {upload_result}")
    file_id = upload_result.get("file_id")

# Example 2: Analyze the uploaded CSV
if file_id:
    question = "What are the top 5 most expensive products?"
    response = requests.post(f"{BASE_URL}/analyze/", json={ "question": question, "file_id": file_id })
    analysis_result = response.json()
    print(f"Analysis Result: {analysis_result}")

# Example 3: Download a summary (if applicable)
if file_id:
    response = requests.get(f"{BASE_URL}/download-summary/?file_id={file_id}")
    if response.status_code == 200:
        with open(f"summary_{file_id}.txt", "wb") as f:
            f.write(response.content)
        print(f"Summary downloaded as summary_{file_id}.txt")
```

---

## 💡 Best Practices & Tips

### ✍️ Writing Effective Queries

**🎯 Be Specific and Detailed:**
- ❌ **Vague**: "Analyze data"
- ✅ **Specific**: "What is the average sales revenue per quarter?"

**📊 Include Desired Output:**
- ❌ **Generic**: "Tell me about products"
- ✅ **Targeted**: "Show me the distribution of product categories in a pie chart."

**📈 Experiment with Chart Types:**
- Request specific chart types (e.g., "bar chart", "line graph", "scatter plot") when appropriate.

### 🚀 Performance Optimization

**⚡ Faster Processing:**
- For very large CSVs, consider pre-processing or sampling data if full precision isn't critical.
- Ensure your API keys have sufficient quota to avoid rate limiting.

**💾 Better Organization:**
- Keep your `uploads/` and `charts/` directories clean by periodically removing old files.

### 🔒 Security Best Practices

- **API Key Management**: Use environment variables for API keys and never hardcode them.
- **Input Sanitization**: Always validate and sanitize user inputs to prevent injection attacks.
- **Access Control**: If deploying, ensure appropriate authentication and authorization are in place.

---

## 🔮 Future Roadmap

### 🚀 Planned Features

| Feature | Status | Description |
|---------|--------|-------------|
| **Advanced Charting** | 🔄 Planned | Support for more complex chart types and customizations |
| **Data Cleaning** | 🔄 Planned | AI-assisted data cleaning and pre-processing suggestions |
| **Predictive Analytics** | 🔄 Planned | Basic forecasting and predictive modeling capabilities |
| **Multiple File Analysis** | 🔄 Planned | Ability to analyze and compare insights from multiple CSVs |
| **User Accounts** | 🔄 Planned | Secure user authentication and personal data dashboards |
| **Export Formats** | 🔄 Planned | Export charts and summaries in various formats (e.g., PDF, Excel) |

### 🎯 Enhancement Ideas

- **Interactive Dashboards**: Dynamic dashboards for deeper data exploration.
- **Machine Learning Integration**: Integrate with popular ML libraries for advanced analysis.
- **Real-time Data Streams**: Connect to live data sources for continuous analysis.
- **Version Control for Data**: Track changes and versions of uploaded CSV files.
- **Mobile Responsiveness**: Optimize the web interface for mobile devices.

---

## 🤝 Contributing

We welcome contributions to make CSVAnalyzerBot even better!

### 🛠️ How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes** and test thoroughly
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/your-feature-name`
6. **Open a Pull Request**

### 🎯 Areas for Contribution

- **New Features**: Implement planned features or suggest new ones.
- **UI Improvements**: Enhance the user interface and experience.
- **Performance**: Optimize data processing and API response times.
- **Documentation**: Improve guides and examples.
- **Testing**: Add more test cases.
- **Bug Fixes**: Report and fix issues.

### 📋 Contribution Guidelines

- Follow the existing code style.
- Add tests for new features.
- Update documentation as needed.
- Ensure all tests pass.
- Be respectful and constructive.

---

## 📞 Support & Community

### 🆘 Getting Help

1. **📖 Documentation**: Check this README for comprehensive guides.
2. **🧪 Test Suite**: Run `python test_installation.py` to verify your setup.
3. **🔍 Troubleshooting**: Review the troubleshooting section for common issues.
4. **📊 Logs**: Check console output for error messages.
5. **🌐 API Status**: Verify Gemini/OpenAI API is operational.

### 🐛 Reporting Issues

When reporting issues, please include:
- **System Information**: OS, Python version, browser, LLM used.
- **Error Messages**: Full error output or relevant logs.
- **Steps to Reproduce**: What you were doing when it happened.
- **Expected vs Actual**: What you expected vs what happened.

### 💬 Community

- **GitHub Issues**: Report bugs and request features.
- **Discussions**: Ask questions, share ideas, and connect with other users.
- **Showcase**: Share your interesting data analyses and insights!

---

## 📄 License & Credits

### 📜 License

This project is part of the **#100DaysOfAI-Agents** challenge by **Muhammad Sami Asghar Mughal**.

**MIT License** - Feel free to use, modify, and distribute!

### 🙏 Acknowledgments

- **Google Gemini** and **OpenAI** for powerful LLM APIs.
- **FastAPI** team for the excellent web framework.
- **Pandas** for efficient data handling.
- **TailwindCSS** for streamlined styling.
- **All contributors** who help improve this project.

### 🌟 Inspiration

This project was inspired by the growing need for accessible and intelligent data analysis tools that empower users to derive insights from their data using natural language.

---

<div align="center">

## 🎉 Ready to Analyze Your Data?

**Transform your CSV files into actionable insights with the power of AI!**

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [💻 Web Interface](#-web-interface) • [🔌 API](#-api)

---

**Made with ❤️ by the #100DaysOfAI-Agents community**

*Day 81 of 100 - Building the future of AI Agents, one day at a time!*

</div>
