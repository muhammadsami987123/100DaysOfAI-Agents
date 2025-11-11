# agent_3.py - PythonDocAgent

import pydoc

class PythonDocAgent:
    def get_documentation(self, module_name):
        try:
            # pydoc.render_doc() returns the documentation as a string
            documentation = pydoc.render_doc(module_name)
            return documentation
        except ImportError:
            return f"Module '{module_name}' not found."
        except Exception as e:
            return f"An error occurred: {e}"
