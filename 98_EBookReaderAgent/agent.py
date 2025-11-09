"""
EBookReaderAgent
Main agent for reading and analyzing eBooks (PDF and ePub)
"""

import os
import json
import re
from typing import Dict, List, Optional, Any
from datetime import datetime
from config import Config
from utils.book_parser import BookParser, Chapter, BookMetadata
from utils.llm_service import LLMService


class EBookReaderAgent:
    """AI-powered eBook reader and analyzer agent"""
    
    def __init__(self, llm_service: Optional[LLMService] = None):
        """Initialize the agent"""
        self.llm_service = llm_service or LLMService()
        self.parser = BookParser()
        self.current_book_loaded = False
    
    def cleanup(self):
        """Clean up temporary files (e.g., downloaded from URLs)"""
        self.parser.cleanup_temp_files()
    
    def load_book(self, file_path: str) -> Dict:
        """Load and parse a book file"""
        try:
            result = self.parser.parse_file(file_path)
            if result['success']:
                self.current_book_loaded = True
            return result
        except Exception as e:
            return {
                'success': False,
                'error': f'Error loading book: {str(e)}'
            }
    
    def get_book_info(self) -> Dict:
        """Get information about the currently loaded book"""
        if not self.current_book_loaded:
            return {
                'success': False,
                'error': 'No book loaded'
            }
        
        metadata = self.parser.get_metadata()
        chapters = self.parser.get_all_chapters()
        
        if not metadata:
            return {
                'success': False,
                'error': 'Book metadata not available'
            }
        
        return {
            'success': True,
            'metadata': {
                'title': metadata.title,
                'author': metadata.author,
                'total_pages': metadata.total_pages,
                'total_chapters': metadata.total_chapters,
                'file_type': metadata.file_type,
                'word_count': metadata.word_count,
                'estimated_reading_time': self._calculate_reading_time(metadata.word_count)
            },
            'chapters': [
                {
                    'number': ch.chapter_number,
                    'title': ch.title,
                    'word_count': len(ch.content.split())
                }
                for ch in chapters
            ]
        }
    
    def _calculate_reading_time(self, word_count: int) -> Dict:
        """Calculate estimated reading time"""
        minutes = word_count / Config.WORDS_PER_MINUTE
        hours = int(minutes // 60)
        mins = int(minutes % 60)
        
        return {
            'minutes': int(minutes),
            'hours': hours,
            'minutes_remainder': mins,
            'formatted': f"{hours}h {mins}m" if hours > 0 else f"{mins}m"
        }
    
    def summarize_chapter(self, chapter_number: int) -> Dict:
        """Generate AI summary for a specific chapter"""
        if not self.current_book_loaded:
            return {
                'success': False,
                'error': 'No book loaded'
            }
        
        chapter = self.parser.get_chapter(chapter_number)
        if not chapter:
            return {
                'success': False,
                'error': f'Chapter {chapter_number} not found'
            }
        
        try:
            # Load prompt template
            prompt_template = self.llm_service._read_template("chapter_summary_prompt.txt")
            if not prompt_template:
                prompt_template = self._get_default_summary_prompt()
            
            prompt = prompt_template.format(
                chapter_title=chapter.title,
                chapter_content=chapter.content[:Config.MAX_CHAPTER_LENGTH]  # Limit content length
            )
            
            # Generate summary
            result = self.llm_service.generate_content(prompt, max_tokens=2000)
            summary = result.get('summary', 'Summary not available')
            
            return {
                'success': True,
                'chapter_number': chapter_number,
                'chapter_title': chapter.title,
                'summary': summary,
                'word_count': len(chapter.content.split())
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'Error generating summary: {str(e)}'
            }
    
    def summarize_all_chapters(self) -> Dict:
        """Generate summaries for all chapters"""
        if not self.current_book_loaded:
            return {
                'success': False,
                'error': 'No book loaded'
            }
        
        chapters = self.parser.get_all_chapters()
        summaries = []
        
        for chapter in chapters:
            summary_result = self.summarize_chapter(chapter.chapter_number)
            if summary_result['success']:
                summaries.append(summary_result)
        
        return {
            'success': True,
            'total_chapters': len(summaries),
            'summaries': summaries
        }
    
    def get_key_takeaways(self, num_takeaways: int = 10) -> Dict:
        """Extract key takeaways from the book"""
        if not self.current_book_loaded:
            return {
                'success': False,
                'error': 'No book loaded'
            }
        
        try:
            # Get all chapter summaries first
            all_summaries = self.summarize_all_chapters()
            if not all_summaries['success']:
                return all_summaries
            
            # Combine summaries
            combined_text = "\n\n".join([
                f"Chapter {s['chapter_number']}: {s['chapter_title']}\n{s['summary']}"
                for s in all_summaries['summaries']
            ])
            
            # Load prompt template
            prompt_template = self.llm_service._read_template("key_takeaways_prompt.txt")
            if not prompt_template:
                prompt_template = self._get_default_takeaways_prompt()
            
            prompt = prompt_template.format(
                book_title=self.parser.get_metadata().title if self.parser.get_metadata() else "the book",
                num_takeaways=num_takeaways,
                chapter_summaries=combined_text[:10000]  # Limit length
            )
            
            # Generate takeaways
            result = self.llm_service.generate_content(prompt, max_tokens=2000)
            takeaways_text = result.get('summary', 'Key takeaways not available')
            
            # Parse takeaways (try to extract list)
            takeaways = self._parse_takeaways(takeaways_text)
            
            return {
                'success': True,
                'takeaways': takeaways,
                'formatted_text': takeaways_text
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'Error extracting takeaways: {str(e)}'
            }
    
    def _parse_takeaways(self, text: str) -> List[str]:
        """Parse takeaways from text (numbered list, bullet points, etc.)"""
        takeaways = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Remove numbering and bullets
            line = re.sub(r'^\d+[\.\)]\s*', '', line)
            line = re.sub(r'^[-•*]\s*', '', line)
            
            if line and len(line) > 10:  # Minimum length
                takeaways.append(line)
        
        return takeaways[:10]  # Limit to 10
    
    def ask_question(self, question: str, chapter_number: Optional[int] = None) -> Dict:
        """Ask a question about the book content"""
        if not self.current_book_loaded:
            return {
                'success': False,
                'error': 'No book loaded'
            }
        
        try:
            # Get relevant content
            if chapter_number:
                chapter = self.parser.get_chapter(chapter_number)
                if not chapter:
                    return {
                        'success': False,
                        'error': f'Chapter {chapter_number} not found'
                    }
                content = chapter.content[:Config.MAX_CHAPTER_LENGTH]
                context_title = f"Chapter {chapter_number}: {chapter.title}"
            else:
                # Use all chapters (limited)
                chapters = self.parser.get_all_chapters()
                content_parts = [ch.content[:2000] for ch in chapters[:5]]  # First 5 chapters, 2000 chars each
                content = "\n\n".join(content_parts)
                context_title = "the entire book"
            
            # Load prompt template
            prompt_template = self.llm_service._read_template("question_prompt.txt")
            if not prompt_template:
                prompt_template = self._get_default_question_prompt()
            
            book_title = self.parser.get_metadata().title if self.parser.get_metadata() else "the book"
            
            prompt = prompt_template.format(
                book_title=book_title,
                context_title=context_title,
                question=question,
                content=content
            )
            
            # Generate answer
            result = self.llm_service.generate_content(prompt, max_tokens=1500)
            answer = result.get('summary', 'Answer not available')
            
            return {
                'success': True,
                'question': question,
                'answer': answer,
                'chapter_context': context_title if chapter_number else None
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'Error answering question: {str(e)}'
            }
    
    def get_important_quotes(self, chapter_number: Optional[int] = None, num_quotes: int = 5) -> Dict:
        """Extract important quotes from the book or a specific chapter"""
        if not self.current_book_loaded:
            return {
                'success': False,
                'error': 'No book loaded'
            }
        
        try:
            # Get relevant content
            if chapter_number:
                chapter = self.parser.get_chapter(chapter_number)
                if not chapter:
                    return {
                        'success': False,
                        'error': f'Chapter {chapter_number} not found'
                    }
                content = chapter.content
                context_title = f"Chapter {chapter_number}: {chapter.title}"
            else:
                # Use all chapters
                chapters = self.parser.get_all_chapters()
                content_parts = [ch.content for ch in chapters]
                content = "\n\n".join(content_parts)
                context_title = "the entire book"
            
            # Load prompt template
            prompt_template = self.llm_service._read_template("quotes_prompt.txt")
            if not prompt_template:
                prompt_template = self._get_default_quotes_prompt()
            
            book_title = self.parser.get_metadata().title if self.parser.get_metadata() else "the book"
            
            prompt = prompt_template.format(
                book_title=book_title,
                context_title=context_title,
                num_quotes=num_quotes,
                content=content[:15000]  # Limit content length
            )
            
            # Generate quotes
            result = self.llm_service.generate_content(prompt, max_tokens=1500)
            quotes_text = result.get('summary', 'Quotes not available')
            
            # Parse quotes
            quotes = self._parse_quotes(quotes_text)
            
            return {
                'success': True,
                'quotes': quotes,
                'formatted_text': quotes_text,
                'context': context_title
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'Error extracting quotes: {str(e)}'
            }
    
    def _parse_quotes(self, text: str) -> List[Dict[str, str]]:
        """Parse quotes from text"""
        quotes = []
        lines = text.split('\n')
        current_quote = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for quoted text
            if '"' in line or "'" in line:
                # Extract quote
                quote_matches = re.findall(r'["\']([^"\']+)["\']', line)
                if quote_matches:
                    for quote_text in quote_matches:
                        if len(quote_text) > 20:  # Minimum quote length
                            quotes.append({
                                'quote': quote_text,
                                'context': line
                            })
        
        return quotes[:10]  # Limit to 10
    
    def analyze_book(self, include_summaries: bool = True, include_takeaways: bool = True, 
                     include_quotes: bool = True) -> Dict:
        """Complete book analysis"""
        if not self.current_book_loaded:
            return {
                'success': False,
                'error': 'No book loaded'
            }
        
        result = {
            'success': True,
            'book_info': self.get_book_info()
        }
        
        if include_summaries:
            result['chapter_summaries'] = self.summarize_all_chapters()
        
        if include_takeaways:
            result['key_takeaways'] = self.get_key_takeaways()
        
        if include_quotes:
            result['important_quotes'] = self.get_important_quotes()
        
        return result
    
    def _get_default_summary_prompt(self) -> str:
        """Default prompt for chapter summarization"""
        return """Summarize the following chapter from a book in approximately 500 words.

Chapter Title: {chapter_title}

Chapter Content:
{chapter_content}

Provide a clear, concise summary that captures the main points, key concepts, and important details of this chapter."""

    def _get_default_takeaways_prompt(self) -> str:
        """Default prompt for key takeaways"""
        return """Extract the top {num_takeaways} key takeaways from the following book summaries.

Book: {book_title}

Chapter Summaries:
{chapter_summaries}

Provide {num_takeaways} key insights, lessons, or important points from this book. Format as a numbered list."""

    def _get_default_question_prompt(self) -> str:
        """Default prompt for questions"""
        return """Answer the following question based on the content from {book_title}, specifically from {context_title}.

Question: {question}

Relevant Content:
{content}

Provide a clear, accurate answer based on the content provided. If the answer cannot be found in the content, state that clearly."""

    def _get_default_quotes_prompt(self) -> str:
        """Default prompt for quotes"""
        return """Extract {num_quotes} important, memorable, or impactful quotes from the following content from {book_title} ({context_title}).

Content:
{content}

Provide {num_quotes} quotes that are particularly meaningful, insightful, or representative of the book's key themes. Include the quotes with brief context if available."""
