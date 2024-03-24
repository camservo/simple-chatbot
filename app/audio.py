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
    def __init__(
        self,
        client,
        default_renderer="speech_recognition",
        default_input_type="microphone",
    ):
        """
        Initializes a new instance of the TextToSpeechConverter class.
        """
        self.client = client
        self.default_renderer = default_renderer
        self.default_input_type = default_input_type

    def convert(self, renderer=None, input_type=None):
        try:
            renderer = renderer or self.default_renderer
            input_type = input_type or self.default_input_type
            if renderer == "speech_recognition":
                response = self.convert_sr(input_type=input_type)
                return response
            else:
                logging.error(f"Unknown renderer: {renderer}")
        except Exception as e:
            logging.error(f"Error in convert method: {str(e)}")

    def get_microphone_input(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print("You said: " + text)
            return text
        except sr.UnknownValueError:
            # This exception is raised if the speech is unintelligible.
            print("Could not understand audio")
        except sr.RequestError as e:
            # This exception is raised if there's an issue with the Google API request.
            print(
                f"Could not request results from Google Speech Recognition service; {e}"
            )

    def convert_sr(self, input_type=None):
        input_type = input_type or self.default_input_type
        if input_type.lower() == "microphone":
            input = self.get_microphone_input()
            return input
