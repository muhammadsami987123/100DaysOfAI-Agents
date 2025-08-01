#!/usr/bin/env python3
"""
🤖 TodoAgent - Day 1 of #100DaysOfAI-Agents

A smart todo management agent that understands natural language commands
and manages tasks with priority levels, due dates, categories, and status tracking.

Features:
- Natural language processing with OpenAI GPT
- CRUD operations (Create, Read, Update, Delete)
- Priority levels (High, Medium, Low)
- Due dates and reminders
- Categories and tags
- Status tracking (Pending, In Progress, Completed)
- Persistent JSON storage
- Interactive CLI interface

Author: Muhammad Sami Asghar Mughal
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import openai
from colorama import init, Fore, Back, Style
from config import get_api_key, setup_instructions

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class TodoAgent:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the TodoAgent with OpenAI API key and load existing todos."""
        self.api_key = api_key or get_api_key()
        if not self.api_key:
            print(f"{Fore.RED}❌ Error: OpenAI API key not found!")
            print()
            setup_instructions()
            sys.exit(1)
        self.todos_file = "todos.json"
        self.todos = self.load_todos()
        self.categories = ["work", "personal", "shopping", "health", "learning", "other"]
        self.priorities = ["high", "medium", "low"]
        self.statuses = ["pending", "in_progress", "completed"]
        
    def load_todos(self) -> List[Dict[str, Any]]:
        """Load todos from JSON file."""
        try:
            if os.path.exists(self.todos_file):
                with open(self.todos_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"{Fore.RED}❌ Error loading todos: {e}")
        return []
    
    def save_todos(self):
        """Save todos to JSON file."""
        try:
            with open(self.todos_file, 'w', encoding='utf-8') as f:
                json.dump(self.todos, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"{Fore.RED}❌ Error saving todos: {e}")
    
    def parse_natural_language(self, command: str) -> Dict[str, Any]:
        """Use OpenAI GPT to parse natural language commands into structured data."""
        try:
            system_prompt = """You are a todo management assistant. Parse the user's natural language command and return a JSON object with the following structure:

{
    "action": "add|list|update|delete|mark|search",
    "task": "task description",
    "priority": "high|medium|low",
    "category": "work|personal|shopping|health|learning|other",
    "due_date": "YYYY-MM-DD",
    "status": "pending|in_progress|completed",
    "task_id": null,
    "search_term": null
}

Rules:
- For "add" action: extract task, priority, category, due_date
- For "list" action: just return {"action": "list"}
- For "update" action: extract task_id and fields to update
- For "delete" action: extract task_id
- For "mark" action: extract task_id and status
- For "search" action: extract search_term
- If due_date is mentioned as "tomorrow", "next week", etc., convert to YYYY-MM-DD
- If priority is mentioned as "urgent", "important", "low priority", etc., map to high/medium/low
- If no specific values are provided, use null

Examples:
- "add buy groceries" → {"action": "add", "task": "buy groceries", "priority": null, "category": null, "due_date": null, "status": "pending", "task_id": null, "search_term": null}
- "add urgent meeting with client tomorrow" → {"action": "add", "task": "meeting with client", "priority": "high", "category": "work", "due_date": "2024-01-16", "status": "pending", "task_id": null, "search_term": null}
- "mark task 1 as completed" → {"action": "mark", "task": null, "priority": null, "category": null, "due_date": null, "status": "completed", "task_id": 1, "search_term": null}
- "delete task 3" → {"action": "delete", "task": null, "priority": null, "category": null, "due_date": null, "status": null, "task_id": 3, "search_term": null}
- "search groceries" → {"action": "search", "task": null, "priority": null, "category": null, "due_date": null, "status": null, "task_id": null, "search_term": "groceries"}

Return only the JSON object, no additional text."""

            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": command}
                ],
                temperature=0.1,
                max_tokens=200
            )
            
            result = json.loads(response.choices[0].message.content.strip())
            return result
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error parsing command: {e}")
            return {"action": "error", "error": str(e)}
    
    def add_todo(self, task: str, priority: str = "medium", category: str = "other", 
                 due_date: Optional[str] = None, status: str = "pending") -> bool:
        """Add a new todo item."""
        try:
            # Validate due date format
            if due_date:
                datetime.strptime(due_date, "%Y-%m-%d")
            
            todo = {
                "id": len(self.todos) + 1,
                "task": task,
                "priority": priority,
                "category": category,
                "due_date": due_date,
                "status": status,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            self.todos.append(todo)
            self.save_todos()
            
            print(f"{Fore.GREEN}✅ Added todo: {task}")
            self.display_todo(todo)
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error adding todo: {e}")
            return False
    
    def list_todos(self, filter_status: Optional[str] = None, 
                   filter_category: Optional[str] = None, 
                   filter_priority: Optional[str] = None):
        """List all todos with optional filtering."""
        filtered_todos = self.todos.copy()
        
        if filter_status:
            filtered_todos = [t for t in filtered_todos if t["status"] == filter_status]
        if filter_category:
            filtered_todos = [t for t in filtered_todos if t["category"] == filter_category]
        if filter_priority:
            filtered_todos = [t for t in filtered_todos if t["priority"] == filter_priority]
        
        if not filtered_todos:
            print(f"{Fore.YELLOW}📝 No todos found.")
            return
        
        print(f"{Fore.CYAN}📋 Your Todos ({len(filtered_todos)} items):")
        print("-" * 80)
        
        for todo in filtered_todos:
            self.display_todo(todo)
    
    def display_todo(self, todo: Dict[str, Any]):
        """Display a single todo item with color coding."""
        # Priority colors
        priority_colors = {
            "high": Fore.RED,
            "medium": Fore.YELLOW,
            "low": Fore.GREEN
        }
        
        # Status colors
        status_colors = {
            "pending": Fore.YELLOW,
            "in_progress": Fore.BLUE,
            "completed": Fore.GREEN
        }
        
        # Status symbols
        status_symbols = {
            "pending": "⏳",
            "in_progress": "🔄",
            "completed": "✅"
        }
        
        priority_color = priority_colors.get(todo["priority"], Fore.WHITE)
        status_color = status_colors.get(todo["status"], Fore.WHITE)
        status_symbol = status_symbols.get(todo["status"], "❓")
        
        print(f"{Fore.CYAN}[{todo['id']:2d}] {status_symbol} {todo['task']}")
        print(f"     {Fore.WHITE}Priority: {priority_color}{todo['priority'].upper()}")
        print(f"     {Fore.WHITE}Category: {Fore.MAGENTA}{todo['category']}")
        print(f"     {Fore.WHITE}Status: {status_color}{todo['status'].replace('_', ' ').title()}")
        
        if todo["due_date"]:
            due_date = datetime.strptime(todo["due_date"], "%Y-%m-%d")
            today = datetime.now().date()
            if due_date.date() < today:
                print(f"     {Fore.WHITE}Due: {Fore.RED}{todo['due_date']} (OVERDUE!)")
            elif due_date.date() == today:
                print(f"     {Fore.WHITE}Due: {Fore.YELLOW}{todo['due_date']} (TODAY!)")
            else:
                print(f"     {Fore.WHITE}Due: {Fore.GREEN}{todo['due_date']}")
        
        print()
    
    def update_todo(self, task_id: int, **kwargs) -> bool:
        """Update a todo item."""
        try:
            todo = next((t for t in self.todos if t["id"] == task_id), None)
            if not todo:
                print(f"{Fore.RED}❌ Todo with ID {task_id} not found.")
                return False
            
            # Update fields
            for key, value in kwargs.items():
                if key in todo and value is not None:
                    todo[key] = value
            
            todo["updated_at"] = datetime.now().isoformat()
            self.save_todos()
            
            print(f"{Fore.GREEN}✅ Updated todo {task_id}")
            self.display_todo(todo)
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error updating todo: {e}")
            return False
    
    def delete_todo(self, task_id: int) -> bool:
        """Delete a todo item."""
        try:
            todo = next((t for t in self.todos if t["id"] == task_id), None)
            if not todo:
                print(f"{Fore.RED}❌ Todo with ID {task_id} not found.")
                return False
            
            self.todos = [t for t in self.todos if t["id"] != task_id]
            self.save_todos()
            
            print(f"{Fore.GREEN}✅ Deleted todo: {todo['task']}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error deleting todo: {e}")
            return False
    
    def mark_todo(self, task_id: int, status: str) -> bool:
        """Mark a todo as completed, in progress, or pending."""
        return self.update_todo(task_id, status=status)
    
    def search_todos(self, search_term: str):
        """Search todos by task description."""
        matching_todos = [
            todo for todo in self.todos 
            if search_term.lower() in todo["task"].lower()
        ]
        
        if not matching_todos:
            print(f"{Fore.YELLOW}🔍 No todos found matching '{search_term}'")
            return
        
        print(f"{Fore.CYAN}🔍 Search results for '{search_term}' ({len(matching_todos)} items):")
        print("-" * 80)
        
        for todo in matching_todos:
            self.display_todo(todo)
    
    def get_statistics(self):
        """Display todo statistics."""
        total = len(self.todos)
        completed = len([t for t in self.todos if t["status"] == "completed"])
        pending = len([t for t in self.todos if t["status"] == "pending"])
        in_progress = len([t for t in self.todos if t["status"] == "in_progress"])
        
        print(f"{Fore.CYAN}📊 Todo Statistics:")
        print(f"{Fore.WHITE}Total todos: {Fore.CYAN}{total}")
        print(f"{Fore.WHITE}Completed: {Fore.GREEN}{completed}")
        print(f"{Fore.WHITE}Pending: {Fore.YELLOW}{pending}")
        print(f"{Fore.WHITE}In Progress: {Fore.BLUE}{in_progress}")
        
        if total > 0:
            completion_rate = (completed / total) * 100
            print(f"{Fore.WHITE}Completion rate: {Fore.CYAN}{completion_rate:.1f}%")
    
    def process_command(self, command: str):
        """Process natural language command using GPT parsing."""
        print(f"{Fore.CYAN}🤖 Processing: {command}")
        
        # Parse the command
        parsed = self.parse_natural_language(command)
        
        if parsed.get("action") == "error":
            print(f"{Fore.RED}❌ Could not understand command. Please try again.")
            return
        
        action = parsed["action"]
        
        try:
            if action == "add":
                self.add_todo(
                    task=parsed["task"],
                    priority=parsed["priority"] or "medium",
                    category=parsed["category"] or "other",
                    due_date=parsed["due_date"],
                    status=parsed["status"] or "pending"
                )
            
            elif action == "list":
                self.list_todos()
            
            elif action == "update":
                if parsed["task_id"]:
                    update_data = {}
                    if parsed["task"]: update_data["task"] = parsed["task"]
                    if parsed["priority"]: update_data["priority"] = parsed["priority"]
                    if parsed["category"]: update_data["category"] = parsed["category"]
                    if parsed["due_date"]: update_data["due_date"] = parsed["due_date"]
                    
                    self.update_todo(parsed["task_id"], **update_data)
                else:
                    print(f"{Fore.RED}❌ Please specify a task ID to update.")
            
            elif action == "delete":
                if parsed["task_id"]:
                    self.delete_todo(parsed["task_id"])
                else:
                    print(f"{Fore.RED}❌ Please specify a task ID to delete.")
            
            elif action == "mark":
                if parsed["task_id"] and parsed["status"]:
                    self.mark_todo(parsed["task_id"], parsed["status"])
                else:
                    print(f"{Fore.RED}❌ Please specify a task ID and status.")
            
            elif action == "search":
                if parsed["search_term"]:
                    self.search_todos(parsed["search_term"])
                else:
                    print(f"{Fore.RED}❌ Please specify a search term.")
            
            else:
                print(f"{Fore.RED}❌ Unknown action: {action}")
                
        except Exception as e:
            print(f"{Fore.RED}❌ Error processing command: {e}")
    
    def run_interactive(self):
        """Run the interactive CLI interface."""
        print(f"{Fore.CYAN}🤖 Welcome to TodoAgent!")
        print(f"{Fore.WHITE}I can help you manage your todos using natural language.")
        print(f"{Fore.YELLOW}Type 'help' for commands, 'quit' to exit.")
        print("-" * 50)
        
        while True:
            try:
                command = input(f"{Fore.GREEN}📝 TodoAgent> ").strip()
                
                if not command:
                    continue
                
                if command.lower() in ['quit', 'exit', 'q']:
                    print(f"{Fore.CYAN}👋 Goodbye! Your todos are saved.")
                    break
                
                elif command.lower() == 'help':
                    self.show_help()
                
                elif command.lower() == 'stats':
                    self.get_statistics()
                
                elif command.lower() == 'list':
                    self.list_todos()
                
                else:
                    self.process_command(command)
                    
            except KeyboardInterrupt:
                print(f"\n{Fore.CYAN}👋 Goodbye! Your todos are saved.")
                break
            except Exception as e:
                print(f"{Fore.RED}❌ Unexpected error: {e}")
    
    def show_help(self):
        """Show help information."""
        print(f"{Fore.CYAN}📖 TodoAgent Help:")
        print(f"{Fore.WHITE}Natural Language Commands:")
        print(f"  {Fore.GREEN}• add buy groceries")
        print(f"  {Fore.GREEN}• add urgent meeting with client tomorrow")
        print(f"  {Fore.GREEN}• add workout session high priority health category")
        print(f"  {Fore.GREEN}• mark task 1 as completed")
        print(f"  {Fore.GREEN}• delete task 3")
        print(f"  {Fore.GREEN}• search groceries")
        print(f"  {Fore.GREEN}• update task 2 priority high due_date 2024-01-20")
        print()
        print(f"{Fore.WHITE}Direct Commands:")
        print(f"  {Fore.YELLOW}• list - Show all todos")
        print(f"  {Fore.YELLOW}• stats - Show statistics")
        print(f"  {Fore.YELLOW}• help - Show this help")
        print(f"  {Fore.YELLOW}• quit - Exit the program")
        print()
        print(f"{Fore.WHITE}Features:")
        print(f"  {Fore.MAGENTA}• Priority levels: high, medium, low")
        print(f"  {Fore.MAGENTA}• Categories: work, personal, shopping, health, learning, other")
        print(f"  {Fore.MAGENTA}• Status: pending, in_progress, completed")
        print(f"  {Fore.MAGENTA}• Due dates: YYYY-MM-DD format")
        print(f"  {Fore.MAGENTA}• Persistent storage in todos.json")


def main():
    """Main function to run the TodoAgent."""
    print(f"{Fore.CYAN}🚀 Starting TodoAgent - Day 1 of #100DaysOfAI-Agents")
    print(f"{Fore.WHITE}Author: Muhammad Sami Asghar Mughal")
    print()
    
    # Check if API key is provided as command line argument
    api_key = None
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    
    try:
        agent = TodoAgent(api_key)
        agent.run_interactive()
    except Exception as e:
        print(f"{Fore.RED}❌ Failed to start TodoAgent: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
