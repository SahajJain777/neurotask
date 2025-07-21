import random
import os
import webbrowser
import requests
from bs4 import BeautifulSoup
import speech_recognition as sr
import pyttsx3
from datetime import datetime

class VoiceAssistant:
    def __init__(self, root, status_callback=None, chat_callback=None):
        self.root = root
        self.chatStr = ""
        self.engine = pyttsx3.init()
        self.r = sr.Recognizer()
        self.is_listening = False
        self.status_callback = status_callback
        self.chat_callback = chat_callback
        
        # Adjust for ambient noise
        try:
            with sr.Microphone() as source:
                self.r.adjust_for_ambient_noise(source, duration=1)
        except Exception as e:
            print(f"Warning: Could not adjust for ambient noise: {e}")
            if self.status_callback:
                self.status_callback("error", f"Microphone Error: {str(e)}. Please check your microphone permissions and connections.")
            if self.chat_callback:
                self.chat_callback("NeuroTask: I couldn't access your microphone. Please check if it's properly connected and permissions are granted.")

    def say(self, text):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
            if self.chat_callback:
                self.chat_callback(f"NeuroTask: {text}")
        except Exception as e:
            print(f"Error in text-to-speech: {e}")
            if self.status_callback:
                self.status_callback("error", "Text-to-speech error")

    def takeCommand(self):
        try:
            with sr.Microphone() as source:
                if self.status_callback:
                    self.status_callback("listening", "Listening...")
                try:
                    audio = self.r.listen(source, timeout=5)
                    try:
                        query = self.r.recognize_google(audio, language='en-in')
                        if self.status_callback:
                            self.status_callback("ready", f"Heard: {query[:20]}...")
                        if self.chat_callback:
                            self.chat_callback(f"You: {query}")
                        return query.lower()
                    except sr.UnknownValueError:
                        if self.status_callback:
                            self.status_callback("ready", "No speech detected after 5 seconds")
                        self.say("No speech detected after 5 seconds.")
                        self.is_listening = False
                        return None
                    except sr.RequestError as e:
                        if self.status_callback:
                            self.status_callback("error", f"Could not request results from Google Speech Recognition service; {e}")
                        self.say("Sorry, I encountered an error with speech recognition.")
                        self.is_listening = False
                        return None
                except sr.WaitTimeoutError:
                    if self.status_callback:
                        self.status_callback("ready", "Listening timed out (no speech)")
                    self.say("Listening timed out. Please try again.")
                    self.is_listening = False
                    return None
        except Exception as e:
            print(f"Microphone error: {e}")
            if self.status_callback:
                self.status_callback("error", f"Microphone error: {str(e)}")
            self.say("There was a problem accessing the microphone. Please check your microphone permissions and try again.")
            self.is_listening = False
            return None

    def toggle_listening(self):
        if self.is_listening:
            self.is_listening = False
            if self.status_callback:
                self.status_callback("ready", "Ready")
        else:
            # Check microphone availability before starting
            try:
                with sr.Microphone() as source:
                    self.r.adjust_for_ambient_noise(source, duration=0.5)
                self.is_listening = True
                if self.status_callback:
                    self.status_callback("listening", "Listening...")
                self.root.after(100, self.listen_once)
            except Exception as e:
                print(f"Microphone initialization error: {e}")
                if self.status_callback:
                    self.status_callback("error", "Could not access microphone")
                self.say("Could not access microphone. Please check your microphone permissions.")
                self.is_listening = False

    def listen_once(self):
        if not self.is_listening:
            return

        query = self.takeCommand()
        if query:
            self.process_command(query)

        self.is_listening = False
        if self.status_callback:
            self.status_callback("ready", "Ready")

    def process_command(self, query):
        if "quit" in query or "exit" in query:
            self.say("Goodbye! Assistant is signing off!")
            self.is_listening = False
            if self.status_callback:
                self.status_callback("ready", "Offline")
        elif "reset chat" in query:
            self.chatStr = ""
            self.say("Chat history has been reset!")
            if self.chat_callback:
                # Optionally clear the chat UI via the callback
                self.chat_callback("Chat history has been reset!", reset=True)
        elif "open" in query or "search" in query or "play music" in query or "date" in query or "time" in query:
            self.handle_web_commands(query)
        elif "news" in query:
            news = self.get_news()
            self.say("Here are some news headlines...")
            for headline in news[:3]:
                self.say(headline)
        elif "weather" in query:
            weather = self.get_weather()
            self.say(weather)
        else:
            self.say("Sorry, I did not understand that command.")

    def handle_web_commands(self, query):
        sites = [["youtube", "https://youtube.com"],
                 ["wikipedia", "https://wikipedia.com"],
                 ["google", "https://google.com"],
                 ["top bhopal", "https://vtop.vitbhopal.ac.in/vtop"],
                 ["instagram", "https://instagram.com"],
                 ["linkedin", "https://linkedin.com"],
                 ["chatgpt", "https://chat.openai.com"]]

        for site in sites:
            if f"open {site[0]}".lower() in query.lower():
                self.say(f"Opening {site[0]}...")
                webbrowser.open(site[1])
            elif f"search {site[0]}".lower() in query.lower():
                self.say(f"Searching {site[0]}...")
                webbrowser.open(f"{site[1]}/search?q={query.split(f'search {site[0]}', 1)[1].strip()}")

        if "play music" in query.lower():
            self.say("Playing music on Spotify...")
            webbrowser.open("https://open.spotify.com")
        elif "search music" in query.lower():
            search_term = query.split("search music", 1)[1].strip()
            self.say(f"Searching for {search_term} on Spotify...")
            webbrowser.open(f"https://open.spotify.com/search/{search_term}")
        elif "date" in query.lower():
            current_date = datetime.now().strftime("%B %d, %Y")
            self.say(f"Today's date is {current_date}.")
        elif "time" in query.lower():
            current_time = datetime.now().strftime("%H:%M:%S")
            self.say(f"The current time is {current_time}.")
        elif "search google" in query.lower():
            search_term = query.split("search google", 1)[1].strip()
            self.say(f"Searching for {search_term} on Google...")
            webbrowser.open(f"https://www.google.com/search?q={search_term}")
        elif "open chatgpt" in query.lower():
            self.say("Opening ChatGPT...")
            webbrowser.open("https://chat.openai.com")

    def get_news(self):
        news_sources = ["https://timesofindia.indiatimes.com/news", "https://indianexpress.com/latest-news"]
        news = []
        for source in news_sources:
            try:
                response = requests.get(source)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                headlines = soup.find_all('h3', class_='title')
                for headline in headlines[:5]:
                    news.append(headline.text.strip())
            except requests.exceptions.RequestException as e:
                print(f"Error fetching news from {source}: {e}")
        return news

    def get_weather(self):
        try:
            response = requests.get("https://a.msn.com/54/EN-IN/ct23.0151,76.7248?ocid=ansmsnweather")
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            current_temp_span = soup.find('span', class_='current-temp')
            forecast_div = soup.find('div', class_='forecast')
            if current_temp_span and forecast_div:
                current_temp = current_temp_span.text
                forecast = forecast_div.text
                return f"Current temperature: {current_temp}\nForecast: {forecast}"
            else:
                return "Could not retrieve weather information."
        except requests.exceptions.RequestException as e:
            return f"Error fetching weather information: {e}"

# Keep the original functions for backward compatibility (though they won't integrate with the UI as intended now)
def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(query)
            return query.lower()
        except Exception as e:
            print(f"Error: {str(e)}")
            return "some error occurred, sorry from NeuroTask"

def get_news():
    news_sources = ["https://timesofindia.indiatimes.com/news", "https://indianexpress.com/latest-news"]
    news = []
    for source in news_sources:
        response = requests.get(source)
        soup = BeautifulSoup(response.content, 'html.parser')
        headlines = soup.find_all('h3', class_='title')
        for headline in headlines:
            news.append(headline.text.strip())
    return news

def get_weather():
    response = requests.get("https://a.msn.com/54/EN-IN/ct23.0151,76.7248?ocid=ansmsnweather")
    soup = BeautifulSoup(response.content, 'html.parser')
    current_temp = soup.find('span', class_='current-temp').text
    forecast = soup.find('div', class_='forecast').text
    return f"Current temperature: {current_temp}\nForecast: {forecast}"

if __name__ == '__main__':
    print("This file is designed to be integrated into a larger UI application.")
    print("The standalone execution with the 'while True' loop is no longer the primary way to use it.")
    print("Please use the VoiceAssistant class within your UI's event handling for the button.")