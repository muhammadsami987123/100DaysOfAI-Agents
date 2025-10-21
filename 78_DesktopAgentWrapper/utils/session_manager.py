"""
Session management utilities for DesktopAgentWrapper
"""

import os
import json
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

class SessionManager:
    """Manages session data for DesktopAgentWrapper"""
    
    def __init__(self, sessions_dir: str = "sessions"):
        self.sessions_dir = Path(sessions_dir)
        self.sessions_dir.mkdir(exist_ok=True)
        self.current_session = None
    
    def create_session(self, agent_name: str, session_data: Dict[str, Any]) -> str:
        """Create a new session"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_id = f"{agent_name}_{timestamp}"
        
        session_info = {
            "session_id": session_id,
            "agent_name": agent_name,
            "created_at": datetime.now().isoformat(),
            "data": session_data
        }
        
        session_file = self.sessions_dir / f"{session_id}.json"
        
        try:
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session_info, f, indent=2, ensure_ascii=False)
            
            self.current_session = session_id
            return session_id
            
        except Exception as e:
            raise Exception(f"Failed to create session: {str(e)}")
    
    def load_session(self, session_id: str) -> Dict[str, Any]:
        """Load a session by ID"""
        session_file = self.sessions_dir / f"{session_id}.json"
        
        if not session_file.exists():
            raise Exception(f"Session {session_id} not found")
        
        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                session_info = json.load(f)
            
            self.current_session = session_id
            return session_info
            
        except Exception as e:
            raise Exception(f"Failed to load session: {str(e)}")
    
    def save_session(self, session_id: str, session_data: Dict[str, Any]) -> bool:
        """Save session data"""
        session_file = self.sessions_dir / f"{session_id}.json"
        
        if not session_file.exists():
            return False
        
        try:
            # Load existing session
            with open(session_file, 'r', encoding='utf-8') as f:
                session_info = json.load(f)
            
            # Update data
            session_info["data"] = session_data
            session_info["updated_at"] = datetime.now().isoformat()
            
            # Save back
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session_info, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Failed to save session: {e}")
            return False
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        session_file = self.sessions_dir / f"{session_id}.json"
        
        try:
            if session_file.exists():
                session_file.unlink()
                return True
            return False
            
        except Exception as e:
            print(f"Failed to delete session: {e}")
            return False
    
    def list_sessions(self, agent_name: str = None) -> List[Dict[str, Any]]:
        """List available sessions"""
        sessions = []
        
        try:
            for session_file in self.sessions_dir.glob("*.json"):
                with open(session_file, 'r', encoding='utf-8') as f:
                    session_info = json.load(f)
                
                # Filter by agent if specified
                if agent_name and session_info.get("agent_name") != agent_name:
                    continue
                
                sessions.append({
                    "session_id": session_info.get("session_id"),
                    "agent_name": session_info.get("agent_name"),
                    "created_at": session_info.get("created_at"),
                    "updated_at": session_info.get("updated_at"),
                    "file_size": session_file.stat().st_size
                })
            
            # Sort by creation time (newest first)
            sessions.sort(key=lambda x: x.get("created_at", ""), reverse=True)
            
        except Exception as e:
            print(f"Failed to list sessions: {e}")
        
        return sessions
    
    def cleanup_old_sessions(self, days: int = 30) -> int:
        """Clean up sessions older than specified days"""
        cleaned_count = 0
        cutoff_time = time.time() - (days * 24 * 60 * 60)
        
        try:
            for session_file in self.sessions_dir.glob("*.json"):
                if session_file.stat().st_mtime < cutoff_time:
                    session_file.unlink()
                    cleaned_count += 1
                    
        except Exception as e:
            print(f"Failed to cleanup old sessions: {e}")
        
        return cleaned_count
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get session statistics"""
        sessions = self.list_sessions()
        
        total_sessions = len(sessions)
        total_size = sum(session.get("file_size", 0) for session in sessions)
        
        # Group by agent
        agent_counts = {}
        for session in sessions:
            agent_name = session.get("agent_name", "Unknown")
            agent_counts[agent_name] = agent_counts.get(agent_name, 0) + 1
        
        return {
            "total_sessions": total_sessions,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "agent_counts": agent_counts,
            "oldest_session": sessions[-1].get("created_at") if sessions else None,
            "newest_session": sessions[0].get("created_at") if sessions else None
        }
