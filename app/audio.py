import logging
import os
import queue
import tempfile
import threading
import time

import speech_recognition as sr
from playsound import playsound

LOGLEVEL = os.environ.get("LOGLEVEL", "WARNING").upper()
logging.basicConfig(level=LOGLEVEL)


class TextToSpeechConverter:
    """
    Converts text into speech using different backends, including OpenAI's GPT model for text-to-speech conversion and Google's Text-to-Speech (gTTS) API. Allows specifying models, voices, languages, and TLDs for customization. Implements a queue system for orderly processing and playback.
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
        self.client = client
        self.default_gpt_model = default_gpt_model
        self.default_gpt_voice = default_gpt_voice
        self.default_renderer = default_renderer
        self.default_gtts_lang = default_gtts_lang
        self.default_gtts_tld = default_gtts_tld
        self.convert_queue = queue.Queue()
        self.playback_queue = queue.Queue()
        self.convert_worker_thread = threading.Thread(target=self.process_convert_queue)
        self.convert_worker_thread.daemon = True
        self.convert_worker_thread.start()
        self.playback_worker_thread = threading.Thread(
            target=self.process_playback_queue
        )
        self.playback_worker_thread.daemon = True
        self.playback_worker_thread.start()
        self.playback_complete = False

    def convert(self, text, renderer=None):
        renderer = renderer or self.default_renderer
        self.convert_queue.put((text, renderer))

    def process_convert_queue(self):
        while True:
            text, renderer = self.convert_queue.get()
            try:
                if renderer == "chatgpt":
                    self.convert_gpt(text=text)
                elif renderer == "gtts":
                    self.convert_gtts(text=text)
                else:
                    logging.error(f"Unknown renderer: {renderer}")
            finally:
                self.convert_queue.task_done()

    def convert_gpt(self, text, model=None, voice=None):
        model = model or self.default_gpt_model
        voice = voice or self.default_gpt_voice
        try:
            response = self.client.audio.speech.create(
                model=model, voice=voice, input=text
            )
            self.playback_complete = False
            self.playback_queue.put(response)
        except Exception as e:
            logging.error(f"Error in convert_gpt method: {str(e)}")

    ## Need to figure out how to maintain this better
    # def convert_gtts(self, text, lang=None, tld=None):
    #     lang = lang or self.default_gtts_lang
    #     tld = tld or self.default_gtts_tld
    #     try:
    #         tts = gTTS(text=text, lang=lang, tld=tld)
    #         with tempfile.NamedTemporaryFile(delete=True) as fp:
    #             tts.save(fp.name)
    #             playsound(fp.name)
    #     except Exception as e:
    #         logging.error(f"Error in convert_gtts method: {str(e)}")

    def process_playback_queue(self):
        while True:
            response = self.playback_queue.get()
            try:
                with tempfile.NamedTemporaryFile(delete=True) as fp:
                    response.stream_to_file(fp.name)
                    playsound(fp.name)
                    if self.playback_queue.empty():
                        self.playback_complete = True
                    else:
                        time.sleep(0.25)
            except Exception as e:
                logging.error(f"Error in playback method: {str(e)}")


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
            recognizer.adjust_for_ambient_noise(source)
            # This should be done once per session rather than every loop.
            logging.debug("Adjusting for ambient noise")
        with sr.Microphone() as source:
            print("listening...")
            audio = recognizer.listen(source)
            return self.render(renderer, audio)

    def render(self, renderer, audio):
        """
        Renders the audio into text using the specified renderer.

        :param renderer: The renderer to use for speech recognition.
        :param audio: The captured audio to be converted into text.
        :return: The recognized text.
        """
        ## TODO: Rendering should be done by submitting requests to a queue
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
