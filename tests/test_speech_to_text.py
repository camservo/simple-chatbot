import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app")))
import speech_to_text


class TestSpeechToText(unittest.TestCase):
    @patch("speech_to_text.sr.Recognizer")
    @patch("speech_to_text.sr.Microphone")
    def test_listen_and_transcribe_success(self, mock_microphone, mock_recognizer):
        # Setup mock to simulate successful transcription
        mock_recognizer_instance = MagicMock()
        mock_recognizer.return_value = mock_recognizer_instance
        mock_recognizer_instance.recognize_google.return_value = "test transcription"

        # Call the function under test
        result = speech_to_text.listen_and_transcribe()

        # Assert function returned the expected transcription
        self.assertEqual(result, "test transcription")

    @patch("speech_to_text.sr.Recognizer")
    @patch("speech_to_text.sr.Microphone")
    def test_listen_and_transcribe_failure(self, mock_microphone, mock_recognizer):
        # Setup mock to simulate failure in understanding audio
        mock_recognizer_instance = MagicMock()
        mock_recognizer.return_value = mock_recognizer_instance
        mock_recognizer_instance.recognize_google.side_effect = (
            speech_to_text.sr.UnknownValueError
        )

        # Call the function under test and expect it to handle the error gracefully
        result = speech_to_text.listen_and_transcribe()

        # In this case, you might expect None, a specific message, or check if a log was created
        self.assertIsNone(result)  # Adjust based on your function's error handling


if __name__ == "__main__":
    unittest.main()
