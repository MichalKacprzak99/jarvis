import datetime
import os
import webbrowser as wb
import requests

import pyjokes
import pyttsx3
import nltk
import numpy as np
import pytemperature
import wikipedia as wiki
import speech_recognition as sr
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from pymongo import MongoClient, DESCENDING

from utils import run_audio_file


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
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        self.stemmer = SnowballStemmer("english")
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

    def convert_text_to_speech(self, message):
        self.engine.say(message)
        self.engine.runAndWait()

    @staticmethod
    def welcome():
        hour = int(datetime.datetime.now().hour)
        greetings = {
            (0, 11): "Good Morning",
            (12, 17): "Good Afternoon",
            (18, 23): "Good Evening",
        }
        greeting = [value for (key, value) in greetings.items()
                    if hour in set(np.linspace(*key, dtype=int))]
        run_audio_file(*greeting)
        run_audio_file("How may I help you")

    def start(self):
        waiting_for_order = True
        self.welcome()
        with self.micro as source:
            while self.working:
                try:
                    audio = self.recognizer.listen(source, timeout=3)
                    order = self.recognizer.recognize_google(audio)
                    if "Jarvis" in order:
                        waiting_for_order = False
                        self.process_order(order, source)
                        waiting_for_order = True
                except sr.UnknownValueError:
                    if waiting_for_order is False:
                        run_audio_file("Sphinx could not understand audio can you repeat")
                except sr.RequestError:
                    run_audio_file("Sphinx error")
                except sr.WaitTimeoutError:
                    pass

    def browse(self, source):
        if not self.params:
            run_audio_file("What do you want to browse")
            audio = self.recognizer.listen(source)
            browse_for = self.recognizer.recognize_google(audio)
            url = f"www.{browse_for}.com"
        else:
            url = f"www.{self.params[0]}.com"

        wb.open(url)

    def stop(self, _):
        run_audio_file("GoodBye")
        self.working = False

    def joke(self, _):
        run_audio_file("I have a joke for u")
        joke = pyjokes.get_joke()
        self.convert_text_to_speech(joke)

    def google(self, source):

        if not self.params:
            run_audio_file("What do you want to google")
            audio = self.recognizer.listen(source, timeout=1)
            google_for = self.recognizer.recognize_google(audio)
            query = google_for.replace(" ", "+")
        else:
            query = "+".join(self.params)
        url = f"www.google.com/search?q={query}"

        wb.open(url)

    def search(self, source):

        if not self.params:
            run_audio_file("What do you want to search in wikipedia")
            audio = self.recognizer.listen(source)
            search_for = self.recognizer.recognize_google(audio)
            result = wiki.search(search_for)[0]
        else:
            result = wiki.search(" ".join(self.params))[0]
        page = wiki.page(result)
        url = page.url

        wb.open(url)

    def end(self):
        run_audio_file("See you again")
        self.working = False
        os.system("shutdown /s /t 1")

    def stopper(self, source):
        if not self.params:
            run_audio_file("How long")
            audio = self.recognizer.listen(source)
            text = self.recognizer.recognize_google(audio)
            num, time_unit = text.lower().split()
        else:
            [elem.lower() for elem in self.params]
            num, time_unit = self.params

        multipliers = {
            "seconds": 1,
            "minutes": 60,
            "hours": 3600,
        }
        multiplier = [value for (key, value) in multipliers.items()
                      if time_unit == key][0]

        duration = int(num) * multiplier

        run_audio_file("Ready Set Go")
        start = datetime.datetime.now()
        end = start + datetime.timedelta(0, duration)
        while datetime.datetime.now() < end:
            pass

        run_audio_file("Finish")

    @staticmethod
    def introduce_yourself():
        run_audio_file("I am Jarvis")

    def process_order(self, text, source):
        sentence_to_analyze = TextBlob(text.lower())
        polarity = sentence_to_analyze.sentiment.polarity
        if polarity < 0:
            run_audio_file("You seem sad")
            self.joke(source)

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
                self.commands[word](source)
                break

        if matched is False:
            run_audio_file("No match for commend")

    def weather(self, source):
        if not self.params:
            run_audio_file("Where do you want to check the weather")
            audio = self.recognizer.listen(source)
            city_name = self.recognizer.recognize_google(audio)
        else:
            city_name = self.params[0]
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = f"{base_url}appid={self.api_key_weather}&q={city_name}"
        response = requests.get(complete_url).json()
        if response["cod"] != "404":

            weather = response["main"]

            current_temperature = round(pytemperature.k2c(weather["temp"]), 2)

            current_pressure = weather["pressure"]

            current_humidity = weather["humidity"]

            weather_description = response["weather"][0]["description"]

            self.convert_text_to_speech(f"Temperature (in celsius unit) ={current_temperature} "
                                        f"atmospheric pressure (in hPa unit) = {current_pressure} "
                                        f" humidity (in percentage) = {current_humidity} "
                                        f"description = {weather_description}")

        else:
            run_audio_file("City Not Found")

    def take_note(self, source):
        run_audio_file("What note")

        audio = self.recognizer.listen(source)
        text = self.recognizer.recognize_google(audio)
        note = {
            "date": datetime.datetime.now().strftime("%c"),
            "Author": "Michał",
            "text": text
        }
        self.notes.insert_one(note)

    def read_note(self):
        try:
            last_note = self.notes.find().sort("date", DESCENDING)[0]
            self.convert_text_to_speech(last_note["text"])
        except IndexError:
            run_audio_file("There are no notes saved")
