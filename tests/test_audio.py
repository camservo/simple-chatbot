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
