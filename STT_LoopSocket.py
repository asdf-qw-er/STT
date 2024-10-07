import socket
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

def send_to_unity(message, client_socket):
    try:
        # 메시지를 UTF-8로 인코딩하여 전송
        client_socket.sendall(message.encode('utf-8'))
        print(f"Sent to Unity: {message}")
    except Exception as e:
        print(f"Failed to send message: {e}")

def process_speech(client_socket, recognizer, microphone):
    while True:
        response = recognize_speech_from_mic(recognizer, microphone)

        if response["success"]:
            print(f"You said: {response['transcription']}")
            send_to_unity(response['transcription'], client_socket)
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

    # Unity 서버와 클라이언트 연결 설정
    server_ip = '127.0.0.1'  # Unity 서버 IP 주소
    port = 5555  # Unity 서버와 동일한 포트 번호

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_ip, port))
        print(f"Connected to Unity server at {server_ip}:{port}")
    except Exception as e:
        print(f"Failed to connect to Unity server: {e}")
        return

    # 음성 인식 스레드 시작
    speech_thread = threading.Thread(target=process_speech, args=(client_socket, recognizer, microphone))
    speech_thread.start()

if __name__ == "__main__":
    main()