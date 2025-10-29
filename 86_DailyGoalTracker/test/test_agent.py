import unittest
import os
import json
from unittest.mock import MagicMock, patch
from agent import DailyGoalTrackerAgent
from utils.llm_service import LLMService

class TestDailyGoalTrackerAgent(unittest.TestCase):

    def setUp(self):
        self.test_storage_file = "test_goals.json"
        # Ensure a clean state for each test
        if os.path.exists(self.test_storage_file):
            os.remove(self.test_storage_file)

        self.mock_llm_service = MagicMock(spec=LLMService)
        self.agent = DailyGoalTrackerAgent(llm_service=self.mock_llm_service, storage_file=self.test_storage_file)

    def tearDown(self):
        # Clean up after tests
        if os.path.exists(self.test_storage_file):
            os.remove(self.test_storage_file)

    def test_add_goals_success(self):
        self.mock_llm_service.generate_content.return_value = {"summary": json.dumps({"goals": ["Finish report", "Go for a run"]})}
        
        user_input = "I want to finish my report and go for a run today."
        new_goals = self.agent.add_goals(user_input)

        self.assertEqual(len(new_goals), 2)
        self.assertEqual(new_goals[0]["text"], "Finish report")
        self.assertFalse(new_goals[0]["completed"])
        self.assertEqual(new_goals[1]["text"], "Go for a run")
        self.assertFalse(new_goals[1]["completed"])

        # Verify goals are saved
        loaded_goals = self.agent._load_goals()
        today_str = list(loaded_goals.keys())[0]
        self.assertEqual(len(loaded_goals[today_str]), 2)

    def test_add_goals_llm_parse_failure_fallback(self):
        # Simulate LLM returning non-JSON or empty summary
        self.mock_llm_service.generate_content.return_value = {"summary": "I want to finish my report and go for a run today."}

        user_input = "I want to finish my report and go for a run today."
        new_goals = self.agent.add_goals(user_input)

        self.assertEqual(len(new_goals), 2)
        self.assertEqual(new_goals[0]["text"], "I want to finish my report")
        self.assertEqual(new_goals[1]["text"], "go for a run today.")

    def test_get_today_goals(self):
        self.mock_llm_service.generate_content.return_value = {"summary": json.dumps({"goals": ["Read a book"]})}
        self.agent.add_goals("Read a book")
        
        today_goals = self.agent.get_today_goals()
        self.assertEqual(len(today_goals), 1)
        self.assertEqual(today_goals[0]["text"], "Read a book")

    def test_update_goal_status(self):
        self.mock_llm_service.generate_content.return_value = {"summary": json.dumps({"goals": ["Buy groceries"]})}
        self.agent.add_goals("Buy groceries")
        
        today_goals = self.agent.get_today_goals()
        goal_id = today_goals[0]["id"]

        updated_goal = self.agent.update_goal_status(goal_id, True)
        self.assertTrue(updated_goal["completed"])

        # Verify status in loaded goals
        loaded_goals = self.agent._load_goals()
        today_str = list(loaded_goals.keys())[0]
        self.assertTrue(loaded_goals[today_str][0]["completed"])

    def test_generate_daily_review(self):
        self.mock_llm_service.generate_content.side_effect = [
            {"summary": json.dumps({"goals": ["Write code", "Review PR"]})}, # For add_goals
            {"summary": "- ✅ Write code\n- ❌ Review PR\nGreat job!"} # For generate_daily_review
        ]

        self.agent.add_goals("Write code and review PR")
        today_goals = self.agent.get_today_goals()
        self.agent.update_goal_status(today_goals[0]["id"], True) # Mark 'Write code' as completed

        review = self.agent.generate_daily_review()
        self.assertIn("Write code", review["summary"])
        self.assertIn("Review PR", review["summary"])
        self.assertIn("Great job!", review["summary"])
        self.assertEqual(len(review["completed"]), 1)
        self.assertEqual(len(review["pending"]), 1)

if __name__ == '__main__':
    unittest.main()
