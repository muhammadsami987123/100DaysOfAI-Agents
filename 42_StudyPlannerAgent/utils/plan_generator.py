"""
Study Plan Generator - AI-powered study plan creation
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path

import openai
from config import StudyConfig

class StudyPlanGenerator:
    """AI-powered study plan generator using OpenAI GPT"""
    
    def __init__(self, api_key: str):
        """Initialize the study plan generator"""
        self.client = openai.OpenAI(api_key=api_key)
        self.config = StudyConfig()
        
        # Ensure output directories exist
        self.output_dir = Path(self.config.OUTPUT_DIR)
        self.plans_dir = self.output_dir / self.config.PLANS_DIR
        self.plans_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_study_plan(
        self,
        goal: str,
        days_available: int,
        hours_per_day: int,
        learning_style: str = "mixed",
        difficulty: str = "intermediate",
        subject: str = "",
        template: str = "detailed"
    ) -> Dict[str, Any]:
        """Generate a comprehensive study plan"""
        
        # Validate inputs
        if not goal or not goal.strip():
            raise ValueError("Study goal is required")
        
        if days_available <= 0:
            raise ValueError("Days available must be positive")
        
        if hours_per_day <= 0:
            raise ValueError("Hours per day must be positive")
        
        if learning_style not in self.config.LEARNING_STYLES:
            learning_style = self.config.DEFAULT_LEARNING_STYLE
        
        if difficulty not in self.config.DIFFICULTY_LEVELS:
            difficulty = self.config.DEFAULT_DIFFICULTY
        
        # Calculate total study time
        total_hours = days_available * hours_per_day
        
        # Prepare prompt
        prompt = self._prepare_prompt(
            goal=goal,
            days_available=days_available,
            hours_per_day=hours_per_day,
            learning_style=learning_style,
            difficulty=difficulty,
            subject=subject,
            template=template
        )
        
        try:
            # Generate study plan using OpenAI
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert educational consultant and study planner. Create comprehensive, personalized study plans that are practical, achievable, and motivating."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.config.MAX_TOKENS,
                temperature=self.config.TEMPERATURE
            )
            
            plan_content = response.choices[0].message.content
            
            # Create plan metadata
            plan_data = {
                "id": self._generate_plan_id(),
                "goal": goal,
                "days_available": days_available,
                "hours_per_day": hours_per_day,
                "total_hours": total_hours,
                "learning_style": learning_style,
                "difficulty": difficulty,
                "subject": subject,
                "template": template,
                "content": plan_content,
                "created_at": datetime.now().isoformat(),
                "status": "active"
            }
            
            return plan_data
            
        except Exception as e:
            raise Exception(f"Failed to generate study plan: {str(e)}")
    
    def _prepare_prompt(
        self,
        goal: str,
        days_available: int,
        hours_per_day: int,
        learning_style: str,
        difficulty: str,
        subject: str,
        template: str
    ) -> str:
        """Prepare the prompt for study plan generation"""
        
        # Get template-specific prompt
        if template == "quick":
            prompt_template = self.config.STUDY_PLAN_PROMPTS["quick"]
        elif template == "detailed":
            prompt_template = self.config.STUDY_PLAN_PROMPTS["detailed"]
        else:
            prompt_template = self.config.STUDY_PLAN_PROMPTS["base"]
        
        # Format the prompt
        prompt = prompt_template.format(
            goal=goal,
            days_available=days_available,
            hours_per_day=hours_per_day,
            learning_style=learning_style,
            difficulty=difficulty,
            subject=subject or "General"
        )
        
        return prompt
    
    def _generate_plan_id(self) -> str:
        """Generate a unique plan ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"study_plan_{timestamp}"
    
    def save_plan(self, plan_data: Dict[str, Any], format: str = "markdown") -> str:
        """Save study plan to file"""
        
        plan_id = plan_data["id"]
        
        if format == "markdown":
            return self._save_markdown(plan_data)
        elif format == "json":
            return self._save_json(plan_data)
        elif format == "pdf":
            return self._save_pdf(plan_data)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _save_markdown(self, plan_data: Dict[str, Any]) -> str:
        """Save plan as Markdown file"""
        
        plan_id = plan_data["id"]
        filename = f"{plan_id}.md"
        filepath = self.plans_dir / filename
        
        # Create markdown content
        content = f"""# Study Plan: {plan_data['goal']}

**Generated on:** {plan_data['created_at']}
**Plan ID:** {plan_data['id']}

## Study Details
- **Goal:** {plan_data['goal']}
- **Time Available:** {plan_data['days_available']} days
- **Hours per Day:** {plan_data['hours_per_day']} hours
- **Total Study Time:** {plan_data['total_hours']} hours
- **Learning Style:** {plan_data['learning_style']}
- **Difficulty Level:** {plan_data['difficulty']}
- **Subject:** {plan_data['subject'] or 'General'}

---

{plan_data['content']}

---

*This study plan was generated by StudyPlannerAgent*
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(filepath)
    
    def _save_json(self, plan_data: Dict[str, Any]) -> str:
        """Save plan as JSON file"""
        
        plan_id = plan_data["id"]
        filename = f"{plan_id}.json"
        filepath = self.plans_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(plan_data, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def _save_pdf(self, plan_data: Dict[str, Any]) -> str:
        """Save plan as PDF file"""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            
            plan_id = plan_data["id"]
            filename = f"{plan_id}.pdf"
            filepath = self.plans_dir / filename
            
            # Create PDF document
            doc = SimpleDocTemplate(str(filepath), pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                spaceAfter=30,
                alignment=1  # Center alignment
            )
            story.append(Paragraph(f"Study Plan: {plan_data['goal']}", title_style))
            story.append(Spacer(1, 12))
            
            # Study details
            details_style = ParagraphStyle(
                'Details',
                parent=styles['Normal'],
                fontSize=12,
                spaceAfter=12
            )
            
            details = f"""
            <b>Generated on:</b> {plan_data['created_at']}<br/>
            <b>Plan ID:</b> {plan_data['id']}<br/>
            <b>Goal:</b> {plan_data['goal']}<br/>
            <b>Time Available:</b> {plan_data['days_available']} days<br/>
            <b>Hours per Day:</b> {plan_data['hours_per_day']} hours<br/>
            <b>Total Study Time:</b> {plan_data['total_hours']} hours<br/>
            <b>Learning Style:</b> {plan_data['learning_style']}<br/>
            <b>Difficulty Level:</b> {plan_data['difficulty']}<br/>
            <b>Subject:</b> {plan_data['subject'] or 'General'}
            """
            
            story.append(Paragraph(details, details_style))
            story.append(Spacer(1, 20))
            
            # Plan content
            content_style = ParagraphStyle(
                'Content',
                parent=styles['Normal'],
                fontSize=11,
                spaceAfter=12
            )
            
            # Split content into paragraphs and add to PDF
            content_paragraphs = plan_data['content'].split('\n\n')
            for para in content_paragraphs:
                if para.strip():
                    story.append(Paragraph(para.strip(), content_style))
                    story.append(Spacer(1, 6))
            
            # Build PDF
            doc.build(story)
            
            return str(filepath)
            
        except ImportError:
            raise Exception("PDF generation requires reportlab package. Install with: pip install reportlab")
    
    def get_plan_list(self) -> List[Dict[str, Any]]:
        """Get list of all saved study plans"""
        
        plans = []
        
        # Look for JSON files in plans directory
        for json_file in self.plans_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    plan_data = json.load(f)
                    plans.append({
                        "id": plan_data.get("id", ""),
                        "goal": plan_data.get("goal", ""),
                        "created_at": plan_data.get("created_at", ""),
                        "days_available": plan_data.get("days_available", 0),
                        "hours_per_day": plan_data.get("hours_per_day", 0),
                        "learning_style": plan_data.get("learning_style", ""),
                        "difficulty": plan_data.get("difficulty", ""),
                        "status": plan_data.get("status", "active")
                    })
            except Exception as e:
                print(f"Error reading plan file {json_file}: {e}")
                continue
        
        # Sort by creation date (newest first)
        plans.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        return plans
    
    def load_plan(self, plan_id: str) -> Optional[Dict[str, Any]]:
        """Load a specific study plan by ID"""
        
        json_file = self.plans_dir / f"{plan_id}.json"
        
        if not json_file.exists():
            return None
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading plan {plan_id}: {e}")
            return None
    
    def delete_plan(self, plan_id: str) -> bool:
        """Delete a study plan and its associated files"""
        
        try:
            # Delete JSON file
            json_file = self.plans_dir / f"{plan_id}.json"
            if json_file.exists():
                json_file.unlink()
            
            # Delete Markdown file
            md_file = self.plans_dir / f"{plan_id}.md"
            if md_file.exists():
                md_file.unlink()
            
            # Delete PDF file
            pdf_file = self.plans_dir / f"{plan_id}.pdf"
            if pdf_file.exists():
                pdf_file.unlink()
            
            return True
            
        except Exception as e:
            print(f"Error deleting plan {plan_id}: {e}")
            return False
    
    def get_learning_styles(self) -> Dict[str, Dict[str, Any]]:
        """Get available learning styles"""
        return self.config.LEARNING_STYLES
    
    def get_difficulty_levels(self) -> Dict[str, Dict[str, Any]]:
        """Get available difficulty levels"""
        return self.config.DIFFICULTY_LEVELS
    
    def get_study_subjects(self) -> Dict[str, Dict[str, Any]]:
        """Get available study subjects"""
        return self.config.STUDY_SUBJECTS
    
    def get_plan_templates(self) -> Dict[str, Dict[str, Any]]:
        """Get available plan templates"""
        return self.config.PLAN_TEMPLATES
    
    def get_export_formats(self) -> Dict[str, Dict[str, Any]]:
        """Get available export formats"""
        return self.config.EXPORT_FORMATS
