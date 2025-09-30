
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

from config.gemini_config import GeminiConfig
from core.parser import ResumeParser
from core.extractor import ResumeExtractor
from utils.cli_interface import CLIInterface

class ResumeParserAgent:
    """Main Resume Parser Agent class"""

    def __init__(self):
        self.console = Console()
        self.config = GeminiConfig()
        self.cli = CLIInterface()
        self.parser = ResumeParser()
        self.extractor = ResumeExtractor(self.config)
        self.last_parsed_data: Optional[Dict[str, Any]] = None
        self.resume_text = ""

    def validate_fields(self, parsed_data: Dict[str, Any]) -> str:
        missing_fields = []
        key_fields = ["full_name", "email", "phone_number"]
        for field in key_fields:
            if not parsed_data.get(field):
                missing_fields.append(field)
        if missing_fields:
            return f"Missing key fields: {', '.join(missing_fields)}"
        else:
            return "All key fields are present."

    def save_json_output(self, data: Dict[str, Any], filename: str = "resume_parsed.json") -> None:
        if data:
            if self.cli.confirm_action(f"Do you want to save the parsed data to {filename}?"):
                try:
                    with open(filename, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=4)
                    self.cli.print_success(f"Parsed data saved to [green]{filename}[/green]")
                except Exception as e:
                    self.cli.print_error(f"Error saving file: {e}")
            else:
                self.cli.print_info("Save cancelled.")
        else:
            self.cli.print_info("No data to save.")

    def run(self) -> None:
        self.cli.print_welcome()
        
        # Use parse_known_args to separate recognized args from the input source (file/text)
        parser = argparse.ArgumentParser(description="ResumeParserAgent - CLI-based AI HR Assistant")
        parser.add_argument("--summary", action="store_true", help="Summarize the resume in 3-5 lines.")
        parser.add_argument("--skills-only", action="store_true", help="Extract only technical and soft skills.")
        parser.add_argument("--json", action="store_true", help="Save parsed output as resume_parsed.json.")
        parser.add_argument("--validate", action="store_true", help="Check if key fields are missing.")
        
        args, unknown_args = parser.parse_known_args()

        user_input_source = ""
        # If there are unknown args, assume they are part of the input source command (e.g., "file path" or "text content")
        if unknown_args:
            # Join the unknown arguments back to form the potential input command string
            user_input_source = " ".join(unknown_args).strip()
        
        # If no input source was provided via command line, prompt the user interactively
        if not user_input_source:
            user_input_source = self.cli.get_user_input(
                "Please upload a resume file to begin parsing, or paste the resume text directly. \nEnter 'file <path_to_file>' or 'text <your_resume_text>'",
                default=""
            )

        if user_input_source.lower() in ["exit", "quit", "q"]:
            self.cli.print_info("Goodbye! 👋")
            return

        if user_input_source.startswith("file "):
            file_path = user_input_source.split(" ", 1)[1]
            self.resume_text = self.parser.read_file(file_path)
            if not self.resume_text:
                self.cli.print_error(f"Could not read file or file is empty: {file_path}")
                return
            self.cli.print_info(f"Successfully read file: {file_path}")
        elif user_input_source.startswith("text "):
            self.resume_text = user_input_source.split(" ", 1)[1]
            if not self.resume_text:
                self.cli.print_error("No resume text provided.")
                return
            self.cli.print_info("Using provided resume text.")
        else:
            self.cli.print_error("Invalid input. Please start with 'file <path_to_file>' or 'text <your_resume_text>'.")
            return

        if args.summary:
            with self.console.status("[bold blue]Generating resume summary...[/bold blue]", spinner="dots") as status:
                summary = self.extractor.summarize_resume(self.resume_text)
                status.update("[bold green]Summary Generated![/bold green]")
            self.cli.print_markdown(summary, title="Resume Summary")
        elif args.skills_only:
            with self.console.status("[bold blue]Extracting skills...[/bold blue]", spinner="dots") as status:
                skills = self.extractor.extract_skills_only(self.resume_text)
                status.update("[bold green]Skills Extraction Complete![/bold green]")
            if skills:
                self.cli.print_json_output({"skills": skills}, title="Extracted Skills")
            else:
                self.cli.print_warning("No skills extracted or an error occurred.")
        else:
            with self.console.status("[bold blue]Parsing resume...[/bold blue]", spinner="dots") as status:
                self.last_parsed_data = self.extractor.parse_resume(self.resume_text)
                status.update("[bold green]Resume Parsing Complete![/bold green]")

            if self.last_parsed_data and "error" not in self.last_parsed_data:
                self.cli.print_json_output(self.last_parsed_data, title="Parsed Resume Data")

                if args.json:
                    self.save_json_output(self.last_parsed_data)
                if args.validate:
                    validation_result = self.validate_fields(self.last_parsed_data)
                    self.cli.print_info(validation_result)
            else:
                self.cli.print_error(f"Failed to parse resume: {self.last_parsed_data.get('error', 'Unknown error')}")
                if "raw_response" in self.last_parsed_data:
                    self.cli.print_markdown(self.last_parsed_data["raw_response"], title="Raw AI Response")


def main():
    agent = ResumeParserAgent()
    agent.run()

if __name__ == "__main__":
    main()
