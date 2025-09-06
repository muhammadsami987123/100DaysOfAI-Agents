"""
Core StoryWriterAgent functionality for AI-powered story generation
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import openai
from openai import OpenAI

from config import StoryConfig

class StoryAgent:
    """Main agent class for story generation and management"""
    
    def __init__(self, api_key: str):
        """Initialize the StoryAgent with OpenAI API key"""
        self.client = OpenAI(api_key=api_key)
        self.config = StoryConfig()
        self.stories_dir = Path(self.config.STORIES_DIR)
        self.favorites_file = Path(self.config.FAVORITES_FILE)
        
        # Create directories if they don't exist
        self.stories_dir.mkdir(exist_ok=True)
        
        # Load favorites
        self.favorites = self._load_favorites()
    
    def generate_story(
        self, 
        prompt: str, 
        genre: str = "fantasy",
        tone: str = "serious", 
        length: str = "medium",
        language: str = "english"
    ) -> Dict[str, Any]:
        """Generate a story based on the given parameters"""
        
        # Validate inputs
        if genre not in self.config.GENRES:
            genre = self.config.DEFAULT_GENRE
        if tone not in self.config.TONES:
            tone = self.config.DEFAULT_TONE
        if length not in self.config.LENGTHS:
            length = self.config.DEFAULT_LENGTH
        if language not in self.config.LANGUAGES:
            language = self.config.DEFAULT_LANGUAGE
        
        # Get configuration values
        genre_info = self.config.GENRES[genre]
        tone_info = self.config.TONES[tone]
        length_info = self.config.LENGTHS[length]
        language_info = self.config.LANGUAGES[language]
        
        # Prepare the prompt
        if language != "english":
            prompt_template = self.config.STORY_PROMPTS["multilingual"]
        else:
            prompt_template = self.config.STORY_PROMPTS["base"]
        
        formatted_prompt = prompt_template.format(
            prompt=prompt,
            genre=genre_info["name"],
            tone=tone_info["name"],
            length=length_info["name"],
            word_count=length_info["words"],
            language=language_info["name"]
        )
        
        try:
            # Generate story using OpenAI
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a creative and skilled storyteller who can write engaging stories in multiple languages and genres."
                    },
                    {
                        "role": "user",
                        "content": formatted_prompt
                    }
                ],
                max_tokens=self.config.MAX_TOKENS,
                temperature=self.config.TEMPERATURE
            )
            
            story_content = response.choices[0].message.content.strip()
            
            # Extract title and content
            title, content = self._extract_title_and_content(story_content)
            
            # Create story data
            story_data = {
                "id": self._generate_story_id(),
                "title": title,
                "content": content,
                "prompt": prompt,
                "genre": genre,
                "tone": tone,
                "length": length,
                "language": language,
                "created_at": datetime.now().isoformat(),
                "word_count": len(content.split()),
                "character_count": len(content)
            }
            
            return story_data
            
        except Exception as e:
            raise Exception(f"Failed to generate story: {str(e)}")
    
    def save_story(self, story_data: Dict[str, Any], format: str = "both") -> Optional[str]:
        """Save story to file(s)"""
        try:
            story_id = story_data["id"]
            title = story_data["title"]
            content = story_data["content"]
            
            # Clean title for filename
            safe_title = re.sub(r'[^\w\s-]', '', title).strip()
            safe_title = re.sub(r'[-\s]+', '-', safe_title)
            
            saved_paths = []
            
            if format in ["txt", "both"]:
                # Save as TXT
                txt_file = self.stories_dir / f"{story_id}_{safe_title}.txt"
                with open(txt_file, 'w', encoding='utf-8') as f:
                    f.write(f"Title: {title}\n")
                    f.write(f"Genre: {story_data['genre']}\n")
                    f.write(f"Tone: {story_data['tone']}\n")
                    f.write(f"Length: {story_data['length']}\n")
                    f.write(f"Language: {story_data['language']}\n")
                    f.write(f"Created: {story_data['created_at']}\n")
                    f.write(f"Word Count: {story_data['word_count']}\n")
                    f.write("-" * 50 + "\n\n")
                    f.write(content)
                saved_paths.append(str(txt_file))
            
            if format in ["md", "both"]:
                # Save as Markdown
                md_file = self.stories_dir / f"{story_id}_{safe_title}.md"
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(f"# {title}\n\n")
                    f.write(f"**Genre:** {story_data['genre']} | **Tone:** {story_data['tone']} | **Length:** {story_data['length']}\n")
                    f.write(f"**Language:** {story_data['language']} | **Created:** {story_data['created_at']}\n")
                    f.write(f"**Word Count:** {story_data['word_count']}\n\n")
                    f.write("---\n\n")
                    f.write(content)
                saved_paths.append(str(md_file))
            
            # Save metadata
            metadata_file = self.stories_dir / f"{story_id}_metadata.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(story_data, f, indent=2, ensure_ascii=False)
            
            return saved_paths[0] if saved_paths else None
            
        except Exception as e:
            print(f"Error saving story: {e}")
            return None
    
    def get_story_list(self) -> List[Dict[str, Any]]:
        """Get list of all saved stories"""
        stories = []
        
        try:
            for metadata_file in self.stories_dir.glob("*_metadata.json"):
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    story_data = json.load(f)
                    stories.append(story_data)
            
            # Sort by creation date (newest first)
            stories.sort(key=lambda x: x.get('created_at', ''), reverse=True)
            return stories
            
        except Exception as e:
            print(f"Error loading stories: {e}")
            return []
    
    def get_story(self, story_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific story by ID"""
        try:
            metadata_file = self.stories_dir / f"{story_id}_metadata.json"
            if metadata_file.exists():
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"Error loading story {story_id}: {e}")
            return None
    
    def add_to_favorites(self, story_id: str) -> bool:
        """Add a story to favorites"""
        try:
            if story_id not in self.favorites:
                self.favorites.append(story_id)
                self._save_favorites()
                return True
            return False
        except Exception as e:
            print(f"Error adding to favorites: {e}")
            return False
    
    def remove_from_favorites(self, story_id: str) -> bool:
        """Remove a story from favorites"""
        try:
            if story_id in self.favorites:
                self.favorites.remove(story_id)
                self._save_favorites()
                return True
            return False
        except Exception as e:
            print(f"Error removing from favorites: {e}")
            return False
    
    def get_favorites(self) -> List[Dict[str, Any]]:
        """Get list of favorite stories"""
        favorite_stories = []
        for story_id in self.favorites:
            story = self.get_story(story_id)
            if story:
                favorite_stories.append(story)
        return favorite_stories
    
    def delete_story(self, story_id: str) -> bool:
        """Delete a story and its files"""
        try:
            # Find and delete all files with this story ID
            deleted_files = []
            for file_path in self.stories_dir.glob(f"{story_id}_*"):
                file_path.unlink()
                deleted_files.append(str(file_path))
            
            # Remove from favorites if present
            if story_id in self.favorites:
                self.favorites.remove(story_id)
                self._save_favorites()
            
            return len(deleted_files) > 0
            
        except Exception as e:
            print(f"Error deleting story {story_id}: {e}")
            return False
    
    def search_stories(self, query: str) -> List[Dict[str, Any]]:
        """Search stories by title, content, or prompt"""
        all_stories = self.get_story_list()
        query_lower = query.lower()
        
        matching_stories = []
        for story in all_stories:
            # Search in title, content, and prompt
            if (query_lower in story.get('title', '').lower() or
                query_lower in story.get('content', '').lower() or
                query_lower in story.get('prompt', '').lower()):
                matching_stories.append(story)
        
        return matching_stories
    
    def get_genres(self) -> Dict[str, Dict[str, str]]:
        """Get available genres"""
        return self.config.GENRES
    
    def get_tones(self) -> Dict[str, Dict[str, str]]:
        """Get available tones"""
        return self.config.TONES
    
    def get_lengths(self) -> Dict[str, Dict[str, Any]]:
        """Get available lengths"""
        return self.config.LENGTHS
    
    def get_languages(self) -> Dict[str, Dict[str, str]]:
        """Get available languages"""
        return self.config.LANGUAGES
    
    def run_terminal(self):
        """Run the enhanced terminal interface"""
        self._print_banner()
        self._print_help()
        
        while True:
            try:
                command = input("\n📚 StoryWriter> ").strip()
                
                if not command:
                    continue
                    
                cmd_parts = command.split()
                cmd = cmd_parts[0].lower()
                
                if cmd in ["quit", "exit", "q"]:
                    self._print_goodbye()
                    break
                elif cmd in ["help", "h", "?"]:
                    self._print_help()
                elif cmd in ["list", "ls", "l"]:
                    self._handle_list_command()
                elif cmd in ["favorites", "fav", "f"]:
                    self._handle_favorites_command()
                elif cmd in ["search", "find", "s"]:
                    self._handle_search_command(cmd_parts[1:] if len(cmd_parts) > 1 else [])
                elif cmd in ["generate", "gen", "g"]:
                    self._handle_generate_command(cmd_parts[1:] if len(cmd_parts) > 1 else [])
                elif cmd in ["stats", "statistics"]:
                    self._handle_stats_command()
                elif cmd in ["clear", "cls"]:
                    self._clear_screen()
                elif cmd in ["examples", "ex", "e"]:
                    self._show_examples()
                elif cmd in ["config", "settings"]:
                    self._show_config()
                else:
                    # Try to generate with the whole command as prompt
                    self._handle_generate_command([command])
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
    
    def _print_banner(self):
        """Print the application banner"""
        print("\n" + "="*60)
        print("📚 StoryWriterAgent - Enhanced Terminal Mode")
        print("="*60)
        print("🎭 AI-Powered Creative Story Generation")
        print("🌍 Multiple Languages • 🎨 Various Genres • 📏 Different Lengths")
        print("="*60)
    
    def _print_help(self):
        """Print enhanced help information"""
        print("\n📋 Available Commands:")
        print("  🎯 generate <prompt>     - Generate a new story")
        print("  📚 list                  - List all your stories")
        print("  🔍 search <query>        - Search through stories")
        print("  ⭐ favorites             - Show favorite stories")
        print("  📊 stats                 - Show writing statistics")
        print("  🎭 examples              - Show example prompts")
        print("  ⚙️  config                - Show current settings")
        print("  🧹 clear                 - Clear the screen")
        print("  ❓ help                  - Show this help")
        print("  🚪 quit                  - Exit the application")
        print("\n💡 Tip: You can also just type your story idea directly!")
    
    def _print_goodbye(self):
        """Print goodbye message"""
        print("\n" + "="*60)
        print("👋 Thank you for using StoryWriterAgent!")
        print("📚 Keep writing and creating amazing stories!")
        print("="*60)
    
    def _clear_screen(self):
        """Clear the terminal screen"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
        self._print_banner()
    
    def _show_examples(self):
        """Show example prompts"""
        examples = [
            ("🐉 Dragon Chef", "A dragon who wanted to become a chef"),
            ("🤖 Robot Love", "A robot learning to love in a post-apocalyptic world"),
            ("🚀 Space Detective", "A detective solving a mystery in space"),
            ("📚 Living Library", "A magical library where books come alive"),
            ("🧙‍♀️ Time Traveler", "A time traveler stuck in the wrong era"),
            ("🎭 Theater Ghost", "A ghost who haunts a theater and helps actors"),
            ("🌊 Ocean Explorer", "An explorer discovering an underwater city"),
            ("🎪 Circus Dreams", "A child who dreams of running away to join the circus")
        ]
        
        print("\n🎭 Example Story Prompts:")
        print("-" * 50)
        for i, (title, prompt) in enumerate(examples, 1):
            print(f"  {i:2d}. {title}")
            print(f"      \"{prompt}\"")
            print()
    
    def _show_config(self):
        """Show current configuration"""
        print("\n⚙️ Current Configuration:")
        print("-" * 40)
        print(f"  📁 Stories Directory: {self.stories_dir}")
        print(f"  📊 Total Stories: {len(self.get_story_list())}")
        print(f"  ⭐ Favorites: {len(self.favorites)}")
        
        print("\n🎭 Available Genres:")
        for key, genre in self.config.GENRES.items():
            print(f"  • {genre['name']} - {genre['description']}")
        
        print("\n🎨 Available Tones:")
        for key, tone in self.config.TONES.items():
            print(f"  • {tone['name']} - {tone['description']}")
        
        print("\n📏 Available Lengths:")
        for key, length in self.config.LENGTHS.items():
            print(f"  • {length['name']} - {length['description']}")
    
    def _handle_list_command(self):
        """Handle list command with enhanced display"""
        stories = self.get_story_list()
        if not stories:
            print("\n📚 No stories found. Generate some first!")
            return
        
        print(f"\n📚 Your Stories ({len(stories)} total):")
        print("-" * 80)
        
        for i, story in enumerate(stories[:15], 1):  # Show first 15
            created = story.get('created_at', '')[:10] if story.get('created_at') else 'Unknown'
            word_count = story.get('word_count', 0)
            
            print(f"  {i:2d}. 📖 {story['title']}")
            print(f"      🎭 {story['genre']} • 🎨 {story['tone']} • 📏 {story['length']}")
            print(f"      📅 {created} • 📊 {word_count} words")
            print(f"      💭 \"{story['prompt'][:60]}{'...' if len(story['prompt']) > 60 else ''}\"")
            print()
        
        if len(stories) > 15:
            print(f"  ... and {len(stories) - 15} more stories")
    
    def _handle_favorites_command(self):
        """Handle favorites command with enhanced display"""
        favorites = self.get_favorites()
        if not favorites:
            print("\n⭐ No favorite stories yet.")
            print("💡 Generate some stories and add them to favorites!")
            return
        
        print(f"\n⭐ Favorite Stories ({len(favorites)}):")
        print("-" * 60)
        
        for i, story in enumerate(favorites, 1):
            created = story.get('created_at', '')[:10] if story.get('created_at') else 'Unknown'
            word_count = story.get('word_count', 0)
            
            print(f"  {i:2d}. ❤️  {story['title']}")
            print(f"      🎭 {story['genre']} • 🎨 {story['tone']} • 📏 {story['length']}")
            print(f"      📅 {created} • 📊 {word_count} words")
            print()
    
    def _handle_search_command(self, query_parts):
        """Handle search command with enhanced display"""
        if not query_parts:
            print("\n❌ Please provide a search query")
            print("💡 Example: search dragon")
            return
        
        query = " ".join(query_parts)
        results = self.search_stories(query)
        
        if not results:
            print(f"\n🔍 No stories found matching '{query}'")
            print("💡 Try different keywords or generate new stories!")
            return
        
        print(f"\n🔍 Search Results for '{query}' ({len(results)} found):")
        print("-" * 70)
        
        for i, story in enumerate(results[:10], 1):  # Show first 10
            created = story.get('created_at', '')[:10] if story.get('created_at') else 'Unknown'
            word_count = story.get('word_count', 0)
            
            print(f"  {i:2d}. 📖 {story['title']}")
            print(f"      🎭 {story['genre']} • 🎨 {story['tone']} • 📏 {story['length']}")
            print(f"      📅 {created} • 📊 {word_count} words")
            print(f"      💭 \"{story['prompt'][:60]}{'...' if len(story['prompt']) > 60 else ''}\"")
            print()
        
        if len(results) > 10:
            print(f"  ... and {len(results) - 10} more results")
    
    def _handle_generate_command(self, prompt_parts):
        """Handle generate command with enhanced display"""
        if not prompt_parts:
            print("\n❌ Please provide a story prompt")
            print("💡 Example: generate A dragon who wanted to become a chef")
            print("💡 Or just type: A dragon who wanted to become a chef")
            return
        
        prompt = " ".join(prompt_parts)
        
        # Interactive story generation
        print(f"\n📝 Generating story for: \"{prompt}\"")
        print("🎭 Choose your story settings (press Enter for defaults):")
        
        # Get genre
        print("\n🎭 Available Genres:")
        for i, (key, genre) in enumerate(self.config.GENRES.items(), 1):
            print(f"  {i}. {genre['name']} - {genre['description']}")
        
        genre_choice = input("\nSelect genre (1-6) or press Enter for Fantasy: ").strip()
        genre = self._get_choice(genre_choice, list(self.config.GENRES.keys()), "fantasy")
        
        # Get tone
        print("\n🎨 Available Tones:")
        for i, (key, tone) in enumerate(self.config.TONES.items(), 1):
            print(f"  {i}. {tone['name']} - {tone['description']}")
        
        tone_choice = input("\nSelect tone (1-4) or press Enter for Serious: ").strip()
        tone = self._get_choice(tone_choice, list(self.config.TONES.keys()), "serious")
        
        # Get length
        print("\n📏 Available Lengths:")
        for i, (key, length) in enumerate(self.config.LENGTHS.items(), 1):
            print(f"  {i}. {length['name']} - {length['description']}")
        
        length_choice = input("\nSelect length (1-3) or press Enter for Medium: ").strip()
        length = self._get_choice(length_choice, list(self.config.LENGTHS.keys()), "medium")
        
        # Get language
        print("\n🌍 Available Languages:")
        for i, (key, language) in enumerate(self.config.LANGUAGES.items(), 1):
            print(f"  {i}. {language['name']} - {language['description']}")
        
        lang_choice = input("\nSelect language (1-6) or press Enter for English: ").strip()
        language = self._get_choice(lang_choice, list(self.config.LANGUAGES.keys()), "english")
        
        # Generate story
        print(f"\n🚀 Generating {self.config.GENRES[genre]['name']} story with {self.config.TONES[tone]['name']} tone...")
        print("⏳ Please wait...")
        
        try:
            story = self.generate_story(prompt, genre, tone, length, language)
            self._display_story(story)
            
            # Ask to save
            save = input("\n💾 Save this story? (y/n): ").strip().lower()
            if save in ['y', 'yes']:
                saved_path = self.save_story(story)
                if saved_path:
                    print(f"✅ Story saved to: {saved_path}")
                
                # Ask to add to favorites
                favorite = input("⭐ Add to favorites? (y/n): ").strip().lower()
                if favorite in ['y', 'yes']:
                    if self.add_to_favorites(story['id']):
                        print("✅ Added to favorites!")
            
        except Exception as e:
            print(f"❌ Error generating story: {e}")
    
    def _get_choice(self, choice, options, default):
        """Get user choice from options"""
        if not choice:
            return default
        
        try:
            index = int(choice) - 1
            if 0 <= index < len(options):
                return options[index]
        except ValueError:
            pass
        
        return default
    
    def _display_story(self, story):
        """Display story with enhanced formatting"""
        print("\n" + "="*80)
        print(f"📚 {story['title']}")
        print("="*80)
        print(f"🎭 Genre: {story['genre']} • 🎨 Tone: {story['tone']} • 📏 Length: {story['length']}")
        print(f"🌍 Language: {story['language']} • 📊 Words: {story['word_count']}")
        print("-"*80)
        print()
        
        # Display story content with word wrapping
        content = story['content']
        words = content.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= 75:
                current_line += (" " + word) if current_line else word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        for line in lines:
            print(f"  {line}")
        
        print()
        print("-"*80)
    
    def _handle_stats_command(self):
        """Handle stats command"""
        stories = self.get_story_list()
        favorites = self.get_favorites()
        
        if not stories:
            print("\n📊 No stories to analyze yet!")
            return
        
        # Calculate statistics
        total_words = sum(story.get('word_count', 0) for story in stories)
        avg_words = total_words // len(stories) if stories else 0
        
        # Genre distribution
        genre_counts = {}
        for story in stories:
            genre = story.get('genre', 'unknown')
            genre_counts[genre] = genre_counts.get(genre, 0) + 1
        
        # Tone distribution
        tone_counts = {}
        for story in stories:
            tone = story.get('tone', 'unknown')
            tone_counts[tone] = tone_counts.get(tone, 0) + 1
        
        print("\n📊 Writing Statistics:")
        print("-" * 50)
        print(f"📚 Total Stories: {len(stories)}")
        print(f"⭐ Favorites: {len(favorites)}")
        print(f"📝 Total Words: {total_words:,}")
        print(f"📊 Average Words per Story: {avg_words:,}")
        
        print("\n🎭 Genre Distribution:")
        for genre, count in sorted(genre_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(stories)) * 100
            print(f"  • {genre.title()}: {count} stories ({percentage:.1f}%)")
        
        print("\n🎨 Tone Distribution:")
        for tone, count in sorted(tone_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(stories)) * 100
            print(f"  • {tone.title()}: {count} stories ({percentage:.1f}%)")
    
    def _extract_title_and_content(self, story_text: str) -> tuple[str, str]:
        """Extract title and content from generated story text"""
        lines = story_text.strip().split('\n')
        
        # Look for title patterns
        title = "Untitled Story"
        content_start = 0
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Check if this looks like a title (short line, possibly with # or similar)
            if (len(line) < 100 and 
                (line.startswith('#') or 
                 (not line.endswith('.') and not line.endswith('!') and not line.endswith('?')))):
                title = line.replace('#', '').strip()
                content_start = i + 1
                break
        
        # Get content (skip empty lines at start)
        content_lines = []
        for line in lines[content_start:]:
            line = line.strip()
            if line or content_lines:  # Include non-empty lines or if we already have content
                content_lines.append(line)
        
        content = '\n'.join(content_lines).strip()
        
        # If no content found, use the whole text as content
        if not content:
            content = story_text.strip()
            title = "Generated Story"
        
        return title, content
    
    def _generate_story_id(self) -> str:
        """Generate a unique story ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"story_{timestamp}"
    
    def _load_favorites(self) -> List[str]:
        """Load favorites from file"""
        try:
            if self.favorites_file.exists():
                with open(self.favorites_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception:
            return []
    
    def _save_favorites(self):
        """Save favorites to file"""
        try:
            with open(self.favorites_file, 'w', encoding='utf-8') as f:
                json.dump(self.favorites, f, indent=2)
        except Exception as e:
            print(f"Error saving favorites: {e}")
