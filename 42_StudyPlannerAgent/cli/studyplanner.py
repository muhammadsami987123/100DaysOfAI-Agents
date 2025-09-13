"""
StudyPlannerAgent CLI Interface
Command-line interface for study plan generation and management
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from utils.plan_generator import StudyPlanGenerator
from config import StudyConfig, get_api_key, setup_instructions

class StudyPlannerCLI:
    """Command-line interface for StudyPlannerAgent"""
    
    def __init__(self):
        """Initialize the CLI interface"""
        self.config = StudyConfig()
        self.generator = None
        self.running = False
    
    def initialize(self) -> bool:
        """Initialize the study plan generator"""
        api_key = get_api_key()
        if not api_key:
            print("❌ Error: OpenAI API key not found!")
            print()
            setup_instructions()
            return False
        
        try:
            self.generator = StudyPlanGenerator(api_key)
            return True
        except Exception as e:
            print(f"❌ Error initializing StudyPlannerAgent: {e}")
            return False
    
    def show_welcome(self):
        """Display welcome message"""
        print("=" * 60)
        print("📚 StudyPlannerAgent - AI-Powered Study Planning")
        print("=" * 60)
        print("Create personalized, intelligent study plans tailored to your goals!")
        print()
        print("Features:")
        print("• AI-generated study plans")
        print("• Multiple learning styles")
        print("• Flexible time management")
        print("• Progress tracking")
        print("• Export to multiple formats")
        print()
    
    def show_main_menu(self):
        """Display main menu options"""
        print("\n" + "=" * 40)
        print("📋 MAIN MENU")
        print("=" * 40)
        print("1. 📝 Generate New Study Plan")
        print("2. 📋 View Saved Plans")
        print("3. 🔍 Load Existing Plan")
        print("4. ⚙️  Configuration")
        print("5. ❓ Help")
        print("0. 🚪 Exit")
        print("=" * 40)
    
    def generate_study_plan(self):
        """Interactive study plan generation"""
        print("\n" + "=" * 50)
        print("📝 GENERATE NEW STUDY PLAN")
        print("=" * 50)
        
        try:
            # Get study goal
            goal = input("🎯 What is your study goal? (e.g., 'Learn JavaScript', 'Prepare for IELTS'): ").strip()
            if not goal:
                print("❌ Study goal is required!")
                return
            
            # Get time constraints
            print("\n⏰ Time Constraints:")
            try:
                days_available = int(input("📅 How many days do you have? (default: 30): ") or "30")
                hours_per_day = int(input("🕐 How many hours per day? (default: 2): ") or "2")
            except ValueError:
                print("❌ Please enter valid numbers!")
                return
            
            # Get learning style
            print("\n🎨 Learning Style:")
            learning_styles = self.generator.get_learning_styles()
            for i, (key, style) in enumerate(learning_styles.items(), 1):
                print(f"{i}. {style['name']}: {style['description']}")
            
            try:
                style_choice = int(input("Choose learning style (1-4, default: 4): ") or "4")
                style_keys = list(learning_styles.keys())
                learning_style = style_keys[style_choice - 1] if 1 <= style_choice <= len(style_keys) else "mixed"
            except (ValueError, IndexError):
                learning_style = "mixed"
            
            # Get difficulty level
            print("\n📊 Difficulty Level:")
            difficulty_levels = self.generator.get_difficulty_levels()
            for i, (key, level) in enumerate(difficulty_levels.items(), 1):
                print(f"{i}. {level['name']}: {level['description']}")
            
            try:
                diff_choice = int(input("Choose difficulty (1-3, default: 2): ") or "2")
                diff_keys = list(difficulty_levels.keys())
                difficulty = diff_keys[diff_choice - 1] if 1 <= diff_choice <= len(diff_keys) else "intermediate"
            except (ValueError, IndexError):
                difficulty = "intermediate"
            
            # Get subject (optional)
            subject = input("\n📚 Subject area (optional, e.g., 'Programming', 'Languages'): ").strip()
            
            # Get template
            print("\n📋 Plan Template:")
            templates = self.generator.get_plan_templates()
            for i, (key, template) in enumerate(templates.items(), 1):
                print(f"{i}. {template['name']}: {template['description']}")
            
            try:
                template_choice = int(input("Choose template (1-3, default: 2): ") or "2")
                template_keys = list(templates.keys())
                template = template_keys[template_choice - 1] if 1 <= template_choice <= len(template_keys) else "detailed"
            except (ValueError, IndexError):
                template = "detailed"
            
            # Confirm details
            print("\n" + "=" * 50)
            print("📋 STUDY PLAN DETAILS")
            print("=" * 50)
            print(f"🎯 Goal: {goal}")
            print(f"📅 Days Available: {days_available}")
            print(f"🕐 Hours per Day: {hours_per_day}")
            print(f"⏱️  Total Study Time: {days_available * hours_per_day} hours")
            print(f"🎨 Learning Style: {learning_styles[learning_style]['name']}")
            print(f"📊 Difficulty: {difficulty_levels[difficulty]['name']}")
            print(f"📚 Subject: {subject or 'General'}")
            print(f"📋 Template: {templates[template]['name']}")
            print("=" * 50)
            
            confirm = input("\n✅ Generate study plan? (y/N): ").strip().lower()
            if confirm not in ['y', 'yes']:
                print("❌ Study plan generation cancelled.")
                return
            
            # Generate study plan
            print("\n🤖 Generating your personalized study plan...")
            print("⏳ This may take a few moments...")
            
            plan_data = self.generator.generate_study_plan(
                goal=goal,
                days_available=days_available,
                hours_per_day=hours_per_day,
                learning_style=learning_style,
                difficulty=difficulty,
                subject=subject,
                template=template
            )
            
            print("✅ Study plan generated successfully!")
            
            # Display plan
            self._display_plan(plan_data)
            
            # Save plan
            self._save_plan_options(plan_data)
            
        except KeyboardInterrupt:
            print("\n❌ Study plan generation cancelled.")
        except Exception as e:
            print(f"❌ Error generating study plan: {e}")
    
    def _display_plan(self, plan_data: Dict[str, Any]):
        """Display the generated study plan"""
        print("\n" + "=" * 60)
        print("📚 YOUR PERSONALIZED STUDY PLAN")
        print("=" * 60)
        print(f"🎯 Goal: {plan_data['goal']}")
        print(f"📅 Plan ID: {plan_data['id']}")
        print(f"⏰ Total Time: {plan_data['total_hours']} hours over {plan_data['days_available']} days")
        print("=" * 60)
        print()
        print(plan_data['content'])
        print("=" * 60)
    
    def _save_plan_options(self, plan_data: Dict[str, Any]):
        """Handle plan saving options"""
        print("\n💾 Save Options:")
        print("1. Save as Markdown (.md)")
        print("2. Save as JSON (.json)")
        print("3. Save as PDF (.pdf)")
        print("4. Save all formats")
        print("0. Skip saving")
        
        try:
            choice = input("Choose save option (0-4): ").strip()
            
            if choice == "1":
                filepath = self.generator.save_plan(plan_data, "markdown")
                print(f"✅ Plan saved as Markdown: {filepath}")
            elif choice == "2":
                filepath = self.generator.save_plan(plan_data, "json")
                print(f"✅ Plan saved as JSON: {filepath}")
            elif choice == "3":
                try:
                    filepath = self.generator.save_plan(plan_data, "pdf")
                    print(f"✅ Plan saved as PDF: {filepath}")
                except Exception as e:
                    print(f"❌ PDF save failed: {e}")
                    print("💡 Install reportlab for PDF support: pip install reportlab")
            elif choice == "4":
                # Save all formats
                md_path = self.generator.save_plan(plan_data, "markdown")
                json_path = self.generator.save_plan(plan_data, "json")
                print(f"✅ Plan saved as Markdown: {md_path}")
                print(f"✅ Plan saved as JSON: {json_path}")
                
                try:
                    pdf_path = self.generator.save_plan(plan_data, "pdf")
                    print(f"✅ Plan saved as PDF: {pdf_path}")
                except Exception as e:
                    print(f"⚠️  PDF save failed: {e}")
            elif choice == "0":
                print("⏭️  Skipping save.")
            else:
                print("❌ Invalid choice. Plan not saved.")
                
        except Exception as e:
            print(f"❌ Error saving plan: {e}")
    
    def view_saved_plans(self):
        """Display list of saved study plans"""
        print("\n" + "=" * 50)
        print("📋 SAVED STUDY PLANS")
        print("=" * 50)
        
        plans = self.generator.get_plan_list()
        
        if not plans:
            print("📭 No saved study plans found.")
            print("💡 Generate a new study plan to get started!")
            return
        
        print(f"📊 Found {len(plans)} saved plan(s):")
        print()
        
        for i, plan in enumerate(plans, 1):
            print(f"{i}. 🎯 {plan['goal']}")
            print(f"   📅 Created: {plan['created_at'][:10]}")
            print(f"   ⏰ {plan['days_available']} days, {plan['hours_per_day']} hrs/day")
            print(f"   🎨 {plan['learning_style']} | 📊 {plan['difficulty']}")
            print(f"   🆔 ID: {plan['id']}")
            print()
        
        # Option to load a plan
        try:
            choice = input("Enter plan number to view details (0 to go back): ").strip()
            if choice == "0":
                return
            
            plan_index = int(choice) - 1
            if 0 <= plan_index < len(plans):
                plan_id = plans[plan_index]['id']
                self._load_and_display_plan(plan_id)
            else:
                print("❌ Invalid plan number.")
        except ValueError:
            print("❌ Please enter a valid number.")
        except KeyboardInterrupt:
            print("\n⏭️  Returning to main menu.")
    
    def _load_and_display_plan(self, plan_id: str):
        """Load and display a specific study plan"""
        plan_data = self.generator.load_plan(plan_id)
        
        if not plan_data:
            print(f"❌ Plan {plan_id} not found.")
            return
        
        self._display_plan(plan_data)
        
        # Options for loaded plan
        print("\n📋 Plan Options:")
        print("1. Save in different format")
        print("2. Delete this plan")
        print("0. Go back")
        
        try:
            choice = input("Choose option (0-2): ").strip()
            
            if choice == "1":
                self._save_plan_options(plan_data)
            elif choice == "2":
                confirm = input("⚠️  Are you sure you want to delete this plan? (y/N): ").strip().lower()
                if confirm in ['y', 'yes']:
                    if self.generator.delete_plan(plan_id):
                        print("✅ Plan deleted successfully.")
                    else:
                        print("❌ Failed to delete plan.")
            elif choice == "0":
                return
            else:
                print("❌ Invalid choice.")
                
        except KeyboardInterrupt:
            print("\n⏭️  Returning to main menu.")
    
    def load_existing_plan(self):
        """Load an existing study plan by ID"""
        print("\n" + "=" * 50)
        print("🔍 LOAD EXISTING PLAN")
        print("=" * 50)
        
        plan_id = input("🆔 Enter plan ID: ").strip()
        
        if not plan_id:
            print("❌ Plan ID is required!")
            return
        
        self._load_and_display_plan(plan_id)
    
    def show_configuration(self):
        """Display configuration information"""
        print("\n" + "=" * 50)
        print("⚙️  CONFIGURATION")
        print("=" * 50)
        
        print("📚 StudyPlannerAgent Configuration:")
        print(f"• Output Directory: {self.config.OUTPUT_DIR}")
        print(f"• Plans Directory: {self.config.PLANS_DIR}")
        print(f"• Default Learning Style: {self.config.DEFAULT_LEARNING_STYLE}")
        print(f"• Default Difficulty: {self.config.DEFAULT_DIFFICULTY}")
        print(f"• Default Hours per Day: {self.config.DEFAULT_HOURS_PER_DAY}")
        print(f"• Default Days Available: {self.config.DEFAULT_DAYS_AVAILABLE}")
        print()
        
        print("🎨 Available Learning Styles:")
        learning_styles = self.generator.get_learning_styles()
        for key, style in learning_styles.items():
            print(f"• {style['name']}: {style['description']}")
        print()
        
        print("📊 Available Difficulty Levels:")
        difficulty_levels = self.generator.get_difficulty_levels()
        for key, level in difficulty_levels.items():
            print(f"• {level['name']}: {level['description']}")
        print()
        
        print("📋 Available Templates:")
        templates = self.generator.get_plan_templates()
        for key, template in templates.items():
            print(f"• {template['name']}: {template['description']}")
        print()
        
        print("💾 Available Export Formats:")
        export_formats = self.generator.get_export_formats()
        for key, format_info in export_formats.items():
            print(f"• {format_info['name']}: {format_info['description']}")
    
    def show_help(self):
        """Display help information"""
        print("\n" + "=" * 50)
        print("❓ HELP & USAGE GUIDE")
        print("=" * 50)
        
        print("📚 StudyPlannerAgent helps you create personalized study plans using AI.")
        print()
        
        print("🎯 Getting Started:")
        print("1. Choose 'Generate New Study Plan' from the main menu")
        print("2. Enter your study goal (e.g., 'Learn Python', 'Prepare for IELTS')")
        print("3. Set your time constraints (days available, hours per day)")
        print("4. Choose your learning style and difficulty level")
        print("5. Select a plan template")
        print("6. Review and save your personalized study plan")
        print()
        
        print("💡 Tips for Best Results:")
        print("• Be specific about your study goal")
        print("• Set realistic time constraints")
        print("• Choose a learning style that matches your preferences")
        print("• Start with intermediate difficulty if unsure")
        print("• Save your plans in multiple formats for flexibility")
        print()
        
        print("📋 Learning Styles:")
        print("• Reading: Learn through textbooks and written materials")
        print("• Practice: Learn through hands-on exercises and projects")
        print("• Videos: Learn through video tutorials and lectures")
        print("• Mixed: Combination of all learning methods")
        print()
        
        print("📊 Difficulty Levels:")
        print("• Beginner: No prior knowledge required")
        print("• Intermediate: Some prior knowledge helpful")
        print("• Advanced: Strong foundation required")
        print()
        
        print("🔧 Troubleshooting:")
        print("• Make sure your OpenAI API key is set correctly")
        print("• Check your internet connection for AI generation")
        print("• For PDF export, install reportlab: pip install reportlab")
        print("• Plans are saved in the 'output/study_plans' directory")
    
    def run(self):
        """Main CLI loop"""
        if not self.initialize():
            return
        
        self.show_welcome()
        self.running = True
        
        while self.running:
            try:
                self.show_main_menu()
                choice = input("Select option (0-5): ").strip()
                
                if choice == "0":
                    print("\n👋 Thank you for using StudyPlannerAgent!")
                    print("📚 Good luck with your studies!")
                    self.running = False
                elif choice == "1":
                    self.generate_study_plan()
                elif choice == "2":
                    self.view_saved_plans()
                elif choice == "3":
                    self.load_existing_plan()
                elif choice == "4":
                    self.show_configuration()
                elif choice == "5":
                    self.show_help()
                else:
                    print("❌ Invalid choice. Please select 0-5.")
                
                if self.running and choice != "0":
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                self.running = False
            except Exception as e:
                print(f"\n❌ Error: {e}")
                input("Press Enter to continue...")

def main():
    """Main entry point for CLI"""
    cli = StudyPlannerCLI()
    cli.run()

if __name__ == "__main__":
    main()
