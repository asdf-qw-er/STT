import speech_recognition as sr

def recognize_speech_from_mic(recognizer, microphone):
    """
    Recognize speech from the microphone in Korean only.
    
    :param recognizer: Recognizer instance from speech_recognition
    :param microphone: Microphone instance from speech_recognition
    :return: A dictionary with keys 'success', 'error', and 'transcription'
    """
    
    # Check if the recognizer and microphone arguments are of the correct type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be an instance of `speech_recognition.Recognizer`")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be an instance of `speech_recognition.Microphone`")
    
    # Initialize the response dictionary
    response = {
        "success": False,
        "error": None,
        "transcription": None
    }
    
    # Adjust the recognizer sensitivity to ambient noise and record audio from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
    
    try:
        # Recognize speech using Google Web Speech API for Korean language
        response["transcription"] = recognizer.recognize_google(audio, language="ko-KR")
        response["success"] = True
        response["error"] = None
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # Speech was unintelligible
        response["error"] = "Unable to recognize speech"
    
    return response

def main():
    # Create recognizer and microphone instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    print("Say something in Korean!")
    
    # Recognize speech from the microphone
    response = recognize_speech_from_mic(recognizer, microphone)
    
    # Display the response
    if response["success"]:
        print("You said: {}".format(response["transcription"]))
    else:
        print("I didn't catch that. What did you say?")
    
    if response["error"]:
        print("ERROR: {}".format(response["error"]))

if __name__ == "__main__":
    main()