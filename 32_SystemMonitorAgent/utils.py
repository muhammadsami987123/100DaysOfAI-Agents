"""
Utility functions for SystemMonitorAgent
"""
import json
import csv
from datetime import datetime
from typing import Dict, Any, List
import psutil
from colorama import Fore, Back, Style, init

# Initialize colorama for cross-platform color support
init(autoreset=True)

class Colors:
    """Color constants for terminal output"""
    RESET = Style.RESET_ALL
    BOLD = Style.BRIGHT
    
    # Status colors
    SUCCESS = Fore.GREEN
    WARNING = Fore.YELLOW
    ERROR = Fore.RED
    INFO = Fore.CYAN
    
    # Resource colors
    CPU = Fore.MAGENTA
    RAM = Fore.BLUE
    DISK = Fore.GREEN
    PROCESS = Fore.WHITE

def format_bytes(bytes_value: int) -> str:
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"

def format_percentage(value: float) -> str:
    """Format percentage with color coding"""
    if value >= 90:
        color = Colors.ERROR
    elif value >= 80:
        color = Colors.WARNING
    else:
        color = Colors.SUCCESS
    
    return f"{color}{value:.1f}%{Colors.RESET}"

def format_resource_bar(percentage: float, width: int = 20) -> str:
    """Create a visual progress bar for resources"""
    filled = int(width * percentage / 100)
    bar = "█" * filled + "░" * (width - filled)
    
    if percentage >= 90:
        color = Colors.ERROR
    elif percentage >= 80:
        color = Colors.WARNING
    else:
        color = Colors.SUCCESS
    
    return f"{color}{bar}{Colors.RESET}"

def get_system_info() -> Dict[str, Any]:
    """Get basic system information"""
    try:
        return {
            'platform': psutil.sys.platform,
            'python_version': psutil.sys.version,
            'cpu_count': psutil.cpu_count(),
            'cpu_freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
            'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat()
        }
    except Exception as e:
        return {'error': str(e)}

def export_data(data: Dict[str, Any], format_type: str, filename: str = None) -> str:
    """Export data in specified format"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"system_stats_{timestamp}"
    
    if format_type == 'json':
        filepath = f"exports/{filename}.json"
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    elif format_type == 'txt':
        filepath = f"exports/{filename}.txt"
        with open(filepath, 'w') as f:
            f.write("System Monitor Report\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")
            
            for key, value in data.items():
                if isinstance(value, dict):
                    f.write(f"{key}:\n")
                    for k, v in value.items():
                        f.write(f"  {k}: {v}\n")
                else:
                    f.write(f"{key}: {value}\n")
                f.write("\n")
    
    elif format_type == 'csv':
        filepath = f"exports/{filename}.csv"
        # Flatten nested data for CSV
        flat_data = flatten_dict(data)
        if flat_data:
            with open(filepath, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(flat_data.keys())
                writer.writerow(flat_data.values())
    
    return filepath

def flatten_dict(data: Dict[str, Any], parent_key: str = '') -> Dict[str, Any]:
    """Flatten nested dictionary for CSV export"""
    items = []
    for k, v in data.items():
        new_key = f"{parent_key}.{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key).items())
        else:
            items.append((new_key, v))
    return dict(items)

def create_alert_message(metric: str, value: float, threshold: float) -> str:
    """Create alert message for threshold violations"""
    if value >= threshold:
        return f"{Colors.ERROR}⚠️  ALERT: {metric.upper()} usage is {value:.1f}% (threshold: {threshold}%){Colors.RESET}"
    return ""

def print_header(title: str):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.INFO}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.INFO}{title:^60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.INFO}{'='*60}{Colors.RESET}\n")

def print_section(title: str):
    """Print formatted section header"""
    print(f"\n{Colors.BOLD}{Colors.CPU}{title}{Colors.RESET}")
    print(f"{Colors.CPU}{'-' * len(title)}{Colors.RESET}")
