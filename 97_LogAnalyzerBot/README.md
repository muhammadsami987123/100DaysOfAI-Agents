# 🔍 LogAnalyzerBot - Day 97 of #100DaysOfAI-Agents

<div align="center">

![LogAnalyzerBot Banner](https://img.shields.io/badge/LogAnalyzerBot-Day%2097-blue?style=for-the-badge&logo=files&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-AI-orange?style=for-the-badge&logo=ai&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20Framework-red?style=for-the-badge&logo=fastapi&logoColor=white)

**Transform your logs into actionable insights with AI-powered analysis**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎯 Examples](#-examples) • [📚 Documentation](#-documentation) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is LogAnalyzerBot?

LogAnalyzerBot is an intelligent AI-powered log analysis tool that transforms raw system and error logs into meaningful insights. Whether you're a developer debugging production issues, a sysadmin monitoring systems, or a DevOps engineer investigating incidents, this bot helps you quickly identify problems, patterns, and performance bottlenecks.

### 🌟 Key Highlights

- **🔍 6+ Log Formats**: Automatically detects various timestamp and log formats
- **🤖 AI-Powered Insights**: Root cause analysis and recommendations via Groq AI
- **📊 Smart Analysis**: Frequency analysis, pattern detection, error correlations
- **🎯 Advanced Filtering**: By date range, log level, keyword, and more
- **⚡ Real-time Processing**: Parses 10,000+ log lines per second
- **💾 Dual Input**: Upload files or paste content directly
- **🎨 Modern UI**: Beautiful dark-themed, responsive interface
- **🔒 Secure**: Local processing with file validation and size limits

## 🎯 Features

### 🚀 Core Functionality
- ✅ **Multi-Format Parsing**: Automatically detects 6+ log formats
- ✅ **AI Analysis**: Powered by Groq LLaMA for intelligent insights
- ✅ **Pattern Recognition**: Identifies 8+ common error patterns
- ✅ **Real-time Filtering**: Date range, log level, keyword search
- ✅ **Timeline View**: Chronological event visualization
- ✅ **Error Correlation**: Detects related errors occurring together
- ✅ **Export Ready**: Download analysis results

### 🔍 Log Parsing Capabilities
- ✅ **Timestamp Detection**: Multiple date/time formats supported
- ✅ **Log Level Extraction**: CRITICAL, ERROR, WARNING, INFO, DEBUG
- ✅ **Source Identification**: Module/service name extraction
- ✅ **Message Parsing**: Clean message content extraction
- ✅ **Format Recognition**: Bracketed, space-separated, syslog, Python logging
- ✅ **Error Handling**: Graceful handling of malformed entries

### 💻 User Interfaces
- ✅ **Modern Web UI**: Dark-themed, responsive design
- ✅ **Drag & Drop**: Easy file upload with visual feedback
- ✅ **Paste Content**: Direct log content input
- ✅ **Interactive Filters**: Real-time analysis configuration
- ✅ **Mobile Responsive**: Works on all device sizes

### 📊 Analysis Features
- ✅ **Statistical Summary**: Total entries, errors, warnings, critical issues
- ✅ **Frequency Analysis**: Log level and source distribution
- ✅ **Error Patterns**: Common error identification and counting
- ✅ **Known Issues**: Pre-configured pattern matching with solutions
- ✅ **Hourly Distribution**: Time-based event clustering
- ✅ **Affected Modules**: Most problematic components identified

### 🎨 AI-Powered Features
- ✅ **Root Cause Analysis**: AI identifies likely causes of issues
- ✅ **Actionable Recommendations**: Specific steps to resolve problems
- ✅ **Pattern Observations**: Trend detection and insights
- ✅ **Preventive Measures**: How to avoid future occurrences
- ✅ **Error Explanations**: Detailed explanations for specific errors

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.8+** installed on your system
- **Groq API Key** (get one free from [Groq Console](https://console.groq.com))
- **Internet connection** for AI analysis

### ⚡ Installation

```bash
# 1. Navigate to project directory
cd 97_LogAnalyzerBot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API key (create .env file)
echo GROQ_API_KEY=your_api_key_here > .env

# That's it! Ready to run.
```

### 🎯 First Run

```bash
# Start the web interface
python main.py web

# Open your browser to:
# http://localhost:8000
```

### 🧪 Test with Sample Logs

```bash
# The project includes sample logs in test/sample_logs.log
# 1. Start the application
python main.py web

# 2. Upload the sample file through the web interface
# 3. Click "Analyze Logs" 
# 4. Review AI-powered insights!
```

## 🎯 Examples & Usage

### 🌐 Web Interface

The web interface provides a beautiful, interactive experience:

1. **📤 Upload Logs**: Drag & drop files or paste content
2. **🔧 Configure Filters**: Set date range, log levels, keywords
3. **🚀 Analyze**: Click "Analyze Logs" and get instant results
4. **📊 Review Results**: Statistics, patterns, timeline, AI insights
5. **💡 Take Action**: Follow recommendations to resolve issues

**🎯 Pro Tips:**
- Start with ERROR and CRITICAL levels for quick debugging
- Use keyword filter to focus on specific components
- Enable AI insights for detailed root cause analysis
- Check the timeline to understand event sequences

### 📁 Supported Log Formats

LogAnalyzerBot automatically detects various log formats:

**Format 1: Bracketed Timestamp**
```
[2025-01-15 10:30:45] ERROR [db_handler] Connection timeout
```

**Format 2: Space-Separated**
```
2025-01-15 10:30:45 ERROR auth_service: Failed login attempt
```

**Format 3: Python Logging**
```
2025-01-15 10:30:45,123 ERROR module_name - Error message
```

**Format 4: Syslog Format**
```
Jan 15 10:30:45 hostname service: message
```

**Format 5: Simple Level Format**
```
ERROR: [module] message content
```

**Format 6: Generic**
```
ERROR Something went wrong
```

### 🔎 Analysis Example

**Input Log:**
```
[2025-01-15 10:30:45] ERROR [db_handler] Connection timeout after 30s
[2025-01-15 10:31:12] ERROR [db_handler] Connection timeout after 30s
[2025-01-15 10:31:35] ERROR [db_handler] Connection timeout after 30s
[2025-01-15 10:32:25] ERROR [cache_manager] Redis connection refused
[2025-01-15 10:33:50] CRITICAL [ssl_handler] SSL certificate will expire in 3 days
```

**Output Analysis:**
```
📊 SUMMARY STATISTICS
├── Total Entries: 5
├── Errors: 4
├── Warnings: 0
└── Critical: 1

⚠️ IDENTIFIED ISSUES
├── Database Connection Timeout (3 occurrences)
│   💡 Check connection pool settings and increase timeout values
└── SSL Certificate Expiring (1 occurrence)
    💡 Renew certificate before expiration date

⏱️ EVENT TIMELINE
├── 10:30:45 - ERROR - db_handler: Connection timeout
├── 10:31:12 - ERROR - db_handler: Connection timeout
├── 10:31:35 - ERROR - db_handler: Connection timeout
└── 10:33:50 - CRITICAL - ssl_handler: Certificate expiring

🤖 AI INSIGHTS
The repeated database timeout errors suggest a connection pool
exhaustion issue. The pattern shows errors occurring every 30-40
seconds, indicating retry attempts. Recommendations:
1. Increase connection pool size to 50
2. Implement connection retry logic with exponential backoff
3. Monitor database server resource usage
4. Renew SSL certificate immediately to avoid service disruption
```

## 🎭 Analysis Capabilities

### 📚 Detected Error Patterns

| Pattern | Keywords | Common Causes | Recommendation |
|---------|----------|---------------|----------------|
| **🔌 Connection Timeout** | timeout, connection, timed out | Network issues, pool exhaustion | Check network, increase timeouts |
| **💾 Database Errors** | database, sql, query, deadlock | DB overload, bad queries | Optimize queries, check pool |
| **💥 Memory Issues** | outofmemory, memory, heap, oom | Memory leaks, insufficient RAM | Increase memory, fix leaks |
| **🔒 Permission Denied** | permission denied, access denied | File/directory permissions | Check permissions, user rights |
| **📁 File Not Found** | file not found, no such file | Missing files, wrong paths | Verify paths, check deployment |
| **⚠️ Null Pointer** | nullpointer, null reference | Uninitialized variables | Add null checks, initialization |
| **🌐 API Errors** | api, 400, 401, 403, 404, 500 | Endpoint issues, auth problems | Check endpoints, verify tokens |
| **🔐 SSL/Certificate** | ssl, certificate, tls, handshake | Expired/invalid certificates | Update certificates, check chain |

### 🎨 Log Levels

| Level | Description | Color Code | Use Case |
|-------|-------------|------------|----------|
| **🔴 CRITICAL** | System-breaking errors | Red | Immediate attention required |
| **❌ ERROR** | Application errors | Red | Functionality broken |
| **⚠️ WARNING** | Potential problems | Yellow | Should be investigated |
| **ℹ️ INFO** | Informational messages | Blue | Normal operations |
| **🐛 DEBUG** | Debug information | Gray | Development/troubleshooting |

### 📏 Analysis Metrics

| Metric | Description | What It Tells You |
|--------|-------------|-------------------|
| **Total Entries** | All parsed log lines | Volume of logging activity |
| **Error Count** | Number of ERROR level logs | Application health indicator |
| **Warning Count** | Number of WARNING level logs | Potential issues to investigate |
| **Critical Count** | Number of CRITICAL level logs | Severe problems requiring immediate action |
| **Most Frequent Error** | Most repeated error message | Primary issue to address |
| **Affected Modules** | Components with errors | Where problems are concentrated |
| **Hourly Distribution** | Events per hour | When problems occur most |
| **Error Correlations** | Related errors in time | Cascading failure patterns |

## 🏗️ Project Architecture

### 📁 File Structure

```
97_LogAnalyzerBot/
├── 📄 main.py                   # Main entry point
├── ⚙️ config.py                 # Configuration and settings
├── 🤖 agent.py                  # Core AI log analysis logic
├── 🌐 web_app.py                # FastAPI web application
├── 📋 requirements.txt          # Python dependencies
├── 📚 prompts/                  # AI prompt templates
│   ├── analysis_prompt.txt     # Main analysis prompt
│   └── error_explanation_prompt.txt  # Error explanation prompt
├── 🛠️ utils/                    # Utility modules
│   ├── log_parser.py           # Multi-format log parser
│   └── pattern_matcher.py      # Pattern recognition engine
├── 🎨 static/                   # Frontend assets
│   ├── style.css               # Modern dark theme CSS
│   └── script.js               # Interactive JavaScript
├── 📄 templates/                # HTML templates
│   └── index.html              # Main web interface
├── 🧪 test/                     # Test files
│   ├── __init__.py
│   └── sample_logs.log         # Sample log data (40 entries)
├── 📁 uploads/                  # Uploaded files (auto-created)
├── 📁 outputs/                  # Analysis outputs (auto-created)
├── 🖼️ Images/                   # Documentation images
├── 📄 README.md                # This documentation
└── 🔒 .gitignore               # Git ignore rules
```

### 🔧 Technical Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Python 3.8+ | Core application logic |
| **AI Engine** | Groq AI (LLaMA 3.3) | Log analysis and insights |
| **Web Framework** | FastAPI | REST API and web server |
| **Template Engine** | Jinja2 | HTML template rendering |
| **Frontend** | Vanilla JavaScript | Interactive UI |
| **Styling** | CSS3 + Animations | Dark theme, responsive design |
| **Parsing** | Regex + datetime | Log format detection |
| **Server** | Uvicorn | ASGI web server |

### 🎯 Key Components

#### 🤖 LogAnalyzerBot (`agent.py`)
- **Core AI Logic**: Handles Groq API integration
- **Log Processing**: Loads and filters log entries
- **Analysis Coordination**: Manages parsing and pattern matching
- **AI Insights**: Generates root cause analysis and recommendations
- **Error Explanation**: Provides detailed explanations for specific errors

#### 🔍 Log Parser (`utils/log_parser.py`)
- **Format Detection**: Recognizes 6+ log formats automatically
- **Timestamp Parsing**: Handles multiple date/time formats
- **Log Level Extraction**: Identifies severity levels
- **Source Identification**: Extracts module/service names
- **Message Parsing**: Cleans and extracts message content

#### 🎯 Pattern Matcher (`utils/pattern_matcher.py`)
- **Error Patterns**: Detects common error types
- **Frequency Analysis**: Counts log levels, sources, hourly distribution
- **Known Issues**: Matches against pre-configured patterns
- **Correlations**: Finds related errors in time windows
- **Suggestions**: Provides solutions for detected patterns

#### 🌐 Web Application (`web_app.py`)
- **REST API**: 5 endpoints for all operations
- **File Upload**: Handles file uploads with validation
- **Content Analysis**: Processes pasted log content
- **Filtering**: Applies user-defined filters
- **AI Integration**: Requests AI insights when enabled

#### 🎨 Frontend (`static/`)
- **Interactive UI**: Modern, responsive interface
- **Real-time Updates**: Live progress indicators
- **Visual Feedback**: Animations and status messages
- **Drag & Drop**: Easy file upload
- **Responsive Design**: Works on all devices

## ⚙️ Configuration & Setup

### 🔑 API Key Setup

**Step 1: Get Groq API Key**
1. Visit [Groq Console](https://console.groq.com)
2. Sign up or log in to your account
3. Navigate to "API Keys" section
4. Create a new API key
5. Copy the key (starts with `gsk_`)

**Step 2: Configure the Key**

```bash
# Option 1: .env File (Recommended)
echo GROQ_API_KEY=gsk_your_actual_api_key_here > .env
echo MODEL_NAME=llama-3.3-70b-versatile >> .env

# Option 2: Environment Variable
# Windows PowerShell
$env:GROQ_API_KEY="gsk_your_api_key_here"

# Linux/Mac
export GROQ_API_KEY="gsk_your_api_key_here"
```

### 🎛️ Advanced Configuration

Edit `config.py` to customize the application:

```python
# API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

# Application Settings
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'.log', '.txt', '.json'}

# Log Parsing Configuration
LOG_LEVELS = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE']
MIN_PATTERN_FREQUENCY = 2  # Minimum occurrences to identify as pattern

# Analysis Settings
MAX_SUGGESTIONS = 5  # Maximum number of suggestions to provide
```

### 🎨 Custom Pattern Configuration

Add custom error patterns in `utils/pattern_matcher.py`:

```python
self.known_patterns['your_pattern'] = {
    'keywords': ['your', 'error', 'keywords'],
    'suggestion': 'Your custom solution here'
}
```

### 🔧 Custom Log Format

Add custom log formats in `utils/log_parser.py`:

```python
# Add to self.patterns list in LogParser.__init__
re.compile(r'your_custom_regex_pattern_here')
```

## 🔌 API Documentation

### 📚 Core Endpoints

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `POST` | `/api/upload` | Upload log file | `file: <file>` | `{success, total_entries, message}` |
| `POST` | `/api/analyze-content` | Analyze pasted content | `content: <string>` | `{success, total_entries, message}` |
| `POST` | `/api/analyze` | Perform analysis | `start_date, end_date, log_levels, keyword, include_ai` | `{...analysis_results}` |
| `POST` | `/api/explain-error` | Get AI error explanation | `error_message, log_level, source, frequency` | `{success, explanation}` |
| `GET` | `/api/status` | Get application status | - | `{loaded, total_entries, api_available}` |

### 📝 Example API Usage

```javascript
// Upload a file
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const response = await fetch('/api/upload', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log(`Parsed ${result.total_entries} entries`);
```

```python
# Python API usage
import requests

# Analyze logs with filters
response = requests.post('http://localhost:8000/api/analyze', data={
    'start_date': '2025-01-15T00:00:00',
    'end_date': '2025-01-15T23:59:59',
    'log_levels': 'ERROR,CRITICAL',
    'keyword': 'database',
    'include_ai': True
})

analysis = response.json()
print(f"Total errors: {analysis['total_errors']}")
print(f"AI Insights: {analysis['ai_insights']}")
```

## 💡 Best Practices & Tips

### ✍️ Effective Log Analysis

**🎯 Start with High-Severity Issues:**
- ❌ **Don't**: Analyze all log levels at once
- ✅ **Do**: Filter for CRITICAL and ERROR first

**🔍 Use Time-Based Filtering:**
- ❌ **Don't**: Analyze months of logs together
- ✅ **Do**: Focus on specific incident timeframes

**🎯 Leverage Keywords:**
- ❌ **Don't**: Browse through all errors manually
- ✅ **Do**: Search for specific components or error types

**💡 Enable AI Insights:**
- ❌ **Don't**: Skip AI analysis for complex issues
- ✅ **Do**: Use AI for root cause analysis and recommendations

### 🎨 Optimization Strategies

**⚡ Faster Analysis:**
- Filter by date range to reduce log volume
- Focus on specific log levels
- Use keyword search for targeted analysis

**💾 Better Organization:**
- Upload files with descriptive names
- Document incident contexts
- Save analysis results for future reference

**🎯 Quality Improvement:**
- Compare patterns across time periods
- Track recurring issues
- Monitor affected modules over time

### 🔒 Security Best Practices

**🔑 API Key Management:**
- Never commit API keys to version control
- Use environment variables or .env files
- Rotate keys periodically

**📁 File Handling:**
- Validate file types and sizes
- Scan for malicious content
- Use secure file storage

**🔐 Data Privacy:**
- Review logs for sensitive information
- Use local processing when possible
- Implement access controls

## 🧪 Testing & Quality Assurance

### 🔍 Testing with Sample Logs

```bash
# The project includes comprehensive sample logs
# Location: test/sample_logs.log

# Test scenarios included:
# ✅ Database connection timeouts
# ✅ Redis connection failures
# ✅ Failed authentication attempts
# ✅ SSL certificate warnings
# ✅ API gateway errors
# ✅ Memory issues
# ✅ Permission denied errors
```

### 📊 Expected Performance

**Performance Metrics:**
- **Parsing Speed**: ~10,000 log lines per second
- **Memory Usage**: ~100MB for 100K log entries
- **Analysis Time**: 1-5 seconds for most files
- **AI Insights**: 3-10 seconds (depends on Groq API)
- **Web Interface Load**: <1 second
- **API Response Time**: <100ms for most operations

### 🐛 Troubleshooting

**Common Issues & Solutions:**

| Issue | Cause | Solution |
|-------|-------|----------|
| **"AI insights unavailable"** | Missing API key | Set `GROQ_API_KEY` in .env file |
| **"Failed to parse log file"** | Unsupported format | Try paste option, check format |
| **"File too large"** | Exceeds 10MB limit | Split file or adjust `MAX_FILE_SIZE` |
| **"No patterns detected"** | Insufficient data | Use larger log file or adjust `MIN_PATTERN_FREQUENCY` |
| **"Port 8000 already in use"** | Port occupied | Change port in `web_app.py` |

## 🔮 Use Cases

### 💻 Development & Debugging
- **Debug Application Errors**: Quickly identify bugs in development
- **Test Log Analysis**: Validate logging implementation
- **Error Pattern Recognition**: Learn from recurring issues

### 🚀 Production Monitoring
- **Incident Investigation**: Analyze production logs during incidents
- **Error Tracking**: Monitor error rates and patterns
- **Performance Issues**: Identify bottlenecks and slow operations

### 🛡️ DevOps & SRE
- **System Health**: Monitor application and system health
- **Alert Investigation**: Deep-dive into triggered alerts
- **Post-Mortem Analysis**: Review incidents after resolution

### 🔒 Security & Compliance
- **Security Audits**: Review access and authentication logs
- **Intrusion Detection**: Identify suspicious activities
- **Compliance Reporting**: Generate audit reports

## 🔮 Future Roadmap

### 🚀 Planned Features

| Feature | Status | Description |
|---------|--------|-------------|
| **Real-time Streaming** | 🔄 Planned | Monitor logs in real-time |
| **Advanced Visualizations** | 🔄 Planned | Charts and graphs for trends |
| **Custom Alert Rules** | 🔄 Planned | Set up automated alerts |
| **Report Export** | 🔄 Planned | PDF and CSV export options |
| **Multi-file Analysis** | 🔄 Planned | Analyze multiple log files together |
| **Machine Learning** | 🔄 Planned | Anomaly detection with ML |
| **Integration APIs** | 🔄 Planned | Connect with ELK, Splunk, etc. |
| **Team Collaboration** | 🔄 Planned | Share analyses with team |

### 🎯 Enhancement Ideas

- **Dashboard View**: Comprehensive analytics dashboard
- **Custom Filters**: Save and reuse filter configurations
- **Historical Comparison**: Compare logs across time periods
- **Automated Reports**: Schedule regular analysis reports
- **Webhook Notifications**: Real-time alerts via webhooks
- **Log Aggregation**: Pull logs from multiple sources
- **Pattern Learning**: Learn from user feedback
- **API Rate Limiting**: Implement usage quotas

## 🤝 Contributing

We welcome contributions to make LogAnalyzerBot even better!

### 🛠️ How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and test thoroughly
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### 🎯 Areas for Contribution

- **New Log Formats**: Add support for additional formats
- **Error Patterns**: Add more pre-configured patterns
- **UI Improvements**: Enhance user interface and UX
- **Performance**: Optimize parsing and analysis speed
- **Documentation**: Improve guides and examples
- **Testing**: Add more test cases and scenarios
- **Bug Fixes**: Report and fix issues

### 📋 Contribution Guidelines

- Follow existing code style and conventions
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass
- Be respectful and constructive

## 📞 Support & Community

### 🆘 Getting Help

1. **📖 Documentation**: Review this README thoroughly
2. **🧪 Sample Logs**: Test with provided samples first
3. **🔍 Troubleshooting**: Check the troubleshooting section
4. **📊 Console Logs**: Check browser/terminal for errors
5. **🌐 API Status**: Verify Groq API is operational

### 🐛 Reporting Issues

When reporting issues, please include:
- **System Information**: OS, Python version, browser
- **Error Messages**: Full error output and stack traces
- **Steps to Reproduce**: Detailed reproduction steps
- **Expected vs Actual**: What you expected vs what happened
- **Log Sample**: Anonymized sample of logs causing issues

### 💬 Community

- **GitHub Issues**: Report bugs and request features
- **Discussions**: Ask questions and share ideas
- **Showcase**: Share your use cases and success stories!

## 📄 License & Credits

### 📜 License

This project is part of the **#100DaysOfAI-Agents** challenge.

**MIT License** - Feel free to use, modify, and distribute!

### 🙏 Acknowledgments

- **Groq** for providing fast AI inference
- **FastAPI** team for the excellent web framework
- **Python community** for amazing libraries
- **All contributors** who help improve this project

### 🌟 Inspiration

This project was inspired by the need for intelligent log analysis tools that are:
- **Accessible**: Easy to use for everyone
- **Powerful**: Capable of deep analysis with AI
- **Practical**: Provides actionable insights
- **Fast**: Real-time analysis and feedback

---

<div align="center">

## 🎉 Ready to Analyze Your Logs?

**Transform your logs into actionable insights with the power of AI!**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎯 Examples](#-examples) • [📚 Documentation](#-documentation)

---

**Made with ❤️ by the #100DaysOfAI-Agents community**

*Day 97 of 100 - Building the future of AI agents, one day at a time!*

</div>
