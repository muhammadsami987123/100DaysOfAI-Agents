# 💼 JobApplicationAgent - Day 12 of #100DaysOfAI-Agents

A powerful AI agent that generates tailored job applications — including customized resumes, personalized cover letters, and job fit summaries — from uploaded resumes and job descriptions. Features a modern, responsive web interface with support for multiple languages and professional document generation.

---

## ✨ What's Included

- **Resume Upload & Processing**: 
  - Support for PDF and DOCX resume formats
  - Automatic text extraction and parsing
  - Skills and experience identification
- **Job Description Analysis**: 
  - Direct text input with intelligent parsing
  - **Job posting URL extraction** - Paste URLs from LinkedIn, Indeed, Glassdoor, and more
  - Key requirements and skills extraction
- **AI-Powered Generation**: 
  - Customized resume tailored to job requirements
  - Personalized cover letter with company-specific content
  - **Additional documents**: Personal Statement, Reference Page, Thank You Note, Motivation Letter, LinkedIn Bio
  - Job fit summary with match percentage and key highlights
- **Multilingual Support**: 
  - English, Hindi, Urdu, and more languages
  - Localized content generation
- **Document Export**: 
  - PDF and DOCX format downloads with **improved formatting**
  - Professional formatting and styling
- **Modern Web Interface**: 
  - Beautiful glassmorphism design with Tailwind CSS
  - Responsive layout for all devices
  - Smooth animations and transitions
  - Progress tracking and real-time feedback
- **Session-Based Processing**: 
  - No user data saved permanently
  - One-time use, fully session-based

---

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.8+)
- **AI Engine**: OpenAI GPT-4 for content generation
- **Document Processing**: PyMuPDF (PDF), python-docx (DOCX)
- **Document Generation**: python-docx, reportlab (PDF)
- **Web Scraping**: BeautifulSoup4, requests for URL extraction
- **Frontend**: HTML + Tailwind CSS + Vanilla JavaScript
- **Server**: Uvicorn ASGI server
- **Configuration**: `python-dotenv` for environment variables

---

## 🚀 Quick Start

### 1. Clone and Navigate
```bash
cd 12_JobApplicationAgent
```

### 2. Install Dependencies
```bash
# Windows (PowerShell)
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# macOS/Linux
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Environment
Create a `.env` file in the project directory:
```env
OPENAI_API_KEY=sk-your-openai-api-key-here
PORT=8012
MAX_FILE_SIZE=10485760
```

**Getting Your OpenAI API Key:**
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

### 4. Run the Application
```bash
# Windows (PowerShell)
python server.py

# macOS/Linux
python server.py
```

### 5. Open in Browser
Navigate to `http://localhost:8012` to access the web interface.

---

## 💡 Using the App

### Step 1: Upload Your Resume
- **Supported Formats**: PDF (.pdf) and DOCX (.docx)
- **File Size**: Up to 10MB
- **Drag & Drop**: Simply drag your resume file onto the upload area
- **Text Extraction**: Automatically extracts and parses your resume content

### Step 2: Enter Job Description
- **Manual Input**: Paste the job description directly into the text area
- **URL Extraction**: Paste job posting URLs from LinkedIn, Indeed, Glassdoor, Monster, ZipRecruiter, or CareerBuilder
- **Smart Parsing**: AI automatically identifies key requirements and skills
- **Edit Extracted Content**: Review and modify the extracted job description before generation

### Step 3: Select Additional Documents (Optional)
- **Personal Statement**: Professional summary showcasing your unique value
- **Reference Page**: Professional references with contact information
- **Thank You Note**: Post-interview follow-up message
- **Motivation Letter**: Detailed explanation of your interest in the role
- **LinkedIn Bio**: Professional profile optimized for the target position

### Step 4: Generate Applications
- **Customized Resume**: AI creates a job-specific version of your resume
- **Cover Letter**: Personalized cover letter matching the job requirements
- **Additional Documents**: Generate selected supplementary materials
- **Fit Summary**: Analysis of how well you match the position

### Output Features

#### 📄 Customized Resume
- **Job-Specific Content**: Tailored to match job requirements
- **Skills Highlighting**: Emphasizes relevant skills and experiences
- **Professional Formatting**: Clean, ATS-friendly layout with improved structure
- **Download Options**: PDF and DOCX formats with enhanced formatting

#### 📝 Personalized Cover Letter
- **Company-Specific**: References company name and culture
- **Requirement Matching**: Addresses key job requirements
- **Professional Tone**: Appropriate for the industry and role
- **Custom Length**: Adjustable based on job level

#### 📋 Additional Documents
- **Personal Statement**: Compelling professional summary (300-500 words)
- **Reference Page**: Professional references with contact details
- **Thank You Note**: Post-interview follow-up (150-200 words)
- **Motivation Letter**: Detailed interest explanation
- **LinkedIn Bio**: Optimized professional profile

#### 📊 Job Fit Summary
- **Match Percentage**: Overall fit score with the position
- **Key Strengths**: Your top qualifications for the role
- **Gap Analysis**: Areas where you could improve
- **Recommendations**: Suggestions for application enhancement

---

## 🧩 API Endpoints

### Main Application Generation Endpoint
```
POST /api/generate-application
```

**Request Parameters:**
- `resume_file`: Uploaded resume file (PDF/DOCX)
- `job_description`: Job description text
- `language`: Language preference (default: "en")
- `cover_letter_length`: Short/Medium/Long (default: "medium")
- `additional_documents`: Comma-separated list of document types (optional)

**Response:**
```json
{
  "success": true,
  "data": {
    "customized_resume": "Resume content...",
    "cover_letter": "Cover letter content...",
    "additional_documents": {
      "personal_statement": "Content...",
      "reference_page": "Content...",
      "thank_you_note": "Content...",
      "motivation_letter": "Content...",
      "linkedin_bio": "Content..."
    },
    "fit_summary": {
      "match_percentage": 85,
      "key_strengths": ["Skill 1", "Skill 2"],
      "gap_areas": ["Area 1"],
      "recommendations": ["Rec 1", "Rec 2"]
    }
  }
}
```

### URL Extraction Endpoint
```
POST /api/extract-job-from-url
```

**Request Parameters:**
- `url`: Job posting URL

**Response:**
```json
{
  "success": true,
  "content": "Extracted job description...",
  "source_url": "https://example.com/job",
  "job_site": "linkedin"
}
```

### Document Download Endpoints
```
GET /api/download/resume/{format}
GET /api/download/cover-letter/{format}
GET /api/download/additional-document/{doc_type}/{format}
```

**Parameters:**
- `format`: "pdf" or "docx"
- `doc_type`: "personal_statement", "reference_page", "thank_you_note", "motivation_letter", "linkedin_bio"

### Information Endpoints
```
GET /api/languages
GET /api/cover-letter-lengths
GET /api/additional-documents
GET /api/supported-job-sites
GET /api/formats
```

### Frontend Routes
- `GET /`: Main web interface
- `GET /static/js/app.js`: JavaScript application logic
- `GET /static/css/style.css`: Custom styles

---

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description | Required |
|----------|---------|-------------|----------|
| `OPENAI_API_KEY` | - | Your OpenAI API key for GPT-4 | ✅ Yes |
| `PORT` | `8012` | Server port number | ❌ No |
| `MAX_FILE_SIZE` | `10485760` | Maximum file size in bytes (10MB) | ❌ No |
| `DEFAULT_LANGUAGE` | `en` | Default language for generation | ❌ No |

### AI Model Settings

#### OpenAI GPT-4 (Default)
- **Model**: `gpt-4-turbo-preview` (latest and most capable)
- **Temperature**: 0.7 (balanced creativity and consistency)
- **Max Tokens**: 4000 (sufficient for comprehensive documents)
- **Features**: Advanced reasoning, document analysis, multilingual support

---

## 📁 Project Structure

```
12_JobApplicationAgent/
├── server.py                 # FastAPI application and routes
├── job_agent.py              # Main AI agent logic and OpenAI integration
├── document_processor.py     # Resume parsing and document processing
├── document_generator.py     # PDF/DOCX generation utilities
├── config.py                 # Configuration and environment variables
├── requirements.txt          # Python dependencies
├── templates/
│   └── index.html           # Modern web interface with Tailwind CSS
├── static/
│   ├── css/
│   │   └── style.css        # Custom styles and animations
│   └── js/
│       └── app.js           # Frontend JavaScript logic
├── install.bat              # Windows installation script
├── start.bat                # Windows startup script
└── README.md                # This file
```

---

## 🎨 UI Features

### Design Elements
- **Glassmorphism**: Semi-transparent white cards with backdrop blur
- **Gradient Backgrounds**: Professional blue-to-purple gradients
- **Interactive Cards**: Clickable sections with hover effects
- **Smooth Animations**: Fade-in animations and hover transitions
- **Responsive Layout**: Works perfectly on desktop, tablet, and mobile

### User Experience
- **Intuitive Workflow**: Clear step-by-step process
- **Real-time Feedback**: Loading states, progress indicators, and success messages
- **Drag & Drop**: Easy file upload with visual feedback
- **Preview Mode**: Preview generated content before download
- **Accessibility**: Proper labels, focus states, and keyboard navigation
- **Modern Icons**: Font Awesome icons throughout the interface

### Interactive Elements
- **File Upload Zone**: Drag-and-drop resume upload with format validation
- **Job Description Editor**: Rich text area with character count
- **Generation Progress**: Real-time progress tracking during AI processing
- **Download Buttons**: Multiple format options for each document
- **Language Selector**: Dropdown for multilingual support

---

## 🌍 Multilingual Support

### Supported Languages
- **English (en)**: Default language with full support
- **Hindi (hi)**: Native Hindi content generation
- **Urdu (ur)**: Native Urdu content generation
- **Spanish (es)**: Spanish content generation
- **French (fr)**: French content generation
- **German (de)**: German content generation

### Language Features
- **Localized Content**: Culture-appropriate tone and style
- **Native Scripts**: Proper rendering of non-Latin scripts
- **Regional Formats**: Date and number formatting per locale
- **Cultural Context**: Understanding of regional job market norms

---

## 🔍 Document Processing

### Resume Parsing
- **PDF Processing**: PyMuPDF for reliable PDF text extraction
- **DOCX Processing**: python-docx for Word document parsing
- **Format Preservation**: Maintains original formatting where possible
- **Error Handling**: Graceful handling of corrupted or password-protected files

### Content Analysis
- **Skills Extraction**: Identifies technical and soft skills
- **Experience Parsing**: Extracts work history and achievements
- **Education Detection**: Identifies educational background
- **Contact Information**: Safely extracts contact details

### Document Generation
- **PDF Generation**: ReportLab for professional PDF creation
- **DOCX Generation**: python-docx for Word document creation
- **ATS Optimization**: Ensures compatibility with Applicant Tracking Systems
- **Professional Styling**: Clean, modern formatting

---

## 🚨 Common Issues & Solutions

### Issue 1: "OpenAI API key not found"
**Solution**: Ensure your `.env` file contains a valid OpenAI API key starting with `sk-`

### Issue 2: "File upload failed"
**Solution**: Check file format (PDF/DOCX only) and size (max 10MB)

### Issue 3: "Document generation failed"
**Solution**: Verify your OpenAI API key has sufficient credits and is valid

### Issue 4: "Resume parsing error"
**Solution**: Ensure the resume file is not password-protected and is readable

### Issue 5: "Port already in use"
**Solution**: Change the PORT in your `.env` file or kill the existing process

---

## 🔮 Future Enhancements

Potential improvements for future versions:
- **Job URL Processing**: Direct extraction from job posting URLs
- **Multiple Resume Support**: Upload and manage multiple resume versions
- **Template Library**: Pre-built resume and cover letter templates
- **Industry-Specific Optimization**: Tailored content for different industries
- **Voice Input**: Speech-to-text for job descriptions
- **Application Tracking**: Save and track multiple applications
- **Interview Preparation**: Generate interview questions and answers
- **Salary Negotiation**: AI-powered salary negotiation assistance
- **LinkedIn Integration**: Import profile data directly
- **Real-time Collaboration**: Share and edit applications with others

---

## 📝 License

This project is part of the #100DaysOfAI-Agents challenge by Muhammad Sami Asghar Mughal.

---

## 🤝 Contributing

Feel free to contribute to this project by:
- Reporting bugs and issues
- Suggesting new features and improvements
- Improving documentation and code quality
- Adding new document formats or language support
- Enhancing the user interface and experience
- Adding more AI models or processing capabilities

---

## 🙏 Acknowledgments

- **OpenAI**: For providing the GPT-4 models and API
- **FastAPI**: For the modern, fast web framework
- **Tailwind CSS**: For the beautiful, responsive design system
- **Font Awesome**: For the comprehensive icon library
- **PyMuPDF**: For reliable PDF processing
- **python-docx**: For Word document handling
- **ReportLab**: For PDF generation capabilities

---

## 📞 Support & Community

### Getting Help
1. **Check this README** for common issues and solutions
2. **Review server logs** for detailed error information
3. **Check browser console** for frontend issues
4. **Verify API key** and OpenAI account status
5. **Test with simple files** before trying complex ones

### Common Questions

**Q: What resume formats are supported?**
A: Currently PDF (.pdf) and DOCX (.docx) formats are supported.

**Q: How accurate is the AI-generated content?**
A: The AI provides high-quality, professional content but should be reviewed and customized before submission.

**Q: Is my data saved or stored?**
A: No, all processing is session-based and no data is permanently stored.

**Q: Can I use this for multiple job applications?**
A: Yes, you can generate applications for multiple jobs using the same resume.

**Q: How long does generation take?**
A: Typically 30-60 seconds depending on resume complexity and job description length.

---

**Happy Job Application Generation! 🎉**

*Transform your job search with AI-powered, personalized applications that increase your chances of landing interviews.*

---

## 🔄 Version History

- **v1.0.0** - Initial release with basic resume and cover letter generation
- **v1.1.0** - Added job fit analysis and multilingual support
- **v1.2.0** - Enhanced document processing and PDF/DOCX export
- **v1.3.0** - Improved UI/UX with glassmorphism design
- **v1.4.0** - Added progress tracking and error handling
- **v1.5.0** - Enhanced AI prompts and content quality
