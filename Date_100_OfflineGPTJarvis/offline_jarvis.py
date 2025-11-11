


import click
from voice.tts_service import TTSService
from voice.stt_service import STTService
from data.database import Database
from utils.utils import log_action
from utils.llm_service import LLMService
from agents.agent_1 import TodoAgent
from agents.agent_2 import FileManagerAgent
from agents.agent_3 import PythonDocAgent
from agents.agent_4 import MathSolverAgent
from agents.agent_5 import TextFixerAgent
from agents.agent_6 import SystemMonitorAgent
from agents.agent_7 import GitHelperAgent
from agents.agent_8 import DailyGoalTrackerAgent
from agents.agent_9 import MemoryNotesAgent
from agents.agent_10 import ScreenshotTakerAgent

class OfflineGPTJarvis:
    def __init__(self):
        self.tts_service = TTSService()
        self.stt_service = STTService()
        self.db = Database()
        self.llm_service = LLMService()
        self.todo_agent = TodoAgent()
        self.file_manager_agent = FileManagerAgent()
        self.python_doc_agent = PythonDocAgent()
        self.math_solver_agent = MathSolverAgent()
        self.text_fixer_agent = TextFixerAgent()
        self.system_monitor_agent = SystemMonitorAgent()
        self.git_helper_agent = GitHelperAgent()
        self.daily_goal_tracker_agent = DailyGoalTrackerAgent()
        self.memory_notes_agent = MemoryNotesAgent()
        self.screenshot_taker_agent = ScreenshotTakerAgent()

    def speak(self, text):
        self.tts_service.speak(text)

    def listen(self):
        return self.stt_service.listen()

    def execute_command(self, command):
        # Placeholder for command execution logic
        if "hello" in command:
            self.speak("Hello! How can I assist you today?")
            log_action("Jarvis", "Greeting", "Success", "Said hello to the user")
        elif "add a todo" in command:
            self.speak("What task would you like to add?")
            task = self.listen()
            if task:
                response = self.todo_agent.add_todo(task)
                self.speak(response)
                log_action("TodoAgent", "Add Todo", "Success", f"Added todo: {task}")
        elif "list my todos" in command:
            response = self.todo_agent.list_todos()
            self.speak(response)
            log_action("TodoAgent", "List Todos", "Success", "Listed all todos")
        elif "mark todo as done" in command:
            self.speak("Which todo number would you like to mark as done?")
            try:
                index_str = self.listen()
                index = int(index_str) - 1
                response = self.todo_agent.mark_todo_done(index)
                self.speak(response)
                log_action("TodoAgent", "Mark Todo Done", "Success", f"Marked todo {index+1} as done")
            except (ValueError, TypeError):
                self.speak("Invalid number. Please say the todo number.")
                log_action("TodoAgent", "Mark Todo Done", "Fail", "Invalid todo number")
        elif "remove a todo" in command:
            self.speak("Which todo number would you like to remove?")
            try:
                index_str = self.listen()
                index = int(index_str) - 1
                response = self.todo_agent.remove_todo(index)
                self.speak(response)
                log_action("TodoAgent", "Remove Todo", "Success", f"Removed todo {index+1}")
            except (ValueError, TypeError):
                self.speak("Invalid number. Please say the todo number.")
                log_action("TodoAgent", "Remove Todo", "Fail", "Invalid todo number")
        elif "create a directory" in command:
            self.speak("What is the name of the directory you would like to create?")
            path = self.listen()
            if path:
                response = self.file_manager_agent.create_directory(path)
                self.speak(response)
                log_action("FileManagerAgent", "Create Directory", "Success", f"Created directory: {path}")
        elif "delete a directory" in command:
            self.speak("What is the name of the directory you would like to delete?")
            path = self.listen()
            if path:
                response = self.file_manager_agent.delete_directory(path)
                self.speak(response)
                log_action("FileManagerAgent", "Delete Directory", "Success", f"Deleted directory: {path}")
        elif "create a file" in command:
            self.speak("What is the name of the file you would like to create?")
            path = self.listen()
            if path:
                self.speak("What content should I write to the file?")
                content = self.listen()
                response = self.file_manager_agent.create_file(path, content)
                self.speak(response)
                log_action("FileManagerAgent", "Create File", "Success", f"Created file: {path}")
        elif "delete a file" in command:
            self.speak("What is the name of the file you would like to delete?")
            path = self.listen()
            if path:
                response = self.file_manager_agent.delete_file(path)
                self.speak(response)
                log_action("FileManagerAgent", "Delete File", "Success", f"Deleted file: {path}")
        elif "list directory contents" in command:
            self.speak("Which directory's contents would you like to list?")
            path = self.listen()
            if path:
                response = self.file_manager_agent.list_directory_contents(path)
                self.speak(response)
                log_action("FileManagerAgent", "List Directory Contents", "Success", f"Listed contents of: {path}")
        elif "get documentation for" in command:
            module_name = command.replace("get documentation for", "").strip()
            self.speak(f"Getting documentation for {module_name}...")
            documentation = self.python_doc_agent.get_documentation(module_name)
            # The documentation can be very long, so we'll just speak a summary
            self.speak(f"I have found the documentation for {module_name}. I will print it to the console.")
            print(documentation)
            log_action("PythonDocAgent", "Get Documentation", "Success", f"Got documentation for {module_name}")
        elif "calculate" in command:
            expression = command.replace("calculate", "").strip()
            response = self.math_solver_agent.solve(expression)
            self.speak(response)
            log_action("MathSolverAgent", "Calculate", "Success", f"Calculated: {expression}")
        elif "fix this text" in command:
            self.speak("What text would you like me to fix?")
            text = self.listen()
            if text:
                response = self.text_fixer_agent.fix_text(text)
                self.speak(response)
                log_action("TextFixerAgent", "Fix Text", "Success", f"Fixed text: {text}")
        elif "get cpu usage" in command:
            response = self.system_monitor_agent.get_cpu_usage()
            self.speak(response)
            log_action("SystemMonitorAgent", "Get CPU Usage", "Success", "Got CPU usage")
        elif "get memory usage" in command:
            response = self.system_monitor_agent.get_memory_usage()
            self.speak(response)
            log_action("SystemMonitorAgent", "Get Memory Usage", "Success", "Got memory usage")
        elif "get disk usage" in command:
            self.speak("Which disk path would you like to check?")
            path = self.listen()
            if path:
                response = self.system_monitor_agent.get_disk_usage(path)
                self.speak(response)
                log_action("SystemMonitorAgent", "Get Disk Usage", "Success", f"Got disk usage for {path}")
        elif "git status" in command:
            response = self.git_helper_agent.get_status()
            self.speak("Here is the git status:")
            print(response)
            log_action("GitHelperAgent", "Git Status", "Success", "Got git status")
        elif "git add all" in command:
            response = self.git_helper_agent.add_all()
            self.speak(response)
            log_action("GitHelperAgent", "Git Add All", "Success", "Added all files to git")
        elif "git commit" in command:
            self.speak("What is your commit message?")
            message = self.listen()
            if message:
                response = self.git_helper_agent.commit(message)
                self.speak(response)
                log_action("GitHelperAgent", "Git Commit", "Success", f"Committed with message: {message}")
        elif "add a daily goal" in command:
            self.speak("What is your daily goal?")
            goal = self.listen()
            if goal:
                response = self.daily_goal_tracker_agent.add_goal(goal)
                self.speak(response)
                log_action("DailyGoalTrackerAgent", "Add Goal", "Success", f"Added daily goal: {goal}")
        elif "list my daily goals" in command:
            response = self.daily_goal_tracker_agent.list_goals()
            self.speak(response)
            log_action("DailyGoalTrackerAgent", "List Goals", "Success", "Listed all daily goals")
        elif "mark daily goal as complete" in command:
            self.speak("Which daily goal number would you like to mark as complete?")
            try:
                index_str = self.listen()
                index = int(index_str) - 1
                response = self.daily_goal_tracker_agent.mark_goal_complete(index)
                self.speak(response)
                log_action("DailyGoalTrackerAgent", "Mark Goal Complete", "Success", f"Marked goal {index+1} as complete")
            except (ValueError, TypeError):
                self.speak("Invalid number. Please say the goal number.")
                log_action("DailyGoalTrackerAgent", "Mark Goal Complete", "Fail", "Invalid goal number")
        elif "remove a daily goal" in command:
            self.speak("Which daily goal number would you like to remove?")
            try:
                index_str = self.listen()
                index = int(index_str) - 1
                response = self.daily_goal_tracker_agent.remove_goal(index)
                self.speak(response)
                log_action("DailyGoalTrackerAgent", "Remove Goal", "Success", f"Removed goal {index+1}")
            except (ValueError, TypeError):
                self.speak("Invalid number. Please say the goal number.")
                log_action("DailyGoalTrackerAgent", "Remove Goal", "Fail", "Invalid goal number")
        elif "add a note" in command:
            self.speak("What would you like to note down?")
            note_content = self.listen()
            if note_content:
                response = self.memory_notes_agent.add_note(note_content)
                self.speak(response)
                log_action("MemoryNotesAgent", "Add Note", "Success", f"Added note: {note_content}")
        elif "list my notes" in command:
            response = self.memory_notes_agent.list_notes()
            self.speak(response)
            log_action("MemoryNotesAgent", "List Notes", "Success", "Listed all notes")
        elif "find note about" in command:
            keyword = command.replace("find note about", "").strip()
            if keyword:
                response = self.memory_notes_agent.find_note(keyword)
                self.speak(response)
                log_action("MemoryNotesAgent", "Find Note", "Success", f"Found notes about: {keyword}")
        elif "remove a note" in command:
            self.speak("Which note number would you like to remove?")
            try:
                index_str = self.listen()
                index = int(index_str) - 1
                response = self.memory_notes_agent.remove_note(index)
                self.speak(response)
                log_action("MemoryNotesAgent", "Remove Note", "Success", f"Removed note {index+1}")
            except (ValueError, TypeError):
                self.speak("Invalid number. Please say the note number.")
                log_action("MemoryNotesAgent", "Remove Note", "Fail", "Invalid note number")
        elif "take a screenshot" in command:
            self.speak("Taking a screenshot...")
            response = self.screenshot_taker_agent.take_screenshot()
            self.speak(response)
            log_action("ScreenshotTakerAgent", "Take Screenshot", "Success", "Took a screenshot")
        elif "set preference" in command:
            self.speak("What is the key for the preference?")
            key = self.listen()
            if key:
                self.speak(f"What is the value for {key}?")
                value = self.listen()
                if value:
                    self.db.set_user_preference(key, value)
                    self.speak(f"Preference {key} set to {value}")
                    log_action("Jarvis", "Set Preference", "Success", f"Set preference {key} to {value}")
        elif "get preference" in command:
            self.speak("What is the key for the preference?")
            key = self.listen()
            if key:
                value = self.db.get_user_preference(key)
                if value:
                    self.speak(f"The value for {key} is {value}")
                    log_action("Jarvis", "Get Preference", "Success", f"Retrieved preference {key}")
                else:
                    self.speak(f"No preference found for {key}")
                    log_action("Jarvis", "Get Preference", "Fail", f"No preference found for {key}")
        elif "exit" in command:
            self.speak("Goodbye!")
            log_action("Jarvis", "Exit", "Success", "Exiting the application")
            exit()
        else:
            self.speak("That's an interesting command. Let me think...")
            response = self.llm_service.generate_response(command)
            self.speak(response)
            log_action("Jarvis", "LLM Response", "Success", f"Generated LLM response for command: {command}")

@click.command()
def main():
    """
    OfflineGPTJarvis – The Final Boss of AI Agent Automation
    """
    jarvis = OfflineGPTJarvis()
    jarvis.speak("Jarvis is online and ready to assist.")

    while True:
        command = jarvis.listen()
        if command:
            jarvis.execute_command(command)

if __name__ == "__main__":
    main()


