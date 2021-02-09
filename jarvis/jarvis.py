import datetime
import webbrowser as wb
import requests
import pytemperature
import wikipedia as wiki

from pymongo import DESCENDING, MongoClient


from personal_assistant import PersonalAssistant
from config import Config
from phrases import JarvisPhrases


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
        self.api_key_weather = Config.API_KEY_WEATHER.value
        self.commands.update({
            "browse": self.browse,
            "search": self.search,
            "stopper": self.stopper,
            "google": self.google,
            "weather": self.weather,
            "take": self.take_note,
            "note": self.read_note,
        })

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

    def google(self, source, params):
        """
        Jarvis will google sentence created using joined params.
        If params are empty Jarvis will aks to provide extra words.

        :param source: speech_recognition.Microphone
        object of speech_recognition.Microphone,  which represents a physical microphone on the computer
        :param params: part of commend after "hot" word
        :return: None
        """
        if not params:
            self.convert_text_to_speech("What do you want to google")
            audio = self.recognizer.listen(source, timeout=1)
            google_for = self.recognizer.recognize_google(audio)
            query = google_for.replace(" ", "+")
        else:
            query = "+".join(params)
        url = f"www.google.com/search?q={query}"

        wb.open(url)

    def search(self, source, params):
        """
        Jarvis will search in wikipedia sentence created using joined params.
        If params are empty Jarvis will aks to provide extra words.

        :param source: speech_recognition.Microphone
        object of speech_recognition.Microphone,  which represents a physical microphone on the computer
        :param params: part of commend after "hot" word
        :return: None
        """
        if not params:
            self.convert_text_to_speech(JarvisPhrases.WIKIPEDIA)
            audio = self.recognizer.listen(source)
            search_for = self.recognizer.recognize_google(audio)
            result = wiki.search(search_for)[0]
        else:
            result = wiki.search(" ".join(params))[0]
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

    def weather(self, source, params):
        """
        Jarvis will give you current weather in given city.
        If params are empty Jarvis will ask for name of city.

        :param source: speech_recognition.Microphone
        object of speech_recognition.Microphone,  which represents a physical microphone on the computer
        :param params: part of commend after "hot" word
        :return: None
        """
        if not params:
            self.convert_text_to_speech(JarvisPhrases.WEATHER)
            audio = self.recognizer.listen(source)
            city_name = self.recognizer.recognize_google(audio)
        else:
            city_name = params[0]
        base_url = "http://api.openweathermap.org/data/2.5/weather?"

        complete_url = f"{base_url}appid={self.api_key_weather}&q={city_name}"
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
