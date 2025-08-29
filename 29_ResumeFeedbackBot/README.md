# 🤖 ResumeFeedbackBot - AI-Powered Resume & Portfolio Review

A modern, responsive web application that provides AI-powered analysis and feedback for resumes and portfolios. Features a beautiful floating chatbot interface and comprehensive career guidance.

![ResumeFeedbackBot](https://img.shields.io/badge/ResumeFeedbackBot-AI%20Powered-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Flask](https://img.shields.io/badge/Flask-2.3.3-red)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange)
![Responsive](https://img.shields.io/badge/Responsive-Yes-brightgreen)

## ✨ Features

### 🎯 Core Functionality
- **Resume Analysis**: Upload PDF/DOCX resumes for AI-powered feedback
- **Portfolio Review**: Analyze personal websites and portfolios
- **Interactive Chatbot**: Floating AI assistant for follow-up questions
- **Responsive Design**: Works perfectly on mobile, tablet, and desktop
- **Real-time Feedback**: Instant analysis with detailed scoring

### 🎨 Modern UI/UX
- **Floating Chatbot**: Similar to modern e-commerce assistants
- **Glass Morphism**: Beautiful backdrop blur effects
- **Gradient Design**: Modern color schemes and animations
- **Mobile-First**: Optimized for all screen sizes
- **Smooth Animations**: Professional transitions and effects

### 📊 Analysis Features
- **Overall Scoring**: 1-10 rating system
- **Category Breakdown**: Detailed scores for different aspects
- **Strengths & Weaknesses**: Comprehensive feedback
- **Actionable Suggestions**: Specific improvement recommendations
- **Improved Versions**: AI-generated enhanced content

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- Modern web browser

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/muhammadsami987123/29_ResumeFeedbackBot.git
cd 29_ResumeFeedbackBot
```

2. **Create virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Create .env file
cp env.example .env

# Edit .env file with your OpenAI API key
OPENAI_API_KEY=your_openai_api_key_here
```

5. **Run the application**
```bash
python server.py
```

6. **Open in browser**
```
http://127.0.0.1:5000
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=4000
OPENAI_TEMPERATURE=0.7

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key_here

# File Upload Configuration
MAX_CONTENT_LENGTH=16777216  # 16MB in bytes
UPLOAD_FOLDER=uploads
OUTPUT_FOLDER=outputs

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### API Key Setup

1. **Get OpenAI API Key**
   - Visit [OpenAI Platform](https://platform.openai.com/)
   - Sign up or log in
   - Go to API Keys section
   - Create a new API key
   - Copy the key to your `.env` file

2. **API Key Security**
   - Never commit your API key to version control
   - Use environment variables
   - Consider using a secrets manager for production

## 📡 API Documentation

### Resume Analysis Endpoint

**POST** `/api/analyze-resume`

Analyzes uploaded resume files and provides comprehensive feedback.

#### Request
- **Content-Type**: `multipart/form-data`
- **Method**: POST

#### Parameters
```json
{
  "file": "resume.pdf|resume.docx",  // Required: PDF or DOCX file
  "target_role": "Software Engineer", // Optional: Target job role
  "industry": "Technology"           // Optional: Industry sector
}
```

#### Response
```json
{
  "success": true,
  "overall_score": 8.5,
  "scores": {
    "content": 8.0,
    "formatting": 9.0,
    "keywords": 8.5,
    "experience": 8.0
  },
  "strengths": [
    "Strong technical skills section",
    "Clear project descriptions",
    "Good use of action verbs"
  ],
  "weaknesses": [
    "Could include more quantifiable achievements",
    "Summary section needs improvement"
  ],
  "suggestions": [
    "Add metrics to quantify achievements",
    "Include a compelling summary",
    "Optimize for ATS systems"
  ],
  "improvements": {
    "improved_resume": "Enhanced resume content..."
  }
}
```

### Portfolio Analysis Endpoint

**POST** `/api/analyze-portfolio`

Analyzes portfolio websites and provides design and content feedback.

#### Request
- **Content-Type**: `application/json`
- **Method**: POST

#### Parameters
```json
{
  "portfolio_url": "https://your-portfolio.com"
}
```

#### Response
```json
{
  "success": true,
  "overall_score": 7.8,
  "scores": {
    "design": 8.0,
    "content": 7.5,
    "usability": 8.0,
    "performance": 7.5
  },
  "strengths": [
    "Clean and modern design",
    "Good project showcase",
    "Responsive layout"
  ],
  "weaknesses": [
    "Missing contact information",
    "Could improve loading speed"
  ],
  "suggestions": [
    "Add a contact form",
    "Optimize images for faster loading",
    "Include testimonials"
  ],
  "technical_recommendations": [
    "Implement lazy loading",
    "Use WebP image format",
    "Add meta descriptions"
  ]
}
```

### Chat Endpoint

**POST** `/api/chat`

Handles interactive chat with the AI assistant.

#### Request
- **Content-Type**: `application/json`
- **Method**: POST

#### Parameters
```json
{
  "message": "How can I improve my resume?",
  "context": {
    "type": "resume",
    "analysis": { /* previous analysis data */ }
  }
}
```

#### Response
```json
{
  "success": true,
  "response": "Based on your resume analysis, here are some specific improvements..."
}
```

## 🛠️ Error Handling

### Common Errors and Solutions

#### 1. OpenAI API Errors

**Error**: `openai.AuthenticationError`
```python
# Solution: Check your API key
# Make sure OPENAI_API_KEY is set correctly in .env file
```

**Error**: `openai.RateLimitError`
```python
# Solution: Implement retry logic or upgrade plan
# Add delay between requests
```

**Error**: `openai.InvalidRequestError`
```python
# Solution: Check input format and size
# Ensure file is PDF/DOCX and under 16MB
```

#### 2. File Upload Errors

**Error**: `File too large`
```python
# Solution: Check MAX_CONTENT_LENGTH in config
# Default limit is 16MB
```

**Error**: `Unsupported file format`
```python
# Solution: Only PDF and DOCX files are supported
# Convert other formats before uploading
```

**Error**: `File upload failed`
```python
# Solution: Check upload folder permissions
# Ensure uploads/ directory exists and is writable
```

#### 3. Network Errors

**Error**: `Connection timeout`
```python
# Solution: Check internet connection
# Verify OpenAI API is accessible
```

**Error**: `SSL Certificate error`
```python
# Solution: Update certificates
# Check system time is correct
```

### Error Response Format

All API endpoints return consistent error responses:

```json
{
  "success": false,
  "error": "Error description",
  "error_code": "ERROR_CODE",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## 🔍 Troubleshooting

### Installation Issues

#### 1. Python Version
```bash
# Check Python version
python --version

# Should be 3.8 or higher
# If not, install newer version
```

#### 2. Virtual Environment
```bash
# If venv activation fails
python -m venv --clear venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

#### 3. Dependencies
```bash
# If pip install fails
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Runtime Issues

#### 1. Port Already in Use
```bash
# Check what's using port 5000
netstat -ano | findstr :5000  # Windows
lsof -i :5000  # macOS/Linux

# Kill process or change port
python server.py --port 5001
```

#### 2. Permission Errors
```bash
# Create necessary directories
mkdir uploads outputs logs

# Set proper permissions (Linux/macOS)
chmod 755 uploads outputs logs
```

#### 3. Memory Issues
```python
# Reduce file size limits in config.py
MAX_CONTENT_LENGTH = 8388608  # 8MB instead of 16MB
```

### Performance Optimization

#### 1. Enable Caching
```python
# Add Redis caching
pip install redis
```

#### 2. Optimize File Processing
```python
# Use async processing for large files
# Implement background tasks
```

#### 3. Database Integration
```python
# Add SQLite/PostgreSQL for user management
# Store analysis history
```

## 🚀 Deployment

### Local Development
```bash
# Development mode
export FLASK_ENV=development
export FLASK_DEBUG=True
python server.py
```

### Production Deployment

#### 1. Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 server:app
```

#### 2. Using Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "server:app"]
```

#### 3. Environment Variables for Production
```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your_secure_secret_key
OPENAI_API_KEY=your_production_api_key
```

### Cloud Deployment

#### Heroku
```bash
# Create Procfile
echo "web: gunicorn server:app" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

#### AWS/Google Cloud
```bash
# Use App Engine or Elastic Beanstalk
# Configure environment variables
# Set up SSL certificates
```

## 📁 Project Structure

```
29_ResumeFeedbackBot/
├── server.py                 # Main Flask application
├── resume_analyzer.py        # Resume analysis logic
├── portfolio_analyzer.py     # Portfolio analysis logic
├── chat_service.py          # Chat functionality
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── README.md               # This file
├── templates/
│   └── index.html          # Main web interface
├── static/
│   ├── css/
│   └── js/
├── uploads/                # File upload directory
├── outputs/                # Analysis results
└── logs/                   # Application logs
```

## 🔒 Security Considerations

### API Security
- Use HTTPS in production
- Implement rate limiting
- Validate file uploads
- Sanitize user inputs

### Data Privacy
- Don't store sensitive resume data
- Implement data retention policies
- Use secure file handling
- Consider GDPR compliance

### Environment Security
- Use strong secret keys
- Rotate API keys regularly
- Monitor API usage
- Implement logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest

# Run linting
flake8 .
black .
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing the GPT API
- Flask community for the web framework
- Tailwind CSS for the styling framework
- Font Awesome for the icons

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/muhammadsami987123/29_ResumeFeedbackBot/issues) page
2. Create a new issue with detailed information
3. Include error logs and system information

### Contact Information
- **GitHub**: [muhammadsami987123](https://github.com/muhammadsami987123)
- **Email**: [Your Email]
- **LinkedIn**: [Your LinkedIn]

---

**Made with ❤️ for career development**

*This project is part of the 100 Days of AI Agents challenge.*
