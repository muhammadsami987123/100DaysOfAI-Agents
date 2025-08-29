#!/usr/bin/env python3
"""
ResumeFeedbackBot CLI Interface
Command-line interface for resume and portfolio analysis
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Optional

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from resume_analyzer import ResumeAnalyzer
from portfolio_analyzer import PortfolioAnalyzer

class ResumeFeedbackBotCLI:
    """CLI interface for ResumeFeedbackBot"""
    
    def __init__(self):
        """Initialize CLI interface"""
        self.resume_analyzer = ResumeAnalyzer()
        self.portfolio_analyzer = PortfolioAnalyzer()
        
    def validate_config(self) -> bool:
        """Validate configuration and API key"""
        errors = Config.validate_config()
        if errors:
            print("❌ Configuration errors:")
            for error in errors:
                print(f"   - {error}")
            return False
        return True
    
    def analyze_resume_cli(self, file_path: str, target_role: str = "", industry: str = "", output_file: Optional[str] = None):
        """Analyze resume from command line"""
        try:
            # Validate file exists
            if not os.path.exists(file_path):
                print(f"❌ File not found: {file_path}")
                return False
            
            # Check file extension
            file_ext = Path(file_path).suffix.lower()
            if file_ext not in ['.pdf', '.docx', '.doc']:
                print(f"❌ Unsupported file format: {file_ext}")
                print("Supported formats: PDF, DOCX, DOC")
                return False
            
            print(f"📄 Analyzing resume: {file_path}")
            print("⏳ Extracting text...")
            
            # Extract text from file
            resume_text = self.resume_analyzer.extract_text_from_file(file_path)
            print(f"✅ Text extracted ({len(resume_text)} characters)")
            
            print("🤖 Running AI analysis...")
            
            # Analyze resume
            analysis = self.resume_analyzer.analyze_resume(resume_text, target_role, industry)
            
            if analysis.get('error'):
                print(f"❌ Analysis failed: {analysis.get('error_message', 'Unknown error')}")
                return False
            
            # Display results
            self._display_resume_results(analysis)
            
            # Generate improved version
            print("\n🔄 Generating improved version...")
            improvements = self.resume_analyzer.generate_improved_version(resume_text, analysis)
            
            if not improvements.get('error'):
                self._display_improvements(improvements)
            
            # Save results if output file specified
            if output_file:
                self._save_results(analysis, output_file)
            
            return True
            
        except Exception as e:
            print(f"❌ Error analyzing resume: {str(e)}")
            return False
    
    def analyze_portfolio_cli(self, portfolio_url: str, output_file: Optional[str] = None):
        """Analyze portfolio from command line"""
        try:
            print(f"🌐 Analyzing portfolio: {portfolio_url}")
            print("⏳ Fetching website content...")
            
            # Analyze portfolio
            analysis = self.portfolio_analyzer.analyze_portfolio(portfolio_url)
            
            if analysis.get('error'):
                print(f"❌ Analysis failed: {analysis.get('error_message', 'Unknown error')}")
                return False
            
            # Display results
            self._display_portfolio_results(analysis)
            
            # Save results if output file specified
            if output_file:
                self._save_results(analysis, output_file)
            
            return True
            
        except Exception as e:
            print(f"❌ Error analyzing portfolio: {str(e)}")
            return False
    
    def _display_resume_results(self, analysis: dict):
        """Display resume analysis results"""
        print("\n" + "="*60)
        print("📊 RESUME ANALYSIS RESULTS")
        print("="*60)
        
        # Overall score
        overall_score = analysis.get('overall_score', 0)
        print(f"\n🎯 Overall Score: {overall_score:.1f}/10")
        
        # Individual scores
        print("\n📈 Detailed Scores:")
        scores = analysis.get('scores', {})
        for criterion, score in scores.items():
            bar_length = int(score * 5)  # 5 characters for max score
            bar = "█" * bar_length + "░" * (5 - bar_length)
            print(f"   {criterion.replace('_', ' ').title():<20} {score}/10 {bar}")
        
        # Strengths
        strengths = analysis.get('strengths', [])
        if strengths:
            print(f"\n✅ Strengths ({len(strengths)}):")
            for i, strength in enumerate(strengths, 1):
                print(f"   {i}. {strength}")
        
        # Weaknesses
        weaknesses = analysis.get('weaknesses', [])
        if weaknesses:
            print(f"\n⚠️  Areas for Improvement ({len(weaknesses)}):")
            for i, weakness in enumerate(weaknesses, 1):
                print(f"   {i}. {weakness}")
        
        # Suggestions
        suggestions = analysis.get('suggestions', [])
        if suggestions:
            print(f"\n💡 Suggestions ({len(suggestions)}):")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"   {i}. {suggestion}")
        
        # Section analysis
        section_analysis = analysis.get('section_analysis', {})
        if section_analysis:
            print(f"\n📋 Section Analysis:")
            for section, details in section_analysis.items():
                if isinstance(details, dict):
                    score = details.get('score', 'N/A')
                    feedback = details.get('feedback', 'No feedback available')
                    print(f"   {section.title()}: {score}/10 - {feedback}")
        
        print("\n" + "="*60)
    
    def _display_portfolio_results(self, analysis: dict):
        """Display portfolio analysis results"""
        print("\n" + "="*60)
        print("🌐 PORTFOLIO ANALYSIS RESULTS")
        print("="*60)
        
        # Overall score
        overall_score = analysis.get('overall_score', 0)
        print(f"\n🎯 Overall Score: {overall_score:.1f}/10")
        
        # Individual scores
        print("\n📈 Detailed Scores:")
        scores = analysis.get('scores', {})
        for criterion, score in scores.items():
            bar_length = int(score * 5)  # 5 characters for max score
            bar = "█" * bar_length + "░" * (5 - bar_length)
            print(f"   {criterion.replace('_', ' ').title():<20} {score}/10 {bar}")
        
        # Strengths
        strengths = analysis.get('strengths', [])
        if strengths:
            print(f"\n✅ Strengths ({len(strengths)}):")
            for i, strength in enumerate(strengths, 1):
                print(f"   {i}. {strength}")
        
        # Weaknesses
        weaknesses = analysis.get('weaknesses', [])
        if weaknesses:
            print(f"\n⚠️  Areas for Improvement ({len(weaknesses)}):")
            for i, weakness in enumerate(weaknesses, 1):
                print(f"   {i}. {weakness}")
        
        # Suggestions
        suggestions = analysis.get('suggestions', [])
        if suggestions:
            print(f"\n💡 Suggestions ({len(suggestions)}):")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"   {i}. {suggestion}")
        
        # Technical recommendations
        tech_recs = analysis.get('technical_recommendations', [])
        if tech_recs:
            print(f"\n🔧 Technical Recommendations ({len(tech_recs)}):")
            for i, rec in enumerate(tech_recs, 1):
                print(f"   {i}. {rec}")
        
        # Website data
        website_data = analysis.get('website_data', {})
        if website_data:
            print(f"\n📊 Website Statistics:")
            print(f"   Pages Analyzed: {website_data.get('pages_analyzed', 'N/A')}")
            print(f"   Links Found: {website_data.get('links_count', 'N/A')}")
            print(f"   Content Size: {website_data.get('content_length', 'N/A')} bytes")
        
        print("\n" + "="*60)
    
    def _display_improvements(self, improvements: dict):
        """Display resume improvements"""
        print("\n" + "="*60)
        print("✨ IMPROVED RESUME VERSION")
        print("="*60)
        
        # Key improvements
        key_improvements = improvements.get('key_improvements', [])
        if key_improvements:
            print(f"\n🔧 Key Improvements Made:")
            for i, improvement in enumerate(key_improvements, 1):
                print(f"   {i}. {improvement}")
        
        # Improved summary
        improved_summary = improvements.get('improved_summary', '')
        if improved_summary:
            print(f"\n📝 Improved Summary:")
            print(f"   {improved_summary}")
        
        # Improved experience
        improved_experience = improvements.get('improved_experience', [])
        if improved_experience:
            print(f"\n💼 Improved Experience Descriptions:")
            for i, exp in enumerate(improved_experience, 1):
                print(f"   {i}. {exp}")
        
        # Full improved resume
        improved_resume = improvements.get('improved_resume', '')
        if improved_resume:
            print(f"\n📄 Complete Improved Resume:")
            print("-" * 40)
            print(improved_resume)
            print("-" * 40)
        
        print("\n" + "="*60)
    
    def _save_results(self, analysis: dict, output_file: str):
        """Save analysis results to file"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Results saved to: {output_file}")
        except Exception as e:
            print(f"\n❌ Error saving results: {str(e)}")
    
    def interactive_mode(self):
        """Run interactive mode"""
        print("🤖 Welcome to ResumeFeedbackBot CLI!")
        print("="*50)
        
        while True:
            print("\nOptions:")
            print("1. Analyze Resume")
            print("2. Analyze Portfolio")
            print("3. Exit")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                self._interactive_resume_analysis()
            elif choice == '2':
                self._interactive_portfolio_analysis()
            elif choice == '3':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please try again.")
    
    def _interactive_resume_analysis(self):
        """Interactive resume analysis"""
        print("\n📄 Resume Analysis")
        print("-" * 30)
        
        # Get file path
        file_path = input("Enter resume file path: ").strip()
        if not file_path:
            print("❌ No file path provided.")
            return
        
        # Get optional parameters
        target_role = input("Target job role (optional): ").strip()
        industry = input("Industry (optional): ").strip()
        
        # Get output file
        save_results = input("Save results to file? (y/n): ").strip().lower()
        output_file = None
        if save_results == 'y':
            output_file = input("Output file path: ").strip()
            if not output_file:
                output_file = f"resume_analysis_{os.path.basename(file_path)}.json"
        
        # Run analysis
        self.analyze_resume_cli(file_path, target_role, industry, output_file)
    
    def _interactive_portfolio_analysis(self):
        """Interactive portfolio analysis"""
        print("\n🌐 Portfolio Analysis")
        print("-" * 30)
        
        # Get portfolio URL
        portfolio_url = input("Enter portfolio URL: ").strip()
        if not portfolio_url:
            print("❌ No URL provided.")
            return
        
        # Get output file
        save_results = input("Save results to file? (y/n): ").strip().lower()
        output_file = None
        if save_results == 'y':
            output_file = input("Output file path: ").strip()
            if not output_file:
                output_file = f"portfolio_analysis_{portfolio_url.replace('://', '_').replace('/', '_')}.json"
        
        # Run analysis
        self.analyze_portfolio_cli(portfolio_url, output_file)

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="ResumeFeedbackBot - AI-powered resume and portfolio analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze resume
  python cli.py resume resume.pdf --role "Software Engineer" --industry "Technology"
  
  # Analyze portfolio
  python cli.py portfolio https://example.com --output results.json
  
  # Interactive mode
  python cli.py interactive
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Resume analysis parser
    resume_parser = subparsers.add_parser('resume', help='Analyze resume')
    resume_parser.add_argument('file', help='Path to resume file (PDF/DOCX)')
    resume_parser.add_argument('--role', '--target-role', help='Target job role')
    resume_parser.add_argument('--industry', help='Industry')
    resume_parser.add_argument('--output', '-o', help='Output file for results')
    
    # Portfolio analysis parser
    portfolio_parser = subparsers.add_parser('portfolio', help='Analyze portfolio')
    portfolio_parser.add_argument('url', help='Portfolio website URL')
    portfolio_parser.add_argument('--output', '-o', help='Output file for results')
    
    # Interactive mode parser
    subparsers.add_parser('interactive', help='Run in interactive mode')
    
    args = parser.parse_args()
    
    # Initialize CLI
    cli = ResumeFeedbackBotCLI()
    
    # Validate configuration
    if not cli.validate_config():
        sys.exit(1)
    
    # Handle commands
    if args.command == 'resume':
        success = cli.analyze_resume_cli(
            args.file, 
            args.role or "", 
            args.industry or "", 
            args.output
        )
        sys.exit(0 if success else 1)
    
    elif args.command == 'portfolio':
        success = cli.analyze_portfolio_cli(args.url, args.output)
        sys.exit(0 if success else 1)
    
    elif args.command == 'interactive':
        cli.interactive_mode()
    
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
