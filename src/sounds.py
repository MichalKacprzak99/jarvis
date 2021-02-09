from enum import Enum, unique


@unique
class Sounds(Enum):
    GOOD_MORNING = "Good Morning"
    GOOD_AFTERNOON = "Good Afternoon"
    GOOD_EVENING = "Good Evening"
    INCOMPREHENSIBLE_SOUND = "Sphinx could not understand audio can you repeat"
    ERROR = "Sphinx error"
    GOODBYE = "GoodBye"
    JOKE = "I have a joke for u"
    END = "See you again"
    START = "Ready Set Go"
    FINISH = "Finish"
    INTRODUCE = "I am Jarvis"
    SAD = "You seem sad"
    NO_COMMEND = "No match for commend"
    NO_NOTES = "There are no notes saved"
    NO_CITY = "City Not Found"
    BROWSE = "What do you want to browse"
    GOOGLE = "What do you want to google"
    WIKIPEDIA = "What do you want to search in wikipedia",
    WEATHER = "Where do you want to check the weather"
    HELP = "How may I help you"
    CREATE_NOTE = "What note"
    HOW_LONG = "How long"

    def __str__(self):
        return str(self.value)
