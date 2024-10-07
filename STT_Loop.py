import speech_recognition as sr
import threading

def recognize_speech_from_mic(recognizer, microphone):
    response = {
        "success": False,
        "error": None,
        "transcription": None
    }

    # 마이크로부터 음성 수집 (최대 3초까지만 듣기)
    with microphone as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=1, phrase_time_limit=3)  # 짧게 듣기
        except sr.WaitTimeoutError:
            print("Timeout: No speech detected within the time limit.")
            return response  # 시간 초과 시 빈 response 반환

    # Google STT로 음성 인식
    try:
        response["transcription"] = recognizer.recognize_google(audio, language="ko-KR")
        response["success"] = True
    except sr.RequestError:
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response

def process_speech(recognizer, microphone):
    while True:
        response = recognize_speech_from_mic(recognizer, microphone)

        if response["success"]:
            print(f"You said: {response['transcription']}")
        else:
            print("I didn't catch that. What did you say?")

        if response["error"]:
            print(f"ERROR: {response['error']}")

def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # 배경 소음 조정은 한 번만 실행
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Calibration completed. Starting STT loop.")

    # 음성 인식 스레드 시작
    speech_thread = threading.Thread(target=process_speech, args=(recognizer, microphone))
    speech_thread.start()

if __name__ == "__main__":
    main()