#!/usr/bin/env python3
"""
MemoryNotesBot - AI-powered personal memory assistant
Main entry point for choosing between CLI and Web interfaces
"""

import sys
import os
import argparse
import logging
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from cli import MemoryNotesBotCLI
from web_app import app

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('memory_bot.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="MemoryNotesBot - AI-powered personal memory assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Interactive CLI mode
  python main.py --cli             # CLI mode
  python main.py --web             # Web server mode
  python main.py --web --port 8080 # Web server on custom port
  python main.py --demo            # Demo mode with sample data
        """
    )
    
    parser.add_argument(
        '--cli', 
        action='store_true', 
        help='Run in CLI mode'
    )
    
    parser.add_argument(
        '--web', 
        action='store_true', 
        help='Run web server'
    )
    
    parser.add_argument(
        '--port', 
        type=int, 
        default=Config.PORT,
        help=f'Port for web server (default: {Config.PORT})'
    )
    
    parser.add_argument(
        '--host', 
        default=Config.HOST,
        help=f'Host for web server (default: {Config.HOST})'
    )
    
    parser.add_argument(
        '--demo', 
        action='store_true', 
        help='Run in demo mode with sample data'
    )
    
    parser.add_argument(
        '--version', 
        action='version', 
        version=f'MemoryNotesBot {Config.VERSION}'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Ensure directories exist
    Config.create_directories()
    
    # Demo mode
    if args.demo:
        logger.info("Running in demo mode...")
        run_demo_mode()
        return
    
    # Web mode
    if args.web:
        logger.info(f"Starting web server on {args.host}:{args.port}")
        try:
            app.run(
                host=args.host,
                port=args.port,
                debug=Config.DEBUG
            )
        except KeyboardInterrupt:
            logger.info("Web server stopped by user")
        except Exception as e:
            logger.error(f"Error starting web server: {e}")
            sys.exit(1)
        return
    
    # CLI mode (default)
    if args.cli or not args.web:
        logger.info("Starting CLI mode...")
        try:
            cli = MemoryNotesBotCLI()
            cli.run()
        except KeyboardInterrupt:
            logger.info("CLI stopped by user")
        except Exception as e:
            logger.error(f"Error in CLI mode: {e}")
            sys.exit(1)
        return

def run_demo_mode():
    """Run demo mode with sample data"""
    from memory_store import MemoryStore
    from ai_service import AIService
    
    logger = logging.getLogger(__name__)
    
    # Initialize services
    memory_store = MemoryStore()
    ai_service = AIService()
    
    # Sample memories for demonstration
    sample_memories = [
        {
            "content": "My GitHub personal access token is ghp_1234567890abcdef",
            "memory_type": "password",
            "priority": "critical",
            "tags": ["github", "token", "development"],
            "category": "development"
        },
        {
            "content": "Remember to call Sarah about the project meeting tomorrow at 2 PM",
            "memory_type": "reminder",
            "priority": "high",
            "tags": ["meeting", "sarah", "project"],
            "category": "work"
        },
        {
            "content": "Great idea: Create a mobile app for tracking daily habits",
            "memory_type": "idea",
            "priority": "medium",
            "tags": ["mobile", "app", "habits", "productivity"],
            "category": "ideas"
        },
        {
            "content": "Bank support number: 1-800-123-4567, available 24/7",
            "memory_type": "contact",
            "priority": "medium",
            "tags": ["bank", "support", "contact"],
            "category": "personal"
        },
        {
            "content": "Project deadline for website redesign is March 15th",
            "memory_type": "task",
            "priority": "high",
            "tags": ["deadline", "website", "redesign"],
            "category": "work"
        },
        {
            "content": "Remember to buy groceries: milk, bread, eggs, and vegetables",
            "memory_type": "reminder",
            "priority": "medium",
            "tags": ["groceries", "shopping", "food"],
            "category": "personal"
        },
        {
            "content": "Python virtual environment activation: source venv/bin/activate",
            "memory_type": "long_term",
            "priority": "medium",
            "tags": ["python", "venv", "development"],
            "category": "development"
        },
        {
            "content": "Dentist appointment on Friday at 3 PM",
            "memory_type": "reminder",
            "priority": "high",
            "tags": ["dentist", "appointment", "health"],
            "category": "health"
        }
    ]
    
    logger.info("Adding sample memories...")
    
    for memory_data in sample_memories:
        try:
            memory = memory_store.add_memory(
                content=memory_data["content"],
                memory_type=memory_data["memory_type"],
                priority=memory_data["priority"],
                tags=memory_data["tags"],
                category=memory_data["category"]
            )
            logger.info(f"Added sample memory: {memory.content[:50]}...")
        except Exception as e:
            logger.error(f"Error adding sample memory: {e}")
    
    # Show statistics
    stats = memory_store.get_stats()
    logger.info(f"Demo setup complete! Total memories: {stats.total_memories}")
    logger.info("You can now run the CLI or web interface to explore the sample data.")
    logger.info("Sample commands:")
    logger.info("  python main.py --cli")
    logger.info("  python main.py --web")

if __name__ == "__main__":
    main()
