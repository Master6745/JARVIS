import openai

import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
from gtts import gTTS
import pygame
import os
import uuid
from openai import OpenAI, RateLimitError, APIError

import time

#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

USE_GTTS = True
NEWS_API_KEY = "fa98e586a4124a738d69c61fcc422ed5"
OPENAI_API_KEY = "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"


engine = pyttsx3.init()
engine.setProperty("rate", 250)

if USE_GTTS:
    pygame.mixer.init()  

recognizer = sr.Recognizer()


music_library = {
    "song a": "https://youtu.be/cQM55aOrZCg?si=MSQ08tqQC4k6bnKv",
    "song b": "https://youtu.be/qxZGhxlmUak?si=GZ5GLeJbUyQFjcO_"
}

api_key = os.getenv(OPENAI_API_KEY)
client = OpenAI(api_key=api_key)



def speak(text):
   
    print(f"Nova: {text}")
    if USE_GTTS:
        filename = f"voice_{uuid.uuid4().hex}.mp3"
        tts = gTTS(text=text, lang="en")
        tts.save(filename)

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        try:
            os.remove(filename)
        except:
            pass
    else:
        engine.say(text)
        engine.runAndWait()


def listen(timeout=5, phrase_time_limit=5):
   
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            command = recognizer.recognize_google(audio) # type: ignore
            # print("recognising..") 
            print(f"You said: {command}")
            return command.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            speak("No Internet")
            return ""


def ai_process(command):
   
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Nova. Keep answers short and concise."},
            {"role": "user", "content": command}
        ]
    )
    return completion.choices[0].message.content


def fetch_news():
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])[:5]
        for article in articles:
            speak(article.get("title", "No title"))
    else:
        speak("Unable to fetch news right now.")


def process_command(command):
    if not command:
        return
    try:
        if "open google" in command:
            speak("Opening Google...")
            time.sleep(0.5)
            webbrowser.open("https://www.google.com")
        elif "open facebook" in command:
            speak("Opening Facebook...")
            time.sleep(0.5)
            webbrowser.open("https://www.facebook.com")
        elif "open youtube" in command:
            speak("Opening YouTube...")
            time.sleep(0.5)
            webbrowser.open("https://www.youtube.com")
        elif "open linkedin" in command:
            speak("Opening LinkedIn...")
            time.sleep(0.5)
            webbrowser.open("https://www.linkedin.com")
        elif command.startswith("play"):
            song_name = command.split("play")[-1].strip()
            link = music_library.get(song_name)
            if link:
                speak(f"Playing {song_name}")
                webbrowser.open(link)
            else:
                speak(f"Sorry, I do not have {song_name} in library.")
        elif "news" in command:
            speak("Here are the top headlines")
            fetch_news()
        elif "exit" in command or "quit" in command or "stop" in command:
            speak("Goodbye! Have a great day")
            exit()
        else:
        
            try:
                response = ai_process(command)
                speak(response)
            except RateLimitError:
                speak("Sorry, my API quota is exhausted. Try again later.")
            except APIError as e:
                speak("There was a problem communicating with the AI service.")
                print("API Error:", e)
            except Exception as e:
                speak("Sorry, I could not process that command.")
                print("Error in AI response:", e)

    except Exception as e:
            print("Unexpected error in process_command:", e)


if __name__ == "__main__":
    speak("Initializing Nova...")

    while True:
        
        word = listen(timeout=10, phrase_time_limit=3)
        word_lower = word.lower()
        if "nova" in word:
            speak("Hello Master....")
            speak("I am Nova  How may i assist you today...")

            while True:
                command = listen(timeout=7, phrase_time_limit=5)
                if not command:
                    continue  

                command_lower = command.lower()

                if "standby" in command_lower:
                    speak("Going to standby mode. Say 'Nova' to wake me up again.")
                    break  

                elif "exit" in command_lower or "quit" in command_lower or "stop" in command_lower:
                    speak("Shutting down. Goodbye!")
                    exit() 
                process_command(command)

