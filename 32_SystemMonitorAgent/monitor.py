"""
Core system monitoring functionality
"""
import time
import psutil
from datetime import datetime
from typing import Dict, Any, List, Optional
from config import DEFAULT_ALERT_THRESHOLDS, PROCESS_LIMIT
from utils import (
    format_bytes, format_percentage, format_resource_bar, 
    create_alert_message, Colors, print_section
)

class SystemMonitor:
    """Main system monitoring class"""
    
    def __init__(self, alert_thresholds: Optional[Dict[str, float]] = None):
        self.alert_thresholds = alert_thresholds or DEFAULT_ALERT_THRESHOLDS
        self.history = []
        self.max_history = 100  # Keep last 100 readings
        
    def get_cpu_stats(self) -> Dict[str, Any]:
        """Get CPU usage statistics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            return {
                'usage_percent': cpu_percent,
                'core_count': cpu_count,
                'frequency_mhz': cpu_freq.current if cpu_freq else None,
                'frequency_min_mhz': cpu_freq.min if cpu_freq else None,
                'frequency_max_mhz': cpu_freq.max if cpu_freq else None,
                'alert': create_alert_message('CPU', cpu_percent, self.alert_thresholds['cpu'])
            }
        except Exception as e:
            return {'error': str(e), 'usage_percent': 0}
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get RAM memory statistics"""
        try:
            memory = psutil.virtual_memory()
            
            return {
                'total_bytes': memory.total,
                'available_bytes': memory.available,
                'used_bytes': memory.used,
                'free_bytes': memory.free,
                'usage_percent': memory.percent,
                'total_human': format_bytes(memory.total),
                'available_human': format_bytes(memory.available),
                'used_human': format_bytes(memory.used),
                'free_human': format_bytes(memory.free),
                'alert': create_alert_message('RAM', memory.percent, self.alert_thresholds['ram'])
            }
        except Exception as e:
            return {'error': str(e), 'usage_percent': 0}
    
    def get_disk_stats(self) -> Dict[str, Any]:
        """Get disk usage statistics"""
        try:
            disk = psutil.disk_usage('/')
            
            return {
                'total_bytes': disk.total,
                'used_bytes': disk.used,
                'free_bytes': disk.free,
                'usage_percent': (disk.used / disk.total) * 100,
                'total_human': format_bytes(disk.total),
                'used_human': format_bytes(disk.used),
                'free_human': format_bytes(disk.free),
                'alert': create_alert_message('Disk', (disk.used / disk.total) * 100, self.alert_thresholds['disk'])
            }
        except Exception as e:
            return {'error': str(e), 'usage_percent': 0}
    
    def get_network_stats(self) -> Dict[str, Any]:
        """Get network interface statistics"""
        try:
            network = psutil.net_io_counters()
            
            return {
                'bytes_sent': network.bytes_sent,
                'bytes_recv': network.bytes_recv,
                'packets_sent': network.packets_sent,
                'packets_recv': network.packets_recv,
                'bytes_sent_human': format_bytes(network.bytes_sent),
                'bytes_recv_human': format_bytes(network.bytes_recv)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_top_processes(self, limit: int = None) -> List[Dict[str, Any]]:
        """Get top processes by resource consumption"""
        try:
            limit = limit or PROCESS_LIMIT
            processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'memory_info']):
                try:
                    proc_info = proc.info
                    if proc_info['cpu_percent'] is not None and proc_info['memory_percent'] is not None:
                        processes.append({
                            'pid': proc_info['pid'],
                            'name': proc_info['name'],
                            'cpu_percent': proc_info['cpu_percent'],
                            'memory_percent': proc_info['memory_percent'],
                            'memory_bytes': proc_info['memory_info'].rss if proc_info['memory_info'] else 0,
                            'memory_human': format_bytes(proc_info['memory_info'].rss) if proc_info['memory_info'] else '0 B'
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            # Sort by CPU usage first, then by memory usage
            processes.sort(key=lambda x: (x['cpu_percent'], x['memory_percent']), reverse=True)
            return processes[:limit]
            
        except Exception as e:
            return [{'error': str(e)}]
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get comprehensive system statistics"""
        timestamp = datetime.now()
        
        stats = {
            'timestamp': timestamp.isoformat(),
            'cpu': self.get_cpu_stats(),
            'memory': self.get_memory_stats(),
            'disk': self.get_disk_stats(),
            'network': self.get_network_stats(),
            'processes': self.get_top_processes()
        }
        
        # Add to history
        self.history.append(stats)
        if len(self.history) > self.max_history:
            self.history.pop(0)
        
        return stats
    
    def display_stats(self, stats: Dict[str, Any], show_processes: bool = True):
        """Display formatted system statistics"""
        print_section("CPU Usage")
        cpu = stats['cpu']
        if 'error' not in cpu:
            print(f"Usage: {format_percentage(cpu['usage_percent'])}")
            print(f"Bar:   {format_resource_bar(cpu['usage_percent'])}")
            print(f"Cores: {cpu['core_count']}")
            if cpu['frequency_mhz']:
                print(f"Freq:  {cpu['frequency_mhz']:.0f} MHz")
            if cpu['alert']:
                print(cpu['alert'])
        else:
            print(f"{Colors.ERROR}Error: {cpu['error']}{Colors.RESET}")
        
        print_section("Memory Usage")
        memory = stats['memory']
        if 'error' not in memory:
            print(f"Usage: {format_percentage(memory['usage_percent'])}")
            print(f"Bar:   {format_resource_bar(memory['usage_percent'])}")
            print(f"Total: {memory['total_human']}")
            print(f"Used:  {memory['used_human']}")
            print(f"Free:  {memory['free_human']}")
            if memory['alert']:
                print(memory['alert'])
        else:
            print(f"{Colors.ERROR}Error: {memory['error']}{Colors.RESET}")
        
        print_section("Disk Usage")
        disk = stats['disk']
        if 'error' not in disk:
            print(f"Usage: {format_percentage(disk['usage_percent'])}")
            print(f"Bar:   {format_resource_bar(disk['usage_percent'])}")
            print(f"Total: {disk['total_human']}")
            print(f"Used:  {disk['used_human']}")
            print(f"Free:  {disk['free_human']}")
            if disk['alert']:
                print(disk['alert'])
        else:
            print(f"{Colors.ERROR}Error: {disk['error']}{Colors.RESET}")
        
        print_section("Network I/O")
        network = stats['network']
        if 'error' not in network:
            print(f"Sent:     {network['bytes_sent_human']}")
            print(f"Received: {network['bytes_recv_human']}")
            print(f"Packets:  {network['packets_sent']} sent, {network['packets_recv']} received")
        else:
            print(f"{Colors.ERROR}Error: {network['error']}{Colors.RESET}")
        
        if show_processes:
            print_section(f"Top {len(stats['processes'])} Processes")
            if stats['processes'] and 'error' not in stats['processes'][0]:
                print(f"{'PID':<8} {'Name':<20} {'CPU%':<8} {'Memory%':<10} {'Memory'}")
                print("-" * 60)
                for proc in stats['processes']:
                    print(f"{proc['pid']:<8} {proc['name'][:19]:<20} "
                          f"{proc['cpu_percent']:<8.1f} {proc['memory_percent']:<10.1f} "
                          f"{proc['memory_human']}")
            else:
                print(f"{Colors.ERROR}Error: {stats['processes'][0]['error']}{Colors.RESET}")
        
        print(f"\n{Colors.INFO}Last updated: {stats['timestamp']}{Colors.RESET}")
    
    def get_alerts(self, stats: Dict[str, Any]) -> List[str]:
        """Get all active alerts from current stats"""
        alerts = []
        
        for metric in ['cpu', 'memory', 'disk']:
            if metric in stats and 'error' not in stats[metric]:
                try:
                    value = stats[metric]['usage_percent']
                    threshold = self.alert_thresholds[metric]
                    if value >= threshold:
                        alerts.append(f"{metric.upper()}: {value:.1f}% >= {threshold}%")
                except (KeyError, TypeError):
                    # Skip this metric if data is malformed
                    continue
        
        return alerts
    
    def set_alert_thresholds(self, thresholds: Dict[str, float]):
        """Update alert thresholds"""
        self.alert_thresholds.update(thresholds)
    
    def get_history_summary(self) -> Dict[str, Any]:
        """Get summary statistics from history"""
        if not self.history:
            return {}
        
        cpu_values = [s['cpu']['usage_percent'] for s in self.history if 'error' not in s['cpu']]
        memory_values = [s['memory']['usage_percent'] for s in self.history if 'error' not in s['memory']]
        disk_values = [s['disk']['usage_percent'] for s in self.history if 'error' not in s['disk']]
        
        return {
            'cpu': {
                'min': min(cpu_values) if cpu_values else 0,
                'max': max(cpu_values) if cpu_values else 0,
                'avg': sum(cpu_values) / len(cpu_values) if cpu_values else 0
            },
            'memory': {
                'min': min(memory_values) if memory_values else 0,
                'max': max(memory_values) if memory_values else 0,
                'avg': sum(memory_values) / len(memory_values) if memory_values else 0
            },
            'disk': {
                'min': min(disk_values) if disk_values else 0,
                'max': max(disk_values) if disk_values else 0,
                'avg': sum(disk_values) / len(disk_values) if disk_values else 0
            },
            'samples': len(self.history)
        }
