# 🌤️ Weather Speaker Agent - Day 2

A sophisticated AI-powered weather assistant that combines live weather data with natural language processing and text-to-speech capabilities. Built for Day 2 of the 100 Days of AI Agents challenge.

## ✨ Features

### 🎨 Beautiful UI
- **Modern Design**: Clean, responsive interface with glassmorphism effects
- **Tailwind CSS**: Beautiful styling with smooth animations and transitions
- **Mobile Responsive**: Works perfectly on desktop, tablet, and mobile devices
- **Interactive Elements**: Loading animations, particle effects, and smooth scrolling

### 🤖 AI-Powered Intelligence
- **OpenAI Integration**: Uses GPT-4o-mini for natural weather descriptions
- **Smart Responses**: Conversational weather reports with personalized tips
- **Context Awareness**: AI understands weather conditions and provides relevant advice

### 🌍 Live Weather Data
- **Real-time Data**: Uses Open-Meteo API for accurate, up-to-date weather information
- **Global Coverage**: Supports cities worldwide with automatic geocoding
- **Comprehensive Data**: Temperature, humidity, wind, precipitation, and forecasts

### 🔊 Voice Capabilities
- **Text-to-Speech**: Natural voice output using pyttsx3 and gTTS
- **Voice Control**: Toggle voice on/off and stop ongoing speech
- **Multiple TTS Engines**: Fallback support for different platforms

### 🚀 Fast & Reliable
- **FastAPI Backend**: High-performance async API
- **Error Handling**: Graceful error management with user-friendly messages
- **Caching**: Optimized for fast responses

## 🛠️ Technology Stack

### Frontend
- **HTML5**: Semantic markup
- **Tailwind CSS**: Utility-first CSS framework
- **Vanilla JavaScript**: Modern ES6+ features
- **Responsive Design**: Mobile-first approach

### Backend
- **FastAPI**: Modern, fast web framework
- **Python 3.8+**: Async/await support
- **OpenAI SDK**: GPT-4o-mini integration
- **Requests**: HTTP client for weather API

### APIs & Services
- **Open-Meteo**: Free weather data API
- **OpenAI GPT-4o-mini**: Natural language processing
- **Geocoding API**: City to coordinates conversion

### Voice & Audio
- **pyttsx3**: Cross-platform text-to-speech
- **gTTS**: Google Text-to-Speech fallback
- **Async Audio**: Non-blocking voice playback

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- Internet connection

### Quick Setup (Windows)

1. **Run the installation script**
   ```bash
   install.bat
   ```

2. **Edit the .env file**
   Add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Start the application**
   ```bash
   start.bat
   ```

### Manual Setup

1. **Clone the repository**
   ```bash
   cd 02_WeatherSpeaker
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

6. **Run the application**
   ```bash
   python main.py
   ```

7. **Open your browser**
   Navigate to `http://localhost:8000`

## 🎯 Usage

### Basic Usage
1. Enter a city name in the input field
2. Toggle voice output if desired
3. Click "Get Weather" or press Enter
4. View the beautiful weather display with AI-enhanced descriptions
5. Get additional weather tips by clicking "Get More Tips"

### Voice Features
- **Enable Voice**: Check the "Enable Voice Output" checkbox
- **Stop Voice**: Click the stop button to halt ongoing speech
- **Voice Content**: Hear natural language weather descriptions

### Advanced Features
- **Weather Tips**: Get AI-generated recommendations based on current conditions
- **Error Handling**: Clear error messages for invalid cities or network issues
- **Responsive Design**: Works on all device sizes

## 🏗️ Project Structure

```
02_WeatherSpeaker/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration and environment variables
├── ai_agent.py            # OpenAI integration and AI logic
├── weather_service.py     # Weather API integration
├── tts_service.py         # Text-to-speech functionality
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── install.bat           # Windows installation script
├── start.bat             # Windows startup script
├── demo.py               # Demo script
├── test_installation.py  # Installation verification
├── templates/
│   └── index.html        # Main HTML template
└── static/
    └── js/
        └── app.js        # Frontend JavaScript
```

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: GPT model to use (default: gpt-4o-mini)
- `TTS_ENABLED`: Enable/disable voice features (default: true)
- `TTS_LANGUAGE`: Voice language (default: en)
- `TTS_VOICE_RATE`: Speech rate (default: 150)

### API Endpoints
- `GET /`: Main weather interface
- `POST /api/weather`: Get weather data with AI enhancement
- `POST /api/weather/tips`: Get AI-generated weather tips
- `POST /api/voice/stop`: Stop ongoing voice output
- `GET /api/health`: Health check endpoint

## 🎨 UI Features

### Visual Design
- **Gradient Background**: Beautiful purple-blue gradient
- **Glassmorphism**: Modern glass-like card effects
- **Smooth Animations**: Fade-in and slide-up animations
- **Particle Effects**: Floating background particles
- **Responsive Grid**: Adaptive layout for all screen sizes

### Interactive Elements
- **Loading States**: Spinning indicators during API calls
- **Hover Effects**: Smooth transitions on interactive elements
- **Form Validation**: Real-time input validation
- **Error Display**: User-friendly error messages

## 🚀 Performance Features

### Optimization
- **Async Operations**: Non-blocking API calls
- **Error Recovery**: Graceful fallbacks for API failures
- **Caching**: Efficient data handling
- **Minimal Dependencies**: Lightweight package requirements

### Scalability
- **Modular Architecture**: Easy to extend and modify
- **API-First Design**: Clean separation of concerns
- **Stateless Operations**: No server-side state management

## 🐛 Troubleshooting

### Common Issues

1. **OpenAI Client Error: "proxies" argument**
   ```
   TypeError: Client.__init__() got an unexpected keyword argument 'proxies'
   ```
   **Solution**: This is a dependency version conflict. Use the installation script:
   ```bash
   install.bat
   ```
   Or manually install compatible versions:
   ```bash
   pip install httpx==0.25.2
   pip install openai==1.3.7
   ```

2. **OpenAI API Key Error**
   - Ensure your API key is correctly set in the `.env` file
   - Verify the key has sufficient credits
   - Check that the key is valid and active

3. **Voice Not Working**
   - Check if TTS is enabled in configuration
   - Install system audio drivers
   - Try the gTTS fallback option
   - On Windows, ensure Windows Media Player is installed

4. **City Not Found**
   - Check spelling and try alternative names
   - Use English city names for best results
   - Try adding country name (e.g., "London, UK")

5. **Network Errors**
   - Verify internet connection
   - Check firewall settings
   - Ensure weather API is accessible
   - Try using a VPN if geo-restricted

6. **Port Already in Use**
   - Change the port in `config.py`:
     ```python
     PORT = 8001  # or any available port
     ```

### Debug Mode
Enable debug mode by setting `DEBUG = True` in `config.py` for detailed logging.

### Installation Verification
Run the test script to verify your installation:
```bash
python test_installation.py
```

### Dependency Conflicts
If you encounter dependency conflicts:

1. **Clean installation**:
   ```bash
   # Remove existing environment
   rmdir /s /q venv
   
   # Reinstall with specific versions
   install.bat
   ```

2. **Manual dependency resolution**:
   ```bash
   pip install --upgrade pip
   pip install httpx==0.25.2
   pip install openai==1.3.7
   pip install -r requirements.txt
   ```

## 🤝 Contributing

This project is part of the 100 Days of AI Agents challenge. Feel free to:
- Report bugs and issues
- Suggest new features
- Submit pull requests
- Share your improvements

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Open-Meteo**: Free weather data API
- **OpenAI**: GPT-4o-mini for natural language processing
- **Tailwind CSS**: Beautiful UI framework
- **FastAPI**: Modern Python web framework

---

**Built with ❤️ for Day 2 of 100 Days of AI Agents**

*Experience the future of weather information with AI-powered insights and natural voice interaction!* 