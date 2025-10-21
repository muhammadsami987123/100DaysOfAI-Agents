"""
Export utilities for DesktopAgentWrapper
"""

import os
import json
import html
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

class ExportManager:
    """Manages export functionality for different formats"""
    
    def __init__(self, exports_dir: str = "exports"):
        self.exports_dir = Path(exports_dir)
        self.exports_dir.mkdir(exist_ok=True)
    
    def export_text(self, content: str, filename: str = None) -> str:
        """Export content as text file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"export_{timestamp}.txt"
        
        filepath = self.exports_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return str(filepath)
        except Exception as e:
            raise Exception(f"Failed to export text: {str(e)}")
    
    def export_json(self, data: Dict[str, Any], filename: str = None) -> str:
        """Export data as JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"export_{timestamp}.json"
        
        filepath = self.exports_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return str(filepath)
        except Exception as e:
            raise Exception(f"Failed to export JSON: {str(e)}")
    
    def export_html(self, content: str, title: str = "Export", filename: str = None) -> str:
        """Export content as HTML file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"export_{timestamp}.html"
        
        filepath = self.exports_dir / filename
        
        # Escape HTML content
        escaped_content = html.escape(content)
        
        # Create HTML template
        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
        }}
        .content {{
            white-space: pre-wrap;
            font-size: 14px;
            color: #555;
        }}
        .metadata {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
            font-size: 12px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <div class="content">{escaped_content}</div>
        <div class="metadata">
            <p><strong>Exported:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Source:</strong> DesktopAgentWrapper</p>
        </div>
    </div>
</body>
</html>
        """
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_template)
            return str(filepath)
        except Exception as e:
            raise Exception(f"Failed to export HTML: {str(e)}")
    
    def export_pdf(self, content: str, title: str = "Export", filename: str = None) -> str:
        """Export content as PDF file"""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
        except ImportError:
            raise Exception("reportlab package required for PDF export. Install with: pip install reportlab")
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"export_{timestamp}.pdf"
        
        filepath = self.exports_dir / filename
        
        try:
            doc = SimpleDocTemplate(str(filepath), pagesize=letter)
            styles = getSampleStyleSheet()
            
            # Create custom style
            custom_style = ParagraphStyle(
                'CustomStyle',
                parent=styles['Normal'],
                fontSize=12,
                leading=14,
                spaceAfter=12
            )
            
            # Build content
            story = []
            
            # Title
            title_para = Paragraph(f"<b>{title}</b>", styles['Title'])
            story.append(title_para)
            story.append(Spacer(1, 12))
            
            # Content
            content_para = Paragraph(content, custom_style)
            story.append(content_para)
            
            # Metadata
            story.append(Spacer(1, 20))
            metadata_para = Paragraph(
                f"<i>Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>",
                styles['Normal']
            )
            story.append(metadata_para)
            
            # Build PDF
            doc.build(story)
            return str(filepath)
            
        except Exception as e:
            raise Exception(f"Failed to export PDF: {str(e)}")
    
    def get_export_formats(self) -> Dict[str, Dict[str, str]]:
        """Get available export formats"""
        return {
            "txt": {
                "name": "Text File",
                "extension": ".txt",
                "description": "Plain text format"
            },
            "json": {
                "name": "JSON File",
                "extension": ".json", 
                "description": "Structured JSON format"
            },
            "html": {
                "name": "HTML File",
                "extension": ".html",
                "description": "HTML format with styling"
            },
            "pdf": {
                "name": "PDF File",
                "extension": ".pdf",
                "description": "PDF document format"
            }
        }
    
    def cleanup_old_exports(self, days: int = 30):
        """Clean up exports older than specified days"""
        try:
            cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)
            
            for file_path in self.exports_dir.iterdir():
                if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
                    file_path.unlink()
                    
        except Exception as e:
            print(f"Warning: Failed to cleanup old exports: {e}")
