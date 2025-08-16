#!/usr/bin/env python3
"""
Demo script for WhatsApp Scheduler Agent
Showcases the functionality without actually sending messages
"""

import datetime
import json
from pathlib import Path

class WhatsAppSchedulerDemo:
    def __init__(self):
        self.scheduled_messages = {}
        self.message_id_counter = 1
        
    def validate_phone_number(self, phone: str) -> bool:
        """Validate phone number format (demo version)"""
        import re
        cleaned = re.sub(r'[\s\-\(\)]', '', phone)
        return bool(re.match(r'^\+[1-9]\d{10,14}$', cleaned))
    
    def validate_time_format(self, time_str: str) -> bool:
        """Validate time format (HH:MM)"""
        try:
            hour, minute = map(int, time_str.split(':'))
            return 0 <= hour <= 23 and 0 <= minute <= 59
        except:
            return False
    
    def get_default_time(self) -> str:
        """Get default time (2 minutes from now)"""
        now = datetime.datetime.now()
        default_time = now + datetime.timedelta(minutes=2)
        return default_time.strftime("%H:%M")
    
    def schedule_message_demo(self, phone: str, message: str, time_str: str) -> int:
        """Demo version of message scheduling"""
        import re
        
        # Clean phone number
        phone = re.sub(r'[\s\-\(\)]', '', phone)
        
        # Validate inputs
        if not self.validate_phone_number(phone):
            raise ValueError("Invalid phone number format. Use format: +1234567890")
        
        if not self.validate_time_format(time_str):
            raise ValueError("Invalid time format. Use HH:MM (24-hour format)")
        
        # Parse time
        hour, minute = map(int, time_str.split(':'))
        scheduled_time = datetime.datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # If time has passed today, schedule for tomorrow
        if scheduled_time <= datetime.datetime.now():
            scheduled_time += datetime.timedelta(days=1)
        
        # Create message entry
        message_id = self.message_id_counter
        self.message_id_counter += 1
        
        message_data = {
            'phone': phone,
            'message': message,
            'scheduled_time': scheduled_time.isoformat(),
            'status': 'scheduled'
        }
        
        self.scheduled_messages[message_id] = message_data
        
        return message_id
    
    def list_scheduled_messages(self):
        """List all scheduled messages"""
        if not self.scheduled_messages:
            print("📋 No scheduled messages found.")
            return
        
        print("\n📋 Scheduled Messages:")
        print("-" * 80)
        print(f"{'ID':<4} {'Phone':<15} {'Time':<20} {'Status':<12} {'Message'}")
        print("-" * 80)
        
        for msg_id, data in self.scheduled_messages.items():
            scheduled_time = datetime.datetime.fromisoformat(data['scheduled_time'])
            time_str = scheduled_time.strftime("%Y-%m-%d %H:%M")
            message_preview = data['message'][:30] + "..." if len(data['message']) > 30 else data['message']
            
            status_icon = {
                'scheduled': '⏰',
                'sending': '📤',
                'sent': '✅',
                'failed': '❌'
            }.get(data['status'], '❓')
            
            print(f"{msg_id:<4} {data['phone']:<15} {time_str:<20} {status_icon} {data['status']:<8} {message_preview}")
    
    def show_help(self):
        """Show help information"""
        help_text = """
🤖 WhatsApp Scheduler Agent - Demo Mode

This is a DEMO version that shows how the scheduler works
without actually sending WhatsApp messages.

Commands:
  schedule    - Schedule a new WhatsApp message (demo)
  view        - List all scheduled messages
  help        - Show this help message
  exit        - Exit the demo

Usage Examples:
  schedule
  view
  help
  exit

Notes:
  - This is a DEMO - no actual messages will be sent
  - Phone numbers must include country code (e.g., +1234567890)
  - Time format: HH:MM (24-hour format)
  - If no time is provided, message will be scheduled 2 minutes from now
        """
        print(help_text)
    
    def run_demo(self):
        """Main demo loop"""
        print("🤖 Welcome to WhatsApp Scheduler Agent - DEMO MODE!")
        print("This demo shows how the scheduler works without sending actual messages.")
        print("Type 'help' for available commands or 'exit' to quit.")
        
        while True:
            try:
                command = input("\n📝 Enter command: ").strip().lower()
                
                if command == 'exit':
                    print("👋 Demo ended!")
                    break
                
                elif command == 'help':
                    self.show_help()
                
                elif command == 'view':
                    self.list_scheduled_messages()
                
                elif command == 'schedule':
                    self._schedule_interactive_demo()
                
                else:
                    print("❌ Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\n👋 Demo ended!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def _schedule_interactive_demo(self):
        """Interactive message scheduling (demo)"""
        print("\n📅 Schedule New WhatsApp Message (DEMO)")
        print("-" * 40)
        
        try:
            # Get phone number
            phone = input("📱 Enter phone number (with country code): ").strip()
            if not phone:
                print("❌ Phone number is required.")
                return
            
            # Get message
            message = input("💬 Enter message: ").strip()
            if not message:
                print("❌ Message is required.")
                return
            
            # Get time (optional)
            time_input = input("⏰ Enter time (HH:MM, 24h format) [press Enter for 2 min from now]: ").strip()
            if not time_input:
                time_input = self.get_default_time()
                print(f"⏰ Using default time: {time_input}")
            
            # Schedule the message (demo)
            message_id = self.schedule_message_demo(phone, message, time_input)
            
            # Show confirmation
            scheduled_time = datetime.datetime.fromisoformat(self.scheduled_messages[message_id]['scheduled_time'])
            time_str = scheduled_time.strftime("%Y-%m-%d %H:%M")
            
            print(f"\n✅ Message scheduled successfully! (DEMO)")
            print(f"📋 ID: {message_id}")
            print(f"📱 To: {phone}")
            print(f"⏰ Time: {time_str}")
            print(f"💬 Message: {message}")
            print(f"\n💡 DEMO MODE: No actual message will be sent!")
            
        except ValueError as e:
            print(f"❌ {e}")
        except Exception as e:
            print(f"❌ Error scheduling message: {e}")

def main():
    """Main demo entry point"""
    print("🎭 WhatsApp Scheduler Agent - Demo Mode")
    print("=" * 50)
    print("This demo showcases the WhatsApp Scheduler functionality")
    print("without actually sending WhatsApp messages.")
    print("=" * 50)
    
    try:
        demo = WhatsAppSchedulerDemo()
        demo.run_demo()
    except KeyboardInterrupt:
        print("\n👋 Demo ended!")
    except Exception as e:
        print(f"❌ Demo error: {e}")

if __name__ == "__main__":
    main()
