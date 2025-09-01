import json
import os
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Tuple
from pathlib import Path
import logging
from models import Memory, MemoryType, MemoryHistory, MemorySearchResult, MemoryStats
from config import Config

logger = logging.getLogger(__name__)

class MemoryStore:
    """Core memory storage and management system"""
    
    def __init__(self, memory_file: str = None, history_file: str = None):
        self.memory_file = memory_file or Config.MEMORY_FILE
        self.history_file = history_file or Config.HISTORY_FILE
        self.memories: Dict[str, Memory] = {}
        self.history: List[MemoryHistory] = []
        self._load_data()
    
    def _load_data(self):
        """Load memories and history from files"""
        try:
            # Load memories
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for memory_data in data:
                        memory = Memory(**memory_data)
                        self.memories[memory.id] = memory
                logger.info(f"Loaded {len(self.memories)} memories from {self.memory_file}")
            
            # Load history
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for history_data in data:
                        history = MemoryHistory(**history_data)
                        self.history.append(history)
                logger.info(f"Loaded {len(self.history)} history entries from {self.history_file}")
                
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            # Create backup of corrupted files
            self._backup_corrupted_files()
    
    def _save_data(self):
        """Save memories and history to files"""
        try:
            # Save memories
            os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                memories_data = [memory.dict() for memory in self.memories.values()]
                json.dump(memories_data, f, indent=2, default=str)
            
            # Save history
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
            with open(self.history_file, 'w', encoding='utf-8') as f:
                history_data = [h.dict() for h in self.history]
                json.dump(history_data, f, indent=2, default=str)
                
        except Exception as e:
            logger.error(f"Error saving data: {e}")
    
    def _backup_corrupted_files(self):
        """Backup corrupted files with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        for file_path in [self.memory_file, self.history_file]:
            if os.path.exists(file_path):
                backup_path = f"{file_path}.backup.{timestamp}"
                try:
                    os.rename(file_path, backup_path)
                    logger.info(f"Backed up corrupted file to {backup_path}")
                except Exception as e:
                    logger.error(f"Failed to backup {file_path}: {e}")
    
    def add_memory(self, content: str, memory_type: MemoryType = MemoryType.LONG_TERM,
                   tags: List[str] = None, category: str = None, 
                   priority: str = "medium", expires_in_hours: int = None) -> Memory:
        """Add a new memory"""
        # Clean up expired memories first
        self._cleanup_expired_memories()
        
        # Check memory limit
        if len(self.memories) >= Config.MAX_MEMORIES:
            self._remove_oldest_memories(100)  # Remove 100 oldest memories
        
        # Create memory
        memory = Memory(
            content=content,
            memory_type=memory_type,
            tags=tags or [],
            category=category,
            priority=priority
        )
        
        if expires_in_hours:
            memory.expires_at = datetime.now() + timedelta(hours=expires_in_hours)
        
        # Store memory
        self.memories[memory.id] = memory
        
        # Add to history
        history_entry = MemoryHistory(
            memory_id=memory.id,
            operation="created",
            user_input=content
        )
        self.history.append(history_entry)
        
        # Save data
        self._save_data()
        
        logger.info(f"Added new memory: {memory.id[:8]}...")
        return memory
    
    def get_memory(self, memory_id: str) -> Optional[Memory]:
        """Get a memory by ID"""
        memory = self.memories.get(memory_id)
        if memory:
            memory.mark_accessed()
            # Add to history
            history_entry = MemoryHistory(
                memory_id=memory_id,
                operation="accessed"
            )
            self.history.append(history_entry)
            self._save_data()
        return memory
    
    def search_memories(self, query: str, limit: int = 10, 
                       tags: List[str] = None, category: str = None,
                       memory_type: MemoryType = None) -> List[MemorySearchResult]:
        """Search memories using semantic and keyword matching"""
        results = []
        query_lower = query.lower()
        
        for memory in self.memories.values():
            # Skip expired memories
            if memory.is_expired():
                continue
            
            # Filter by type if specified
            if memory_type and memory.memory_type != memory_type:
                continue
            
            # Filter by category if specified
            if category and memory.category != category:
                continue
            
            # Filter by tags if specified
            if tags and not any(tag in memory.tags for tag in tags):
                continue
            
            # Calculate relevance score
            relevance_score = 0
            matched_terms = []
            
            # Content matching
            if query_lower in memory.content.lower():
                relevance_score += 3
                matched_terms.append("content")
            
            # Tag matching
            for tag in memory.tags:
                if query_lower in tag.lower():
                    relevance_score += 2
                    matched_terms.append(f"tag:{tag}")
            
            # Category matching
            if memory.category and query_lower in memory.category.lower():
                relevance_score += 1
                matched_terms.append(f"category:{memory.category}")
            
            # Priority boost
            if memory.priority == "critical":
                relevance_score += 1
            elif memory.priority == "high":
                relevance_score += 0.5
            
            # Recency boost
            days_old = (datetime.now() - memory.created_at).days
            if days_old < 7:
                relevance_score += 0.3
            elif days_old < 30:
                relevance_score += 0.1
            
            # Only include if there's some relevance
            if relevance_score > 0:
                results.append(MemorySearchResult(
                    memory=memory,
                    relevance_score=relevance_score,
                    matched_terms=matched_terms
                ))
        
        # Sort by relevance and return top results
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        return results[:limit]
    
    def update_memory(self, memory_id: str, **kwargs) -> Optional[Memory]:
        """Update an existing memory"""
        memory = self.memories.get(memory_id)
        if not memory:
            return None
        
        # Update fields
        for key, value in kwargs.items():
            if hasattr(memory, key):
                setattr(memory, key, value)
        
        memory.updated_at = datetime.now()
        
        # Add to history
        history_entry = MemoryHistory(
            memory_id=memory_id,
            operation="updated",
            details=f"Updated fields: {', '.join(kwargs.keys())}"
        )
        self.history.append(history_entry)
        
        self._save_data()
        return memory
    
    def delete_memory(self, memory_id: str) -> bool:
        """Delete a memory"""
        if memory_id not in self.memories:
            return False
        
        # Add to history before deletion
        history_entry = MemoryHistory(
            memory_id=memory_id,
            operation="deleted",
            details="Memory deleted"
        )
        self.history.append(history_entry)
        
        # Remove from memories
        del self.memories[memory_id]
        
        self._save_data()
        logger.info(f"Deleted memory: {memory_id[:8]}...")
        return True
    
    def delete_memories_by_tag(self, tag: str) -> int:
        """Delete all memories with a specific tag"""
        deleted_count = 0
        memory_ids = [mid for mid, mem in self.memories.items() if tag in mem.tags]
        
        for memory_id in memory_ids:
            if self.delete_memory(memory_id):
                deleted_count += 1
        
        return deleted_count
    
    def get_memories_by_tag(self, tag: str) -> List[Memory]:
        """Get all memories with a specific tag"""
        return [mem for mem in self.memories.values() if tag in mem.tags and not mem.is_expired()]
    
    def get_memories_by_category(self, category: str) -> List[Memory]:
        """Get all memories in a specific category"""
        return [mem for mem in self.memories.values() if mem.category == category and not mem.is_expired()]
    
    def get_recent_memories(self, limit: int = 10) -> List[Memory]:
        """Get recently created memories"""
        memories = [mem for mem in self.memories.values() if not mem.is_expired()]
        memories.sort(key=lambda x: x.created_at, reverse=True)
        return memories[:limit]
    
    def get_frequently_accessed(self, limit: int = 10) -> List[Memory]:
        """Get most frequently accessed memories"""
        memories = [mem for mem in self.memories.values() if not mem.is_expired()]
        memories.sort(key=lambda x: x.access_count, reverse=True)
        return memories[:limit]
    
    def _cleanup_expired_memories(self):
        """Remove expired memories"""
        expired_ids = [mid for mid, mem in self.memories.items() if mem.is_expired()]
        for memory_id in expired_ids:
            self.delete_memory(memory_id)
        
        if expired_ids:
            logger.info(f"Cleaned up {len(expired_ids)} expired memories")
    
    def _remove_oldest_memories(self, count: int):
        """Remove oldest memories to make space"""
        memories = sorted(self.memories.values(), key=lambda x: x.created_at)
        for memory in memories[:count]:
            self.delete_memory(memory.id)
        
        logger.info(f"Removed {count} oldest memories to make space")
    
    def get_stats(self) -> MemoryStats:
        """Get memory statistics"""
        total_memories = len(self.memories)
        short_term_count = len([m for m in self.memories.values() if m.is_short_term()])
        long_term_count = total_memories - short_term_count
        expired_count = len([m for m in self.memories.values() if m.is_expired()])
        
        # Count unique tags
        all_tags = set()
        for memory in self.memories.values():
            all_tags.update(memory.tags)
        total_tags = len(all_tags)
        
        # Most used tags
        tag_counts = {}
        for memory in self.memories.values():
            for tag in memory.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        most_used_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Recent activity
        recent_activity = sorted(self.history, key=lambda x: x.timestamp, reverse=True)[:20]
        
        # Calculate storage size
        storage_size_mb = self._calculate_storage_size()
        
        return MemoryStats(
            total_memories=total_memories,
            short_term_count=short_term_count,
            long_term_count=long_term_count,
            expired_count=expired_count,
            total_tags=total_tags,
            most_used_tags=most_used_tags,
            recent_activity=recent_activity,
            storage_size_mb=storage_size_mb
        )
    
    def _calculate_storage_size(self) -> float:
        """Calculate storage size in MB"""
        try:
            memory_size = os.path.getsize(self.memory_file) if os.path.exists(self.memory_file) else 0
            history_size = os.path.getsize(self.history_file) if os.path.exists(self.history_file) else 0
            total_bytes = memory_size + history_size
            return round(total_bytes / (1024 * 1024), 2)
        except Exception:
            return 0.0
    
    def export_memories(self, format_type: str = "json", 
                       tags: List[str] = None, category: str = None) -> str:
        """Export memories in various formats"""
        memories = list(self.memories.values())
        
        # Apply filters
        if tags:
            memories = [m for m in memories if any(tag in m.tags for tag in tags)]
        if category:
            memories = [m for m in memories if m.category == category]
        
        if format_type == "json":
            return json.dumps([m.dict() for m in memories], indent=2, default=str)
        elif format_type == "markdown":
            return self._export_to_markdown(memories)
        elif format_type == "csv":
            return self._export_to_csv(memories)
        else:
            raise ValueError(f"Unsupported export format: {format_type}")
    
    def _export_to_markdown(self, memories: List[Memory]) -> str:
        """Export memories to Markdown format"""
        md_content = ["# Memory Notes Export\n", f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"]
        
        for memory in memories:
            md_content.append(f"## {memory.content[:50]}...")
            md_content.append(f"- **ID**: {memory.id}")
            md_content.append(f"- **Type**: {memory.memory_type.value}")
            md_content.append(f"- **Priority**: {memory.priority.value}")
            md_content.append(f"- **Created**: {memory.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            if memory.tags:
                md_content.append(f"- **Tags**: {', '.join(memory.tags)}")
            if memory.category:
                md_content.append(f"- **Category**: {memory.category}")
            md_content.append(f"- **Content**: {memory.content}")
            md_content.append("")
        
        return "\n".join(md_content)
    
    def _export_to_csv(self, memories: List[Memory]) -> str:
        """Export memories to CSV format"""
        import csv
        from io import StringIO
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            "ID", "Content", "Type", "Priority", "Tags", "Category", 
            "Created", "Updated", "Access Count"
        ])
        
        # Write data
        for memory in memories:
            writer.writerow([
                memory.id,
                memory.content,
                memory.memory_type.value,
                memory.priority.value,
                ";".join(memory.tags),
                memory.category or "",
                memory.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                memory.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                memory.access_count
            ])
        
        return output.getvalue()
