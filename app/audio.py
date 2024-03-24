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
        """
        try:
            renderer = renderer or self.default_renderer
            if renderer == "chatgpt":
                self.convert_gpt(text=text)
            elif renderer == "gtts":
                self.convert_gtts(text=text)
            else:
                logging.error(f"Unknown renderer: {renderer}")
        except Exception as e:
            logging.error(f"Error in convert method: {str(e)}")

    def convert_gpt(self, text, model=None, voice=None):
        """
        Converts text to speech using the GPT model and plays it.
        """
        try:
            model = model or self.default_gpt_model
            voice = voice or self.default_gpt_voice

            response = self.client.audio.speech.create(
                model=model, voice=voice, input=text
            )
            with tempfile.NamedTemporaryFile(delete=True) as fp:
                response.stream_to_file(fp.name)
                playsound.playsound(fp.name)
        except Exception as e:
            logging.error(f"Error in convert_gpt method: {str(e)}")

    def convert_gtts(self, text, lang=None, tld=None):
        """
        Converts text to speech using the Google Text-to-Speech (gTTS) API and plays it.
        """
        try:
            lang = lang or self.default_gtts_lang
            tld = tld or self.default_gtts_tld

            tts = gTTS(text=text, lang=lang, tld=tld)
            with tempfile.NamedTemporaryFile(delete=True) as fp:
                tts.save(fp.name)
                playsound.playsound(fp.name)
        except Exception as e:
            logging.error(f"Error in convert_gtts method: {str(e)}")
