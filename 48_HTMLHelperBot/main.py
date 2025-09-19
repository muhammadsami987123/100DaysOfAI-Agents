import argparse
import sys
import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.status import Status
from rich.live import Live
from rich.spinner import Spinner
from time import sleep
from typing import Optional

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.openai_config import OpenAIConfig
from core.html_generator import HtmlGenerator
from core.html_explainer import HtmlExplainer
from utils.cli_interface import CLIInterface
from core.html_chatbot import HtmlChatbot

class HTMLHelperBot:
    """Main HTML Helper Bot class"""

    def __init__(self):
        self.console = Console()
        self.config = OpenAIConfig()
        self.cli = CLIInterface()
        self.generator = HtmlGenerator(self.config)
        self.explainer = HtmlExplainer(self.config)
        self.chatbot = HtmlChatbot(self.config)
        self.last_output_html = None

    def process_input(self, args) -> None:
        """Process user input and determine action"""
        if args.generate:
            self.handle_generate_html(args.generate, args.version, args.minimal, args.save)
        elif args.explain:
            self.handle_explain_html(args.explain, args.save)
        elif args.menu:
            self.show_main_menu()
        elif args.interactive:
            self.interactive_mode()
        elif args.chat:
            self.handle_chat_mode()
        else:
            self.cli.print_info("Welcome to HTMLHelperBot. Use --menu or --help for options.")

    def handle_generate_html(self, description: str, html_version: str, minimal: bool, save_file: Optional[str]) -> None:
        """Handle HTML generation request"""
        self.cli.print_header("🧠 Generating HTML")
        generated_html = ""
        with self.console.status("[bold blue]Calling OpenAI for HTML generation...[/bold blue]", spinner="dots") as status:
            # For a streaming effect, we could modify HtmlGenerator to stream tokens.
            # For now, we'll just show a spinner.
            sleep(1)
            generated_html = self.generator.generate_html(description, html_version, minimal)
            status.update("[bold green]HTML Generation Complete![/bold green]")

        self.last_output_html = generated_html
        self.cli.print_html_output(generated_html)

        if save_file:
            self.save_html_to_file(generated_html, save_file)
        
        if self.cli.confirm_action("Do you want to copy the generated HTML to clipboard?"):
            self.cli.copy_to_clipboard(generated_html)

    def handle_explain_html(self, html_code: str, save_file: Optional[str]) -> None:
        """Handle HTML explanation request"""
        self.cli.print_header("🔍 Explaining HTML")
        explained_content = ""
        with self.console.status("[bold blue]Calling OpenAI for HTML explanation...[/bold blue]", spinner="dots") as status:
            sleep(1)
            explained_content = self.explainer.explain_html(html_code)
            status.update("[bold green]HTML Explanation Complete![/bold green]")

        self.last_output_html = explained_content # Store explanation for potential saving
        self.cli.print_markdown(explained_content)

        if save_file:
            self.save_html_to_file(explained_content, save_file, is_html=False) # Save explanation as text

        if self.cli.confirm_action("Do you want to copy the explanation to clipboard?"):
            self.cli.copy_to_clipboard(explained_content)

    def save_html_to_file(self, content: str, filename: str, is_html: bool = True) -> None:
        """Save generated HTML or explanation to a file"""
        if not self.cli.confirm_action(f"Do you want to save the output to {filename}?"):
            self.cli.print_info("Save cancelled.")
            return

        try:
            if is_html:
                # Extract raw HTML from markdown code block if present
                if content.strip().startswith('```html') and content.strip().endswith('```'):
                    content_to_save = content.strip()[len('```html'):-len('```')].strip()
                else:
                    content_to_save = content
            else:
                # For explanations, save the markdown content directly
                content_to_save = content

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content_to_save)
            self.cli.print_success(f"Output successfully saved to [green]{filename}[/green]")
        except Exception as e:
            self.cli.print_error(f"Error saving file: {e}")

    def handle_chat_mode(self) -> None:
        """Handles conversational chat mode"""
        self.cli.print_header("💬 HTML Chatbot")
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

            with self.console.status("[bold blue]Chatbot thinking...[/bold blue]", spinner="dots"):
                response = self.chatbot.chat(user_message)
            self.cli.print_markdown(response)

    def show_main_menu(self) -> None:
        """Show main menu and handle user choices"""
        self.cli.print_welcome()
        while True:
            choice = self.cli.show_main_menu()

            if choice == "1":
                description = self.cli.get_user_input("Describe the HTML you want to generate:")
                if description:
                    self.handle_generate_html(description, self.config.get_env_variable("HTML_VERSION", "html5"),
                                              self.config.get_env_variable("MINIMAL_MARKUP", "false").lower() == "true", None)
            elif choice == "2":
                html_code = self.cli.get_user_input("Paste your HTML code to explain:")
                if html_code:
                    self.handle_explain_html(html_code, None)
            elif choice == "3":
                if self.last_output_html:
                    filename = self.cli.get_user_input("Enter filename to save (e.g., output.html):", default="output.html")
                    is_html_content = self.last_output_html.strip().startswith('```html') # Simple heuristic
                    self.save_html_to_file(self.last_output_html, filename, is_html=is_html_content)
                else:
                    self.cli.print_warning("No output to save. Generate or explain HTML first.")
            elif choice == "4":
                self.handle_chat_mode()
            elif choice == "5":
                self.cli.print_help()
            elif choice in ["0", "exit", "quit", "q"]:
                self.cli.print_info("Goodbye! 👋")
                break
            elif choice:
                # Attempt to parse direct commands from menu input
                self.parse_and_process_direct_command(choice)

    def parse_and_process_direct_command(self, command_str: str) -> None:
        """Parses a command string from direct input and processes it."""
        parser = self._create_arg_parser()
        try:
            # Split the command string, handling quoted arguments
            import shlex
            args_list = shlex.split(command_str)
            args = parser.parse_args(args_list)

            # Re-use existing handlers
            if args.generate:
                self.handle_generate_html(args.generate, args.version, args.minimal, args.save)
            elif args.explain:
                self.handle_explain_html(args.explain, args.save)
            else:
                self.cli.print_error("Invalid command. Use --generate or --explain.")
        except SystemExit: # argparse exits on error or --help
            self.cli.print_error("Invalid command syntax or argument. Use --help for usage.")
        except Exception as e:
            self.cli.print_error(f"Error processing command: {e}")

    def interactive_mode(self) -> None:
        """Run in interactive mode (future expansion for quick actions)"""
        self.cli.print_info("Interactive mode is under development. Please use the main menu for now.")
        self.show_main_menu()

    def _create_arg_parser(self):
        """Creates and returns the argument parser."""
        parser = argparse.ArgumentParser(description="HTMLHelperBot - AI-powered HTML assistant")
        parser.add_argument('--generate', type=str, help='Describe the HTML to generate (e.g., "responsive pricing table")')
        parser.add_argument('--explain', type=str, help='Provide HTML code to explain (e.g., "<div><h1>Hello</h1></div>")')
        parser.add_argument('--save', type=str, help='Save the output to a specified .html file')
        parser.add_argument('--version', type=str, default=self.config.get_env_variable("HTML_VERSION", "html5"),
                            help='Specify HTML version for generation (e.g., html5). Default from .env or html5.')
        parser.add_argument('--minimal', action='store_true', help='Generate minimal HTML markup.')
        parser.add_argument('--menu', '-m', action='store_true', help='Show main menu (default if no other args)')
        parser.add_argument('--interactive', '-i', action='store_true', help='Run in interactive mode (future quick actions)')
        parser.add_argument('--chat', '-c', action='store_true', help='Enter chatbot conversation mode')
        return parser

def main():
    """Main entry point"""
    bot = HTMLHelperBot()
    parser = bot._create_arg_parser() # Get the parser from the bot instance
    args = parser.parse_args()

    if len(sys.argv) == 1 or args.menu: # If no arguments or --menu is passed
        bot.show_main_menu()
    else:
        bot.process_input(args)

if __name__ == "__main__":
    main()
