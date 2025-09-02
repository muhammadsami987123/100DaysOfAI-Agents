"""
Main CLI application for SystemMonitorAgent
"""
import argparse
import signal
import sys
import time
from typing import Dict, Any
from monitor import SystemMonitor
from ai_assistant import AIAssistant
from utils import print_header, export_data, get_system_info, Colors
from config import DEFAULT_REFRESH_INTERVAL, DEFAULT_EXPORT_FORMAT

class SystemMonitorAgent:
    """Main application class for SystemMonitorAgent"""
    
    def __init__(self):
        self.monitor = SystemMonitor()
        self.ai_assistant = AIAssistant()
        self.running = False
        self.export_history = []
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"\n{Colors.INFO}Shutting down SystemMonitorAgent...{Colors.RESET}")
        self.running = False
        if self.export_history:
            print(f"{Colors.SUCCESS}Exported {len(self.export_history)} reports{Colors.RESET}")
        sys.exit(0)
    
    def parse_arguments(self):
        """Parse command line arguments"""
        parser = argparse.ArgumentParser(
            description="SystemMonitorAgent - Real-time system resource monitoring",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python main.py                    # Monitor with default 5s interval
  python main.py -i 2              # Monitor with 2s interval
  python main.py --export json     # Export current stats to JSON
  python main.py --suggest         # Get AI optimization suggestions
  python main.py --health          # Get AI health assessment
  python main.py --no-processes    # Hide process list
  python main.py --log             # Enable logging mode
  python main.py --thresholds      # Set custom alert thresholds
            """
        )
        
        parser.add_argument(
            '-i', '--interval',
            type=int,
            default=DEFAULT_REFRESH_INTERVAL,
            help=f'Refresh interval in seconds (default: {DEFAULT_REFRESH_INTERVAL})'
        )
        
        parser.add_argument(
            '--export',
            choices=['json', 'txt', 'csv'],
            default=None,
            help='Export current stats to specified format'
        )
        
        parser.add_argument(
            '--suggest',
            action='store_true',
            help='Get AI-powered optimization suggestions'
        )
        
        parser.add_argument(
            '--health',
            action='store_true',
            help='Get AI-powered system health assessment'
        )
        
        parser.add_argument(
            '--no-processes',
            action='store_true',
            help='Hide process list from display'
        )
        
        parser.add_argument(
            '--log',
            action='store_true',
            help='Enable logging mode (save usage history)'
        )
        
        parser.add_argument(
            '--thresholds',
            nargs=3,
            type=float,
            metavar=('CPU', 'RAM', 'DISK'),
            help='Set custom alert thresholds (CPU RAM DISK percentages)'
        )
        
        parser.add_argument(
            '--single',
            action='store_true',
            help='Show single snapshot and exit (no continuous monitoring)'
        )
        
        parser.add_argument(
            '--summary',
            action='store_true',
            help='Show summary statistics from monitoring history'
        )
        
        return parser.parse_args()
    
    def set_custom_thresholds(self, thresholds):
        """Set custom alert thresholds"""
        if len(thresholds) == 3:
            custom_thresholds = {
                'cpu': thresholds[0],
                'ram': thresholds[1],
                'disk': thresholds[2]
            }
            self.monitor.set_alert_thresholds(custom_thresholds)
            print(f"{Colors.SUCCESS}Custom thresholds set: CPU {thresholds[0]}%, RAM {thresholds[1]}%, Disk {thresholds[2]}%{Colors.RESET}")
    
    def export_current_stats(self, format_type: str):
        """Export current system statistics"""
        stats = self.monitor.get_system_stats()
        system_info = get_system_info()
        
        export_data = {
            'system_info': system_info,
            'current_stats': stats,
            'export_timestamp': time.time(),
            'export_format': format_type
        }
        
        try:
            filepath = export_data(export_data, format_type)
            self.export_history.append(filepath)
            print(f"{Colors.SUCCESS}✓ Exported to: {filepath}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.ERROR}Export failed: {e}{Colors.RESET}")
    
    def show_system_info(self):
        """Display basic system information"""
        print_header("System Information")
        system_info = get_system_info()
        
        for key, value in system_info.items():
            if isinstance(value, dict) and value:
                print(f"{Colors.BOLD}{key.title()}:{Colors.RESET}")
                for k, v in value.items():
                    print(f"  {k}: {v}")
            elif value:
                print(f"{Colors.BOLD}{key.title()}:{Colors.RESET} {value}")
    
    def show_summary(self):
        """Show summary statistics from monitoring history"""
        if not self.monitor.history:
            print(f"{Colors.WARNING}No monitoring history available. Run monitoring first.{Colors.RESET}")
            return
        
        print_header("Monitoring History Summary")
        summary = self.monitor.get_history_summary()
        
        for metric, data in summary.items():
            if metric != 'samples':
                print(f"\n{Colors.BOLD}{metric.upper()}:{Colors.RESET}")
                print(f"  Min: {data['min']:.1f}%")
                print(f"  Max: {data['max']:.1f}%")
                print(f"  Avg: {data['avg']:.1f}%")
        
        print(f"\n{Colors.INFO}Total samples: {summary['samples']}{Colors.RESET}")
    
    def run_monitoring_loop(self, interval: int, show_processes: bool = True):
        """Run continuous monitoring loop"""
        print_header("System Monitor - Live Mode")
        print(f"{Colors.INFO}Press Ctrl+C to stop monitoring{Colors.RESET}")
        print(f"{Colors.INFO}Refresh interval: {interval} seconds{Colors.RESET}")
        
        self.running = True
        iteration = 0
        
        try:
            while self.running:
                iteration += 1
                
                # Clear screen for better readability (optional)
                if iteration > 1:
                    print("\n" + "="*80 + "\n")
                
                # Get and display current stats
                stats = self.monitor.get_system_stats()
                self.monitor.display_stats(stats, show_processes)
                
                # Show active alerts
                alerts = self.monitor.get_alerts(stats)
                if alerts:
                    print(f"\n{Colors.ERROR}🚨 ACTIVE ALERTS:{Colors.RESET}")
                    for alert in alerts:
                        print(f"  {Colors.ERROR}• {alert}{Colors.RESET}")
                
                # Export if logging mode is enabled
                if hasattr(self, 'logging_enabled') and self.logging_enabled:
                    self.export_current_stats('json')
                
                if self.running:  # Don't sleep if we're shutting down
                    time.sleep(interval)
                    
        except KeyboardInterrupt:
            print(f"\n{Colors.INFO}Monitoring stopped by user{Colors.RESET}")
        except Exception as e:
            print(f"\n{Colors.ERROR}Monitoring error: {e}{Colors.RESET}")
            # Continue monitoring instead of crashing
    
    def run(self):
        """Main application entry point"""
        args = self.parse_arguments()
        
        # Show system information
        self.show_system_info()
        
        # Set custom thresholds if provided
        if args.thresholds:
            self.set_custom_thresholds(args.thresholds)
        
        # Handle single snapshot mode
        if args.single:
            print_header("System Snapshot")
            stats = self.monitor.get_system_stats()
            self.monitor.display_stats(stats, not args.no_processes)
            
            if args.suggest:
                self.ai_assistant.display_suggestions(stats)
            
            if args.health:
                self.ai_assistant.display_health_score(stats)
            
            if args.export:
                self.export_current_stats(args.export)
            
            return
        
        # Handle summary mode
        if args.summary:
            self.show_summary()
            return
        
        # Handle export mode
        if args.export:
            self.export_current_stats(args.export)
            return
        
        # Handle AI suggestions
        if args.suggest:
            print_header("AI Optimization Analysis")
            stats = self.monitor.get_system_stats()
            self.ai_assistant.display_suggestions(stats)
            return
        
        # Handle AI health assessment
        if args.health:
            print_header("AI Health Assessment")
            stats = self.monitor.get_system_stats()
            self.ai_assistant.display_health_score(stats)
            return
        
        # Enable logging mode if requested
        if args.log:
            self.logging_enabled = True
            print(f"{Colors.INFO}Logging mode enabled - stats will be saved to exports/ directory{Colors.RESET}")
        
        # Start monitoring loop
        self.run_monitoring_loop(args.interval, not args.no_processes)

def main():
    """Main entry point"""
    try:
        agent = SystemMonitorAgent()
        agent.run()
    except Exception as e:
        print(f"{Colors.ERROR}Fatal error: {e}{Colors.RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
