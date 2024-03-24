import os

from dotenv import load_dotenv
from openai import OpenAI

import app.ask_questions as ask_questions
import app.speech_to_text as speech_to_text
import app.text_to_speech as text_to_speech

if __name__ == "__main__":
    load_dotenv()
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    n = 1
    for i in range(n):
        question = speech_to_text.listen_and_transcribe()
        if question:
            print("Question: ", question)
            for sentence in ask_questions.get_openai_responses_in_sentences(
                client, question
            ):
                print
                print(sentence)
                text_to_speech(sentence)
