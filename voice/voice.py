import speech_recognition as sr
while(True):
# Recording the audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak Anything :")
        audio = r.listen(source)

# Recognizing the text
    try:
        text = r.recognize_sphinx(audio, language="en-US")
        print("You said : {}".format(text))
    except:
        print("Sorry could not recognize your voice")