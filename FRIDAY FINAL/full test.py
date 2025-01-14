import pyttsx3
import speech_recognition as sr
from mtranslate import translate
import wolframalpha

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)  # Using the first voice
engine.setProperty("rate", 180)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source, timeout=8)

    try:
        print("Understanding...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")
        return query.lower()
    except sr.UnknownValueError:
        print("Say that again...")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

if __name__ == "__main__":
    while True:
        # Wait for the wake-up command (e.g., "Jarvis")
        wakeup_command = "Friday"
        print("Say the wake-up command to activate Jarvis...")
        
        while True:
            command = take_command()
            
            if command and wakeup_command in command:
                print("Jarvis activated!")
                speak("Jarvis activated!")
                break

        while True:
            hinglish_phrase = take_command()

            if hinglish_phrase:
                english_trans = translate(hinglish_phrase, "en", "auto")
                query = english_trans.lower()

                if "disconnect" in query:
                    speak("Disconnecting. Goodbye!")
                    print("Disconnecting...")
                    break

                app_id = "API KEY"
                client = wolframalpha.Client(app_id)
                
                speak("What do you want to know, sir?")
                query = take_command()

                if query:
                    query = query.lower()
                    res = client.query(query)

                    try:
                        answer = next(res.results).text
                    except StopIteration:
                        answer = "I'm sorry, I couldn't find any relevant information."

                    speak(answer)
                    print(answer)
