# 📊 SystemMonitorAgent

**Day 32 of the 100 Days of AI Agents Series**

A powerful, lightweight CLI-based system monitoring agent that provides real-time insights into CPU, RAM, disk, and network usage with optional AI-powered optimization suggestions.

## 🎯 Features

### 🔍 Core Monitoring
- **Real-time Resource Tracking**: Monitor CPU, RAM, disk, and network usage
- **Process Analysis**: View top processes by resource consumption
- **Visual Progress Bars**: Color-coded resource bars for quick assessment
- **Threshold Alerts**: Configurable alerts for high resource usage

### 🚀 Advanced Features
- **Export Functionality**: Save stats in JSON, TXT, or CSV formats
- **Logging Mode**: Continuous monitoring with automatic data export
- **Custom Thresholds**: Set personalized alert levels
- **History Tracking**: Maintain monitoring history for trend analysis

### 🤖 AI Assistant (Optional)
- **Optimization Suggestions**: Get AI-powered performance tips
- **Health Assessment**: Receive intelligent system health scoring
- **Performance Analysis**: Context-aware recommendations

## 🛠 Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Quick Install

#### Windows
```bash
# Run the installer
install.bat

# Or manually install dependencies
pip install -r requirements.txt
```

#### Linux/macOS
```bash
# Make install script executable
chmod +x install.sh

# Run the installer
./install.sh

# Or manually install dependencies
pip3 install -r requirements.txt
```

## 🚀 Usage

### 🖥️ **Interactive CLI Interface (Recommended)**
```bash
# Start the beautiful interactive CLI
python cli.py
```

The interactive CLI provides:
- 📊 **Live Monitoring** with customizable settings
- 📸 **Single Snapshots** with AI analysis options
- 🤖 **AI Optimization** suggestions
- 🏥 **AI Health Assessment**
- 📤 **Data Export** in multiple formats
- ⚙️ **Custom Thresholds** configuration
- 📈 **History Summary** and statistics
- 🎯 **Quick Commands** reference

### 💻 **Command Line Interface**
```bash
# Start real-time monitoring (5s refresh)
python main.py

# Custom refresh interval (2 seconds)
python main.py -i 2

# Hide process list for cleaner output
python main.py --no-processes
```

### Single Snapshots
```bash
# Get current system stats and exit
python main.py --single

# Single snapshot with AI suggestions
python main.py --single --suggest

# Single snapshot with health assessment
python main.py --single --health
```

### Export & Logging
```bash
# Export current stats to JSON
python main.py --export json

# Export to different formats
python main.py --export txt
python main.py --export csv

# Enable logging mode (continuous export)
python main.py --log
```

### AI Features
```bash
# Get optimization suggestions
python main.py --suggest

# Get system health assessment
python main.py --health

# Combine AI features with monitoring
python main.py --suggest --health
```

### Custom Configuration
```bash
# Set custom alert thresholds (CPU RAM DISK)
python main.py --thresholds 70 80 85

# View monitoring history summary
python main.py --summary
```

## 🔧 Configuration

### Environment Variables
```bash
# For AI features (optional)
export OPENAI_API_KEY="your-api-key-here"

# Windows
set OPENAI_API_KEY=your-api-key-here
```

### Default Settings
- **Refresh Interval**: 5 seconds
- **Alert Thresholds**: CPU 80%, RAM 85%, Disk 90%
- **Process Limit**: Top 10 processes
- **History Size**: Last 100 readings

## 📊 Output Examples

### System Information
```
============================================================
                System Information
============================================================

Platform: win32
Python Version: 3.9.7 (default, Sep 16 2021, 16:59:28)
CPU Count: 8
CPU Freq: 3200.0 MHz
Boot Time: 2024-01-15T08:30:00
```

### Resource Monitoring
```
CPU Usage
---------
Usage: 45.2%
Bar:   █████████░░░░░░░░░░
Cores: 8
Freq:  3200 MHz

Memory Usage
------------
Usage: 67.8%
Bar:   ██████████████░░░░
Total: 16.0 GB
Used:  10.9 GB
Free:  5.1 GB
```

### AI Suggestions
```
🤖 AI Optimization Suggestions
-----------------------------
💡 AI Recommendations:
1. Close unnecessary browser tabs to reduce memory usage
2. Consider upgrading to 32GB RAM for better performance
3. Run disk cleanup to free up disk space
4. Check for background processes consuming CPU
```

## 🏗 Architecture

### Modular Design
- **`cli.py`**: Interactive CLI interface with Rich library (recommended)
- **`main.py`**: Traditional CLI interface with argument parsing
- **`monitor.py`**: Core system monitoring functionality
- **`ai_assistant.py`**: AI-powered optimization suggestions
- **`utils.py`**: Utility functions and formatting
- **`config.py`**: Configuration and constants

### Key Components
- **SystemMonitor**: Main monitoring class with resource collection
- **AIAssistant**: Optional OpenAI integration for smart suggestions
- **Export System**: Multi-format data export capabilities
- **Alert System**: Threshold-based notification system

## 🔒 Privacy & Security

- **Local-First**: All monitoring data stays on your machine
- **Optional AI**: OpenAI API only called when explicitly requested
- **No Data Collection**: No telemetry or external data transmission
- **Secure**: No sensitive system information is logged

## 🚨 Troubleshooting

### Common Issues

#### Import Errors
```bash
# Ensure dependencies are installed
pip install -r requirements.txt

# Check Python version
python --version
```

#### Permission Errors
```bash
# On Linux/macOS, run with sudo if needed
sudo python3 main.py

# Or adjust file permissions
chmod +x *.sh
```

#### AI Features Not Working
```bash
# Check API key is set
echo $OPENAI_API_KEY

# Verify internet connection
ping openai.com
```

### Performance Tips
- Use `--no-processes` for faster refresh rates
- Increase refresh interval for lower CPU usage
- Use `--single` mode for quick checks
- Enable logging only when needed

## 🔮 Future Enhancements

- **Web Dashboard**: Browser-based monitoring interface
- **Email Alerts**: Send notifications when thresholds are exceeded
- **Custom Metrics**: User-defined monitoring parameters
- **Performance Trends**: Historical analysis and predictions
- **Integration**: Connect with other monitoring tools

## 📝 License

This project is part of the 100 Days of AI Agents series. Feel free to use, modify, and distribute according to your needs.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## 📚 Related Projects

- **Day 1**: TodoAgent - Task management with AI
- **Day 2**: WeatherSpeaker - Voice-enabled weather updates
- **Day 3**: JarvisLauncher - Voice-controlled application launcher
- **Day 4**: EmailWriterAgent - AI-powered email composition
- **Day 5**: TranslatorAgent - Multi-language translation tool

---

**Built with ❤️ for developers, engineers, and system administrators who need powerful, lightweight system monitoring tools.**
