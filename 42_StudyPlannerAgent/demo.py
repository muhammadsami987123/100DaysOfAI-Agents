#!/usr/bin/env python3
"""
StudyPlannerAgent - Demo Script
Demonstrates the key features of the study planning system
"""

import sys
import os
from pathlib import Path

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from utils.plan_generator import StudyPlanGenerator
from config import get_api_key, setup_instructions

def demo_plan_generation():
    """Demonstrate study plan generation"""
    print("🎯 StudyPlannerAgent Demo - Plan Generation")
    print("=" * 50)
    
    # Check API key
    api_key = get_api_key()
    if not api_key:
        print("❌ OpenAI API key not found!")
        print("Please set your API key and try again.")
        setup_instructions()
        return False
    
    try:
        # Initialize generator
        generator = StudyPlanGenerator(api_key)
        print("✅ StudyPlanGenerator initialized successfully!")
        
        # Demo study plan
        demo_goal = "Learn Python Programming"
        print(f"\n📚 Generating demo study plan for: {demo_goal}")
        print("⏳ This may take a few moments...")
        
        plan_data = generator.generate_study_plan(
            goal=demo_goal,
            days_available=30,
            hours_per_day=2,
            learning_style="mixed",
            difficulty="intermediate",
            subject="Programming",
            template="detailed"
        )
        
        print("✅ Study plan generated successfully!")
        
        # Display plan summary
        print("\n" + "=" * 60)
        print("📋 GENERATED STUDY PLAN SUMMARY")
        print("=" * 60)
        print(f"🎯 Goal: {plan_data['goal']}")
        print(f"📅 Plan ID: {plan_data['id']}")
        print(f"⏰ Total Time: {plan_data['total_hours']} hours over {plan_data['days_available']} days")
        print(f"🎨 Learning Style: {plan_data['learning_style']}")
        print(f"📊 Difficulty: {plan_data['difficulty']}")
        print(f"📚 Subject: {plan_data['subject']}")
        print(f"📋 Template: {plan_data['template']}")
        print(f"📅 Created: {plan_data['created_at']}")
        print("=" * 60)
        
        # Show first part of the plan
        content_preview = plan_data['content'][:500] + "..." if len(plan_data['content']) > 500 else plan_data['content']
        print("\n📖 Plan Preview:")
        print("-" * 40)
        print(content_preview)
        print("-" * 40)
        
        # Save the plan
        print("\n💾 Saving demo plan...")
        md_path = generator.save_plan(plan_data, "markdown")
        json_path = generator.save_plan(plan_data, "json")
        print(f"✅ Markdown: {md_path}")
        print(f"✅ JSON: {json_path}")
        
        try:
            pdf_path = generator.save_plan(plan_data, "pdf")
            print(f"✅ PDF: {pdf_path}")
        except Exception as e:
            print(f"⚠️  PDF save failed: {e}")
            print("💡 Install reportlab for PDF support: pip install reportlab")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating demo plan: {e}")
        return False

def demo_configuration():
    """Demonstrate configuration options"""
    print("\n⚙️  StudyPlannerAgent Demo - Configuration")
    print("=" * 50)
    
    try:
        generator = StudyPlanGenerator("dummy_key")  # Just for config access
        
        print("🎨 Available Learning Styles:")
        learning_styles = generator.get_learning_styles()
        for key, style in learning_styles.items():
            print(f"  • {style['name']}: {style['description']}")
        
        print("\n📊 Available Difficulty Levels:")
        difficulty_levels = generator.get_difficulty_levels()
        for key, level in difficulty_levels.items():
            print(f"  • {level['name']}: {level['description']}")
        
        print("\n📚 Available Study Subjects:")
        study_subjects = generator.get_study_subjects()
        for key, subject in study_subjects.items():
            print(f"  • {subject['name']}: {', '.join(subject['topics'][:3])}...")
        
        print("\n📋 Available Plan Templates:")
        plan_templates = generator.get_plan_templates()
        for key, template in plan_templates.items():
            print(f"  • {template['name']}: {template['description']}")
        
        print("\n💾 Available Export Formats:")
        export_formats = generator.get_export_formats()
        for key, format_info in export_formats.items():
            print(f"  • {format_info['name']}: {format_info['description']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error accessing configuration: {e}")
        return False

def demo_plan_management():
    """Demonstrate plan management features"""
    print("\n📋 StudyPlannerAgent Demo - Plan Management")
    print("=" * 50)
    
    try:
        api_key = get_api_key()
        if not api_key:
            print("⚠️  Skipping plan management demo (no API key)")
            return True
        
        generator = StudyPlanGenerator(api_key)
        
        # Get list of saved plans
        plans = generator.get_plan_list()
        
        if plans:
            print(f"📊 Found {len(plans)} saved study plan(s):")
            for i, plan in enumerate(plans[:3], 1):  # Show first 3
                print(f"  {i}. 🎯 {plan['goal']}")
                print(f"     📅 {plan['days_available']} days, {plan['hours_per_day']} hrs/day")
                print(f"     🎨 {plan['learning_style']} | 📊 {plan['difficulty']}")
                print(f"     🆔 ID: {plan['id']}")
                print()
        else:
            print("📭 No saved study plans found.")
            print("💡 Generate a plan first to see plan management features.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in plan management demo: {e}")
        return False

def main():
    """Run all demos"""
    print("🎓 StudyPlannerAgent - Feature Demonstration")
    print("=" * 60)
    print("This demo showcases the key features of StudyPlannerAgent")
    print("=" * 60)
    
    demos = [
        ("Configuration Options", demo_configuration),
        ("Plan Management", demo_plan_management),
        ("Plan Generation", demo_plan_generation)
    ]
    
    results = []
    
    for demo_name, demo_func in demos:
        try:
            print(f"\n🚀 Running: {demo_name}")
            result = demo_func()
            results.append((demo_name, result))
        except Exception as e:
            print(f"❌ {demo_name} demo failed: {e}")
            results.append((demo_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 DEMO SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for demo_name, result in results:
        status = "✅ SUCCESS" if result else "❌ FAILED"
        print(f"{status} - {demo_name}")
        if result:
            passed += 1
    
    print(f"\n📈 Results: {passed}/{total} demos completed successfully")
    
    if passed == total:
        print("\n🎉 All demos completed successfully!")
        print("\n🚀 Ready to use StudyPlannerAgent:")
        print("• Web Interface: python main.py --web")
        print("• Terminal Interface: python main.py --terminal")
        print("• Quick Plan: python main.py --quick \"Your Goal Here\"")
    else:
        print(f"\n⚠️  {total - passed} demo(s) had issues.")
        print("Check the error messages above and ensure your setup is correct.")
    
    print("\n" + "=" * 60)
    print("📚 For more information, see README.md")
    print("=" * 60)

if __name__ == "__main__":
    main()
