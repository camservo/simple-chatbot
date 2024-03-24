import tempfile

import playsound


class TextToSpeechConverter:
    """
    A class to convert text to speech using OpenAI's text-to-speech API.

    This class provides an interface to convert a given text string into speech,
    which is then played back using the playsound module. It allows specifying
    the model and voice to be used for the text-to-speech conversion.

    Attributes:
        client (openai.OpenAI): The OpenAI client instance used for API requests.
        default_model (str): The default model to use for text-to-speech conversion.
        default_voice (str): The default voice to use for the spoken text.
    """

    def __init__(self, client, default_model="tts-1", default_voice="nova"):
        """
        Initializes the TextToSpeechConverter with an OpenAI client, and optionally,
        a default model and voice for the text-to-speech conversion.

        Args:
            client (openai.OpenAI): The OpenAI client instance.
            default_model (str, optional): The default model to use for text-to-speech.
                Defaults to "tts-1".
            default_voice (str, optional): The default voice to use for the spoken text.
                Defaults to "nova".
        """
        self.client = client
        self.default_model = default_model
        self.default_voice = default_voice

    def convert(self, text, model=None, voice=None):
        """
        Converts the provided text to speech, using the specified or default model and voice.
        The generated speech audio is played back using the playsound module.

        Args:
            text (str): The text to convert to speech.
            model (str, optional): The model to use for the conversion. If not specified,
                the default model is used.
            voice (str, optional): The voice to use for the conversion. If not specified,
                the default voice is used.

        Raises:
            Exception: If any error occurs during the API request or while playing the sound.
        """
        model = model if model else self.default_model
        voice = voice if voice else self.default_voice

        try:
            response = self.client.audio.speech.create(
                model=model, voice=voice, input=text
            )
            with tempfile.NamedTemporaryFile(delete=True) as fp:
                response.stream_to_file(fp.name)
                playsound.playsound(fp.name)
        except Exception as e:
            print(f"An error occurred during text-to-speech conversion: {e}")
            raise
