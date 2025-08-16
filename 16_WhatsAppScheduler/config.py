"""
Configuration file for WhatsApp Scheduler Agent
Customize settings here
"""

# WhatsApp Web Settings
WHATSAPP_WEB_URL = "https://web.whatsapp.com"
WAIT_TIME = 20  # Seconds to wait for WhatsApp Web to load (increased for reliability)
TAB_CLOSE = True  # Close browser tab after sending message

# Message Scheduling Settings
DEFAULT_DELAY_SECONDS = 30  # Default delay if no time specified (30 seconds)
MIN_DELAY_SECONDS = 30  # Minimum delay required for WhatsApp Web loading
MAX_MESSAGE_LENGTH = 1000  # Maximum message length
MAX_SCHEDULED_MESSAGES = 50  # Maximum number of scheduled messages

# Reliability Settings
ENABLE_MESSAGE_VERIFICATION = True  # Enable message delivery verification
VERIFICATION_TIMEOUT = 10  # Seconds to wait for verification
RETRY_FAILED_MESSAGES = True  # Automatically retry failed messages
MAX_RETRY_ATTEMPTS = 3  # Maximum retry attempts for failed messages
RETRY_DELAY_SECONDS = 60  # Delay between retry attempts

# Debug Settings
DEBUG_MODE = False  # Enable debug mode for development
LOG_VERBOSE = False  # Log detailed information about message sending
SHOW_BROWSER_ACTIONS = True  # Show browser actions during sending

# File Settings
DATA_FILE = "scheduled_messages.json"  # File to store scheduled messages
LOG_FILE = "whatsapp_scheduler.log"  # Log file (optional)

# Validation Settings
PHONE_NUMBER_REGEX = r'^\+[1-9]\d{10,14}$'  # Phone number validation regex
TIME_FORMAT = "%H:%M"  # Time format for input validation

# UI Settings
ENABLE_EMOJIS = True  # Enable emoji display in CLI
ENABLE_COLORS = True  # Enable colored output (if supported)
SHOW_PREVIEW_LENGTH = 30  # Length of message preview in list

# Error Handling
MAX_RETRY_ATTEMPTS = 3  # Maximum retry attempts for failed messages
RETRY_DELAY_SECONDS = 60  # Delay between retry attempts

# Browser Settings
BROWSER_TYPE = "chrome"  # Browser to use (chrome, firefox, edge)
HEADLESS_MODE = False  # Run browser in headless mode (no GUI)
BROWSER_TIMEOUT = 30  # Browser timeout in seconds

# Development Settings
DEMO_MODE = False  # Enable demo mode (no actual messages sent)
