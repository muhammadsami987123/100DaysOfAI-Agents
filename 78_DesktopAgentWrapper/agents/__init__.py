"""
Agent wrapper system for DesktopAgentWrapper
"""

from .agent_base import BaseAgent
from .article_rewriter_wrapper import ArticleRewriterWrapper
from .story_writer_wrapper import StoryWriterWrapper
from .prompt_improver_wrapper import PromptImproverWrapper

__all__ = [
    'BaseAgent',
    'ArticleRewriterWrapper', 
    'StoryWriterWrapper',
    'PromptImproverWrapper'
]
