"""
LogAnalyzerBot Agent
Main agent for analyzing system and error logs
"""

import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME, MAX_SUGGESTIONS
from utils.log_parser import LogParser, LogEntry
from utils.pattern_matcher import PatternMatcher


class LogAnalyzerBot:
    """AI-powered log analyzer agent"""
    
    def __init__(self, groq_api_key: str = None):
        """Initialize the agent"""
        self.api_key = groq_api_key or GROQ_API_KEY
        self.client = Groq(api_key=self.api_key) if self.api_key else None
        self.parser = LogParser()
        self.pattern_matcher = PatternMatcher()
        self.log_entries: List[LogEntry] = []
    
    def load_log_file(self, file_path: str) -> Dict:
        """Load and parse log file"""
        try:
            self.log_entries = self.parser.parse_file(file_path)
            return {
                'success': True,
                'total_entries': len(self.log_entries),
                'message': f'Successfully parsed {len(self.log_entries)} log entries'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def load_log_content(self, content: str) -> Dict:
        """Load and parse log content from string"""
        try:
            self.log_entries = self.parser.parse_content(content)
            return {
                'success': True,
                'total_entries': len(self.log_entries),
                'message': f'Successfully parsed {len(self.log_entries)} log entries'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def filter_entries(self, 
                      start_date: Optional[datetime] = None,
                      end_date: Optional[datetime] = None,
                      log_levels: Optional[List[str]] = None,
                      keyword: Optional[str] = None) -> List[LogEntry]:
        """Filter log entries based on criteria"""
        filtered = self.log_entries
        
        # Filter by date range
        if start_date:
            filtered = [e for e in filtered if e.timestamp and e.timestamp >= start_date]
        if end_date:
            filtered = [e for e in filtered if e.timestamp and e.timestamp <= end_date]
        
        # Filter by log level
        if log_levels:
            log_levels_upper = [level.upper() for level in log_levels]
            filtered = [e for e in filtered if e.level in log_levels_upper]
        
        # Filter by keyword
        if keyword:
            keyword_lower = keyword.lower()
            filtered = [e for e in filtered if keyword_lower in e.message.lower() or 
                       keyword_lower in e.source.lower()]
        
        return filtered
    
    def get_summary(self, entries: Optional[List[LogEntry]] = None) -> Dict:
        """Get summary of log analysis"""
        entries = entries or self.log_entries
        
        if not entries:
            return {'error': 'No log entries to analyze'}
        
        # Frequency analysis
        frequency = self.pattern_matcher.analyze_frequency(entries)
        
        # Known issues
        known_issues = self.pattern_matcher.identify_known_issues(entries)
        
        # Error patterns
        error_patterns = self.pattern_matcher.extract_error_patterns(entries)
        
        # Timeline of critical events
        timeline = self.pattern_matcher.get_timeline(entries, ['ERROR', 'CRITICAL'])
        
        # Correlations
        correlations = self.pattern_matcher.find_correlations(entries)
        
        # Get most frequent error
        most_frequent_error = None
        if error_patterns:
            most_frequent_error = max(error_patterns.items(), key=lambda x: x[1])
        
        # Get affected modules
        error_sources = [e.source for e in entries if e.level in ['ERROR', 'CRITICAL']]
        affected_modules = list(set(error_sources))[:10]
        
        return {
            'total_entries': len(entries),
            'frequency': frequency,
            'total_errors': frequency['level_counts'].get('ERROR', 0),
            'total_warnings': frequency['level_counts'].get('WARNING', 0),
            'total_critical': frequency['level_counts'].get('CRITICAL', 0),
            'most_frequent_error': most_frequent_error,
            'affected_modules': affected_modules,
            'known_issues': known_issues[:MAX_SUGGESTIONS],
            'error_patterns': dict(list(error_patterns.items())[:10]),
            'timeline': timeline[:50],  # Last 50 important events
            'correlations': correlations,
            'date_range': self._get_date_range(entries)
        }
    
    def _get_date_range(self, entries: List[LogEntry]) -> Dict:
        """Get date range of log entries"""
        timestamps = [e.timestamp for e in entries if e.timestamp]
        if timestamps:
            return {
                'start': min(timestamps).isoformat(),
                'end': max(timestamps).isoformat()
            }
        return {'start': None, 'end': None}
    
    def get_ai_insights(self, summary: Dict) -> str:
        """Get AI-powered insights using Groq"""
        if not self.client:
            return "AI insights unavailable: No API key configured"
        
        try:
            # Load prompt template
            with open('prompts/analysis_prompt.txt', 'r') as f:
                prompt_template = f.read()
            
            # Prepare analysis data
            analysis_data = json.dumps(summary, indent=2)
            prompt = prompt_template.format(analysis_data=analysis_data)
            
            # Call Groq API
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are an expert log analyzer and system administrator."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            return f"Error generating AI insights: {str(e)}"
    
    def explain_error(self, error_message: str, context: Dict = None) -> str:
        """Get AI explanation for a specific error"""
        if not self.client:
            return "AI explanation unavailable: No API key configured"
        
        try:
            # Load prompt template
            with open('prompts/error_explanation_prompt.txt', 'r') as f:
                prompt_template = f.read()
            
            # Prepare context
            context = context or {}
            additional_context = ""
            if context.get('timestamp'):
                additional_context += f"\n- Timestamp: {context['timestamp']}"
            if context.get('similar_errors'):
                additional_context += f"\n- Similar errors found: {context['similar_errors']}"
            
            prompt = prompt_template.format(
                error_message=error_message,
                log_level=context.get('log_level', 'ERROR'),
                source=context.get('source', 'unknown'),
                frequency=context.get('frequency', 1),
                additional_context=additional_context
            )
            
            # Call Groq API
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a helpful technical expert explaining log errors."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            return f"Error generating explanation: {str(e)}"
    
    def analyze(self, 
                file_path: str = None,
                content: str = None,
                start_date: Optional[datetime] = None,
                end_date: Optional[datetime] = None,
                log_levels: Optional[List[str]] = None,
                keyword: Optional[str] = None,
                include_ai_insights: bool = True) -> Dict:
        """Complete analysis pipeline"""
        
        # Load logs
        if file_path:
            result = self.load_log_file(file_path)
        elif content:
            result = self.load_log_content(content)
        else:
            return {'error': 'No log file or content provided'}
        
        if not result['success']:
            return result
        
        # Filter entries
        filtered_entries = self.filter_entries(start_date, end_date, log_levels, keyword)
        
        # Get summary
        summary = self.get_summary(filtered_entries)
        
        # Add AI insights if requested
        if include_ai_insights and self.client:
            summary['ai_insights'] = self.get_ai_insights(summary)
        
        return summary
