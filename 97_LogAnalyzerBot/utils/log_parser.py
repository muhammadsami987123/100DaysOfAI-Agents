"""
Log Parser Utility
Handles parsing of various log formats
"""

import re
from datetime import datetime
from typing import List, Dict, Optional
from config import LOG_LEVELS, DEFAULT_DATE_FORMATS


class LogEntry:
    """Represents a single log entry"""
    
    def __init__(self, timestamp: Optional[datetime], level: str, source: str, message: str, raw_line: str):
        self.timestamp = timestamp
        self.level = level.upper() if level else 'UNKNOWN'
        self.source = source
        self.message = message
        self.raw_line = raw_line
    
    def to_dict(self):
        return {
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'level': self.level,
            'source': self.source,
            'message': self.message,
            'raw_line': self.raw_line
        }


class LogParser:
    """Parse various log formats"""
    
    def __init__(self):
        self.patterns = [
            # Pattern 1: [YYYY-MM-DD HH:MM:SS] LEVEL [source] message
            re.compile(r'\[(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}(?:\.\d+)?)\]\s*(\w+)\s*\[([^\]]+)\]\s*(.+)'),
            
            # Pattern 2: YYYY-MM-DD HH:MM:SS LEVEL source: message
            re.compile(r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}(?:\.\d+)?)\s+(\w+)\s+([^:]+):\s*(.+)'),
            
            # Pattern 3: YYYY-MM-DD HH:MM:SS,mmm LEVEL module - message
            re.compile(r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2},\d+)\s+(\w+)\s+([^\-]+)\s*-\s*(.+)'),
            
            # Pattern 4: Mon DD HH:MM:SS hostname source: message
            re.compile(r'(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+\S+\s+([^:]+):\s*(.+)'),
            
            # Pattern 5: LEVEL: [source] message (timestamp optional)
            re.compile(r'(\w+):\s*\[([^\]]+)\]\s*(.+)'),
            
            # Pattern 6: Simple format - LEVEL message
            re.compile(r'(\w+)\s+(.+)')
        ]
    
    def parse_timestamp(self, timestamp_str: str) -> Optional[datetime]:
        """Try to parse timestamp using various formats"""
        # Replace comma with dot for milliseconds
        timestamp_str = timestamp_str.replace(',', '.')
        
        for fmt in DEFAULT_DATE_FORMATS:
            try:
                return datetime.strptime(timestamp_str, fmt)
            except ValueError:
                continue
        
        # Try without year (add current year)
        try:
            dt = datetime.strptime(timestamp_str, '%b %d %H:%M:%S')
            return dt.replace(year=datetime.now().year)
        except ValueError:
            pass
        
        return None
    
    def extract_log_level(self, text: str) -> str:
        """Extract log level from text"""
        text_upper = text.upper()
        for level in LOG_LEVELS:
            if level in text_upper:
                return level
        return 'UNKNOWN'
    
    def parse_line(self, line: str) -> LogEntry:
        """Parse a single log line"""
        line = line.strip()
        
        if not line:
            return None
        
        # Try each pattern
        for i, pattern in enumerate(self.patterns):
            match = pattern.match(line)
            if match:
                groups = match.groups()
                
                if i == 0:  # Pattern 1
                    timestamp = self.parse_timestamp(groups[0])
                    level = groups[1]
                    source = groups[2]
                    message = groups[3]
                elif i == 1:  # Pattern 2
                    timestamp = self.parse_timestamp(groups[0])
                    level = groups[1]
                    source = groups[2]
                    message = groups[3]
                elif i == 2:  # Pattern 3
                    timestamp = self.parse_timestamp(groups[0])
                    level = groups[1]
                    source = groups[2]
                    message = groups[3]
                elif i == 3:  # Pattern 4
                    timestamp = self.parse_timestamp(groups[0])
                    level = self.extract_log_level(line)
                    source = groups[1]
                    message = groups[2]
                elif i == 4:  # Pattern 5
                    timestamp = None
                    level = groups[0]
                    source = groups[1]
                    message = groups[2]
                elif i == 5:  # Pattern 6
                    timestamp = None
                    level = groups[0] if groups[0].upper() in LOG_LEVELS else 'INFO'
                    source = 'unknown'
                    message = groups[1]
                
                return LogEntry(timestamp, level, source, message, line)
        
        # If no pattern matches, create a generic entry
        return LogEntry(None, 'UNKNOWN', 'unknown', line, line)
    
    def parse_file(self, file_path: str) -> List[LogEntry]:
        """Parse entire log file"""
        entries = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    entry = self.parse_line(line)
                    if entry:
                        entries.append(entry)
        except Exception as e:
            print(f"Error parsing file: {e}")
        
        return entries
    
    def parse_content(self, content: str) -> List[LogEntry]:
        """Parse log content from string"""
        entries = []
        
        for line in content.split('\n'):
            entry = self.parse_line(line)
            if entry:
                entries.append(entry)
        
        return entries

