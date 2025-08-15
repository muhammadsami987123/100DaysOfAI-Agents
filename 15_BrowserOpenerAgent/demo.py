#!/usr/bin/env python3
"""
🎬 Demo script for BrowserOpenerAgent

Showcases the new smart search and improved features.
"""

import sys
import os
from unittest.mock import patch

# Add the current directory to the path so we can import main
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import BrowserOpenerAgent
from rich.console import Console
from rich.panel import Panel

console = Console()


def demo_basic_commands():
    """Demo basic site opening commands."""
    console.print(Panel.fit(
        "🎯 Demo: Basic Commands",
        title="Basic Site Opening",
        border_style="blue"
    ))
    
    agent = BrowserOpenerAgent(enable_voice=False)
    
    test_commands = [
        "Open YouTube",
        "Go to Google", 
        "Launch GitHub",
        "Visit OpenAI"
    ]
    
    for command in test_commands:
        console.print(f"\n🎤 Command: {command}")
        with patch('webbrowser.open') as mock_open:
            agent.process_command(command)
            console.print("✅ Command processed successfully!")


def demo_smart_search():
    """Demo smart search functionality."""
    console.print(Panel.fit(
        "🔍 Demo: Smart Search",
        title="Search Within Websites",
        border_style="green"
    ))
    
    agent = BrowserOpenerAgent(enable_voice=False)
    
    test_commands = [
        "Open YouTube and search for lo-fi music",
        "Go to Google and search for AI tools",
        "Launch GitHub and search for python projects",
        "Open Wikipedia and search for machine learning"
    ]
    
    for command in test_commands:
        console.print(f"\n🎤 Command: {command}")
        with patch('webbrowser.open') as mock_open:
            agent.process_command(command)
            console.print("✅ Search command processed successfully!")


def demo_fallback():
    """Demo fallback to Google search."""
    console.print(Panel.fit(
        "🤔 Demo: Fallback to Google",
        title="Unknown Commands",
        border_style="yellow"
    ))
    
    agent = BrowserOpenerAgent(enable_voice=False)
    
    test_commands = [
        "Open my custom tutorials",
        "Go to machine learning course",
        "Visit my personal blog"
    ]
    
    for command in test_commands:
        console.print(f"\n🎤 Command: {command}")
        with patch('webbrowser.open') as mock_open:
            agent.process_command(command)
            console.print("✅ Fallback processed successfully!")


def demo_clean_ui():
    """Demo the clean UI improvements."""
    console.print(Panel.fit(
        "✨ Demo: Clean UI Features",
        title="Improved User Experience",
        border_style="cyan"
    ))
    
    console.print("🎤 Listening...")
    console.print("🧠 Processing...")
    console.print("🌐 Opening: YouTube")
    console.print("✅ YouTube opened successfully!")
    
    console.print("\n🎤 Listening...")
    console.print("🧠 Processing: YouTube search for 'lo-fi music'")
    console.print("✅ YouTube search completed!")
    
    console.print("\n🤔 Couldn't understand your command. Redirecting to Google search.")
    console.print("✅ Browser opened successfully!")


def main():
    """Run the demo."""
    console.print(Panel.fit(
        "🌐 BrowserOpenerAgent Demo\n"
        "Showcasing the new smart search and improved features!",
        title="BrowserOpenerAgent Demo",
        border_style="blue"
    ))
    
    # Demo basic commands
    demo_basic_commands()
    
    # Demo smart search
    demo_smart_search()
    
    # Demo fallback
    demo_fallback()
    
    # Demo clean UI
    demo_clean_ui()
    
    console.print(Panel.fit(
        "🎉 Demo completed!\n"
        "Try running the agent with:\n"
        "• python main.py (CLI mode)\n"
        "• python main.py --voice (Voice mode)",
        title="Demo Complete",
        border_style="green"
    ))


if __name__ == "__main__":
    main()
