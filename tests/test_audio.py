from unittest.mock import Mock, patch

import pytest

from app.audio import (
    TextToSpeechConverter,  # Adjust the import path according to your project structure.
)


@pytest.fixture
def mock_openai_client():
    """Provides a mocked OpenAI client."""
    return Mock()


@pytest.fixture
def text_to_speech_converter(mock_openai_client):
    """Provides a TextToSpeechConverter instance with a mocked OpenAI client."""
    return TextToSpeechConverter(
        client=mock_openai_client,
        default_gpt_model="test-model",
        default_gpt_voice="test-voice",
        default_renderer="gtts",  # Assuming gTTS as default to simplify testing without hitting API.
        default_gtts_lang="en",
        default_gtts_tld="com",
    )


def test_convert_uses_default_renderer(text_to_speech_converter, mock_openai_client):
    """Tests that the convert method uses the default renderer when none is specified."""
    with patch("tempfile.NamedTemporaryFile") as mock_tempfile, patch(
        "playsound.playsound"
    ) as mock_playsound:
        mock_tempfile.return_value.__enter__.return_value.name = "tempfile.mp3"
        text_to_speech_converter.convert("Hello, world!")
        # Ensure playsound was called, indicating that the conversion (mocked) took place.
        mock_playsound.assert_called_once_with("tempfile.mp3")


def test_convert_gtts_creates_and_plays_file(text_to_speech_converter):
    """Tests that convert_gtts method creates and plays an audio file."""
    with patch("tempfile.NamedTemporaryFile") as mock_tempfile, patch(
        "playsound.playsound"
    ) as mock_playsound, patch("gtts.gTTS.save") as mock_gtts_save:
        mock_tempfile.return_value.__enter__.return_value.name = "tempfile.mp3"
        text_to_speech_converter.convert_gtts("Test gTTS conversion")
        # Ensure gTTS's save method was called to save the audio file.
        mock_gtts_save.assert_called()
        # Ensure playsound was called, indicating the audio file was played.
        mock_playsound.assert_called_once_with("tempfile.mp3")


# Additional tests can be created to cover more cases, such as testing different renderer paths,
# handling exceptions, or testing with different languages and TLDs for gTTS.
