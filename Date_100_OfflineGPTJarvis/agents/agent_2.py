# agent_2.py - FileManagerAgent

import os
import shutil

class FileManagerAgent:
    def create_directory(self, path):
        try:
            os.makedirs(path, exist_ok=True)
            return f"Successfully created directory: {path}"
        except Exception as e:
            return f"Error creating directory: {e}"

    def delete_directory(self, path):
        try:
            shutil.rmtree(path)
            return f"Successfully deleted directory: {path}"
        except Exception as e:
            return f"Error deleting directory: {e}"

    def create_file(self, path, content=""):
        try:
            with open(path, 'w') as f:
                f.write(content)
            return f"Successfully created file: {path}"
        except Exception as e:
            return f"Error creating file: {e}"

    def delete_file(self, path):
        try:
            os.remove(path)
            return f"Successfully deleted file: {path}"
        except Exception as e:
            return f"Error deleting file: {e}"

    def list_directory_contents(self, path="."):
        try:
            contents = os.listdir(path)
            if not contents:
                return f"The directory {path} is empty."
            
            return f"Contents of {path}:\n" + "\n".join(contents)
        except Exception as e:
            return f"Error listing directory contents: {e}"
