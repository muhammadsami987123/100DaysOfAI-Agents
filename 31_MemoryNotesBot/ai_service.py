import openai
import logging
from typing import List, Optional, Dict, Any
from models import Memory, MemoryType, MemoryPriority
from config import Config

logger = logging.getLogger(__name__)

class AIService:
    """AI service for intelligent memory processing and enhancement"""
    
    def __init__(self):
        self.client = None
        if Config.OPENAI_API_KEY:
            try:
                self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
                logger.info("OpenAI client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
        else:
            logger.warning("No OpenAI API key provided. AI features will be limited.")
    
    def is_available(self) -> bool:
        """Check if AI service is available"""
        return self.client is not None
    
    def enhance_memory_content(self, content: str) -> Dict[str, Any]:
        """Enhance memory content with AI analysis"""
        if not self.is_available():
            return {"enhanced": False, "reason": "AI service not available"}
        
        try:
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": """You are a memory enhancement assistant. Analyze the given content and provide:
                        1. Suggested tags (as a list of strings)
                        2. Suggested category
                        3. Suggested priority (low, medium, high, critical)
                        4. Suggested memory type (short_term, long_term, reminder, password, idea, task, contact, project)
                        5. Brief summary (max 100 characters)
                        6. Related concepts (as a list of strings)
                        
                        Return as JSON with keys: tags, category, priority, memory_type, summary, related_concepts
                        Example: {"tags": ["work", "project"], "category": "work", "priority": "high", "memory_type": "task", "summary": "Project deadline", "related_concepts": ["deadline", "management"]}"""
                    },
                    {
                        "role": "user",
                        "content": content
                    }
                ],
                max_tokens=300,
                temperature=0.3
            )
            
            # Parse the response
            ai_suggestions = response.choices[0].message.content
            try:
                import json
                suggestions = json.loads(ai_suggestions)
                
                # Ensure tags is a list
                if 'tags' in suggestions:
                    if isinstance(suggestions['tags'], str):
                        suggestions['tags'] = [tag.strip() for tag in suggestions['tags'].split(',') if tag.strip()]
                    elif not isinstance(suggestions['tags'], list):
                        suggestions['tags'] = []
                
                # Ensure related_concepts is a list
                if 'related_concepts' in suggestions:
                    if isinstance(suggestions['related_concepts'], str):
                        suggestions['related_concepts'] = [concept.strip() for concept in suggestions['related_concepts'].split(',') if concept.strip()]
                    elif not isinstance(suggestions['related_concepts'], list):
                        suggestions['related_concepts'] = []
                
                return {
                    "enhanced": True,
                    "suggestions": suggestions
                }
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse AI response: {ai_suggestions}")
                return {"enhanced": False, "reason": "Failed to parse AI response"}
                
        except Exception as e:
            logger.error(f"Error enhancing memory content: {e}")
            return {"enhanced": False, "reason": str(e)}
    
    def categorize_memory(self, content: str) -> Optional[str]:
        """Categorize memory content using AI"""
        if not self.is_available():
            return None
        
        try:
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a memory categorization expert. Given a piece of content, suggest the most appropriate category from: work, personal, project, idea, reminder, contact, technical, creative, health, finance, travel, education, entertainment, other. Return only the category name."
                    },
                    {
                        "role": "user",
                        "content": content
                    }
                ],
                max_tokens=50,
                temperature=0.1
            )
            
            category = response.choices[0].message.content.strip()
            return category if category else None
            
        except Exception as e:
            logger.error(f"Error categorizing memory: {e}")
            return None
    
    def suggest_tags(self, content: str) -> List[str]:
        """Suggest relevant tags for memory content"""
        if not self.is_available():
            return []
        
        try:
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a tagging expert. Given content, suggest 3-5 relevant tags. Return only the tags, comma-separated, no explanations."
                    },
                    {
                        "role": "user",
                        "content": content
                    }
                ],
                max_tokens=100,
                temperature=0.3
            )
            
            tags_text = response.choices[0].message.content.strip()
            tags = [tag.strip() for tag in tags_text.split(",") if tag.strip()]
            return tags
            
        except Exception as e:
            logger.error(f"Error suggesting tags: {e}")
            return []
    
    def determine_priority(self, content: str) -> str:
        """Determine priority level for memory content"""
        if not self.is_available():
            return "medium"
        
        try:
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a priority assessment expert. Given content, determine if it's low, medium, high, or critical priority. Consider urgency, importance, and impact. Return only the priority level."
                    },
                    {
                        "role": "user",
                        "content": content
                    }
                ],
                max_tokens=50,
                temperature=0.1
            )
            
            priority = response.choices[0].message.content.strip().lower()
            valid_priorities = ["low", "medium", "high", "critical"]
            
            if priority in valid_priorities:
                return priority
            else:
                return "medium"
                
        except Exception as e:
            logger.error(f"Error determining priority: {e}")
            return "medium"
    
    def suggest_memory_type(self, content: str) -> str:
        """Suggest the most appropriate memory type"""
        if not self.is_available():
            return "long_term"
        
        try:
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": """You are a memory type expert. Given content, suggest the most appropriate memory type from:
                        - short_term: temporary, expires soon
                        - long_term: permanent, important
                        - reminder: time-sensitive action
                        - password: credentials, secrets
                        - idea: creative thoughts, concepts
                        - task: actionable items
                        - contact: people, organizations
                        - project: work-related, complex
                        
                        Return only the memory type."""
                    },
                    {
                        "role": "user",
                        "content": content
                    }
                ],
                max_tokens=50,
                temperature=0.1
            )
            
            memory_type = response.choices[0].message.content.strip()
            valid_types = [t.value for t in MemoryType]
            
            if memory_type in valid_types:
                return memory_type
            else:
                return "long_term"
                
        except Exception as e:
            logger.error(f"Error suggesting memory type: {e}")
            return "long_term"
    
    def enhance_search_query(self, query: str) -> Dict[str, Any]:
        """Enhance search query with AI suggestions"""
        if not self.is_available():
            return {"enhanced": False, "query": query}
        
        try:
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": """You are a search query enhancement expert. Given a search query, provide:
                        1. Enhanced query (improved version)
                        2. Related terms (comma-separated)
                        3. Suggested filters (tags, categories, time periods)
                        4. Search strategy (exact, semantic, fuzzy)
                        
                        Return as JSON with keys: enhanced_query, related_terms, suggested_filters, search_strategy"""
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ],
                max_tokens=200,
                temperature=0.3
            )
            
            ai_suggestions = response.choices[0].message.content
            try:
                import json
                suggestions = json.loads(ai_suggestions)
                return {
                    "enhanced": True,
                    "query": query,
                    "suggestions": suggestions
                }
            except json.JSONDecodeError:
                return {"enhanced": False, "query": query}
                
        except Exception as e:
            logger.error(f"Error enhancing search query: {e}")
            return {"enhanced": False, "query": query}
    
    def generate_memory_summary(self, memories: List[Memory]) -> str:
        """Generate a summary of multiple memories using AI"""
        if not self.is_available() or not memories:
            return "No memories to summarize"
        
        try:
            # Prepare memory content for AI
            memory_texts = []
            for i, memory in enumerate(memories[:10]):  # Limit to 10 memories
                memory_texts.append(f"{i+1}. {memory.content[:100]}...")
            
            content = "\n".join(memory_texts)
            
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a memory summarization expert. Given a list of memories, provide a concise summary highlighting key themes, patterns, and insights. Keep it under 200 words."
                    },
                    {
                        "role": "user",
                        "content": f"Summarize these memories:\n\n{content}"
                    }
                ],
                max_tokens=300,
                temperature=0.3
            )
            
            summary = response.choices[0].message.content.strip()
            return summary
            
        except Exception as e:
            logger.error(f"Error generating memory summary: {e}")
            return f"Summary of {len(memories)} memories (AI summary unavailable)"
    
    def suggest_related_memories(self, content: str, existing_memories: List[Memory]) -> List[str]:
        """Suggest related memories based on content similarity"""
        if not self.is_available() or not existing_memories:
            return []
        
        try:
            # Get sample of existing memories
            sample_memories = existing_memories[:20]  # Limit to 20 for context
            memory_context = "\n".join([f"- {m.content[:100]}..." for m in sample_memories])
            
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a memory relationship expert. Given new content and existing memories, suggest which existing memories might be related. Return only the IDs of related memories, comma-separated."
                    },
                    {
                        "role": "user",
                        "content": f"New content: {content}\n\nExisting memories:\n{memory_context}\n\nWhich memory IDs are related to the new content?"
                    }
                ],
                max_tokens=100,
                temperature=0.2
            )
            
            related_ids_text = response.choices[0].message.content.strip()
            related_ids = [id.strip() for id in related_ids_text.split(",") if id.strip()]
            
            # Filter to only valid IDs
            valid_ids = [mid for mid in related_ids if any(m.id == mid for m in existing_memories)]
            return valid_ids
            
        except Exception as e:
            logger.error(f"Error suggesting related memories: {e}")
            return []
