# Day 24: MoodMusicAgent – Emotion-Based Music Player

An intelligent agent that plays music based on the user's current mood or emotion, detected via voice input, text input, or manual selection.

## 🎵 Features

### Core Features
- **Mood Detection**: Accept mood via text prompt, voice input, or manual selection
- **Smart Music Selection**: Maps moods to music genres or playlists
- **Multiple Music Sources**: Integrates with Spotify, YouTube, or local MP3 files
- **CLI Interface**: Simple and intuitive command-line interface

### Mood Categories
- 🎉 **Happy** - Upbeat, cheerful music
- 😢 **Sad** - Soothing, melancholic tunes
- ⚡ **Energetic** - High-energy, motivational tracks
- 😌 **Relaxed** - Calm, ambient sounds
- 💕 **Romantic** - Love songs and ballads
- 😰 **Stressed** - Calming, stress-relief music
- 🚀 **Motivated** - Inspirational, driving beats
- 🎯 **Focus** - Concentration-enhancing tracks

## 🚀 Installation

1. **Clone and navigate to the project:**
   ```bash
   cd 24_MoodMusicAgent
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

4. **Run the agent:**
   ```bash
   python main.py
   ```

## 🎮 Usage

### CLI Interface
```bash
🎵 Welcome to MoodMusicAgent

What's your current mood?
> [Happy] [Sad] [Focus] [Romantic] [Stressed] [Motivated]

🔍 Finding upbeat playlists for you...

🎧 Now playing: "High Energy Workout Mix" via Spotify
```

### Voice Input (Optional)
- Say your mood out loud for hands-free operation
- The agent will transcribe and interpret your emotional state

### Manual Selection
- Choose from predefined mood categories
- Quick access to your favorite mood-music combinations

## 🔧 Configuration

### Environment Variables
- `SPOTIFY_CLIENT_ID`: Spotify API client ID
- `SPOTIFY_CLIENT_SECRET`: Spotify API client secret
- `YOUTUBE_API_KEY`: YouTube Data API key
- `OPENAI_API_KEY`: OpenAI API key for mood analysis

### Music Sources
- **Spotify**: Premium integration with mood-based playlists
- **YouTube**: Free music streaming with mood categorization
- **Local Files**: Play MP3 files from your music library

## 🎯 Advanced Features

### Mood History
- Track your mood patterns over time
- Learn your music preferences for different emotional states
- Personalized recommendations based on past choices

### Smart Volume Control
- Auto-adjust volume based on time of day
- Mood-appropriate volume levels (louder for energetic, softer for relaxed)

### AI-Powered Analysis
- Natural language processing for mood detection
- Context-aware music selection
- Continuous learning from user feedback

## 🛠️ Technical Details

### Architecture
- **Mood Detection Engine**: Analyzes text/voice input for emotional content
- **Music Mapping Service**: Connects moods to appropriate music genres
- **Player Interface**: Handles music playback across different platforms
- **Data Persistence**: Stores mood history and preferences

### Dependencies
- `spotipy`: Spotify Web API integration
- `youtube-search-python`: YouTube search functionality
- `pygame`: Audio playback for local files
- `openai`: AI-powered mood analysis
- `speech_recognition`: Voice input processing
- `pyttsx3`: Text-to-speech for feedback

## 📁 Project Structure

```
24_MoodMusicAgent/
├── main.py                 # Main application entry point
├── mood_detector.py        # Mood detection and analysis
├── music_service.py        # Music selection and playback
├── spotify_service.py      # Spotify API integration
├── youtube_service.py      # YouTube API integration
├── local_player.py         # Local MP3 file player
├── voice_interface.py      # Voice input/output handling
├── mood_history.py         # Mood tracking and analytics
├── config.py               # Configuration management
├── requirements.txt        # Python dependencies
├── env.example             # Environment variables template
├── install.bat             # Windows installation script
├── start.bat               # Windows startup script
└── README.md               # This file
```

## 🎵 Example Use Cases

### Morning Motivation
- Wake up feeling tired → Agent plays energetic workout music
- Need to focus on work → Agent selects concentration-enhancing tracks

### Evening Relaxation
- Feeling stressed from work → Agent plays calming ambient music
- Want to unwind → Agent selects relaxing instrumental pieces

### Social Situations
- Hosting a party → Agent plays upbeat party music
- Romantic dinner → Agent selects romantic ballads

## 🔮 Future Enhancements

- **Biometric Integration**: Heart rate and stress level monitoring
- **Weather Correlation**: Adjust music based on weather conditions
- **Social Sharing**: Share mood-music combinations with friends
- **Cross-Platform Sync**: Sync preferences across devices
- **Machine Learning**: Advanced mood prediction and music recommendation

## 🤝 Contributing

Feel free to contribute to this project by:
- Adding new mood categories
- Improving music selection algorithms
- Enhancing the voice interface
- Adding support for new music platforms

## 📄 License

This project is part of the 100 Days of AI Agents challenge. See LICENSE file for details.

---

**Happy listening! 🎧✨**
