import logging
import os
import tempfile

import playsound
import speech_recognition as sr
from gtts import gTTS

LOGLEVEL = os.environ.get("LOGLEVEL", "WARNING").upper()
logging.basicConfig(level=LOGLEVEL)


class TextToSpeechConverter:
    """
    Converts text into speech using different backends, including OpenAI's GPT model for text-to-speech conversion and Google's Text-to-Speech (gTTS) API. Allows specifying models, voices, languages, and TLDs for customization.
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
        Initializes the text-to-speech converter with default settings.

        Parameters:
            client: The OpenAI client instance for API requests.
            default_gpt_model (str): Default GPT model for text-to-speech conversion.
            default_gpt_voice (str): Default voice for GPT-based conversions.
            default_renderer (str): Default backend renderer ('gtts' for Google TTS, 'chatgpt' for OpenAI GPT).
            default_gtts_lang (str): Default language for gTTS.
            default_gtts_tld (str): Default top-level domain for gTTS, affecting accent.
        """
        self.client = client
        self.default_gpt_model = default_gpt_model
        self.default_gpt_voice = default_gpt_voice
        self.default_renderer = default_renderer
        self.default_gtts_lang = default_gtts_lang
        self.default_gtts_tld = default_gtts_tld

    def convert(self, text, renderer=None):
        """
        Converts text to speech using a specified or default rendering backend.

        Parameters:
            text (str): Text to be converted to speech.
            renderer (str, optional): Rendering backend to use ('gtts' or 'chatgpt'). Defaults to None, which uses the default_renderer.
        """
        try:
            renderer = renderer or self.default_renderer
            if renderer == "chatgpt":
                logging.debug(f"running TTS renderer ${renderer}")
                self.convert_gpt(text=text)
            elif renderer == "gtts":
                logging.debug(f"running TTS renderer ${renderer}")
                self.convert_gtts(text=text)
            else:
                logging.error(f"Unknown renderer: {renderer}")
        except Exception as e:
            logging.error(f"Error in convert method: {str(e)}")

    def convert_gpt(self, text, model=None, voice=None):
        """
        Converts text to speech using the GPT model and plays it.

        Parameters:
            text (str): Text to be converted.
            model (str, optional): GPT model to use. Defaults to None, which uses the default_gpt_model.
            voice (str, optional): Voice for GPT-based conversion. Defaults to None, which uses the default_gpt_voice.
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

        Parameters:
            text (str): Text to be converted.
            lang (str, optional): Language for gTTS. Defaults to None, which uses the default_gtts_lang.
            tld (str, optional): Top-level domain for gTTS, affecting accent. Defaults to None, which uses the default_gtts_tld.
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


class SpeechToTextConverter:
    def __init__(
        self, client=None, default_renderer="gtts", default_input_type="microphone"
    ):
        """
        Initializes the SpeechToTextConverter.

        :param client: An optional client object for interacting with external speech recognition services.
        :param default_renderer: The default service to use for speech recognition. Supports 'google_cloud' and 'gtts'.
        :param default_input_type: The default method for capturing speech input. Currently, only 'microphone' is supported.
        """
        self.client = client
        self.default_renderer = default_renderer
        self.default_input_type = default_input_type

    def convert(self, renderer=None, input_type=None):
        """
        Converts speech to text using the specified or default renderer and input type.

        :param renderer: The renderer to use for speech recognition.
        :param input_type: The method for capturing speech input.
        :return: The recognized text or None if an error occurs.
        """
        renderer = renderer or self.default_renderer
        input_type = input_type or self.default_input_type

        if input_type != "microphone":
            logging.error(
                "Unsupported input type. Currently, only 'microphone' is supported."
            )
            return None

        try:
            return self.get_microphone_input(renderer)
        except Exception as e:
            logging.error(f"Error in convert method: {str(e)}")
            return None

    def get_microphone_input(self, renderer):
        """
        Captures audio from the microphone and converts it to text using the specified renderer.

        :param renderer: The renderer to use for speech recognition.
        :return: The recognized text.
        """
        logging.debug("Getting input from microphone.")
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = recognizer.listen(source)
            return self.render(renderer, audio)

    def render(self, renderer, audio):
        """
        Renders the audio into text using the specified renderer.

        :param renderer: The renderer to use for speech recognition.
        :param audio: The captured audio to be converted into text.
        :return: The recognized text.
        """
        recognizer = sr.Recognizer()
        try:
            if renderer == "google_cloud":
                logging.debug("Rending with google cloud STT converter.")
                # Assuming credentials and configuration for Google Cloud are set elsewhere
                return recognizer.recognize_google_cloud(audio)
            elif renderer == "gtts":
                logging.debug("Rending with google local STT converter.")
                return recognizer.recognize_google(audio)
            else:
                logging.error("Unsupported renderer specified.")
                return None
        except Exception as e:
            logging.error(f"Error in render method: {str(e)}")
            return None
