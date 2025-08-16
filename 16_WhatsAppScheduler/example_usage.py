#!/usr/bin/env python3
"""
Example usage of WhatsApp Scheduler Agent
This script demonstrates how to use the scheduler programmatically
"""

import datetime
import time
from main import WhatsAppScheduler

def example_basic_usage():
    """Example of basic usage"""
    print("📱 Example: Basic WhatsApp Scheduler Usage")
    print("=" * 50)
    
    # Create scheduler instance
    scheduler = WhatsAppScheduler()
    
    # Example phone number (replace with real number for testing)
    phone = "+1234567890"  # Replace with actual number
    message = "Hello! This is a test message from WhatsApp Scheduler."
    
    # Get time 3 minutes from now
    future_time = datetime.datetime.now() + datetime.timedelta(minutes=3)
    time_str = future_time.strftime("%H:%M")
    
    print(f"📱 Phone: {phone}")
    print(f"💬 Message: {message}")
    print(f"⏰ Time: {time_str}")
    
    try:
        # Schedule the message
        message_id = scheduler.schedule_message(phone, message, time_str)
        print(f"✅ Message scheduled with ID: {message_id}")
        
        # Show scheduled messages
        print("\n📋 Current scheduled messages:")
        scheduler.list_scheduled_messages()
        
        # Wait a moment to see the status
        print("\n⏳ Waiting 5 seconds to see status updates...")
        time.sleep(5)
        
        # Show updated status
        print("\n📋 Updated scheduled messages:")
        scheduler.list_scheduled_messages()
        
    except Exception as e:
        print(f"❌ Error: {e}")

def example_multiple_messages():
    """Example of scheduling multiple messages"""
    print("\n📱 Example: Multiple Message Scheduling")
    print("=" * 50)
    
    scheduler = WhatsAppScheduler()
    
    # Example messages
    messages = [
        ("+1234567890", "Good morning! Have a great day!", "09:00"),
        ("+1234567890", "Lunch reminder!", "12:30"),
        ("+1234567890", "Good evening! How was your day?", "18:00"),
    ]
    
    for phone, message, time_str in messages:
        try:
            message_id = scheduler.schedule_message(phone, message, time_str)
            print(f"✅ Scheduled: {message} at {time_str} (ID: {message_id})")
        except Exception as e:
            print(f"❌ Failed to schedule: {e}")
    
    print("\n📋 All scheduled messages:")
    scheduler.list_scheduled_messages()

def example_message_management():
    """Example of message management operations"""
    print("\n📱 Example: Message Management")
    print("=" * 50)
    
    scheduler = WhatsAppScheduler()
    
    # Schedule a test message
    phone = "+1234567890"
    message = "Test message for management demo"
    time_str = (datetime.datetime.now() + datetime.timedelta(minutes=5)).strftime("%H:%M")
    
    try:
        message_id = scheduler.schedule_message(phone, message, time_str)
        print(f"✅ Scheduled message with ID: {message_id}")
        
        # Show all messages
        print("\n📋 Before cancellation:")
        scheduler.list_scheduled_messages()
        
        # Cancel the message
        print(f"\n🗑️ Cancelling message {message_id}...")
        scheduler.cancel_message(message_id)
        
        # Show updated list
        print("\n📋 After cancellation:")
        scheduler.list_scheduled_messages()
        
    except Exception as e:
        print(f"❌ Error: {e}")

def example_validation():
    """Example of input validation"""
    print("\n📱 Example: Input Validation")
    print("=" * 50)
    
    scheduler = WhatsAppScheduler()
    
    # Test cases
    test_cases = [
        ("1234567890", "Test message", "14:30"),  # Invalid phone (no country code)
        ("+1234567890", "", "14:30"),  # Empty message
        ("+1234567890", "Test message", "25:30"),  # Invalid time
        ("+1234567890", "Test message", "14:30"),  # Valid case
    ]
    
    for phone, message, time_str in test_cases:
        print(f"\nTesting: Phone={phone}, Message='{message}', Time={time_str}")
        try:
            message_id = scheduler.schedule_message(phone, message, time_str)
            print(f"✅ Success: Message ID {message_id}")
        except Exception as e:
            print(f"❌ Validation failed: {e}")

def main():
    """Run all examples"""
    print("🚀 WhatsApp Scheduler Agent - Example Usage")
    print("=" * 60)
    print("This script demonstrates various features of the WhatsApp Scheduler.")
    print("Note: Replace phone numbers with real numbers for actual testing.")
    print("=" * 60)
    
    try:
        # Run examples
        example_basic_usage()
        example_multiple_messages()
        example_message_management()
        example_validation()
        
        print("\n🎉 All examples completed!")
        print("\n💡 To run the interactive scheduler:")
        print("   python main.py")
        
    except KeyboardInterrupt:
        print("\n👋 Examples interrupted by user")
    except Exception as e:
        print(f"\n❌ Example error: {e}")

if __name__ == "__main__":
    main()
