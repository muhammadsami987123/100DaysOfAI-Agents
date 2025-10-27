import unittest
from unittest.mock import MagicMock, patch
from agent import BookSummaryAgent
from utils.llm_service import LLMService
from config import Config

class TestBookSummaryAgent(unittest.TestCase):
    def setUp(self):
        # Mock LLMService
        self.mock_llm_service = MagicMock(spec=LLMService)
        self.agent = BookSummaryAgent(llm_service=self.mock_llm_service)

    def test_summarize_chapter_concise(self):
        chapter_text = "This is a test chapter about the importance of good habits. It details how small, consistent actions can lead to significant changes over time. The author emphasizes the compound effect of daily routines and provides examples of successful habit formation."
        expected_summary = {
            "summary": "This chapter highlights the significance of cultivating good habits through small, consistent actions. It explains the compound effect of daily routines and offers illustrative examples of how habits can be successfully formed.",
            "key_points": ["Importance of good habits", "Compound effect of daily routines", "Examples of habit formation"]
        }

        self.mock_llm_service._read_template.return_value = "Summarize the following chapter: {chapter_text}"
        self.mock_llm_service.generate_content.return_value = expected_summary

        result = self.agent.summarize_chapter(chapter_text, summary_type="concise")
        self.assertEqual(result, expected_summary)
        self.mock_llm_service._read_template.assert_called_once_with("summary_prompt.txt")
        self.mock_llm_service.generate_content.assert_called_once()

    def test_summarize_chapter_bullet_points(self):
        chapter_text = "Another test chapter focusing on the benefits of reading. Regular reading improves vocabulary, critical thinking, and general knowledge. It also reduces stress and can enhance empathy by exposing readers to diverse perspectives."
        expected_summary = {
            "summary": "- Reading improves vocabulary and critical thinking.\n- Enhances general knowledge.\n- Reduces stress.\n- Increases empathy through diverse perspectives.",
            "key_points": []
        }

        self.mock_llm_service._read_template.return_value = "Summarize the following chapter in bullet points: {chapter_text}"
        self.mock_llm_service.generate_content.return_value = expected_summary

        result = self.agent.summarize_chapter(chapter_text, summary_type="bullet_points")
        self.assertEqual(result, expected_summary)
        self.mock_llm_service._read_template.assert_called_once_with("summary_prompt.txt")
        self.mock_llm_service.generate_content.assert_called_once()

    @patch('utils.llm_service.Config')
    def test_llm_service_initialization(self, MockConfig):
        MockConfig.GEMINI_API_KEY = "test_gemini_key"
        MockConfig.OPENAI_API_KEY = "test_openai_key"
        MockConfig.DEFAULT_LLM = "gemini"
        MockConfig.GEMINI_MODEL = "gemini-test-model"
        MockConfig.OPENAI_MODEL = "gpt-test-model"

        llm_service = LLMService()
        self.assertIsNotNone(llm_service.gemini_client)
        self.assertIsNotNone(llm_service.openai_client)
        self.assertEqual(llm_service.current_llm, "gemini")

    @patch('utils.llm_service.Config')
    def test_set_llm(self, MockConfig):
        MockConfig.GEMINI_API_KEY = "test_gemini_key"
        MockConfig.OPENAI_API_KEY = "test_openai_key"
        MockConfig.DEFAULT_LLM = "gemini"
        MockConfig.GEMINI_MODEL = "gemini-test-model"
        MockConfig.OPENAI_MODEL = "gpt-test-model"

        llm_service = LLMService()
        llm_service.set_llm("openai")
        self.assertEqual(llm_service.current_llm, "openai")
        llm_service.set_llm("gemini")
        self.assertEqual(llm_service.current_llm, "gemini")

        with self.assertRaises(ValueError):
            llm_service.set_llm("unsupported_llm")

if __name__ == '__main__':
    unittest.main()
