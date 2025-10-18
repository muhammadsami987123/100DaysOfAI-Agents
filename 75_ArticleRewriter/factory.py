"""
Factory module for ArticleRewriter
Creates and configures the application instance
"""

from main import app
from agents.article_rewriter_agent import ArticleRewriterAgent
from config import Config

def create_app():
    """Create and configure the ArticleRewriter application"""
    return app

def create_agent():
    """Create and configure the ArticleRewriterAgent"""
    return ArticleRewriterAgent()

def get_config():
    """Get the application configuration"""
    return Config

if __name__ == "__main__":
    # Run the application
    import uvicorn
    uvicorn.run(
        "main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=Config.DEBUG,
        log_level="info"
    )
