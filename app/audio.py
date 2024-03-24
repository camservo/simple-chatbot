import logging
import tempfile

import playsound
from gtts import gTTS


class TextToSpeechConverter:
    """
    A class to convert text into speech using different backends.

    This class provides functionality to convert text into speech using either
    OpenAI's GPT model for text-to-speech conversion or Google's Text-to-Speech (gTTS) API.
    It allows for specifying different models, voices, languages, and top-level domains (TLDs)
    for the gTTS API to customize the speech output.

    Attributes:
        client (openai.OpenAI): The OpenAI client instance used for API requests.
        default_gpt_model (str): Default GPT model to use for text-to-speech conversion with OpenAI.
        default_gpt_voice (str): Default voice to use for the OpenAI text-to-speech conversion.
        default_renderer (str): Default backend to use for text-to-speech conversion ('chatgpt' or 'gtts').
        default_gtts_lang (str): Default language to use with gTTS.
        default_gtts_tld (str): Default top-level domain to use with gTTS for different accents.
    """

    def __init__(
        self,
        client,
        default_gpt_model="tts-1",
        default_gpt_voice="nova",
        default_renderer="gtts",
        default_gtts_lang="en",
        default_gtts_tld="ie",
    ):
        """
        Initializes a new instance of the TextToSpeechConverter class.

        :param client: The OpenAI client instance.
        :param default_gpt_model: The default GPT model for text-to-speech conversion.
        :param default_gpt_voice: The default voice for GPT-based conversions.
        :param default_renderer: The default rendering engine ('chatgpt' or 'gtts').
        :param default_gtts_lang: The default language for gTTS.
        :param default_gtts_tld: The default top-level domain for gTTS.
        """
        self.client = client
        self.default_gpt_model = default_gpt_model
        self.default_gpt_voice = default_gpt_voice
        self.default_renderer = default_renderer
        self.default_gtts_lang = default_gtts_lang
        self.default_gtts_tld = default_gtts_tld

    def convert(self, text, renderer=None):
        """
        Converts text to speech using the specified or default rendering backend.

        :param text: The text to be converted to speech.
        :param renderer: The rendering backend to use ('chatgpt' or 'gtts'). If None, uses the default renderer.
        """
        renderer = renderer or self.default_renderer
        if renderer == "chatgpt":
            self.convert_gpt(text=text)
        elif renderer == "gtts":
            self.convert_gtts(text=text)
        else:
            logging.error("Unknown renderer: %s", renderer)

    def convert_gpt(self, text, model=None, voice=None):
        """
        Converts text to speech using the GPT model and plays it.

        :param text: The text to convert.
        :param model: The GPT model to use. Defaults to the instance's default model.
        :param voice: The voice to use. Defaults to the instance's default voice.
        """
        model = model or self.default_gpt_model
        voice = voice or self.default_gpt_voice

        response = self.client.audio.speech.create(model=model, voice=voice, input=text)
        with tempfile.NamedTemporaryFile(delete=True) as fp:
            response.stream_to_file(fp.name)
            playsound.playsound(fp.name)

    def convert_gtts(self, text, lang=None, tld=None):
        """
        Converts text to speech using the Google Text-to-Speech (gTTS) API and plays it.

        :param text: The text to convert.
        :param lang: The language to use for the gTTS API. Defaults to the instance's default language.
        :param tld: The top-level domain to use for the gTTS API, affecting the accent. Defaults to the instance's default TLD.
        """
        lang = lang or self.default_gtts_lang
        tld = tld or self.default_gtts_tld

        tts = gTTS(text=text, lang=lang, tld=tld)
        with tempfile.NamedTemporaryFile(delete=True) as fp:
            tts.save(fp.name)
            playsound.playsound(fp.name)
