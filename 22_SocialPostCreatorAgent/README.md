# Day 22: SocialPostCreatorAgent – AI Social Media Post Generator

Generate high-quality, platform-specific social media posts using AI with both CLI and Web UI interfaces.

## ✨ Features

### 🎯 Multi-Platform Support
- **Twitter**: 280 characters, concise and engaging
- **Facebook**: 63,206 characters, conversational tone
- **Instagram**: 2,200 characters, hashtag-optimized
- **LinkedIn**: 3,000 characters, professional focus
- **TikTok**: 150 characters, trending and catchy
- **YouTube**: 5,000 characters, SEO-optimized

### 🖥️ Dual Interface
- **CLI Interface**: Rich, interactive command-line experience
- **Web UI**: Modern, responsive browser interface
- **Cross-platform**: Works on Windows, macOS, and Linux

### 🧠 AI-Powered Generation
- OpenAI GPT models for intelligent content creation
- Platform-specific formatting and tone adaptation
- Topic research integration (NewsAPI)
- Character limit enforcement and validation

### 💾 Output Options
- Copy to clipboard (CLI & Web)
- Save to local files with markdown formatting
- Platform-specific folder organization
- Character count validation

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key
- Optional: NewsAPI key for topic research

### Installation
1. **Clone and navigate to the project:**
   ```bash
   cd 22_SocialPostCreatorAgent
   ```

2. **Set up environment variables:**
   ```bash
   # Copy example file
   copy env.example .env
   
   # Edit .env with your API keys
   OPENAI_API_KEY=your_openai_api_key_here
   NEWSAPI_KEY=your_newsapi_key_here  # Optional
   ```

3. **Install dependencies:**
   ```bash
   # Windows
   install.bat
   
   # Or manually
   pip install -r requirements.txt
   ```

### Usage

#### 🖥️ CLI Interface
```bash
# Interactive mode
python -m 22_SocialPostCreatorAgent.cli

# Quick generation with parameters
python -m 22_SocialPostCreatorAgent.cli \
  --platform "LinkedIn" \
  --topic "AI in Healthcare" \
  --tone "professional" \
  --save --copy

# Non-interactive mode
python -m 22_SocialPostCreatorAgent.cli \
  --platform "Instagram" \
  --topic "Sustainable Living" \
  --tone "inspirational" \
  --non-interactive
```

#### 🌐 Web UI
```bash
# Start the web server
python -m 22_SocialPostCreatorAgent.web_app

# Open browser to: http://localhost:5000
```

#### 🎮 Interactive Launcher (Windows)
```bash
# Run the launcher for guided setup
start.bat
```

## 📱 Platform-Specific Features

### Twitter
- 280 character limit
- Hashtag optimization
- Engagement-focused writing
- URL-friendly formatting

### Facebook
- Extended character limit
- Conversational tone
- Comment-encouraging content
- Line break optimization

### Instagram
- Caption-focused content
- Hashtag strategy (5-10 tags)
- Visual storytelling
- Engagement optimization

### LinkedIn
- Professional tone
- Business insights
- Industry hashtags
- Thought leadership content

### TikTok
- Short, catchy captions
- Trending hashtags
- Youth-focused language
- Viral potential

### YouTube
- SEO-optimized descriptions
- Keyword integration
- Call-to-action elements
- Subscription encouragement

## 🎨 Tone Options

- **Professional**: Business-focused, authoritative
- **Casual**: Friendly, conversational
- **Witty**: Humorous, clever
- **Inspirational**: Motivational, uplifting
- **Friendly**: Warm, approachable
- **Authoritative**: Expert, confident
- **Playful**: Fun, energetic

## 📁 File Organization

Generated posts are saved in organized folders:
```
posts/
├── twitter/
│   ├── twitter_20241201_143022_ai_education.md
│   └── twitter_20241201_143156_climate_change.md
├── linkedin/
│   └── linkedin_20241201_143245_tech_innovation.md
└── instagram/
    └── instagram_20241201_143334_sustainable_living.md
```

Each file contains:
- Platform and topic information
- Generated content
- Character count validation
- Posting instructions
- Metadata and timestamps

## 🔧 Configuration

### Environment Variables
```bash
# Required
OPENAI_API_KEY=your_openai_api_key

# Optional
NEWSAPI_KEY=your_newsapi_key
OPENAI_MODEL=gpt-4o-mini
TW_TZ=UTC
```

### Customization
- Modify `config.py` for platform limits
- Adjust AI prompts in `ai_service.py`
- Customize web UI styling in templates
- Add new platforms and tones

## 🧪 Testing

### Test Installation
```bash
python test_installation.py
```

### Test Basic Functionality
```bash
# Test CLI
python -m 22_SocialPostCreatorAgent.cli --platform "Twitter" --topic "Test" --tone "professional" --non-interactive

# Test Web UI
python -m 22_SocialPostCreatorAgent.web_app
# Then visit http://localhost:5000
```

## 🚨 Troubleshooting

### Common Issues
1. **Missing OpenAI API key**: Set `OPENAI_API_KEY` in `.env`
2. **Import errors**: Ensure all dependencies are installed
3. **Web UI not loading**: Check if port 5000 is available
4. **Clipboard issues**: Install `pyperclip` for clipboard support

### Dependencies
- **rich**: CLI formatting and colors
- **flask**: Web interface framework
- **openai**: AI content generation
- **pyperclip**: Clipboard operations
- **requests**: API calls for topic research

## 🔮 Future Enhancements

- [ ] Multi-language support
- [ ] Post scheduling and automation
- [ ] Social media API integration
- [ ] Content analytics and optimization
- [ ] Team collaboration features
- [ ] Advanced tone customization
- [ ] Bulk post generation
- [ ] Content templates and presets

## 📄 License

This project is part of the 100 Days of AI Agents challenge. See LICENSE for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

---

**Built with ❤️ using OpenAI, Flask, and modern web technologies**


