import pyttsx3
import datetime
import datetime


engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[5].id)
engine.setProperty("rate",180)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def greetMe():
    hour  = int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        speak("Good Morning sir")
        strTime = datetime.datetime.now().strftime("%H:%M")    
        speak(f"It is {strTime}")
        speak(" I am ready to assist you. let me know how i can help you ")
        
        
    elif hour >12 and hour<=18:
        speak("Good Afternoon sir")
        strTime = datetime.datetime.now().strftime("%H:%M")    
        speak(f"It is {strTime}")
        speak(" i am ready to assist you. let me know how i can help you ")
       


    elif hour >18 and hour<=24:
        speak("Good Evening  sir ")
        strTime = datetime.datetime.now().strftime("%H:%M")    
        speak(f"It is {strTime}")

        speak( "  i am ready to assist you. let me know how i can help you ")
        
 