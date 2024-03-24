import os

from dotenv import load_dotenv
from openai import OpenAI

import app.ask_questions as ask_questions
from app.audio import SpeechToTextConverter, TextToSpeechConverter

if __name__ == "__main__":
    load_dotenv()
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    tts_converter = TextToSpeechConverter(client)
    stt_converter = SpeechToTextConverter(client)
    tts_converter.default_renderer = "chatgpt"
    n = 1
    for i in range(n):
        question = stt_converter.convert()
        if question:
            print("Question: ", question)
            for sentence in ask_questions.get_openai_responses_in_sentences(
                client, question
            ):
                print("Sentence: ", sentence)
                tts_converter.convert(text=sentence)
