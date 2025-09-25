# 🔧 AppUninstaller - Day 54 of #100DaysOfAI-Agents

<div align="center">

![AppUninstaller Banner](https://img.shields.io/badge/AppUninstaller-Day%2054-blue?style=for-the-badge&logo=windows&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![Voice Control](https://img.shields.io/badge/Voice%20Control-Enabled-red?style=for-the-badge&logo=google-assistant&logoColor=white)

**Intelligent voice-controlled agent to manage and uninstall applications effortlessly**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎭 Examples](#-examples) • [📚 Documentation](#-documentation) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is AppUninstaller?

AppUninstaller is an intelligent AI agent designed to simplify the process of managing and uninstalling applications from your Windows system using natural language voice commands. This tool is built to provide a hands-free, accessible, and efficient way to clean up your system, making it ideal for various users, including those who are visually impaired, elderly, or simply prefer voice interaction.

### 🌟 Key Highlights

- **🗣️ Voice-Controlled**: Interact with the uninstaller using natural language.
- **🗑️ Intelligent Uninstallation**: Remove applications with simple commands like "Uninstall Zoom."
- **🔍 Smart Listing**: Voice-based app listing with optional filters.
- **✅ Confirmation Prompts**: Prevents accidental uninstallation with verbal confirmation.
- **📊 Flexible Filters**: Filter applications by size, last used date, and category (expandable).
- **Accessibility**: Enhances usability for visually impaired and non-tech-savvy users.

## 🎯 Features

### 🚀 Core Functionality
- ✅ **Voice Command Processing**: Understands and acts on spoken commands.
- ✅ **Text-to-Speech Feedback**: Provides verbal responses and confirmations.
- ✅ **Application Detection**: Accurately identifies installed applications on Windows.
- ✅ **Registry Integration**: Fetches uninstall strings and other app details from the Windows Registry.
- ✅ **WMI Integration**: Utilizes WMI for more comprehensive system information (planned expansion).

### 📊 Management & Filtering
- ✅ **List Applications**: Verbally lists all or filtered installed applications.
- ✅ **Filter by Name**: Find applications by spoken name.
- ✅ **Filter by Size**: Identify large applications for cleanup.
- ✅ **Filter by Last Used Date**: Discover unused applications (e.g., "Clear apps I haven’t used in 30 days").
- 📝 **Category Filtering (Planned)**: Group applications by type (e.g., games, utilities).

### 🛡️ Safety & Usability
- ✅ **Confirmation Prompts**: Requires verbal confirmation before proceeding with uninstallation.
- 📝 **"Without Confirmation" Option (Planned)**: Bypass prompts for advanced users.
- ✅ **Error Handling**: Provides clear feedback on uninstallation failures.

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.8+** installed on your system.
- **Windows Operating System**: This agent is specifically designed for Windows.
- **Microphone**: For voice input.
- **Speakers/Headphones**: For AI voice feedback.
- **OpenAI API Key** (optional for future AI-powered enhancements, but included in `config.py`).

### 🔧 Manual Installation

```bash
# 1. Clone or download the project
git clone <repository-url>
cd 54_AppUninstaller

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows
vvenv\Scripts\activate
# Linux/Mac (if running on other OS for dev/testing)
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up environment variables (if using OpenAI API)
echo OPENAI_API_KEY=your_api_key_here > .env
```

### 🎯 First Run

```bash
# Run the AppUninstaller agent
python main.py
```

### 🧪 Verify Installation

Run the agent and try the following commands:

1.  **"List apps"**: The agent should verbally list installed applications.
2.  **"Uninstall [App Name]"**: The agent should prompt for confirmation and attempt uninstallation.

## 🎭 Examples & Usage

### 🗣️ Voice Commands

AppUninstaller responds to a variety of natural language commands:

-   **"Uninstall [App Name]"**: Initiates the uninstallation process for the specified application.
    *Example: "Uninstall Zoom"*
-   **"Remove [App Name]"**: Alias for uninstall.
    *Example: "Remove Spotify"*
-   **"Uninstall [App Name] without confirmation"**: Uninstalls without asking for a verbal 'yes'.
    *Example: "Uninstall VLC media player without confirmation"*
-   **"List apps"**: Lists all detected installed applications.
-   **"List applications"**: Alias for list apps.
-   **"Clear apps I haven't used in 30 days"**: Lists applications not used for more than 30 days.
    *Example: "Clear apps I haven't used in 90 days"*
-   **"Show me big apps" (Planned)**: Lists applications larger than a certain size.

### 💻 CLI Interaction

While primarily voice-controlled, the agent provides console output for debugging and visibility into its operations.

## 🏗️ Project Architecture

### 📁 File Structure

```
54_AppUninstaller/
├── 📄 README.md                 # This comprehensive documentation
├── 📋 requirements.txt          # Python dependencies
├── ⚙️ config.py                 # Configuration and settings management
├── 🚀 main.py                   # Main entry point for the agent
└── 🤖 app_uninstaller_agent.py  # Core logic for app uninstallation and voice interaction
```

### 🔧 Technical Stack

| Component        | Technology           | Purpose                                    |
|------------------|----------------------|--------------------------------------------|
| **Voice Input**  | `SpeechRecognition`  | Transcribing speech to text                |
| **Voice Output** | `pyttsx3`            | Converting text to speech                  |
| **App Listing**  | `winreg`, `wmi`      | Interacting with Windows Registry and WMI for app data |
| **App Uninstall**| `subprocess`         | Executing uninstall commands               |
| **Audio Playback** | `pygame`             | (Optional) For custom audio prompts/feedback |
| **Environment**  | `python-dotenv`      | Managing environment variables             |

### 🎯 Key Components

#### 🤖 AppUninstallerAgent (`app_uninstaller_agent.py`)
-   **Voice I/O**: Handles speech recognition and text-to-speech.
-   **Application Discovery**: Scans Windows Registry for installed programs.
-   **Uninstallation Logic**: Executes uninstall commands safely with confirmation.
-   **Command Processing**: Interprets user voice commands and triggers actions.
-   **Filtering**: Applies criteria (name, size, date) to list applications.

#### ⚙️ Configuration (`config.py`)
-   **API Keys**: Stores `OPENAI_API_KEY` (if used for future AI enhancements).
-   **Voice Prompts**: Customizable greeting, confirmation, and error messages.
-   **Timeouts**: Configures voice input listening durations.

#### 🚀 Main Entry Point (`main.py`)
-   Initializes the `AppUninstallerAgent`.
-   Manages the continuous listening loop for voice commands.
-   Integrates `pygame` for potential audio feedback (e.g., alert sounds).

## ⚙️ Configuration & Setup

### 🔑 API Key Setup (Optional)

If you plan to extend the agent with more advanced AI functionalities requiring OpenAI:

**Step 1: Get OpenAI API Key**
1.  Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2.  Sign up or log in to your account
3.  Navigate to "API Keys" section
4.  Create a new API key
5.  Copy the key (starts with `sk-`)

**Step 2: Configure the Key**

```bash
# Option 1: Environment Variable (Recommended)
# Windows
set OPENAI_API_KEY=sk-your_actual_api_key_here

# Linux/Mac
export OPENAI_API_KEY=sk-your_actual_api_key_here

# Option 2: .env File
echo OPENAI_API_KEY=sk-your_actual_api_key_here > .env
```

### 🎛️ Advanced Configuration

Edit `config.py` to customize the agent's behavior and messages:

```python
# Voice instructions and prompts
GREETING_MESSAGE = "Hello! I am App Uninstaller..."
UNINSTALL_CONFIRMATION_PROMPT = "Are you sure you want to uninstall {}?..."
APP_NOT_FOUND_MESSAGE = "I could not find an app named {}...."

# Other configurations
VOICE_INPUT_TIMEOUT = 5 # seconds
VOICE_INPUT_PHRASE_TIME_LIMIT = 10 # seconds
```

## 🧪 Testing & Quality Assurance

### 🔍 Installation & Functionality Testing

1.  **Verify Dependencies**: Ensure all packages in `requirements.txt` are installed.
2.  **Run `main.py`**: Start the agent.
3.  **Voice Commands**: Test the following scenarios:
    *   "List apps" - Check if applications are listed correctly.
    *   "Uninstall [Existing App Name]" - Verify confirmation and uninstallation attempt.
    *   "Uninstall [Non-existent App Name]" - Confirm appropriate error message.
    *   "Clear apps I haven't used in X days" - Test filtering by date.

### 🐛 Troubleshooting

**Common Issues & Solutions:**

| Issue                                  | Cause                                       | Solution                                                                |
|----------------------------------------|---------------------------------------------|-------------------------------------------------------------------------|
| **`SpeechRecognition` errors**         | Missing audio input device or drivers       | Ensure microphone is connected and drivers are up to date.              |
| **`pyttsx3` errors**                   | Missing text-to-speech engine               | Check Windows TTS settings; ensure voices are installed.                 |
| **"App not found"**                   | Incorrect app name or app not in registry   | Try different variations of the app name; verify app is truly installed. |
| **Uninstallation failure**             | Insufficient privileges or app is running   | Run the script as Administrator; close the application before uninstalling. |
| **`winreg` or `wmi` access issues**    | Permissions or system integrity             | Ensure script has necessary permissions (run as Admin).                 |

## 🔮 Future Roadmap

### 🚀 Planned Features

| Feature                       | Status    | Description                                                     |
|-------------------------------|-----------|-----------------------------------------------------------------|
| **UI-Based Interaction**      | 🔄 Planned | Develop a simple graphical interface for visual interaction.       |
| **Advanced Filtering**        | 🔄 Planned | Filter by app category, publisher, installation source.         |
| **Batch Uninstallation**      | 🔄 Planned | Uninstall multiple selected apps at once (e.g., "Remove all games").|
| **Usage Tracking**            | 🔄 Planned | Monitor app usage to suggest uninstallation of idle apps.       |
| **System Restore Point**      | 🔄 Planned | Create a restore point before critical uninstallations.         |
| **Dependency Analysis**       | 🔄 Planned | Identify and warn about dependent applications.                 |
| **Cloud Integration**         | 🔄 Planned | Synchronize app lists and preferences across devices.             |

### 🎯 Enhancement Ideas

-   **Voice Assistant Integration**: Integrate with existing voice assistants (e.g., Cortana, Alexa).
-   **Machine Learning**: Improve natural language understanding for more complex commands.
-   **Cross-Platform Support**: Extend to macOS and Linux (requires platform-specific uninstallation methods).
-   **Customizable Voice**: Allow users to select different AI voices.
-   **Configuration UI**: A simple web interface to manage agent settings.

## 🤝 Contributing

We welcome contributions to make AppUninstaller even more powerful and user-friendly!

### 🛠️ How to Contribute

1.  **Fork the repository**.
2.  **Create a feature branch**: `git checkout -b feature/your-feature-name`.
3.  **Implement your changes** and test thoroughly.
4.  **Commit your changes**: `git commit -m 'Add your amazing feature'`.
5.  **Push to the branch**: `git push origin feature/your-feature-name`.
6.  **Open a Pull Request**.

### 🎯 Areas for Contribution

-   Implementing new filtering options (e.g., by app category).
-   Adding a simple UI for listing and selecting apps.
-   Improving voice command parsing and robustness.
-   Enhancing cross-platform compatibility (e.g., macOS, Linux support).
-   Expanding the `get_installed_applications` logic to capture more details.
-   Bug fixes and performance optimizations.

### 📋 Contribution Guidelines

-   Follow the existing code style.
-   Add comments where necessary to explain complex logic.
-   Ensure all tests (manual or automated) pass.
-   Update documentation (`README.md`) for new features.

## 📞 Support & Community

### 🆘 Getting Help

1.  **📖 Documentation**: Refer to this `README.md` for installation and usage.
2.  **🐛 Troubleshooting**: Check the troubleshooting section for common issues.
3.  **💻 Console Output**: Review terminal logs for error messages.
4.  **GitHub Issues**: For bugs and feature requests, open an issue on the GitHub repository.

### 💬 Community

-   **GitHub Issues**: Report bugs, suggest features, and ask questions.
-   **Discussions**: Share your ideas and help others.

## 📄 License & Credits

### 📜 License

This project is part of the **#100DaysOfAI-Agents** challenge by **Muhammad Sami Asghar Mughal**.

**MIT License** - Feel free to use, modify, and distribute!

### 🙏 Acknowledgments

-   **`SpeechRecognition` & `pyttsx3`**: For enabling voice interaction.
-   **Python Community**: For the rich ecosystem of libraries.
-   **Windows API Documentation**: For guiding the system interaction.

### 🌟 Inspiration

Inspired by the need for accessible and intuitive system utility tools that leverage the power of voice AI for hands-free operation and enhanced user experience.

---

<div align="center">

## 🎉 Ready to Clean Up Your System?

**Empower your system maintenance with intelligent voice control!**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎭 Examples](#-examples) • [📚 Documentation](#-documentation)

---

**Made with ❤️ by the #100DaysOfAI-Agents community**

*Day 54 of 100 - Building the future of AI agents, one day at a time!*

</div>
