#!/usr/bin/env python3
"""
GitHelperBot - AI-powered terminal Git assistant
Main CLI entry point for the Git helper bot
"""

import argparse
import sys
import os
from pathlib import Path
from rich.table import Table
from rich.box import ROUNDED

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.command_corrector import CommandCorrector
from core.command_explainer import CommandExplainer
from core.command_executor import CommandExecutor
from config.openai_config import OpenAIConfig
from utils.cli_interface import CLIInterface
from utils.file_generator import FileGenerator
from utils.command_history import CommandHistory


class GitHelperBot:
    """Main Git Helper Bot class"""
    
    def __init__(self):
        self.config = OpenAIConfig()
        self.corrector = CommandCorrector()
        self.explainer = CommandExplainer(self.config)
        self.executor = CommandExecutor()
        self.file_generator = FileGenerator()
        self.cli = CLIInterface()
        self.history = CommandHistory()
        
    def process_input(self, user_input: str) -> None:
        """Process user input and determine action"""
        user_input = user_input.strip()
        
        if not user_input:
            return
            
        # Check if it's a raw Git command
        if user_input.startswith('git '):
            self.handle_git_command(user_input)
        else:
            # Treat as natural language query
            self.handle_natural_language(user_input)
    
    def handle_git_command(self, command: str) -> None:
        """Handle raw Git commands with typo detection"""
        self.cli.print_header("🔍 Analyzing Git Command")
        
        # Check for typos
        correction = self.corrector.correct_command(command)
        
        if correction and correction != command:
            # Show suggestions menu
            suggestions = [correction]
            additional_suggestions = self.corrector.get_suggestions(command, 2)
            suggestions.extend(additional_suggestions)
            
            selected = self.cli.show_suggestion_menu(suggestions, "Command Corrections")
            
            if selected:
                if selected == correction:
                    self.execute_command(selected)
                else:
                    # User selected a different suggestion
                    self.execute_command(selected)
            else:
                # User wants to edit manually
                edited = self.cli.get_user_input("Enter corrected command: ")
                if edited:
                    self.execute_command(edited)
                else:
                    self.cli.print_info("Command cancelled.")
        else:
            # No typos detected, proceed with explanation and execution
            self.explain_and_execute(command)
    
    def handle_natural_language(self, query: str) -> None:
        """Handle natural language queries"""
        self.cli.print_header("🧠 Processing Natural Language Query")
        
        try:
            explanation = self.explainer.explain_query(query)
            self.cli.print_markdown(explanation)
            
            # Ask if user wants to execute any suggested commands
            if "```bash" in explanation:
                choice = self.cli.get_user_choice(
                    "Would you like to execute any of these commands? [Y/N]",
                    ['y', 'n']
                )
                
                if choice == 'y':
                    command = self.cli.get_user_input("Enter the command to execute: ")
                    if command:
                        self.execute_command(command)
                        
        except Exception as e:
            self.cli.print_error(f"Error processing query: {e}")
    
    def explain_and_execute(self, command: str) -> None:
        """Explain command and ask for execution confirmation"""
        try:
            explanation = self.explainer.explain_command(command)
            self.cli.print_markdown(explanation)
            
            choice = self.cli.get_user_choice(
                "Execute this command? [Y/N]",
                ['y', 'n']
            )
            
            if choice == 'y':
                self.execute_command(command)
                
        except Exception as e:
            self.cli.print_error(f"Error explaining command: {e}")
    
    def execute_command(self, command: str) -> None:
        """Execute Git command with safety checks"""
        self.cli.print_header("⚡ Executing Command")
        
        import time
        start_time = time.time()
        
        try:
            result = self.executor.execute_command(command)
            execution_time = time.time() - start_time
            
            if result['success']:
                self.cli.print_success("Command executed successfully!")
                if result['output']:
                    self.cli.print_output(result['output'])
                
                # Add to history
                self.history.add_command(command, success=True, execution_time=execution_time)
            else:
                if result.get('is_help_message', False):
                    self.cli.print_warning("Command needs additional arguments. Here's the usage:")
                    if result['error']:
                        self.cli.print_output(result['error'])
                    
                    # Show usage examples
                    examples = self.corrector.get_usage_examples(command)
                    if examples:
                        self.cli.print_info("Common usage examples:")
                        for example in examples[:3]:  # Show first 3 examples
                            self.cli.print_output(f"  {example}")
                else:
                    self.cli.print_error(f"Command failed: {result['error']}")
                
                # Add to history even if failed
                self.history.add_command(command, success=False, execution_time=execution_time)
                
        except Exception as e:
            self.cli.print_error(f"Execution error: {e}")
            # Add to history even if exception
            self.history.add_command(command, success=False, execution_time=time.time() - start_time)
    
    def generate_files(self, file_type: str) -> None:
        """Generate project files like .gitignore or README"""
        self.cli.print_header(f"📄 Generating {file_type}")
        
        try:
            if file_type.lower() == 'gitignore':
                self.file_generator.generate_gitignore()
            elif file_type.lower() == 'readme':
                self.file_generator.generate_readme()
            else:
                self.cli.print_error(f"Unknown file type: {file_type}")
                return
                
            self.cli.print_success(f"{file_type} generated successfully!")
            
        except Exception as e:
            self.cli.print_error(f"Error generating {file_type}: {e}")
    
    def interactive_mode(self) -> None:
        """Run in interactive mode"""
        self.cli.print_welcome()
        
        while True:
            try:
                # Show quick actions menu
                user_input = self.cli.show_quick_actions()
                
                if not user_input:
                    continue
                elif user_input.lower() in ['exit', 'quit', 'q']:
                    self.cli.print_info("Goodbye! 👋")
                    break
                elif user_input.lower().startswith('generate '):
                    file_type = user_input[9:].strip()
                    self.generate_files(file_type)
                elif user_input.lower() == 'history':
                    self.show_history()
                elif user_input.lower() == 'favorites':
                    self.show_favorites()
                elif user_input.lower() == 'stats':
                    self.show_stats()
                else:
                    self.process_input(user_input)
                    
            except KeyboardInterrupt:
                self.cli.print_info("\nGoodbye! 👋")
                break
            except Exception as e:
                self.cli.print_error(f"Unexpected error: {e}")
    
    def show_main_menu(self) -> None:
        """Show main menu with options"""
        menu_options = [
            ("1", "Git Commands", "Execute Git commands with assistance"),
            ("2", "Natural Language", "Ask questions about Git"),
            ("3", "Generate Files", "Create .gitignore or README files"),
            ("4", "Quick Actions", "Common Git workflows"),
            ("5", "Help", "Show help information"),
            ("0", "Exit", "Leave the application")
        ]
        
        self.cli.console.print("\n[bold cyan]📋 Main Menu[/bold cyan]")
        
        table = Table(show_header=True, box=ROUNDED, padding=(0, 1))
        table.add_column("Key", style="cyan", width=3)
        table.add_column("Option", style="bold white", width=20)
        table.add_column("Description", style="dim white", width=40)
        
        for key, option, desc in menu_options:
            table.add_row(key, option, desc)
        
        self.cli.console.print(table)
        
        choice = self.cli.get_user_input(
            "\n[bold]Select an option (0-5) or type a command",
            default=""
        )
        
        if choice == "1":
            cmd = self.cli.get_user_input("Enter Git command: ")
            if cmd:
                self.process_input(cmd)
        elif choice == "2":
            query = self.cli.get_user_input("Ask about Git: ")
            if query:
                self.handle_natural_language(query)
        elif choice == "3":
            file_type = self.cli.get_user_input("Generate file (gitignore/readme): ")
            if file_type:
                self.generate_files(file_type)
        elif choice == "4":
            self.interactive_mode()
        elif choice == "5":
            self.cli.print_help()
        elif choice == "0":
            self.cli.print_info("Goodbye! 👋")
            return False
        else:
            # Treat as direct command
            if choice:
                self.process_input(choice)
        
        return True
    
    def show_history(self) -> None:
        """Show command history"""
        recent_commands = self.history.get_recent_commands(20)
        if not recent_commands:
            self.cli.print_info("No command history found.")
            return
        
        # Get full history data for display
        history_data = self.history.history[:20]
        selected = self.cli.show_command_history(history_data, 20)
        
        if selected:
            self.process_input(selected)
    
    def show_favorites(self) -> None:
        """Show favorite commands"""
        favorites = self.history.get_favorite_commands()
        if not favorites:
            self.cli.print_info("No favorite commands found.")
            return
        
        selected = self.cli.show_favorites(favorites)
        
        if selected:
            self.process_input(selected)
    
    def show_stats(self) -> None:
        """Show command statistics"""
        stats = self.history.get_command_stats()
        self.cli.show_command_stats(stats)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="GitHelperBot - AI-powered Git assistant")
    parser.add_argument('command', nargs='?', help='Git command or natural language query')
    parser.add_argument('--generate', choices=['gitignore', 'readme'], 
                       help='Generate project files')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Run in interactive mode')
    parser.add_argument('--menu', '-m', action='store_true',
                       help='Show main menu')
    
    args = parser.parse_args()
    
    bot = GitHelperBot()
    
    if args.generate:
        bot.generate_files(args.generate)
    elif args.command:
        bot.process_input(args.command)
    elif args.menu:
        while True:
            if not bot.show_main_menu():
                break
    elif args.interactive:
        bot.interactive_mode()
    else:
        # Default to main menu
        while True:
            if not bot.show_main_menu():
                break


if __name__ == "__main__":
    main()
