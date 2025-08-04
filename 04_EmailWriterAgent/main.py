#!/usr/bin/env python3
"""
🤖 EmailWriterAgent - Day 4 of #100DaysOfAI-Agents

A smart email composition agent that uses GPT to help write professional emails.
Supports both web UI and terminal interfaces.

Features:
- Natural language email composition with GPT
- Multiple email templates (formal, casual, follow-up, etc.)
- Tone adjustment (professional, friendly, urgent, etc.)
- Subject line generation
- Email preview and editing
- Template management
- Web UI with rich text editor
- Terminal interface for quick emails

Author: Muhammad Sami Asghar Mughal
"""

import argparse
import sys
import uvicorn
from pathlib import Path

from email_agent import EmailAgent
from web_app import create_app
from config import get_api_key, setup_instructions

def main():
    """Main entry point for EmailWriterAgent"""
    parser = argparse.ArgumentParser(
        description="EmailWriterAgent - AI-powered email composition tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --web                    # Start web interface
  python main.py --terminal               # Start terminal interface
  python main.py --quick "meeting tomorrow"  # Quick email via terminal
        """
    )
    
    parser.add_argument(
        "--web", 
        action="store_true", 
        help="Start web interface (default)"
    )
    
    parser.add_argument(
        "--terminal", 
        action="store_true", 
        help="Start terminal interface"
    )
    
    parser.add_argument(
        "--quick", 
        type=str, 
        help="Generate a quick email with the given prompt"
    )
    
    parser.add_argument(
        "--host", 
        default="127.0.0.1", 
        help="Host for web interface (default: 127.0.0.1)"
    )
    
    parser.add_argument(
        "--port", 
        type=int, 
        default=8004, 
        help="Port for web interface (default: 8004)"
    )
    
    args = parser.parse_args()
    
    # Check API key
    api_key = get_api_key()
    if not api_key:
        print("❌ Error: OpenAI API key not found!")
        print()
        setup_instructions()
        sys.exit(1)
    
    # Initialize email agent
    try:
        email_agent = EmailAgent(api_key)
        print("✅ EmailWriterAgent initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing EmailWriterAgent: {e}")
        sys.exit(1)
    
    # Handle different modes
    if args.quick:
        # Quick email generation via terminal
        print(f"📧 Generating quick email for: {args.quick}")
        email = email_agent.generate_quick_email(args.quick)
        print("\n" + "="*50)
        print("📧 GENERATED EMAIL")
        print("="*50)
        print(f"Subject: {email['subject']}")
        print(f"To: {email['to']}")
        print(f"From: {email['from']}")
        print("-" * 50)
        print(email['body'])
        print("="*50)
        
    elif args.terminal:
        # Terminal interface
        print("🤖 EmailWriterAgent - Terminal Mode")
        print("Type 'help' for commands, 'quit' to exit")
        email_agent.run_terminal()
        
    else:
        # Web interface (default)
        print(f"🌐 Starting EmailWriterAgent web interface...")
        print(f"📧 Open your browser to: http://{args.host}:{args.port}")
        print("Press Ctrl+C to stop the server")
        
        app = create_app(email_agent)
        uvicorn.run(
            app, 
            host=args.host, 
            port=args.port,
            log_level="info"
        )

if __name__ == "__main__":
    main() 