import os
import sys
import unittest
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app")))
import text_to_speech


class TestTextToSpeech(unittest.TestCase):
    @patch("text_to_speech.playsound.playsound")
    @patch("text_to_speech.gTTS")
    def test_text_to_speech_calls_gTTS_and_playsound(self, mock_gTTS, mock_playsound):
        # Setup: Define the text and language to be used in the test
        test_text = "Hello, world!"
        test_lang = "en"
        test_tld = "ie"

        # Execute: Call the function under test
        text_to_speech.text_to_speech(test_text, test_lang)

        # Assert: Check that gTTS was called with the expected arguments
        mock_gTTS.assert_called_once_with(text=test_text, lang=test_lang, tld=test_tld)

        # We also want to ensure that gTTS.save() was called, but since mock_gTTS is
        # a MagicMock object for the gTTS class itself, we access its instance's `save` method.
        mock_gTTS.return_value.save.assert_called()

        # Assert: Check that playsound was called. We cannot assert on the exact filename
        # because it's a temporary file, so we just check if it was called.
        mock_playsound.assert_called()


if __name__ == "__main__":
    unittest.main()
