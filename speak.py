from gtts import gTTS
import os
from playsound import playsound

def speak(text):
    print(f"CECAR: {text}")
    tts = gTTS(text=text, lang='en')
    filename = "temp.mp3"
    tts.save(filename)
    playsound(filename)
    os.remove(filename)
