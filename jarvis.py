import datetime
import os
import webbrowser as wb
import requests

import numpy as np
import pyjokes
import pytemperature
import wikipedia as wiki
import pyttsx3
import speech_recognition as sr
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from pymongo import MongoClient, DESCENDING


class Jarvis:
    def __init__(self):
        self.api_key_weather = "2bd8dbd4b1f673a2ea92a2a9b30a85be"
        self.mongo_client = MongoClient()
        self.database = self.mongo_client.database
        self.notes = self.database.notes
        self.recognizer = sr.Recognizer()
        self.micro = sr.Microphone()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 125)
        self.order = ""
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        self.stemmer = SnowballStemmer("english")
        self.command = ""
        self.params = []
        self.working = True
        self.commands = {
            "browse": self.browse,
            "stop": self.stop,
            "joke": self.joke,
            "search": self.search,
            "end": self.end,
            "stopper": self.stopper,
            "google": self.google,
            "introduce": self.introduce_yourself,
            "weather": self.weather,
            "take": self.take_note,
            "note": self.read_note,
        }

    def speak(self, message):
        self.engine.say(message)
        self.engine.runAndWait()

    def welcome(self):
        hour = int(datetime.datetime.now().hour)
        greetings = {
            (0, 11): "Good Morning!",
            (12, 17): "Good Afternoon!",
            (18, 23): "Good Evening!",
        }
        greeting = [value for (key, value) in greetings.items()
                    if hour in set(np.linspace(*key, dtype=int))]
        self.speak(*greeting)
        self.speak("How may I help you?")

    def start(self):
        self.welcome()
        with self.micro as source:
            print("ala")
            while self.working:
                try:
                    audio = self.recognizer.listen(source)
                    print("kasia")
                    self.process_order(self.recognizer.recognize_google(audio))

                except sr.UnknownValueError:
                    self.speak("Sphinx could not understand audio, can you repeat?")
                except sr.RequestError as e:
                    self.speak("Sphinx error; {0}".format(e))

    def browse(self):
        try:
            url = f"www.{self.params[0]}.com"
        except IndexError:
            url = "www.google.com"
        wb.open(url)

    def stop(self):
        self.speak("GoodBye")
        self.working = False

    def joke(self):
        self.speak("I have a joke for u")
        joke = pyjokes.get_joke()
        print(joke)
        self.engine.say(joke)
        self.engine.runAndWait()

    def google(self):
        try:
            query = "+".join(self.params)
            url = f"www.google.com/search?q={query}"
        except IndexError:
            url = "www.google.com"
        wb.open(url)

    def search(self):
        try:
            result = wiki.search(" ".join(self.params))[0]
            page = wiki.page(result)
            url = page.url
        except IndexError:
            url = "www.google.com"
        wb.open(url)

    def end(self):
        self.speak("See you again")
        self.working = False
        os.system("shutdown /s /t 1")

    def stopper(self):
        self.speak("Ready, Set, Go")
        try:
            duration = int(self.params[0])
        except ValueError:
            duration = 60
        start = datetime.datetime.now()
        end = start + datetime.timedelta(0, duration)
        while datetime.datetime.now() < end:
            pass
        self.speak("Finish")

    def introduce_yourself(self):
        self.speak("I am Jarvis")

    def process_order(self, text):
        sentence_to_analyze = TextBlob(text.lower())
        polarity = sentence_to_analyze.sentiment.polarity
        if polarity < 0:
            self.speak("You seem sad")
            self.joke()

        tokenized_text = sentence_to_analyze.tokenize()
        filtered_words = [word for word in tokenized_text
                          if word not in stopwords.words('english')]
        tagged = nltk.pos_tag(filtered_words)
        words = [self.stemmer.stem(word) if tag in ('VB', 'VBG') else word
                 for (word, tag) in tagged]
        matched = False
        for word in words:
            if word in self.commands.keys():
                matched = True
                ind = words.index(word)
                self.params = words[ind + 1:]
                self.commands[word]()
                break

        if matched is False:
            self.speak("No match for commend")

    def weather(self):
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        city_name = self.params[0]
        complete_url = f"{base_url}appid={self.api_key_weather}&q={city_name}"
        response = requests.get(complete_url).json()
        if response["cod"] != "404":

            weather = response["main"]

            current_temperature = round(pytemperature.k2c(weather["temp"]), 2)

            current_pressure = weather["pressure"]

            current_humidity = weather["humidity"]

            weather_description = response["weather"][0]["description"]

            self.speak(f"Temperature (in celsius unit) ={current_temperature} "
                       f"atmospheric pressure (in hPa unit) = {current_pressure} "
                       f" humidity (in percentage) = {current_humidity} "
                       f"description = {weather_description}")

        else:
            self.speak(" City Not Found ")

    def take_note(self):
        self.speak("What note")
        try:
            audio = self.recognizer.listen(self.micro)
            text = self.recognizer.recognize_google(audio)
            note = {
                "date": datetime.datetime.now().strftime("%c"),
                "Author": "Michał",
                "text": text
            }
            self.notes.insert_one(note)

        except sr.UnknownValueError:
            self.speak("Sphinx could not understand audio, can you repeat?")
            self.take_note()
        except sr.RequestError as e:
            self.speak("Sphinx error; {0}".format(e))

    def read_note(self):
        last_note = self.notes.find().sort("date", DESCENDING)[0]
        self.speak(last_note["text"])
