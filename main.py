import speech_recognition as sr
import webbrowser
import pyttsx3
import time


r=sr.Recognizer()
   
def speak(text):
    engine=pyttsx3.init('sapi5')
    engine.setProperty('rate', 220)
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()
    # engine.stop()
def wish_user():
    speak("INITIALISING JARVIS...What can  I do for you") 
    speak("Hello MASTER")   

def take_command():
    with sr.Microphone() as source:
        print("\nListening....")
        r.pause_threshold=1
        audio=r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')   # type: ignore
        print(f"You said: {query}\n")
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I could not understand your audio.")
        return ""
    
    except sr.RequestError:
        print("Could not request results from Google. Check your internet connection.")
        return ""
def to_wake():
    while True:
        query=take_command()
        if "jarvis" in query:
            speak("I am Awaken")
            return




if __name__=="__main__":
    wish_user()

    while True:
        to_wake()
        speak("listening to your command")
        command=take_command()
        if  "exit" in command :
            speak("Nice talking to You")
            break
           
        else:
            speak("You said "+command)