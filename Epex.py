# only works on python 3.12 version 

import pyautogui
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import requests
import os
import sys
import pywhatkit
import pyjokes
import pyautogui
from urllib.parse import quote
import win32com.client 

# ------------------- API KEY -------------------
API_KEY = " your API key"

# ------------------- SPEAK -------------------
def speak(text):
    print(f"Epex: {text}")
    try:
        
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Rate = 2
        speaker.Speak(text)
    except Exception as e:
        print(f"Audio error: {e}")

# ------------------- GREET -------------------
def greet():
    hour = datetime.datetime.now().hour
    if hour < 12:
        greeting = "Good morning"
    elif hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    speak(f"{greeting}! I am Epex, your virtual assistant. How can I help you?")

# ------------------- TAKE COMMAND -------------------
def take_command():
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(source, phrase_time_limit=6)
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language="en-in")
            print(f"You said: {query}")
            return query.lower()

        except sr.WaitTimeoutError:
            return ""

        except sr.UnknownValueError:
            speak("Sorry, I didn't understand. Please say again.")
            return ""

        except sr.RequestError:
            speak("Speech service is unavailable right now.")
            return ""

# ------------------- WIKIPEDIA -------------------
def search_wikipedia(query):
    topic = query.replace("wikipedia", "").strip()

    if not topic:
        speak("What should I search on Wikipedia?")
        return

    try:
        result = wikipedia.summary(topic, sentences=2)
        speak(result)

    except wikipedia.exceptions.DisambiguationError:
        speak("That topic is too broad. Please be specific.")

    except wikipedia.exceptions.PageError:
        speak("No Wikipedia page found for this topic.")

    except Exception:
        speak("Error while searching Wikipedia.")

# ------------------- OPEN WEBSITE -------------------
def open_website(name, url):
    speak(f"Opening {name}")
    webbrowser.open(url)

# ------------------- WEATHER -------------------
def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        data = requests.get(url).json()

        if data.get("cod") != 200:
            speak("City not found.")
            return

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]

        speak(f"Weather in {city} is {desc} with {temp} degree celsius and humidity {humidity} percent.")

    except Exception:
        speak("Unable to get weather right now.")

# ------------------- CALCULATOR -------------------
def calculate_expression(query):
    try:
        expr = query.lower()
        replacements = {
            "plus": "+",
            "add": "+",
            "minus": "-",
            "subtract": "-",
            "times": "*",
            "multiply": "*",
            "x": "*",
            "divided by": "/",
            "divide": "/",
            "over": "/"
        }

        for word, symbol in replacements.items():
            expr = expr.replace(word, symbol)

        expr = expr.replace(" ", "")

        allowed = "0123456789+-*/()."
        if not all(ch in allowed for ch in expr):
            speak("I can calculate only numbers.")
            return

        result = eval(expr)
        speak(f"The answer is {result}")

    except Exception:
        speak("Calculation error.")

# ------------------- HANDLE QUERY -------------------
def handle_query(query):

    if "time" in query:
        speak(datetime.datetime.now().strftime("Time is %H:%M"))

    elif "date" in query:
        speak(datetime.datetime.now().strftime("Today's date is %B %d, %Y"))

    elif "wikipedia" in query:
        search_wikipedia(query)

    elif "open youtube" in query:
        open_website("YouTube", "https://www.youtube.com")

    elif "open google" in query:
        open_website("Google", "https://www.google.com")

    elif "play music" in query:
        open_website("JioSaavn", "https://www.jiosaavn.com")

    elif "open chat gpt" in query or "open chatgpt" in query:
        open_website("ChatGPT", "https://chat.openai.com")

    elif "weather" in query:
        speak("Tell me the city name.")
        city = take_command()
        if city:
            get_weather(city)

    elif any(op in query for op in ["+", "-", "*", "/"]):
        calculate_expression(query)

    elif "who are you" in query:
        speak("I am Epex, your personal virtual assistant.")

    elif "who is your creator" in query:
        speak("I was created by Sukhvir.")
        
    elif "open notepad" in query:
        speak("Opening Notepad for you.")
        os.system("start notepad")

    elif "open calculator" in query:
        speak("Opening Calculator.")
        os.system("start calc")

    elif "open command prompt" in query or "open cmd" in query:
        speak("Opening Command Prompt.")
        os.system("start cmd")
       
    elif "play" in query:
       
        song = query.replace("play", "").strip()
        speak(f"Playing {song} for you.")
        

        pywhatkit.playonyt(song)
        
    elif "joke" in query:
        
        joke = pyjokes.get_joke()
        speak(joke)

    elif "exit" in query or "quit" in query or "stop" in query:
        speak("Goodbye! Have a great day.")
        sys.exit()

    else:
        speak("I am not trained for this yet.")
        
        
        

# ------------------- MAIN LOOP -------------------
def run_assistant():
    greet()
    while True:
        query = take_command()
        if query:
            handle_query(query)

# ------------------- START -------------------
if __name__ == "__main__":
    run_assistant()
