"""
Mood detection and analysis for MoodMusicAgent
"""
import re
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from textblob import TextBlob
import nltk
from config import Config

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

from nltk.sentiment.vader import SentimentIntensityAnalyzer

class MoodDetector:
    """Detects and analyzes user mood from text input"""
    
    def __init__(self):
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.mood_keywords = {
            "happy": ["happy", "joy", "excited", "cheerful", "delighted", "pleased", "content", "glad"],
            "sad": ["sad", "depressed", "melancholy", "gloomy", "sorrow", "grief", "unhappy", "miserable"],
            "energetic": ["energetic", "energized", "pumped", "motivated", "enthusiastic", "vibrant", "lively"],
            "relaxed": ["relaxed", "calm", "peaceful", "serene", "tranquil", "chill", "laid-back", "easygoing"],
            "romantic": ["romantic", "loving", "passionate", "intimate", "tender", "affectionate", "sweet"],
            "stressed": ["stressed", "anxious", "worried", "tense", "overwhelmed", "frustrated", "nervous"],
            "motivated": ["motivated", "inspired", "determined", "focused", "driven", "ambitious", "goal-oriented"],
            "focus": ["focused", "concentrated", "attentive", "mindful", "studious", "productive", "alert"]
        }
        
        # Mood intensity modifiers
        self.intensity_modifiers = {
            "very": 2.0,
            "really": 1.8,
            "extremely": 2.2,
            "super": 1.5,
            "kinda": 0.7,
            "sorta": 0.6,
            "a bit": 0.5,
            "slightly": 0.4
        }
    
    def detect_mood(self, text: str) -> Dict[str, any]:
        """
        Analyze text input and detect the user's mood
        
        Args:
            text: User input text
            
        Returns:
            Dictionary containing mood analysis results
        """
        if not text or not text.strip():
            return {"mood": "neutral", "confidence": 0.0, "description": "No text provided"}
        
        text = text.lower().strip()
        
        # Method 1: Direct mood matching
        direct_mood = self._direct_mood_match(text)
        if direct_mood:
            return direct_mood
        
        # Method 2: Keyword-based mood detection
        keyword_mood = self._keyword_based_detection(text)
        if keyword_mood:
            return keyword_mood
        
        # Method 3: Sentiment analysis
        sentiment_mood = self._sentiment_analysis(text)
        if sentiment_mood:
            return sentiment_mood
        
        # Method 4: Context-based inference
        context_mood = self._context_based_inference(text)
        if context_mood:
            return context_mood
        
        # Default to neutral
        return {
            "mood": "neutral",
            "confidence": 0.3,
            "description": "Unable to determine mood from text",
            "analysis": "neutral"
        }
    
    def _direct_mood_match(self, text: str) -> Optional[Dict[str, any]]:
        """Check if text directly mentions a mood category"""
        for mood, keywords in self.mood_keywords.items():
            if mood in text:
                confidence = 0.9
                description = Config.get_mood_config(mood)["description"]
                return {
                    "mood": mood,
                    "confidence": confidence,
                    "description": description,
                    "method": "direct_match"
                }
        return None
    
    def _keyword_based_detection(self, text: str) -> Optional[Dict[str, any]]:
        """Detect mood based on keyword analysis"""
        mood_scores = {}
        
        for mood, keywords in self.mood_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in text:
                    score += 1
                    # Check for intensity modifiers
                    for modifier, multiplier in self.intensity_modifiers.items():
                        if f"{modifier} {keyword}" in text:
                            score *= multiplier
            
            if score > 0:
                mood_scores[mood] = score
        
        if not mood_scores:
            return None
        
        # Find the mood with highest score
        best_mood = max(mood_scores, key=mood_scores.get)
        best_score = mood_scores[best_mood]
        
        # Normalize confidence (0.0 to 1.0)
        confidence = min(best_score / 3.0, 1.0)
        description = Config.get_mood_config(best_mood)["description"]
        
        return {
            "mood": best_mood,
            "confidence": confidence,
            "description": description,
            "method": "keyword_analysis",
            "scores": mood_scores
        }
    
    def _sentiment_analysis(self, text: str) -> Optional[Dict[str, any]]:
        """Use NLTK sentiment analysis to determine mood"""
        try:
            # TextBlob sentiment
            blob = TextBlob(text)
            blob_polarity = blob.sentiment.polarity
            
            # VADER sentiment
            vader_scores = self.sentiment_analyzer.polarity_scores(text)
            
            # Combine both analyses
            combined_polarity = (blob_polarity + vader_scores['compound']) / 2
            
            # Map polarity to mood
            if combined_polarity > 0.3:
                mood = "happy"
                description = "Feeling positive and upbeat"
            elif combined_polarity > 0.1:
                mood = "relaxed"
                description = "Feeling calm and content"
            elif combined_polarity < -0.3:
                mood = "sad"
                description = "Feeling down or melancholic"
            elif combined_polarity < -0.1:
                mood = "stressed"
                description = "Feeling tense or anxious"
            else:
                mood = "neutral"
                description = "Feeling neutral or balanced"
            
            confidence = abs(combined_polarity) * 0.8 + 0.2  # Base confidence of 0.2
            
            return {
                "mood": mood,
                "confidence": confidence,
                "description": description,
                "method": "sentiment_analysis",
                "polarity": combined_polarity,
                "vader_scores": vader_scores
            }
            
        except Exception as e:
            return None
    
    def _context_based_inference(self, text: str) -> Optional[Dict[str, any]]:
        """Infer mood from context and common phrases"""
        context_patterns = {
            "workout": ("energetic", "High energy for workout"),
            "study": ("focus", "Time to concentrate"),
            "party": ("happy", "Party mood activated"),
            "sleep": ("relaxed", "Time to wind down"),
            "date": ("romantic", "Romantic evening ahead"),
            "deadline": ("stressed", "Under pressure"),
            "achievement": ("motivated", "Feeling accomplished"),
            "morning": ("motivated", "Fresh start of the day"),
            "evening": ("relaxed", "Evening relaxation time")
        }
        
        for pattern, (mood, description) in context_patterns.items():
            if pattern in text:
                return {
                    "mood": mood,
                    "confidence": 0.6,
                    "description": description,
                    "method": "context_inference"
                }
        
        return None
    
    def get_mood_suggestions(self, text: str = "") -> List[str]:
        """Get suggested mood categories based on input"""
        if text:
            detected = self.detect_mood(text)
            if detected["confidence"] > 0.5:
                # Return similar moods
                mood = detected["mood"]
                similar_moods = self._get_similar_moods(mood)
                return [mood] + similar_moods[:2]
        
        # Return all available moods
        return list(Config.MOOD_CATEGORIES.keys())
    
    def _get_similar_moods(self, mood: str) -> List[str]:
        """Get moods similar to the given mood"""
        mood_config = Config.get_mood_config(mood)
        energy_level = mood_config["energy_level"]
        tempo = mood_config["tempo"]
        
        similar = []
        for other_mood, other_config in Config.MOOD_CATEGORIES.items():
            if other_mood != mood:
                if (other_config["energy_level"] == energy_level or 
                    other_config["tempo"] == tempo):
                    similar.append(other_mood)
        
        return similar
    
    def analyze_mood_trends(self, mood_history: List[Dict]) -> Dict[str, any]:
        """Analyze mood patterns over time"""
        if not mood_history:
            return {"message": "No mood history available"}
        
        # Count mood frequencies
        mood_counts = {}
        for entry in mood_history:
            mood = entry.get("mood", "unknown")
            mood_counts[mood] = mood_counts.get(mood, 0) + 1
        
        # Find most common mood
        most_common = max(mood_counts.items(), key=lambda x: x[1]) if mood_counts else ("unknown", 0)
        
        # Calculate average confidence
        avg_confidence = sum(entry.get("confidence", 0) for entry in mood_history) / len(mood_history)
        
        return {
            "total_entries": len(mood_history),
            "most_common_mood": most_common[0],
            "most_common_count": most_common[1],
            "average_confidence": avg_confidence,
            "mood_distribution": mood_counts,
            "analysis_date": datetime.now().isoformat()
        }
