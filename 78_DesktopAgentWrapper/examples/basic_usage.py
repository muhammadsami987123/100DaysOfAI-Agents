"""
Basic usage example for DesktopAgentWrapper
"""

from desktop_gui import DesktopAgentWrapper
from agents import ArticleRewriterWrapper

def main():
    """Basic usage example"""
    
    # Create an ArticleRewriter wrapper
    article_wrapper = ArticleRewriterWrapper()
    
    # Create desktop wrapper
    desktop_wrapper = DesktopAgentWrapper(
        agent_class=article_wrapper.agent_class,
        agent_name=article_wrapper.agent_name,
        description=article_wrapper.description,
        ui_config=article_wrapper.get_ui_config()
    )
    
    # Run the desktop application
    desktop_wrapper.run()

if __name__ == "__main__":
    main()
