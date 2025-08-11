# 🎤 SpeechToTextAgent - Day 11 of #100DaysOfAI-Agents

A powerful speech-to-text agent that converts audio files, video files, and YouTube URLs into clean, formatted text using AI-powered transcription. Features a modern, responsive web interface with support for multiple audio formats and automatic language detection.

---

## ✨ What's Included

- **Multiple Input Methods**: 
  - Audio file upload (.mp3, .wav, .m4a, .ogg) with drag-and-drop support
  - Video file upload (.mp4, .avi, .mov) with automatic audio extraction
  - YouTube URL input for fetching and transcribing public videos
- **AI-Powered Transcription**: 
  - OpenAI Whisper API for high-accuracy transcription
  - Automatic language detection and support for 100+ languages
  - Special support for Hindi, Urdu, English, and South Asian languages
  - Clean, formatted text output with punctuation and structure
- **Advanced Processing**: 
  - Automatic audio extraction from video files
  - YouTube video processing with audio download
  - Support for long audio files with progress tracking
  - 2-minute timeout protection with user cancellation
- **Modern Web Interface**: 
  - Beautiful glassmorphism design with Tailwind CSS
  - Responsive layout for all devices
  - Smooth animations and transitions
  - Interactive input method selection cards
  - Real-time progress timer and cancellation
- **Session-Based Processing**: 
  - No user data saved permanently
  - One-time use, fully session-based

---

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.8+)
- **Transcription Engine**: OpenAI Whisper API
- **Audio Processing**: `pydub`, `moviepy` for video processing
- **Video Processing**: `moviepy` for audio extraction
- **YouTube Processing**: `yt-dlp` for video download
- **Frontend**: HTML + Tailwind CSS + Vanilla JavaScript
- **Server**: Uvicorn ASGI server
- **Configuration**: `python-dotenv` for environment variables
- **System Dependencies**: FFmpeg for audio/video processing

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.8 or higher** installed on your system
- **FFmpeg** installed and accessible from command line (see FFmpeg installation section below)
- **OpenAI API key** (see API key setup section below)

### 1. Clone and Navigate
```bash
cd 11_SpeechToTextAgent
```

### 2. Install FFmpeg (Required for Audio/Video Processing)

#### Windows - Option 1: Winget (Recommended)
```cmd
winget install --id=Gyan.FFmpeg -e
```
**After installation, restart your terminal/PowerShell** for PATH changes to take effect.

#### Windows - Option 2: Chocolatey (Admin Required)
```cmd
# Run PowerShell as Administrator
choco install ffmpeg -y
```

#### Windows - Option 3: Manual Download
1. Download from [FFmpeg Official Site](https://ffmpeg.org/download.html)
2. Extract to `C:\ffmpeg\`
3. Add `C:\ffmpeg\bin\` to your system PATH environment variable

#### macOS
```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

#### Verify FFmpeg Installation
```bash
ffmpeg -version
```
**Expected Output**: Should show FFmpeg version information. If you get "command not found", restart your terminal or check PATH settings.

### 3. Install Python Dependencies

#### Windows (PowerShell)
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### macOS/Linux
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Alternative: Use Provided Scripts (Windows)
```cmd
# Run the installation script
install.bat
```

### 4. Configure Environment Variables

Create a `.env` file in the project directory:
```env
OPENAI_API_KEY=sk-your-openai-api-key-here
WHISPER_MODEL=whisper-1
MAX_FILE_SIZE=26214400
PORT=8010
```

**Getting Your OpenAI API Key:**
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. Paste it in your `.env` file

**⚠️ Important**: Never share your API key or commit it to version control!

### 5. Run the Application

#### Windows (PowerShell)
```powershell
# Make sure virtual environment is activated
venv\Scripts\activate

# Start the server
python server.py
```

#### macOS/Linux
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Start the server
python server.py
```

#### Alternative: Use Provided Scripts (Windows)
```cmd
# Run the startup script
start.bat
```

### 6. Access the Application
Open your browser and navigate to `http://localhost:8010`

---

## 🚨 Common Setup Issues & Solutions

### Issue 1: "FFmpeg not found" or "RuntimeWarning: Couldn't find ffmpeg"

**Symptoms:**
- Application hangs when processing video/YouTube files
- Runtime warnings about FFmpeg not being found
- Audio/video processing fails silently

**Solutions:**
1. **Verify FFmpeg installation:**
   ```bash
   ffmpeg -version
   ```

2. **If not found, install FFmpeg (see installation section above)**

3. **Check PATH environment variable:**
   ```cmd
   where ffmpeg
   ```
   Should show the path to ffmpeg.exe

4. **Restart your terminal/PowerShell** after installation

5. **If using virtual environment, restart it:**
   ```cmd
   deactivate
   venv\Scripts\activate
   ```

### Issue 2: "ValueError: invalid literal for int() with base 10: '25MB'"

**Symptoms:**
- Server fails to start with configuration error
- Error about MAX_FILE_SIZE parsing

**Solutions:**
1. **Check your `.env` file format:**
   ```env
   # ❌ Wrong - Don't use text like "25MB"
   MAX_FILE_SIZE=25MB
   
   # ✅ Correct - Use bytes (25MB = 26214400 bytes)
   MAX_FILE_SIZE=26214400
   ```

2. **Use the provided `.env.example` as a template**

### Issue 3: "OpenAI API key not found" or "Invalid API key"

**Symptoms:**
- Transcription requests fail immediately
- Authentication errors in logs

**Solutions:**
1. **Verify `.env` file exists in project root**
2. **Check API key format:**
   ```env
   # ❌ Wrong - Missing sk- prefix
   OPENAI_API_KEY=your-key-here
   
   # ✅ Correct - Should start with sk-
   OPENAI_API_KEY=sk-your-actual-key-here
   ```
3. **Verify API key is valid at [OpenAI Platform](https://platform.openai.com/api-keys)**
4. **Check you have sufficient API credits**

### Issue 4: "Module not found" errors during pip install

**Symptoms:**
- `pip install -r requirements.txt` fails
- Missing module errors

**Solutions:**
1. **Update pip:**
   ```bash
   python -m pip install --upgrade pip
   ```

2. **Install build tools (Windows):**
   ```cmd
   pip install wheel setuptools
   ```

3. **Try installing packages individually:**
   ```bash
   pip install fastapi uvicorn python-dotenv openai
   pip install pydub moviepy yt-dlp
   ```

### Issue 5: Application hangs at "Finalizing..." or 100% progress

**Symptoms:**
- Frontend shows 100% progress but no results
- No error messages displayed
- Application appears stuck

**Solutions:**
1. **Check browser console for JavaScript errors**
2. **Verify FFmpeg is properly installed (see Issue 1)**
3. **Check server logs for backend errors**
4. **Use the Cancel button if available**
5. **Try with a smaller audio file first**

### Issue 6: PowerShell execution policy errors

**Symptoms:**
- Scripts won't run
- "Execution policy" errors

**Solutions:**
1. **Check execution policy:**
   ```powershell
   Get-ExecutionPolicy
   ```

2. **Set execution policy (run as Administrator):**
   ```powershell
   Set-ExecutionPolicy RemoteSigned
   ```

3. **Or run scripts with bypass:**
   ```powershell
   PowerShell -ExecutionPolicy Bypass -File install.bat
   ```

### Issue 7: Port already in use

**Symptoms:**
- "Address already in use" error
- Can't start server

**Solutions:**
1. **Change port in `.env` file:**
   ```env
   PORT=8011
   ```

2. **Or kill existing process:**
   ```cmd
   # Windows
   netstat -ano | findstr :8010
   taskkill /PID <PID> /F
   
   # macOS/Linux
   lsof -ti:8010 | xargs kill -9
   ```

---

## 💡 Using the App

### Input Methods

#### 🎵 Audio File Upload
- Upload audio files (.mp3, .wav, .m4a, .ogg) by clicking or dragging and dropping
- Drag-and-drop interface for easy file selection
- Automatic format detection and processing
- Support for files up to 25MB
- **Supported formats**: MP3, WAV, M4A, OGG, FLAC

#### 🎬 Video File Upload
- Upload video files (.mp4, .avi, .mov) with automatic audio extraction
- Extracts audio track and transcribes it to text
- Maintains original video quality while processing audio
- Perfect for transcribing recorded presentations, meetings, or videos
- **Supported formats**: MP4, AVI, MOV, MKV, WMV

#### 🔗 YouTube URL Input
- Paste any public YouTube video URL
- Automatically downloads audio and transcribes it
- Supports all public YouTube videos
- Great for transcribing educational content, podcasts, or interviews
- **Note**: Age-restricted or private videos may not work

### Transcription Features

#### 🌍 Language Support
- **Auto-detect**: Automatically detects audio language
- **Priority Languages**: Hindi (हिन्दी), Urdu (اردو), English
- **100+ Languages**: Support for Spanish, French, German, Chinese, Japanese, Arabic, and many more
- **South Asian Support**: Bengali, Tamil, Telugu, Kannada, Malayalam, Gujarati, Punjabi, Oriya, Assamese, Nepali, Sinhala, Myanmar, Khmer, Lao, Thai, Vietnamese, Indonesian, Malay, Tagalog
- **Accent Recognition**: Handles various accents and dialects
- **Multi-language**: Can transcribe mixed-language content

#### 📝 Output Quality
- **Clean Text**: Proper punctuation and formatting
- **Timestamps**: Optional timestamp markers for audio segments
- **Speaker Detection**: Identifies different speakers when possible
- **Confidence Scores**: Shows transcription confidence levels
- **Language Detection**: Displays detected language with native name

### Output Features

#### 📄 Text Display
- Clean, formatted text output in the interface
- Copy-to-clipboard functionality
- Download as .txt file option
- Real-time transcription progress with timer
- **Progress Tracking**: Visual progress bar with percentage and time elapsed
- **Timeout Protection**: 2-minute timeout with user cancellation option

#### ⬇️ Download Options
- Download transcribed text as .txt files
- Automatic file naming based on source
- UTF-8 encoding for international character support
- **File Naming**: Includes source name and timestamp

---

## 🧩 API Endpoints

### Main Transcription Endpoint
```
POST /api/transcribe
```

**Request Parameters:**
- `file` (optional): Uploaded audio/video file
- `youtube_url` (optional): YouTube video URL
- `language` (optional): Language hint for transcription
- `timestamp` (optional): Include timestamps in output

**Response:**
```json
{
  "text": "Transcribed text content...",
  "language": "en",
  "duration": 120.5,
  "segments": [...],
  "model": "whisper-1",
  "success": true
}
```

**Error Response:**
```json
{
  "error": "Error description",
  "success": false
}
```

### Additional Endpoints
- `GET /`: Main web interface
- `GET /api/languages`: Get supported languages
- `GET /health`: Health check endpoint

---

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description | Required |
|----------|---------|-------------|----------|
| `OPENAI_API_KEY` | - | Your OpenAI API key for Whisper API | ✅ Yes |
| `WHISPER_MODEL` | `whisper-1` | Whisper model to use for transcription | ❌ No |
| `MAX_FILE_SIZE` | `26214400` | Maximum file size in bytes (25MB) | ❌ No |
| `PORT` | `8010` | Server port number | ❌ No |
| `INCLUDE_TIMESTAMPS` | `false` | Include timestamps in output | ❌ No |

### File Size Limits
- **Default**: 25MB (26,214,400 bytes)
- **Audio Formats**: MP3, WAV, M4A, OGG, FLAC
- **Video Formats**: MP4, AVI, MOV, MKV, WMV
- **YouTube**: No size limit (but processing time increases)

### Whisper Model Settings

#### OpenAI Whisper (Default)
- **Model**: `whisper-1` (latest and most accurate)
- **Languages**: 100+ languages supported
- **Quality**: High-accuracy transcription with punctuation
- **Features**: Automatic language detection, speaker diarization
- **Cost**: Pay-per-use based on audio duration

---

## 📁 Project Structure

```
11_SpeechToTextAgent/
├── server.py                 # FastAPI application and routes
├── stt_service.py            # Speech-to-text engine logic and OpenAI Whisper integration
├── audio_processor.py        # Audio/video processing utilities
├── youtube_processor.py      # YouTube video processing
├── config.py                 # Configuration and environment variables
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
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
- **Real-time Feedback**: Loading states, progress bars, and success indicators
- **Progress Tracking**: Visual progress bar with percentage and elapsed time
- **Timeout Protection**: 2-minute timeout with user cancellation
- **Accessibility**: Proper labels, focus states, and keyboard navigation
- **Modern Icons**: Font Awesome icons throughout the interface

### Interactive Elements
- **Input Method Selection**: Three distinct cards for different input types
- **Drag & Drop**: Intuitive file upload with visual feedback
- **Progress Visualization**: Animated waveform during processing
- **Real-time Timer**: Countdown timer showing elapsed time
- **Cancel Button**: User-initiated cancellation of ongoing transcription

---

## 🔍 Debugging & Logs

### Server Logs
The server provides detailed logging for troubleshooting:

```bash
# Start server with verbose logging
python server.py

# Look for these log levels:
INFO:     Starting up
INFO:     Processing uploaded file: filename.ext
INFO:     File processed: filename.ext
INFO:     Starting transcription...
INFO:     Transcription completed successfully
ERROR:    Transcription failed: error details
```

### Common Log Messages

#### Successful Processing
```
INFO:server:Processing uploaded file: speech.mp3
INFO:audio_processor:Converting audio to WAV: temp_file.mp3
INFO:audio_processor:Audio converted to WAV successfully: temp_file.wav
INFO:server:File processed: temp_file.mp3
INFO:server:Starting transcription...
INFO:stt_service:Starting transcription of: temp_file.wav
INFO:stt_service:Sending audio to OpenAI Whisper API...
INFO:stt_service:Transcription completed successfully. Language: en, Duration: 45.2s
```

#### Error Scenarios
```
ERROR:stt_service:Transcription failed: 'Transcription' object has no attribute 'language'
ERROR:server:Transcription error: Transcription failed: 'Transcription' object has no attribute 'language'
ERROR:audio_processor:Failed to clean up file: [WinError 32] The process cannot access the file
```

### Browser Console
Check browser developer tools (F12) for JavaScript errors:
- **Network tab**: Monitor API requests and responses
- **Console tab**: JavaScript errors and warnings
- **Application tab**: Check if files are being uploaded correctly

---

## 🚀 Performance & Optimization

### Processing Times
- **Small files (< 1MB)**: 5-15 seconds
- **Medium files (1-10MB)**: 15-60 seconds
- **Large files (10-25MB)**: 1-3 minutes
- **YouTube videos**: 2-5 minutes (depends on length and quality)

### Optimization Tips
1. **Use appropriate audio quality**: Higher quality = longer processing time
2. **Convert to WAV**: WAV files process faster than MP3
3. **Limit file size**: Stay under 25MB for best performance
4. **Check internet speed**: Faster upload = faster processing
5. **Use language hints**: Specify language for faster detection

### Memory Usage
- **Peak memory**: ~100-200MB during processing
- **Temporary files**: Automatically cleaned up after processing
- **Cache**: No persistent caching (session-based)

---

## 🔮 Future Enhancements

Potential improvements for future versions:
- **Real-time Transcription**: Live audio streaming and transcription
- **Batch Processing**: Transcribe multiple files at once
- **Custom Models**: Fine-tuned Whisper models for specific domains
- **Audio Editing**: Basic audio editing and enhancement
- **Translation**: Automatic translation of transcribed text
- **Mobile App**: Native mobile applications
- **API Rate Limiting**: Better handling of API quotas
- **Audio Preview**: Sample audio playback before transcription
- **Export Formats**: Support for SRT, VTT, and other subtitle formats
- **Offline Processing**: Local Whisper model support
- **Cloud Storage**: Integration with Google Drive, Dropbox, etc.

---

## 📝 License

This project is part of the #100DaysOfAI-Agents challenge by Muhammad Sami Asghar Mughal.

---

## 🤝 Contributing

Feel free to contribute to this project by:
- Reporting bugs and issues
- Suggesting new features and improvements
- Improving documentation and code quality
- Adding new transcription engines or language support
- Enhancing the user interface and experience
- Adding more language support and localization

---

## 🙏 Acknowledgments

- **OpenAI**: For providing the Whisper API and transcription models
- **FastAPI**: For the modern, fast web framework
- **Tailwind CSS**: For the beautiful, responsive design system
- **Font Awesome**: For the comprehensive icon library
- **pydub**: For audio processing capabilities
- **moviepy**: For video processing and audio extraction
- **yt-dlp**: For YouTube video processing
- **FFmpeg**: For audio/video format conversion and processing

---

## 📞 Support & Community

### Getting Help
1. **Check this README** for common issues and solutions
2. **Review server logs** for detailed error information
3. **Check browser console** for frontend issues
4. **Verify FFmpeg installation** if audio/video processing fails
5. **Test with simple files** before trying complex ones

### Common Questions

**Q: Why is my transcription taking so long?**
A: Large files (>10MB) take longer to process. Check your file size and consider compressing audio files.

**Q: Can I transcribe videos without audio?**
A: No, the system requires audio content to transcribe. Videos without audio will fail.

**Q: Why does YouTube transcription fail?**
A: Check if the video is public, has audio, and isn't age-restricted. Some videos may be blocked in your region.

**Q: How accurate is the transcription?**
A: OpenAI Whisper provides high-accuracy transcription, especially for clear audio. Background noise may reduce accuracy.

**Q: Can I use this offline?**
A: No, this requires an internet connection for the OpenAI API and YouTube processing.

---

**Happy Speech-to-Text Conversion! 🎉**

*Transform your audio and video content into searchable, editable text with AI-powered transcription technology.*

---

## 🔄 Version History

- **v1.0.0** - Initial release with basic audio transcription
- **v1.1.0** - Added video file support and audio extraction
- **v1.2.0** - Added YouTube URL processing
- **v1.3.0** - Enhanced language support for South Asian languages
- **v1.4.0** - Added progress tracking and timeout protection
- **v1.5.0** - Improved error handling and user experience
