"""
Theme management utilities for DesktopAgentWrapper
"""

import os
import json
from typing import Dict, Any, Optional
from pathlib import Path

class ThemeManager:
    """Manages themes for DesktopAgentWrapper"""
    
    def __init__(self, themes_dir: str = "themes"):
        self.themes_dir = Path(themes_dir)
        self.themes_dir.mkdir(exist_ok=True)
        self.current_theme = "dark"
        self.custom_themes = {}
        
        # Load custom themes
        self._load_custom_themes()
    
    def _load_custom_themes(self):
        """Load custom themes from files"""
        try:
            for theme_file in self.themes_dir.glob("*.json"):
                with open(theme_file, 'r', encoding='utf-8') as f:
                    theme_data = json.load(f)
                
                theme_name = theme_file.stem
                self.custom_themes[theme_name] = theme_data
                
        except Exception as e:
            print(f"Failed to load custom themes: {e}")
    
    def get_available_themes(self) -> Dict[str, Dict[str, Any]]:
        """Get all available themes"""
        themes = {
            "dark": {
                "name": "Dark Theme",
                "description": "Dark theme with blue accents",
                "colors": {
                    "primary_color": "#3b82f6",
                    "secondary_color": "#1e40af",
                    "background_color": "#0f172a",
                    "surface_color": "#1e293b",
                    "text_color": "#f8fafc",
                    "accent_color": "#f59e0b",
                    "success_color": "#10b981",
                    "error_color": "#ef4444",
                    "warning_color": "#f59e0b"
                }
            },
            "light": {
                "name": "Light Theme",
                "description": "Light theme with blue accents",
                "colors": {
                    "primary_color": "#3b82f6",
                    "secondary_color": "#1e40af",
                    "background_color": "#ffffff",
                    "surface_color": "#f8fafc",
                    "text_color": "#1e293b",
                    "accent_color": "#f59e0b",
                    "success_color": "#10b981",
                    "error_color": "#ef4444",
                    "warning_color": "#f59e0b"
                }
            },
            "purple": {
                "name": "Purple Theme",
                "description": "Purple theme with gradient accents",
                "colors": {
                    "primary_color": "#8b5cf6",
                    "secondary_color": "#7c3aed",
                    "background_color": "#1e1b2e",
                    "surface_color": "#2d1b69",
                    "text_color": "#f8fafc",
                    "accent_color": "#f59e0b",
                    "success_color": "#10b981",
                    "error_color": "#ef4444",
                    "warning_color": "#f59e0b"
                }
            },
            "green": {
                "name": "Green Theme",
                "description": "Green theme with nature colors",
                "colors": {
                    "primary_color": "#10b981",
                    "secondary_color": "#059669",
                    "background_color": "#0f1419",
                    "surface_color": "#1f2937",
                    "text_color": "#f8fafc",
                    "accent_color": "#f59e0b",
                    "success_color": "#10b981",
                    "error_color": "#ef4444",
                    "warning_color": "#f59e0b"
                }
            }
        }
        
        # Add custom themes
        themes.update(self.custom_themes)
        
        return themes
    
    def get_theme_colors(self, theme_name: str) -> Dict[str, str]:
        """Get colors for a specific theme"""
        themes = self.get_available_themes()
        
        if theme_name in themes:
            return themes[theme_name].get("colors", {})
        
        # Fallback to dark theme
        return themes["dark"].get("colors", {})
    
    def set_theme(self, theme_name: str) -> bool:
        """Set the current theme"""
        themes = self.get_available_themes()
        
        if theme_name in themes:
            self.current_theme = theme_name
            return True
        
        return False
    
    def get_current_theme(self) -> str:
        """Get the current theme name"""
        return self.current_theme
    
    def create_custom_theme(self, theme_name: str, theme_data: Dict[str, Any]) -> bool:
        """Create a custom theme"""
        try:
            theme_file = self.themes_dir / f"{theme_name}.json"
            
            with open(theme_file, 'w', encoding='utf-8') as f:
                json.dump(theme_data, f, indent=2, ensure_ascii=False)
            
            # Reload custom themes
            self._load_custom_themes()
            
            return True
            
        except Exception as e:
            print(f"Failed to create custom theme: {e}")
            return False
    
    def delete_custom_theme(self, theme_name: str) -> bool:
        """Delete a custom theme"""
        try:
            theme_file = self.themes_dir / f"{theme_name}.json"
            
            if theme_file.exists():
                theme_file.unlink()
                
                # Remove from custom themes
                if theme_name in self.custom_themes:
                    del self.custom_themes[theme_name]
                
                return True
            
            return False
            
        except Exception as e:
            print(f"Failed to delete custom theme: {e}")
            return False
    
    def export_theme(self, theme_name: str, export_path: str) -> bool:
        """Export a theme to a file"""
        try:
            themes = self.get_available_themes()
            
            if theme_name not in themes:
                return False
            
            theme_data = themes[theme_name]
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(theme_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Failed to export theme: {e}")
            return False
    
    def import_theme(self, import_path: str) -> bool:
        """Import a theme from a file"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                theme_data = json.load(f)
            
            theme_name = theme_data.get("name", "imported_theme")
            theme_file = self.themes_dir / f"{theme_name}.json"
            
            with open(theme_file, 'w', encoding='utf-8') as f:
                json.dump(theme_data, f, indent=2, ensure_ascii=False)
            
            # Reload custom themes
            self._load_custom_themes()
            
            return True
            
        except Exception as e:
            print(f"Failed to import theme: {e}")
            return False
