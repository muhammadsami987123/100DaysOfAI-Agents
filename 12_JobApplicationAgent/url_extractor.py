"""
URL extraction service for job descriptions
"""

import re
import logging
import requests
from typing import Optional, Dict, Any
from urllib.parse import urlparse
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class JobURLExtractor:
    """Extracts job descriptions from various job posting URLs"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive'
        })
        
        # Common job site patterns
        self.job_sites = {
            'linkedin': {
                'pattern': r'linkedin\.com/jobs',
                'selectors': [
                    '.job-description',
                    '.description__text',
                    '.show-more-less-html__markup',
                    '[data-job-description]'
                ]
            },
            'indeed': {
                'pattern': r'indeed\.com',
                'selectors': [
                    '#jobDescriptionText',
                    '.job-description',
                    '[data-testid="job-description"]'
                ]
            },
            'glassdoor': {
                'pattern': r'glassdoor\.com',
                'selectors': [
                    '.jobDescriptionContent',
                    '.desc',
                    '[data-test="job-description"]'
                ]
            },
            'monster': {
                'pattern': r'monster\.com',
                'selectors': [
                    '.job-description',
                    '.description',
                    '[data-testid="job-description"]'
                ]
            },
            'ziprecruiter': {
                'pattern': r'ziprecruiter\.com',
                'selectors': [
                    '.jobDescription',
                    '.description',
                    '[data-test="job-description"]'
                ]
            },
            'careerbuilder': {
                'pattern': r'careerbuilder\.com',
                'selectors': [
                    '.job-description',
                    '.description',
                    '[data-testid="job-description"]'
                ]
            }
        }
    
    def extract_job_description(self, url: str) -> Dict[str, Any]:
        """Extract job description from URL"""
        try:
            # Validate URL
            if not self._is_valid_url(url):
                return {
                    "success": False,
                    "error": "Invalid URL format"
                }
            
            # Fetch content
            try:
                response = self.session.get(url, timeout=15, allow_redirects=True)
            except requests.RequestException as e:
                logger.error(f"Request error for {url}: {e}")
                return {
                    "success": False,
                    "error": "Network error while fetching URL"
                }

            # Handle common block/authorization codes
            if response.status_code in (401, 403, 429, 999):
                return {
                    "success": False,
                    "error": "The site blocked the request or requires login (try a public job URL such as Indeed/Greenhouse/Lever)."
                }

            if response.status_code >= 400:
                return {
                    "success": False,
                    "error": f"Failed to fetch URL (status {response.status_code})"
                }

            content_type = response.headers.get('Content-Type', '')
            if 'text/html' not in content_type.lower():
                return {
                    "success": False,
                    "error": "Unsupported content type. Please provide a public HTML job posting URL."
                }
            
            # Parse content
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Try to identify the job site and extract content
            job_site = self._identify_job_site(url)
            if job_site:
                content = self._extract_from_job_site(soup, job_site)
            else:
                content = None
            
            # Generic fallbacks
            if not content:
                content = self._extract_generic(soup)
            if not content:
                content = self._extract_main_text(soup)
            
            if not content or len(content) < 80:
                return {
                    "success": False,
                    "error": "Could not extract job description from this URL (page may be behind login)."
                }
            
            # Clean and format content
            cleaned_content = self._clean_content(content)
            
            return {
                "success": True,
                "content": cleaned_content[:12000],  # guardrail
                "source_url": url,
                "job_site": job_site
            }
            
        except Exception as e:
            logger.error(f"Extraction failed for URL {url}: {e}")
            return {
                "success": False,
                "error": f"Extraction failed: {str(e)}"
            }
    
    def _is_valid_url(self, url: str) -> bool:
        """Validate URL format"""
        try:
            result = urlparse(url)
            return all([result.scheme in ("http", "https"), result.netloc])
        except Exception:
            return False
    
    def _identify_job_site(self, url: str) -> Optional[str]:
        """Identify which job site the URL belongs to"""
        url_lower = url.lower()
        for site_name, config in self.job_sites.items():
            if re.search(config['pattern'], url_lower):
                return site_name
        return None
    
    def _extract_from_job_site(self, soup: BeautifulSoup, site_name: str) -> Optional[str]:
        """Extract content using site-specific selectors"""
        selectors = self.job_sites[site_name]['selectors']
        
        for selector in selectors:
            try:
                element = soup.select_one(selector)
                if element:
                    text = element.get_text(separator='\n', strip=True)
                    if len(text) > 120:
                        return text
            except Exception as e:
                logger.warning(f"Selector {selector} failed for {site_name}: {e}")
                continue
        
        return None
    
    def _extract_generic(self, soup: BeautifulSoup) -> Optional[str]:
        """Generic extraction for unknown job sites"""
        # Remove script and style elements
        for script in soup(["script", "style", "noscript"]):
            script.decompose()
        
        # Try common job description containers
        candidates = []
        candidates.extend(soup.select('[id*="description" i], [class*="description" i]'))
        candidates.extend(soup.select('[id*="job" i][id*="content" i], [class*="job" i][class*="content" i]'))
        candidates.extend(soup.select('article, main, section'))
        
        best_text = None
        best_len = 0
        for el in candidates:
            try:
                text = el.get_text(separator='\n', strip=True)
                score = len(text)
                if score > best_len:
                    best_len = score
                    best_text = text
            except Exception:
                continue
        
        if best_text and best_len > 200:
            return best_text
        return None

    def _extract_main_text(self, soup: BeautifulSoup) -> Optional[str]:
        """Very broad fallback: concatenate paragraph text"""
        paragraphs = [p.get_text(separator=' ', strip=True) for p in soup.find_all('p')]
        text = '\n'.join([p for p in paragraphs if len(p) > 20])
        return text if len(text) > 120 else None
    
    def _clean_content(self, content: str) -> str:
        """Clean and format extracted content"""
        if not content:
            return ""
        
        # Remove common unwanted patterns
        unwanted_patterns = [
            r'cookie.*policy',
            r'privacy.*policy',
            r'terms.*of.*service',
            r'©.*all.*rights.*reserved',
            r'powered.*by',
            r'loading\.\.\.',
            r'javascript.*error',
            r'please.*enable.*javascript',
            r'sign in to.*',
            r'log in to.*'
        ]
        
        for pattern in unwanted_patterns:
            content = re.sub(pattern, '', content, flags=re.IGNORECASE)
        
        # Normalize whitespace
        content = re.sub(r'\s+\n', '\n', content)
        content = re.sub(r'\n{3,}', '\n\n', content)
        content = re.sub(r'[ \t]{2,}', ' ', content)
        content = content.strip()
        
        return content
    
    def get_supported_sites(self) -> Dict[str, str]:
        """Get list of supported job sites"""
        return {
            'linkedin': 'LinkedIn Jobs',
            'indeed': 'Indeed',
            'glassdoor': 'Glassdoor',
            'monster': 'Monster',
            'ziprecruiter': 'ZipRecruiter',
            'careerbuilder': 'CareerBuilder'
        }
