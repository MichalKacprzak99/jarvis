import datetime
import requests
import pytemperature
import webbrowser as wb
import wikipedia as wiki


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
            "stopper": self.stopper,
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
        if not params:
            self.convert_text_to_speech(JarvisPhrases.HOW_LONG)
            audio = self.recognizer.listen(source)
            text = self.recognizer.recognize_google(audio)
            num, time_unit = text.lower().split()
        else:
            [elem.lower() for elem in params]
            num, time_unit = params

        multipliers = {
            "seconds": 1,
            "minutes": 60,
            "hours": 3600,
        }
        multiplier = [value for (key, value) in multipliers.items()
                      if time_unit == key][0]

        duration = int(num) * multiplier

        self.convert_text_to_speech(JarvisPhrases.START)
        start = datetime.datetime.now()
        end = start + datetime.timedelta(0, duration)
        while datetime.datetime.now() < end:
            pass

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

        extractor = extraction.Extractor(text=" ".join(location_params))

        while True:
            extractor.find_entities()
            if len(extractor.places) > 0:
                city = extractor.places[0]
                get_weather(city)
                break
            else:
                self.convert_text_to_speech(JarvisPhrases.WEATHER)
                audio = self.recognizer.listen(source)
                location = self.recognizer.recognize_google(audio)
                extractor.text = location


    def organize_notes(self, source):
        pass

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

    def read_note(self, _):
        """
        Jarvis will read last taken note. If no notes was taken user will be informed.

        :return: None
        """
        try:
            last_note = self.notes.find().sort("date", DESCENDING)[0]
            self.convert_text_to_speech(last_note["text"])
        except IndexError:
            self.convert_text_to_speech(JarvisPhrases.NO_NOTES)
