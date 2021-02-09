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
from .phrases import BasicPhrases


class PersonalAssistant:
    """
    A class to represent voice personal assistant with basic features.

    ...

    Attributes
    ----------
    recognizer: speech_recognition.Recognizer
        object of speech_recognition.Recognizer,  which represents a collection of speech recognition functionality
    micro: speech_recognition.Microphone
        object of speech_recognition.Microphone,  which represents a physical microphone on the computer
    engine:
        text to speech engine
    stemmer: nltk.stem.snowball.SnowballStemmer
        object of SnowballStemmer used in text analyze
    working: bool
        variable, which represent if personal assistant is working
    name: str
        name of the personal assistant
    commands: dict
        dictionary where are stored all implemented features
    """
    def __init__(self, name: str):
        """
        Creates a new ``PersonalAssistant`` instance, which represents voice personal assistant with basic features.

        Parameters
        ----------
            name : str
                name of the personal assistant
        """
        self.recognizer = sr.Recognizer()
        self.micro = sr.Microphone()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 125)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        self.stemmer = SnowballStemmer("english")
        self.working = True
        self.name = name
        self.commands = {
            "introduce": self.introduce_yourself,
            "stop": self.stop,
            "joke": self.joke,
            "end": self.end,
        }

    def convert_text_to_speech(self, message):
        """
        String representation of parameter "message" will be converted to speech using self.engine

        :param message: str
        :return: None
        """
        self.engine.say(message)
        self.engine.runAndWait()

    def welcome(self):
        """
        Personal assistant will greet you with the appropriate greeting depending on the current time

        :return: None
        """
        hour = int(datetime.datetime.now().hour)
        greetings = {
            (0, 11): BasicPhrases.GOOD_MORNING,
            (12, 17): BasicPhrases.GOOD_AFTERNOON,
            (18, 23): BasicPhrases.GOOD_EVENING,
        }
        greeting = [value for (key, value) in greetings.items()
                    if hour in set(np.linspace(*key, dtype=int))]
        self.convert_text_to_speech(*greeting)
        self.convert_text_to_speech(BasicPhrases.HELP)

    def start(self):
        """
        Main function responsible for convert voice command to text.
        If in command there is no word equals to self.name the command is no longer process.

        :return: None
        """
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
                        self.convert_text_to_speech(BasicPhrases.INCOMPREHENSIBLE_SOUND)
                except sr.RequestError:
                    self.convert_text_to_speech(BasicPhrases.ERROR)
                except sr.WaitTimeoutError:
                    pass

    def introduce_yourself(self, _):
        """
        Personal assistant introduce yourself using self.name

        :return: None
        """
        self.convert_text_to_speech(f"I am {self.name}")

    def process_order(self, text: str, source: sr.Microphone):
        """
        Converted voice command is processed using nltk,TextBlob.
        Command sentence is tokenized and filtered in purpose to catch "hot" words and decide
        if sentence is connected with any implemented feature.

        :param text: str
            Voice command converted to text
        :param source: speech_recognition.Microphone
            object of speech_recognition.Microphone,  which represents a physical microphone on the computer
        :return: None
        """
        sentence_to_analyze = TextBlob(text.lower())
        polarity = sentence_to_analyze.sentiment.polarity
        if polarity < 0:
            self.convert_text_to_speech(BasicPhrases.SAD)
            self.joke(source)

        tokenized_text = sentence_to_analyze.tokenize()
        filtered_words = [word for word in tokenized_text
                          if word not in stopwords.words('english')]
        tagged = nltk.pos_tag(filtered_words)
        words = [self.stemmer.stem(word) if tag in ('VB', 'VBG') else word
                 for (word, tag) in tagged]

        for index, word in enumerate(words):
            if word in self.commands.keys():
                params = words[index + 1:]
                self.commands[word](source, params)
                break
        else:
            self.convert_text_to_speech(BasicPhrases.NO_COMMEND)

    def stop(self, _):
        """
        The personal assistant stops the program

        :return: None
        """
        self.convert_text_to_speech(BasicPhrases.GOODBYE)
        self.working = False

    def end(self, _):
        """
        The personal assistant stops the program and shuts down the computer

        :return: None
        """
        self.convert_text_to_speech(BasicPhrases.END)
        self.working = False
        os.system("shutdown /s /t 1")

    def joke(self, _):
        """
        Personal assistant will tell random joke(from pyjokes library)

        :return: None
        """
        self.convert_text_to_speech(BasicPhrases.JOKE)
        joke = pyjokes.get_joke()
        self.convert_text_to_speech(joke)
