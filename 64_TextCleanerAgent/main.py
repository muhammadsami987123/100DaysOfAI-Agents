import os
import requests
from bs4 import BeautifulSoup
from docx import Document
from .text_cleaner_agent import TextCleanerAgent
from dotenv import load_dotenv

load_dotenv()

def run_cli():
    import argparse
    # The TextCleanerAgent import is already handled by the package-level import
    # from .text_cleaner_agent import TextCleanerAgent # Removed this line as it's redundant/problematic for direct execution
    parser = argparse.ArgumentParser(description="TextCleanerAgent - Smart Text Polisher Using Gemini API")
    parser.add_argument("--text", type=str, help="Text to clean.")
    parser.add_argument("--file", type=str, help="Path to .txt or .docx file to clean.")
    parser.add_argument("--url", type=str, help="URL to fetch content from and clean.")
    parser.add_argument("--summarize", action="store_true", help="Summarize the cleaned text.")
    parser.add_argument("--diff", action="store_true", help="Show original and cleaned versions.")
    parser.add_argument("--api_key", type=str, default=os.getenv("GEMINI_API_KEY"),
                        help="Your Gemini API key. Defaults to GEMINI_API_KEY environment variable.")

    args = parser.parse_args()

    api_key = args.api_key
    if not api_key:
        print("Error: Gemini API key not provided. Please set GEMINI_API_KEY environment variable or use --api_key argument.")
        return

    agent = TextCleanerAgent(api_key=api_key)

    input_content = ""
    if args.text:
        input_content = args.text
    elif args.file:
        if args.file.endswith(".docx"):
            input_content = agent._read_docx(args.file)
        elif args.file.endswith(".txt"):
            input_content = agent._read_txt(args.file)
        else:
            print("Error: Unsupported file type. Only .txt and .docx are supported.")
            return
    elif args.url:
        input_content = agent._fetch_url_content(args.url)
    else:
        print("Error: No input provided. Please use --text, --file, or --url.")
        return

    if not input_content:
        print("No content to clean.")
        return

    cleaned_output = agent.clean_text(input_content, summarize=args.summarize, provide_diff=args.diff)
    print(cleaned_output)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="TextCleanerAgent - Smart Text Polisher Using Gemini API")
    parser.add_argument("--mode", type=str, default="cli", choices=["cli", "web"], help="Run in CLI or Web mode.")
    args = parser.parse_args()

    if args.mode == "web":
        from .web_app import app
        app.run(debug=True)
    else:
        run_cli()

if __name__ == "__main__":
    main()
