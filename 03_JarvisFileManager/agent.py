import openai
import os
import json
from dotenv import load_dotenv
from pathlib import Path
import subprocess
import sys
from difflib import get_close_matches

# Load environment variables from .env file
load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
current_dir = os.getcwd()

# --- Universal App/Folder Indexing ---
app_index = {}
folder_index = {}

# Build app index from Start Menu shortcuts
def build_app_index():
    app_paths = {}
    start_menu_dirs = [
        os.path.join(os.environ.get("PROGRAMDATA", ""), r"Microsoft\Windows\Start Menu\Programs"),
        os.path.join(os.environ.get("APPDATA", ""), r"Microsoft\Windows\Start Menu\Programs"),
    ]
    for dir in start_menu_dirs:
        if not os.path.isdir(dir):
            continue
        for root, _, files in os.walk(dir):
            for file in files:
                if file.endswith(".lnk"):
                    name = os.path.splitext(file)[0].lower()
                    app_paths[name] = os.path.join(root, file)
    return app_paths

# Build folder index from common user folders
def build_folder_index():
    folder_paths = {}
    home = str(Path.home())
    user_dirs = ["Desktop", "Downloads", "Documents", "Pictures", "Music", "Videos"]
    for d in user_dirs:
        path = os.path.join(home, d)
        if os.path.isdir(path):
            folder_paths[d.lower()] = path
    return folder_paths

app_index = build_app_index()
folder_index = build_folder_index()

def get_special_folder_path(name):
    # Try indexed folders first
    if name.lower() in folder_index:
        return folder_index[name.lower()]
    # Fallback to home subfolders
    home = str(Path.home())
    mapping = {
        "desktop": os.path.join(home, "Desktop"),
        "downloads": os.path.join(home, "Downloads"),
        "documents": os.path.join(home, "Documents"),
        "pictures": os.path.join(home, "Pictures"),
        "music": os.path.join(home, "Music"),
        "videos": os.path.join(home, "Videos"),
    }
    return mapping.get(name.lower())

def find_best_app(app_name):
    matches = get_close_matches(app_name.lower(), app_index.keys(), n=1, cutoff=0.6)
    if matches:
        return app_index[matches[0]]
    return None

def find_best_folder(folder_name):
    matches = get_close_matches(folder_name.lower(), folder_index.keys(), n=1, cutoff=0.6)
    if matches:
        return folder_index[matches[0]]
    return None

def open_app(app_name):
    # Try fuzzy match in app index
    path = find_best_app(app_name)
    if path:
        try:
            os.startfile(path)
            return f"Opened {app_name}."
        except Exception as e:
            return f"Failed to open {app_name}: {e}"
    # Fallback to known apps
    app_name = app_name.lower()
    try:
        if app_name == "notepad":
            subprocess.Popen(["notepad.exe"])
        elif app_name == "chrome":
            subprocess.Popen(["chrome.exe"])
        elif app_name == "camera":
            subprocess.Popen(["start", "microsoft.windows.camera:"], shell=True)
        else:
            return f"App '{app_name}' not recognized."
        return f"Opened {app_name}."
    except Exception as e:
        return f"Failed to open {app_name}: {e}"

def close_app(app_name):
    # Try to close by process name (fuzzy match)
    app_proc = app_name.lower() + ".exe"
    try:
        os.system(f"taskkill /im {app_proc} /f")
        return f"Closed {app_name}."
    except Exception as e:
        return f"Failed to close {app_name}: {e}"

def process_command(text):
    global current_dir
    prompt = f"""
You are a file manager assistant. Given a user's command, return a JSON with the action and parameters. Supported actions: 'change_directory', 'create_folder', 'create_file', 'rename_item', 'open_folder', 'open_app', 'close_app'.
Paths like 'Desktop', 'Downloads', etc. refer to the user's system folders. You can open or close any app or folder on the system by name. Only output a valid JSON object as described. Do not include any explanation or extra text.
Examples:
Input: Go to Downloads and create a folder named Invoices.
Output: {{"actions": [{{"action": "change_directory", "path": "Downloads"}}, {{"action": "create_folder", "name": "Invoices"}}]}}
Input: Make a file called notes.txt on Desktop.
Output: {{"actions": [{{"action": "change_directory", "path": "Desktop"}}, {{"action": "create_file", "name": "notes.txt"}}]}}
Input: Rename folder Test to Work.
Output: {{"actions": [{{"action": "rename_item", "old_name": "Test", "new_name": "Work"}}]}}
Input: Open my Downloads folder.
Output: {{"actions": [{{"action": "open_folder", "path": "Downloads"}}]}}
Input: Open Notepad.
Output: {{"actions": [{{"action": "open_app", "app_name": "Notepad"}}]}}
Input: Close Notepad.
Output: {{"actions": [{{"action": "close_app", "app_name": "Notepad"}}]}}
Input: Open Visual Studio Code.
Output: {{"actions": [{{"action": "open_app", "app_name": "Visual Studio Code"}}]}}
Input: Open folder Projects.
Output: {{"actions": [{{"action": "open_folder", "path": "Projects"}}]}}
Input: {text}
Output:
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful file manager assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.2,
        )
        actions_json = response.choices[0].message.content.strip()
        print("OpenAI raw response:", actions_json)  # Debug print
        try:
            actions = json.loads(actions_json)
        except Exception as e:
            return f"Could not parse OpenAI response: {actions_json}"
        feedback = []
        for act in actions.get("actions", []):
            if act["action"] == "change_directory":
                special_path = get_special_folder_path(act["path"])
                if special_path and os.path.isdir(special_path):
                    current_dir = special_path
                    feedback.append(f"Changed directory to {special_path}.")
                else:
                    new_dir = os.path.abspath(os.path.join(current_dir, act["path"]))
                    if os.path.isdir(new_dir):
                        current_dir = new_dir
                        feedback.append(f"Changed directory to {new_dir}.")
                    else:
                        feedback.append(f"Directory {act['path']} does not exist.")
            elif act["action"] == "create_folder":
                folder_path = os.path.join(current_dir, act["name"])
                try:
                    os.makedirs(folder_path, exist_ok=True)
                    feedback.append(f"Folder '{act['name']}' created.")
                except Exception as e:
                    feedback.append(f"Failed to create folder: {e}")
            elif act["action"] == "create_file":
                file_path = os.path.join(current_dir, act["name"])
                try:
                    with open(file_path, 'w') as f:
                        f.write("")
                    feedback.append(f"File '{act['name']}' created.")
                except Exception as e:
                    feedback.append(f"Failed to create file: {e}")
            elif act["action"] == "rename_item":
                old_path = os.path.join(current_dir, act["old_name"])
                new_path = os.path.join(current_dir, act["new_name"])
                try:
                    os.rename(old_path, new_path)
                    feedback.append(f"Renamed '{act['old_name']}' to '{act['new_name']}'.")
                except Exception as e:
                    feedback.append(f"Failed to rename: {e}")
            elif act["action"] == "open_folder":
                # Try fuzzy match in folder index
                folder_path = find_best_folder(act["path"]) or get_special_folder_path(act["path"]) or os.path.join(current_dir, act["path"])
                try:
                    os.startfile(folder_path)
                    feedback.append(f"Opened folder '{folder_path}'.")
                except Exception as e:
                    feedback.append(f"Failed to open folder: {e}")
            elif act["action"] == "open_app":
                feedback.append(open_app(act["app_name"]))
            elif act["action"] == "close_app":
                feedback.append(close_app(act["app_name"]))
            else:
                feedback.append(f"Unknown action: {act['action']}")
        return " ".join(feedback)
    except Exception as e:
        return f"Sorry, I couldn't process your request: {e}"