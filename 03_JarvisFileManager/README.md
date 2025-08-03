# Jarvis File Manager - Voice-Controlled Desktop Agent

A powerful voice-controlled desktop assistant that allows you to control your entire PC through natural language commands. Built with Python, OpenAI GPT, and speech recognition, this agent can manage files, folders, applications, and perform system operations using only your voice.

## 🎯 Features

### File & Folder Management
- **Create folders and files** in any directory
- **Rename items** with voice commands
- **Navigate directories** using natural language
- **Open folders** by name (Desktop, Downloads, Documents, etc.)

### Application Control
- **Open any installed application** by name
- **Close applications** with voice commands
- **Universal app recognition** using Start Menu shortcuts
- **Fuzzy matching** for app and folder names

### System Integration
- **Voice input/output** with real-time feedback
- **Conversational UI** with status indicators
- **Multi-language support** (English, with Urdu support ready)
- **Desktop application** (no browser required)

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Windows 10/11
- OpenAI API key
- Microphone and speakers

### Installation

1. **Clone or download the project:**
   ```bash
   cd 03_JarvisFileManager
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

### Combined Commands
```
"Go to Desktop and create a folder called Work"
"Open Downloads and make a file called todo.txt"
"Go to Documents, create a folder called Reports, and open it"
```

## 🏗️ Technical Architecture

### Core Components

- **`main.py`** - Application entry point
- **`ui.py`** - Tkinter-based desktop UI with status indicators
- **`voice.py`** - Speech recognition and text-to-speech handling
- **`agent.py`** - OpenAI integration and command processing

### Key Technologies

- **Speech Recognition:** Google Speech API via `SpeechRecognition`
- **Text-to-Speech:** `pyttsx3` for voice feedback
- **AI Processing:** OpenAI GPT-3.5-turbo for command interpretation
- **System Integration:** Python `os`, `subprocess`, and `pathlib`
- **UI Framework:** Tkinter for desktop application

### Intelligent Features

- **App Indexing:** Automatically discovers installed applications from Start Menu
- **Fuzzy Matching:** Intelligently matches spoken names to actual apps/folders
- **Context Awareness:** Maintains current directory state
- **Error Handling:** Graceful fallbacks and user feedback

## 🎨 User Interface

The application opens as a desktop window with:

- **Status Indicator:** Shows current state (Listening, Processing, Ready)
- **Last Command Display:** Shows your most recent voice command
- **Color-coded Feedback:** 
  - Blue: Listening for voice input
  - Orange: Processing with AI
  - Green: Success
  - Red: Error

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)

### Supported Applications
The agent can open/close any application found in your Start Menu, including:
- Notepad, Chrome, Firefox, Edge
- Visual Studio Code, PyCharm, Sublime Text
- Microsoft Office applications
- Windows built-in apps (Camera, Calculator, etc.)

### Supported Folders
- Desktop, Downloads, Documents
- Pictures, Music, Videos
- Any folder accessible from your user directory

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
- Check microphone permissions
- Ensure clear speech and minimal background noise
- Try speaking more slowly or clearly

**"App not found"**
- The app must be installed and have a Start Menu shortcut
- Try using the exact app name or a close variation

### Performance Tips

- **Clear speech:** Speak clearly and at a moderate pace
- **Quiet environment:** Minimize background noise
- **Specific commands:** Be specific about what you want to do
- **Wait for feedback:** Let the agent complete each action before giving the next command

## 🔮 Future Enhancements

Potential features for future versions:
- **File search and content reading**
- **System monitoring and alerts**
- **Automated workflows and scripting**
- **Integration with cloud storage**
- **Advanced natural language processing**
- **Custom voice commands and macros**

## 📝 License

This project is part of the "100 AI Agents in 100 Days" challenge.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the agent's capabilities.

## 📞 Support

If you encounter any issues or have questions, please check the troubleshooting section above or create an issue in the project repository.

---

**Enjoy controlling your PC with voice commands! 🎤✨** 