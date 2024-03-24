import speech_recognition as sr


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
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(
                e
            )
        )
