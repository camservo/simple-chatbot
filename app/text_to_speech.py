import tempfile

import playsound
from gtts import gTTS


def text_to_speech(text, lang="en", tld="ie"):
    """
    Converts text to speech, saves it as a temporary audio file, and plays the file.

    This function utilizes the Google Text-to-Speech (gTTS) library to convert a given
    text string into speech in the specified language and dialect. The audio is then
    saved to a temporary file and played back using the playsound library.

    Parameters:
    - text (str): The text string to be converted to speech.
    - lang (str, optional): The language in which to synthesize the speech. Defaults to "en" (English).
    - tld (str, optional): The top-level domain for the Google Translate service that affects
      the accent/dialect. Defaults to "ie" for Ireland, affecting the English accent.

    Note:
    - The temporary audio file is automatically deleted after playback is complete.
    """

    # Create a gTTS object with the specified text and language settings.
    tts = gTTS(text=text, lang=lang, tld=tld)

    # Create a temporary file to save the synthesized speech audio. The 'delete=True' argument
    # ensures that the file is deleted once it is closed (after exiting the 'with' block).
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        # Save the synthesized speech audio to the temporary file.
        tts.save(fp.name)

        # Play the saved audio file. The playsound function blocks until the audio is finished playing.
        playsound.playsound(fp.name)
