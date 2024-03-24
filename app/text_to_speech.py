import tempfile

import playsound
from gtts import gTTS


def text_to_speech(text, lang="en", tld="ie"):
    tts = gTTS(text=text, lang=lang, tld=tld)
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts.save(fp.name)
        playsound.playsound(fp.name)
