#!/usr/bin/env python3
"""
🌐 BrowserOpenerAgent - Day 15 of #100DaysOfAI-Agents

A voice and CLI-driven agent that opens URLs in the system's default web browser.
Supports natural language commands and voice input for opening websites.

Features:
- Voice command recognition with silence detection
- Natural language URL parsing
- Smart search within websites
- Common site name mapping (YouTube, Google, etc.)
- Fallback to Google search for unknown sites
- Clean and minimal UI feedback
- Cross-platform browser support

Author: Muhammad Sami Asghar Mughal
"""

import argparse
import json
import logging
import os
import re
import sys
import time
import webbrowser
from typing import Optional, Dict, List, Tuple
from urllib.parse import urlparse, quote_plus

try:
    import speech_recognition as sr
except ImportError:
    sr = None

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.status import Status
from rich.prompt import Prompt

console = Console()


class SpeechOutput:
    """Handles text-to-speech output for voice feedback."""
    
    def __init__(self, enable_voice: bool = True, rate: int = 175):
        self.enable_voice = enable_voice and (pyttsx3 is not None)
        self.engine = None
        if self.enable_voice:
            try:
                self.engine = pyttsx3.init()
                self.engine.setProperty("rate", rate)
            except Exception:
                self.enable_voice = False

    def say(self, text: str) -> None:
        """Speak the given text."""
        if not self.enable_voice or not self.engine:
            return
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception:
            pass


class SpeechInput:
    """Handles speech recognition for voice input with improved accuracy."""
    
    def __init__(self, language_hint: Optional[str] = None):
        self.language_hint = language_hint
        self.available = sr is not None
        if self.available:
            try:
                self.recognizer = sr.Recognizer()
                # Improved settings for better accuracy
                self.recognizer.dynamic_energy_threshold = True
                self.recognizer.energy_threshold = 4000  # Higher threshold to reduce background noise
                self.recognizer.pause_threshold = 0.8  # Shorter pause to detect end of speech
                self.recognizer.non_speaking_duration = 0.5  # Stop listening after 0.5s of silence
            except Exception:
                self.available = False

    def listen_once(self) -> Optional[str]:
        """Listen for voice input with improved silence detection and return transcribed text."""
        if not self.available:
            return None
        try:
            with sr.Microphone() as source:
                with console.status("🎤 Listening...", spinner="dots"):
                    # Adjust for ambient noise with shorter duration
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    # Listen with shorter timeout and phrase time limit
                    audio = self.recognizer.listen(
                        source, 
                        timeout=8,  # Reduced timeout
                        phrase_time_limit=10,  # Reduced phrase time limit
                        snowboy_configuration=None  # Disable hotword detection
                    )
            
            lang = self.language_hint or "en-US"
            try:
                text = self.recognizer.recognize_google(audio, language=lang)
                # Clean up the text
                text = text.strip()
                # Only return if we have meaningful content
                if len(text) > 2:  # Minimum 3 characters to avoid false positives
                    return text
                return None
            except sr.UnknownValueError:
                # Speech was unintelligible
                return None
            except sr.RequestError:
                # API error
                return None
            except Exception:
                # Fallback to Sphinx if available
                try:
                    text = self.recognizer.recognize_sphinx(audio)
                    text = text.strip()
                    if len(text) > 2:
                        return text
                    return None
                except Exception:
                    return None
        except sr.WaitTimeoutError:
            # No speech detected within timeout
            return None
        except Exception:
            return None


class BrowserOpenerAgent:
    """Main agent class for opening URLs in the default browser with smart search capabilities."""
    
    def __init__(self, enable_voice: bool = True):
        self.enable_voice = enable_voice
        self.speech_output = SpeechOutput(enable_voice)
        self.speech_input = SpeechInput()
        
        # Common site mappings with search capabilities
        self.site_mappings = {
            # Social Media
            "youtube": {"url": "https://youtube.com", "search_url": "https://youtube.com/results?search_query={}"},
            "facebook": {"url": "https://facebook.com", "search_url": "https://facebook.com/search/top/?q={}"},
            "twitter": {"url": "https://twitter.com", "search_url": "https://twitter.com/search?q={}"},
            "instagram": {"url": "https://instagram.com", "search_url": "https://instagram.com/explore/tags/{}"},
            "linkedin": {"url": "https://linkedin.com", "search_url": "https://linkedin.com/search/results/all/?keywords={}"},
            "reddit": {"url": "https://reddit.com", "search_url": "https://reddit.com/search/?q={}"},
            "tiktok": {"url": "https://tiktok.com", "search_url": "https://tiktok.com/search?q={}"},
            
            # Search Engines
            "google": {"url": "https://google.com", "search_url": "https://google.com/search?q={}"},
            "bing": {"url": "https://bing.com", "search_url": "https://bing.com/search?q={}"},
            "yahoo": {"url": "https://yahoo.com", "search_url": "https://search.yahoo.com/search?p={}"},
            "duckduckgo": {"url": "https://duckduckgo.com", "search_url": "https://duckduckgo.com/?q={}"},
            
            # Tech Companies
            "openai": {"url": "https://openai.com", "search_url": "https://openai.com/search?q={}"},
            "github": {"url": "https://github.com", "search_url": "https://github.com/search?q={}"},
            "stackoverflow": {"url": "https://stackoverflow.com", "search_url": "https://stackoverflow.com/search?q={}"},
            "microsoft": {"url": "https://microsoft.com", "search_url": "https://microsoft.com/search?q={}"},
            "apple": {"url": "https://apple.com", "search_url": "https://apple.com/search?q={}"},
            "amazon": {"url": "https://amazon.com", "search_url": "https://amazon.com/s?k={}"},
            "netflix": {"url": "https://netflix.com", "search_url": "https://netflix.com/search?q={}"},
            "spotify": {"url": "https://spotify.com", "search_url": "https://open.spotify.com/search/{}"},
            
            # News & Information
            "wikipedia": {"url": "https://wikipedia.org", "search_url": "https://wikipedia.org/wiki/Special:Search?search={}"},
            "bbc": {"url": "https://bbc.com", "search_url": "https://bbc.com/search?q={}"},
            "cnn": {"url": "https://cnn.com", "search_url": "https://cnn.com/search?q={}"},
            "reuters": {"url": "https://reuters.com", "search_url": "https://reuters.com/search/news?blob={}"},
            
            # Development & Learning
            "w3schools": {"url": "https://w3schools.com", "search_url": "https://w3schools.com/search?q={}"},
            "mdn": {"url": "https://developer.mozilla.org", "search_url": "https://developer.mozilla.org/en-US/search?q={}"},
            "python": {"url": "https://python.org", "search_url": "https://python.org/search/?q={}"},
            "pypi": {"url": "https://pypi.org", "search_url": "https://pypi.org/search/?q={}"},
            
            # Common Services
            "gmail": {"url": "https://gmail.com", "search_url": None},
            "outlook": {"url": "https://outlook.com", "search_url": None},
            "dropbox": {"url": "https://dropbox.com", "search_url": None},
            "drive": {"url": "https://drive.google.com", "search_url": None},
            "maps": {"url": "https://maps.google.com", "search_url": "https://maps.google.com/maps?q={}"},
            "translate": {"url": "https://translate.google.com", "search_url": "https://translate.google.com/?sl=auto&tl=en&text={}"},
        }
        
        # Voice command triggers
        self.voice_triggers = [
            "open", "go to", "launch", "navigate to", "visit", "browse to",
            "please open", "can you open", "would you open", "i want to go to"
        ]
        
        # Search keywords
        self.search_keywords = [
            "search for", "search", "find", "look for", "look up", "show me",
            "and search for", "and find", "and look for"
        ]
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('browser_opener.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def is_valid_url(self, url: str) -> bool:
        """Check if a string is a valid URL."""
        try:
            result = urlparse(url)
            # Only accept HTTP and HTTPS protocols for browser opening
            return all([result.scheme in ['http', 'https'], result.netloc])
        except Exception:
            return False

    def extract_site_and_search(self, command: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract site name and search terms from command."""
        original_command = command
        command = command.lower().strip()
        
        # Remove voice triggers
        sorted_triggers = sorted(self.voice_triggers, key=len, reverse=True)
        for trigger in sorted_triggers:
            if command.startswith(trigger):
                command = command[len(trigger):].strip()
                break
        
        # Remove filler words
        filler_words = ["a", "the", "an", "some", "my", "this", "that"]
        command_words = command.split()
        command_words = [word for word in command_words if word.lower() not in filler_words]
        command = " ".join(command_words)
        
        # Check if it's already a valid URL
        if self.is_valid_url(command):
            return command, None
        
        # Check if it contains a URL pattern
        url_pattern = r'https?://[^\s]+'
        url_match = re.search(url_pattern, command)
        if url_match:
            return url_match.group(0), None
        
        # Check for search patterns
        search_terms = None
        for search_keyword in self.search_keywords:
            if search_keyword in command:
                # Split on search keyword
                parts = command.split(search_keyword, 1)
                if len(parts) == 2:
                    site_part = parts[0].strip()
                    search_terms = parts[1].strip()
                    command = site_part
                    break
        
        # Check site mappings
        command_words = command.split()
        
        # Handle repeated words
        if len(command_words) >= 2 and command_words[0] == command_words[1]:
            command_words = [command_words[0]]
            command = command_words[0]
        elif len(command_words) > 2:
            unique_words = list(dict.fromkeys(command_words))
            if len(unique_words) == 1:
                command_words = [unique_words[0]]
                command = unique_words[0]
            elif len(command_words) == 4 and command_words[0] == "open" and command_words[2] == "open" and command_words[1] == command_words[3]:
                command_words = [command_words[1]]
                command = command_words[0]
            elif len(command_words) == 3 and command_words[0] == command_words[2] and command_words[1] == "open":
                command_words = [command_words[0]]
                command = command_words[0]
        
        # Find matching site
        matched_site = None
        for site_name, site_info in self.site_mappings.items():
            if site_name == command:
                matched_site = site_name
                break
            elif site_name in command_words:
                if len(command_words) == 1:
                    matched_site = site_name
                    break
                elif len(command_words) == 2 and command_words[0] == site_name:
                    matched_site = site_name
                    break
                elif site_name in ["youtube", "facebook", "google", "github", "openai"] and len(command_words) <= 2:
                    matched_site = site_name
                    break
        
        return matched_site, search_terms

    def get_clean_site_name(self, site_name: str) -> str:
        """Get a clean, user-friendly site name."""
        site_display_names = {
            "youtube": "YouTube",
            "facebook": "Facebook", 
            "twitter": "Twitter",
            "instagram": "Instagram",
            "linkedin": "LinkedIn",
            "reddit": "Reddit",
            "tiktok": "TikTok",
            "google": "Google",
            "bing": "Bing",
            "yahoo": "Yahoo",
            "duckduckgo": "DuckDuckGo",
            "openai": "OpenAI",
            "github": "GitHub",
            "stackoverflow": "Stack Overflow",
            "microsoft": "Microsoft",
            "apple": "Apple",
            "amazon": "Amazon",
            "netflix": "Netflix",
            "spotify": "Spotify",
            "wikipedia": "Wikipedia",
            "bbc": "BBC",
            "cnn": "CNN",
            "reuters": "Reuters",
            "w3schools": "W3Schools",
            "mdn": "MDN",
            "python": "Python.org",
            "pypi": "PyPI",
            "gmail": "Gmail",
            "outlook": "Outlook",
            "dropbox": "Dropbox",
            "drive": "Google Drive",
            "maps": "Google Maps",
            "translate": "Google Translate"
        }
        return site_display_names.get(site_name, site_name.title())

    def open_url(self, url: str, site_name: Optional[str] = None, search_terms: Optional[str] = None) -> bool:
        """Open URL in the default browser with clean messaging."""
        try:
            # Determine what to display
            if site_name and search_terms:
                clean_name = self.get_clean_site_name(site_name)
                console.print(f"🧠 Processing: {clean_name} search for '{search_terms}'")
                self.speech_output.say(f"Searching {clean_name} for {search_terms}")
            elif site_name:
                clean_name = self.get_clean_site_name(site_name)
                console.print(f"🌐 Opening: {clean_name}")
                self.speech_output.say(f"Opening {clean_name}")
            else:
                console.print(f"🌐 Opening browser...")
                self.speech_output.say("Opening browser")
            
            # Open in default browser
            webbrowser.open(url)
            
            # Success message
            if site_name and search_terms:
                clean_name = self.get_clean_site_name(site_name)
                console.print(f"✅ {clean_name} search completed!")
                self.speech_output.say(f"{clean_name} search completed")
            elif site_name:
                clean_name = self.get_clean_site_name(site_name)
                console.print(f"✅ {clean_name} opened successfully!")
                self.speech_output.say(f"{clean_name} opened successfully")
            else:
                console.print("✅ Browser opened successfully!")
                self.speech_output.say("Browser opened successfully")
            
            self.logger.info(f"Successfully opened URL: {url}")
            return True
            
        except Exception as e:
            error_msg = "❌ Failed to open browser"
            console.print(error_msg)
            self.speech_output.say("Sorry, I couldn't open the browser")
            self.logger.error(f"Failed to open URL {url}: {str(e)}")
            return False

    def process_command(self, command: str) -> bool:
        """Process a voice or text command with smart search capabilities."""
        console.print(f"🧠 Processing...")
        
        site_name, search_terms = self.extract_site_and_search(command)
        
        if not site_name:
            # Fallback to Google search
            console.print("🤔 Couldn't understand your command. Redirecting to Google search.")
            self.speech_output.say("Couldn't understand your command. Redirecting to Google search.")
            
            # Use the original command as search terms
            search_query = command.strip()
            if search_query:
                url = f"https://google.com/search?q={quote_plus(search_query)}"
                return self.open_url(url)
            else:
                # If no search terms, just open Google
                return self.open_url("https://google.com")
        
        # Get site info
        site_info = self.site_mappings.get(site_name)
        if not site_info:
            # Fallback to Google search
            url = f"https://google.com/search?q={quote_plus(command)}"
            return self.open_url(url)
        
        # Determine URL to open
        if search_terms and site_info.get("search_url"):
            # Use search URL
            url = site_info["search_url"].format(quote_plus(search_terms))
        else:
            # Use regular URL
            url = site_info["url"]
            if search_terms:
                # If site doesn't support search, fallback to Google
                url = f"https://google.com/search?q={quote_plus(site_name + ' ' + search_terms)}"
        
        return self.open_url(url, site_name, search_terms)

    def voice_mode(self):
        """Run the agent in voice command mode with improved feedback."""
        console.print(Panel.fit(
            "🎤 Voice Mode Active\n"
            "Say commands like:\n"
            "• 'Open YouTube'\n"
            "• 'Go to Google and search for AI tools'\n"
            "• 'Launch GitHub'\n"
            "• 'Open YouTube and search for lo-fi music'\n\n"
            "Say 'exit' or 'quit' to stop",
            title="BrowserOpenerAgent Voice Mode",
            border_style="blue"
        ))
        
        self.speech_output.say("Voice mode activated. Ready for commands.")
        
        while True:
            try:
                command = self.speech_input.listen_once()
                
                if not command:
                    console.print("🔇 No speech detected, try again...")
                    continue
                
                # Only show heard command if it's not too long
                if len(command) < 50:
                    console.print(f"🎤 Heard: {command}")
                else:
                    console.print(f"🎤 Heard: {command[:47]}...")
                
                if command.lower() in ['exit', 'quit', 'stop', 'goodbye']:
                    console.print("👋 Goodbye!")
                    self.speech_output.say("Goodbye!")
                    break
                
                self.process_command(command)
                
            except KeyboardInterrupt:
                console.print("\n👋 Goodbye!")
                break
            except Exception as e:
                console.print(f"❌ Error: {str(e)}")
                self.logger.error(f"Error in voice mode: {str(e)}")

    def cli_mode(self):
        """Run the agent in CLI mode with improved feedback."""
        console.print(Panel.fit(
            "💻 CLI Mode Active\n"
            "Enter commands like:\n"
            "• 'Open YouTube'\n"
            "• 'Go to Google and search for AI tools'\n"
            "• 'Launch GitHub'\n"
            "• 'Open YouTube and search for lo-fi music'\n\n"
            "Type 'exit' or 'quit' to stop",
            title="BrowserOpenerAgent CLI Mode",
            border_style="green"
        ))
        
        while True:
            try:
                command = Prompt.ask("\n🌐 BrowserOpenerAgent")
                
                if command.lower() in ['exit', 'quit', 'stop']:
                    console.print("👋 Goodbye!")
                    break
                
                if not command.strip():
                    continue
                
                self.process_command(command)
                
            except KeyboardInterrupt:
                console.print("\n👋 Goodbye!")
                break
            except Exception as e:
                console.print(f"❌ Error: {str(e)}")
                self.logger.error(f"Error in CLI mode: {str(e)}")

    def show_help(self):
        """Display help information."""
        help_text = """
🌐 BrowserOpenerAgent - Help

Voice Commands:
• "Open YouTube"
• "Go to Google and search for AI tools"
• "Launch GitHub"
• "Open YouTube and search for lo-fi music"
• "Visit my portfolio"

Smart Search Examples:
• "Open YouTube and search for lo-fi music"
• "Go to Google and search for AI tools"
• "Launch GitHub and search for python projects"
• "Open Wikipedia and search for machine learning"

Supported Sites:
• Social Media: YouTube, Facebook, Twitter, Instagram, LinkedIn, Reddit, TikTok
• Search: Google, Bing, Yahoo, DuckDuckGo
• Tech: OpenAI, GitHub, Stack Overflow, Microsoft, Apple, Amazon
• News: Wikipedia, BBC, CNN, Reuters
• Development: W3Schools, MDN, Python.org, PyPI
• Services: Gmail, Outlook, Dropbox, Google Drive, Maps, Translate

Features:
• Voice recognition with silence detection
• Smart search within websites
• Clean and minimal UI feedback
• Automatic Google search fallback
• Cross-platform browser support

Usage:
• Voice mode: python main.py --voice
• CLI mode: python main.py
• Help: python main.py --help
        """
        console.print(Panel(help_text, title="Help", border_style="yellow"))


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="🌐 BrowserOpenerAgent - Voice and CLI browser opener with smart search",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # CLI mode
  python main.py --voice           # Voice mode
  python main.py --no-voice        # CLI mode without voice feedback
  python main.py --help            # Show help
        """
    )
    
    parser.add_argument(
        "--voice", 
        action="store_true",
        help="Enable voice command mode"
    )
    
    parser.add_argument(
        "--no-voice",
        action="store_true", 
        help="Disable voice feedback in CLI mode"
    )
    
    parser.add_argument(
        "--help-sites",
        action="store_true",
        help="Show list of supported sites"
    )
    
    args = parser.parse_args()
    
    # Show help for sites
    if args.help_sites:
        agent = BrowserOpenerAgent()
        sites_text = "\n".join([f"• {site}: {info['url']}" for site, info in agent.site_mappings.items()])
        console.print(Panel(sites_text, title="Supported Sites", border_style="cyan"))
        return
    
    # Initialize agent
    enable_voice = not args.no_voice
    agent = BrowserOpenerAgent(enable_voice=enable_voice)
    
    # Show welcome message
    console.print(Panel.fit(
        "🌐 Welcome to BrowserOpenerAgent!\n"
        "Your intelligent voice and CLI browser assistant",
        title="BrowserOpenerAgent",
        border_style="blue"
    ))
    
    # Check voice capabilities
    if args.voice and not agent.speech_input.available:
        console.print("❌ Voice recognition not available. Install speech_recognition package.")
        console.print("Running in CLI mode instead...")
        args.voice = False
    
    if enable_voice and not agent.speech_output.enable_voice:
        console.print("⚠️  Text-to-speech not available. Install pyttsx3 package for voice feedback.")
    
    # Run appropriate mode
    if args.voice:
        agent.voice_mode()
    else:
        agent.cli_mode()


if __name__ == "__main__":
    main()
