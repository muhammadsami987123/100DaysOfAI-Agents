#!/usr/bin/env python3
"""
🤖 AI Quiz Maker - Day 33 of #100DaysOfAI-Agents

A powerful AI-powered quiz generator that creates engaging quizzes from topics, 
articles, or text files using OpenAI's GPT models.

Features:
- AI-powered quiz generation with OpenAI GPT
- Multiple question types (MCQs with 4 options)
- Difficulty levels (Easy, Medium, Hard)
- Customizable question count
- Multiple export formats (Markdown, JSON, CSV)
- Command Line Interface (CLI) and Web UI
- Interactive mode for easy use

Author: Muhammad Sami Asghar Mughal
"""

import argparse
import os
import sys
import json
from typing import Optional
from colorama import init, Fore, Back, Style
from config import get_api_key, setup_instructions, DEFAULT_QUESTIONS, DEFAULT_DIFFICULTY, DEFAULT_FORMAT, SUPPORTED_FORMATS, SUPPORTED_DIFFICULTIES
from quiz_generator import QuizGenerator

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class QuizMakerCLI:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the QuizMakerCLI."""
        self.api_key = api_key or get_api_key()
        if not self.api_key:
            print(f"{Fore.RED}❌ Error: OpenAI API key not found!")
            print()
            setup_instructions()
            sys.exit(1)
        
        # Initialize default settings
        self.default_questions = DEFAULT_QUESTIONS
        self.default_difficulty = DEFAULT_DIFFICULTY
        
        try:
            self.generator = QuizGenerator(self.api_key)
            print(f"{Fore.GREEN}✅ Quiz Generator initialized successfully!")
        except Exception as e:
            print(f"{Fore.RED}❌ Failed to initialize Quiz Generator: {e}")
            sys.exit(1)
    
    def generate_quiz_from_topic(self, topic: str, num_questions: int, difficulty: str, 
                                include_answers: bool = True, output_format: str = "md") -> bool:
        """Generate quiz from a topic."""
        try:
            print(f"{Fore.CYAN}🎯 Generating quiz for topic: {topic}")
            print(f"{Fore.WHITE}   Questions: {num_questions}")
            print(f"{Fore.WHITE}   Difficulty: {difficulty}")
            print(f"{Fore.WHITE}   Format: {output_format}")
            print(f"{Fore.WHITE}   Include answers: {'Yes' if include_answers else 'No'}")
            print("-" * 60)
            
            quiz_data = self.generator.generate_quiz(
                content=topic,
                num_questions=num_questions,
                difficulty=difficulty,
                include_answers=include_answers
            )
            
            # Display the quiz
            self.display_quiz(quiz_data, output_format)
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ Failed to generate quiz: {e}")
            return False
    
    def generate_quiz_from_file(self, filepath: str, num_questions: int, difficulty: str,
                               include_answers: bool = True, output_format: str = "md") -> bool:
        """Generate quiz from a text file."""
        try:
            if not os.path.exists(filepath):
                print(f"{Fore.RED}❌ File not found: {filepath}")
                return False
            
            print(f"{Fore.CYAN}📁 Generating quiz from file: {filepath}")
            print(f"{Fore.WHITE}   Questions: {num_questions}")
            print(f"{Fore.WHITE}   Difficulty: {difficulty}")
            print(f"{Fore.WHITE}   Format: {output_format}")
            print("-" * 60)
            
            quiz_data = self.generator.generate_quiz_from_file(
                filepath=filepath,
                num_questions=num_questions,
                difficulty=difficulty,
                include_answers=include_answers
            )
            
            # Display the quiz
            self.display_quiz(quiz_data, output_format)
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ Failed to generate quiz from file: {e}")
            return False
    
    def generate_quiz_from_text(self, text: str, num_questions: int, difficulty: str,
                               include_answers: bool = True, output_format: str = "md") -> bool:
        """Generate quiz from pasted text."""
        try:
            print(f"{Fore.CYAN}📝 Generating quiz from text content")
            print(f"{Fore.WHITE}   Content length: {len(text)} characters")
            print(f"{Fore.WHITE}   Questions: {num_questions}")
            print(f"{Fore.WHITE}   Difficulty: {difficulty}")
            print(f"{Fore.WHITE}   Format: {output_format}")
            print("-" * 60)
            
            quiz_data = self.generator.generate_quiz(
                content=text,
                num_questions=num_questions,
                difficulty=difficulty,
                include_answers=include_answers
            )
            
            # Display the quiz
            self.display_quiz(quiz_data, output_format)
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ Failed to generate quiz from text: {e}")
            return False
    
    def display_quiz(self, quiz_data: dict, output_format: str = "md"):
        """Display the generated quiz."""
        print(f"{Fore.GREEN}✅ Quiz generated successfully!")
        print(f"{Fore.CYAN}📊 Quiz Statistics:")
        print(f"{Fore.WHITE}   Topic: {quiz_data['topic']}")
        print(f"{Fore.WHITE}   Questions: {quiz_data['questions']}")
        print(f"{Fore.WHITE}   Difficulty: {quiz_data['difficulty']}")
        print(f"{Fore.WHITE}   Model: {quiz_data['model']}")
        print(f"{Fore.WHITE}   Generated: {quiz_data['generated_at']}")
        print()
        
        # Show quiz preview
        print(f"{Fore.YELLOW}📋 Quiz Preview:")
        print("-" * 60)
        
        for i, question in enumerate(quiz_data['quiz'], 1):
            print(f"{Fore.CYAN}{i}. {question['question']}")
            
            for option, text in question['options'].items():
                print(f"   {Fore.WHITE}{option}) {text}")
            
            if quiz_data.get('include_answers', True):
                print(f"   {Fore.GREEN}Answer: {question['answer']}")
            
            print()
        
        # Export options
        self.handle_export(quiz_data, output_format)
    
    def handle_export(self, quiz_data: dict, output_format: str):
        """Handle quiz export in various formats."""
        print(f"{Fore.YELLOW}📤 Export Options:")
        print("-" * 60)
        
        try:
            # Export in the specified format
            exported_content = self.generator.export_quiz(quiz_data, output_format)
            
            # Save to file
            filename = f"quiz_{quiz_data['topic'].replace(' ', '_').lower()}_{output_format}"
            filepath = self.generator.save_quiz(quiz_data, filename, output_format)
            
            print(f"{Fore.GREEN}✅ Quiz saved to: {filepath}")
            
            # Copy to clipboard if possible
            try:
                import pyperclip
                pyperclip.copy(exported_content)
                print(f"{Fore.GREEN}✅ Quiz copied to clipboard!")
            except ImportError:
                print(f"{Fore.YELLOW}💡 Install pyperclip to enable clipboard copying: pip install pyperclip")
            
            # Show export options
            print(f"\n{Fore.CYAN}🔄 Export in other formats:")
            for fmt in SUPPORTED_FORMATS:
                if fmt != output_format:
                    print(f"   {Fore.WHITE}• {fmt.upper()}: python main.py --export {fmt} --file {filepath}")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Export failed: {e}")
    
    def run_interactive(self):
        """Run the interactive CLI interface."""
        print(f"{Fore.CYAN}🎯 Welcome to AI Quiz Maker!")
        print(f"{Fore.WHITE}I can help you create engaging quizzes using AI.")
        print(f"{Fore.YELLOW}Type 'help' for commands, 'quit' to exit.")
        print("-" * 60)
        
        while True:
            try:
                command = input(f"{Fore.GREEN}🎓 QuizMaker> ").strip()
                
                if not command:
                    continue
                
                if command.lower() in ['quit', 'exit', 'q']:
                    print(f"{Fore.CYAN}👋 Goodbye! Happy quiz making!")
                    break
                
                elif command.lower() == 'help':
                    self.show_help()
                
                elif command.lower() == 'stats':
                    self.show_statistics()
                
                elif command.lower().startswith('topic:'):
                    topic = command[6:].strip()
                    if topic:
                        self.generate_quiz_from_topic(topic, self.default_questions, self.default_difficulty)
                    else:
                        print(f"{Fore.RED}❌ Please provide a topic after 'topic:'")
                
                elif command.lower().startswith('file:'):
                    filepath = command[5:].strip()
                    if filepath:
                        self.generate_quiz_from_file(filepath, self.default_questions, self.default_difficulty)
                    else:
                        print(f"{Fore.RED}❌ Please provide a file path after 'file:'")
                
                elif command.lower().startswith('text:'):
                    text = command[5:].strip()
                    if text:
                        self.generate_quiz_from_text(text, self.default_questions, self.default_difficulty)
                    else:
                        print(f"{Fore.RED}❌ Please provide text content after 'text:'")
                
                elif command.lower().startswith('questions:'):
                    try:
                        num = int(command[9:].strip())
                        if 1 <= num <= 50:
                            self.default_questions = num
                            print(f"{Fore.GREEN}✅ Default questions set to: {num}")
                        else:
                            print(f"{Fore.RED}❌ Please specify a number between 1 and 50")
                    except ValueError:
                        print(f"{Fore.RED}❌ Please specify a valid number")
                
                elif command.lower().startswith('difficulty:'):
                    diff = command[11:].strip().lower()
                    if diff in SUPPORTED_DIFFICULTIES:
                        self.default_difficulty = diff
                        print(f"{Fore.GREEN}✅ Default difficulty set to: {diff}")
                    else:
                        print(f"{Fore.RED}❌ Supported difficulties: {', '.join(SUPPORTED_DIFFICULTIES)}")
                
                else:
                    # Try to interpret as a topic
                    print(f"{Fore.CYAN}🎯 Generating quiz for topic: {command}")
                    self.generate_quiz_from_topic(command, self.default_questions, self.default_difficulty)
                    
            except KeyboardInterrupt:
                print(f"\n{Fore.CYAN}👋 Goodbye! Happy quiz making!")
                break
            except Exception as e:
                print(f"{Fore.RED}❌ Unexpected error: {e}")
    
    def show_help(self):
        """Show help information."""
        print(f"{Fore.CYAN}📖 AI Quiz Maker Help:")
        print(f"{Fore.WHITE}Commands:")
        print(f"  {Fore.GREEN}• topic: [topic name] - Generate quiz from topic")
        print(f"  {Fore.GREEN}• file: [filepath] - Generate quiz from text file")
        print(f"  {Fore.GREEN}• text: [content] - Generate quiz from pasted text")
        print(f"  {Fore.GREEN}• questions: [number] - Set default question count")
        print(f"  {Fore.GREEN}• difficulty: [easy/medium/hard] - Set default difficulty")
        print(f"  {Fore.GREEN}• stats - Show statistics")
        print(f"  {Fore.GREEN}• help - Show this help")
        print(f"  {Fore.GREEN}• quit - Exit the program")
        print()
        print(f"{Fore.WHITE}Examples:")
        print(f"  {Fore.YELLOW}• Python programming")
        print(f"  {Fore.YELLOW}• topic: Machine Learning")
        print(f"  {Fore.YELLOW}• file: notes.txt")
        print(f"  {Fore.YELLOW}• text: Your content here...")
        print(f"  {Fore.YELLOW}• questions: 10")
        print(f"  {Fore.YELLOW}• difficulty: hard")
        print()
        print(f"{Fore.WHITE}Features:")
        print(f"  {Fore.MAGENTA}• AI-powered quiz generation")
        print(f"  {Fore.MAGENTA}• Multiple choice questions (A-D)")
        print(f"  {Fore.MAGENTA}• Difficulty levels: easy, medium, hard")
        print(f"  {Fore.MAGENTA}• Export formats: Markdown, JSON, CSV")
        print(f"  {Fore.MAGENTA}• Automatic answer key generation")
    
    def show_statistics(self):
        """Show application statistics."""
        print(f"{Fore.CYAN}📊 AI Quiz Maker Statistics:")
        print(f"{Fore.WHITE}   OpenAI Model: {self.generator.model}")
        print(f"{Fore.WHITE}   Default Questions: {self.default_questions}")
        print(f"{Fore.WHITE}   Default Difficulty: {self.default_difficulty}")
        print(f"{Fore.WHITE}   Supported Formats: {', '.join(SUPPORTED_FORMATS)}")
        print(f"{Fore.WHITE}   Supported Difficulties: {', '.join(SUPPORTED_DIFFICULTIES)}")
        print(f"{Fore.WHITE}   API Key: {'✅ Set' if self.api_key else '❌ Not set'}")


def main():
    """Main function to run the AI Quiz Maker CLI."""
    parser = argparse.ArgumentParser(
        description="AI Quiz Maker - Generate engaging quizzes using OpenAI GPT",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --topic "Python Programming" --questions 10 --difficulty medium
  python main.py --file "article.txt" --questions 5 --difficulty easy
  python main.py --text "Your content here..." --questions 8 --difficulty hard
  python main.py --interactive
        """
    )
    
    # Input options (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=False)
    input_group.add_argument('--topic', type=str, help='Generate quiz from a topic')
    input_group.add_argument('--file', type=str, help='Generate quiz from a text file')
    input_group.add_argument('--text', type=str, help='Generate quiz from pasted text')
    input_group.add_argument('--interactive', action='store_true', help='Run in interactive mode')
    
    # Quiz configuration
    parser.add_argument('--questions', type=int, default=DEFAULT_QUESTIONS,
                       help=f'Number of questions (default: {DEFAULT_QUESTIONS})')
    parser.add_argument('--difficulty', choices=SUPPORTED_DIFFICULTIES, default=DEFAULT_DIFFICULTY,
                       help=f'Difficulty level (default: {DEFAULT_DIFFICULTY})')
    parser.add_argument('--format', choices=SUPPORTED_FORMATS, default=DEFAULT_FORMAT,
                       help=f'Output format (default: {DEFAULT_FORMAT})')
    parser.add_argument('--no-answers', action='store_true', help='Exclude answer key')
    
    # Output options
    parser.add_argument('--output', type=str, help='Output file path')
    parser.add_argument('--api-key', type=str, help='OpenAI API key')
    
    # Other options
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    # If no arguments provided, run interactive mode
    if len(sys.argv) == 1:
        args.interactive = True
    
    try:
        # Initialize the CLI
        cli = QuizMakerCLI(api_key=args.api_key)
        
        if args.interactive:
            cli.run_interactive()
        elif args.topic:
            success = cli.generate_quiz_from_topic(
                topic=args.topic,
                num_questions=args.questions,
                difficulty=args.difficulty,
                include_answers=not args.no_answers,
                output_format=args.format
            )
            if not success:
                sys.exit(1)
        elif args.file:
            success = cli.generate_quiz_from_file(
                filepath=args.file,
                num_questions=args.questions,
                difficulty=args.difficulty,
                include_answers=not args.no_answers,
                output_format=args.format
            )
            if not success:
                sys.exit(1)
        elif args.text:
            success = cli.generate_quiz_from_text(
                text=args.text,
                num_questions=args.questions,
                difficulty=args.difficulty,
                include_answers=not args.no_answers,
                output_format=args.format
            )
            if not success:
                sys.exit(1)
        else:
            parser.print_help()
            sys.exit(1)
            
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}👋 Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}❌ Fatal error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
