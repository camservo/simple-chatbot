import os

from dotenv import load_dotenv
from openai import OpenAI

from app.audio import SpeechToTextConverter, TextToSpeechConverter
from app.openai import OpenAiQuery

if __name__ == "__main__":
    load_dotenv()
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    tts_converter = TextToSpeechConverter(client)
    stt_converter = SpeechToTextConverter(client)
    query_engine = OpenAiQuery(client)
    tts_converter.default_renderer = "chatgpt"
    stt_converter.default_renderer = "gtts"
    enable_voice = True
    n = 10
    for i in range(n):
        question = ""
        if enable_voice:
            question = stt_converter.convert()
        else:
            question = "hello, how are you?"
        if question:
            print("Question: ", question)
            for sentence in query_engine.get_openai_responses_in_sentences(
                question=question
            ):
                print("Response sentence: ", sentence)
                tts_converter.convert(text=sentence)
