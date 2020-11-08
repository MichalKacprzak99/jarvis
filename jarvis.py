import datetime
import pyttsx3
import speech_recognition as sr
import webbrowser as wb
import pyjokes
import wikipedia as wiki
import os
from textblob import TextBlob


class Jarvis:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.working = True
        self.micro = sr.Microphone()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 125)
        self.commend = ""
        self.params = None
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        self.commends = {
            "browse": self.browse,
            "stop": self.stop,
            "joke": self.joke,
            "search": self.search,
            "end": self.end,
            "stopper": self.stopper,
            "google": self.google,
        }

    def speak(self, message):
        self.engine.say(message)
        self.engine.runAndWait()

    def wishMe(self):
        hour = int(datetime.datetime.now().hour)
        if 0 <= hour < 12:
            self.speak("Good Morning!")
        elif 12 <= hour < 18:
            self.speak("Good Afternoon!")
        else:
            self.speak("Good Evening!")
        self.speak("Please tell me how may I help you")

    def start(self):
        self.wishMe()
        with self.micro as source:
            print("ala")
            while self.working:
                print("basia")
                audio = self.recognizer.listen(source)
                print("kasia")
                try:
                    print(self.recognizer.recognize_google(audio))
                    self.process(self.recognizer.recognize_google(audio))
                    order, *self.params = self.recognizer.recognize_google(audio).lower().split()
                    self.commends[order]()
                except KeyError:
                    self.speak("No match for commend")
                except sr.UnknownValueError:
                    print("Sphinx could not understand audio")
                except sr.RequestError as e:
                    print("Sphinx error; {0}".format(e))

                self.speak("what's next")

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
        os.system("shutdown /s /t 1")

    def stopper(self):
        self.speak("Ready, Set, Go")
        print(self.params)
        try:
            duration = int(self.params[0])
        except ValueError:
            duration = 60

        start = datetime.datetime.now()
        end = start + datetime.timedelta(0, duration)
        while datetime.datetime.now() < end:
            pass
        self.speak("Finish")

    def process(self, text):
        sentence_to_analize = TextBlob(text)
        polarity = sentence_to_analize.sentiment.polarity
        if polarity < 0:
            self.speak("You seem sad")
            self.joke()
