import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser

engine = pyttsx3.init()
engine.setProperty("rate", 200)  
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)  

def speak(text):

    print(f"Epex: {text}")
    engine.say(text)
    engine.runAndWait()

def greet():

    hour = datetime.datetime.now().hour
    if hour < 12:
        greeting = "Good morning"
    elif hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    speak(f"{greeting}! I am Epex, your virtual assistant. How can I help you today?")

def take_command():
    
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        try:
            audio = recognizer.listen(source, timeout=5)
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-in')
            print(f"You said: {query}")
            return query.lower()
        except sr.WaitTimeoutError:
            speak("You didn’t say anything. Please try again.")
        except sr.UnknownValueError:
            speak("Sorry, I didn’t catch that. Can you repeat?")
        except sr.RequestError:
            speak("Speech service is currently unavailable.")
        return ""

def search_wikipedia(query):
    topic = query.replace("wikipedia", "").strip()
    if not topic:
        speak("What should I search on Wikipedia?")
        return
    try:
        results = wikipedia.summary(topic, sentences=2)
        speak(f"Here’s what I found about {topic}:")
        speak(results)
    except wikipedia.exceptions.DisambiguationError:
        speak("That topic is too broad. Please be more specific.")
    except wikipedia.exceptions.PageError:
        speak("I couldn’t find anything on Wikipedia.")
    except Exception:
        speak("Something went wrong while searching Wikipedia.")

def open_website(site_name, url):
    speak(f"Opening {site_name}")
    webbrowser.open(url)

def handle_query(query):
    
    if "time" in query:
        current_time = datetime.datetime.now().strftime("%H:%M")
        speak(f"The time is {current_time}")

    elif "date" in query:
        current_date = datetime.datetime.now().strftime("%B %d, %Y") 
        speak(f"Today's date is {current_date}")

    elif "wikipedia" in query:
        speak("Searching Wikipedia...")
        search_wikipedia(query)

    elif "open youtube" in query:
        open_website("YouTube", "https://www.youtube.com")

    elif "open google" in query:
        open_website("Google", "https://www.google.com")

    elif "play music" in query:
        open_website("JioSaavn", "https://www.jiosaavn.com")

    elif "open chat gpt" in query or "open chatgpt" in query:
        open_website("ChatGPT", "https://chat.openai.com")
    
        
    elif "who are you" in query:
        speak("I am Epex, your personal virtual assistant created to make your life easier and more fun.")

    elif "who is your creator" in query:
        speak("I was created by Sukhvir, a passionate developer who loves smart and creative solutions.")

    elif "exit" in query:
        speak("Goodbye! Have a nice day.")
        return False

    else:
        speak("I'm not sure how to help with that yet.")
    
    return True

def run_assistant():
    greet()
    while True:
        query = take_command()
        if query and not handle_query(query):
            break

if __name__ == "__main__":
    run_assistant()
