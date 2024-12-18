import queue
import sounddevice as sd
import vosk
import json

# 모델 경로 설정
ENGLISH_MODEL_PATH = "vosk-model-small-en-us-0.15"

# 오디오 스트림 설정
SAMPLE_RATE = 16000

def recognize_speech(model, q):
    rec = vosk.KaldiRecognizer(model, SAMPLE_RATE)
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = rec.Result()
            text = json.loads(result).get("text", "")
            if text:
                print(f"Recognized: {text}")
        else:
            partial_result = rec.PartialResult()
            partial_text = json.loads(partial_result).get("partial", "")
            # if partial_text:
            #     print(f"Partial: {partial_text}")

def main():
    q = queue.Queue()

    # 영어 모델 로드
    english_model = vosk.Model(ENGLISH_MODEL_PATH)

    # 오디오 스트림 콜백 함수
    def callback(indata, frames, time, status):
        q.put(bytes(indata))

    # 오디오 스트림 시작
    with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        print("Say something in English!")

        # 영어 음성 인식 스레드 시작
        recognize_speech(english_model, q)

if __name__ == "__main__":
    main()