# WhatsApp Scheduler Agent - Day 16

A CLI-based WhatsApp message scheduler that allows you to auto-schedule WhatsApp messages using WhatsApp Web.

## 🚀 Features

- **Message Scheduling**: Schedule messages for specific times
- **Phone Number Validation**: Ensures proper phone number format
- **Persistent Storage**: Messages are saved between sessions
- **Status Tracking**: Monitor message status (scheduled, sending, sent, failed)
- **Error Handling**: Comprehensive error messages and tips
- **Message Verification**: Built-in verification to confirm message delivery
- **Diagnostic Tools**: Built-in tools to troubleshoot sending issues

## ⚠️ Important Notes

- **WhatsApp Web Required**: You must have WhatsApp Web open and logged in
- **Phone Number Format**: Use international format with country code (e.g., +1234567890)
- **Timing**: Messages need at least 30 seconds to ensure WhatsApp Web loads properly
- **Browser**: Chrome browser is recommended for best compatibility
- **Message Verification**: The agent will ask you to confirm if messages were actually delivered

## 🔧 Installation

### Prerequisites
- Python 3.7+
- Chrome browser
- WhatsApp account
- Internet connection

### Setup
1. **Clone or download** this project
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Test your setup** (recommended):
   ```bash
   python test_setup.py
   ```
4. **Run the agent**:
   ```bash
   python main.py
   ```

## 📱 Usage

### Basic Commands
- `schedule` - Schedule a new message
- `view` - List all scheduled messages
- `cancel <id>` - Cancel a scheduled message
- `clear` - Clear all failed messages
- `test` - Test WhatsApp Web connection
- `diagnose` - Diagnose common sending issues
- `help` - Show help information
- `exit` - Exit the application

### Scheduling a Message
1. Run `schedule` command
2. Enter phone number with country code (e.g., +1234567890)
3. Enter your message
4. Enter time in HH:MM format (or press Enter for 30 seconds from now)

## 🚨 Troubleshooting

### Common Issue: Messages Show as "Sent" But Don't Appear in WhatsApp

This is a known issue with WhatsApp Web automation. Here's how to diagnose and fix it:

#### 🔍 Quick Diagnosis
1. **Run the diagnose command**:
   ```
   diagnose
   ```
   This will check for common issues like:
   - pywhatkit installation problems
   - Browser accessibility issues
   - WhatsApp Web connectivity problems
   - Configuration issues

2. **Test WhatsApp Web connection**:
   ```
   test
   ```
   This will:
   - Open WhatsApp Web in your browser
   - Check if you're properly logged in
   - Optionally test with a message to yourself

#### 🛠️ Common Solutions

1. **WhatsApp Web Not Logged In**
   - Open WhatsApp Web manually in your browser
   - Scan the QR code with your phone
   - Ensure you stay logged in

2. **Phone Number Issues**
   - Verify the phone number includes country code (+1234567890)
   - Check if the number exists in WhatsApp
   - Try sending a message to yourself first

3. **Timing Issues**
   - Increase `WAIT_TIME` in `config.py` (default: 20 seconds)
   - Ensure WhatsApp Web has fully loaded before sending
   - Wait at least 30 seconds between messages

4. **Browser Issues**
   - Use Chrome browser (recommended)
   - Update Chrome to latest version
   - Check if Chrome is accessible from command line

5. **Network Issues**
   - Verify your internet connection
   - Check if WhatsApp is working on your phone
   - Try using a different network

#### 🔧 Advanced Troubleshooting

1. **Check Configuration**:
   ```python
   # In config.py, try these settings:
   WAIT_TIME = 30  # Increase wait time
   TAB_CLOSE = False  # Keep tabs open for debugging
   DEBUG_MODE = True  # Enable debug output
   ```

2. **Manual Verification**:
   - The agent will ask you to confirm if messages were delivered
   - Check your WhatsApp app for delivery checkmarks (✓✓)
   - Verify the recipient actually received the message

3. **Alternative Solutions**:
   - Use WhatsApp Business API for production use
   - Consider using Selenium for more reliable automation
   - Use official WhatsApp integration tools

#### 📋 Troubleshooting Checklist

- [ ] WhatsApp Web is open and logged in
- [ ] Phone number includes country code (+1234567890)
- [ ] Chrome browser is installed and updated
- [ ] Internet connection is stable
- [ ] WhatsApp is working on your phone
- [ ] Wait time is sufficient (at least 20 seconds)
- [ ] No other WhatsApp Web sessions are active
- [ ] Phone number exists in WhatsApp

#### 🆘 Still Having Issues?

If the problem persists:

1. **Check the logs**: Look for error messages in the terminal
2. **Try different timing**: Increase delays between messages
3. **Test with yourself**: Send a message to your own number first
4. **Restart WhatsApp Web**: Log out and log back in
5. **Check pywhatkit version**: Ensure you have the latest version
6. **Report the issue**: Include error messages and your configuration

## 📁 Project Structure

```
16_WhatsAppScheduler/
├── main.py              # Main application logic
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── scheduled_messages.json  # Stored messages (created automatically)
└── install.bat         # Windows installation script
```

## 🔒 Privacy & Security

- **Local Storage**: All data is stored locally on your computer
- **No Data Collection**: The agent doesn't collect or transmit your data
- **WhatsApp Web**: Uses official WhatsApp Web interface
- **Phone Numbers**: Stored locally for message management

## 📝 License

This project is part of the 100 Days of AI Agents challenge. Feel free to use and modify for educational purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

---

**Note**: This tool is for educational and personal use. Please respect WhatsApp's terms of service and use responsibly.
