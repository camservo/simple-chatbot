import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app")))
import ask_questions


class TestAskQuestions(unittest.TestCase):
    @patch("ask_questions.get_openai_response_complete")
    def test_get_openai_response_complete(self, mock_get_response):
        # Create a mock client
        mock_client = MagicMock()
        question = "What is the capital of France?"

        # Set up what the mock should return
        expected_response = {"choices": [{"text": "Paris"}]}
        mock_get_response.return_value = expected_response

        # Call the function with the mock client
        response = ask_questions.get_openai_response_complete(mock_client, question)

        # Assertions to validate the behavior
        self.assertEqual(response, expected_response)
        mock_get_response.assert_called_once_with(mock_client, question)


if __name__ == "__main__":
    unittest.main()
