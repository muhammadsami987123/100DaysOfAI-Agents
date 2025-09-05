"""
Command history and favorites management
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


class CommandHistory:
    """Manages command history and favorites"""
    
    def __init__(self, history_file: str = "command_history.json"):
        self.history_file = Path(history_file)
        self.history = self._load_history()
        self.max_history = 100
    
    def _load_history(self) -> List[Dict[str, Any]]:
        """Load command history from file"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return []
        return []
    
    def _save_history(self) -> None:
        """Save command history to file"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except Exception:
            pass  # Fail silently
    
    def add_command(self, command: str, success: bool = True, execution_time: float = 0.0) -> None:
        """Add a command to history"""
        entry = {
            "command": command,
            "timestamp": datetime.now().isoformat(),
            "success": success,
            "execution_time": execution_time,
            "favorite": False
        }
        
        # Add to beginning of list
        self.history.insert(0, entry)
        
        # Keep only the last max_history entries
        if len(self.history) > self.max_history:
            self.history = self.history[:self.max_history]
        
        self._save_history()
    
    def get_recent_commands(self, limit: int = 10) -> List[str]:
        """Get recent commands"""
        return [entry["command"] for entry in self.history[:limit]]
    
    def get_favorite_commands(self) -> List[Dict[str, Any]]:
        """Get favorite commands"""
        return [entry for entry in self.history if entry.get("favorite", False)]
    
    def toggle_favorite(self, command: str) -> bool:
        """Toggle favorite status for a command"""
        for entry in self.history:
            if entry["command"] == command:
                entry["favorite"] = not entry.get("favorite", False)
                self._save_history()
                return entry["favorite"]
        return False
    
    def get_command_stats(self) -> Dict[str, Any]:
        """Get command usage statistics"""
        if not self.history:
            return {"total": 0, "success_rate": 0, "most_used": []}
        
        total = len(self.history)
        successful = sum(1 for entry in self.history if entry.get("success", False))
        success_rate = (successful / total) * 100 if total > 0 else 0
        
        # Count command usage
        command_counts = {}
        for entry in self.history:
            cmd = entry["command"].split()[0] if entry["command"].startswith("git ") else "other"
            command_counts[cmd] = command_counts.get(cmd, 0) + 1
        
        most_used = sorted(command_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "total": total,
            "success_rate": round(success_rate, 1),
            "most_used": most_used
        }
    
    def search_commands(self, query: str) -> List[Dict[str, Any]]:
        """Search commands by query"""
        query_lower = query.lower()
        results = []
        
        for entry in self.history:
            if query_lower in entry["command"].lower():
                results.append(entry)
        
        return results
    
    def clear_history(self) -> None:
        """Clear all command history"""
        self.history = []
        self._save_history()
    
    def export_history(self, filename: str = None) -> str:
        """Export history to a file"""
        if filename is None:
            filename = f"git_helper_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        export_path = Path(filename)
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, indent=2, ensure_ascii=False)
        
        return str(export_path)
