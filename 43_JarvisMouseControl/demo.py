#!/usr/bin/env python3
"""
JarvisMouseControl Demo Script
Demonstrates the improved voice control functionality
"""

import sys
import time
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from main import JarvisMouseControl

def main():
    """Run a demo of JarvisMouseControl"""
    print("=" * 60)
    print("🎬 JarvisMouseControl Demo")
    print("=" * 60)
    print("This demo showcases the improved voice control functionality.")
    print("You can switch between voice and text modes during the demo.")
    print("=" * 60)
    
    # Create agent with voice enabled
    agent = JarvisMouseControl(language="en", voice_enabled=True, tts_enabled=True)
    
    print("\n🚀 Starting demo...")
    print("💡 Try these commands:")
    print("   - 'click' - Left click")
    print("   - 'move up' - Move cursor up")
    print("   - 'move down' - Move cursor down")
    print("   - 'voice' - Switch to voice mode")
    print("   - 'help' - Show all commands")
    print("   - 'quit' - Exit demo")
    
    try:
        # Start the agent
        agent.start()
    except KeyboardInterrupt:
        print("\n🛑 Demo interrupted by user")
    except Exception as e:
        print(f"❌ Demo error: {e}")
    finally:
        print("\n👋 Demo completed. Thank you!")

if __name__ == "__main__":
    main()
