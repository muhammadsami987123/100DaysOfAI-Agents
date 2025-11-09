"""
ePub extraction utility using ebooklib and beautifulsoup4
Extracts text with proper chapter segmentation
"""

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from typing import List, Dict
import re


class ePubExtractor:
    """Extract text and structure from ePub files"""
    
    def __init__(self):
        self.book = None
    
    def load_epub(self, file_path: str) -> Dict:
        """Load ePub file"""
        try:
            self.book = epub.read_epub(file_path)
            return {
                'success': True,
                'item_count': len(list(self.book.get_items()))
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def extract_full_text(self) -> str:
        """Extract all text from ePub"""
        if not self.book:
            return ""
        
        full_text = ""
        for item in self.book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                text = soup.get_text()
                full_text += text + "\n\n"
        
        return full_text
    
    def extract_chapters(self) -> List[Dict]:
        """Extract chapters from ePub"""
        if not self.book:
            return []
        
        chapters = []
        
        # Get spine (reading order)
        spine = [item[0] for item in self.book.spine]
        
        for item_id in spine:
            item = self.book.get_item_by_id(item_id)
            if item and item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                
                # Try to get chapter title from heading
                title = "Untitled Chapter"
                headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                if headings:
                    title = headings[0].get_text().strip()
                
                # Extract text content
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                
                text = soup.get_text()
                # Clean up whitespace
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = '\n'.join(chunk for chunk in chunks if chunk)
                
                if text.strip():
                    chapters.append({
                        'title': title,
                        'content': text.strip(),
                        'word_count': len(text.split())
                    })
        
        # If no chapters found, try to extract from all items
        if not chapters:
            full_text = self.extract_full_text()
            chapters.append({
                'title': 'Full Document',
                'content': full_text,
                'word_count': len(full_text.split())
            })
        
        return chapters
    
    def get_metadata(self) -> Dict:
        """Get ePub metadata"""
        if not self.book:
            return {}
        
        metadata = {}
        
        # Extract title
        title = self.book.get_metadata('DC', 'title')
        metadata['title'] = title[0][0] if title else 'Unknown'
        
        # Extract author
        author = self.book.get_metadata('DC', 'creator')
        metadata['author'] = author[0][0] if author else 'Unknown'
        
        # Extract other metadata
        subject = self.book.get_metadata('DC', 'subject')
        metadata['subject'] = subject[0][0] if subject else ''
        
        description = self.book.get_metadata('DC', 'description')
        metadata['description'] = description[0][0] if description else ''
        
        language = self.book.get_metadata('DC', 'language')
        metadata['language'] = language[0][0] if language else ''
        
        # Count chapters/pages (estimated)
        chapters = self.extract_chapters()
        metadata['chapters'] = len(chapters)
        metadata['word_count'] = sum(ch['word_count'] for ch in chapters)
        
        return metadata
    
    def estimate_reading_time(self, text: str) -> Dict:
        """Estimate reading time based on word count"""
        from config import Config
        
        word_count = len(text.split())
        minutes = word_count / Config.WORDS_PER_MINUTE
        hours = int(minutes // 60)
        mins = int(minutes % 60)
        
        return {
            'word_count': word_count,
            'minutes': round(minutes, 1),
            'hours': hours,
            'minutes_remainder': mins,
            'formatted': f"{hours}h {mins}m" if hours > 0 else f"{mins}m"
        }

