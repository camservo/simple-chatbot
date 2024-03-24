import speech_recognition as sr


def listen_and_transcribe():
    """
    Listens to an audio input from the microphone and transcribes it to text using Google's Speech Recognition.

    This function initializes the microphone, listens for an audio input, and then attempts
    to convert the audio to text using Google's Speech Recognition API. If the audio is
    successfully recognized, the transcribed text is printed and returned. If the audio
    is not understood or if there's an issue with the request to Google's service, an
    error message is printed instead.

    Returns:
    - str: The transcribed text if the audio is successfully recognized. None is returned
           if an error occurs during speech recognition.
    """

    # Create a recognizer object from the speech_recognition library.
    r = sr.Recognizer()

    # Open the microphone for listening. The 'with' statement ensures that the microphone
    # is properly closed after finishing the block, even if an error occurs.
    with sr.Microphone() as source:
        print("Speak something!")
        # Listen for the first phrase and extract the audio data
        audio = r.listen(source)

    # Try to recognize the speech in the audio using Google's Speech Recognition API.
    try:
        # Attempt to convert the audio to text.
        text = r.recognize_google(audio)
        print("You said: " + text)
        return text
    except sr.UnknownValueError:
        # This exception is raised if the speech is unintelligible.
        print("Could not understand audio")
    except sr.RequestError as e:
        # This exception is raised if there's an issue with the Google API request.
        print(f"Could not request results from Google Speech Recognition service; {e}")
