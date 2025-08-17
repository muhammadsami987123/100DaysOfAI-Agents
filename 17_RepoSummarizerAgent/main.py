#!/usr/bin/env python3
"""
RepoSummarizerAgent - Day 17 of #100DaysOfAI-Agents

A CLI-based AI agent that analyzes GitHub repositories and provides comprehensive summaries
using OpenAI GPT. Supports multiple languages and can save output to files.
"""

import argparse
import sys
import os
import time
from typing import Optional
from pathlib import Path

from config import (
    validate_config, get_language_config, SUPPORTED_LANGUAGES,
    ERROR_MESSAGES, SUCCESS_MESSAGES
)
from github_service import GitHubService
from ai_summarizer import AISummarizer


class RepoSummarizerAgent:
    """Main CLI application for repository summarization."""
    
    def __init__(self):
        self.github_service = None
        self.ai_summarizer = None
        self.language = "en"
        self.language_config = get_language_config("en")
    
    def setup_services(self):
        """Initialize GitHub and AI services."""
        try:
            self.github_service = GitHubService()
            self.ai_summarizer = AISummarizer()
            return True
        except Exception as e:
            self.print_error(f"Failed to initialize services: {str(e)}")
            return False
    
    def print_banner(self):
        """Print the application banner."""
        banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🔍 RepoSummarizerAgent - Day 17                        ║
║                                                                              ║
║           AI-powered GitHub repository analysis and summarization           ║
║                                                                              ║
║                    Part of #100DaysOfAI-Agents Challenge                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def print_progress(self, message: str, end: str = "\n"):
        """Print a progress message with spinner."""
        spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        current_spinner = spinner[int(time.time() * 10) % len(spinner)]
        print(f"{current_spinner} {message}", end=end, flush=True)
    
    def print_success(self, message: str):
        """Print a success message."""
        print(f"✅ {message}")
    
    def print_error(self, message: str):
        """Print an error message."""
        print(f"❌ {message}")
    
    def print_info(self, message: str):
        """Print an info message."""
        print(f"ℹ️  {message}")
    
    def print_summary(self, summary: str, repo_name: str):
        """Print the generated summary in a formatted way."""
        print("\n" + "="*80)
        print(f"📋 Repository Summary: {repo_name}")
        print("="*80)
        print(summary)
        print("="*80)
    
    def save_summary(self, summary: str, repo_name: str) -> bool:
        """Save the summary to a text file."""
        try:
            # Clean repo name for filename
            safe_name = "".join(c for c in repo_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_')
            
            filename = f"{safe_name}_summary.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Repository Summary: {repo_name}\n")
                f.write("="*50 + "\n")
                f.write(f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Language: {self.language_config['name']}\n")
                f.write("="*50 + "\n\n")
                f.write(summary)
            
            self.print_success(f"Summary saved to: {filename}")
            return True
            
        except Exception as e:
            self.print_error(f"Failed to save summary: {str(e)}")
            return False
    
    def analyze_repository(self, github_url: str, save_output: bool = False) -> bool:
        """Main method to analyze a GitHub repository."""
        try:
            # Step 1: Fetch repository data
            self.print_progress(self.language_config["fetching"])
            repo_data = self.github_service.analyze_repository(github_url)
            repo_name = repo_data['repository_info']['name']
            
            print(f"\r✅ {self.language_config['fetching']}")
            self.print_info(f"Found {repo_data['total_files']} files, analyzing {repo_data['analyzable_files']} key files")
            
            # Step 2: Generate AI summary
            self.print_progress(self.language_config["generating"])
            summary = self.ai_summarizer.generate_summary(repo_data, self.language)
            
            print(f"\r✅ {self.language_config['generating']}")
            
            # Step 3: Display summary
            self.print_summary(summary, repo_name)
            
            # Step 4: Save to file if requested
            if save_output:
                self.print_progress(self.language_config["saving"])
                success = self.save_summary(summary, repo_name)
                if success:
                    print(f"\r✅ {self.language_config['saved']}")
                else:
                    print(f"\r❌ Failed to save")
            
            return True
            
        except ValueError as e:
            self.print_error(str(e))
            return False
        except Exception as e:
            self.print_error(f"Unexpected error: {str(e)}")
            return False
    
    def run(self, args):
        """Main run method."""
        # Print banner
        self.print_banner()
        
        # Validate configuration
        errors = validate_config()
        if errors:
            for error in errors:
                self.print_error(error)
            return False
        
        # Setup services
        if not self.setup_services():
            return False
        
        # Set language
        self.language = args.lang.lower()
        self.language_config = get_language_config(self.language)
        
        # Show language info
        self.print_info(f"Language: {self.language_config['name']} ({self.language.upper()})")
        
        # Show model info
        model_info = self.ai_summarizer.get_model_info()
        self.print_info(f"AI Model: {model_info['model']}")
        
        # Analyze repository
        success = self.analyze_repository(args.url, args.save)
        
        if success:
            self.print_success(self.language_config["complete"])
        else:
            self.print_error("Repository analysis failed")
        
        return success


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="RepoSummarizerAgent - AI-powered GitHub repository analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --url https://github.com/user/repo
  python main.py --url https://github.com/user/repo --lang hi
  python main.py --url https://github.com/user/repo --lang ur --save

Supported Languages:
  en - English (default)
  hi - Hindi
  ur - Urdu
        """
    )
    
    parser.add_argument(
        '--url', '-u',
        required=True,
        help='GitHub repository URL to analyze'
    )
    
    parser.add_argument(
        '--lang', '-l',
        choices=['en', 'hi', 'ur'],
        default='en',
        help='Language for output (default: en)'
    )
    
    parser.add_argument(
        '--save', '-s',
        action='store_true',
        help='Save summary to a text file'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='RepoSummarizerAgent v1.0.0 - Day 17 of #100DaysOfAI-Agents'
    )
    
    args = parser.parse_args()
    
    # Create and run the agent
    agent = RepoSummarizerAgent()
    success = agent.run(args)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
