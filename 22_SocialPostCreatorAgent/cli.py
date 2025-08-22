import argparse
import sys
from datetime import datetime
from pathlib import Path
import pyperclip

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich.markdown import Markdown
from rich.syntax import Syntax

from config import Config
from search_service import fetch_latest_insights
from ai_service import generate_social_post
from poster import save_post_to_file

console = Console()


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="SocialPostCreatorAgent – Generate AI-crafted social media posts for multiple platforms.",
    )
    parser.add_argument("--platform", required=False, help='Platform (Twitter, Facebook, Instagram, LinkedIn, TikTok, YouTube)')
    parser.add_argument("--topic", required=False, help='Topic to post about (e.g., "AI in Education")')
    parser.add_argument("--tone", required=False, default="professional", help='Tone (e.g., professional, casual, witty, inspirational)')
    parser.add_argument("--save", action="store_true", help="Save post to local folder")
    parser.add_argument("--copy", action="store_true", help="Copy post to clipboard")
    parser.add_argument("--non-interactive", action="store_true", help="Skip interactive prompts")
    return parser.parse_args(argv)


def get_available_platforms():
    """Get list of available platforms from config"""
    return list(Config.PLATFORM_LIMITS.keys())


def get_available_tones():
    """Get list of available tones"""
    return ["professional", "casual", "witty", "inspirational", "friendly", "authoritative", "playful"]


def interactive_collect(args):
    """Collect user input interactively"""
    # Platform selection
    if args.platform:
        platform = args.platform
        if platform not in get_available_platforms():
            console.print(f"[red]Invalid platform: {platform}[/red]")
            platform = Prompt.ask(
                "Choose Platform", 
                choices=get_available_platforms(), 
                default=Config.DEFAULT_PLATFORM
            )
    else:
        platform = Prompt.ask(
            "Choose Platform", 
            choices=get_available_platforms(), 
            default=Config.DEFAULT_PLATFORM
        )
    
    # Topic input
    topic = args.topic or Prompt.ask("Enter Topic", default="AI in Education")
    
    # Tone selection
    if args.tone:
        tone = args.tone
        if tone not in get_available_tones():
            console.print(f"[red]Invalid tone: {tone}[/red]")
            tone = Prompt.ask("Select Tone", choices=get_available_tones(), default="professional")
    else:
        tone = Prompt.ask("Select Tone", choices=get_available_tones(), default="professional")
    
    # Action preferences
    save_post = args.save or Confirm.ask("Save post to local folder?", default=True)
    copy_to_clipboard = args.copy or Confirm.ask("Copy post to clipboard?", default=True)
    
    return platform, topic, tone, save_post, copy_to_clipboard


def render_overview(platform: str, topic: str, tone: str, char_limit: int):
    """Display overview of the post generation request"""
    table = Table(title="Post Generation Overview", show_lines=True)
    table.add_column("Field", style="bold cyan", no_wrap=True)
    table.add_column("Value", style="white")
    table.add_row("Platform", platform)
    table.add_row("Topic", topic)
    table.add_row("Tone", tone)
    table.add_row("Character Limit", str(char_limit))
    
    console.print(Panel.fit(table, title="SocialPostCreatorAgent", border_style="green"))


def display_generated_post(platform: str, topic: str, tone: str, post_text: str, char_limit: int):
    """Display the generated post with formatting"""
    char_count = len(post_text)
    char_status = "✅" if char_count <= char_limit else "⚠️"
    
    # Create a nice display panel
    content = f"""
[bold cyan]Generated {platform} Post[/bold cyan]

[white]{post_text}[/white]

[dim]Character count: {char_count}/{char_limit} {char_status}[/dim]
[dim]Platform: {platform} | Tone: {tone}[/dim]
[dim]Topic: {topic}[/dim]
"""
    
    console.print(Panel.fit(content, title="🎯 Your Post is Ready!", border_style="blue"))


def main(argv=None):
    args = parse_args(argv or sys.argv[1:])

    # Preflight: require OpenAI API key
    if not Config.OPENAI_API_KEY:
        console.print(Panel.fit(
            Text("Missing OPENAI_API_KEY. Set it in environment or .env."), 
            border_style="red"
        ))
        return 2

    # Welcome message
    console.print(Panel.fit(
        Text("Welcome to SocialPostCreatorAgent 💬", style="bold green"), 
        border_style="green"
    ))

    # Collect user input
    platform, topic, tone, save_post, copy_to_clipboard = interactive_collect(args)
    
    # Get platform character limit
    char_limit = Config.PLATFORM_LIMITS.get(platform, 280)
    
    # Show overview
    render_overview(platform, topic, tone, char_limit)
    
    # Confirm generation
    if not args.non_interactive:
        if not Confirm.ask("Generate this post?", default=True):
            console.print("Aborted.")
            return 1

    # Generate post
    console.print("\n[bold yellow]Generating post...[/bold yellow]")
    
    try:
        insights = fetch_latest_insights(topic)
        post_text = generate_social_post(platform, topic, tone, insights)
        
        # Display the generated post
        display_generated_post(platform, topic, tone, post_text, char_limit)
        
        # Handle copy to clipboard
        if copy_to_clipboard:
            try:
                pyperclip.copy(post_text)
                console.print("[green]✅ Post copied to clipboard![/green]")
            except Exception as e:
                console.print(f"[yellow]⚠️ Could not copy to clipboard: {e}[/yellow]")
        
        # Handle save to file
        if save_post:
            try:
                filepath = save_post_to_file(post_text, platform, topic, tone)
                console.print(f"[green]📁 Post saved to: {filepath}[/green]")
            except Exception as e:
                console.print(f"[red]❌ Error saving post: {e}[/red]")
        
        # Final actions
        if not args.non_interactive:
            console.print("\n[bold]What would you like to do next?[/bold]")
            actions = []
            if not copy_to_clipboard:
                actions.append("Copy to clipboard")
            if not save_post:
                actions.append("Save to file")
            actions.append("Generate another post")
            actions.append("Exit")
            
            choice = Prompt.ask("Choose action", choices=actions, default="Exit")
            
            if choice == "Copy to clipboard":
                try:
                    pyperclip.copy(post_text)
                    console.print("[green]✅ Post copied to clipboard![/green]")
                except Exception as e:
                    console.print(f"[yellow]⚠️ Could not copy to clipboard: {e}[/yellow]")
            elif choice == "Save to file":
                try:
                    filepath = save_post_to_file(post_text, platform, topic, tone)
                    console.print(f"[green]📁 Post saved to: {filepath}[/green]")
                except Exception as e:
                    console.print(f"[red]❌ Error saving post: {e}[/red]")
            elif choice == "Generate another post":
                # Recursive call for another post
                return main([])
        
        return 0
        
    except Exception as e:
        console.print(Panel.fit(
            Text(f"Error generating post: {e}", style="red"), 
            border_style="red"
        ))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())


