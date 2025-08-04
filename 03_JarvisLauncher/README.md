# JarvisLauncher - Voice-Controlled Desktop Agent

A powerful, modern voice-controlled desktop assistant that allows you to control your entire PC through natural language commands. Built with Python, OpenAI GPT, and advanced speech recognition, this agent provides a seamless hands-free experience for managing files, folders, applications, and performing system operations.

## 🎯 Features

### 🎤 Voice Control
- **Hands-free operation** - No clicking required, just speak naturally
- **Automatic continuous listening** - Always ready for your commands
- **Multi-language support** - English, Urdu, and Hindi recognition
- **Real-time voice feedback** - Agent speaks back confirmations

### 📁 File & Folder Management
- **Create folders and files** in any directory with voice commands
- **Rename items** using natural language
- **Navigate directories** with simple voice instructions
- **Open folders** by name (Desktop, Downloads, Documents, etc.)
- **Universal folder access** - Works with any system directory

### 🖥️ Application Control
- **Open any installed application** by name
- **Close applications** with voice commands
- **Universal app recognition** using Start Menu shortcuts
- **Fuzzy matching** for app and folder names
- **System-wide control** - Access to all installed programs

### 🎨 Modern User Interface
- **Professional dark theme** with modern styling
- **Real-time status indicators** with animated feedback
- **Command history** with timestamps and responses
- **Visual listening indicator** - Animated dot shows active listening
- **Responsive design** - Smooth, non-blocking interface

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Windows 10/11
- OpenAI API key
- Microphone and speakers
- Internet connection for speech recognition

### Installation

1. **Clone or download the project:**
   ```bash
   cd 03_JarvisLauncher
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key:**
   Create a `.env` file in the project directory:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```

## 🎤 Usage Examples

### File Operations
```
"Create a folder called Invoices in Downloads"
"Make a file called notes.txt on Desktop"
"Rename folder Test to Work"
"Go to Documents and create a folder named Projects"
```

### Application Control
```
"Open Notepad"
"Open Visual Studio Code"
"Open Chrome"
"Close Notepad"
"Close Chrome"
```

### Folder Navigation
```
"Open my Downloads folder"
"Open Desktop"
"Go to Documents"
"Open Pictures folder"
```

### Multilingual Commands
**English:**
- "Open Notepad"
- "Create a folder called Work"

**Urdu:**
- "نوٹ پیڈ کھولیں" (Notepad kholo)
- "ورک نام کا فولڈر بنائیں" (Work naam ka folder banayein)

**Hindi:**
- "नोटपैड खोलें" (Notepad kholo)
- "वर्क नाम का फोल्डर बनाएं" (Work naam ka folder banayein)

### Combined Commands
```
"Go to Desktop and create a folder called Work"
"Open Downloads and make a file called todo.txt"
"Go to Documents, create a folder called Reports, and open it"
```

## 🏗️ Technical Architecture

### Core Components

- **`main.py`** - Application entry point
- **`ui.py`** - Modern Tkinter-based desktop UI with threading
- **`voice.py`** - Speech recognition and text-to-speech handling
- **`agent.py`** - OpenAI integration and intelligent command processing

### Key Technologies

- **Speech Recognition:** Google Speech API via `SpeechRecognition`
- **Text-to-Speech:** `pyttsx3` for voice feedback
- **AI Processing:** OpenAI GPT-3.5-turbo for command interpretation
- **System Integration:** Python `os`, `subprocess`, and `pathlib`
- **UI Framework:** Tkinter with modern styling and threading
- **Multilingual Support:** Language detection and processing

### Intelligent Features

- **App Indexing:** Automatically discovers installed applications from Start Menu
- **Fuzzy Matching:** Intelligently matches spoken names to actual apps/folders
- **Context Awareness:** Maintains current directory state
- **Error Handling:** Graceful fallbacks and user feedback
- **Continuous Listening:** Always-on voice recognition
- **Language Detection:** Automatic language identification

## 🎨 User Interface

The application features a modern, professional interface:

### Visual Elements
- **🎤 Title bar** with application branding
- **🎧 Status indicator** showing current state
- **🔴 Animated listening dot** - pulses when actively listening
- **Command display** showing last spoken command
- **Scrollable history** with timestamps and responses
- **Helpful instructions** at the bottom

### Status Indicators
- **🎧 Listening...** - Actively listening for voice input
- **⚙️ Processing command...** - Working on your request
- **✅ Command completed** - Successfully executed
- **❌ Error messages** - Clear error feedback

### Color Scheme
- **Dark theme** (#2c3e50, #34495e) for professional look
- **Blue accents** (#3498db) for status information
- **Red indicators** (#e74c3c) for active listening
- **Green success** (#27ae60) for completed actions

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)

### Supported Applications
The agent can open/close any application found in your Start Menu, including:
- **Text editors:** Notepad, Visual Studio Code, Sublime Text
- **Browsers:** Chrome, Firefox, Edge
- **Office apps:** Microsoft Office applications
- **System tools:** Calculator, Camera, File Explorer
- **Development tools:** PyCharm, IntelliJ, etc.

### Supported Folders
- **User folders:** Desktop, Downloads, Documents, Pictures, Music, Videos
- **System folders:** Any accessible directory on your system
- **Custom folders:** Any folder you can navigate to

## 🛠️ Troubleshooting

### Common Issues

**"No module named 'pyaudio'"**
```bash
# Install PyAudio using pipwin (recommended for Windows)
pip install pipwin
pipwin install pyaudio
```

**"OpenAI API key not found"**
- Ensure your `.env` file exists with the correct API key
- Check that `python-dotenv` is installed

**"Speech not recognized"**
- Check microphone permissions in Windows settings
- Ensure clear speech and minimal background noise
- Try speaking more slowly or clearly
- Verify internet connection for Google Speech API

**"App not found"**
- The app must be installed and have a Start Menu shortcut
- Try using the exact app name or a close variation
- Check if the app is in the Start Menu Programs folder

**"Listening timeout"**
- The app now uses automatic continuous listening
- No more timeout issues - just speak when ready
- Ensure microphone is working and not muted

### Performance Tips

- **Clear speech:** Speak clearly and at a moderate pace
- **Quiet environment:** Minimize background noise
- **Specific commands:** Be specific about what you want to do
- **Natural language:** Use natural phrases like "Open Notepad" or "Create a folder"
- **Wait for feedback:** Let the agent complete each action before giving the next command

## 🔮 Future Enhancements

Potential features for future versions:
- **File search and content reading**
- **System monitoring and alerts**
- **Automated workflows and scripting**
- **Integration with cloud storage**
- **Advanced natural language processing**
- **Custom voice commands and macros**
- **Voice wake word detection**
- **Integration with smart home devices**
- **Calendar and email management**
- **Web search and information retrieval**

## 📝 License

This project is part of the "100 AI Agents in 100 Days" challenge.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the agent's capabilities. We welcome contributions to make Jarvis even more powerful and user-friendly.

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the command examples
3. Ensure all dependencies are properly installed
4. Create an issue in the project repository with detailed information

## 🎉 What's New in This Version

- **Modern UI redesign** with professional dark theme
- **Automatic continuous listening** - no more button clicks
- **Multilingual support** for English, Urdu, and Hindi
- **Enhanced app recognition** with fuzzy matching
- **Real-time status indicators** with animations
- **Command history** with timestamps
- **Improved error handling** and user feedback
- **Threading support** for responsive interface

---

**Experience the future of desktop control with Jarvis - your intelligent voice assistant! 🎤✨** 
