import pyttsx3
import time
import datetime
import speech_recognition as sr
import dateutil.parser
import os



def get_alarm_time():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say the alarm time (e.g., 'Set alarm for 7:30 AM')")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        time_str = recognizer.recognize_google(audio)
        print(f"Recognized time string: {time_str}")
        time_str_cleaned = time_str.replace("set alarm for", "").strip()
        print(f"Cleaned time string: {time_str_cleaned}")

        alarm_time = dateutil.parser.parse(time_str_cleaned)
        print(f"Parsed alarm time: {alarm_time}")
        return alarm_time
    except sr.UnknownValueError:
        print("Sorry, could not understand the audio. Please try again.")
        return get_alarm_time()
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None
    except ValueError as e:
        print(f"Error parsing the time: {e}")
        print("Please try again with a valid time format.")
        return get_alarm_time()

def givealarm():
    engine = pyttsx3.init()

    while True:
        alarm_time = get_alarm_time()

        if alarm_time:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            print(f"Alarm set for {alarm_time.strftime('%I:%M %p')}. Current time is {current_time}.")

            while datetime.datetime.now() < alarm_time:
                time.sleep(1)

            print("Time to wake up!")
            engine.say("Wake up! It's time to start your day.")
            engine.runAndWait()
            os.startfile("musicsolo.mp3")
            break

           

if __name__ == "__main__":
    givealarm()
    
