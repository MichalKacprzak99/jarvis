import datetime
import time

import requests
import pytemperature
import webbrowser as wb
import wikipedia as wiki
import parsedatetime


from geograpy import extraction
from pymongo import DESCENDING, MongoClient


from .personal_assistant import PersonalAssistant
from .config import Config
from .phrases import JarvisPhrases


class Jarvis(PersonalAssistant):
    """
    A class to represent Jarvis an extended version of voice personal assistant.
    Subclass of ``PersonalAssistant``

    ...

    Attributes
    ----------
    mongo_client: pymongo.mongo_client.MongoClient
        Client for a MongoDB instance
    jarvis_database: pymongo.database.Database
        independent MongoDB database created for jarvis
    notes: pymongo.collection.Collection
        independent collection created inside jarvis_database for storing notes
    api_key_weather: str
        key to using weather api from "https://openweathermap.org/api"
    """

    def __init__(self):
        """
        Creates a new ``Jarvis`` instance.
        """
        super().__init__("Jarvis")
        self.mongo_client = MongoClient()
        self.jarvis_database = self.mongo_client.jarvis_database
        self.notes = self.jarvis_database.notes
        self.api_key_weather = Config.API_KEY_WEATHER
        self.commands.update({
            "browse": self.browse,
            "wikipedia": self.search_in_wikipedia,
            "timer": self.stopper,
            "google": self.search_in_google,
            "weather": self.weather,
            "note": self.organize_notes,
        })

    # this feature is not available due to not being included in trained classifier
    def browse(self, source, params):
        """
        Jarvis will open url, created by using first item(word) in params.
        If params are empty Jarvis will aks to provide extra word.

        :param source: speech_recognition.Microphone
        object of speech_recognition.Microphone,  which represents a physical microphone on the computer
        :param params: part of commend after "hot" word
        :return: None
        """
        if not params:
            self.convert_text_to_speech(JarvisPhrases.BROWSE)
            audio = self.recognizer.listen(source)
            browse_for = self.recognizer.recognize_google(audio)
            url = f"www.{browse_for}.com"
        else:
            url = f"www.{params[0]}.com"

        wb.open(url)

    def search_in_google(self, params):
        """
        Jarvis will google sentence created using joined params.
        If params are empty Jarvis will aks to provide extra words.

        object of speech_recognition.Microphone,  which represents a physical microphone on the computer
        :param params: part of commend after "hot" word
        :return: None
        """
        query = "+".join(params)
        url = f"www.google.com/search?q={query}"
        wb.open(url)

    def search_in_wikipedia(self, searching):
        """
        Jarvis will search in wikipedia sentence created using joined params.
        If searching is empty Jarvis will aks to provide extra words.

        :param searching: part of commend after "hot" word
        :return: None
        """
        result = wiki.search(" ".join(searching))[0]
        page = wiki.page(result)
        url = page.url

        wb.open(url)

    def stopper(self, source, params):
        """
        Jarvis will set a stopper. Time will be calculated depending by params.
        User needs to provide value and unit e.g. 50 seconds.
        If params are empty Jarvis will ask for time.

        :param source: speech_recognition.Microphone
        object of speech_recognition.Microphone,  which represents a physical microphone on the computer
        :param params: part of commend after "hot" word
        :return: None
        """

        cal = parsedatetime.Calendar()
        time_chunks = cal.nlp(" ".join(params))

        while True:
            if len(time_chunks) > 0:
                duration = sum((time_chunk[0] - datetime.datetime.now()).total_seconds() for time_chunk in time_chunks)
                end = datetime.datetime.now() + datetime.timedelta(seconds=duration)
                break
            else:
                self.convert_text_to_speech(JarvisPhrases.TIME)
                audio = self.recognizer.listen(source)
                additional_command = self.recognizer.recognize_google(audio)
                time_chunks = cal.nlp(additional_command)

        while datetime.datetime.now() < end:
            time.sleep(1)
        self.convert_text_to_speech(JarvisPhrases.FINISH)

    def weather(self, source, location_params):
        """
        Jarvis will give you current weather in given city.
        If params are empty Jarvis will ask for name of city.

        :param source: speech_recognition.Microphone
        object of speech_recognition.Microphone,  which represents a physical microphone on the computer
        :param location_params: part of commend after "hot" word
        :return: None
        """

        base_url = "http://api.openweathermap.org/data/2.5/weather?"

        def get_weather(city):
            complete_url = f"{base_url}appid={self.api_key_weather}&q={city}"
            response = requests.get(complete_url).json()
            if response["cod"] != "404":
                weather = response["main"]

                current_temperature = round(pytemperature.k2c(weather["temp"]), 2)
                current_temperature = f'{"minus" if current_temperature < 0 else ""}' + str(current_temperature)
                current_pressure = weather["pressure"]

                current_humidity = weather["humidity"]

                weather_description = response["weather"][0]["description"]

                self.convert_text_to_speech(f'Temperature (in celsius unit) = {current_temperature} '
                                            f'atmospheric pressure (in hPa unit) = {current_pressure} '
                                            f' humidity (in percentage) = {current_humidity} '
                                            f'description = {weather_description}')
            else:
                self.convert_text_to_speech(JarvisPhrases.NO_CITY)

        city_extractor = extraction.Extractor(text=" ".join(location_params))

        while True:
            city_extractor.find_entities()
            if len(city_extractor.places) > 0:
                city = city_extractor.places[0]
                get_weather(city)
                break
            else:
                self.convert_text_to_speech(JarvisPhrases.WEATHER)
                audio = self.recognizer.listen(source)
                location = self.recognizer.recognize_google(audio)
                city_extractor.text = location


    def organize_notes(self, source, order):

        self.convert_text_to_speech(f"Sir, you wanna take a note or get your last note?"
                                    f"Choose option 1 or 2")
        audio = self.recognizer.listen(source, timeout=3)
        try:
            answer = int(self.recognizer.recognize_google(audio).lower())
            if answer == 1:
                self.take_note(source)
            else:
                self.read_note()
        except ValueError:
            self.convert_text_to_speech(f"Sir, you just made mistake during choosing option")

    def take_note(self, source):
        """
        Jarvis will ask for text of note and save it to local database.

        :param source: speech_recognition.Microphone
        object of speech_recognition.Microphone,  which represents a physical microphone on the computer
        :return: None
        """
        self.convert_text_to_speech(JarvisPhrases.CREATE_NOTE)

        audio = self.recognizer.listen(source)
        text = self.recognizer.recognize_google(audio)
        note = {
            "date": datetime.datetime.now().strftime("%c"),
            "text": text
        }
        self.notes.insert_one(note)
        self.convert_text_to_speech(JarvisPhrases.INSERTED_NOTE)

    def read_note(self, *_):
        """
        Jarvis will read last taken note. If no notes was taken user will be informed.

        :return: None
        """
        try:
            last_note = self.notes.find().sort("date", DESCENDING)[0]
            self.convert_text_to_speech(last_note["text"])
        except IndexError:
            self.convert_text_to_speech(JarvisPhrases.NO_NOTES)
