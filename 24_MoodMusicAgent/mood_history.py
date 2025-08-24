"""
Mood history tracking and analytics for MoodMusicAgent
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path
from config import Config

class MoodHistory:
    """Tracks and analyzes user mood patterns over time"""
    
    def __init__(self):
        self.history_file = Config.MOOD_HISTORY_FILE
        self.history = self._load_history()
        self.max_entries = 1000  # Keep last 1000 entries
    
    def _load_history(self) -> List[Dict]:
        """Load mood history from file"""
        if not self.history_file.exists():
            return []
        
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("entries", [])
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"⚠️  Error loading mood history: {e}")
            return []
    
    def _save_history(self):
        """Save mood history to file"""
        try:
            # Create directory if it doesn't exist
            self.history_file.parent.mkdir(parents=True, exist_ok=True)
            
            data = {
                "last_updated": datetime.now().isoformat(),
                "total_entries": len(self.history),
                "entries": self.history
            }
            
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"❌ Error saving mood history: {e}")
    
    def add_mood_entry(self, mood: str, confidence: float, method: str = "manual", 
                       music_played: Optional[Dict] = None, user_input: str = "") -> bool:
        """
        Add a new mood entry to the history
        
        Args:
            mood: The detected mood
            confidence: Confidence level (0.0 to 1.0)
            method: How the mood was detected
            music_played: Optional music that was played
            user_input: Original user input text
            
        Returns:
            True if entry was added successfully
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "mood": mood,
            "confidence": confidence,
            "method": method,
            "user_input": user_input,
            "music_played": music_played or {},
            "day_of_week": datetime.now().strftime("%A"),
            "hour": datetime.now().hour,
            "date": datetime.now().date().isoformat()
        }
        
        self.history.append(entry)
        
        # Keep only the last max_entries
        if len(self.history) > self.max_entries:
            self.history = self.history[-self.max_entries:]
        
        # Save to file
        self._save_history()
        
        return True
    
    def get_recent_moods(self, hours: int = 24) -> List[Dict]:
        """Get mood entries from the last N hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        recent_moods = []
        for entry in self.history:
            entry_time = datetime.fromisoformat(entry["timestamp"])
            if entry_time >= cutoff_time:
                recent_moods.append(entry)
        
        return recent_moods
    
    def get_mood_by_date(self, date: str) -> List[Dict]:
        """Get all mood entries for a specific date (YYYY-MM-DD)"""
        return [entry for entry in self.history if entry.get("date") == date]
    
    def get_mood_trends(self, days: int = 7) -> Dict[str, Any]:
        """Analyze mood trends over the last N days"""
        cutoff_date = datetime.now().date() - timedelta(days=days)
        
        # Filter entries by date
        recent_entries = []
        for entry in self.history:
            entry_date = datetime.fromisoformat(entry["timestamp"]).date()
            if entry_date >= cutoff_date:
                recent_entries.append(entry)
        
        if not recent_entries:
            return {"message": f"No mood data for the last {days} days"}
        
        # Analyze trends
        mood_counts = {}
        mood_confidence = {}
        hourly_patterns = {}
        daily_patterns = {}
        
        for entry in recent_entries:
            mood = entry["mood"]
            
            # Count moods
            mood_counts[mood] = mood_counts.get(mood, 0) + 1
            
            # Average confidence
            if mood not in mood_confidence:
                mood_confidence[mood] = []
            mood_confidence[mood].append(entry["confidence"])
            
            # Hourly patterns
            hour = entry["hour"]
            if hour not in hourly_patterns:
                hourly_patterns[hour] = []
            hourly_patterns[hour].append(mood)
            
            # Daily patterns
            day = entry["day_of_week"]
            if day not in daily_patterns:
                daily_patterns[day] = []
            daily_patterns[day].append(mood)
        
        # Calculate averages
        mood_confidence_avg = {}
        for mood, confidences in mood_confidence.items():
            mood_confidence_avg[mood] = sum(confidences) / len(confidences)
        
        # Find most common mood
        most_common_mood = max(mood_counts.items(), key=lambda x: x[1]) if mood_counts else ("none", 0)
        
        # Find peak hours for each mood
        mood_peak_hours = {}
        for mood in mood_counts.keys():
            hour_counts = {}
            for hour, moods in hourly_patterns.items():
                hour_counts[hour] = moods.count(mood)
            
            if hour_counts:
                peak_hour = max(hour_counts.items(), key=lambda x: x[1])
                mood_peak_hours[mood] = peak_hour
        
        return {
            "period_days": days,
            "total_entries": len(recent_entries),
            "mood_distribution": mood_counts,
            "most_common_mood": most_common_mood[0],
            "most_common_count": most_common_mood[1],
            "average_confidence_by_mood": mood_confidence_avg,
            "overall_average_confidence": sum(entry["confidence"] for entry in recent_entries) / len(recent_entries),
            "hourly_patterns": hourly_patterns,
            "daily_patterns": daily_patterns,
            "mood_peak_hours": mood_peak_hours,
            "analysis_date": datetime.now().isoformat()
        }
    
    def get_mood_correlations(self) -> Dict[str, Any]:
        """Find correlations between moods and other factors"""
        if len(self.history) < 10:
            return {"message": "Need at least 10 mood entries for correlation analysis"}
        
        # Analyze mood vs time of day
        morning_moods = []  # 6-12
        afternoon_moods = []  # 12-18
        evening_moods = []  # 18-24
        night_moods = []  # 0-6
        
        for entry in self.history:
            hour = entry["hour"]
            if 6 <= hour < 12:
                morning_moods.append(entry["mood"])
            elif 12 <= hour < 18:
                afternoon_moods.append(entry["mood"])
            elif 18 <= hour < 24:
                evening_moods.append(entry["mood"])
            else:
                night_moods.append(entry["mood"])
        
        # Analyze mood vs day of week
        weekday_moods = []
        weekend_moods = []
        
        for entry in self.history:
            day = entry["day_of_week"]
            if day in ["Saturday", "Sunday"]:
                weekend_moods.append(entry["mood"])
            else:
                weekday_moods.append(entry["mood"])
        
        # Find most common moods for each time period
        def get_most_common(mood_list):
            if not mood_list:
                return "none"
            mood_counts = {}
            for mood in mood_list:
                mood_counts[mood] = mood_counts.get(mood, 0) + 1
            return max(mood_counts.items(), key=lambda x: x[1])[0]
        
        return {
            "time_correlations": {
                "morning": get_most_common(morning_moods),
                "afternoon": get_most_common(afternoon_moods),
                "evening": get_most_common(evening_moods),
                "night": get_most_common(night_moods)
            },
            "day_correlations": {
                "weekday": get_most_common(weekday_moods),
                "weekend": get_most_common(weekend_moods)
            },
            "sample_sizes": {
                "morning": len(morning_moods),
                "afternoon": len(afternoon_moods),
                "evening": len(evening_moods),
                "night": len(night_moods),
                "weekday": len(weekday_moods),
                "weekend": len(weekend_moods)
            }
        }
    
    def get_music_preferences(self) -> Dict[str, Any]:
        """Analyze music preferences based on mood"""
        mood_music = {}
        
        for entry in self.history:
            mood = entry["mood"]
            music = entry.get("music_played", {})
            
            if music and "title" in music:
                if mood not in mood_music:
                    mood_music[mood] = []
                mood_music[mood].append({
                    "title": music["title"],
                    "artist": music["artist"],
                    "source": music.get("source", "unknown")
                })
        
        # Find most played music for each mood
        mood_favorites = {}
        for mood, tracks in mood_music.items():
            # Count track occurrences
            track_counts = {}
            for track in tracks:
                track_key = f"{track['title']} - {track['artist']}"
                track_counts[track_key] = track_counts.get(track_key, 0) + 1
            
            if track_counts:
                favorite = max(track_counts.items(), key=lambda x: x[1])
                mood_favorites[mood] = {
                    "track": favorite[0],
                    "play_count": favorite[1],
                    "total_tracks": len(tracks)
                }
        
        return {
            "mood_music_data": mood_music,
            "mood_favorites": mood_favorites,
            "total_music_entries": sum(len(tracks) for tracks in mood_music.values())
        }
    
    def export_history(self, format: str = "json") -> str:
        """Export mood history in specified format"""
        if format.lower() == "json":
            return json.dumps(self.history, indent=2, ensure_ascii=False)
        elif format.lower() == "csv":
            # Simple CSV export
            if not self.history:
                return ""
            
            headers = list(self.history[0].keys())
            csv_lines = [",".join(headers)]
            
            for entry in self.history:
                row = []
                for header in headers:
                    value = entry.get(header, "")
                    # Escape commas and quotes
                    if isinstance(value, str) and ("," in value or '"' in value):
                        escaped_value = value.replace('"', '""')
                        value = f'"{escaped_value}"'
                    row.append(str(value))
                csv_lines.append(",".join(row))
            
            return "\n".join(csv_lines)
        else:
            return f"Unsupported format: {format}"
    
    def clear_history(self) -> bool:
        """Clear all mood history"""
        try:
            self.history = []
            self._save_history()
            return True
        except Exception as e:
            print(f"❌ Error clearing history: {e}")
            return False
    
    def get_stats_summary(self) -> Dict[str, Any]:
        """Get a summary of mood history statistics"""
        if not self.history:
            return {"message": "No mood history available"}
        
        total_entries = len(self.history)
        unique_moods = set(entry["mood"] for entry in self.history)
        
        # Date range
        dates = [datetime.fromisoformat(entry["timestamp"]).date() for entry in self.history]
        date_range = {
            "start": min(dates).isoformat(),
            "end": max(dates).isoformat(),
            "days": (max(dates) - min(dates)).days + 1
        }
        
        # Most recent mood
        most_recent = max(self.history, key=lambda x: x["timestamp"])
        
        return {
            "total_entries": total_entries,
            "unique_moods": list(unique_moods),
            "mood_count": len(unique_moods),
            "date_range": date_range,
            "most_recent_mood": most_recent["mood"],
            "most_recent_time": most_recent["timestamp"],
            "average_confidence": sum(entry["confidence"] for entry in self.history) / total_entries
        }
