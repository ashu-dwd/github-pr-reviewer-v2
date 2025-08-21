import unittest
from unittest.mock import patch, MagicMock
from src.ai_service import AIService

class TestAIService(unittest.TestCase):
    def setUp(self):
        with patch('builtins.open', unittest.mock.mock_open(read_data='ai_service:\n  model: "gemini-pro"\n  max_tokens: 2048')):
            with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
                self.service = AIService()

    @patch('google.generativeai.GenerativeModel.generate_content')
    def test_generate_review(self, mock_generate_content):
        mock_response = MagicMock()
        mock_response.text = "This is a test review."
        mock_generate_content.return_value = mock_response

        analyzed_diff = {
            "pr_title": "Test PR",
            "pr_body": "This is a test PR.",
            "files": [
                {
                    "file_name": "test.py",
                    "chunks": ["diff --git a/test.py b/test.py"]
                }
            ]
        }

        review = self.service.generate_review(analyzed_diff)

        self.assertEqual(review, "This is a test review.")
        mock_generate_content.assert_called_once()

if __name__ == '__main__':
    unittest.main()