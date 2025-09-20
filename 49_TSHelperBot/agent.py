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
from core.ts_generator import TSGenerator
from core.ts_explainer import TSExplainer
from core.ts_refactorer import TSRefactorer
from core.ts_converter import TSConverter
from core.ts_debugger import TSDebugger
from utils.cli_interface import CLIInterface

class TSHelperBot:
    """Main TSHelperBot class"""

    def __init__(self):
        self.console = Console()
        self.config = OpenAIConfig()
        self.cli = CLIInterface()
        self.generator = TSGenerator(self.config)
        self.explainer = TSExplainer(self.config)
        self.refactorer = TSRefactorer(self.config)
        self.converter = TSConverter(self.config)
        self.debugger = TSDebugger(self.config)
        self.last_output_code = None
        self.last_output_lang = "ts"

    def process_input(self, args) -> None:
        """Process user input and determine action"""
        if args.generate:
            self.handle_generate_code(args.generate, args.lang, args.minimal, args.save)
        elif args.explain:
            self.handle_explain_code(args.explain, args.lang, args.save)
        elif args.refactor:
            self.handle_refactor_code(args.refactor, args.lang, args.minimal, args.save)
        elif args.convert and args.to:
            self.handle_convert_code(args.convert, args.to, args.save)
        elif args.debug:
            self.handle_debug_code(args.debug, args.error, args.lang, args.save)
        elif args.menu:
            self.show_main_menu()
        elif args.interactive:
            self.interactive_mode()
        elif args.chat:
            self.handle_chat_mode() # Placeholder for future chat integration
        else:
            self.cli.print_info("Welcome to TSHelperBot. Use --menu or --help for options.")

    def handle_generate_code(self, description: str, language: str, minimal: bool, save_file: Optional[str]) -> None:
        """Handle code generation request"""
        self.cli.print_header("🧠 Generating Code")
        generated_code = ""
        with self.console.status(f"[bold blue]Calling OpenAI for {language.upper()} generation...[/bold blue]", spinner="dots") as status:
            sleep(1) # Simulate work
            generated_code = self.generator.generate_code(description, language, minimal)
            status.update(f"[bold green]{language.upper()} Generation Complete![/bold green]")

        self.last_output_code = generated_code
        self.last_output_lang = language
        self.cli.print_code_output(generated_code, language)

        if save_file:
            self.save_code_to_file(generated_code, save_file, language)
        
        if self.cli.confirm_action("Do you want to copy the generated code to clipboard?"):
            self.cli.copy_to_clipboard(self.extract_raw_code(generated_code, language))

    def handle_explain_code(self, code_snippet: str, language: str, save_file: Optional[str]) -> None:
        """Handle code explanation request"""
        self.cli.print_header("🔍 Explaining Code")
        explained_content = ""
        with self.console.status(f"[bold blue]Calling OpenAI for {language.upper()} explanation...[/bold blue]", spinner="dots") as status:
            sleep(1) # Simulate work
            explained_content = self.explainer.explain_code(code_snippet, language)
            status.update(f"[bold green]{language.upper()} Explanation Complete![/bold green]")

        self.last_output_code = explained_content # Store explanation for potential saving
        self.last_output_lang = "md" # Markdown output
        self.cli.print_markdown(explained_content)

        if save_file:
            self.save_code_to_file(explained_content, save_file, is_code=False) # Save explanation as text

        if self.cli.confirm_action("Do you want to copy the explanation to clipboard?"):
            self.cli.copy_to_clipboard(explained_content)

    def handle_refactor_code(self, code_snippet: str, language: str, minimal: bool, save_file: Optional[str]) -> None:
        """Handle code refactoring request"""
        self.cli.print_header("♻️ Refactoring Code")
        refactored_code = ""
        with self.console.status(f"[bold blue]Calling OpenAI for {language.upper()} refactoring...[/bold blue]", spinner="dots") as status:
            sleep(1) # Simulate work
            refactored_code = self.refactorer.refactor_code(code_snippet, language, minimal)
            status.update(f"[bold green]{language.upper()} Refactoring Complete![/bold green]")

        self.last_output_code = refactored_code
        self.last_output_lang = language
        self.cli.print_code_output(refactored_code, language)

        if save_file:
            self.save_code_to_file(refactored_code, save_file, language)

        if self.cli.confirm_action("Do you want to copy the refactored code to clipboard?"):
            self.cli.copy_to_clipboard(self.extract_raw_code(refactored_code, language))

    def handle_convert_code(self, code_snippet: str, target_language: str, save_file: Optional[str]) -> None:
        """Handle code conversion request"""
        self.cli.print_header("↔️ Converting Code")
        converted_code = ""
        with self.console.status(f"[bold blue]Calling OpenAI for conversion to {target_language.upper()}...[/bold blue]", spinner="dots") as status:
            sleep(1) # Simulate work
            converted_code = self.converter.convert_code(code_snippet, target_language)
            status.update(f"[bold green]Conversion to {target_language.upper()} Complete![/bold green]")

        self.last_output_code = converted_code
        self.last_output_lang = target_language
        self.cli.print_code_output(converted_code, target_language)

        if save_file:
            self.save_code_to_file(converted_code, save_file, target_language)

        if self.cli.confirm_action("Do you want to copy the converted code to clipboard?"):
            self.cli.copy_to_clipboard(self.extract_raw_code(converted_code, target_language))

    def handle_debug_code(self, code_snippet: str, error_message: Optional[str], language: str, save_file: Optional[str]) -> None:
        """Handle code debugging request"""
        self.cli.print_header("🐞 Debugging Code")
        debug_output = ""
        with self.console.status(f"[bold blue]Calling OpenAI for {language.upper()} debugging...[/bold blue]", spinner="dots") as status:
            sleep(1) # Simulate work
            debug_output = self.debugger.debug_code(code_snippet, error_message, language)
            status.update(f"[bold green]{language.upper()} Debugging Complete![/bold green]")

        self.last_output_code = debug_output
        self.last_output_lang = "md" # Debug output will be markdown
        self.cli.print_markdown(debug_output)

        if save_file:
            self.save_code_to_file(debug_output, save_file, is_code=False) # Save explanation as text

        if self.cli.confirm_action("Do you want to copy the debug explanation to clipboard?"):
            self.cli.copy_to_clipboard(debug_output)

    def extract_raw_code(self, content: str, language: str) -> str:
        """Extracts raw code from a markdown code block."""
        # Regex to find code blocks: ```lang\ncode\n```
        pattern = rf"```{{0,3}}{language}\n([\s\S]*?)\n```"
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return content # Return original if no markdown block found

    def save_code_to_file(self, content: str, filename: str, language: str = "txt", is_code: bool = True) -> None:
        """Save generated code or explanation to a file"""
        if not self.cli.confirm_action(f"Do you want to save the output to {filename}?"):
            self.cli.print_info("Save cancelled.")
            return

        try:
            content_to_save = self.extract_raw_code(content, language) if is_code else content

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content_to_save)
            self.cli.print_success(f"Output successfully saved to [green]{filename}[/green]")
        except Exception as e:
            self.cli.print_error(f"Error saving file: {e}")

    def handle_chat_mode(self) -> None:
        """Handles conversational chat mode (placeholder) """
        self.cli.print_info("Chat mode is not yet implemented. Please use other commands.")

    def show_main_menu(self) -> None:
        """Show main menu and handle user choices"""
        self.cli.print_welcome()
        while True:
            choice = self.cli.show_main_menu()

            if choice == "1": # Generate Code
                description = self.cli.get_user_input("Describe the code you want to generate:")
                if description:
                    language = self.cli.get_user_input("Target language (js/ts)", default="ts")
                    minimal = self.cli.confirm_action("Generate minimal code?")
                    self.handle_generate_code(description, language, minimal, None)
            elif choice == "2": # Explain Code
                code_snippet = self.cli.get_user_input("Paste your code snippet to explain:")
                if code_snippet:
                    language = self.cli.get_user_input("Code language (js/ts)", default="ts")
                    self.handle_explain_code(code_snippet, language, None)
            elif choice == "3": # Refactor Code
                code_snippet = self.cli.get_user_input("Paste your code snippet to refactor:")
                if code_snippet:
                    language = self.cli.get_user_input("Code language (js/ts)", default="ts")
                    minimal = self.cli.confirm_action("Generate minimal refactoring?")
                    self.handle_refactor_code(code_snippet, language, minimal, None)
            elif choice == "4": # Convert JS <-> TS
                code_snippet = self.cli.get_user_input("Paste your code snippet to convert:")
                if code_snippet:
                    target_language = self.cli.get_user_input("Target language (js/ts)", default="ts")
                    self.handle_convert_code(code_snippet, target_language, None)
            elif choice == "5": # Debug Code
                code_snippet = self.cli.get_user_input("Paste your code snippet to debug:")
                if code_snippet:
                    error_message = self.cli.get_user_input("Optional: Paste any error message received:", default="")
                    language = self.cli.get_user_input("Code language (js/ts)", default="ts")
                    self.handle_debug_code(code_snippet, error_message if error_message else None, language, None)
            elif choice == "6": # Save Output
                if self.last_output_code:
                    filename = self.cli.get_user_input(f"Enter filename to save (e.g., output.{self.last_output_lang}):", default=f"output.{self.last_output_lang}")
                    is_code_content = self.last_output_lang != "md" # Simple heuristic
                    self.save_code_to_file(self.last_output_code, filename, self.last_output_lang, is_code=is_code_content)
                else:
                    self.cli.print_warning("No output to save. Generate, explain, refactor, convert, or debug code first.")
            elif choice == "7": # Help
                self.cli.print_help()
            elif choice in ["0", "exit", "quit", "q"]:
                self.cli.print_info("Goodbye! 👋")
                break
            elif choice:
                # Attempt to parse direct commands from menu input
                self.parse_and_process_direct_command(choice)

    def parse_and_process_direct_command(self, command_str: str) -> None:
        """Parses a command string from direct input and processes it."""
        import re
        parser = self._create_arg_parser()
        try:
            # Split the command string, handling quoted arguments
            import shlex
            args_list = shlex.split(command_str)
            args = parser.parse_args(args_list)

            # Re-use existing handlers
            if args.generate:
                self.handle_generate_code(args.generate, args.lang, args.minimal, args.save)
            elif args.explain:
                self.handle_explain_code(args.explain, args.lang, args.save)
            elif args.refactor:
                self.handle_refactor_code(args.refactor, args.lang, args.minimal, args.save)
            elif args.convert and args.to:
                self.handle_convert_code(args.convert, args.to, args.save)
            elif args.debug:
                self.handle_debug_code(args.debug, args.error, args.lang, args.save)
            else:
                self.cli.print_error("Invalid command. Use --help for usage.")
        except SystemExit: # argparse exits on error or --help
            self.cli.print_error("Invalid command syntax or argument. Use --help for usage.")
        except Exception as e:
            self.cli.print_error(f"Error processing command: {e}")

    def interactive_mode(self) -> None:
        """Run in interactive mode (future expansion for quick actions) """
        self.cli.print_info("Interactive mode is under development. Please use the main menu for now.")
        self.show_main_menu()

    def _create_arg_parser(self):
        """Creates and returns the argument parser."""
        parser = argparse.ArgumentParser(description="TSHelperBot - AI-powered JavaScript/TypeScript assistant")
        parser.add_argument('--generate', type=str, help='Describe the code to generate (e.g., "function to validate email")')
        parser.add_argument('--explain', type=str, help='Provide code snippet to explain (e.g., "const x = 5;")')
        parser.add_argument('--refactor', type=str, help='Provide code snippet to refactor (e.g., "function add(a,b){return a+b}")')
        parser.add_argument('--convert', type=str, help='Provide code snippet to convert (e.g., "let x = 5;")')
        parser.add_argument('--to', type=str, choices=['js', 'ts'], help='Target language for conversion (js or ts)')
        parser.add_argument('--debug', type=str, help='Provide code snippet to debug (e.g., "function sum(a, b) { return a  b; }")')
        parser.add_argument('--error', type=str, help='Optional: provide an error message for debugging (e.g., "ReferenceError: c is not defined")')
        parser.add_argument('--lang', type=str, choices=['js', 'ts'], default=self.config.get_env_variable("DEFAULT_LANG", "ts"),
                            help='Specify output language for generation/refactoring (js or ts). Default from .env or ts.')
        parser.add_argument('--save', type=str, help='Save the output to a specified .js or .ts file')
        parser.add_argument('--minimal', action='store_true', help='Generate minimal code/markup.')
        parser.add_argument('--menu', '-m', action='store_true', help='Show main menu (default if no other args)')
        parser.add_argument('--interactive', '-i', action='store_true', help='Run in interactive mode (future quick actions)')
        parser.add_argument('--chat', '-c', action='store_true', help='Enter chatbot conversation mode (future)')
        return parser

def main():
    """Main entry point"""
    bot = TSHelperBot()
    parser = bot._create_arg_parser() # Get the parser from the bot instance
    args = parser.parse_args()

    if len(sys.argv) == 1 or args.menu: # If no arguments or --menu is passed
        bot.show_main_menu()
    else:
        bot.process_input(args)

if __name__ == "__main__":
    import re # Import re for extract_raw_code
    main()
