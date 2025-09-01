from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum
import uuid

class MemoryType(str, Enum):
    """Types of memories"""
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    REMINDER = "reminder"
    PASSWORD = "password"
    IDEA = "idea"
    TASK = "task"
    CONTACT = "contact"
    PROJECT = "project"

class MemoryPriority(str, Enum):
    """Priority levels for memories"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Memory(BaseModel):
    """Memory entry model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str = Field(..., description="The memory content")
    memory_type: MemoryType = Field(default=MemoryType.LONG_TERM)
    priority: MemoryPriority = Field(default=MemoryPriority.MEDIUM)
    tags: List[str] = Field(default_factory=list)
    category: Optional[str] = Field(default=None, description="Category for grouping")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    accessed_at: Optional[datetime] = Field(default=None)
    access_count: int = Field(default=0)
    expires_at: Optional[datetime] = Field(default=None)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def is_expired(self) -> bool:
        """Check if memory has expired"""
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at
    
    def is_short_term(self) -> bool:
        """Check if this is a short-term memory"""
        return self.memory_type == MemoryType.SHORT_TERM
    
    def mark_accessed(self):
        """Mark memory as accessed"""
        self.accessed_at = datetime.now()
        self.access_count += 1
        self.updated_at = datetime.now()
    
    def add_tag(self, tag: str):
        """Add a tag to the memory"""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now()
    
    def remove_tag(self, tag: str):
        """Remove a tag from the memory"""
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now()

class MemoryHistory(BaseModel):
    """History entry for memory operations"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    memory_id: str
    operation: str  # "created", "updated", "accessed", "deleted"
    timestamp: datetime = Field(default_factory=datetime.now)
    details: Optional[str] = None
    user_input: Optional[str] = None

class MemorySearchResult(BaseModel):
    """Result of a memory search"""
    memory: Memory
    relevance_score: float
    matched_terms: List[str]
    context: Optional[str] = None

class MemoryStats(BaseModel):
    """Statistics about memories"""
    total_memories: int
    short_term_count: int
    long_term_count: int
    expired_count: int
    total_tags: int
    most_used_tags: List[tuple]
    recent_activity: List[MemoryHistory]
    storage_size_mb: float

class ExportFormat(str, Enum):
    """Export formats"""
    MARKDOWN = "markdown"
    PDF = "pdf"
    JSON = "json"
    CSV = "csv"
