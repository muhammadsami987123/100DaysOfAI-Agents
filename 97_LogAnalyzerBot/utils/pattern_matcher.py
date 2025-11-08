"""
Pattern Matcher Utility
Identifies common patterns and suggests solutions
"""

import re
from collections import Counter, defaultdict
from typing import List, Dict, Tuple
from config import MIN_PATTERN_FREQUENCY


class PatternMatcher:
    """Identifies patterns in log entries and suggests solutions"""
    
    def __init__(self):
        self.known_patterns = {
            'connection_timeout': {
                'keywords': ['timeout', 'connection', 'timed out', 'connect failed'],
                'suggestion': 'Check network connectivity, firewall settings, and increase timeout values'
            },
            'database_error': {
                'keywords': ['database', 'sql', 'query', 'deadlock', 'lock timeout'],
                'suggestion': 'Check database connection pool, optimize queries, and review transaction isolation levels'
            },
            'memory_error': {
                'keywords': ['outofmemory', 'memory', 'heap', 'oom'],
                'suggestion': 'Increase memory allocation, check for memory leaks, and optimize resource usage'
            },
            'permission_denied': {
                'keywords': ['permission denied', 'access denied', 'forbidden', 'unauthorized'],
                'suggestion': 'Verify file/directory permissions, check user privileges, and review access control settings'
            },
            'file_not_found': {
                'keywords': ['file not found', 'no such file', 'does not exist', 'missing file'],
                'suggestion': 'Verify file path, check file existence, and ensure proper file deployment'
            },
            'null_pointer': {
                'keywords': ['nullpointer', 'null reference', 'null object', 'nonetype'],
                'suggestion': 'Add null checks, initialize variables properly, and review object lifecycle'
            },
            'api_error': {
                'keywords': ['api', '400', '401', '403', '404', '500', '502', '503', 'bad gateway'],
                'suggestion': 'Check API endpoint, verify authentication tokens, and review API rate limits'
            },
            'ssl_certificate': {
                'keywords': ['ssl', 'certificate', 'tls', 'handshake failed', 'cert expired'],
                'suggestion': 'Verify SSL certificate validity, update certificates, and check certificate chain'
            }
        }
    
    def extract_error_patterns(self, log_entries: List) -> Dict[str, int]:
        """Extract common error patterns from log entries"""
        error_messages = [entry.message for entry in log_entries if entry.level in ['ERROR', 'CRITICAL']]
        
        # Normalize messages (remove numbers, paths, etc.)
        normalized = []
        for msg in error_messages:
            # Remove file paths
            msg = re.sub(r'[/\\][\w/\\.-]+', '<PATH>', msg)
            # Remove numbers
            msg = re.sub(r'\d+', '<NUM>', msg)
            # Remove URLs
            msg = re.sub(r'https?://[^\s]+', '<URL>', msg)
            # Remove IPs
            msg = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', '<IP>', msg)
            normalized.append(msg)
        
        # Count patterns
        pattern_counts = Counter(normalized)
        
        # Filter by minimum frequency
        return {pattern: count for pattern, count in pattern_counts.items() 
                if count >= MIN_PATTERN_FREQUENCY}
    
    def identify_known_issues(self, log_entries: List) -> List[Dict]:
        """Identify known issues based on predefined patterns"""
        identified_issues = []
        
        for pattern_name, pattern_info in self.known_patterns.items():
            matching_entries = []
            
            for entry in log_entries:
                if entry.level in ['ERROR', 'CRITICAL', 'WARNING']:
                    message_lower = entry.message.lower()
                    if any(keyword in message_lower for keyword in pattern_info['keywords']):
                        matching_entries.append(entry)
            
            if matching_entries:
                identified_issues.append({
                    'issue_type': pattern_name.replace('_', ' ').title(),
                    'count': len(matching_entries),
                    'suggestion': pattern_info['suggestion'],
                    'sample_entries': [e.message for e in matching_entries[:3]]
                })
        
        return sorted(identified_issues, key=lambda x: x['count'], reverse=True)
    
    def analyze_frequency(self, log_entries: List) -> Dict:
        """Analyze frequency of log levels, sources, and errors"""
        level_counts = Counter()
        source_counts = Counter()
        hourly_distribution = defaultdict(int)
        
        for entry in log_entries:
            level_counts[entry.level] += 1
            source_counts[entry.source] += 1
            
            if entry.timestamp:
                hour = entry.timestamp.strftime('%Y-%m-%d %H:00')
                hourly_distribution[hour] += 1
        
        return {
            'level_counts': dict(level_counts),
            'source_counts': dict(source_counts.most_common(10)),
            'hourly_distribution': dict(sorted(hourly_distribution.items()))
        }
    
    def get_timeline(self, log_entries: List, level_filter: List[str] = None) -> List[Dict]:
        """Get timeline of important events"""
        timeline = []
        
        for entry in log_entries:
            if level_filter and entry.level not in level_filter:
                continue
            
            if entry.level in ['ERROR', 'CRITICAL', 'WARNING']:
                timeline.append({
                    'timestamp': entry.timestamp.isoformat() if entry.timestamp else 'Unknown',
                    'level': entry.level,
                    'source': entry.source,
                    'message': entry.message[:200]  # Truncate long messages
                })
        
        return timeline
    
    def find_correlations(self, log_entries: List) -> List[Dict]:
        """Find correlations between errors (e.g., errors happening together)"""
        # Group by timestamp (within 1 minute window)
        time_groups = defaultdict(list)
        
        for entry in log_entries:
            if entry.timestamp and entry.level in ['ERROR', 'CRITICAL']:
                # Round to nearest minute
                time_key = entry.timestamp.strftime('%Y-%m-%d %H:%M')
                time_groups[time_key].append(entry)
        
        # Find groups with multiple errors
        correlations = []
        for time_key, entries in time_groups.items():
            if len(entries) > 1:
                sources = [e.source for e in entries]
                correlations.append({
                    'timestamp': time_key,
                    'error_count': len(entries),
                    'affected_sources': list(set(sources)),
                    'messages': [e.message[:100] for e in entries[:3]]
                })
        
        return sorted(correlations, key=lambda x: x['error_count'], reverse=True)[:10]

