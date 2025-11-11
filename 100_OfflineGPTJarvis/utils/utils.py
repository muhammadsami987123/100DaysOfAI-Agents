# utils.py

def get_project_root():
    """Returns the root directory of the project."""
    # In a real application, this would be more robust.
    # For now, we'll just return the current working directory.
    import os
    return os.getcwd()

def log_action(agent, action, status, output):
    """Logs the action taken by an agent."""
    import datetime
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "agent": agent,
        "action": action,
        "status": status,
        "output": output
    }
    print(log_entry)
    # In a real application, this would write to a log file.
