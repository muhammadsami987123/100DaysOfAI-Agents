"""Storage Manager for Bookmarks - Handles JSON-based bookmark storage"""
import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from config import Config


class StorageManager:
    def __init__(self):
        self.bookmarks_file = Config.BOOKMARKS_FILE
        self.ensure_storage_exists()

    def ensure_storage_exists(self):
        """Ensure the storage file exists with proper structure"""
        if not os.path.exists(self.bookmarks_file):
            self._save_bookmarks({"bookmarks": [], "tags": {}})

    def _load_bookmarks(self) -> Dict[str, Any]:
        """Load bookmarks from JSON file"""
        try:
            with open(self.bookmarks_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except (json.JSONDecodeError, FileNotFoundError):
            return {"bookmarks": [], "tags": {}}

    def _save_bookmarks(self, data: Dict[str, Any]):
        """Save bookmarks to JSON file"""
        os.makedirs(os.path.dirname(self.bookmarks_file), exist_ok=True)
        with open(self.bookmarks_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add_bookmark(self, url: str, title: str, tags: List[str] = None, category: str = None) -> Dict[str, Any]:
        """Add a new bookmark"""
        data = self._load_bookmarks()
        
        # Generate unique ID
        bookmark_id = len(data["bookmarks"]) + 1
        
        bookmark = {
            "id": bookmark_id,
            "url": url,
            "title": title,
            "tags": tags or [],
            "category": category or "uncategorized",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        data["bookmarks"].append(bookmark)
        
        # Update tags index
        for tag in (tags or []):
            if tag not in data["tags"]:
                data["tags"][tag] = []
            data["tags"][tag].append(bookmark_id)
        
        self._save_bookmarks(data)
        return bookmark

    def get_all_bookmarks(self) -> List[Dict[str, Any]]:
        """Get all bookmarks"""
        data = self._load_bookmarks()
        return data.get("bookmarks", [])

    def get_bookmark_by_id(self, bookmark_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific bookmark by ID"""
        bookmarks = self.get_all_bookmarks()
        for bookmark in bookmarks:
            if bookmark["id"] == bookmark_id:
                return bookmark
        return None

    def get_bookmarks_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        """Get all bookmarks with a specific tag"""
        bookmarks = self.get_all_bookmarks()
        return [b for b in bookmarks if tag.lower() in [t.lower() for t in b.get("tags", [])]]

    def get_bookmarks_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all bookmarks in a specific category"""
        bookmarks = self.get_all_bookmarks()
        return [b for b in bookmarks if b.get("category", "").lower() == category.lower()]

    def search_bookmarks(self, query: str) -> List[Dict[str, Any]]:
        """Search bookmarks by title or URL (basic search)"""
        bookmarks = self.get_all_bookmarks()
        query_lower = query.lower()
        results = []
        
        for bookmark in bookmarks:
            if (query_lower in bookmark.get("title", "").lower() or 
                query_lower in bookmark.get("url", "").lower()):
                results.append(bookmark)
        
        return results

    def delete_bookmark(self, bookmark_id: int) -> bool:
        """Delete a bookmark"""
        data = self._load_bookmarks()
        bookmarks = data.get("bookmarks", [])
        
        # Find and remove the bookmark
        bookmark_to_delete = None
        for i, bookmark in enumerate(bookmarks):
            if bookmark["id"] == bookmark_id:
                bookmark_to_delete = bookmarks.pop(i)
                break
        
        if bookmark_to_delete:
            # Update tags index
            for tag in bookmark_to_delete.get("tags", []):
                if tag in data["tags"]:
                    data["tags"][tag].remove(bookmark_id)
                    if not data["tags"][tag]:
                        del data["tags"][tag]
            
            self._save_bookmarks(data)
            return True
        
        return False

    def update_bookmark(self, bookmark_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """Update a bookmark"""
        data = self._load_bookmarks()
        bookmarks = data.get("bookmarks", [])
        
        for bookmark in bookmarks:
            if bookmark["id"] == bookmark_id:
                # Update allowed fields
                allowed_fields = ["title", "url", "tags", "category"]
                for field, value in kwargs.items():
                    if field in allowed_fields:
                        bookmark[field] = value
                
                bookmark["updated_at"] = datetime.now().isoformat()
                self._save_bookmarks(data)
                return bookmark
        
        return None

    def get_all_tags(self) -> List[str]:
        """Get all unique tags"""
        data = self._load_bookmarks()
        return list(data.get("tags", {}).keys())

    def get_all_categories(self) -> List[str]:
        """Get all unique categories"""
        bookmarks = self.get_all_bookmarks()
        categories = set()
        for bookmark in bookmarks:
            categories.add(bookmark.get("category", "uncategorized"))
        return sorted(list(categories))

    def delete_bookmarks_by_tag(self, tag: str) -> int:
        """Delete all bookmarks with a specific tag"""
        bookmarks_to_delete = self.get_bookmarks_by_tag(tag)
        count = 0
        for bookmark in bookmarks_to_delete:
            if self.delete_bookmark(bookmark["id"]):
                count += 1
        return count

    def export_bookmarks(self) -> Dict[str, Any]:
        """Export all bookmarks as JSON"""
        return self._load_bookmarks()

    def import_bookmarks(self, import_data: Dict[str, Any]) -> bool:
        """Import bookmarks from JSON"""
        try:
            if "bookmarks" in import_data:
                self._save_bookmarks(import_data)
                return True
            return False
        except Exception as e:
            print(f"Error importing bookmarks: {e}")
            return False

