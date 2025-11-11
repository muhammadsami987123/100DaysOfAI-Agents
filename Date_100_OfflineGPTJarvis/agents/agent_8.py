# agent_8.py - DailyGoalTrackerAgent

from data.database import Database

class DailyGoalTrackerAgent:
    def __init__(self, db_path='jarvis_db.json'):
        self.db = Database(db_path)
        self.goals_table = self.db.db.table('daily_goals')

    def add_goal(self, goal_description):
        self.goals_table.insert({"goal": goal_description, "completed": False, "date": self.db.get_timestamp()})
        return f"Added daily goal: {goal_description}"

    def list_goals(self):
        goals = self.goals_table.all()
        if not goals:
            return "You have no daily goals set."
        
        goal_list_str = "Your daily goals:\n"
        for i, goal in enumerate(goals):
            status = "Completed" if goal['completed'] else "Pending"
            goal_list_str += f"{i+1}. {goal['goal']} - {status} (Added on: {goal['date']})\n"
        return goal_list_str

    def mark_goal_complete(self, index):
        goals = self.goals_table.all()
        if 0 <= index < len(goals):
            goal_id = goals[index].doc_id
            self.goals_table.update({"completed": True}, doc_ids=[goal_id])
            return f"Marked goal '{goals[index]['goal']}' as complete."
        else:
            return "Invalid goal index."

    def remove_goal(self, index):
        goals = self.goals_table.all()
        if 0 <= index < len(goals):
            goal_id = goals[index].doc_id
            removed_goal = goals[index]['goal']
            self.goals_table.remove(doc_ids=[goal_id])
            return f"Removed goal: {removed_goal}"
        else:
            return "Invalid goal index."
