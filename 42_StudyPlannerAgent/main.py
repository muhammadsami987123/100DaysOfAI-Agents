#!/usr/bin/env python3
"""
📚 StudyPlannerAgent - Day 42 of #100DaysOfAI-Agents

An intelligent AI-powered study planning tool that creates personalized study plans
tailored to your goals, time constraints, and learning preferences.

Features:
- AI-generated personalized study plans using GPT-4
- Multiple learning styles (Reading, Practice, Videos, Mixed)
- Flexible difficulty levels (Beginner, Intermediate, Advanced)
- Customizable time constraints and study goals
- Export plans in multiple formats (Markdown, JSON, PDF)
- Both CLI and Web UI interfaces
- Progress tracking and plan management
- Beautiful, responsive web interface

Author: Muhammad Sami Asghar Mughal
"""

import argparse
import sys
import uvicorn
from pathlib import Path

from cli.studyplanner import StudyPlannerCLI
from web_app import create_app
from utils.plan_generator import StudyPlanGenerator
from config import get_api_key, setup_instructions

def main():
    """Main entry point for StudyPlannerAgent"""
    parser = argparse.ArgumentParser(
        description="StudyPlannerAgent - AI-powered personalized study planning tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --web                    # Start web interface (default)
  python main.py --terminal               # Start terminal interface
  python main.py --quick "Learn JavaScript"  # Quick study plan via terminal
  python main.py --quick "Prepare for IELTS" --style practice --difficulty intermediate
  python main.py --host 0.0.0.0 --port 8080  # Custom host and port
        """
    )
    
    # Interface selection
    parser.add_argument(
        "--web", 
        action="store_true", 
        help="Start web interface (default)"
    )
    
    parser.add_argument(
        "--terminal", 
        action="store_true", 
        help="Start terminal interface"
    )
    
    # Quick plan generation
    parser.add_argument(
        "--quick", 
        type=str, 
        help="Generate a quick study plan with the given goal"
    )
    
    # Quick plan options
    parser.add_argument(
        "--days", 
        type=int, 
        default=30,
        help="Days available for quick plan (default: 30)"
    )
    
    parser.add_argument(
        "--hours", 
        type=int, 
        default=2,
        help="Hours per day for quick plan (default: 2)"
    )
    
    parser.add_argument(
        "--style", 
        type=str, 
        default="mixed",
        choices=["reading", "practice", "videos", "mixed"],
        help="Learning style for quick plan (default: mixed)"
    )
    
    parser.add_argument(
        "--difficulty", 
        type=str, 
        default="intermediate",
        choices=["beginner", "intermediate", "advanced"],
        help="Difficulty level for quick plan (default: intermediate)"
    )
    
    parser.add_argument(
        "--subject", 
        type=str, 
        default="",
        help="Subject area for quick plan (optional)"
    )
    
    parser.add_argument(
        "--template", 
        type=str, 
        default="detailed",
        choices=["basic", "detailed", "intensive"],
        help="Plan template for quick plan (default: detailed)"
    )
    
    # Web server options
    parser.add_argument(
        "--host", 
        default="127.0.0.1", 
        help="Host for web interface (default: 127.0.0.1)"
    )
    
    parser.add_argument(
        "--port", 
        type=int, 
        default=8042, 
        help="Port for web interface (default: 8042)"
    )
    
    # Output options
    parser.add_argument(
        "--output", 
        type=str, 
        choices=["markdown", "json", "pdf", "all"],
        default="markdown",
        help="Output format for quick plan (default: markdown)"
    )
    
    parser.add_argument(
        "--no-save", 
        action="store_true",
        help="Don't save quick plan to file"
    )
    
    args = parser.parse_args()
    
    # Check API key
    api_key = get_api_key()
    if not api_key:
        print("❌ Error: OpenAI API key not found!")
        print()
        setup_instructions()
        sys.exit(1)
    
    # Initialize study plan generator
    try:
        plan_generator = StudyPlanGenerator(api_key)
        print("✅ StudyPlannerAgent initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing StudyPlannerAgent: {e}")
        sys.exit(1)
    
    # Handle different modes
    if args.quick:
        # Quick study plan generation via terminal
        print("📚 StudyPlannerAgent - Quick Plan Generation")
        print("=" * 50)
        print(f"🎯 Goal: {args.quick}")
        print(f"📅 Days: {args.days} | 🕐 Hours/day: {args.hours}")
        print(f"🎨 Style: {args.style} | 📊 Difficulty: {args.difficulty}")
        print(f"📚 Subject: {args.subject or 'General'}")
        print(f"📋 Template: {args.template}")
        print("=" * 50)
        
        try:
            print("🤖 Generating your study plan...")
            print("⏳ This may take a few moments...")
            
            plan_data = plan_generator.generate_study_plan(
                goal=args.quick,
                days_available=args.days,
                hours_per_day=args.hours,
                learning_style=args.style,
                difficulty=args.difficulty,
                subject=args.subject,
                template=args.template
            )
            
            print("✅ Study plan generated successfully!")
            print()
            
            # Display plan
            print("=" * 60)
            print("📚 YOUR STUDY PLAN")
            print("=" * 60)
            print(f"🎯 Goal: {plan_data['goal']}")
            print(f"📅 Plan ID: {plan_data['id']}")
            print(f"⏰ Total Time: {plan_data['total_hours']} hours over {plan_data['days_available']} days")
            print("=" * 60)
            print()
            print(plan_data['content'])
            print("=" * 60)
            
            # Save plan if requested
            if not args.no_save:
                print()
                print("💾 Saving study plan...")
                
                if args.output == "all":
                    # Save all formats
                    md_path = plan_generator.save_plan(plan_data, "markdown")
                    json_path = plan_generator.save_plan(plan_data, "json")
                    print(f"✅ Markdown: {md_path}")
                    print(f"✅ JSON: {json_path}")
                    
                    try:
                        pdf_path = plan_generator.save_plan(plan_data, "pdf")
                        print(f"✅ PDF: {pdf_path}")
                    except Exception as e:
                        print(f"⚠️  PDF save failed: {e}")
                        print("💡 Install reportlab for PDF support: pip install reportlab")
                else:
                    try:
                        filepath = plan_generator.save_plan(plan_data, args.output)
                        print(f"✅ Plan saved: {filepath}")
                    except Exception as e:
                        print(f"❌ Save failed: {e}")
                        if args.output == "pdf":
                            print("💡 Install reportlab for PDF support: pip install reportlab")
            
        except Exception as e:
            print(f"❌ Error generating study plan: {e}")
            sys.exit(1)
    
    elif args.terminal:
        # Terminal interface
        print("📚 StudyPlannerAgent - Terminal Mode")
        print("Type 'help' for commands, 'quit' to exit")
        cli = StudyPlannerCLI()
        cli.run()
        
    else:
        # Web interface (default)
        print(f"🌐 Starting StudyPlannerAgent web interface...")
        print(f"📚 Open your browser to: http://{args.host}:{args.port}")
        print("Press Ctrl+C to stop the server")
        
        app = create_app(plan_generator)
        uvicorn.run(
            app, 
            host=args.host, 
            port=args.port,
            log_level="info"
        )

if __name__ == "__main__":
    main()
