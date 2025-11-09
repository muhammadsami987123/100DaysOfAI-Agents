"""
PDF extraction utility using PyMuPDF (fitz)
Extracts text with chapter segmentation
"""

import fitz  # PyMuPDF
from typing import List, Dict, Optional
import re


class PDFExtractor:
    """Extract text and structure from PDF files"""
    
    def __init__(self):
        self.doc = None
    
    def load_pdf(self, file_path: str) -> Dict:
        """Load PDF file"""
        try:
            self.doc = fitz.open(file_path)
            return {
                'success': True,
                'pages': len(self.doc),
                'metadata': self.doc.metadata
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def extract_full_text(self) -> str:
        """Extract all text from PDF"""
        if not self.doc:
            return ""
        
        full_text = ""
        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            full_text += page.get_text()
        
        return full_text
    
    def extract_chapters(self) -> List[Dict]:
        """Extract chapters based on heading patterns"""
        if not self.doc:
            return []
        
        chapters = []
        current_chapter = None
        current_text = ""
        
        # Common chapter heading patterns
        chapter_patterns = [
            r'^(Chapter\s+\d+[:\-]?\s*.+)',
            r'^(CHAPTER\s+\d+[:\-]?\s*.+)',
            r'^(\d+\.\s+[A-Z][^.]+)',
            r'^([A-Z][A-Z\s]{3,50})$',  # All caps headings
        ]
        
        full_text = self.extract_full_text()
        lines = full_text.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Check if line matches chapter heading pattern
            is_chapter = False
            for pattern in chapter_patterns:
                match = re.match(pattern, line)
                if match:
                    is_chapter = True
                    # Save previous chapter if exists
                    if current_chapter:
                        chapters.append({
                            'title': current_chapter,
                            'content': current_text.strip(),
                            'word_count': len(current_text.split())
                        })
                    
                    # Start new chapter
                    current_chapter = line
                    current_text = ""
                    break
            
            if not is_chapter:
                current_text += line + "\n"
        
        # Add last chapter
        if current_chapter:
            chapters.append({
                'title': current_chapter,
                'content': current_text.strip(),
                'word_count': len(current_text.split())
            })
        
        # If no chapters found, create single chapter
        if not chapters:
            full_text = self.extract_full_text()
            chapters.append({
                'title': 'Full Document',
                'content': full_text,
                'word_count': len(full_text.split())
            })
        
        return chapters
    
    def extract_by_pages(self, pages_per_chunk: int = 10) -> List[Dict]:
        """Extract text divided into page-based chunks"""
        if not self.doc:
            return []
        
        chunks = []
        total_pages = len(self.doc)
        
        for start_page in range(0, total_pages, pages_per_chunk):
            end_page = min(start_page + pages_per_chunk, total_pages)
            chunk_text = ""
            
            for page_num in range(start_page, end_page):
                page = self.doc[page_num]
                chunk_text += page.get_text() + "\n"
            
            chunks.append({
                'title': f'Pages {start_page + 1}-{end_page}',
                'content': chunk_text.strip(),
                'word_count': len(chunk_text.split()),
                'page_range': (start_page + 1, end_page)
            })
        
        return chunks
    
    def get_metadata(self) -> Dict:
        """Get PDF metadata"""
        if not self.doc:
            return {}
        
        metadata = self.doc.metadata
        return {
            'title': metadata.get('title', 'Unknown'),
            'author': metadata.get('author', 'Unknown'),
            'subject': metadata.get('subject', ''),
            'pages': len(self.doc),
            'creator': metadata.get('creator', ''),
            'producer': metadata.get('producer', ''),
            'creation_date': metadata.get('creationDate', ''),
            'modification_date': metadata.get('modDate', '')
        }
    
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
    
    def close(self):
        """Close PDF document"""
        if self.doc:
            self.doc.close()
            self.doc = None

