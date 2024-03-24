import logging
import tempfile

import playsound
from gtts import gTTS


class TextToSpeechConverter:
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
        Initialize the text-to-speech converter.

        :param client: The OpenAI client instance.
        :param default_gpt_model: The default model to use for text-to-speech.
        :param default_gpt_voice: The default voice to use for text-to-speech.
        """
        self.client = client
        self.default_gpt_model = default_gpt_model
        self.default_gpt_voice = default_gpt_voice
        self.default_renderer = default_renderer
        self.default_gtts_lang = default_gtts_lang
        self.default_gtts_tld = default_gtts_tld

    def convert(self, text, renderer=None):
        if renderer is None:
            renderer = self.default_renderer
        if renderer == "chatgpt":
            self.convert_gpt(text=text)
        elif renderer == "gtts":
            self.convert_gtts(text=text)
        else:
            logging.error("Unknown renderer")

    def convert_gpt(self, text, model=None, voice=None):
        """
        Convert text to speech and play it.

        :param text: The text to convert.
        :param model: The model to use, defaults to the instance's default model.
        :param voice: The voice to use, defaults to the instance's default voice.
        """
        if model is None:
            model = self.default_gpt_model
        if voice is None:
            voice = self.default_gpt_voice

        response = self.client.audio.speech.create(model=model, voice=voice, input=text)
        with tempfile.NamedTemporaryFile(delete=True) as fp:
            response.stream_to_file(fp.name)
            playsound.playsound(fp.name)

    def convert_gtts(self, text, lang=None, tld=None):
        if lang is None:
            lang = self.default_gtts_lang
        if tld is None:
            tld = self.default_gtts_tld

        tts = gTTS(text=text, lang=lang, tld=tld)
        with tempfile.NamedTemporaryFile(delete=True) as fp:
            # Save the synthesized speech audio to the temporary file.
            tts.save(fp.name)

            # Play the saved audio file. The playsound function blocks until the audio is finished playing.
            playsound.playsound(fp.name)
