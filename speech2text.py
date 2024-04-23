import speech_recognition as sr


def speech_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # checks for ambient noise
        print("Talk...")
        try:
            audio = recognizer.listen(source)
        except:
            exit(0)

    try:
        text = recognizer.recognize_google(audio, language="en-US")
        return text
    except:
        exit(0)
