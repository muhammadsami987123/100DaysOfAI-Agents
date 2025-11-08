"""
Main entry point for LogAnalyzerBot
Can run as CLI or web application
"""

import sys
from agent import LogAnalyzerBot


def main():
    """Main function"""
    print("🔍 LogAnalyzerBot - AI-Powered Log Analysis Tool")
    print("=" * 60)
    
    if len(sys.argv) > 1 and sys.argv[1] == 'web':
        # Start web application
        print("Starting web interface...")
        print("Navigate to: http://localhost:8000")
        import uvicorn
        from web_app import app
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        # CLI mode
        print("\nUsage:")
        print("  python main.py web          - Start web interface")
        print("  python web_app.py           - Start web interface directly")
        print("\nFor detailed usage, see README.md")


if __name__ == "__main__":
    main()
