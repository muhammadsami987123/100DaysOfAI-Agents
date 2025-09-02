"""
CLI interface for SystemMonitorAgent
Follows consistent patterns from other agents in the series
"""
import sys
import time
import threading
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.layout import Layout
from rich.live import Live
from rich.align import Align
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
from rich.markdown import Markdown

from monitor import SystemMonitor
from ai_assistant import AIAssistant
from utils import print_header, export_data, get_system_info, Colors, format_percentage
from config import DEFAULT_REFRESH_INTERVAL, DEFAULT_ALERT_THRESHOLDS

# Initialize Rich console
console = Console()

class SystemMonitorAgentCLI:
    """CLI interface for SystemMonitorAgent"""
    
    def __init__(self):
        self.monitor = SystemMonitor()
        self.ai_assistant = AIAssistant()
        self.running = False
        self.export_history = []
        
        # Ensure directories exist
        import os
        os.makedirs('exports', exist_ok=True)
        os.makedirs('logs', exist_ok=True)
    
    def show_welcome(self):
        """Display welcome message"""
        welcome_text = Text()
        welcome_text.append("📊 ", style="bold blue")
        welcome_text.append("SystemMonitorAgent", style="bold white")
        welcome_text.append(" - Real-time System Monitoring", style="italic white")
        
        console.print(Panel(
            welcome_text,
            title="Welcome",
            border_style="blue",
            padding=(1, 2)
        ))
        
        # Show system info
        system_info = get_system_info()
        console.print(f"🖥️  Platform: {system_info.get('platform', 'Unknown')}")
        console.print(f"🐍 Python: {system_info.get('python_version', 'Unknown').split()[0]}")
        console.print(f"🔧 CPU Cores: {system_info.get('cpu_count', 'Unknown')}")
        
        # Show AI status
        if self.ai_assistant.is_available:
            console.print("✅ AI Assistant: Enabled", style="green")
        else:
            console.print("⚠️  AI Assistant: Disabled (No API key)", style="yellow")
        
        console.print()
    
    def show_main_menu(self):
        """Display main menu"""
        menu_options = [
            "1. 📊 Live Monitoring",
            "2. 📸 Single Snapshot", 
            "3. 🤖 AI Optimization",
            "4. 🏥 AI Health Assessment",
            "5. 📤 Export Data",
            "6. ⚙️  Custom Thresholds",
            "7. 📈 History Summary",
            "8. 🎯 Quick Commands",
            "9. 🔧 Configuration",
            "0. ❌ Exit"
        ]
        
        menu_text = "\n".join(menu_options)
        console.print(Panel(menu_text, title="Main Menu", border_style="green"))
    
    def live_monitoring(self):
        """Start live monitoring with menu"""
        console.print("\n📊 [bold]Live System Monitoring[/bold]")
        
        # Get monitoring options
        interval = Prompt.ask("Refresh interval (seconds)", default=str(DEFAULT_REFRESH_INTERVAL))
        try:
            interval = int(interval)
        except ValueError:
            interval = DEFAULT_REFRESH_INTERVAL
        
        show_processes = Confirm.ask("Show process list?", default=True)
        enable_logging = Confirm.ask("Enable logging mode?", default=False)
        
        if enable_logging:
            self.logging_enabled = True
            console.print("📝 Logging enabled - stats will be saved to exports/", style="green")
        
        console.print(f"\n🔄 Starting monitoring with {interval}s refresh...")
        console.print("Press Ctrl+C to stop monitoring\n")
        
        self.run_monitoring_loop(interval, show_processes)
    
    def single_snapshot(self):
        """Show single system snapshot"""
        console.print("\n📸 [bold]System Snapshot[/bold]")
        
        with console.status("[bold blue]Collecting system statistics...", spinner="dots"):
            stats = self.monitor.get_system_stats()
        
        self.display_stats_panel(stats)
        
        # Ask for additional actions
        if Confirm.ask("Get AI optimization suggestions?"):
            self.ai_assistant.display_suggestions(stats)
        
        if Confirm.ask("Export this snapshot?"):
            self.export_snapshot(stats)
    
    def ai_optimization(self):
        """Get AI optimization suggestions"""
        console.print("\n🤖 [bold]AI Optimization Analysis[/bold]")
        
        if not self.ai_assistant.is_available:
            console.print("⚠️  AI Assistant not available. Set OPENAI_API_KEY environment variable.", style="yellow")
            return
        
        with console.status("[bold blue]Collecting system metrics...", spinner="dots"):
            stats = self.monitor.get_system_stats()
        
        self.ai_assistant.display_suggestions(stats)
    
    def ai_health_assessment(self):
        """Get AI health assessment"""
        console.print("\n🏥 [bold]AI System Health Assessment[/bold]")
        
        if not self.ai_assistant.is_available:
            console.print("⚠️  AI Assistant not available. Set OPENAI_API_KEY environment variable.", style="yellow")
            return
        
        with console.status("[bold blue]Analyzing system health...", spinner="dots"):
            stats = self.monitor.get_system_stats()
        
        self.ai_assistant.display_health_score(stats)
    
    def export_data(self):
        """Export system data"""
        console.print("\n📤 [bold]Export System Data[/bold]")
        
        formats = ['json', 'txt', 'csv']
        format_choice = Prompt.ask(
            "Export format", 
            choices=formats, 
            default='json'
        )
        
        with console.status("[bold blue]Collecting data...", spinner="dots"):
            stats = self.monitor.get_system_stats()
            system_info = get_system_info()
            
            export_data = {
                'system_info': system_info,
                'current_stats': stats,
                'export_timestamp': time.time(),
                'export_format': format_choice
            }
        
        try:
            filepath = export_data(export_data, format_choice)
            self.export_history.append(filepath)
            console.print(f"✅ Exported to: {filepath}", style="green")
        except Exception as e:
            console.print(f"❌ Export failed: {e}", style="red")
    
    def custom_thresholds(self):
        """Set custom alert thresholds"""
        console.print("\n⚙️  [bold]Custom Alert Thresholds[/bold]")
        
        current = self.monitor.alert_thresholds
        console.print(f"Current thresholds: CPU {current['cpu']}%, RAM {current['ram']}%, Disk {current['disk']}%")
        
        if Confirm.ask("Set custom thresholds?"):
            try:
                cpu = float(Prompt.ask("CPU threshold (%)", default=str(current['cpu'])))
                ram = float(Prompt.ask("RAM threshold (%)", default=str(current['ram'])))
                disk = float(Prompt.ask("Disk threshold (%)", default=str(current['disk'])))
                
                custom_thresholds = {'cpu': cpu, 'ram': ram, 'disk': disk}
                self.monitor.set_alert_thresholds(custom_thresholds)
                
                console.print(f"✅ Custom thresholds set: CPU {cpu}%, RAM {ram}%, Disk {disk}%", style="green")
            except ValueError:
                console.print("❌ Invalid input. Using default thresholds.", style="red")
    
    def history_summary(self):
        """Show monitoring history summary"""
        console.print("\n📈 [bold]Monitoring History Summary[/bold]")
        
        if not self.monitor.history:
            console.print("⚠️  No monitoring history available. Run monitoring first.", style="yellow")
            return
        
        summary = self.monitor.get_history_summary()
        
        # Create summary table
        table = Table(title="Resource Usage Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Min", style="green")
        table.add_column("Max", style="red")
        table.add_column("Average", style="yellow")
        
        for metric, data in summary.items():
            if metric != 'samples':
                table.add_row(
                    metric.upper(),
                    f"{data['min']:.1f}%",
                    f"{data['max']:.1f}%",
                    f"{data['avg']:.1f}%"
                )
        
        console.print(table)
        console.print(f"\n📊 Total samples: {summary['samples']}")
    
    def quick_commands(self):
        """Show quick command examples"""
        console.print("\n🎯 [bold]Quick Commands[/bold]")
        
        commands = [
            ("Single snapshot", "python main.py --single"),
            ("Live monitoring", "python main.py"),
            ("AI suggestions", "python main.py --suggest"),
            ("Health assessment", "python main.py --health"),
            ("Export JSON", "python main.py --export json"),
            ("Custom interval", "python main.py -i 2"),
            ("No processes", "python main.py --no-processes"),
            ("Logging mode", "python main.py --log")
        ]
        
        table = Table(title="Quick Commands")
        table.add_column("Description", style="cyan")
        table.add_column("Command", style="green")
        
        for desc, cmd in commands:
            table.add_row(desc, cmd)
        
        console.print(table)
    
    def configuration(self):
        """Show configuration options"""
        console.print("\n🔧 [bold]Configuration[/bold]")
        
        config_info = [
            ("Default refresh interval", f"{DEFAULT_REFRESH_INTERVAL} seconds"),
            ("CPU alert threshold", f"{DEFAULT_ALERT_THRESHOLDS['cpu']}%"),
            ("RAM alert threshold", f"{DEFAULT_ALERT_THRESHOLDS['ram']}%"),
            ("Disk alert threshold", f"{DEFAULT_ALERT_THRESHOLDS['disk']}%"),
            ("Process limit", "10"),
            ("History size", "100 samples"),
            ("Export directory", "exports/"),
            ("Log directory", "logs/")
        ]
        
        table = Table(title="Current Configuration")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="green")
        
        for setting, value in config_info:
            table.add_row(setting, value)
        
        console.print(table)
        
        if Confirm.ask("Edit configuration file?"):
            console.print("📝 Edit config.py to modify these settings", style="yellow")
    
    def display_stats_panel(self, stats):
        """Display stats in a rich panel"""
        # Create stats table
        table = Table(title="System Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        table.add_column("Status", style="yellow")
        
        # CPU
        cpu = stats['cpu']
        if 'error' not in cpu:
            cpu_status = "🟢 Normal" if cpu['usage_percent'] < 80 else "🟡 Warning" if cpu['usage_percent'] < 90 else "🔴 Critical"
            table.add_row("CPU Usage", f"{cpu['usage_percent']:.1f}%", cpu_status)
        
        # Memory
        memory = stats['memory']
        if 'error' not in memory:
            mem_status = "🟢 Normal" if memory['usage_percent'] < 85 else "🟡 Warning" if memory['usage_percent'] < 90 else "🔴 Critical"
            table.add_row("Memory Usage", f"{memory['usage_percent']:.1f}%", mem_status)
        
        # Disk
        disk = stats['disk']
        if 'error' not in disk:
            disk_status = "🟢 Normal" if disk['usage_percent'] < 90 else "🟡 Warning" if disk['usage_percent'] < 95 else "🔴 Critical"
            table.add_row("Disk Usage", f"{disk['usage_percent']:.1f}%", disk_status)
        
        console.print(table)
        
        # Show top processes
        if stats['processes'] and 'error' not in stats['processes'][0]:
            proc_table = Table(title="Top 5 Processes")
            proc_table.add_column("PID", style="cyan")
            proc_table.add_column("Name", style="green")
            proc_table.add_column("CPU%", style="yellow")
            proc_table.add_column("Memory", style="magenta")
            
            for proc in stats['processes'][:5]:
                proc_table.add_row(
                    str(proc['pid']),
                    proc['name'][:20],
                    f"{proc['cpu_percent']:.1f}%",
                    proc['memory_human']
                )
            
            console.print(proc_table)
    
    def export_snapshot(self, stats):
        """Export current snapshot"""
        formats = ['json', 'txt', 'csv']
        format_choice = Prompt.ask("Export format", choices=formats, default='json')
        
        try:
            filepath = export_data(stats, format_choice)
            console.print(f"✅ Exported to: {filepath}", style="green")
        except Exception as e:
            console.print(f"❌ Export failed: {e}", style="red")
    
    def run_monitoring_loop(self, interval: int, show_processes: bool = True):
        """Run continuous monitoring loop"""
        self.running = True
        iteration = 0
        
        try:
            while self.running:
                iteration += 1
                
                # Clear screen for better readability
                if iteration > 1:
                    console.print("\n" + "="*80 + "\n")
                
                # Get and display current stats
                stats = self.monitor.get_system_stats()
                self.display_stats_panel(stats)
                
                # Show active alerts
                alerts = self.monitor.get_alerts(stats)
                if alerts:
                    alert_text = "\n".join([f"🚨 {alert}" for alert in alerts])
                    console.print(Panel(alert_text, title="Active Alerts", border_style="red"))
                
                # Export if logging mode is enabled
                if hasattr(self, 'logging_enabled') and self.logging_enabled:
                    self.export_snapshot(stats)
                
                if self.running:
                    time.sleep(interval)
                    
        except KeyboardInterrupt:
            console.print("\n🛑 Monitoring stopped by user", style="yellow")
            self.running = False
        except Exception as e:
            console.print(f"\n❌ Monitoring error: {e}", style="red")
    
    def run(self):
        """Main CLI loop"""
        self.show_welcome()
        
        while True:
            try:
                self.show_main_menu()
                choice = Prompt.ask("Select option", choices=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
                
                if choice == "0":
                    console.print("👋 Goodbye!", style="green")
                    break
                elif choice == "1":
                    self.live_monitoring()
                elif choice == "2":
                    self.single_snapshot()
                elif choice == "3":
                    self.ai_optimization()
                elif choice == "4":
                    self.ai_health_assessment()
                elif choice == "5":
                    self.export_data()
                elif choice == "6":
                    self.custom_thresholds()
                elif choice == "7":
                    self.history_summary()
                elif choice == "8":
                    self.quick_commands()
                elif choice == "9":
                    self.configuration()
                
                if choice != "1":  # Don't wait after live monitoring
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                console.print("\n👋 Goodbye!", style="green")
                break
            except Exception as e:
                console.print(f"\n❌ Error: {e}", style="red")
                input("Press Enter to continue...")

def main():
    """Main entry point"""
    try:
        cli = SystemMonitorAgentCLI()
        cli.run()
    except Exception as e:
        console.print(f"❌ Fatal error: {e}", style="red")
        sys.exit(1)

if __name__ == "__main__":
    main()
