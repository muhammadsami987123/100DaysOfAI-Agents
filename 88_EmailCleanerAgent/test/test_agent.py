import unittest
from agent import EmailCleanerAgent
from utils.llm_service import LLMService
from config import Config

class TestEmailCleanerAgent(unittest.TestCase):
    def setUp(self):
        # This is a mock LLM service for testing purposes
        class MockLLMService(LLMService):
            def generate(self, prompt):
                if "newsletter" in prompt.lower():
                    return "Promotional"
                elif "unsubscribe" in prompt.lower():
                    return "Spam"
                else:
                    return "Important"

        self.llm_service = MockLLMService(api_key="test_key", provider="gemini")
        self.agent = EmailCleanerAgent(self.llm_service)

    def test_email_classification(self):
        emails = [
            {'id': '1', 'snippet': 'This is an important email.'},
            {'id': '2', 'snippet': 'Check out our new newsletter.'},
            {'id': '3', 'snippet': 'Click here to unsubscribe.'}
        ]
        classified_emails = self.agent.analyze_and_classify_emails(emails)
        self.assertEqual(classified_emails[0]['classification'], 'Important')
        self.assertEqual(classified_emails[1]['classification'], 'Promotional')
        self.assertEqual(classified_emails[2]['classification'], 'Spam')

if __name__ == '__main__':
    unittest.main()
