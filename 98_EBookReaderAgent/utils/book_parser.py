"""
Book Parser for EBookReaderAgent
Supports PDF and ePub file parsing with chapter segmentation
Supports downloading books from public URLs
"""

import os
import re
import tempfile
from typing import Dict, List, Optional
from dataclasses import dataclass
from urllib.parse import urlparse
from pathlib import Path


@dataclass
class Chapter:
    """Represents a chapter in a book"""
    title: str
    content: str
    page_number: Optional[int] = None
    chapter_number: Optional[int] = None


@dataclass
class BookMetadata:
    """Book metadata"""
    title: str
    author: str
    total_pages: int
    total_chapters: int
    file_type: str
    word_count: int


class BookParser:
    """Parser for PDF and ePub files"""
    
    def __init__(self):
        self.chapters: List[Chapter] = []
        self.metadata: Optional[BookMetadata] = None
        self._temp_files: List[str] = []  # Track temp files for cleanup
    
    def is_url(self, path_or_url: str) -> bool:
        """Check if the input is a URL"""
        try:
            result = urlparse(path_or_url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def download_from_url(self, url: str) -> Dict:
        """Download a book file from a public URL"""
        try:
            import requests
        except ImportError:
            return {
                'success': False,
                'error': 'requests library not installed. Install with: pip install requests'
            }
        
        try:
            # Validate URL
            if not self.is_url(url):
                return {
                    'success': False,
                    'error': 'Invalid URL format'
                }
            
            # Get filename from URL or content-disposition
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            
            # Download file
            print(f"Downloading book from URL: {url}")
            response = requests.get(url, timeout=60, stream=True)
            response.raise_for_status()
            
            # Check content type
            content_type = response.headers.get('Content-Type', '').lower()
            if 'pdf' in content_type:
                file_ext = '.pdf'
            elif 'epub' in content_type or 'application/epub' in content_type:
                file_ext = '.epub'
            else:
                # Try to get extension from filename
                file_ext = os.path.splitext(filename)[1].lower()
                if not file_ext or file_ext not in ['.pdf', '.epub']:
                    # Default to PDF if unknown
                    file_ext = '.pdf'
            
            # Create temp file
            temp_dir = Path(tempfile.gettempdir()) / 'ebookreader'
            temp_dir.mkdir(exist_ok=True)
            
            temp_file = temp_dir / f"book_{os.urandom(8).hex()}{file_ext}"
            
            # Save downloaded content
            with open(temp_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            self._temp_files.append(str(temp_file))
            
            return {
                'success': True,
                'file_path': str(temp_file),
                'message': f'Successfully downloaded book from URL'
            }
        
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'Error downloading from URL: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}'
            }
    
    def parse_file(self, file_path: str) -> Dict:
        """Parse a book file (PDF or ePub) or download from URL"""
        # Check if it's a URL
        if self.is_url(file_path):
            download_result = self.download_from_url(file_path)
            if not download_result['success']:
                return download_result
            file_path = download_result['file_path']
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.pdf':
            return self._parse_pdf(file_path)
        elif file_ext == '.epub':
            return self._parse_epub(file_path)
        else:
            return {
                'success': False,
                'error': f'Unsupported file type: {file_ext}'
            }
    
    def cleanup_temp_files(self):
        """Clean up temporary downloaded files"""
        for temp_file in self._temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception:
                pass
        self._temp_files = []
    
    def _parse_pdf(self, file_path: str) -> Dict:
        """Parse PDF file using PyMuPDF"""
        try:
            import fitz  # PyMuPDF
        except ImportError:
            return {
                'success': False,
                'error': 'PyMuPDF not installed. Install it with: pip install PyMuPDF'
            }
        
        try:
            doc = fitz.open(file_path)
            total_pages = len(doc)
            
            # Extract metadata
            metadata = doc.metadata
            title = metadata.get('title', 'Unknown Title')
            author = metadata.get('author', 'Unknown Author')
            
            # Extract text from all pages
            full_text = ""
            for page_num in range(total_pages):
                page = doc[page_num]
                full_text += page.get_text()
            
            doc.close()
            
            # Segment into chapters
            chapters = self._segment_chapters(full_text, file_type='pdf')
            
            # Calculate word count
            word_count = len(full_text.split())
            
            self.metadata = BookMetadata(
                title=title,
                author=author,
                total_pages=total_pages,
                total_chapters=len(chapters),
                file_type='pdf',
                word_count=word_count
            )
            
            self.chapters = chapters
            
            return {
                'success': True,
                'metadata': self.metadata,
                'chapters': len(chapters),
                'message': f'Successfully parsed PDF with {len(chapters)} chapters'
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'Error parsing PDF: {str(e)}'
            }
    
    def _parse_epub(self, file_path: str) -> Dict:
        """Parse ePub file using ebooklib"""
        try:
            import ebooklib
            from ebooklib import epub
            from bs4 import BeautifulSoup
        except ImportError:
            return {
                'success': False,
                'error': 'ebooklib or beautifulsoup4 not installed. Install with: pip install ebooklib beautifulsoup4'
            }
        
        try:
            book = epub.read_epub(file_path)
            
            # Extract metadata
            title = book.get_metadata('DC', 'title')[0][0] if book.get_metadata('DC', 'title') else 'Unknown Title'
            author = book.get_metadata('DC', 'creator')[0][0] if book.get_metadata('DC', 'creator') else 'Unknown Author'
            
            # Extract text from all items
            chapters = []
            chapter_num = 1
            full_text = ""
            
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    soup = BeautifulSoup(item.get_content(), 'html.parser')
                    text = soup.get_text()
                    
                    if text.strip():
                        # Try to extract chapter title
                        chapter_title = self._extract_chapter_title(soup, text)
                        
                        chapters.append(Chapter(
                            title=chapter_title,
                            content=text,
                            chapter_number=chapter_num
                        ))
                        
                        full_text += text + "\n\n"
                        chapter_num += 1
            
            # Calculate word count
            word_count = len(full_text.split())
            
            # Estimate pages (assuming ~250 words per page)
            estimated_pages = max(1, word_count // 250)
            
            self.metadata = BookMetadata(
                title=title,
                author=author,
                total_pages=estimated_pages,
                total_chapters=len(chapters),
                file_type='epub',
                word_count=word_count
            )
            
            self.chapters = chapters
            
            return {
                'success': True,
                'metadata': self.metadata,
                'chapters': len(chapters),
                'message': f'Successfully parsed ePub with {len(chapters)} chapters'
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'Error parsing ePub: {str(e)}'
            }
    
    def _extract_chapter_title(self, soup, text: str) -> str:
        """Extract chapter title from HTML or text"""
        # Try to find h1, h2, or h3 tags
        for tag in ['h1', 'h2', 'h3']:
            headings = soup.find_all(tag)
            if headings:
                title = headings[0].get_text().strip()
                if title and len(title) < 200:
                    return title
        
        # Try to find title in first few lines
        lines = text.strip().split('\n')
        for line in lines[:5]:
            line = line.strip()
            if line and len(line) < 200 and len(line) > 3:
                # Check if it looks like a title (short, capitalized)
                if line[0].isupper() and len(line.split()) < 20:
                    return line
        
        return "Chapter"
    
    def _segment_chapters(self, text: str, file_type: str = 'pdf') -> List[Chapter]:
        """Segment text into chapters"""
        chapters = []
        
        # Common chapter patterns
        chapter_patterns = [
            r'^Chapter\s+\d+[\.\:]\s*(.+)$',
            r'^CHAPTER\s+\d+[\.\:]\s*(.+)$',
            r'^\d+[\.\:]\s*(.+)$',
            r'^Part\s+\d+[\.\:]\s*(.+)$',
            r'^PART\s+\d+[\.\:]\s*(.+)$',
        ]
        
        lines = text.split('\n')
        current_chapter_title = "Introduction"
        current_chapter_content = []
        chapter_num = 1
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line matches a chapter pattern
            is_chapter_header = False
            for pattern in chapter_patterns:
                match = re.match(pattern, line, re.IGNORECASE)
                if match:
                    # Save previous chapter
                    if current_chapter_content:
                        chapters.append(Chapter(
                            title=current_chapter_title,
                            content='\n'.join(current_chapter_content),
                            chapter_number=chapter_num
                        ))
                        chapter_num += 1
                    
                    # Start new chapter
                    current_chapter_title = match.group(1) if match.lastindex else f"Chapter {chapter_num}"
                    current_chapter_content = []
                    is_chapter_header = True
                    break
            
            if not is_chapter_header:
                current_chapter_content.append(line)
        
        # Add final chapter
        if current_chapter_content:
            chapters.append(Chapter(
                title=current_chapter_title,
                content='\n'.join(current_chapter_content),
                chapter_number=chapter_num
            ))
        
        # If no chapters found, create a single chapter
        if not chapters:
            chapters.append(Chapter(
                title="Full Book",
                content=text,
                chapter_number=1
            ))
        
        return chapters
    
    def get_chapter(self, chapter_number: int) -> Optional[Chapter]:
        """Get a specific chapter by number"""
        for chapter in self.chapters:
            if chapter.chapter_number == chapter_number:
                return chapter
        return None
    
    def get_all_chapters(self) -> List[Chapter]:
        """Get all chapters"""
        return self.chapters
    
    def get_metadata(self) -> Optional[BookMetadata]:
        """Get book metadata"""
        return self.metadata

