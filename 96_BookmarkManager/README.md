# 📚 BookmarkManager - Day 96 of #100DaysOfAI-Agents

<div align="center">

![BookmarkManager Banner](https://img.shields.io/badge/BookmarkManager-Day%2096-blue?style=for-the-badge&logo=bookmark&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20Framework-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-API-blue?style=for-the-badge&logo=google&logoColor=white)

**Your intelligent bookmark management assistant powered by AI!**

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [🎭 Examples](#-examples) • [🏗️ Architecture](#-project-architecture) • [⚙️ Configuration](#-configuration--setup)

</div>

---

## ✨ What is BookmarkManager?

**BookmarkManager** is a sophisticated yet user-friendly bookmark management system that combines a modern web interface with AI-powered semantic search capabilities. It allows you to organize, categorize, and intelligently search through your bookmarks using natural language queries.

### 🌟 Key Highlights

- **🏷️ Smart Organization**: Organize bookmarks with tags and categories
- **🔍 Semantic Search**: Find bookmarks using natural language queries powered by Gemini 2.0-flash
- **💾 Persistent Storage**: JSON-based storage for easy backup and portability
- **🎨 Modern UI**: Beautiful, responsive dark-mode dashboard built with Tailwind CSS
- **⚡ Fast & Lightweight**: Built with FastAPI for optimal performance
- **📤 Import/Export**: Easily backup and restore your bookmarks
- **🏠 Local First**: All data stored locally - complete privacy

---

## 🎯 Features

### 🚀 Core Functionality

- ✅ **Add Bookmarks**: Save URLs with titles, tags, and categories
- ✅ **Browse Bookmarks**: View all bookmarks in an organized grid layout
- ✅ **Search Bookmarks**: Two search modes:
  - **Semantic Search**: AI-powered natural language search (e.g., "Show me design tools")
  - **Basic Search**: Simple text-based search in titles and URLs
- ✅ **Filter by Tag**: Quick filtering by bookmark tags
- ✅ **Filter by Category**: Organize by predefined categories
- ✅ **Delete Bookmarks**: Remove individual bookmarks or all under a tag
- ✅ **Statistics Dashboard**: View bookmark counts, tags, and categories
- ✅ **Export/Import**: JSON export and import functionality
- ✅ **Dark Mode UI**: Eye-friendly modern interface
- ✅ **Multiple LLM Support**: Choose between Gemini and OpenAI

---

## 🎭 Examples

### Adding a Bookmark

```
Title: Dribbble - Design Inspiration
URL: https://dribbble.com
Tags: design, inspiration, ui
Category: design
```

### Semantic Search Examples

- "Show me all design tools" → Finds bookmarks tagged with design, ui, graphics, etc.
- "Find my learning resources" → Finds bookmarks in learning category
- "Show me productivity tools" → Finds bookmarks tagged with productivity

### API Usage

```python
# Add a bookmark
POST /api/bookmarks/add
{
    "url": "https://example.com",
    "title": "Example Site",
    "tags": "example,test",
    "category": "learning"
}

# Search bookmarks
POST /api/bookmarks/search
{
    "query": "design tools",
    "method": "semantic",
    "llm_choice": "gemini"
}

# Get all bookmarks
GET /api/bookmarks/all

# Filter by tag
GET /api/bookmarks/by-tag?tag=design

# Filter by category
GET /api/bookmarks/by-category?category=learning
```

---

## 🏗️ Project Architecture

```
96_BookmarkManager/
├── main.py                    # Entry point
├── config.py                  # Configuration & environment variables
├── agent.py                   # Main BookmarkManager agent logic
├── web_app.py                 # FastAPI application & routes
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore rules
│
├── utils/
│   ├── __init__.py
│   ├── llm_service.py        # LLM service for Gemini & OpenAI
│   └── storage_manager.py    # Bookmark storage & management
│
├── templates/
│   └── index.html            # Main dashboard UI
│
├── prompts/
│   └── semantic_search_prompt.txt  # LLM prompt for semantic search
│
└── storage/
    └── bookmarks.json        # Bookmark storage file
```

### Component Breakdown

#### 1. **Agent (agent.py)**
- Core business logic for bookmark operations
- Semantic and basic search functionality
- Statistics generation
- Import/Export handling

#### 2. **Storage Manager (utils/storage_manager.py)**
- JSON-based bookmark persistence
- Tag and category indexing
- Search operations
- CRUD operations for bookmarks

#### 3. **LLM Service (utils/llm_service.py)**
- Integration with Gemini 2.0-flash API
- Integration with OpenAI GPT-4
- Template management
- Content generation

#### 4. **Web Application (web_app.py)**
- FastAPI REST API
- Static file serving
- Template rendering
- Request handling

#### 5. **Frontend (templates/index.html)**
- Alpine.js for interactivity
- Tailwind CSS for styling
- Real-time updates
- Responsive design

---

## ⚙️ Configuration & Setup

### 1. Prerequisites

- Python 3.8+
- pip package manager
- API keys for:
  - Google Gemini API (optional, but recommended)
  - OpenAI API (optional)

### 2. Installation

```bash
# Clone or navigate to the project
cd 96_BookmarkManager

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Setup

Create a `.env` file in the project root:

```env
# API Keys
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Configuration
DEFAULT_LLM=gemini
GEMINI_MODEL=gemini-2.0-flash
OPENAI_MODEL=gpt-4

# Storage
STORAGE_DIR=./storage

# Server
HOST=0.0.0.0
PORT=8000
```

### 4. Running the Application

```bash
# Start the server
python main.py

# Server will be available at http://localhost:8000
```

---

## 🧪 Testing & Quality Assurance

### API Testing

```bash
# Test health check
curl http://localhost:8000/api/health

# Add a bookmark
curl -X POST http://localhost:8000/api/bookmarks/add \
  -d "url=https://example.com&title=Example&tags=test&category=learning"

# Get all bookmarks
curl http://localhost:8000/api/bookmarks/all

# Semantic search
curl -X POST http://localhost:8000/api/bookmarks/search \
  -d "query=design tools&method=semantic&llm_choice=gemini"
```

### Frontend Testing

1. Open http://localhost:8000 in your browser
2. Test adding a bookmark
3. Test searching with semantic search
4. Test filtering by tags and categories
5. Test export/import functionality

---

## 📊 Data Storage Format

Bookmarks are stored in `storage/bookmarks.json`:

```json
{
  "bookmarks": [
    {
      "id": 1,
      "url": "https://example.com",
      "title": "Example Bookmark",
      "tags": ["example", "test"],
      "category": "learning",
      "created_at": "2025-01-01T12:00:00",
      "updated_at": "2025-01-01T12:00:00"
    }
  ],
  "tags": {
    "example": [1],
    "test": [1]
  }
}
```

---

## 🚀 Usage Workflow

### For Users

1. **Add Bookmarks**: Click "Add Bookmark" tab and fill in the form
2. **Browse**: View all bookmarks in the "Browse Bookmarks" tab
3. **Search**: Use semantic search for natural language queries
4. **Organize**: Filter by tags or categories
5. **Manage**: Delete unwanted bookmarks
6. **Backup**: Export bookmarks to JSON regularly

### For Developers

1. **Custom Search Logic**: Modify semantic_search_prompt.txt
2. **Storage Backend**: Extend StorageManager for database support
3. **Additional Categories**: Add more predefined categories in the UI
4. **LLM Integration**: Add support for more LLM providers

---

## 🔧 Advanced Features

### Adding Custom Categories

Edit the category dropdown in `templates/index.html`:

```html
<select x-model="form.category">
    <option value="custom-category">Custom Category</option>
</select>
```

### Extending Storage to Database

Implement a new storage backend in `utils/storage_manager.py`:

```python
class DatabaseStorageManager(StorageManager):
    def __init__(self, connection_string):
        # Implement database operations
        pass
```

### Custom LLM Prompts

Modify `prompts/semantic_search_prompt.txt`:

```
Add custom instructions for semantic search behavior
```

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | >=0.109.0 | Web framework |
| uvicorn | >=0.27.0 | ASGI server |
| jinja2 | >=3.1.2 | Template engine |
| python-dotenv | >=1.0.0 | Environment variables |
| google-generativeai | >=0.5.0 | Gemini API |
| openai | >=1.10.0 | OpenAI API |
| python-multipart | >=0.0.9 | Form data handling |
| requests | >=2.31.0 | HTTP requests |
| httpx | >=0.25.0 | Async HTTP |

---

## 🔐 Security Considerations

- ✅ Never commit `.env` file with API keys
- ✅ API keys should be stored securely
- ✅ Use environment variables for sensitive data
- ✅ Validate all user inputs
- ✅ Consider adding authentication for multi-user deployment

---

## 🐛 Troubleshooting

### Issue: "API key not found"
**Solution**: Ensure `.env` file exists and `GEMINI_API_KEY` is set

### Issue: "Bookmarks not saving"
**Solution**: Check that `storage/` directory exists and has write permissions

### Issue: "Semantic search returns empty results"
**Solution**: Ensure Gemini API is working correctly and bookmarks exist in database

### Issue: "Port 8000 already in use"
**Solution**: Change port in `.env` or use `PORT=8001 python main.py`

---

## 📚 API Documentation

Full API documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🤝 Contributing

This is part of the #100DaysOfAI-Agents initiative. Contributions are welcome!

### How to Contribute

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Areas for Enhancement

- Database support (SQLite/PostgreSQL)
- Browser extension for quick bookmarking
- Mobile app
- Collaborative bookmarks
- Shared bookmark collections
- Advanced analytics

---

## 📝 License

This project is open-source and available for personal and commercial use.

---

## 🎓 Learning Outcomes

By using BookmarkManager, you'll learn:

- ✅ Building web applications with FastAPI
- ✅ Semantic search with LLMs
- ✅ Frontend development with Alpine.js and Tailwind CSS
- ✅ JSON-based data persistence
- ✅ RESTful API design
- ✅ AI integration in practical applications

---

## 📞 Support

For issues, questions, or suggestions:

1. Check the troubleshooting section
2. Review the API documentation
3. Examine example implementations in other Day agents

---

## 🌟 Future Roadmap

- [ ] Database backend support (SQLite/PostgreSQL)
- [ ] User authentication
- [ ] Collaborative bookmarks
- [ ] Mobile app
- [ ] Browser extension
- [ ] Advanced filtering
- [ ] Bookmark analytics
- [ ] Scheduled archival
- [ ] Full-text search
- [ ] Integration with popular bookmarking services

---

**Made with ❤️ as part of #100DaysOfAI-Agents**

Day 96 • BookmarkManager • Smart Bookmark Management with AI

