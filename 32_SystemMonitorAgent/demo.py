"""
Demo script for SystemMonitorAgent
Showcases key features and capabilities
"""
import time
import sys
from monitor import SystemMonitor
from ai_assistant import AIAssistant
from utils import print_header, Colors

def demo_basic_monitoring():
    """Demonstrate basic monitoring capabilities"""
    print_header("Basic System Monitoring Demo")
    
    monitor = SystemMonitor()
    
    print(f"{Colors.INFO}Collecting system statistics...{Colors.RESET}")
    stats = monitor.get_system_stats()
    
    # Display stats
    monitor.display_stats(stats, show_processes=True)
    
    # Show alerts
    alerts = monitor.get_alerts(stats)
    if alerts:
        print(f"\n{Colors.ERROR}🚨 Active Alerts:{Colors.RESET}")
        for alert in alerts:
            print(f"  {Colors.ERROR}• {alert}{Colors.RESET}")
    else:
        print(f"\n{Colors.SUCCESS}✅ No active alerts - system is healthy!{Colors.RESET}")
    
    return stats

def demo_custom_thresholds():
    """Demonstrate custom threshold functionality"""
    print_header("Custom Alert Thresholds Demo")
    
    # Create monitor with custom thresholds
    custom_thresholds = {
        'cpu': 50.0,    # Alert at 50% CPU
        'ram': 60.0,    # Alert at 60% RAM
        'disk': 70.0    # Alert at 70% Disk
    }
    
    monitor = SystemMonitor(custom_thresholds)
    print(f"{Colors.INFO}Custom thresholds set: CPU {custom_thresholds['cpu']}%, RAM {custom_thresholds['ram']}%, Disk {custom_thresholds['disk']}%{Colors.RESET}")
    
    # Get stats with custom thresholds
    stats = monitor.get_system_stats()
    alerts = monitor.get_alerts(stats)
    
    if alerts:
        print(f"\n{Colors.ERROR}🚨 Alerts with custom thresholds:{Colors.RESET}")
        for alert in alerts:
            print(f"  {Colors.ERROR}• {alert}{Colors.RESET}")
    else:
        print(f"\n{Colors.SUCCESS}✅ No alerts with custom thresholds{Colors.RESET}")

def demo_ai_features():
    """Demonstrate AI assistant features"""
    print_header("AI Assistant Demo")
    
    ai = AIAssistant()
    
    if not ai.is_available:
        print(f"{Colors.WARNING}AI Assistant not available. Set OPENAI_API_KEY environment variable to enable.{Colors.RESET}")
        print(f"{Colors.INFO}Example: export OPENAI_API_KEY='your-api-key-here'{Colors.RESET}")
        return
    
    print(f"{Colors.INFO}AI Assistant is available!{Colors.RESET}")
    
    # Get current stats for AI analysis
    monitor = SystemMonitor()
    stats = monitor.get_system_stats()
    
    # Get optimization suggestions
    print(f"\n{Colors.INFO}Getting AI optimization suggestions...{Colors.RESET}")
    ai.display_suggestions(stats)
    
    # Get health assessment
    print(f"\n{Colors.INFO}Getting AI health assessment...{Colors.RESET}")
    ai.display_health_score(stats)

def demo_export_features():
    """Demonstrate export functionality"""
    print_header("Export Features Demo")
    
    monitor = SystemMonitor()
    stats = monitor.get_system_stats()
    
    print(f"{Colors.INFO}Exporting system statistics...{Colors.RESET}")
    
    # Export to different formats
    formats = ['json', 'txt', 'csv']
    
    for format_type in formats:
        try:
            from utils import export_data
            filepath = export_data(stats, format_type)
            print(f"{Colors.SUCCESS}✓ Exported to {format_type.upper()}: {filepath}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.ERROR}✗ Failed to export {format_type}: {e}{Colors.RESET}")

def demo_history_tracking():
    """Demonstrate history tracking"""
    print_header("History Tracking Demo")
    
    monitor = SystemMonitor()
    
    print(f"{Colors.INFO}Collecting multiple samples for history...{Colors.RESET}")
    
    # Collect several samples
    for i in range(3):
        stats = monitor.get_system_stats()
        print(f"Sample {i+1}: CPU {stats['cpu']['usage_percent']:.1f}%, RAM {stats['memory']['usage_percent']:.1f}%")
        time.sleep(1)
    
    # Show history summary
    summary = monitor.get_history_summary()
    
    print(f"\n{Colors.BOLD}History Summary:{Colors.RESET}")
    for metric, data in summary.items():
        if metric != 'samples':
            print(f"{metric.upper()}: Min {data['min']:.1f}%, Max {data['max']:.1f}%, Avg {data['avg']:.1f}%")
    
    print(f"Total samples: {summary['samples']}")

def demo_process_monitoring():
    """Demonstrate process monitoring"""
    print_header("Process Monitoring Demo")
    
    monitor = SystemMonitor()
    
    print(f"{Colors.INFO}Getting top processes by resource usage...{Colors.RESET}")
    
    processes = monitor.get_top_processes(limit=5)
    
    if processes and 'error' not in processes[0]:
        print(f"{'PID':<8} {'Name':<20} {'CPU%':<8} {'Memory%':<10} {'Memory'}")
        print("-" * 60)
        for proc in processes:
            print(f"{proc['pid']:<8} {proc['name'][:19]:<20} "
                  f"{proc['cpu_percent']:<8.1f} {proc['memory_percent']:<10.1f} "
                  f"{proc['memory_human']}")
    else:
        print(f"{Colors.ERROR}Failed to get process information{Colors.RESET}")

def main():
    """Run all demos"""
    print_header("SystemMonitorAgent Feature Demo")
    print(f"{Colors.INFO}This demo showcases the key features of SystemMonitorAgent{Colors.RESET}")
    print(f"{Colors.INFO}Press Enter to continue between demos...{Colors.RESET}")
    
    demos = [
        ("Basic Monitoring", demo_basic_monitoring),
        ("Custom Thresholds", demo_custom_thresholds),
        ("Process Monitoring", demo_process_monitoring),
        ("History Tracking", demo_history_tracking),
        ("Export Features", demo_export_features),
        ("AI Assistant", demo_ai_features)
    ]
    
    for demo_name, demo_func in demos:
        try:
            print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
            demo_func()
            
            if demo_name != "AI Assistant":  # Don't wait after AI demo
                input(f"\n{Colors.INFO}Press Enter to continue to next demo...{Colors.RESET}")
                
        except Exception as e:
            print(f"{Colors.ERROR}Demo '{demo_name}' failed: {e}{Colors.RESET}")
            input(f"\n{Colors.INFO}Press Enter to continue...{Colors.RESET}")
    
    print_header("Demo Complete!")
    print(f"{Colors.SUCCESS}You've seen all the main features of SystemMonitorAgent!{Colors.RESET}")
    print(f"\n{Colors.INFO}Try these commands:{Colors.RESET}")
    print(f"  python main.py --single          # Quick system snapshot")
    print(f"  python main.py                   # Start real-time monitoring")
    print(f"  python main.py --suggest         # Get AI optimization tips")
    print(f"  python main.py --export json     # Export current stats")
    print(f"  python main.py --help            # View all options")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.INFO}Demo interrupted by user{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.ERROR}Demo failed: {e}{Colors.RESET}")
        sys.exit(1)
