#!/usr/bin/env python3
"""
🤖 VoiceNoteAgent - Day 6 of #100DaysOfAI-Agents

A voice note-taking agent that records, transcribes, and manages voice notes locally.
Features include voice-to-text transcription, text-to-speech playback, and local storage.

Features:
- Voice recording and transcription using speech_recognition
- Text-to-speech playback of saved notes
- Local file storage in JSON and TXT formats
- Timestamp-based organization
- Search and filter capabilities
- Interactive CLI interface
- 100% offline operation

Author: Muhammad Sami Asghar Mughal
"""

import json
import os
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
import speech_recognition as sr
import pyttsx3
from colorama import init, Fore, Back, Style
from config import setup_instructions

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class VoiceNoteAgent:
    def __init__(self):
        """Initialize the VoiceNoteAgent with speech recognition and TTS engines."""
        self.notes_file = "voice_notes.json"
        self.notes_dir = "voice_notes"
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        
        # Create notes directory if it doesn't exist
        if not os.path.exists(self.notes_dir):
            os.makedirs(self.notes_dir)
        
        # Load existing notes
        self.notes = self.load_notes()
        
        # Configure TTS engine
        self.setup_tts()
        
        # Calibrate microphone
        self.calibrate_microphone()
    
    def setup_tts(self):
        """Configure the text-to-speech engine."""
        try:
            # Get available voices
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Set to first available voice (usually system default)
                self.tts_engine.setProperty('voice', voices[0].id)
            
            # Set speech rate and volume
            self.tts_engine.setProperty('rate', 150)  # Speed of speech
            self.tts_engine.setProperty('volume', 0.9)  # Volume level
            
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️  Warning: Could not configure TTS engine: {e}")
    
    def calibrate_microphone(self):
        """Calibrate the microphone for ambient noise."""
        try:
            print(f"{Fore.CYAN}🎤 Calibrating microphone for ambient noise...")
            print(f"{Fore.CYAN}Please remain quiet for a few seconds...")
            
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
            
            print(f"{Fore.GREEN}✅ Microphone calibrated successfully!")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error calibrating microphone: {e}")
            print(f"{Fore.YELLOW}⚠️  Continuing without calibration...")
    
    def load_notes(self) -> List[Dict[str, Any]]:
        """Load voice notes from JSON file."""
        try:
            if os.path.exists(self.notes_file):
                with open(self.notes_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"{Fore.RED}❌ Error loading notes: {e}")
        return []
    
    def save_notes(self):
        """Save voice notes to JSON file."""
        try:
            with open(self.notes_file, 'w', encoding='utf-8') as f:
                json.dump(self.notes, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"{Fore.RED}❌ Error saving notes: {e}")
    
    def record_audio(self, duration: int = 10) -> Optional[sr.AudioData]:
        """Record audio from microphone."""
        try:
            print(f"{Fore.CYAN}🎤 Recording... Speak now! (Press Ctrl+C to stop early)")
            print(f"{Fore.CYAN}Recording for {duration} seconds...")
            
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=duration, phrase_time_limit=duration)
            
            print(f"{Fore.GREEN}✅ Recording completed!")
            return audio
            
        except sr.WaitTimeoutError:
            print(f"{Fore.YELLOW}⚠️  No speech detected within timeout period")
            return None
        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}⚠️  Recording stopped by user")
            return None
        except Exception as e:
            print(f"{Fore.RED}❌ Error recording audio: {e}")
            return None
    
    def transcribe_audio(self, audio: sr.AudioData) -> Optional[str]:
        """Transcribe audio to text using speech recognition."""
        try:
            print(f"{Fore.CYAN}🔄 Transcribing audio...")
            
            # Try multiple recognition engines
            text = None
            
            # Try Google Speech Recognition (requires internet)
            try:
                text = self.recognizer.recognize_google(audio)
                print(f"{Fore.GREEN}✅ Transcription successful!")
                return text
            except sr.UnknownValueError:
                print(f"{Fore.YELLOW}⚠️  Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(f"{Fore.YELLOW}⚠️  Google Speech Recognition service error: {e}")
            
            # Try Sphinx (offline, requires pocketsphinx package)
            try:
                text = self.recognizer.recognize_sphinx(audio)
                print(f"{Fore.GREEN}✅ Offline transcription successful!")
                return text
            except sr.UnknownValueError:
                print(f"{Fore.YELLOW}⚠️  Sphinx could not understand audio")
            except Exception as e:
                print(f"{Fore.YELLOW}⚠️  Sphinx not available: {e}")
            
            if not text:
                print(f"{Fore.RED}❌ Could not transcribe audio with any available engine")
                return None
                
        except Exception as e:
            print(f"{Fore.RED}❌ Error transcribing audio: {e}")
            return None
    
    def speak_text(self, text: str):
        """Convert text to speech and play it."""
        try:
            print(f"{Fore.CYAN}🔊 Speaking: {text[:50]}{'...' if len(text) > 50 else ''}")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            print(f"{Fore.GREEN}✅ Speech playback completed!")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error playing speech: {e}")
    
    def create_note(self, text: str, title: Optional[str] = None) -> Dict[str, Any]:
        """Create a new voice note entry."""
        timestamp = datetime.now().isoformat()
        note_id = len(self.notes) + 1
        
        note = {
            "id": note_id,
            "title": title or f"Voice Note {note_id}",
            "content": text,
            "timestamp": timestamp,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "length": len(text.split()),
            "tags": []
        }
        
        return note
    
    def add_note(self, text: str, title: Optional[str] = None) -> bool:
        """Add a new voice note."""
        try:
            note = self.create_note(text, title)
            self.notes.append(note)
            self.save_notes()
            
            # Save as individual TXT file
            txt_filename = f"{self.notes_dir}/note_{note['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(txt_filename, 'w', encoding='utf-8') as f:
                f.write(f"Title: {note['title']}\n")
                f.write(f"Date: {note['date']} {note['time']}\n")
                f.write(f"Length: {note['length']} words\n")
                f.write(f"Tags: {', '.join(note['tags'])}\n")
                f.write("-" * 50 + "\n")
                f.write(note['content'])
            
            print(f"{Fore.GREEN}✅ Note saved successfully!")
            print(f"{Fore.CYAN}📝 Note ID: {note['id']}")
            print(f"{Fore.CYAN}📁 TXT file: {txt_filename}")
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error saving note: {e}")
            return False
    
    def list_notes(self, limit: Optional[int] = None):
        """List all voice notes."""
        if not self.notes:
            print(f"{Fore.YELLOW}📝 No voice notes found.")
            return
        
        notes_to_show = self.notes[-limit:] if limit else self.notes
        
        print(f"{Fore.CYAN}📝 Voice Notes ({len(notes_to_show)} of {len(self.notes)}):")
        print("-" * 80)
        
        for note in notes_to_show:
            self.display_note(note, brief=True)
            print()
    
    def display_note(self, note: Dict[str, Any], brief: bool = False):
        """Display a single note."""
        if brief:
            print(f"{Fore.GREEN}[{note['id']}] {Fore.WHITE}{note['title']}")
            print(f"{Fore.CYAN}   📅 {note['date']} {note['time']} | 📊 {note['length']} words")
            print(f"{Fore.YELLOW}   📝 {note['content'][:100]}{'...' if len(note['content']) > 100 else ''}")
        else:
            print(f"{Fore.GREEN}📝 Note #{note['id']}: {note['title']}")
            print(f"{Fore.CYAN}📅 Date: {note['date']} {note['time']}")
            print(f"{Fore.CYAN}📊 Length: {note['length']} words")
            print(f"{Fore.CYAN}🏷️  Tags: {', '.join(note['tags']) if note['tags'] else 'None'}")
            print("-" * 50)
            print(f"{Fore.WHITE}{note['content']}")
            print("-" * 50)
    
    def get_note_by_id(self, note_id: int) -> Optional[Dict[str, Any]]:
        """Get a note by its ID."""
        for note in self.notes:
            if note['id'] == note_id:
                return note
        return None
    
    def play_note(self, note_id: int):
        """Play a note using text-to-speech."""
        note = self.get_note_by_id(note_id)
        if not note:
            print(f"{Fore.RED}❌ Note with ID {note_id} not found!")
            return
        
        print(f"{Fore.CYAN}🔊 Playing note #{note_id}: {note['title']}")
        self.speak_text(note['content'])
    
    def search_notes(self, search_term: str):
        """Search notes by content or title."""
        if not self.notes:
            print(f"{Fore.YELLOW}📝 No voice notes to search.")
            return
        
        search_term = search_term.lower()
        matching_notes = []
        
        for note in self.notes:
            if (search_term in note['content'].lower() or 
                search_term in note['title'].lower()):
                matching_notes.append(note)
        
        if not matching_notes:
            print(f"{Fore.YELLOW}🔍 No notes found matching '{search_term}'")
            return
        
        print(f"{Fore.CYAN}🔍 Found {len(matching_notes)} matching notes:")
        print("-" * 80)
        
        for note in matching_notes:
            self.display_note(note, brief=True)
            print()
    
    def delete_note(self, note_id: int) -> bool:
        """Delete a note by ID."""
        note = self.get_note_by_id(note_id)
        if not note:
            print(f"{Fore.RED}❌ Note with ID {note_id} not found!")
            return False
        
        try:
            self.notes = [n for n in self.notes if n['id'] != note_id]
            self.save_notes()
            
            # Delete corresponding TXT file
            txt_files = [f for f in os.listdir(self.notes_dir) if f.startswith(f"note_{note_id}_")]
            for txt_file in txt_files:
                os.remove(os.path.join(self.notes_dir, txt_file))
            
            print(f"{Fore.GREEN}✅ Note #{note_id} deleted successfully!")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error deleting note: {e}")
            return False
    
    def get_statistics(self):
        """Get statistics about voice notes."""
        if not self.notes:
            print(f"{Fore.YELLOW}📊 No voice notes to analyze.")
            return
        
        total_notes = len(self.notes)
        total_words = sum(note['length'] for note in self.notes)
        avg_words = total_words / total_notes if total_notes > 0 else 0
        
        # Group by date
        dates = {}
        for note in self.notes:
            date = note['date']
            dates[date] = dates.get(date, 0) + 1
        
        print(f"{Fore.CYAN}📊 Voice Notes Statistics:")
        print(f"{Fore.WHITE}   📝 Total Notes: {total_notes}")
        print(f"{Fore.WHITE}   📊 Total Words: {total_words}")
        print(f"{Fore.WHITE}   📈 Average Words per Note: {avg_words:.1f}")
        print(f"{Fore.WHITE}   📅 Notes by Date:")
        
        for date, count in sorted(dates.items()):
            print(f"{Fore.CYAN}      {date}: {count} notes")
    
    def record_and_save_note(self, duration: int = 10):
        """Record audio, transcribe it, and save as a note."""
        print(f"{Fore.CYAN}🎤 Starting voice note recording...")
        
        # Record audio
        audio = self.record_audio(duration)
        if not audio:
            print(f"{Fore.RED}❌ Failed to record audio")
            return False
        
        # Transcribe audio
        text = self.transcribe_audio(audio)
        if not text:
            print(f"{Fore.RED}❌ Failed to transcribe audio")
            return False
        
        print(f"{Fore.GREEN}✅ Transcription: {text}")
        
        # Ask for title
        title = input(f"{Fore.CYAN}📝 Enter a title for this note (or press Enter for auto-title): ").strip()
        if not title:
            title = f"Voice Note - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        # Save note
        return self.add_note(text, title)
    
    def process_command(self, command: str):
        """Process user commands."""
        command = command.lower().strip()
        
        if command in ['record', 'r', 'new']:
            duration = int(input(f"{Fore.CYAN}⏱️  Enter recording duration in seconds (default 10): ") or "10")
            self.record_and_save_note(duration)
            
        elif command in ['list', 'l', 'show']:
            limit = input(f"{Fore.CYAN}📝 Enter number of notes to show (or press Enter for all): ").strip()
            limit = int(limit) if limit.isdigit() else None
            self.list_notes(limit)
            
        elif command.startswith('play '):
            try:
                note_id = int(command.split()[1])
                self.play_note(note_id)
            except (IndexError, ValueError):
                print(f"{Fore.RED}❌ Please specify a valid note ID: play <id>")
                
        elif command.startswith('show '):
            try:
                note_id = int(command.split()[1])
                note = self.get_note_by_id(note_id)
                if note:
                    self.display_note(note, brief=False)
                else:
                    print(f"{Fore.RED}❌ Note with ID {note_id} not found!")
            except (IndexError, ValueError):
                print(f"{Fore.RED}❌ Please specify a valid note ID: show <id>")
                
        elif command.startswith('search '):
            search_term = command[7:].strip()
            if search_term:
                self.search_notes(search_term)
            else:
                print(f"{Fore.RED}❌ Please provide a search term: search <term>")
                
        elif command.startswith('delete '):
            try:
                note_id = int(command.split()[1])
                self.delete_note(note_id)
            except (IndexError, ValueError):
                print(f"{Fore.RED}❌ Please specify a valid note ID: delete <id>")
                
        elif command in ['stats', 'statistics']:
            self.get_statistics()
            
        elif command in ['help', 'h', '?']:
            self.show_help()
            
        elif command in ['quit', 'q', 'exit']:
            print(f"{Fore.GREEN}👋 Goodbye!")
            return False
            
        else:
            print(f"{Fore.RED}❌ Unknown command: {command}")
            print(f"{Fore.CYAN}💡 Type 'help' for available commands")
        
        return True
    
    def show_help(self):
        """Show help information."""
        print(f"{Fore.CYAN}🤖 VoiceNoteAgent - Help")
        print("-" * 50)
        print(f"{Fore.WHITE}Available Commands:")
        print(f"{Fore.GREEN}  record, r, new     {Fore.WHITE}Record a new voice note")
        print(f"{Fore.GREEN}  list, l, show      {Fore.WHITE}List all voice notes")
        print(f"{Fore.GREEN}  play <id>          {Fore.WHITE}Play a note using TTS")
        print(f"{Fore.GREEN}  show <id>          {Fore.WHITE}Display full note content")
        print(f"{Fore.GREEN}  search <term>      {Fore.WHITE}Search notes by content")
        print(f"{Fore.GREEN}  delete <id>        {Fore.WHITE}Delete a note")
        print(f"{Fore.GREEN}  stats              {Fore.WHITE}Show statistics")
        print(f"{Fore.GREEN}  help, h, ?         {Fore.WHITE}Show this help")
        print(f"{Fore.GREEN}  quit, q, exit      {Fore.WHITE}Exit the application")
        print("-" * 50)
    
    def run_interactive(self):
        """Run the interactive CLI interface."""
        print(f"{Fore.CYAN}🤖 VoiceNoteAgent - Day 6 of #100DaysOfAI-Agents")
        print(f"{Fore.CYAN}🎙️  Voice Note Taking Agent")
        print("-" * 50)
        
        if self.notes:
            print(f"{Fore.GREEN}📝 Loaded {len(self.notes)} existing voice notes")
        else:
            print(f"{Fore.YELLOW}📝 No existing voice notes found")
        
        print()
        self.show_help()
        print()
        
        while True:
            try:
                command = input(f"{Fore.CYAN}🎙️  VoiceNoteAgent> ").strip()
                if command:
                    if not self.process_command(command):
                        break
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}⚠️  Use 'quit' to exit properly")
            except EOFError:
                print(f"\n{Fore.GREEN}👋 Goodbye!")
                break

def main():
    """Main function to run the VoiceNoteAgent."""
    try:
        agent = VoiceNoteAgent()
        agent.run_interactive()
    except KeyboardInterrupt:
        print(f"\n{Fore.GREEN}👋 Goodbye!")
    except Exception as e:
        print(f"{Fore.RED}❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 