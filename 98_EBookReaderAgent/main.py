"""
Main entry point for EBookReaderAgent
CLI-first design with optional UI interfaces
"""

import sys
import argparse
import json
from pathlib import Path
from agent import EBookReaderAgent
from utils.llm_service import LLMService


def print_book_info(book_info: dict):
    """Print book information in a formatted way"""
    if not book_info.get('success'):
        print(f"❌ Error: {book_info.get('error', 'Unknown error')}")
        return
    
    metadata = book_info['metadata']
    chapters = book_info['chapters']
    
    print("\n" + "=" * 60)
    print("📚 BOOK INFORMATION")
    print("=" * 60)
    print(f"Title:       {metadata['title']}")
    print(f"Author:      {metadata['author']}")
    print(f"Pages:       {metadata['total_pages']}")
    print(f"Chapters:    {metadata['total_chapters']}")
    print(f"Word Count:  {metadata['word_count']:,}")
    print(f"Reading Time: {metadata['estimated_reading_time']['formatted']}")
    print(f"File Type:   {metadata['file_type'].upper()}")
    print("\n📑 Chapters:")
    for ch in chapters:
        print(f"  {ch['number']}. {ch['title']} ({ch['word_count']:,} words)")
    print("=" * 60 + "\n")


def print_summary(summary: dict):
    """Print chapter summary"""
    if not summary.get('success'):
        print(f"❌ Error: {summary.get('error', 'Unknown error')}")
        return
    
    print("\n" + "=" * 60)
    print(f"📝 CHAPTER {summary['chapter_number']}: {summary['chapter_title']}")
    print("=" * 60)
    print(summary['summary'])
    print("=" * 60 + "\n")


def print_takeaways(takeaways: dict):
    """Print key takeaways"""
    if not takeaways.get('success'):
        print(f"❌ Error: {takeaways.get('error', 'Unknown error')}")
        return
    
    print("\n" + "=" * 60)
    print("💡 KEY TAKEAWAYS")
    print("=" * 60)
    
    if takeaways.get('takeaways') and len(takeaways['takeaways']) > 0:
        for i, takeaway in enumerate(takeaways['takeaways'], 1):
            print(f"\n{i}. {takeaway}")
    else:
        print(takeaways.get('formatted_text', 'No takeaways available'))
    
    print("=" * 60 + "\n")


def print_quotes(quotes: dict):
    """Print important quotes"""
    if not quotes.get('success'):
        print(f"❌ Error: {quotes.get('error', 'Unknown error')}")
        return
    
    print("\n" + "=" * 60)
    print("💬 IMPORTANT QUOTES")
    print("=" * 60)
    
    if quotes.get('quotes') and len(quotes['quotes']) > 0:
        for i, quote in enumerate(quotes['quotes'], 1):
            print(f"\n{i}. \"{quote['quote']}\"")
            if quote.get('context'):
                print(f"   Context: {quote['context']}")
    else:
        print(quotes.get('formatted_text', 'No quotes available'))
    
    print("=" * 60 + "\n")


def print_answer(answer: dict):
    """Print Q&A answer"""
    if not answer.get('success'):
        print(f"❌ Error: {answer.get('error', 'Unknown error')}")
        return
    
    print("\n" + "=" * 60)
    print("❓ QUESTION & ANSWER")
    print("=" * 60)
    print(f"Question: {answer['question']}")
    if answer.get('chapter_context'):
        print(f"Context: {answer['chapter_context']}")
    print("\nAnswer:")
    print(answer['answer'])
    print("=" * 60 + "\n")


def save_output(data: dict, output_file: str, format: str = 'json'):
    """Save output to file"""
    output_path = Path(output_file)
    
    if format == 'json':
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    elif format == 'txt':
        with open(output_path, 'w', encoding='utf-8') as f:
            if 'summary' in data:
                f.write(f"Chapter {data.get('chapter_number', 'N/A')}: {data.get('chapter_title', 'N/A')}\n")
                f.write("=" * 60 + "\n")
                f.write(data.get('summary', ''))
            elif 'takeaways' in data:
                f.write("Key Takeaways\n")
                f.write("=" * 60 + "\n")
                for i, takeaway in enumerate(data.get('takeaways', []), 1):
                    f.write(f"{i}. {takeaway}\n")
            elif 'quotes' in data:
                f.write("Important Quotes\n")
                f.write("=" * 60 + "\n")
                for i, quote in enumerate(data.get('quotes', []), 1):
                    f.write(f"{i}. \"{quote.get('quote', '')}\"\n")
    
    print(f"✅ Output saved to: {output_path}")


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="EBookReaderAgent - AI-Powered eBook Reader and Analyzer (CLI-first)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage - analyze a book (local file)
  python main.py book.pdf --analyze
  
  # Analyze book from URL
  python main.py https://example.com/book.pdf --analyze
  
  # Get key takeaways
  python main.py book.pdf --takeaways
  
  # Summarize a specific chapter
  python main.py book.pdf --chapter 1
  
  # Ask a question
  python main.py book.pdf --question "What is the main theme?"
  
  # Get quotes and save to file
  python main.py book.pdf --quotes --output quotes.json
  
  # Start Streamlit UI
  python main.py --streamlit
  
  # Start FastAPI web interface
  python main.py --web
        """,
        add_help=True
    )
    
    # File input
    parser.add_argument(
        'file',
        nargs='?',
        help='Path to PDF/ePub file or public URL to download book'
    )
    
    # Actions
    parser.add_argument(
        '--info',
        action='store_true',
        help='Show book information'
    )
    
    parser.add_argument(
        '--analyze',
        action='store_true',
        help='Perform full book analysis (summaries + takeaways + quotes)'
    )
    
    parser.add_argument(
        '--summarize',
        action='store_true',
        help='Summarize all chapters'
    )
    
    parser.add_argument(
        '--chapter',
        type=int,
        metavar='N',
        help='Summarize a specific chapter number'
    )
    
    parser.add_argument(
        '--takeaways',
        action='store_true',
        help='Extract key takeaways'
    )
    
    parser.add_argument(
        '--quotes',
        action='store_true',
        help='Extract important quotes'
    )
    
    parser.add_argument(
        '--question',
        type=str,
        metavar='Q',
        help='Ask a question about the book'
    )
    
    parser.add_argument(
        '--question-chapter',
        type=int,
        metavar='N',
        help='Chapter number for question context (optional)'
    )
    
    # Output options
    parser.add_argument(
        '--output',
        '-o',
        type=str,
        metavar='FILE',
        help='Save output to file (JSON or TXT based on extension)'
    )
    
    parser.add_argument(
        '--num-takeaways',
        type=int,
        default=10,
        help='Number of takeaways to extract (default: 10)'
    )
    
    parser.add_argument(
        '--num-quotes',
        type=int,
        default=5,
        help='Number of quotes to extract (default: 5)'
    )
    
    # UI options
    parser.add_argument(
        '--streamlit',
        action='store_true',
        help='Start Streamlit UI'
    )
    
    parser.add_argument(
        '--web',
        action='store_true',
        help='Start FastAPI web interface'
    )
    
    # LLM selection
    parser.add_argument(
        '--llm',
        choices=['gemini', 'openai'],
        default='gemini',
        help='LLM to use (default: gemini)'
    )
    
    args = parser.parse_args()
    
    # Handle legacy commands: "web" or "streamlit" without -- flag
    if args.file in ['web', 'streamlit']:
        if args.file == 'web':
            print("💡 Tip: Use --web flag instead: python main.py --web")
            args.web = True
            args.file = None
        elif args.file == 'streamlit':
            print("💡 Tip: Use --streamlit flag instead: python main.py --streamlit")
            args.streamlit = True
            args.file = None
    
    # Handle UI modes
    if args.streamlit:
        print("🚀 Starting Streamlit UI...")
        print("Opening browser at http://localhost:8501")
        try:
            import streamlit.web.cli as stcli
            import sys as sys_module
            sys_module.argv = ["streamlit", "run", "streamlit_app.py"]
            stcli.main()
        except ImportError:
            print("❌ Streamlit not installed. Install with: pip install streamlit")
            sys.exit(1)
        return
    
    if args.web:
        print("🚀 Starting FastAPI web interface...")
        print("Navigate to: http://localhost:8000")
        try:
            import uvicorn
            from web_app import app
            uvicorn.run(app, host="0.0.0.0", port=8000)
        except ImportError:
            print("❌ FastAPI/uvicorn not installed. Install with: pip install fastapi uvicorn")
            sys.exit(1)
        return
    
    # CLI mode - require file or URL
    if not args.file:
        parser.print_help()
        print("\n❌ Error: Please provide a book file/URL or use --streamlit/--web for UI")
        print("\n💡 Tip: Use --web or --streamlit flag, e.g., python main.py --web")
        sys.exit(1)
    
    # Check if it's a URL or file path
    is_url = args.file.startswith(('http://', 'https://'))
    
    if not is_url:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"❌ Error: File not found: {file_path}")
            sys.exit(1)
        book_source = file_path.name
    else:
        book_source = args.file
    
    # Initialize agent
    print("📚 EBookReaderAgent - AI-Powered eBook Reader")
    print("=" * 60)
    if is_url:
        print(f"Loading book from URL: {args.file}")
    else:
        print(f"Loading book: {book_source}")
    
    llm_service = LLMService()
    llm_service.set_llm(args.llm)
    agent = EBookReaderAgent(llm_service=llm_service)
    
    # Load book (handles both file paths and URLs)
    result = agent.load_book(args.file)
    if not result['success']:
        print(f"❌ Error loading book: {result.get('error', 'Unknown error')}")
        sys.exit(1)
    
    print(f"✅ Book loaded successfully: {result['message']}")
    
    # Execute actions
    output_data = {}
    
    if args.info or not any([args.analyze, args.summarize, args.chapter, args.takeaways, args.quotes, args.question]):
        book_info = agent.get_book_info()
        print_book_info(book_info)
        output_data['book_info'] = book_info
    
    if args.analyze or args.summarize:
        print("📝 Generating summaries for all chapters...")
        summaries = agent.summarize_all_chapters()
        if summaries['success']:
            for summary in summaries['summaries']:
                print_summary(summary)
            output_data['summaries'] = summaries
    
    if args.chapter:
        print(f"📝 Generating summary for chapter {args.chapter}...")
        summary = agent.summarize_chapter(args.chapter)
        print_summary(summary)
        output_data['summary'] = summary
    
    if args.analyze or args.takeaways:
        print("💡 Extracting key takeaways...")
        takeaways = agent.get_key_takeaways(args.num_takeaways)
        print_takeaways(takeaways)
        output_data['takeaways'] = takeaways
    
    if args.analyze or args.quotes:
        print("💬 Extracting important quotes...")
        quotes = agent.get_important_quotes(num_quotes=args.num_quotes)
        print_quotes(quotes)
        output_data['quotes'] = quotes
    
    if args.question:
        print(f"❓ Answering question: {args.question}")
        answer = agent.ask_question(args.question, args.question_chapter)
        print_answer(answer)
        output_data['answer'] = answer
    
    # Save output if requested
    if args.output:
        output_format = 'json' if args.output.endswith('.json') else 'txt'
        if 'summary' in output_data:
            save_output(output_data['summary'], args.output, output_format)
        elif 'takeaways' in output_data:
            save_output(output_data['takeaways'], args.output, output_format)
        elif 'quotes' in output_data:
            save_output(output_data['quotes'], args.output, output_format)
        else:
            save_output(output_data, args.output, 'json')


if __name__ == "__main__":
    main()
