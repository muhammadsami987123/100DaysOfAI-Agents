"""
Main entry point for DesktopAgentWrapper
"""

import os
import sys
import logging
from typing import Dict, Any, Optional
import customtkinter as ctk

from desktop_gui import DesktopAgentWrapper
from config import Config
from agents import (
    ArticleRewriterWrapper,
    StoryWriterWrapper, 
    PromptImproverWrapper
)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AgentSelector:
    """Agent selection dialog"""
    
    def __init__(self):
        self.selected_agent = None
        self.root = None
        
    def show_selection_dialog(self) -> Optional[str]:
        """Show agent selection dialog"""
        self.root = ctk.CTk()
        self.root.title("Select Agent")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (500 // 2)
        self.root.geometry(f"600x500+{x}+{y}")
        
        # Create main frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="DesktopAgentWrapper",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Select an AI agent to run:",
            font=ctk.CTkFont(size=16)
        )
        subtitle_label.pack(pady=10)
        
        # Agent selection frame
        selection_frame = ctk.CTkFrame(main_frame)
        selection_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Available agents
        agents = {
            "ArticleRewriter": {
                "description": "AI-powered content rewriting tool with multiple tone options",
                "icon": "📝",
                "wrapper": ArticleRewriterWrapper
            },
            "StoryWriter": {
                "description": "AI-powered creative story generation tool",
                "icon": "📚",
                "wrapper": StoryWriterWrapper
            },
            "PromptImprover": {
                "description": "AI-powered prompt optimization and enhancement tool",
                "icon": "🔧",
                "wrapper": PromptImproverWrapper
            }
        }
        
        # Create agent buttons
        self.agent_buttons = {}
        for agent_name, agent_info in agents.items():
            agent_frame = ctk.CTkFrame(selection_frame)
            agent_frame.pack(fill="x", padx=10, pady=5)
            
            # Agent button
            agent_button = ctk.CTkButton(
                agent_frame,
                text=f"{agent_info['icon']} {agent_name}",
                command=lambda name=agent_name: self._select_agent(name),
                height=60,
                font=ctk.CTkFont(size=16, weight="bold")
            )
            agent_button.pack(fill="x", padx=10, pady=10)
            
            # Agent description
            desc_label = ctk.CTkLabel(
                agent_frame,
                text=agent_info["description"],
                font=ctk.CTkFont(size=12),
                wraplength=500
            )
            desc_label.pack(pady=(0, 10))
            
            self.agent_buttons[agent_name] = agent_button
        
        # Close button
        close_button = ctk.CTkButton(
            main_frame,
            text="Close",
            command=self._close_dialog,
            width=100
        )
        close_button.pack(pady=20)
        
        # Start the dialog
        self.root.mainloop()
        
        return self.selected_agent
    
    def _select_agent(self, agent_name: str):
        """Select an agent"""
        self.selected_agent = agent_name
        self.root.destroy()
    
    def _close_dialog(self):
        """Close the dialog"""
        self.selected_agent = None
        self.root.destroy()

def create_agent_wrapper(agent_name: str) -> Optional[DesktopAgentWrapper]:
    """Create agent wrapper based on selection"""
    agent_wrappers = {
        "ArticleRewriter": ArticleRewriterWrapper,
        "StoryWriter": StoryWriterWrapper,
        "PromptImprover": PromptImproverWrapper
    }
    
    if agent_name not in agent_wrappers:
        logger.error(f"Unknown agent: {agent_name}")
        return None
    
    try:
        wrapper_class = agent_wrappers[agent_name]
        wrapper_instance = wrapper_class()
        
        # Create DesktopAgentWrapper
        desktop_wrapper = DesktopAgentWrapper(
            agent_class=wrapper_instance.agent_class,
            agent_name=wrapper_instance.agent_name,
            description=wrapper_instance.description,
            ui_config=wrapper_instance.get_ui_config()
        )
        
        return desktop_wrapper
        
    except Exception as e:
        logger.error(f"Failed to create agent wrapper: {e}")
        return None

def main():
    """Main application entry point"""
    try:
        # Validate configuration
        if not Config.validate():
            logger.error("Configuration validation failed")
            return 1
        
        # Show agent selection dialog
        selector = AgentSelector()
        selected_agent = selector.show_selection_dialog()
        
        if not selected_agent:
            logger.info("No agent selected, exiting")
            return 0
        
        # Create agent wrapper
        desktop_wrapper = create_agent_wrapper(selected_agent)
        if not desktop_wrapper:
            logger.error(f"Failed to create wrapper for {selected_agent}")
            return 1
        
        # Run the desktop application
        logger.info(f"Starting desktop application for {selected_agent}")
        desktop_wrapper.run()
        
        return 0
        
    except Exception as e:
        logger.error(f"Application error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
