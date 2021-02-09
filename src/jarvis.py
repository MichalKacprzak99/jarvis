import datetime
import webbrowser as wb
import requests
import pytemperature
import wikipedia as wiki

from pymongo import DESCENDING, MongoClient

from sounds import Sounds
from personal_assistant import PersonalAssistant
from config import Config


class Jarvis(PersonalAssistant):
    def __init__(self):
        super().__init__("Jarvis")
        self.mongo_client = MongoClient()
        self.database = self.mongo_client.database
        self.notes = self.database.notes
        self.api_key_weather = Config.API_KEY_WEATHER
        self.commands.update({
            "browse": self.browse,
            "search": self.search,
            "stopper": self.stopper,
            "google": self.google,
            "weather": self.weather,
            "take": self.take_note,
            "note": self.read_note,
        })

    def browse(self, source):
        if not self.params:
            self.convert_text_to_speech(Sounds.BROWSE)
            audio = self.recognizer.listen(source)
            browse_for = self.recognizer.recognize_google(audio)
            url = f"www.{browse_for}.com"
        else:
            url = f"www.{self.params[0]}.com"

        wb.open(url)

    def google(self, source):

        if not self.params:
            self.convert_text_to_speech("What do you want to google")
            audio = self.recognizer.listen(source, timeout=1)
            google_for = self.recognizer.recognize_google(audio)
            query = google_for.replace(" ", "+")
        else:
            query = "+".join(self.params)
        url = f"www.google.com/search?q={query}"

        wb.open(url)

    def search(self, source):

        if not self.params:
            self.convert_text_to_speech(Sounds.WIKIPEDIA)
            audio = self.recognizer.listen(source)
            search_for = self.recognizer.recognize_google(audio)
            result = wiki.search(search_for)[0]
        else:
            result = wiki.search(" ".join(self.params))[0]
        page = wiki.page(result)
        url = page.url

        wb.open(url)

    def stopper(self, source):
        if not self.params:
            self.convert_text_to_speech(Sounds.HOW_LONG)
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

        self.convert_text_to_speech(Sounds.START)
        start = datetime.datetime.now()
        end = start + datetime.timedelta(0, duration)
        while datetime.datetime.now() < end:
            pass

        self.convert_text_to_speech(Sounds.FINISH)

    def weather(self, source):
        if not self.params:
            self.convert_text_to_speech(Sounds.WEATHER)
            audio = self.recognizer.listen(source)
            city_name = self.recognizer.recognize_google(audio)
        else:
            city_name = self.params[0]
        print(city_name)
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = f"{base_url}appid={self.api_key_weather}&q={city_name}"
        response = requests.get(complete_url).json()
        if response["cod"] != "404":

            weather = response["main"]

            current_temperature = round(pytemperature.k2c(weather["temp"]), 2)
            print(current_temperature)
            current_pressure = weather["pressure"]

            current_humidity = weather["humidity"]

            weather_description = response["weather"][0]["description"]
            current_temperature = f'{"minus" if current_temperature<0 else ""}' + current_temperature
            self.convert_text_to_speech(f'Temperature (in celsius unit) = {current_temperature} '
                                        f'atmospheric pressure (in hPa unit) = {current_pressure} '
                                        f' humidity (in percentage) = {current_humidity} '
                                        f'description = {weather_description}')
        else:
            self.convert_text_to_speech(Sounds.NO_CITY)

    def take_note(self, source):
        self.convert_text_to_speech(Sounds.CREATE_NOTE)

        audio = self.recognizer.listen(source)
        text = self.recognizer.recognize_google(audio)
        note = {
            "date": datetime.datetime.now().strftime("%c"),
            "Author": "Michał",
            "text": text
        }
        self.notes.insert_one(note)

    def read_note(self, _):
        try:
            last_note = self.notes.find().sort("date", DESCENDING)[0]
            self.convert_text_to_speech(last_note["text"])
        except IndexError:
            self.convert_text_to_speech(Sounds.NO_NOTES)
