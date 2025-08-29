import os
import json
import logging
import requests
from typing import Dict, List, Optional
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import openai
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PortfolioAnalyzer:
    """Handles portfolio website analysis and feedback"""
    
    def __init__(self):
        """Initialize the portfolio analyzer"""
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def validate_url(self, url: str) -> str:
        """Validate and normalize URL"""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        try:
            parsed = urlparse(url)
            if not parsed.netloc:
                raise ValueError("Invalid URL format")
            return url
        except Exception as e:
            raise ValueError(f"Invalid URL: {str(e)}")
    
    def extract_website_content(self, url: str) -> Dict:
        """Extract content from website"""
        try:
            url = self.validate_url(url)
            
            # Fetch the main page
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract text content
            text_content = self._extract_text_content(soup)
            
            # Extract metadata
            metadata = self._extract_metadata(soup, url)
            
            # Extract links for further analysis
            links = self._extract_links(soup, url)
            
            # Analyze additional pages if available
            additional_pages = self._analyze_additional_pages(links, url)
            
            return {
                'url': url,
                'main_content': text_content,
                'metadata': metadata,
                'links': links,
                'additional_pages': additional_pages,
                'status_code': response.status_code,
                'content_length': len(response.content)
            }
            
        except Exception as e:
            logger.error(f"Error extracting website content: {e}")
            raise Exception(f"Failed to extract website content: {str(e)}")
    
    def _extract_text_content(self, soup: BeautifulSoup) -> str:
        """Extract meaningful text content from HTML"""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def _extract_metadata(self, soup: BeautifulSoup, url: str) -> Dict:
        """Extract metadata from HTML"""
        metadata = {
            'title': '',
            'description': '',
            'keywords': '',
            'author': '',
            'viewport': '',
            'robots': ''
        }
        
        # Title
        title_tag = soup.find('title')
        if title_tag:
            metadata['title'] = title_tag.get_text().strip()
        
        # Meta tags
        meta_tags = soup.find_all('meta')
        for meta in meta_tags:
            name = meta.get('name', '').lower()
            property = meta.get('property', '').lower()
            content = meta.get('content', '')
            
            if name == 'description' or property == 'og:description':
                metadata['description'] = content
            elif name == 'keywords':
                metadata['keywords'] = content
            elif name == 'author':
                metadata['author'] = content
            elif name == 'viewport':
                metadata['viewport'] = content
            elif name == 'robots':
                metadata['robots'] = content
        
        return metadata
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """Extract and categorize links"""
        links = []
        base_domain = urlparse(base_url).netloc
        
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            text = link.get_text().strip()
            
            if href:
                # Normalize URL
                if href.startswith('/'):
                    full_url = urljoin(base_url, href)
                elif href.startswith('http'):
                    full_url = href
                else:
                    full_url = urljoin(base_url, href)
                
                # Categorize link
                link_type = self._categorize_link(href, text, base_domain)
                
                links.append({
                    'url': full_url,
                    'text': text,
                    'type': link_type,
                    'is_internal': urlparse(full_url).netloc == base_domain
                })
        
        return links
    
    def _categorize_link(self, href: str, text: str, base_domain: str) -> str:
        """Categorize link based on URL and text"""
        href_lower = href.lower()
        text_lower = text.lower()
        
        if any(word in href_lower or word in text_lower for word in ['about', 'bio', 'profile']):
            return 'about'
        elif any(word in href_lower or word in text_lower for word in ['project', 'work', 'portfolio']):
            return 'projects'
        elif any(word in href_lower or word in text_lower for word in ['contact', 'email', 'phone']):
            return 'contact'
        elif any(word in href_lower or word in text_lower for word in ['resume', 'cv', 'experience']):
            return 'resume'
        elif any(word in href_lower or word in text_lower for word in ['blog', 'article', 'post']):
            return 'blog'
        elif any(word in href_lower for word in ['github', 'linkedin', 'twitter', 'facebook']):
            return 'social'
        else:
            return 'other'
    
    def _analyze_additional_pages(self, links: List[Dict], base_url: str) -> List[Dict]:
        """Analyze additional pages for comprehensive portfolio review"""
        additional_pages = []
        base_domain = urlparse(base_url).netloc
        
        # Focus on internal pages that are likely portfolio-related
        portfolio_links = [
            link for link in links 
            if link['is_internal'] and link['type'] in ['about', 'projects', 'resume']
        ][:Config.PORTFOLIO_ANALYSIS_DEPTH]
        
        for link in portfolio_links:
            try:
                response = self.session.get(link['url'], timeout=5)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    text_content = self._extract_text_content(soup)
                    
                    additional_pages.append({
                        'url': link['url'],
                        'type': link['type'],
                        'content': text_content[:1000],  # Limit content length
                        'status_code': response.status_code
                    })
            except Exception as e:
                logger.warning(f"Failed to analyze page {link['url']}: {e}")
        
        return additional_pages
    
    def analyze_portfolio(self, portfolio_url: str) -> Dict:
        """Analyze portfolio website using AI and return detailed feedback"""
        try:
            # Extract website content
            website_data = self.extract_website_content(portfolio_url)
            
            # Prepare content for analysis
            website_content = f"""
            URL: {website_data['url']}
            
            Main Content:
            {website_data['main_content'][:2000]}
            
            Metadata:
            Title: {website_data['metadata']['title']}
            Description: {website_data['metadata']['description']}
            
            Additional Pages:
            {self._format_additional_pages(website_data['additional_pages'])}
            
            Links Found: {len(website_data['links'])}
            Internal Links: {len([l for l in website_data['links'] if l['is_internal']])}
            External Links: {len([l for l in website_data['links'] if not l['is_internal']])}
            """
            
            # Prepare the prompt
            prompt = Config.PORTFOLIO_ANALYSIS_PROMPT.format(
                portfolio_url=portfolio_url,
                website_content=website_content
            )
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert web designer and UX consultant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=Config.OPENAI_MAX_TOKENS,
                temperature=Config.OPENAI_TEMPERATURE
            )
            
            # Parse the response
            content = response.choices[0].message.content
            
            try:
                # Find JSON in the response
                start_idx = content.find('{')
                end_idx = content.rfind('}') + 1
                json_str = content[start_idx:end_idx]
                analysis = json.loads(json_str)
            except json.JSONDecodeError:
                # If JSON parsing fails, create a structured response
                analysis = self._create_fallback_analysis(content, website_data)
            
            # Add website data to analysis
            analysis['website_data'] = {
                'url': website_data['url'],
                'content_length': website_data['content_length'],
                'pages_analyzed': len(website_data['additional_pages']) + 1,
                'links_count': len(website_data['links'])
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing portfolio: {e}")
            return self._create_error_analysis(str(e))
    
    def _format_additional_pages(self, pages: List[Dict]) -> str:
        """Format additional pages for analysis"""
        if not pages:
            return "No additional pages analyzed"
        
        formatted = []
        for page in pages:
            formatted.append(f"Page: {page['url']} ({page['type']})")
            formatted.append(f"Content: {page['content'][:500]}...")
            formatted.append("---")
        
        return "\n".join(formatted)
    
    def _create_fallback_analysis(self, content: str, website_data: Dict) -> Dict:
        """Create a fallback analysis when JSON parsing fails"""
        return {
            "overall_score": 7.0,
            "scores": {
                "design": 7,
                "usability": 7,
                "content": 7,
                "performance": 7,
                "mobile_responsiveness": 7,
                "professionalism": 7
            },
            "strengths": ["Portfolio website accessible"],
            "weaknesses": ["AI analysis encountered issues"],
            "suggestions": ["Please review the raw feedback below"],
            "technical_recommendations": ["Review content manually"],
            "raw_feedback": content
        }
    
    def _create_error_analysis(self, error_message: str) -> Dict:
        """Create an error analysis when portfolio analysis fails"""
        return {
            "overall_score": 0.0,
            "scores": {
                "design": 0,
                "usability": 0,
                "content": 0,
                "performance": 0,
                "mobile_responsiveness": 0,
                "professionalism": 0
            },
            "strengths": [],
            "weaknesses": [f"Analysis failed: {error_message}"],
            "suggestions": ["Please check the URL and try again"],
            "technical_recommendations": ["Verify website accessibility"],
            "error": True,
            "error_message": error_message
        }
    
    def save_analysis(self, analysis: Dict, filename: str) -> str:
        """Save analysis results to a JSON file"""
        try:
            output_path = os.path.join(Config.OUTPUT_FOLDER, f"{filename}_portfolio_analysis.json")
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            return output_path
        except Exception as e:
            logger.error(f"Error saving analysis: {e}")
            raise Exception(f"Failed to save analysis: {str(e)}")
    
    def get_analysis_summary(self, analysis: Dict) -> Dict:
        """Extract key summary information from analysis"""
        return {
            "overall_score": analysis.get("overall_score", 0),
            "top_strengths": analysis.get("strengths", [])[:3],
            "top_weaknesses": analysis.get("weaknesses", [])[:3],
            "key_suggestions": analysis.get("suggestions", [])[:3],
            "technical_recommendations": analysis.get("technical_recommendations", [])[:3],
            "has_error": analysis.get("error", False)
        }
