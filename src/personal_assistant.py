import datetime
import os
import pyjokes
import pyttsx3
import nltk
import numpy as np
import speech_recognition as sr

from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from pymongo import MongoClient

from sounds import Sounds
from config import Config


class PersonalAssistant:
    def __init__(self, name):

        self.api_key_weather = Config.API_KEY_WEATHER
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
        self.name = name
        self.commands = {
            "introduce": self.introduce_yourself,
            "stop": self.stop,
            "joke": self.joke,
            "end": self.end,
        }

    def convert_text_to_speech(self, message: str):
        self.engine.say(message)
        self.engine.runAndWait()

    def welcome(self):
        hour = int(datetime.datetime.now().hour)
        greetings = {
            (0, 11): Sounds.GOOD_MORNING,
            (12, 17): Sounds.GOOD_AFTERNOON,
            (18, 23): Sounds.GOOD_EVENING,
        }
        greeting = [value for (key, value) in greetings.items()
                    if hour in set(np.linspace(*key, dtype=int))]
        self.convert_text_to_speech(*greeting)
        self.convert_text_to_speech(Sounds.HELP)

    def start(self):
        waiting_for_order = True
        self.welcome()
        with self.micro as source:
            while self.working:
                try:
                    audio = self.recognizer.listen(source, timeout=3)
                    order = self.recognizer.recognize_google(audio)
                    if self.name in order:
                        waiting_for_order = False
                        self.process_order(order, source)
                        waiting_for_order = True
                except sr.UnknownValueError:
                    if waiting_for_order is False:
                        self.convert_text_to_speech(Sounds.INCOMPREHENSIBLE_SOUND)
                except sr.RequestError:
                    self.convert_text_to_speech(Sounds.ERROR)
                except sr.WaitTimeoutError:
                    pass

    def introduce_yourself(self, _):
        self.convert_text_to_speech(f"I am {self.name}")

    def process_order(self, text, source):
        sentence_to_analyze = TextBlob(text.lower())
        polarity = sentence_to_analyze.sentiment.polarity
        if polarity < 0:
            self.convert_text_to_speech(Sounds.SAD)
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
            self.convert_text_to_speech(Sounds.NO_COMMEND)

    def stop(self, _):
        self.convert_text_to_speech(Sounds.GOODBYE)
        self.working = False

    def end(self, _):
        self.convert_text_to_speech(Sounds.END)
        self.working = False
        os.system("shutdown /s /t 1")

    def joke(self, _):
        self.convert_text_to_speech(Sounds.JOKE)
        joke = pyjokes.get_joke()
        self.convert_text_to_speech(joke)
