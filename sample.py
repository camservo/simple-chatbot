import os

from dotenv import load_dotenv
from openai import OpenAI

import app.ask_questions as ask_questions
import app.speech_to_text as speech_to_text
from app.audio import TextToSpeechConverter

# # import app.text_to_speech as text_to_speech
# from app.text_to_speech import text_to_speech

if __name__ == "__main__":
    load_dotenv()
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    tts_converter = TextToSpeechConverter(client)
    # tts_converter.default_renderer = "chatgpt"
    n = 1
    for i in range(n):
        # question = speech_to_text.listen_and_transcribe()
        question = "can you tell me a few sample sentences?"
        if question:
            print("Question: ", question)
            for sentence in ask_questions.get_openai_responses_in_sentences(
                client, question
            ):
                print("Sentence: ", sentence)
                tts_converter.convert(text=sentence)
