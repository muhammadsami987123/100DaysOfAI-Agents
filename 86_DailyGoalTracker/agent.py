from typing import Dict, Any, List, Optional
from utils.llm_service import LLMService
import datetime
import json
import os

class DailyGoalTrackerAgent:
    def __init__(self, llm_service: Optional[LLMService] = None, storage_file: str = "goals.json"):
        self.llm = llm_service or LLMService()
        self.storage_file = storage_file
        self.goals = self._load_goals()

    def _load_goals(self) -> Dict[str, Any]:
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_goals(self) -> None:
        with open(self.storage_file, "w", encoding="utf-8") as f:
            json.dump(self.goals, f, indent=4)

    def add_goals(self, user_input: str) -> List[Dict[str, Any]]:
        today_str = datetime.date.today().isoformat()
        if today_str not in self.goals:
            self.goals[today_str] = []

        # Use LLM to parse natural language input into structured goals
        prompt_template = self._read_prompt_template("goal_parser_prompt.txt")
        prompt = prompt_template.replace("{user_input}", user_input)
        llm_response = self.llm.generate_content(prompt)
        
        parsed_goals_str = llm_response.get("summary", "")
        new_goals_data = []
        try:
            # Assuming LLM returns a JSON string of goals
            parsed_goals = json.loads(parsed_goals_str)
            for goal_text in parsed_goals.get("goals", []):
                new_goal = {"id": len(self.goals[today_str]) + 1, "text": goal_text, "completed": False, "timestamp": datetime.datetime.now().isoformat()}
                self.goals[today_str].append(new_goal)
                new_goals_data.append(new_goal)
            self._save_goals()
            return new_goals_data
        except json.JSONDecodeError:
            print(f"Error parsing LLM response as JSON: {parsed_goals_str}")
            # Fallback: if LLM fails to return JSON, try to extract simple goals
            simple_goals = [g.strip() for g in user_input.split("and") if g.strip()]
            for goal_text in simple_goals:
                new_goal = {"id": len(self.goals[today_str]) + 1, "text": goal_text, "completed": False, "timestamp": datetime.datetime.now().isoformat()}
                self.goals[today_str].append(new_goal)
                new_goals_data.append(new_goal)
            self._save_goals()
            return new_goals_data

    def get_today_goals(self) -> List[Dict[str, Any]]:
        today_str = datetime.date.today().isoformat()
        return self.goals.get(today_str, [])

    def update_goal_status(self, goal_id: int, completed: bool) -> Optional[Dict[str, Any]]:
        today_str = datetime.date.today().isoformat()
        for goal in self.goals.get(today_str, []):
            if goal["id"] == goal_id:
                goal["completed"] = completed
                self._save_goals()
                return goal
        return None

    def generate_daily_review(self) -> Dict[str, Any]:
        today_str = datetime.date.today().isoformat()
        today_goals = self.goals.get(today_str, [])

        completed_goals = [goal for goal in today_goals if goal["completed"]]
        pending_goals = [goal for goal in today_goals if not goal["completed"]]

        prompt_template = self._read_prompt_template("review_prompt.txt")
        prompt = prompt_template.replace("{completed_goals}", json.dumps(completed_goals))
        prompt = prompt.replace("{pending_goals}", json.dumps(pending_goals))
        prompt = prompt.replace("{total_goals}", str(len(today_goals)))
        prompt = prompt.replace("{completed_count}", str(len(completed_goals)))

        llm_response = self.llm.generate_content(prompt)
        review_summary = llm_response.get("summary", "")

        return {
            "completed": completed_goals,
            "pending": pending_goals,
            "summary": review_summary,
            "message": llm_response.get("message", "")
        }

    def _read_prompt_template(self, template_name: str) -> str:
        template_path = os.path.join(os.path.dirname(__file__), "prompts", template_name)
        try:
            with open(template_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""
