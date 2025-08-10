# 🎙️ TextToSpeechAgent - Day 10 of #100DaysOfAI-Agents

A powerful text-to-speech agent that converts any input text, file, or URL into natural-sounding speech with AI-powered voice synthesis. Features a modern, responsive web interface with support for multiple languages and voice types.

---

## ✨ What's Included

- **Multiple Input Methods**: 
  - Direct text input with a beautiful textarea
  - File upload (.txt files) with drag-and-drop support
  - URL input for extracting content from web pages
- **AI-Powered TTS**: 
  - OpenAI TTS-1 and TTS-1-HD models for premium quality
  - Google TTS fallback for reliability
  - Support for multiple languages (English, Hindi, Urdu, and more)
- **Voice Customization**: 
  - Male/Female voice selection
  - High-quality audio output
- **Modern Web Interface**: 
  - Beautiful glassmorphism design with Tailwind CSS
  - Responsive layout for all devices
  - Smooth animations and transitions
  - Interactive input method selection cards
- **Session-Based Processing**: 
  - No user data saved permanently
  - One-time use, fully session-based

---

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.8+)
- **TTS Engines**: OpenAI TTS API, Google TTS (gTTS)
- **Text Extraction**: `trafilatura` for URL content extraction
- **Frontend**: HTML + Tailwind CSS + Vanilla JavaScript
- **Server**: Uvicorn ASGI server
- **Configuration**: `python-dotenv` for environment variables

---

## 🚀 Quick Start

### 1. Clone and Navigate
```bash
cd 10_TextToSpeechAgent
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
TTS_ENGINE=openai
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
Navigate to `http://localhost:8009` to access the web interface.

---

## 💡 Using the App

### Input Methods

#### 📝 Text Input
- Type or paste any text directly into the textarea
- Supports multiple languages and long paragraphs
- Perfect for quick text-to-speech conversion

#### 📁 File Upload
- Upload `.txt` files by clicking or dragging and dropping
- Drag-and-drop interface for easy file selection
- Automatic text extraction from uploaded files

#### 🔗 URL Input
- Paste any public webpage URL
- Automatically extracts main content using AI-powered text extraction
- Great for converting articles, blog posts, or news content

### Voice Options

#### 🌍 Language Support
- **Auto-detect**: Automatically detects text language
- **English**: Optimized for English text
- **Hindi**: Native Hindi pronunciation
- **Urdu**: Native Urdu pronunciation
- **Additional languages**: Can be easily extended

#### 🎭 Voice Types
- **Female Voice**: Clear, professional female voice
- **Male Voice**: Deep, authoritative male voice

### Output Features

#### 🔊 Audio Playback
- Built-in audio player with standard controls
- Play, pause, seek, and volume control
- High-quality MP3 audio output

#### ⬇️ Download
- Download generated speech as MP3 files
- Automatic file naming
- High-quality audio preservation

---

## 🧩 API Endpoints

### Main TTS Endpoint
```
POST /api/tts
```

**Request Parameters:**
- `text` (optional): Direct text input
- `file` (optional): Uploaded .txt file
- `url` (optional): Public webpage URL
- `language`: Language selection (default: "auto")
- `gender`: Voice type (default: "female")

**Response:**
- Audio file stream (MP3 format)
- Content-Disposition header for download

### Frontend Routes
- `GET /`: Main web interface
- `GET /static/js/app.js`: JavaScript application logic

---

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | Required | Your OpenAI API key for TTS-1 models |
| `TTS_ENGINE` | `openai` | TTS engine preference (`openai` or `gtts`) |

### TTS Engine Settings

#### OpenAI TTS (Default)
- **Models**: `tts-1`, `tts-1-hd`
- **Voices**: 
  - Female: `alloy` (clear, professional)
  - Male: `echo` (deep, authoritative)
- **Quality**: High-quality, natural-sounding speech

#### Google TTS (Fallback)
- **Quality**: Good quality, reliable fallback
- **Languages**: Extensive language support
- **Usage**: Automatic fallback if OpenAI fails

---

## 📁 Project Structure

```
10_TextToSpeechAgent/
├── server.py                 # FastAPI application and routes
├── tts_service.py            # TTS engine logic and OpenAI/gTTS integration
├── config.py                 # Configuration and environment variables
├── requirements.txt          # Python dependencies
├── templates/
│   └── index.html           # Modern web interface with Tailwind CSS
├── static/
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
- **Gradient Backgrounds**: Beautiful blue-to-purple gradients
- **Interactive Cards**: Clickable input method selection with hover effects
- **Smooth Animations**: Fade-in animations and hover transitions
- **Responsive Layout**: Works perfectly on desktop, tablet, and mobile

### User Experience
- **Intuitive Navigation**: Clear visual hierarchy and intuitive controls
- **Real-time Feedback**: Loading states, error messages, and success indicators
- **Accessibility**: Proper labels, focus states, and keyboard navigation
- **Modern Icons**: Font Awesome icons throughout the interface

---

## 🐛 Troubleshooting

### Common Issues

#### 1. "OpenAI API key not found"
- Ensure you've created a `.env` file with your API key
- Check that the key starts with `sk-` and is valid
- Verify you have sufficient OpenAI API credits

#### 2. "400 Bad Request" errors
- Make sure only one input method is selected
- Check that the selected input field has content
- Ensure file uploads are `.txt` files only

#### 3. "TTS generation failed"
- Check your internet connection
- Verify your OpenAI API key is valid
- Try switching to a different TTS engine in config

#### 4. Audio not playing
- Check browser console for JavaScript errors
- Ensure your browser supports MP3 audio playback
- Try refreshing the page

### PowerShell Issues (Windows)
If you encounter `&&` syntax errors in PowerShell:
```powershell
# Use this instead:
cd 10_TextToSpeechAgent; python server.py

# Or run commands separately:
cd 10_TextToSpeechAgent
python server.py
```

---

## 🔮 Future Enhancements

Potential improvements for future versions:
- **Voice Cloning**: Custom voice training and cloning
- **Batch Processing**: Convert multiple files at once
- **Audio Effects**: Speed control, pitch adjustment, background music
- **Real-time Streaming**: Live text-to-speech conversion
- **Mobile App**: Native mobile applications
- **API Rate Limiting**: Better handling of API quotas
- **Voice Preview**: Sample audio before full generation
- **Export Formats**: Support for WAV, OGG, and other formats

---

## 📝 License

This project is part of the #100DaysOfAI-Agents challenge by Muhammad Sami Asghar Mughal.

---

## 🤝 Contributing

Feel free to contribute to this project by:
- Reporting bugs and issues
- Suggesting new features and improvements
- Improving documentation and code quality
- Adding new TTS engines or language support
- Enhancing the user interface and experience

---

## 🙏 Acknowledgments

- **OpenAI**: For providing the TTS-1 models and API
- **Google**: For the reliable gTTS fallback service
- **FastAPI**: For the modern, fast web framework
- **Tailwind CSS**: For the beautiful, responsive design system
- **Font Awesome**: For the comprehensive icon library

---

**Happy Text-to-Speech Conversion! 🎉**

*Transform your words into beautiful speech with AI-powered technology.*


