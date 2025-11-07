"""BookmarkManager Agent - Main agent logic for bookmark management and search"""
from typing import Dict, Any, List, Optional
from utils.llm_service import LLMService
from utils.storage_manager import StorageManager
from config import Config
import json


class BookmarkManagerAgent:
    def __init__(self, llm_service: Optional[LLMService] = None, storage_manager: Optional[StorageManager] = None):
        self.llm_service = llm_service or LLMService()
        self.storage_manager = storage_manager or StorageManager()

    def add_bookmark(self, url: str, title: str, tags: List[str] = None, category: str = None) -> Dict[str, Any]:
        """Add a new bookmark"""
        try:
            bookmark = self.storage_manager.add_bookmark(url, title, tags, category)
            return {
                "success": True,
                "message": f"Bookmark '{title}' added successfully!",
                "bookmark": bookmark
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error adding bookmark: {str(e)}",
                "error": str(e)
            }

    def delete_bookmark(self, bookmark_id: int) -> Dict[str, Any]:
        """Delete a bookmark by ID"""
        try:
            bookmark = self.storage_manager.get_bookmark_by_id(bookmark_id)
            if bookmark:
                self.storage_manager.delete_bookmark(bookmark_id)
                return {
                    "success": True,
                    "message": f"Bookmark '{bookmark['title']}' deleted successfully!"
                }
            else:
                return {
                    "success": False,
                    "message": f"Bookmark with ID {bookmark_id} not found"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error deleting bookmark: {str(e)}",
                "error": str(e)
            }

    def get_all_bookmarks(self) -> Dict[str, Any]:
        """Get all bookmarks"""
        try:
            bookmarks = self.storage_manager.get_all_bookmarks()
            return {
                "success": True,
                "bookmarks": bookmarks,
                "count": len(bookmarks)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error retrieving bookmarks: {str(e)}",
                "error": str(e)
            }

    def search_bookmarks_by_tag(self, tag: str) -> Dict[str, Any]:
        """Search bookmarks by tag"""
        try:
            bookmarks = self.storage_manager.get_bookmarks_by_tag(tag)
            return {
                "success": True,
                "tag": tag,
                "bookmarks": bookmarks,
                "count": len(bookmarks)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error searching by tag: {str(e)}",
                "error": str(e)
            }

    def search_bookmarks_by_category(self, category: str) -> Dict[str, Any]:
        """Search bookmarks by category"""
        try:
            bookmarks = self.storage_manager.get_bookmarks_by_category(category)
            return {
                "success": True,
                "category": category,
                "bookmarks": bookmarks,
                "count": len(bookmarks)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error searching by category: {str(e)}",
                "error": str(e)
            }

    def semantic_search_bookmarks(self, query: str, llm_choice: str = None) -> Dict[str, Any]:
        """Search bookmarks using natural language via LLM"""
        try:
            if llm_choice:
                self.llm_service.set_llm(llm_choice)
            
            # Get all bookmarks first
            all_bookmarks = self.storage_manager.get_all_bookmarks()
            
            if not all_bookmarks:
                return {
                    "success": True,
                    "query": query,
                    "bookmarks": [],
                    "count": 0,
                    "message": "No bookmarks found in database"
                }
            
            # Create context for LLM
            bookmarks_context = json.dumps(all_bookmarks, indent=2)
            
            # Read the search prompt template
            search_prompt_template = self.llm_service._read_template("semantic_search_prompt.txt")
            
            if not search_prompt_template:
                # Fallback to basic search if template not found
                return {
                    "success": True,
                    "query": query,
                    "bookmarks": self.storage_manager.search_bookmarks(query),
                    "method": "basic_search"
                }
            
            # Format the prompt
            formatted_prompt = search_prompt_template.replace("{query}", query)
            formatted_prompt = formatted_prompt.replace("{bookmarks}", bookmarks_context)
            
            # Generate search results using LLM
            llm_response = self.llm_service.generate_content(formatted_prompt)
            
            if not llm_response.get("success"):
                # Fall back to basic search
                return {
                    "success": True,
                    "query": query,
                    "bookmarks": self.storage_manager.search_bookmarks(query),
                    "method": "basic_search"
                }
            
            # Parse LLM response to extract relevant bookmark IDs
            response_text = llm_response.get("content", "")
            
            try:
                # Try to extract JSON from response
                json_start = response_text.find('[')
                json_end = response_text.rfind(']') + 1
                
                if json_start >= 0 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    relevant_ids = json.loads(json_str)
                else:
                    # Fallback to basic search
                    return {
                        "success": True,
                        "query": query,
                        "bookmarks": self.storage_manager.search_bookmarks(query),
                        "method": "basic_search"
                    }
            except json.JSONDecodeError:
                # Fallback to basic search
                return {
                    "success": True,
                    "query": query,
                    "bookmarks": self.storage_manager.search_bookmarks(query),
                    "method": "basic_search"
                }
            
            # Collect bookmarks based on IDs
            result_bookmarks = []
            for bookmark_id in relevant_ids:
                bookmark = self.storage_manager.get_bookmark_by_id(bookmark_id)
                if bookmark:
                    result_bookmarks.append(bookmark)
            
            return {
                "success": True,
                "query": query,
                "bookmarks": result_bookmarks,
                "count": len(result_bookmarks),
                "method": "semantic_search"
            }
        
        except Exception as e:
            return {
                "success": False,
                "query": query,
                "message": f"Error in semantic search: {str(e)}",
                "error": str(e)
            }

    def get_all_tags(self) -> Dict[str, Any]:
        """Get all unique tags"""
        try:
            tags = self.storage_manager.get_all_tags()
            return {
                "success": True,
                "tags": tags,
                "count": len(tags)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error retrieving tags: {str(e)}",
                "error": str(e)
            }

    def get_all_categories(self) -> Dict[str, Any]:
        """Get all unique categories"""
        try:
            categories = self.storage_manager.get_all_categories()
            return {
                "success": True,
                "categories": categories,
                "count": len(categories)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error retrieving categories: {str(e)}",
                "error": str(e)
            }

    def delete_bookmarks_by_tag(self, tag: str) -> Dict[str, Any]:
        """Delete all bookmarks with a specific tag"""
        try:
            count = self.storage_manager.delete_bookmarks_by_tag(tag)
            return {
                "success": True,
                "message": f"Deleted {count} bookmark(s) with tag '{tag}'",
                "deleted_count": count
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error deleting bookmarks by tag: {str(e)}",
                "error": str(e)
            }

    def export_bookmarks(self) -> Dict[str, Any]:
        """Export all bookmarks as JSON"""
        try:
            bookmarks_data = self.storage_manager.export_bookmarks()
            return {
                "success": True,
                "data": bookmarks_data
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error exporting bookmarks: {str(e)}",
                "error": str(e)
            }

    def import_bookmarks(self, import_data: Dict[str, Any]) -> Dict[str, Any]:
        """Import bookmarks from JSON"""
        try:
            success = self.storage_manager.import_bookmarks(import_data)
            if success:
                return {
                    "success": True,
                    "message": "Bookmarks imported successfully!"
                }
            else:
                return {
                    "success": False,
                    "message": "Invalid bookmark data format"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error importing bookmarks: {str(e)}",
                "error": str(e)
            }

    def get_bookmark_stats(self) -> Dict[str, Any]:
        """Get statistics about bookmarks"""
        try:
            bookmarks = self.storage_manager.get_all_bookmarks()
            tags = self.storage_manager.get_all_tags()
            categories = self.storage_manager.get_all_categories()
            
            return {
                "success": True,
                "total_bookmarks": len(bookmarks),
                "total_tags": len(tags),
                "total_categories": len(categories),
                "tags": tags,
                "categories": categories
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error retrieving statistics: {str(e)}",
                "error": str(e)
            }

