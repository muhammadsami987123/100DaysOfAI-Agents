"""
Local music player for MoodMusicAgent - plays MP3 files from local library
"""
import os
import random
import time
from pathlib import Path
from typing import Dict, List, Optional
import pygame
from config import Config

class LocalPlayer:
    """Local music player using pygame for MP3 playback"""
    
    def __init__(self):
        self.music_path = Path(Config.LOCAL_MUSIC_PATH)
        self.current_track = None
        self.is_playing = False
        self.is_paused = False
        self.volume = Config.DEFAULT_VOLUME
        self.playlist = []
        self.current_index = 0
        
        # Initialize pygame mixer
        try:
            pygame.mixer.init()
            self.mixer_available = True
        except Exception as e:
            print(f"⚠️  Pygame mixer not available: {e}")
            self.mixer_available = False
        
        # Load music library
        self.music_library = self._load_music_library()
    
    def _load_music_library(self) -> Dict[str, List[Dict]]:
        """Load and categorize local music files"""
        if not self.music_path.exists():
            print(f"⚠️  Local music path does not exist: {self.music_path}")
            return {}
        
        music_library = {}
        supported_formats = {'.mp3', '.wav', '.ogg', '.flac'}
        
        print(f"🔍 Scanning music library: {self.music_path}")
        
        for file_path in self.music_path.rglob('*'):
            if file_path.suffix.lower() in supported_formats:
                # Extract metadata from filename
                metadata = self._extract_metadata(file_path)
                
                # Categorize by genre/mood (simple heuristic)
                category = self._categorize_music(metadata)
                
                if category not in music_library:
                    music_library[category] = []
                
                music_library[category].append({
                    "path": str(file_path),
                    "title": metadata["title"],
                    "artist": metadata["artist"],
                    "album": metadata["album"],
                    "duration": metadata["duration"],
                    "category": category
                })
        
        print(f"📚 Loaded {sum(len(tracks) for tracks in music_library.values())} tracks")
        return music_library
    
    def _extract_metadata(self, file_path: Path) -> Dict:
        """Extract basic metadata from filename"""
        filename = file_path.stem
        
        # Try to parse common filename patterns
        # Pattern: "Artist - Title" or "Title - Artist"
        if " - " in filename:
            parts = filename.split(" - ", 1)
            if len(parts) == 2:
                # Try to determine which is artist vs title
                if len(parts[0]) < len(parts[1]):
                    artist, title = parts[0], parts[1]
                else:
                    title, artist = parts[0], parts[1]
            else:
                title, artist = filename, "Unknown Artist"
        else:
            title, artist = filename, "Unknown Artist"
        
        return {
            "title": title.strip(),
            "artist": artist.strip(),
            "album": file_path.parent.name if file_path.parent != self.music_path else "Unknown Album",
            "duration": 0,  # Would need additional library to get actual duration
            "filename": filename
        }
    
    def _categorize_music(self, metadata: Dict) -> str:
        """Categorize music based on metadata and filename"""
        title = metadata["title"].lower()
        artist = metadata["artist"].lower()
        album = metadata["album"].lower()
        
        # Simple keyword-based categorization
        if any(word in title for word in ["workout", "gym", "exercise", "energy", "pump"]):
            return "energetic"
        elif any(word in title for word in ["chill", "relax", "calm", "ambient", "lofi"]):
            return "relaxed"
        elif any(word in title for word in ["love", "romantic", "romance", "heart"]):
            return "romantic"
        elif any(word in title for word in ["sad", "melancholy", "blue", "tears"]):
            return "sad"
        elif any(word in title for word in ["happy", "joy", "sunshine", "smile"]):
            return "happy"
        elif any(word in title for word in ["focus", "study", "concentration", "work"]):
            return "focus"
        elif any(word in title for word in ["motivation", "inspire", "drive", "success"]):
            return "motivated"
        elif any(word in title for word in ["stress", "anxiety", "peace", "zen"]):
            return "stressed"
        else:
            # Default categorization based on artist/genre patterns
            if any(word in artist for word in ["rock", "metal", "punk"]):
                return "energetic"
            elif any(word in artist for word in ["classical", "jazz", "ambient"]):
                return "relaxed"
            else:
                return "happy"  # Default to happy
    
    def search_music(self, mood: str, genres: List[str] = None) -> Optional[Dict]:
        """
        Search for music matching the mood and genres
        
        Args:
            mood: The target mood
            genres: Optional list of preferred genres
            
        Returns:
            Music track data or None
        """
        if not self.music_library:
            return None
        
        # Get tracks for the mood
        mood_tracks = self.music_library.get(mood, [])
        
        if not mood_tracks:
            # Try similar moods
            similar_moods = self._get_similar_moods(mood)
            for similar_mood in similar_moods:
                mood_tracks = self.music_library.get(similar_mood, [])
                if mood_tracks:
                    break
        
        if not mood_tracks:
            # Fallback to any available tracks
            all_tracks = []
            for tracks in self.music_library.values():
                all_tracks.extend(tracks)
            mood_tracks = all_tracks
        
        if not mood_tracks:
            return None
        
        # Select a random track
        selected_track = random.choice(mood_tracks)
        
        return {
            "title": selected_track["title"],
            "artist": selected_track["artist"],
            "album": selected_track["album"],
            "path": selected_track["path"],
            "category": selected_track["category"],
            "source": "local"
        }
    
    def _get_similar_moods(self, mood: str) -> List[str]:
        """Get moods similar to the given mood"""
        mood_config = Config.get_mood_config(mood)
        energy_level = mood_config.get("energy_level", "medium")
        tempo = mood_config.get("tempo", "medium")
        
        similar = []
        for other_mood, other_config in Config.MOOD_CATEGORIES.items():
            if other_mood != mood:
                if (other_config["energy_level"] == energy_level or 
                    other_config["tempo"] == tempo):
                    similar.append(other_mood)
        
        return similar
    
    def play(self, music_data: Dict, volume: float = None) -> bool:
        """
        Play the selected music
        
        Args:
            music_data: Music data from search_music
            volume: Optional volume override
            
        Returns:
            True if playback started successfully
        """
        if not self.mixer_available:
            print("❌ Audio playback not available")
            return False
        
        if not music_data or "path" not in music_data:
            print("❌ Invalid music data")
            return False
        
        try:
            # Stop current playback
            self.stop()
            
            # Set volume
            if volume is not None:
                self.volume = volume
            
            # Load and play the track
            file_path = music_data["path"]
            if not os.path.exists(file_path):
                print(f"❌ File not found: {file_path}")
                return False
            
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play()
            
            self.current_track = music_data
            self.is_playing = True
            self.is_paused = False
            
            print(f"🎵 Playing: {music_data['title']} by {music_data['artist']}")
            return True
            
        except Exception as e:
            print(f"❌ Error playing music: {e}")
            return False
    
    def stop(self) -> bool:
        """Stop music playback"""
        if not self.mixer_available:
            return True
        
        try:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.is_paused = False
            self.current_track = None
            return True
        except Exception as e:
            print(f"❌ Error stopping music: {e}")
            return False
    
    def pause(self) -> bool:
        """Pause music playback"""
        if not self.mixer_available or not self.is_playing:
            return True
        
        try:
            pygame.mixer.music.pause()
            self.is_paused = True
            return True
        except Exception as e:
            print(f"❌ Error pausing music: {e}")
            return False
    
    def resume(self) -> bool:
        """Resume paused music playback"""
        if not self.mixer_available or not self.is_paused:
            return True
        
        try:
            pygame.mixer.music.unpause()
            self.is_paused = False
            return True
        except Exception as e:
            print(f"❌ Error resuming music: {e}")
            return False
    
    def set_volume(self, volume: float) -> bool:
        """Set playback volume (0.0 to 1.0)"""
        if not self.mixer_available:
            return False
        
        if 0.0 <= volume <= 1.0:
            self.volume = volume
            try:
                pygame.mixer.music.set_volume(volume)
                return True
            except Exception as e:
                print(f"❌ Error setting volume: {e}")
                return False
        else:
            print("❌ Volume must be between 0.0 and 1.0")
            return False
    
    def get_playlists(self, mood: str) -> List[Dict]:
        """Get playlist suggestions for a mood"""
        if not self.music_library:
            return []
        
        mood_tracks = self.music_library.get(mood, [])
        if not mood_tracks:
            return []
        
        # Create a simple playlist
        return [{
            "name": f"{mood.title()} Mix",
            "tracks": len(mood_tracks),
            "duration": "Unknown",
            "source": "local"
        }]
    
    def create_playlist(self, mood: str, genres: List[str] = None) -> Optional[Dict]:
        """Create a custom playlist for a mood"""
        tracks = self.search_music(mood, genres)
        if not tracks:
            return None
        
        return {
            "name": f"Custom {mood.title()} Playlist",
            "tracks": [tracks],
            "source": "local",
            "mood": mood
        }
    
    def get_library_stats(self) -> Dict:
        """Get statistics about the music library"""
        if not self.music_library:
            return {"total_tracks": 0, "categories": {}}
        
        total_tracks = sum(len(tracks) for tracks in self.music_library.values())
        categories = {cat: len(tracks) for cat, tracks in self.music_library.items()}
        
        return {
            "total_tracks": total_tracks,
            "categories": categories,
            "music_path": str(self.music_path)
        }
