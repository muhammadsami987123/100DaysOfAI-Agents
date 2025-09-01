import typer
import rich
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.layout import Layout
from rich.live import Live
from rich.align import Align
import json
import os
from datetime import datetime
from typing import Optional, List
import logging

from memory_store import MemoryStore
from ai_service import AIService
from voice_service import VoiceService, VoiceCommandProcessor
from models import MemoryType, MemoryPriority, ExportFormat
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Typer app
app = typer.Typer(
    name="MemoryNotesBot",
    help="🧠 AI-powered personal memory assistant",
    add_completion=False
)

# Rich console
console = Console()

class MemoryNotesBotCLI:
    """CLI interface for MemoryNotesBot"""
    
    def __init__(self):
        self.memory_store = MemoryStore()
        self.ai_service = AIService()
        self.voice_service = VoiceService()
        self.voice_processor = VoiceCommandProcessor(self.memory_store, self.ai_service)
        
        # Ensure directories exist
        Config.create_directories()
    
    def show_welcome(self):
        """Display welcome message"""
        welcome_text = Text()
        welcome_text.append("🧠 ", style="bold blue")
        welcome_text.append("MemoryNotesBot", style="bold white")
        welcome_text.append(" - Your AI Memory Assistant", style="italic white")
        
        console.print(Panel(
            welcome_text,
            title="Welcome",
            border_style="blue",
            padding=(1, 2)
        ))
        
        # Show AI status
        if self.ai_service.is_available():
            console.print("✅ AI Enhancement: Enabled", style="green")
        else:
            console.print("⚠️  AI Enhancement: Disabled (No API key)", style="yellow")
        
        # Show voice status
        voice_status = self.voice_service.get_voice_status()
        if voice_status["tts_available"]:
            console.print("✅ Voice Output: Available", style="green")
        else:
            console.print("⚠️  Voice Output: Unavailable", style="yellow")
        
        console.print()
    
    def show_main_menu(self):
        """Display main menu"""
        menu_options = [
            "1. 💾 Save Memory",
            "2. 🔍 Search Memories", 
            "3. 📋 Show Recent",
            "4. 🏷️  Show by Tag",
            "5. 📊 Statistics",
            "6. 🗑️  Delete Memory",
            "7. 📤 Export Memories",
            "8. 🎤 Voice Interface",
            "9. 🧹 Cleanup",
            "0. ❌ Exit"
        ]
        
        menu_text = "\n".join(menu_options)
        console.print(Panel(menu_text, title="Main Menu", border_style="green"))
    
    def save_memory(self):
        """Interactive memory saving"""
        console.print("\n💾 [bold]Save New Memory[/bold]")
        
        # Get memory content
        content = Prompt.ask("What would you like me to remember?")
        if not content:
            console.print("❌ No content provided", style="red")
            return
        
        # AI enhancement
        if self.ai_service.is_available():
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Enhancing memory with AI...", total=None)
                ai_enhancement = self.ai_service.enhance_memory_content(content)
            
            if ai_enhancement.get("enhanced"):
                suggestions = ai_enhancement["suggestions"]
                console.print("🤖 [bold]AI Suggestions:[/bold]", style="blue")
                console.print(f"   Tags: {', '.join(suggestions.get('tags', []))}")
                console.print(f"   Category: {suggestions.get('category', 'None')}")
                console.print(f"   Priority: {suggestions.get('priority', 'medium')}")
                console.print(f"   Type: {suggestions.get('memory_type', 'long_term')}")
                
                use_ai = Confirm.ask("Use AI suggestions?", default=True)
                if use_ai:
                    tags = suggestions.get("tags", [])
                    category = suggestions.get("category")
                    priority = suggestions.get("priority", "medium")
                    memory_type = suggestions.get("memory_type", "long_term")
                else:
                    tags = []
                    category = None
                    priority = "medium"
                    memory_type = "long_term"
            else:
                tags = []
                category = None
                priority = "medium"
                memory_type = "long_term"
        else:
            # Manual input without AI
            tags_input = Prompt.ask("Tags (comma-separated, optional)")
            tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
            
            category = Prompt.ask("Category (optional)")
            category = category if category else None
            
            priority = Prompt.ask("Priority", choices=["low", "medium", "high", "critical"], default="medium")
            memory_type = Prompt.ask("Memory Type", choices=[t.value for t in MemoryType], default="long_term")
        
        # Additional options
        expires_in = Prompt.ask("Expires in hours (optional, 0 for no expiry)")
        expires_in = int(expires_in) if expires_in and expires_in != "0" else None
        
        # Save memory
        try:
            memory = self.memory_store.add_memory(
                content=content,
                memory_type=memory_type,
                tags=tags,
                category=category,
                priority=priority,
                expires_in_hours=expires_in
            )
            
            console.print(f"✅ [bold]Memory saved successfully![/bold]", style="green")
            console.print(f"   ID: {memory.id[:8]}...")
            console.print(f"   Content: {memory.content}")
            console.print(f"   Type: {memory.memory_type.value}")
            console.print(f"   Priority: {memory.priority.value}")
            if memory.tags:
                console.print(f"   Tags: {', '.join(memory.tags)}")
            if memory.category:
                console.print(f"   Category: {memory.category}")
            if memory.expires_at:
                console.print(f"   Expires: {memory.expires_at.strftime('%Y-%m-%d %H:%M')}")
                
        except Exception as e:
            console.print(f"❌ Error saving memory: {e}", style="red")
    
    def search_memories(self):
        """Interactive memory search"""
        console.print("\n🔍 [bold]Search Memories[/bold]")
        
        query = Prompt.ask("What are you looking for?")
        if not query:
            console.print("❌ No search query provided", style="red")
            return
        
        # AI enhancement
        if self.ai_service.is_available():
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Enhancing search with AI...", total=None)
                search_enhancement = self.ai_service.enhance_search_query(query)
            
            if search_enhancement.get("enhanced"):
                suggestions = search_enhancement["suggestions"]
                console.print("🤖 [bold]AI Search Enhancement:[/bold]", style="blue")
                console.print(f"   Enhanced query: {suggestions.get('enhanced_query', query)}")
                console.print(f"   Related terms: {suggestions.get('related_terms', 'None')}")
                console.print(f"   Strategy: {suggestions.get('search_strategy', 'semantic')}")
        
        # Search filters
        tags_filter = Prompt.ask("Filter by tags (comma-separated, optional)")
        tags = [tag.strip() for tag in tags_filter.split(",")] if tags_filter else None
        
        category_filter = Prompt.ask("Filter by category (optional)")
        category = category_filter if category_filter else None
        
        memory_type_filter = Prompt.ask("Filter by memory type (optional)", choices=["", "short_term", "long_term", "reminder", "password", "idea", "task", "contact", "project"])
        memory_type = MemoryType(memory_type_filter) if memory_type_filter else None
        
        # Perform search
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Searching memories...", total=None)
            results = self.memory_store.search_memories(
                query=query,
                limit=20,
                tags=tags,
                category=category,
                memory_type=memory_type
            )
        
        if results:
            console.print(f"\n✅ Found {len(results)} memories:", style="green")
            
            # Create results table
            table = Table(title="Search Results")
            table.add_column("Rank", style="cyan", no_wrap=True)
            table.add_column("Content", style="white")
            table.add_column("Type", style="magenta")
            table.add_column("Priority", style="yellow")
            table.add_column("Tags", style="blue")
            table.add_column("Relevance", style="green")
            
            for i, result in enumerate(results, 1):
                memory = result.memory
                table.add_row(
                    str(i),
                    memory.content[:60] + "..." if len(memory.content) > 60 else memory.content,
                    memory.memory_type.value,
                    memory.priority.value,
                    ", ".join(memory.tags[:3]) + ("..." if len(memory.tags) > 3 else ""),
                    f"{result.relevance_score:.1f}"
                )
            
            console.print(table)
            
            # Show detailed view option
            if Confirm.ask("Show detailed view of a specific memory?"):
                try:
                    choice = int(Prompt.ask("Enter memory number", choices=[str(i) for i in range(1, len(results) + 1)]))
                    memory = results[choice - 1].memory
                    self.show_memory_details(memory)
                except (ValueError, IndexError):
                    console.print("❌ Invalid selection", style="red")
        else:
            console.print("❌ No memories found matching your search", style="red")
    
    def show_memory_details(self, memory):
        """Display detailed memory information"""
        console.print(f"\n📋 [bold]Memory Details[/bold]")
        
        details_table = Table(show_header=False, box=None)
        details_table.add_column("Field", style="cyan", no_wrap=True)
        details_table.add_column("Value", style="white")
        
        details_table.add_row("ID", memory.id)
        details_table.add_row("Content", memory.content)
        details_table.add_row("Type", memory.memory_type.value)
        details_table.add_row("Priority", memory.priority.value)
        details_table.add_row("Category", memory.category or "None")
        details_table.add_row("Tags", ", ".join(memory.tags) if memory.tags else "None")
        details_table.add_row("Created", memory.created_at.strftime('%Y-%m-%d %H:%M:%S'))
        details_table.add_row("Updated", memory.updated_at.strftime('%Y-%m-%d %H:%M:%S'))
        details_table.add_row("Accessed", memory.accessed_at.strftime('%Y-%m-%d %H:%M:%S') if memory.accessed_at else "Never")
        details_table.add_row("Access Count", str(memory.access_count))
        if memory.expires_at:
            details_table.add_row("Expires", memory.expires_at.strftime('%Y-%m-%d %H:%M:%S'))
        
        console.print(details_table)
        
        # Action options
        actions = ["Edit", "Delete", "Back"]
        action = Prompt.ask("What would you like to do?", choices=actions)
        
        if action == "Edit":
            self.edit_memory(memory)
        elif action == "Delete":
            if Confirm.ask("Are you sure you want to delete this memory?"):
                self.memory_store.delete_memory(memory.id)
                console.print("✅ Memory deleted", style="green")
    
    def edit_memory(self, memory):
        """Edit memory properties"""
        console.print(f"\n✏️  [bold]Edit Memory[/bold]")
        
        # Get new values
        new_content = Prompt.ask("New content", default=memory.content)
        new_tags = Prompt.ask("New tags (comma-separated)", default=", ".join(memory.tags))
        new_category = Prompt.ask("New category", default=memory.category or "")
        new_priority = Prompt.ask("New priority", choices=["low", "medium", "high", "critical"], default=memory.priority.value)
        new_type = Prompt.ask("New memory type", choices=[t.value for t in MemoryType], default=memory.memory_type.value)
        
        # Update memory
        try:
            updated_memory = self.memory_store.update_memory(
                memory.id,
                content=new_content,
                tags=[tag.strip() for tag in new_tags.split(",")] if new_tags else [],
                category=new_category if new_category else None,
                priority=new_priority,
                memory_type=new_type
            )
            
            if updated_memory:
                console.print("✅ Memory updated successfully", style="green")
                self.show_memory_details(updated_memory)
            else:
                console.print("❌ Failed to update memory", style="red")
                
        except Exception as e:
            console.print(f"❌ Error updating memory: {e}", style="red")
    
    def show_recent_memories(self):
        """Display recent memories"""
        console.print("\n📋 [bold]Recent Memories[/bold]")
        
        limit = Prompt.ask("How many recent memories?", default="10")
        try:
            limit = int(limit)
        except ValueError:
            limit = 10
        
        memories = self.memory_store.get_recent_memories(limit)
        
        if memories:
            table = Table(title=f"Recent {len(memories)} Memories")
            table.add_column("Content", style="white")
            table.add_column("Type", style="magenta")
            table.add_column("Priority", style="yellow")
            table.add_column("Created", style="cyan")
            table.add_column("Tags", style="blue")
            
            for memory in memories:
                table.add_row(
                    memory.content[:50] + "..." if len(memory.content) > 50 else memory.content,
                    memory.memory_type.value,
                    memory.priority.value,
                    memory.created_at.strftime('%m-%d %H:%M'),
                    ", ".join(memory.tags[:2]) + ("..." if len(memory.tags) > 2 else "")
                )
            
            console.print(table)
        else:
            console.print("❌ No recent memories found", style="red")
    
    def show_memories_by_tag(self):
        """Display memories by tag"""
        console.print("\n🏷️  [bold]Memories by Tag[/bold]")
        
        tag = Prompt.ask("Enter tag to search for")
        if not tag:
            console.print("❌ No tag provided", style="red")
            return
        
        memories = self.memory_store.get_memories_by_tag(tag)
        
        if memories:
            console.print(f"✅ Found {len(memories)} memories with tag '{tag}':", style="green")
            
            table = Table(title=f"Memories tagged '{tag}'")
            table.add_column("Content", style="white")
            table.add_column("Type", style="magenta")
            table.add_column("Priority", style="yellow")
            table.add_column("Created", style="cyan")
            
            for memory in memories:
                table.add_row(
                    memory.content[:60] + "..." if len(memory.content) > 60 else memory.content,
                    memory.memory_type.value,
                    memory.priority.value,
                    memory.created_at.strftime('%m-%d %H:%M')
                )
            
            console.print(table)
        else:
            console.print(f"❌ No memories found with tag '{tag}'", style="red")
    
    def show_statistics(self):
        """Display memory statistics"""
        console.print("\n📊 [bold]Memory Statistics[/bold]")
        
        stats = self.memory_store.get_stats()
        
        # Create stats table
        stats_table = Table(title="Memory Statistics", show_header=False, box=None)
        stats_table.add_column("Metric", style="cyan", no_wrap=True)
        stats_table.add_column("Value", style="white")
        
        stats_table.add_row("Total Memories", str(stats.total_memories))
        stats_table.add_row("Long-term Memories", str(stats.long_term_count))
        stats_table.add_row("Short-term Memories", str(stats.short_term_count))
        stats_table.add_row("Expired Memories", str(stats.expired_count))
        stats_table.add_row("Total Tags", str(stats.total_tags))
        stats_table.add_row("Storage Size", f"{stats.storage_size_mb} MB")
        
        console.print(stats_table)
        
        # Show most used tags
        if stats.most_used_tags:
            console.print("\n🏷️  [bold]Most Used Tags:[/bold]")
            tag_table = Table()
            tag_table.add_column("Tag", style="blue")
            tag_table.add_column("Count", style="green")
            
            for tag, count in stats.most_used_tags[:10]:
                tag_table.add_row(tag, str(count))
            
            console.print(tag_table)
        
        # Show recent activity
        if stats.recent_activity:
            console.print("\n📝 [bold]Recent Activity:[/bold]")
            activity_table = Table()
            activity_table.add_column("Time", style="cyan")
            activity_table.add_column("Operation", style="yellow")
            activity_table.add_column("Memory ID", style="white")
            
            for activity in stats.recent_activity[:10]:
                activity_table.add_row(
                    activity.timestamp.strftime('%m-%d %H:%M'),
                    activity.operation,
                    activity.memory_id[:8] + "..."
                )
            
            console.print(activity_table)
    
    def delete_memory(self):
        """Interactive memory deletion"""
        console.print("\n🗑️  [bold]Delete Memory[/bold]")
        
        query = Prompt.ask("Search for memory to delete")
        if not query:
            console.print("❌ No search query provided", style="red")
            return
        
        results = self.memory_store.search_memories(query, limit=10)
        
        if results:
            console.print(f"Found {len(results)} matching memories:")
            
            for i, result in enumerate(results, 1):
                memory = result.memory
                console.print(f"{i}. {memory.content[:60]}...")
            
            try:
                choice = int(Prompt.ask("Select memory to delete", choices=[str(i) for i in range(1, len(results) + 1)]))
                memory = results[choice - 1].memory
                
                if Confirm.ask(f"Delete memory: '{memory.content[:50]}...'?"):
                    self.memory_store.delete_memory(memory.id)
                    console.print("✅ Memory deleted successfully", style="green")
                else:
                    console.print("❌ Deletion cancelled", style="yellow")
                    
            except (ValueError, IndexError):
                console.print("❌ Invalid selection", style="red")
        else:
            console.print("❌ No memories found matching your search", style="red")
    
    def export_memories(self):
        """Export memories in various formats"""
        console.print("\n📤 [bold]Export Memories[/bold]")
        
        # Export options
        format_choice = Prompt.ask(
            "Export format",
            choices=["json", "markdown", "csv"],
            default="json"
        )
        
        # Filter options
        use_filters = Confirm.ask("Apply filters to export?", default=False)
        tags_filter = None
        category_filter = None
        
        if use_filters:
            tags_input = Prompt.ask("Filter by tags (comma-separated, optional)")
            tags_filter = [tag.strip() for tag in tags_input.split(",")] if tags_input else None
            
            category_filter = Prompt.ask("Filter by category (optional)")
            category_filter = category_filter if category_filter else None
        
        # Export
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Exporting memories...", total=None)
                export_data = self.memory_store.export_memories(
                    format_type=format_choice,
                    tags=tags_filter,
                    category=category_filter
                )
            
            # Save to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"memories_export_{timestamp}.{format_choice}"
            filepath = os.path.join(Config.EXPORT_DIR, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(export_data)
            
            console.print(f"✅ Memories exported to: {filepath}", style="green")
            
            # Show preview for text formats
            if format_choice in ["markdown", "csv"]:
                if Confirm.ask("Show export preview?"):
                    preview = export_data[:500] + "..." if len(export_data) > 500 else export_data
                    console.print(Panel(preview, title="Export Preview"))
                    
        except Exception as e:
            console.print(f"❌ Error exporting memories: {e}", style="red")
    
    def start_voice_interface(self):
        """Start voice interface"""
        console.print("\n🎤 [bold]Voice Interface[/bold]")
        
        if not Config.ENABLE_VOICE:
            console.print("❌ Voice interface is disabled", style="red")
            return
        
        console.print("Starting voice interface...")
        console.print("Say 'help' for available commands")
        console.print("Press Ctrl+C to stop")
        
        try:
            self.voice_processor.start_voice_interface()
        except KeyboardInterrupt:
            self.voice_processor.stop_voice_interface()
            console.print("\n✅ Voice interface stopped", style="green")
    
    def cleanup_memories(self):
        """Clean up expired and old memories"""
        console.print("\n🧹 [bold]Memory Cleanup[/bold]")
        
        # Get current stats
        stats_before = self.memory_store.get_stats()
        console.print(f"Before cleanup: {stats_before.total_memories} memories")
        
        # Cleanup expired memories
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Cleaning up expired memories...", total=None)
            # This is handled automatically in the memory store
            pass
        
        # Get stats after cleanup
        stats_after = self.memory_store.get_stats()
        console.print(f"After cleanup: {stats_after.total_memories} memories")
        
        cleaned_count = stats_before.total_memories - stats_after.total_memories
        if cleaned_count > 0:
            console.print(f"✅ Cleaned up {cleaned_count} expired memories", style="green")
        else:
            console.print("✅ No cleanup needed", style="green")
    
    def run(self):
        """Main CLI loop"""
        self.show_welcome()
        
        while True:
            try:
                self.show_main_menu()
                choice = Prompt.ask("Select option", choices=[str(i) for i in range(10)])
                
                if choice == "1":
                    self.save_memory()
                elif choice == "2":
                    self.search_memories()
                elif choice == "3":
                    self.show_recent_memories()
                elif choice == "4":
                    self.show_memories_by_tag()
                elif choice == "5":
                    self.show_statistics()
                elif choice == "6":
                    self.delete_memory()
                elif choice == "7":
                    self.export_memories()
                elif choice == "8":
                    self.start_voice_interface()
                elif choice == "9":
                    self.cleanup_memories()
                elif choice == "0":
                    if Confirm.ask("Are you sure you want to exit?"):
                        console.print("👋 Goodbye! Your memories are safely stored.", style="green")
                        break
                
                console.print("\n" + "="*50 + "\n")
                
            except KeyboardInterrupt:
                if Confirm.ask("\nAre you sure you want to exit?"):
                    console.print("👋 Goodbye! Your memories are safely stored.", style="green")
                    break
            except Exception as e:
                console.print(f"❌ An error occurred: {e}", style="red")
                logger.error(f"CLI error: {e}")

@app.command()
def main():
    """Launch MemoryNotesBot CLI"""
    bot = MemoryNotesBotCLI()
    bot.run()

@app.command()
def save(
    content: str = typer.Argument(..., help="Memory content to save"),
    tags: str = typer.Option("", help="Comma-separated tags"),
    category: str = typer.Option("", help="Memory category"),
    priority: str = typer.Option("medium", help="Priority level"),
    memory_type: str = typer.Option("long_term", help="Memory type"),
    expires_in: int = typer.Option(None, help="Expires in hours")
):
    """Save a memory from command line"""
    bot = MemoryNotesBotCLI()
    
    # Parse tags
    tag_list = [tag.strip() for tag in tags.split(",")] if tags else []
    
    # Save memory
    try:
        memory = bot.memory_store.add_memory(
            content=content,
            memory_type=memory_type,
            tags=tag_list,
            category=category if category else None,
            priority=priority,
            expires_in_hours=expires_in
        )
        
        console.print(f"✅ Memory saved: {memory.id[:8]}...", style="green")
        console.print(f"Content: {memory.content}")
        
    except Exception as e:
        console.print(f"❌ Error saving memory: {e}", style="red")
        raise typer.Exit(1)

@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
    limit: int = typer.Option(10, help="Maximum results to return"),
    tags: str = typer.Option("", help="Filter by tags (comma-separated)"),
    category: str = typer.Option("", help="Filter by category")
):
    """Search memories from command line"""
    bot = MemoryNotesBotCLI()
    
    # Parse tags
    tag_list = [tag.strip() for tag in tags.split(",")] if tags else []
    
    # Search memories
    try:
        results = bot.memory_store.search_memories(
            query=query,
            limit=limit,
            tags=tag_list,
            category=category if category else None
        )
        
        if results:
            console.print(f"Found {len(results)} memories:")
            for i, result in enumerate(results, 1):
                memory = result.memory
                console.print(f"{i}. {memory.content}")
        else:
            console.print("No memories found")
            
    except Exception as e:
        console.print(f"❌ Error searching memories: {e}", style="red")
        raise typer.Exit(1)

@app.command()
def stats():
    """Show memory statistics"""
    bot = MemoryNotesBotCLI()
    bot.show_statistics()

if __name__ == "__main__":
    app()
