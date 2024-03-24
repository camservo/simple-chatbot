import logging
import tempfile

import playsound
import speech_recognition as sr
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


class SpeechToTextConverter:
    """
    A class to convert speech to text using various backends.

    This class facilitates converting speech input, either from a microphone or other sources,
    into text by using different speech recognition services or APIs. Currently, it primarily supports
    microphone input through the speech_recognition library's Google Web Speech API interface.

    Attributes:
        client: The API client or configuration used for speech recognition services. (Placeholder attribute, as the current implementation does not directly use it with Google's Web Speech API.)
        default_renderer (str): The default backend service for speech-to-text conversion.
        default_input_type (str): The default input type for capturing speech.
    """

    def __init__(
        self,
        client,
        default_renderer="speech_recognition",
        default_input_type="microphone",
    ):
        """
        Initializes a new instance of the SpeechToTextConverter class.

        Args:
            client: A placeholder for an API client or configuration. Currently unused.
            default_renderer (str): The default service for speech-to-text conversion. Defaults to 'speech_recognition'.
            default_input_type (str): The default method of capturing speech. Defaults to 'microphone'.
        """
        self.client = client
        self.default_renderer = default_renderer
        self.default_input_type = default_input_type

    def convert(self, renderer=None, input_type=None):
        """
        Converts speech to text using the specified or default renderer and input type.

        Args:
            renderer (str, optional): The speech-to-text service to use. Currently supports 'speech_recognition' only.
            input_type (str, optional): The method of capturing speech. Currently supports 'microphone' only.

        Returns:
            str: The recognized text from speech input.

        Raises:
            Logs an error if an unknown renderer is specified or if an exception occurs during processing.
        """
        try:
            renderer = renderer or self.default_renderer
            input_type = input_type or self.default_input_type
            if renderer == "speech_recognition":
                return self.convert_sr(input_type=input_type)
            else:
                logging.error(f"Unknown renderer: {renderer}")
        except Exception as e:
            logging.error(f"Error in convert method: {str(e)}")

    def get_microphone_input(self):
        """
        Captures audio input from the microphone and converts it to text using Google's Web Speech API.

        Returns:
            str: The recognized text from the microphone input.

        Raises:
            Prints a message to the console if the speech is unintelligible or if a request error occurs.
        """
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)
        try:
            return r.recognize_google(audio)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(
                f"Could not request results from Google Speech Recognition service; {e}"
            )

    def convert_sr(self, input_type=None):
        """
        Converts speech to text based on the input type. Currently, only 'microphone' input type is supported.

        Args:
            input_type (str, optional): The method of capturing speech. Defaults to the instance's default input type.

        Returns:
            str: The recognized text from the specified input type.
        """
        if input_type.lower() == "microphone":
            return self.get_microphone_input()
