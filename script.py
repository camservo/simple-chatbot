from openai import OpenAI
import speech_recognition as sr
from gtts import gTTS
import os
import playsound
import json
# import nltk
from dotenv import load_dotenv
# import re

load_dotenv()
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

def listen_and_transcribe():
    # Create a recognizer object
    r = sr.Recognizer()

    # Open the microphone and start listening
    with sr.Microphone() as source:
        print("Speak something!")
        audio = r.listen(source)

    # Recognize the speech using Google Speech Recognition
    try:
        text = r.recognize_google(audio)
        print("You said: " + text)
        return text + append_string
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def ask_openai(question):
    buffer = ""  # Initialize a buffer to accumulate text chunks

    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "Please place every sentence in it's own complete json object.  The key of each sentence should be 'message'"},
            {"role": "user", "content": question},
        ],
        stream=True,
        # max_tokens=5
    )        
    for chunk in response:
        if chunk.choices[0].delta.content:
            # print('Chunk: ', chunk.choices[0].delta.content)  # Assuming the correct chunk structure
            buffer += str(chunk.choices[0].delta.content)
        try:
            obj = json.loads(buffer)
            yield obj["message"]
            buffer = ""
            
        except json.JSONDecodeError:
            continue

    if buffer.strip():
        yield buffer.strip()

def text_to_speech(text):
    tts = gTTS(text=text, lang='en', tld='ie')
    filename = "response.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

if __name__ == "__main__":
    n = 1
    for i in range(n):
        question = listen_and_transcribe()
        if question:
            print("Question: ", question)
            for sentence in ask_openai(question):
                print
                print(sentence)
                text_to_speech(sentence)
        

