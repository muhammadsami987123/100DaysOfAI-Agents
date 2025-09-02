"""
Configuration file for SystemMonitorAgent
"""
import os
from typing import Dict, Any

# System monitoring configuration
DEFAULT_REFRESH_INTERVAL = 5  # seconds
DEFAULT_ALERT_THRESHOLDS = {
    'cpu': 80.0,      # CPU usage percentage
    'ram': 85.0,      # RAM usage percentage
    'disk': 90.0      # Disk usage percentage
}

# Export configuration
EXPORT_FORMATS = ['json', 'txt', 'csv']
DEFAULT_EXPORT_FORMAT = 'json'
LOG_FILE = 'system_monitor.log'

# OpenAI API configuration (optional)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_MODEL = 'gpt-4o-mini'
OPENAI_MAX_TOKENS = 200

# Display configuration
ENABLE_COLORS = True
ENABLE_EMOJIS = True
PROCESS_LIMIT = 10  # Number of top processes to show

# File paths
OUTPUT_DIR = 'exports'
LOG_DIR = 'logs'

# Ensure directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
