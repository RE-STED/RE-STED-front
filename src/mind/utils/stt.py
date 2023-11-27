import speech_recognition as sr


def speak():
# 음성 인식 객체 생성
    r = sr.Recognizer()

    # 마이크에서 음성을 가져옴
    with sr.Microphone() as source:
        print("Speak Anything :")
        audio = r.listen(source)

        try:
            # 음성을 텍스트로 변환
            text = r.recognize_google(audio, language='en-US')
            print("You said : {}".format(text))
            return text
        except:
            print("Sorry could not recognize your voice")