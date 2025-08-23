#!/usr/bin/env python3
"""
Demo script for AICommandExplainerAgent
Shows various features without requiring OpenAI API calls
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from rich.markdown import Markdown
import time

console = Console()

def print_demo_banner():
    """Print the demo banner."""
    banner_text = Text()
    banner_text.append("AICommandExplainerAgent ", style="bold cyan")
    banner_text.append("⚙️", style="bold yellow")
    banner_text.append("\n", style="bold cyan")
    banner_text.append("Demo Mode - Smart Terminal Command Interpreter", style="dim")
    
    console.print(Panel.fit(banner_text, border_style="cyan"))

def demo_command_explanation():
    """Demo the command explanation feature."""
    console.print("\n[bold blue]🔍 Command Explanation Demo[/bold blue]")
    
    demo_commands = [
        "rsync -avz folder/ user@host:/backup",
        "find . -name '*.py' -exec grep -l 'import' {} \\;",
        "tar -czf archive.tar.gz directory/",
        "ssh -i ~/.ssh/key.pem user@server.com"
    ]
    
    for cmd in demo_commands:
        console.print(f"\n[cyan]Command:[/cyan] {cmd}")
        
        # Simulate AI processing
        with console.status("[bold magenta]Analyzing command…[/bold magenta]", spinner="dots12"):
            time.sleep(1)
        
        # Show example explanation
        explanation = f"""
**Command Overview**: {cmd.split()[0]} - {get_command_description(cmd.split()[0])}

**Flag Breakdown**:
{get_flag_explanation(cmd)}

**Arguments**: {get_argument_explanation(cmd)}

**What Happens**: {get_what_happens(cmd)}

**Safety Notes**: {get_safety_notes(cmd)}

**Examples**:
{get_examples(cmd)}
        """
        
        console.print(Panel(Markdown(explanation), title="AI Explanation", border_style="cyan"))

def demo_command_suggestion():
    """Demo the command suggestion feature."""
    console.print("\n[bold blue]💡 Command Suggestion Demo[/bold blue]")
    
    suggestions = [
        ("copy all .txt files to another folder", "cp *.txt /target/folder/"),
        ("find files modified in last 24 hours", "find . -mtime -1"),
        ("compress a directory into tar.gz", "tar -czf archive.tar.gz directory/"),
        ("check disk usage by directory", "du -h --max-depth=1")
    ]
    
    for request, command in suggestions:
        console.print(f"\n[cyan]Request:[/cyan] {request}")
        
        with console.status("[bold magenta]Generating suggestion…[/bold magenta]", spinner="dots12"):
            time.sleep(1)
        
        suggestion_text = f"""
**Suggested Command**: `{command}`

**What It Does**: {get_suggestion_explanation(request)}

**Why This Command**: {get_why_this_command(request, command)}

**Safety Notes**: {get_suggestion_safety(request)}

**Alternative Options**: {get_alternatives(request)}
        """
        
        console.print(Panel(Markdown(suggestion_text), title="Command Suggestion", border_style="green"))

def demo_quick_analysis():
    """Demo the quick analysis feature."""
    console.print("\n[bold blue]⚡ Quick Analysis Demo[/bold blue]")
    
    commands = [
        "rm -rf /tmp/*",
        "chmod 777 file.txt",
        "sudo rm -rf /",
        "cp -r source/ destination/"
    ]
    
    for cmd in commands:
        console.print(f"\n[cyan]Analyzing:[/cyan] {cmd}")
        
        summary = get_command_summary(cmd)
        table = Table(title=f"Quick Analysis: {cmd}", show_header=True, header_style="bold magenta")
        table.add_column("Component", style="cyan", no_wrap=True)
        table.add_column("Details", style="white")
        
        table.add_row("Main Command", summary.get("main_command", "N/A"))
        table.add_row("Flags", ", ".join(summary.get("flags", [])) or "None")
        table.add_row("Arguments", ", ".join(summary.get("arguments", [])) or "None")
        table.add_row("Total Parts", str(summary.get("total_parts", 0)))
        
        if summary.get("is_dangerous"):
            table.add_row("⚠️  Safety", "DANGEROUS COMMAND DETECTED", style="bold red")
            table.add_row("Dangerous Patterns", ", ".join(summary.get("dangerous_flags", [])), style="bold red")
        else:
            table.add_row("✅ Safety", "Command appears safe")
        
        console.print(table)

def demo_safety_features():
    """Demo the safety features."""
    console.print("\n[bold blue]🛡️ Safety Features Demo[/bold blue]")
    
    dangerous_commands = [
        "rm -rf /",
        ":(){ :|:& };:",
        "chmod 777 -R /",
        "sudo rm -rf /*"
    ]
    
    for cmd in dangerous_commands:
        console.print(f"\n[red]⚠️  DANGEROUS COMMAND DETECTED:[/red] {cmd}")
        
        warning_text = f"""
**🚨 IMMEDIATE WARNING** 🚨

This command is extremely dangerous and could:
- Delete your entire system
- Corrupt your data
- Cause irreversible damage
- Require system reinstallation

**DO NOT RUN THIS COMMAND!**

**Safer Alternatives**:
{get_safer_alternatives(cmd)}

**What You Probably Want**:
{get_what_you_probably_want(cmd)}
        """
        
        console.print(Panel(warning_text, title="⚠️  SAFETY WARNING", border_style="red"))

def get_command_description(command):
    """Get a description for a command."""
    descriptions = {
        "rsync": "Remote synchronization tool for copying files",
        "find": "Search for files in directory hierarchy",
        "tar": "Tape archive utility for creating/extracting archives",
        "ssh": "Secure shell for remote login and file transfer",
        "cp": "Copy files and directories",
        "rm": "Remove files and directories",
        "chmod": "Change file permissions"
    }
    return descriptions.get(command, "Command utility")

def get_flag_explanation(command):
    """Get flag explanations for a command."""
    if "rsync" in command:
        return "-a: Archive mode (preserves permissions, links, etc.)\n-v: Verbose output\n-z: Compress during transfer"
    elif "find" in command:
        return "-name: Search by filename pattern\n-exec: Execute command on found files"
    elif "tar" in command:
        return "-c: Create archive\n-z: Compress with gzip\n-f: Specify archive filename"
    elif "ssh" in command:
        return "-i: Specify identity file (private key)"
    else:
        return "Various flags for command-specific options"

def get_argument_explanation(command):
    """Get argument explanations for a command."""
    parts = command.split()
    if len(parts) > 1:
        return f"Arguments: {' '.join(parts[1:])}"
    return "No additional arguments"

def get_what_happens(command):
    """Get what happens when command runs."""
    if "rsync" in command:
        return "Files will be copied from source to destination with compression and progress display"
    elif "find" in command:
        return "Will search through directories and execute commands on matching files"
    elif "tar" in command:
        return "Will create a compressed archive of the specified directory"
    elif "ssh" in command:
        return "Will establish a secure connection to the remote server using the specified key"
    else:
        return "Command will execute with the specified parameters"

def get_safety_notes(command):
    """Get safety notes for a command."""
    if "rm" in command or "del" in command:
        return "⚠️  Deletion commands - ensure you have backups and double-check paths"
    elif "chmod" in command:
        return "⚠️  Permission changes - be careful with 777 permissions"
    elif "ssh" in command:
        return "✅ Generally safe - just ensure you trust the destination server"
    else:
        return "✅ Command appears safe when used correctly"

def get_examples(command):
    """Get examples for a command."""
    if "rsync" in command:
        return "rsync -avz /local/folder/ user@server:/backup/\nrsync -avz --delete source/ dest/"
    elif "find" in command:
        return "find . -name '*.txt' -delete\nfind /var/log -mtime +7 -delete"
    elif "tar" in command:
        return "tar -czf backup.tar.gz /home/user/\ntar -xzf archive.tar.gz"
    else:
        return "Command examples would be shown here"

def get_suggestion_explanation(request):
    """Get explanation for a suggestion request."""
    if "copy" in request.lower():
        return "Copies files from one location to another"
    elif "find" in request.lower():
        return "Searches for files based on criteria"
    elif "compress" in request.lower():
        return "Creates a compressed archive"
    elif "check disk" in request.lower():
        return "Shows disk usage information"
    else:
        return "Performs the requested operation"

def get_why_this_command(request, command):
    """Get why a specific command was suggested."""
    if "copy" in request.lower():
        return "cp is the standard Unix/Linux copy command, simple and reliable"
    elif "find" in request.lower():
        return "find is the most powerful file search utility with many options"
    elif "tar" in request.lower():
        return "tar is the standard archive format, widely supported"
    elif "du" in request.lower():
        return "du (disk usage) is the standard tool for checking directory sizes"
    else:
        return "This command is the most appropriate for the task"

def get_suggestion_safety(request):
    """Get safety notes for a suggestion."""
    if "delete" in request.lower() or "remove" in request.lower():
        return "⚠️  Be careful with deletion commands - always verify before running"
    elif "permission" in request.lower() or "chmod" in request.lower():
        return "⚠️  Permission changes can affect system security"
    else:
        return "✅ Generally safe operation"

def get_alternatives(request):
    """Get alternative approaches."""
    if "copy" in request.lower():
        return "rsync (with progress), scp (remote), or GUI file manager"
    elif "find" in request.lower():
        return "locate (faster), grep (content search), or GUI search tools"
    elif "compress" in request.lower():
        return "zip, 7z, or GUI compression tools"
    else:
        return "Various alternative approaches available"

def get_command_summary(command):
    """Get a command summary for analysis."""
    parts = command.strip().split()
    if not parts:
        return {"error": "Empty command"}
    
    main_command = parts[0]
    flags = [part for part in parts[1:] if part.startswith('-')]
    arguments = [part for part in parts[1:] if not part.startswith('-')]
    
    # Check if dangerous
    dangerous_patterns = ['rm -rf', 'chmod 777', 'sudo rm', 'del /s']
    is_dangerous = any(pattern in command.lower() for pattern in dangerous_patterns)
    dangerous_flags = [pattern for pattern in dangerous_patterns if pattern in command.lower()]
    
    return {
        "main_command": main_command,
        "flags": flags,
        "arguments": arguments,
        "is_dangerous": is_dangerous,
        "dangerous_flags": dangerous_flags,
        "total_parts": len(parts)
    }

def get_safer_alternatives(command):
    """Get safer alternatives for dangerous commands."""
    if "rm -rf" in command:
        return "• Use 'rm -i' for interactive deletion\n• Use 'trash' command for reversible deletion\n• Use GUI file manager"
    elif "chmod 777" in command:
        return "• Use 'chmod 644' for files\n• Use 'chmod 755' for directories\n• Only change permissions you understand"
    elif "sudo rm" in command:
        return "• Avoid using sudo with rm\n• Use 'sudo trash' instead\n• Double-check paths before running"
    else:
        return "• Use safer alternatives\n• Test in safe environment first\n• Always have backups"

def get_what_you_probably_want(command):
    """Get what the user probably wants instead."""
    if "rm -rf" in command:
        return "• Delete specific files: 'rm filename'\n• Delete empty directory: 'rmdir directory'\n• List what would be deleted: 'ls -la path'"
    elif "chmod 777" in command:
        return "• Make file readable: 'chmod 644 file'\n• Make directory accessible: 'chmod 755 dir'\n• Check current permissions: 'ls -la'"
    elif "sudo rm" in command:
        return "• Remove as regular user if possible\n• Use 'sudo trash' for system files\n• Check if file is really needed"
    else:
        return "• Use the specific command for your needs\n• Check command help: 'command --help'\n• Test in safe environment"

def main():
    """Run the demo."""
    print_demo_banner()
    
    console.print("\n[dim]This demo shows the AICommandExplainerAgent's capabilities without requiring an OpenAI API key.[/dim]")
    console.print("[dim]In the real application, these explanations would be generated by AI.[/dim]")
    
    # Run all demos
    demo_command_explanation()
    demo_command_suggestion()
    demo_quick_analysis()
    demo_safety_features()
    
    console.print("\n[bold green]🎉 Demo Complete![/bold green]")
    console.print("\n[dim]To use the real AI-powered agent:[/dim]")
    console.print("1. Set up your OpenAI API key in .env file")
    console.print("2. Run: python main.py")
    console.print("3. Enjoy intelligent command explanations! 🚀")

if __name__ == "__main__":
    main()
