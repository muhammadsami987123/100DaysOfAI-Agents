# agent_6.py - SystemMonitorAgent

import psutil

class SystemMonitorAgent:
    def get_cpu_usage(self):
        try:
            usage = psutil.cpu_percent(interval=1)
            return f"CPU usage is at {usage}%."
        except Exception as e:
            return f"An error occurred while getting CPU usage: {e}"

    def get_memory_usage(self):
        try:
            memory = psutil.virtual_memory()
            return f"Memory usage is at {memory.percent}%."
        except Exception as e:
            return f"An error occurred while getting memory usage: {e}"

    def get_disk_usage(self, path="/"):
        try:
            disk = psutil.disk_usage(path)
            return f"Disk usage for {path} is at {disk.percent}%."
        except Exception as e:
            return f"An error occurred while getting disk usage: {e}"
