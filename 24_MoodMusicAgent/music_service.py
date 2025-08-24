"""
Music service for MoodMusicAgent - handles music selection and playback
"""
import os
import random
import time
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from config import Config

class MusicService:
    """Main music service that coordinates different music sources"""
    
    def __init__(self):
        self.current_track = None
        self.is_playing = False
        self.volume = Config.DEFAULT_VOLUME
        self.music_sources = {}
        self._initialize_music_sources()
    
    def _initialize_music_sources(self):
        """Initialize available music sources"""
        # Initialize Spotify if available
        if Config.is_spotify_available():
            try:
                from spotify_service import SpotifyService
                self.music_sources["spotify"] = SpotifyService()
            except ImportError:
                print("⚠️  Spotify service not available")
        
        # Initialize YouTube if available
        if Config.is_youtube_available():
            try:
                from youtube_service import YouTubeService
                self.music_sources["youtube"] = YouTubeService()
            except ImportError:
                print("⚠️  YouTube service not available")
        
        # Initialize local player
        try:
            from local_player import LocalPlayer
            self.music_sources["local"] = LocalPlayer()
        except ImportError:
            print("⚠️  Local player not available")
        
        if not self.music_sources:
            print("❌ No music sources available!")
    
    def get_music_for_mood(self, mood: str, source: str = "auto") -> Optional[Dict]:
        """
        Get music recommendations for a specific mood
        
        Args:
            mood: The detected mood
            source: Preferred music source ("auto", "spotify", "youtube", "local")
            
        Returns:
            Music recommendation dictionary or None
        """
        mood_config = Config.get_mood_config(mood)
        genres = mood_config.get("genres", [])
        
        # Determine which source to use
        if source == "auto":
            source = self._select_best_source(mood, genres)
        
        if source not in self.music_sources:
            print(f"❌ Music source '{source}' not available")
            return None
        
        try:
            music_service = self.music_sources[source]
            recommendation = music_service.search_music(mood, genres)
            
            if recommendation:
                recommendation["source"] = source
                recommendation["mood"] = mood
                recommendation["mood_config"] = mood_config
                return recommendation
            
        except Exception as e:
            print(f"❌ Error getting music from {source}: {e}")
        
        return None
    
    def _select_best_source(self, mood: str, genres: List[str]) -> str:
        """Select the best music source based on mood and availability"""
        # Priority order for different moods
        mood_source_priorities = {
            "energetic": ["spotify", "youtube", "local"],
            "happy": ["spotify", "youtube", "local"],
            "motivated": ["spotify", "youtube", "local"],
            "romantic": ["spotify", "youtube", "local"],
            "focus": ["local", "spotify", "youtube"],
            "relaxed": ["local", "spotify", "youtube"],
            "sad": ["local", "spotify", "youtube"],
            "stressed": ["local", "spotify", "youtube"]
        }
        
        priorities = mood_source_priorities.get(mood, ["spotify", "youtube", "local"])
        
        for source in priorities:
            if source in self.music_sources:
                return source
        
        # Fallback to first available source
        return list(self.music_sources.keys())[0] if self.music_sources else "local"
    
    def play_music(self, music_data: Dict) -> bool:
        """
        Play the selected music
        
        Args:
            music_data: Music data from get_music_for_mood
            
        Returns:
            True if playback started successfully
        """
        if not music_data:
            return False
        
        source = music_data.get("source", "local")
        if source not in self.music_sources:
            print(f"❌ Music source '{source}' not available")
            return False
        
        try:
            music_service = self.music_sources[source]
            
            # Set volume based on mood
            mood_config = music_data.get("mood_config", {})
            volume_multiplier = mood_config.get("volume_multiplier", 1.0)
            adjusted_volume = self.volume * volume_multiplier
            
            # Start playback
            success = music_service.play(music_data, adjusted_volume)
            
            if success:
                self.current_track = music_data
                self.is_playing = True
                self._display_now_playing(music_data)
                return True
            
        except Exception as e:
            print(f"❌ Error playing music: {e}")
        
        return False
    
    def stop_music(self) -> bool:
        """Stop current music playback"""
        if not self.is_playing:
            return True
        
        try:
            for source, service in self.music_sources.items():
                if hasattr(service, 'stop'):
                    service.stop()
            
            self.is_playing = False
            self.current_track = None
            print("⏹️  Music stopped")
            return True
            
        except Exception as e:
            print(f"❌ Error stopping music: {e}")
            return False
    
    def pause_music(self) -> bool:
        """Pause current music playback"""
        if not self.is_playing:
            return True
        
        try:
            for source, service in self.music_sources.items():
                if hasattr(service, 'pause'):
                    service.pause()
            
            print("⏸️  Music paused")
            return True
            
        except Exception as e:
            print(f"❌ Error pausing music: {e}")
            return False
    
    def resume_music(self) -> bool:
        """Resume paused music playback"""
        if self.is_playing:
            return True
        
        try:
            for source, service in self.music_sources.items():
                if hasattr(service, 'resume'):
                    service.resume()
            
            self.is_playing = True
            print("▶️  Music resumed")
            return True
            
        except Exception as e:
            print(f"❌ Error resuming music: {e}")
            return False
    
    def set_volume(self, volume: float) -> bool:
        """Set music volume (0.0 to 1.0)"""
        if 0.0 <= volume <= 1.0:
            self.volume = volume
            
            # Update volume in all music sources
            for source, service in self.music_sources.items():
                if hasattr(service, 'set_volume'):
                    service.set_volume(volume)
            
            print(f"🔊 Volume set to {int(volume * 100)}%")
            return True
        else:
            print("❌ Volume must be between 0.0 and 1.0")
            return False
    
    def get_playlist_suggestions(self, mood: str) -> List[Dict]:
        """Get playlist suggestions for a mood"""
        suggestions = []
        
        for source, service in self.music_sources.items():
            if hasattr(service, 'get_playlists'):
                try:
                    playlists = service.get_playlists(mood)
                    suggestions.extend(playlists)
                except Exception as e:
                    print(f"⚠️  Error getting playlists from {source}: {e}")
        
        return suggestions
    
    def _display_now_playing(self, music_data: Dict):
        """Display information about currently playing music"""
        title = music_data.get("title", "Unknown")
        artist = music_data.get("artist", "Unknown")
        source = music_data.get("source", "Unknown")
        mood = music_data.get("mood", "Unknown")
        
        print(f"\n🎧 Now playing: \"{title}\" by {artist}")
        print(f"📡 Source: {source.title()}")
        print(f"😊 Mood: {mood.title()}")
        print(f"🔊 Volume: {int(self.volume * 100)}%")
    
    def get_available_sources(self) -> List[str]:
        """Get list of available music sources"""
        return list(self.music_sources.keys())
    
    def get_source_status(self) -> Dict[str, bool]:
        """Get status of all music sources"""
        return {
            "spotify": Config.is_spotify_available(),
            "youtube": Config.is_youtube_available(),
            "local": True  # Local player is always available
        }
    
    def create_mood_playlist(self, mood: str, source: str = "auto") -> Optional[Dict]:
        """Create a custom playlist for a specific mood"""
        mood_config = Config.get_mood_config(mood)
        genres = mood_config.get("genres", [])
        
        if source == "auto":
            source = self._select_best_source(mood, genres)
        
        if source not in self.music_sources:
            return None
        
        try:
            music_service = self.music_sources[source]
            if hasattr(music_service, 'create_playlist'):
                return music_service.create_playlist(mood, genres)
        except Exception as e:
            print(f"❌ Error creating playlist: {e}")
        
        return None
