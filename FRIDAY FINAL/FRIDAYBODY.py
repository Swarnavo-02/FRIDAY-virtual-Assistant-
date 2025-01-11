import pyttsx3
import speech_recognition 
import datetime
import webbrowser
import google.generativeai as genai
from config import apikey
import pyautogui
from bs4 import BeautifulSoup
import requests
from gtts import gTTS
import time
import random
import threading
import subprocess
import json
from newsapi import NewsApiClient
import wolframalpha
from mtranslate import translate
import requests
#genrating engine for voice

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[5].id)
rate = engine.setProperty("rate",180)


def speak(audio):
    global engine  # Declare 'engine' as global
    engine.say(audio)
    engine.runAndWait()

def take_command():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source, 0, 8)

    try:
        print("Understanding..")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")
    except Exception as e:
        print("Say that again")
        return "None"
    return query.lower()



genai.configure(api_key=apikey)

# Gemini ai import 

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048
}

# Initialize Generative Model

model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    generation_config=generation_config
)
def get_response(question, model):
   
    try:
        prompt = model.start_chat(history=[])
        prompt.send_message(question)
        response = prompt.last.text
        return response
    except Exception as e:
        print("Error getting response:", e)
        return ""
    
def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)
    subprocess.Popen(["notepad.exe", file_name])
# IMPORTING WEATHER API

def get_weather(city):
    api_key = "c194a7a32b3092c75e06b1617b6a2e02"

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
        weather_description = data["weather"][0]["main"]
        temp = data["main"]["temp"]
        weather_string = f"The weather in {city} is {weather_description} with a temperature of {temp} degrees Celsius."
        return weather_string
    except Exception as e:
        speak(f"Sorry ,currently the weather information for the specified place is not available ")
        return None

if __name__ == "__main__":
    
    is_jarvis_active = False
 

    while True:
        hinglish_phrase = take_command()
        english_trans = translate(hinglish_phrase, "en", "auto")
        query = english_trans.lower()
        sites = [["youtube", "https://www.youtube.com"], ["instagram", "https://www.instagram.com"],
                 ["chrome", "https://www.google.com"]]
        command = take_command()
        for site in sites:
                        if f"Open {site[0]}".lower() in query.lower():
                          speak(f"Opening {site[0]} sir.")
                          webbrowser.open(site[1])

        if command:
            if "pixel" in command.lower():
                if "start" in command.lower():
                    is_jarvis_active = True
                    print("Jarvis activated!")
                    speak("Jarvis activated!")

                elif "deactivate" in command.lower():
                    is_jarvis_active = False
                    print("Jarvis deactivated.")
                    speak( "Jarvis deactivated.")

                elif is_jarvis_active and "restart" in command.lower():
                  is_jarvis_active = True
                  print("Jarvis reactivated!")
                  speak("Jarvis reactivated!")
 
        while is_jarvis_active:
            hinglish_phrase = take_command()

            if hinglish_phrase:
                english_trans = translate(hinglish_phrase, "en", "auto")
                query = english_trans.lower()

                if "connect friday" in query:
                    speak("Connecting to friday  ...Disconnecting. Goodbye!")
                    print("Disconnecting...")
                    is_jarvis_active = False
                    break

                app_id = "QJUKAH-EJAVH9XP5X"
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
 
                
# open various sites ( provide link   # incomplete)
        
        

        if "friday" in query:
            from greetings import greetMe
            greetMe()

        elif "jonathan".lower() in query:
            response = get_response(query, model)
            print(f"F.R.I.D.A.Y : {response}") 
            speak(response)
                  
        elif "hello" in query or "halo" in query:
                    speak("Hello! Sir I am Friday and  i am ready to assist you. let me know if i can help you sir")
        elif "sure" in query:
                    speak("Good to know sir, is there anything you want me to help you with")
        elif "how are you" in query or "how r u" in query or " how r you" in query:
                    speak("Perfect, sir how's your day going? Feel free to ask me anything to assist you today")
        elif "thank you" in query or "for your help" in query:
                   speak("I am not worthy of your praise sir but still thank you it means a lot . Feel free to ask any other questions you might have")
        elif "thanks" in query:
                    speak("No problem at all! Your satisfaction is important to me")
        elif "ready" in query or "initiate" in query:
                    speak("Initiating auto voice control mode , activating all voice commands , you are ready to go sir")
               # elif "thank you" in query:
               #     speak("you are welcome, sir")
               # elif "thank you" in query:
                #    speak("you are welcome, sir")
                    

        # Determine the time and the date 
                    
        elif "the time" in query or "time" in query:
                      strTime = datetime.datetime.now().strftime("%H:%M")    
                      speak(f"Sir, the time is {strTime}")
                      speak("Do you need any more information?")

        elif "the date" in query or "date" in query: 
                      strdate = datetime.datetime.now().strftime("%d %B %Y")
                      speak(f"Sir, the analysed date is {strdate}")
                      speak("Do you need any more information?")

        # If feeling tired

        elif "tired" in query or ("bored") in query or ("bore") in query:
                     speak("Sir i have picked some music for you, hope you like it")
                     a = (1,2,3) # You can choose any number of songs (I have only choosen 3)
                     b = random.choice(a)
                     if b==1:
                         webbrowser.open("https://www.youtube.com/watch?v=HFF8ZIrkej0&list=RDHFF8ZIrkej0&index=1")
                     if b==2:
                         webbrowser.open("https://www.youtube.com/watch?v=4NRXx6U8ABQ&list=RDHFF8ZIrkej0&index=2")
                     if b==3:
                         webbrowser.open("https://www.youtube.com/watch?v=5-ZiKXrnvog&t=2s")

      # searching on GOOGle , youtube , wikipedia 
                                                    
        elif "google" in query:
                      from SearchNow import searchGoogle
                      searchGoogle(query)
        elif "youtube" in query:
                     from SearchNow import searchYoutube
                     searchYoutube(query)
        elif "wikipedia" in query:
                     from SearchNow import searchWikipedia
                     searchWikipedia(query)   

    # to make ai remember something
                         
        elif "remember that" in query or "remember" in query:  
                     rememberMessage = query.replace("remember that","") 
                     rememberMessage = query.replace("keep it in mind","")
                     speak("Your task have been stored in my memory,")
                     #remember_file.write(rememberMessage + "\n")

                     def ask_to_retrieve():
                         speak("Do you want to retrieve the data i stored in my memory?")

                         timer = threading.Timer(40, ask_to_retrieve)
                         timer.daemon = True
                         timer.start()

                     ask_to_retrieve()


        elif "what do you remember" in query:
                          speak("You told me to  " + rememberMessage )
                          speak("Do you need any more information? to store on my data")

    # Make an alarm where user can give input through voice
                          
        elif "set an alarm" in query or "alarm" in query:
                    speak("give a time for your alarm sir")
                    from alarm import givealarm
                    givealarm()

    #asking assistant to make a note and save it on same folder
                    
        elif "make a note" in query or "take a note" in query:
                       speak("What would you like me to write down?")
                       notetext = take_command()
                       note(notetext)
                       speak("You told me to write " )

    #asking assistant to locate any location on world via google maps
                       
        elif "where is" in query or "location of" in query:
                 ind = query.lower().split().index("is")
                 location = query.split()[ind + 1:]
                 speak = "This is where the location of" + str(location) + " is."
                 url = "https://www.google.com/maps/place/" + "".join(location)
                
                 webbrowser.open(url)

    # asking assistant to go to sleep for few seconds
                 

        elif "don't listen" in query or "do not listen" in query:
                    try:
                      speak("For how many seconds do you want me to sleep?")
                      a = int(take_command())
                      time.sleep(a)
                      speak(f"{a} seconds completed. Now you can ask me anything")

                    except ValueError:
                      speak("Invalid input, please enter a number of seconds") 

                    except Exception as e:
                      speak(f"Error occurred: {e}")
    
    # asking assistant to go to sleep permanently
                      
        elif "sleep" in query or "destruct" in query or "self destruct" in query:
                    speak("Initialising self destruct mode. 10...9...8...7...6...5...4...3...2....1.........just kidding  ,  Going to sleep,sir")
                    time.sleep(30)
                    speak("I am awake now, sir")
                    speak("Do you need any more assistance?")

        elif "stop" in query or "exit" in query:
                    speak("Terminating the execution, sir , Free feel to call me anytime if you need any Assistance")
                    exit()

    # asking assistant to take a screenshot and save it on same folder
                    
        elif "screenshot" in query or "take a screenshot" in query:
                    speak("sir, please provide me the name for this screenshot file")
                    name = take_command()
                    speak("sir, please wait while i take the screenshot")
                    time.sleep(3)
                    img = pyautogui.screenshot()
                    img.save(f"{name}.png")
                    speak("screenshot has been taken successfully and saved in our folder sir, now I am ready for new tasks")



        elif "news" in query:
                    url = (
                    "http://newsapi.org/v2/top-headlines?"
                    "country=in&"
                    "apiKey=3062ec12ee9e44f4b9fd71f0dde6e34f"
                )

                    try:
                          response = requests.get(url)
                          news = json.loads(response.text)
                    except:
                        speak("Please check your connection")
                    
                   
        if 'news' in locals():
                 for index, new in enumerate (news["articles"][:6]):
                     print(str(new["title"]), "\n")
                     speak(str(new["title"]))
                     engine.runAndWait()
                     time.sleep(2)

                     print(str(new["description"]), "\n")
                     speak(str(new["description"]))
                     engine.runAndWait()
                     time.sleep(2)  
 
               
                 speak("Do you want to hear more daily news and update , sir")
                 query = take_command().lower()
                 if "more" in query:
                    speak("Here are some more news, sir")
                    for index, new in enumerate (news["articles"][6:12]):
                          print(str(new["title"]), "\n")
                          speak(str(new["title"]))
                          engine.runAndWait()
                          time.sleep(2)
                          print(str(new["description"]), "\n")
                          speak(str(new["description"]))
                          engine.runAndWait()
                          time.sleep(2)

                    if "no" in query:
                        speak("Thank you, sir, for listening")
                        break
 # CHECKING WEATHER STATUS
                      
        elif "weather" in query or "temparature" in query:
                    city = query.split(" ")[2]
                    weather_string = get_weather(city)
                    if weather_string:
                        speak(weather_string)
                        speak("Do you need any more information?")
                        query = take_command().lower()
                        if "yes"  in query:
                            speak("What information do you need?")
                            query = take_command().lower()
                            if "weather" or "temparature" in query:
                                city = query.split(" ")[2]
                                weather_string = get_weather(city)
                                if weather_string:
                                    speak(weather_string)
                            else:
                                speak("Sorry, I don't have that information available.") 
                                continue
    # google automation
                            

        elif "search" in query:
                    query = query.replace("search","")
                    pyautogui.hotkey("alt" , "d") 
                    pyautogui.write(f"{query}", 0.1)   
                    pyautogui.press("enter")
                    speak("Your Query has been searched, sir")
                    speak("Do you need any more information?")
        elif "incognito" in query:
                    pyautogui.hotkey("ctrl","shift","n")
                    speak("Initialising Incognito mode, sir")
                    speak("Do you want to open any website?")
        elif "new tab" in query or "another tab" in query:
                    pyautogui.hotkey("ctrl", "t")
                    speak("New tab opened, sir")
                    speak("Do you want to open any website? To search any website speak search")
        elif "close all tabs" in query or "close tabs" in query or "close" in query:
                    pyautogui.hotkey("ctrl", "shift", "w")
                    speak("All tabs closed, sir")
                    speak("Let me know what else you need")
        elif "voice" in query or "voise" in query:
                    pyautogui.hotkey("ctrl", "shift", ".")
                    speak("Voice mode activated, sir , Voice search any website")
        elif "new window" in query:
                    pyautogui.hotkey("ctrl", "n")
                    speak("New window opened, sir")
        elif "history" in query or "histree" in query:
                    pyautogui.hotkey("ctrl", "h")
                    speak("Webpage History has been opened, sir")
        elif "clear" in query:
                    pyautogui.hotkey("ctrl", "shift", "Del")
                    speak("Webpage History cleared, sir")
        elif "download" in query or "downloads" in query:
                    pyautogui.hotkey("ctrl", "j")
                    speak("Downloads section opened, sir")
        elif "reload" in query or "reload page" in query:
                    pyautogui.hotkey("ctrl", "r")
                    speak("Page has been reloaded, sir")
        elif "add bookmark" in query or "bookmark" in query or "bookmark page" in query:
                    pyautogui.hotkey("ctrl", "d")
                    speak("Bookmark has been added to the page, sir")
        elif "scroll" in query or "scroll down" in query:
                    pyautogui.press('space')
                    speak("Scroll mode activated, sir")
        elif "page top" in query or "top of the page" in query or " top of page" in query:
                    pyautogui.press('home')
                    speak("Top of page, sir") 


       
  # FULL AUTOMATION ON YOUTUBE    
           
        elif "find" in query :
                    query = query.replace("find", "")
                    pyautogui.hotkey("alt", "d")
                    time.sleep(1)
                    pyautogui.press("tab")
                    pyautogui.press("tab")
                    pyautogui.press("tab")
                    pyautogui.press("tab")
                    pyautogui.press("tab")
                    pyautogui.press("tab")
                    time.sleep(1)
                    pyautogui.write(f"{query}", 0.2)
                    pyautogui.press("enter") 
                    speak("Your Query has been searched, sir")
        elif "select" in query or "first video" in query or "select first video" in query:   
                    time.sleep(5)
                    x_coordinate = 635
                    y_coordinate = 299
                    pyautogui.click(x=x_coordinate, y=y_coordinate)
                    speak("Video is starting")
        elif "pause" in query:
                    pyautogui.press("k")
                    speak("video paused , sir")
        elif "play" in query:
                    pyautogui.press("k")
                    speak("video played , sir")
        elif "mute" in query:
                     pyautogui.press("m")
                     speak("video muted sir ")
                     speak("Do you want to increase or decrease the volume?")
        elif "unmute" in query or "un mute" in query:
                    pyautogui.press("m")
                    speak("video unmuted sir ")
                    speak("Do you want to increase or decrease the volume?")
        elif "maximize" in query or "maximise" in query:
                    pyautogui.press("f")
                    speak("Screen has been maximized sir ")
        elif 'next' in query:
                    pyautogui.press('Right')
                    speak("Next video sir")
        elif 'previous' in query:
                    pyautogui.press('left')
                    speak("Previous video sir")      
        elif 'minimize' in query or "minimise" in query:
                    pyautogui.press('esc')
                    speak("Screen has been minimized sir ")
        elif 'skip' in query or "forward" in query:
                    pyautogui.press('l')
                    speak("Video skipped by 10 second sir")
        elif 'volume up' in query or 'increase volume' in query or 'volume increase' in query:
                    pyautogui.press('volumeup')
                    speak("Volume has been increased sir")
        elif 'volume down' in query or 'decrease volume' in query or 'volume decrease' in query:
                    pyautogui.press('volumedown')
                    speak("Volume has been decreased sir")
        elif 'mute' in query:
                    pyautogui.press('volumemute')
                    speak("Volume has been muted sir ")  


# open , close any opened application running
                    
        elif "open" in query:
                    from opencloseapp import openappweb
                    openappweb(query)
        elif "terminate" in query:
                    from opencloseapp import closeappweb
                    closeappweb(query)               
        elif "full screen" in query:
                    pyautogui.hotkey("F11")
                    speak("Full screen mode activated, sir")




    while True:
        command = take_command()

        if command:
            if "jarvis" in command.lower() and "run" in command.lower():
                print("Jarvis activated!")
                speak("Jarvis activated!")
                is_jarvis_active = True

            elif "friday" in command.lower() and "deactivate" in command.lower():
                print("Jarvis deactivated.")
                speak("Jarvis deactivated.")
                is_jarvis_active = False

        while is_jarvis_active:
            hinglish_phrase = take_command()

            if hinglish_phrase:
                english_trans = translate(hinglish_phrase, "en", "auto")
                query = english_trans.lower()

                if "disconnect" in query:
                    speak("Disconnecting. Goodbye!")
                    print("Disconnecting...")
                    is_jarvis_active = False
                    break

                app_id = "QJUKAH-EJAVH9XP5X"
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

 









        

                    

















