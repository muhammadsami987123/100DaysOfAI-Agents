# agent_1.py - TodoAgent

import json

class TodoAgent:
    def __init__(self, filepath="todos.json"):
        self.filepath = filepath
        self.todos = self.load_todos()

    def load_todos(self):
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_todos(self):
        with open(self.filepath, 'w') as f:
            json.dump(self.todos, f, indent=4)

    def add_todo(self, task):
        self.todos.append({"task": task, "done": False})
        self.save_todos()
        return f"Added todo: {task}"

    def list_todos(self):
        if not self.todos:
            return "You have no todos."
        
        todo_list = "Your todos:\n"
        for i, todo in enumerate(self.todos):
            status = "Done" if todo['done'] else "Not Done"
            todo_list += f"{i+1}. {todo['task']} - {status}\n"
        return todo_list

    def mark_todo_done(self, index):
        if 0 <= index < len(self.todos):
            self.todos[index]['done'] = True
            self.save_todos()
            return f"Marked todo {index+1} as done."
        else:
            return "Invalid todo index."

    def remove_todo(self, index):
        if 0 <= index < len(self.todos):
            removed_todo = self.todos.pop(index)
            self.save_todos()
            return f"Removed todo: {removed_todo['task']}"
        else:
            return "Invalid todo index."
