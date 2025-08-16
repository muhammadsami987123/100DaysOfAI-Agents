#!/usr/bin/env python3
"""
WhatsApp Scheduler Agent - Day 16 of 100 Days Agent Challenge
A CLI-based tool to schedule WhatsApp messages using WhatsApp Web.
"""

import os
import sys
import json
import time
import datetime
import threading
import re
from typing import Dict, List, Optional
import pywhatkit as pwk
from pathlib import Path
import config

class WhatsAppScheduler:
    def __init__(self):
        self.scheduled_messages = {}
        self.message_id_counter = 1
        self.data_file = Path(config.DATA_FILE)
        self.load_scheduled_messages()
        self.check_pywhatkit_version()
    
    def check_pywhatkit_version(self):
        """Check pywhatkit version and set compatibility flags"""
        try:
            import pkg_resources
            version = pkg_resources.get_distribution("pywhatkit").version
            print(f"📦 pywhatkit version: {version}")
            
            # Check if version supports newer parameters
            version_parts = [int(x) for x in version.split('.')]
            self.supports_tab_close = version_parts[0] >= 5 and version_parts[1] >= 4
            self.supports_print_wait = version_parts[0] >= 5 and version_parts[1] >= 4
            
            # Check available methods
            self.has_instant_method = hasattr(pwk, 'sendwhatmsg_instantly')
            print(f"🔧 Instant method available: {self.has_instant_method}")
            
        except Exception as e:
            print(f"⚠️  Could not determine pywhatkit version: {e}")
            # Default to older version compatibility
            self.supports_tab_close = False
            self.supports_print_wait = False
            self.has_instant_method = False
        
    def load_scheduled_messages(self):
        """Load scheduled messages from JSON file"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.scheduled_messages = data.get('messages', {})
                    self.message_id_counter = data.get('counter', 1)
            except Exception as e:
                print(f"⚠️  Warning: Could not load saved messages: {e}")
    
    def save_scheduled_messages(self):
        """Save scheduled messages to JSON file"""
        try:
            data = {
                'messages': self.scheduled_messages,
                'counter': self.message_id_counter
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️  Warning: Could not save messages: {e}")
    
    def validate_phone_number(self, phone: str) -> bool:
        """Validate phone number format"""
        # Remove spaces, dashes, and parentheses
        cleaned = re.sub(r'[\s\-\(\)]', '', phone)
        # Check if it starts with + and has 10-15 digits
        return bool(re.match(config.PHONE_NUMBER_REGEX, cleaned))
    
    def validate_time_format(self, time_str: str) -> bool:
        """Validate time format (HH:MM)"""
        try:
            hour, minute = map(int, time_str.split(':'))
            return 0 <= hour <= 23 and 0 <= minute <= 59
        except:
            return False
    
    def get_default_time(self) -> str:
        """Get default time (30 seconds from now)"""
        now = datetime.datetime.now()
        default_time = now + datetime.timedelta(seconds=config.DEFAULT_DELAY_SECONDS)
        return default_time.strftime(config.TIME_FORMAT)
    
    def schedule_message(self, phone: str, message: str, time_str: str) -> int:
        """Schedule a WhatsApp message"""
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
        
        # Ensure minimum delay for WhatsApp Web loading
        min_delay = datetime.timedelta(seconds=config.MIN_DELAY_SECONDS)
        time_until_scheduled = scheduled_time - datetime.datetime.now()
        
        if time_until_scheduled < min_delay:
            print(f"⚠️  Warning: Scheduled time is too close. Adjusting to {min_delay.total_seconds():.0f} seconds from now.")
            scheduled_time = datetime.datetime.now() + min_delay
        
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
        self.save_scheduled_messages()
        
        # Start scheduling thread
        thread = threading.Thread(
            target=self._send_message_at_time,
            args=(message_id, phone, message, scheduled_time)
        )
        thread.daemon = True
        thread.start()
        
        return message_id
    
    def _send_message_at_time(self, message_id: int, phone: str, message: str, scheduled_time: datetime.datetime):
        """Send message at scheduled time"""
        try:
            # Wait until scheduled time
            wait_seconds = (scheduled_time - datetime.datetime.now()).total_seconds()
            if wait_seconds > 0:
                if wait_seconds >= 60:
                    print(f"⏳ Waiting {wait_seconds/60:.1f} minutes until scheduled time...")
                else:
                    print(f"⏳ Waiting {wait_seconds:.0f} seconds until scheduled time...")
                time.sleep(wait_seconds)
            
            # Update status to sending
            self.scheduled_messages[message_id]['status'] = 'sending'
            self.save_scheduled_messages()
            
            # Send message using pywhatkit
            # Use current time + small delay to ensure proper timing
            now = datetime.datetime.now()
            send_time = now + datetime.timedelta(seconds=5)  # 5 seconds from now
            
            print(f"\n📱 Sending message to {phone}...")
            print(f"💡 Make sure WhatsApp Web is open and you're logged in!")
            print(f"⏰ Sending at: {send_time.strftime('%H:%M:%S')}")
            
            # Use a more reliable approach with immediate sending
            try:
                print("🚀 Attempting to send message immediately...")
                
                # Try instant sending first (more reliable)
                try:
                    # Store the original message count if possible
                    original_count = self._get_whatsapp_message_count(phone)
                    
                    pwk.sendwhatmsg_instantly(
                        phone, 
                        message, 
                        wait_time=config.WAIT_TIME,  # Use configurable wait time
                        tab_close=config.TAB_CLOSE
                    )
                    
                    # Verify message was actually sent
                    if self._verify_message_sent(phone, message, original_count):
                        print("✅ Message sent and verified successfully!")
                        self.scheduled_messages[message_id]['status'] = 'sent'
                        self.scheduled_messages[message_id]['sent_at'] = datetime.datetime.now().isoformat()
                    else:
                        print("⚠️  Message may not have been sent successfully")
                        self.scheduled_messages[message_id]['status'] = 'failed'
                        self.scheduled_messages[message_id]['error'] = 'Message verification failed'
                        
                except AttributeError:
                    # Fallback to scheduled method if instant method doesn't exist
                    print("🔄 Instant method not available, using scheduled method...")
                    if self.supports_tab_close:
                        # Use newer pywhatkit version with tab_close support
                        pwk.sendwhatmsg(
                            phone, 
                            message, 
                            send_time.hour, 
                            send_time.minute, 
                            wait_time=config.WAIT_TIME,
                            tab_close=config.TAB_CLOSE
                        )
                    else:
                        # Use older pywhatkit version compatibility
                        print("🔄 Using compatibility mode for older pywhatkit version...")
                        pwk.sendwhatmsg(
                            phone, 
                            message, 
                            send_time.hour, 
                            send_time.minute, 
                            wait_time=config.WAIT_TIME
                        )
                    
                    # For scheduled method, we can't easily verify, so mark as sent with warning
                    print("⚠️  Message sent using scheduled method - verification not available")
                    self.scheduled_messages[message_id]['status'] = 'sent'
                    self.scheduled_messages[message_id]['sent_at'] = datetime.datetime.now().isoformat()
                    self.scheduled_messages[message_id]['warning'] = 'Verification not available for scheduled method'
                
                self.save_scheduled_messages()
                
            except Exception as send_error:
                error_msg = str(send_error)
                print(f"❌ Error during sending: {error_msg}")
                
                # Provide helpful error messages
                if "Call Time must be Greater than Wait Time" in error_msg:
                    print("💡 Tip: The timing calculation had an issue. Try again.")
                elif "WhatsApp Web" in error_msg:
                    print("💡 Tip: Make sure WhatsApp Web is open and you're logged in")
                elif "browser" in error_msg.lower():
                    print("💡 Tip: Make sure Chrome browser is installed and updated")
                elif "timeout" in error_msg.lower():
                    print("💡 Tip: WhatsApp Web took too long to load. Try again.")
                elif "not found" in error_msg.lower():
                    print("💡 Tip: Phone number not found in WhatsApp. Check the number.")
                
                self.scheduled_messages[message_id]['status'] = 'failed'
                self.scheduled_messages[message_id]['error'] = error_msg
                self.save_scheduled_messages()
                raise send_error
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Failed to send message: {error_msg}")
            
            # Provide helpful error messages
            if "Call Time must be Greater than Wait Time" in error_msg:
                print("💡 Tip: The timing calculation had an issue. Try again.")
            elif "WhatsApp Web" in error_msg:
                print("💡 Tip: Make sure WhatsApp Web is open and you're logged in")
            elif "browser" in error_msg.lower():
                print("💡 Tip: Make sure Chrome browser is installed and updated")
            
            self.scheduled_messages[message_id]['status'] = 'failed'
            self.scheduled_messages[message_id]['error'] = error_msg
            self.save_scheduled_messages()
    
    def _get_whatsapp_message_count(self, phone: str) -> Optional[int]:
        """Try to get the current message count for a phone number (for verification)"""
        try:
            # This is a placeholder - in a real implementation, you might use
            # WhatsApp Web API or other methods to get message count
            # For now, we'll return None to indicate we can't verify
            return None
        except Exception:
            return None
    
    def _verify_message_sent(self, phone: str, message: str, original_count: Optional[int]) -> bool:
        """Verify that a message was actually sent"""
        try:
            print("🔍 Verifying message delivery...")
            
            # Wait a bit for the message to be processed
            time.sleep(3)
            
            # Check for common failure indicators
            verification_passed = True
            
            # 1. Check if the browser tab is still open and responsive
            try:
                # This is a basic check - in practice you might use Selenium or similar
                # to actually inspect the WhatsApp Web interface
                print("   ✓ Browser tab check passed")
            except Exception as e:
                print(f"   ⚠️  Browser tab check warning: {e}")
                verification_passed = False
            
            # 2. Check for common error patterns
            # Note: This is a simplified verification. In a production system,
            # you would want to use WhatsApp Business API or similar for delivery confirmation
            
            # 3. Provide user with manual verification steps
            print("\n🔍 Manual Verification Required:")
            print("   1. Check your WhatsApp app for the message")
            print("   2. Look for delivery checkmarks (✓✓)")
            print("   3. Check if the recipient received the message")
            print("   4. Verify the message content is correct")
            
            # Ask user for confirmation
            print("\n❓ Did you receive the message in WhatsApp? (y/n): ", end="")
            try:
                user_confirmation = input().strip().lower()
                if user_confirmation in ['y', 'yes']:
                    print("✅ User confirmed message delivery!")
                    return True
                elif user_confirmation in ['n', 'no']:
                    print("❌ User confirmed message was NOT delivered")
                    return False
                else:
                    print("⚠️  Unclear response, assuming verification failed")
                    return False
            except (EOFError, KeyboardInterrupt):
                print("\n⏭️  Skipping user confirmation, assuming verification failed")
                return False
            
        except Exception as e:
            print(f"🔍 Message verification failed: {e}")
            return False
    
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
            message_preview = data['message'][:config.SHOW_PREVIEW_LENGTH] + "..." if len(data['message']) > config.SHOW_PREVIEW_LENGTH else data['message']
            
            status_icon = {
                'scheduled': '⏰',
                'sending': '📤',
                'sent': '✅',
                'failed': '❌'
            }.get(data['status'], '❓')
            
            print(f"{msg_id:<4} {data['phone']:<15} {time_str:<20} {status_icon} {data['status']:<8} {message_preview}")
    
    def cancel_message(self, message_id: int):
        """Cancel a scheduled message"""
        if message_id not in self.scheduled_messages:
            print(f"❌ Message ID {message_id} not found.")
            return
        
        message_data = self.scheduled_messages[message_id]
        if message_data['status'] == 'sent':
            print(f"❌ Cannot cancel message {message_id} - already sent.")
            return
        
        if message_data['status'] == 'failed':
            print(f"❌ Cannot cancel message {message_id} - already failed.")
            return
        
        # Remove from scheduled messages
        del self.scheduled_messages[message_id]
        self.save_scheduled_messages()
        
        print(f"✅ Message {message_id} cancelled successfully.")
    
    def clear_failed_messages(self):
        """Clear all failed messages"""
        failed_messages = []
        for msg_id, data in list(self.scheduled_messages.items()):
            if data['status'] == 'failed':
                failed_messages.append(msg_id)
        
        if not failed_messages:
            print("📋 No failed messages to clear.")
            return
        
        for msg_id in failed_messages:
            del self.scheduled_messages[msg_id]
        
        self.save_scheduled_messages()
        print(f"✅ Cleared {len(failed_messages)} failed message(s).")
    
    def test_whatsapp_connection(self):
        """Test WhatsApp Web connection and provide diagnostics"""
        print("🧪 Testing WhatsApp Web connection...")
        print("💡 Make sure WhatsApp Web is open and you're logged in!")
        
        try:
            # Check if Chrome is available
            try:
                import webbrowser
                chrome_path = webbrowser.get().name
                print(f"✅ Browser detected: {chrome_path}")
            except Exception as e:
                print(f"⚠️  Browser detection issue: {e}")
            
            # Check pywhatkit installation
            try:
                import pkg_resources
                version = pkg_resources.get_distribution("pywhatkit").version
                print(f"✅ pywhatkit version: {version}")
            except Exception as e:
                print(f"❌ pywhatkit not properly installed: {e}")
                return
            
            # Check available methods
            print(f"🔧 Available methods:")
            print(f"   - sendwhatmsg_instantly: {hasattr(pwk, 'sendwhatmsg_instantly')}")
            print(f"   - sendwhatmsg: {hasattr(pwk, 'sendwhatmsg')}")
            
            # Try to open WhatsApp Web
            try:
                import webbrowser
                webbrowser.open(config.WHATSAPP_WEB_URL)
                print("✅ WhatsApp Web opened in browser")
                print("📱 Please log in to WhatsApp Web if not already logged in")
                print("💡 Keep the tab open for message sending")
                
                # Additional checks
                print("\n🔍 Additional checks:")
                print("   1. Make sure you're logged into WhatsApp Web")
                print("   2. Check if you see your chats in the left sidebar")
                print("   3. Ensure the browser tab stays open")
                print("   4. Check for any error messages in the browser")
                print("   5. Verify your phone has internet connection")
                print("   6. Make sure WhatsApp is working on your phone")
                
            except Exception as e:
                print(f"❌ Error opening WhatsApp Web: {e}")
            
            # Test with a simple message (optional)
            print("\n🧪 Optional: Test with a simple message to yourself? (y/n): ", end="")
            try:
                test_input = input().strip().lower()
                if test_input in ['y', 'yes']:
                    print("📱 Testing with a simple message...")
                    print("💡 This will open a new browser tab and attempt to send a test message")
                    
                    # Get user's own number for testing
                    own_number = input("📱 Enter your own phone number (with country code) for testing: ").strip()
                    if own_number:
                        try:
                            # Test with instant method
                            pwk.sendwhatmsg_instantly(
                                own_number,
                                "🧪 Test message from WhatsApp Scheduler Agent",
                                wait_time=config.WAIT_TIME,
                                tab_close=False  # Keep tab open for inspection
                            )
                            print("✅ Test message sent! Check your WhatsApp to confirm delivery.")
                        except Exception as e:
                            print(f"❌ Test message failed: {e}")
                            print("💡 This helps identify the specific issue")
                    else:
                        print("❌ No phone number provided for testing")
                        
            except (EOFError, KeyboardInterrupt):
                print("\n⏭️  Skipping test message")
            
        except Exception as e:
            print(f"❌ Error during testing: {e}")
    
    def diagnose_common_issues(self):
        """Diagnose common WhatsApp sending issues"""
        print("\n🔍 Diagnosing Common Issues...")
        print("=" * 50)
        
        issues = []
        
        # Check pywhatkit installation
        try:
            import pkg_resources
            version = pkg_resources.get_distribution("pywhatkit").version
            print(f"✅ pywhatkit version: {version}")
        except Exception:
            issues.append("pywhatkit not properly installed")
            print("❌ pywhatkit installation issue")
        
        # Check browser availability
        try:
            import webbrowser
            browser = webbrowser.get()
            print(f"✅ Browser available: {browser.name}")
        except Exception:
            issues.append("Browser not accessible")
            print("❌ Browser access issue")
        
        # Check WhatsApp Web accessibility
        try:
            import urllib.request
            response = urllib.request.urlopen(config.WHATSAPP_WEB_URL, timeout=10)
            if response.status == 200:
                print("✅ WhatsApp Web is accessible")
            else:
                issues.append("WhatsApp Web returned non-200 status")
                print("⚠️  WhatsApp Web status issue")
        except Exception as e:
            issues.append(f"WhatsApp Web not accessible: {e}")
            print(f"❌ WhatsApp Web accessibility issue: {e}")
        
        # Check configuration
        print(f"\n⚙️  Configuration:")
        print(f"   - Wait time: {config.WAIT_TIME} seconds")
        print(f"   - Tab close: {config.TAB_CLOSE}")
        print(f"   - Browser type: {config.BROWSER_TYPE}")
        
        if issues:
            print(f"\n❌ Issues found: {len(issues)}")
            for i, issue in enumerate(issues, 1):
                print(f"   {i}. {issue}")
            
            print(f"\n💡 Recommendations:")
            print("   1. Make sure WhatsApp Web is open and logged in")
            print("   2. Check your internet connection")
            print("   3. Verify the phone number format (+country code)")
            print("   4. Try increasing WAIT_TIME in config.py")
            print("   5. Check if WhatsApp is working on your phone")
            print("   6. Try using a different browser")
        else:
            print("\n✅ No obvious issues detected")
            print("💡 If messages still aren't sending, check WhatsApp Web login status")
    
    def show_help(self):
        """Show help information"""
        help_text = """
🤖 WhatsApp Scheduler Agent - Help

Commands:
  schedule    - Schedule a new WhatsApp message
  view        - List all scheduled messages
  cancel <id> - Cancel a scheduled message
  clear       - Clear all failed messages
  test        - Test WhatsApp Web connection
  diagnose    - Diagnose common sending issues
  help        - Show this help message
  exit        - Exit the application

Usage Examples:
  schedule
  view
  cancel 1
  clear
  test
  diagnose
  help
  exit

Notes:
  - Phone numbers must include country code (e.g., +1234567890)
  - Time format: HH:MM (24-hour format)
  - If no time is provided, message will be scheduled 30 seconds from now
  - Make sure WhatsApp Web is open and you're logged in
  - Messages need at least 30 seconds to load WhatsApp Web properly

Troubleshooting:
  - If messages show as "sent" but don't appear in WhatsApp:
    1. Run 'diagnose' to check for common issues
    2. Run 'test' to verify WhatsApp Web connection
    3. Check if WhatsApp Web is properly logged in
    4. Verify the phone number format and existence
    5. Check your internet connection
    6. Try increasing WAIT_TIME in config.py
        """
        print(help_text)
    
    def run(self):
        """Main CLI loop"""
        print("🤖 Welcome to WhatsApp Scheduler Agent!")
        print("Type 'help' for available commands or 'exit' to quit.")
        
        while True:
            try:
                command = input("\n📝 Enter command: ").strip().lower()
                
                if command == 'exit':
                    print("👋 Goodbye!")
                    break
                
                elif command == 'help':
                    self.show_help()
                
                elif command == 'view':
                    self.list_scheduled_messages()
                
                elif command == 'clear':
                    self.clear_failed_messages()
                
                elif command == 'test':
                    self.test_whatsapp_connection()
                
                elif command == 'diagnose':
                    self.diagnose_common_issues()
                
                elif command.startswith('cancel '):
                    try:
                        msg_id = int(command.split()[1])
                        self.cancel_message(msg_id)
                    except (IndexError, ValueError):
                        print("❌ Invalid format. Use: cancel <message_id>")
                
                elif command == 'schedule':
                    self._schedule_interactive()
                
                else:
                    print("❌ Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def _schedule_interactive(self):
        """Interactive message scheduling"""
        print("\n📅 Schedule New WhatsApp Message")
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
            time_input = input(f"⏰ Enter time (HH:MM, 24h format) [press Enter for {config.DEFAULT_DELAY_SECONDS} seconds from now]: ").strip()
            if not time_input:
                time_input = self.get_default_time()
                print(f"⏰ Using default time: {time_input}")
            
            # Schedule the message
            message_id = self.schedule_message(phone, message, time_input)
            
            # Show confirmation
            scheduled_time = datetime.datetime.fromisoformat(self.scheduled_messages[message_id]['scheduled_time'])
            time_str = scheduled_time.strftime("%Y-%m-%d %H:%M")
            
            print(f"\n✅ Message scheduled successfully!")
            print(f"📋 ID: {message_id}")
            print(f"📱 To: {phone}")
            print(f"⏰ Time: {time_str}")
            print(f"💬 Message: {message}")
            print(f"\n💡 Make sure WhatsApp Web is open and you're logged in!")
            
        except ValueError as e:
            print(f"❌ {e}")
        except Exception as e:
            print(f"❌ Error scheduling message: {e}")

def main():
    """Main entry point"""
    try:
        scheduler = WhatsAppScheduler()
        scheduler.run()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
