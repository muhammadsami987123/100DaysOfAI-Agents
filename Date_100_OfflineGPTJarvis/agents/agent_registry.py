# agent_registry.py

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

AGENT_REGISTRY = {
    "TodoAgent": TodoAgent,
    "FileManagerAgent": FileManagerAgent,
    "PythonDocAgent": PythonDocAgent,
    "MathSolverAgent": MathSolverAgent,
    "TextFixerAgent": TextFixerAgent,
    "SystemMonitorAgent": SystemMonitorAgent,
    "GitHelperAgent": GitHelperAgent,
    "DailyGoalTrackerAgent": DailyGoalTrackerAgent,
    "MemoryNotesAgent": MemoryNotesAgent,
    "ScreenshotTakerAgent": ScreenshotTakerAgent,
}
