import logging
import tempfile

import playsound
import speech_recognition as sr
from gtts import gTTS


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
    """
    Converts speech to text using various backends, primarily supporting microphone input through the speech_recognition library's Google Web Speech API interface.
    """

    def __init__(
        self,
        client,
        default_renderer="speech_recognition",
        default_input_type="microphone",
    ):
        """
        Initializes the speech-to-text converter with default settings.

        Parameters:
            client: A placeholder for an API client or configuration. Currently, this is unused as the implementation leverages the speech_recognition library, which does not require an API client for its default functionality.
            default_renderer (str): The default service for speech-to-text conversion. Defaults to 'speech_recognition', which utilizes the Google Web Speech API.
            default_input_type (str): The default method of capturing speech. Currently, 'microphone' is the supported input type, indicating that speech input will be captured using the device's microphone.
        """
        self.client = client
        self.default_renderer = default_renderer
        self.default_input_type = default_input_type

    def convert(self, renderer=None, input_type=None):
        """
        Converts speech to text using the specified or default renderer and input type.

        Parameters:
            renderer (str, optional): The speech-to-text service to use. Only 'speech_recognition' is currently supported. Defaults to None, which uses the instance's default_renderer.
            input_type (str, optional): The method of capturing speech. Only 'microphone' is currently supported. Defaults to None, which uses the instance's default_input_type.

        Returns:
            The recognized text from speech input as a string. If an error occurs or the speech cannot be recognized, it may return None or log an error.
        """
        renderer = renderer or self.default_renderer
        try:
            input_type = input_type or self.default_input_type
            if input_type == "microphone":
                return self.get_microphone_input(renderer)
        except Exception as e:
            logging.error(f"Error in convert method: {str(e)}")

    def get_microphone_input(self, renderer):
        """
        Captures audio input from the microphone and attempts to convert it to text using the Google Web Speech API.

        Returns:
            The recognized text from the microphone input as a string. If the speech is unintelligible or if a request error occurs, it may print an error message to the console.
        """
        renderer = renderer or self.default_renderer
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = recognizer.listen(source)
            return self.render(renderer, audio)

    def render(self, renderer, audio):
        r = sr.Recognizer()
        if renderer == "google_cloud":
            return r.recognize_google_cloud(audio)
        if renderer == "gtts":
            return r.recognize_google(audio)
