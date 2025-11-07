# 🚀 BookmarkManager - Quick Start Guide

Get started with BookmarkManager in 5 minutes!

## Step 1: Install Dependencies

```bash
# Navigate to project directory
cd 96_BookmarkManager

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

## Step 2: Configure Environment

```bash
# Copy sample environment file
# On Windows (PowerShell):
Copy-Item env.sample -Destination .env

# On macOS/Linux:
cp env.sample .env

# Edit .env with your API keys
# Open .env and replace:
# - GEMINI_API_KEY=your_actual_key
# - OPENAI_API_KEY=your_actual_key (optional)
```

### Getting API Keys

**Google Gemini:**
1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy and paste into `.env`

**OpenAI (Optional):**
1. Go to https://platform.openai.com/api-keys
2. Create new secret key
3. Copy and paste into `.env`

## Step 3: Run the Application

```bash
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Step 4: Open in Browser

Go to: **http://localhost:8000**

## Step 5: Start Using!

### Add Your First Bookmark

1. Click **"Add Bookmark"** tab
2. Fill in the form:
   - **URL**: https://www.dribbble.com
   - **Title**: Design Inspiration Portal
   - **Tags**: design, inspiration, ui
   - **Category**: design
3. Click **"Add Bookmark"**

### Search Bookmarks

1. Click **"Search"** tab
2. Try: "Show me design tools"
3. Select search method: **"Semantic (AI)"**
4. Click **"Search"**

### View Statistics

1. Click **"Statistics"** tab
2. See your bookmark counts and tags

## Common Tasks

### Add Multiple Bookmarks

Repeat Step 5 for each bookmark you want to add.

### Filter Bookmarks

1. Go to **"Browse Bookmarks"** tab
2. Use dropdown filters for tags or categories

### Delete a Bookmark

1. Click the red trash icon on any bookmark card
2. Confirm deletion

### Export Bookmarks

1. Click the download icon in header
2. Click "Download as JSON"
3. File saved as `bookmarks-YYYY-MM-DD.json`

### Import Bookmarks

1. Click the download icon in header
2. Click "Choose File" under Import
3. Select previously exported JSON file
4. Bookmarks imported!

## Troubleshooting

### Port 8000 Already in Use

```bash
# Use a different port
PORT=8001 python main.py
```

### API Key Error

- Check `.env` file exists
- Verify `GEMINI_API_KEY` is set correctly
- Make sure no extra spaces or quotes

### Bookmarks Not Showing

- Navigate to "Browse Bookmarks" tab
- Try refreshing the page
- Check browser console for errors (F12)

## Next Steps

- 📖 Read full [README.md](README.md) for detailed documentation
- 🔧 Explore API endpoints at http://localhost:8000/docs
- 💾 Set up regular backups using Export feature
- 🎨 Customize categories in the UI
- 🔍 Try different semantic search queries

## File Structure

```
96_BookmarkManager/
├── main.py              ← Start here
├── config.py            ← Configuration
├── agent.py             ← Core logic
├── web_app.py           ← API server
├── requirements.txt     ← Dependencies
├── env.sample          ← Copy to .env
│
├── utils/
│   ├── llm_service.py   ← AI integration
│   └── storage_manager.py ← Data storage
│
├── templates/
│   └── index.html       ← Web interface
│
├── prompts/
│   └── semantic_search_prompt.txt
│
└── storage/
    └── bookmarks.json   ← Your bookmarks
```

## Need Help?

1. Check [README.md](README.md) for detailed docs
2. Review API docs at http://localhost:8000/docs
3. Check the prompts in `prompts/` directory
4. Review `config.py` for configuration options

---

**Happy bookmarking! 🎉**

