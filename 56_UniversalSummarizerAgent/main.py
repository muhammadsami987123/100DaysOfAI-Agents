from universal_summarizer_agent import UniversalSummarizerAgent
from config import Config

def main():
    agent = UniversalSummarizerAgent()
    # Example usage (can be replaced by UI interaction)
    content = """Forwarded Email:\n— Team discussion about product launch\n— Timeline adjustments\n— Approval from client pending\n— Marketing budget discussed"""
    summary_format = "Executive Summary"
    language = "English"

    summary = agent.summarize_content(content, summary_format, language)
    print(f"Generated Summary:\n{summary}")

if __name__ == "__main__":
    main()
