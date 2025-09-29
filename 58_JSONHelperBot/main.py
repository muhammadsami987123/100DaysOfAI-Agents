import argparse
import sys
import os
from pathlib import Path
from rich.console import Console
from rich.status import Status
from time import sleep
from typing import Optional, Dict, Any
import json

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.openai_config import OpenAIConfig
from core.json_parser import JsonParser
from core.json_explainer import JsonExplainer
from core.json_formatter import JsonFormatter
from core.json_chatbot import JsonChatbot
from utils.cli_interface import CLIInterface

class JSONHelperBot:
    """Main JSON Helper Bot class"""

    def __init__(self):
        self.console = Console()
        self.config = OpenAIConfig()
        self.cli = CLIInterface()
        self.parser = JsonParser()
        self.explainer = JsonExplainer(self.config)
        self.formatter = JsonFormatter()
        self.chatbot = JsonChatbot(self.config)
        self.last_parsed_json: Optional[Dict[str, Any]] = None

    def process_input(self, args) -> None:
        """Process user input and determine action"""
        if args.interactive:
            self.interactive_mode()
            return
        elif args.chat:
            self.handle_chat_mode()
            return
        elif args.menu:
            self.show_main_menu()
            return

        json_data = None
        error_message = None
        raw_input_content = None
        was_fixed = False

        if args.paste:
            raw_input_content = args.paste
            json_data, error_message, was_fixed = self.parser.parse_from_string(args.paste)
        elif args.upload:
            raw_input_content = f"File: {args.upload}"
            json_data, error_message, was_fixed = self.parser.parse_from_file(args.upload)
        elif args.fetch:
            raw_input_content = f"URL: {args.fetch}"
            json_data, error_message, was_fixed = self.parser.parse_from_url(args.fetch)
        else:
            self.cli.print_info("Welcome to JSONHelperBot. Use --menu or --help for options.")
            return

        if error_message:
            self.cli.print_error(f"Input JSON is invalid: {error_message}")
            if was_fixed:
                self.cli.print_warning("Attempted to fix JSON, but it remains malformed.")
            if raw_input_content:
                self.cli.print_markdown(f"```json\n{raw_input_content}\n```", title="Malformed Input")
            return

        self.last_parsed_json = json_data
        processed_output = self.formatter.pretty_print(json_data)

        if args.clean:
            self.cli.print_header("✨ Cleaned and Formatted JSON")
            if was_fixed:
                self.cli.print_info("Note: Input JSON was automatically fixed before formatting.")
            self.cli.print_json_output(processed_output, title="Formatted JSON")
        else:
            self.cli.print_header("📊 JSON Parsing and Explanation")
            if was_fixed:
                self.cli.print_info("Note: Input JSON was automatically fixed before parsing and explanation.")
            self.cli.print_json_output(processed_output, title="Parsed JSON")
            with self.console.status("[bold blue]Calling OpenAI for JSON explanation...[/bold blue]", spinner="dots") as status:
                sleep(1) # Simulate work
                explanation = self.explainer.explain_json(json_data, was_fixed=was_fixed)
                status.update("[bold green]JSON Explanation Complete![/bold green]")
            self.cli.print_markdown(explanation, title="JSON Explanation and Suggestions")

        if args.save:
            self.save_json_to_file(json_data, args.save)
        
        if args.copy:
            self.cli.copy_to_clipboard(processed_output)
        elif self.cli.confirm_action("Do you want to copy the processed JSON to clipboard?"):
            self.cli.copy_to_clipboard(processed_output)

    def handle_chat_mode(self) -> None:
        """Handles conversational chat mode"""
        self.cli.print_header("💬 JSON Chatbot")
        self.cli.print_info("Type 'reset' to clear chat history, 'exit' or 'quit' to return to the main menu.")
        self.chatbot.reset_chat_history() # Start with a clean history for each chat session

        while True:
            user_message = self.cli.get_user_input("[bold cyan]You[/bold cyan]")
            if user_message.lower() == "exit" or user_message.lower() == "quit":
                self.cli.print_info("Exiting chat mode.")
                break
            if user_message.lower() == "reset":
                self.chatbot.reset_chat_history()
                self.cli.print_info("Chat history reset.")
                continue
            if not user_message.strip():
                continue

            with self.console.status("[bold blue]Chatbot thinking...[/bold blue]", spinner="dots") as status:
                response = self.chatbot.chat(user_message)
            self.cli.print_markdown(response, title="Chatbot Response")

    def interactive_mode(self) -> None:
        """Run in interactive mode"""
        self.cli.print_info("Interactive mode is under development. Please use the main menu for now.")
        self.show_main_menu()

    def save_json_to_file(self, json_data: Dict[str, Any], filename: str) -> None:
        """Save processed JSON to a file"""
        if not self.cli.confirm_action(f"Do you want to save the output to {filename}?"):
            self.cli.print_info("Save cancelled.")
            return

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2)
            self.cli.print_success(f"Output successfully saved to [green]{filename}[/green]")
        except Exception as e:
            self.cli.print_error(f"Error saving file: {e}")

    def show_main_menu(self) -> None:
        """Show main menu and handle user choices"""
        self.cli.print_welcome()
        while True:
            choice = self.cli.show_main_menu()

            if choice == "1": # Paste JSON
                json_string = self.cli.get_multiline_user_input("Paste your JSON string (type END to finish):")
                if json_string:
                    self.process_input(argparse.Namespace(paste=json_string, upload=None, fetch=None, menu=False, clean=False, explain=True, save=None, copy=False, interactive=False, chat=False))
            elif choice == "2": # Upload JSON File
                file_path = self.cli.get_user_input("Enter path to JSON file:")
                if file_path:
                    self.process_input(argparse.Namespace(paste=None, upload=file_path, fetch=None, menu=False, clean=False, explain=True, save=None, copy=False, interactive=False, chat=False))
            elif choice == "3": # Fetch from URL
                url = self.cli.get_user_input("Enter public URL for JSON:")
                if url:
                    self.process_input(argparse.Namespace(paste=None, upload=None, fetch=url, menu=False, clean=False, explain=True, save=None, copy=False, interactive=False, chat=False))
            elif choice == "4": # Chat with Bot
                self.process_input(argparse.Namespace(paste=None, upload=None, fetch=None, menu=False, clean=False, explain=True, save=None, copy=False, interactive=False, chat=True))
            elif choice == "5": # Help
                self.cli.print_help()
            elif choice in ["0", "exit", "quit", "q"]:
                self.cli.print_info("Goodbye! 👋")
                break
            elif choice:
                self.parse_and_process_direct_command(choice)

    def parse_and_process_direct_command(self, command_str: str) -> None:
        """Parses a command string from direct input and processes it."""
        parser = self._create_arg_parser()
        try:
            import shlex
            args_list = shlex.split(command_str)
            args = parser.parse_args(args_list)
            self.process_input(args)
        except SystemExit: # argparse exits on error or --help
            self.cli.print_error("Invalid command syntax or argument. Use --help for usage.")
        except Exception as e:
            self.cli.print_error(f"Error processing command: {e}")

    def _create_arg_parser(self):
        """Creates and returns the argument parser."""
        parser = argparse.ArgumentParser(description="JSONHelperBot - AI-powered JSON assistant")
        parser.add_argument('--paste', type=str, help='Paste JSON string directly (e.g., \'{"key":"value"}\')')
        parser.add_argument('--upload', type=str, help='Upload JSON from a local file path (e.g., data.json)')
        parser.add_argument('--fetch', type=str, help='Fetch JSON from a public URL (e.g., https://api.example.com/data)')
        parser.add_argument('--save', type=str, help='Save the output to a specified .json file')
        parser.add_argument('--clean', action='store_true', help='Only clean/format JSON, skip AI explanation')
        parser.add_argument('--explain', action='store_true', help='Explicitly request AI explanation (default behavior)')
        parser.add_argument('--copy', action='store_true', help='Copy the output to clipboard')
        parser.add_argument('--menu', '-m', action='store_true', help='Show main menu (default if no other args)')
        parser.add_argument('--interactive', '-i', action='store_true', help='Run in interactive mode for quick actions')
        parser.add_argument('--chat', '-c', action='store_true', help='Enter chatbot conversation mode')
        return parser

def main():
    """Main entry point"""
    bot = JSONHelperBot()
    parser = bot._create_arg_parser()
    args = parser.parse_args()

    if len(sys.argv) == 1 or args.menu:
        bot.show_main_menu()
    elif args.interactive:
        bot.interactive_mode()
    else:
        bot.process_input(args)

if __name__ == "__main__":
    main()
