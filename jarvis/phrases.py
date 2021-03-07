from enum import Enum, unique


@unique
class BasicPhrases(Enum):
    """
    Enum used for storing hard coded phrases, which personal assistant will say
    """
    GOOD_MORNING = "Good Morning"
    GOOD_AFTERNOON = "Good Afternoon"
    GOOD_EVENING = "Good Evening"
    INCOMPREHENSIBLE_SOUND = "Sphinx could not understand audio can you repeat"
    ERROR = "Sphinx error"
    GOODBYE = "GoodBye"
    JOKE = "I have a joke for u"
    END = "See you again"
    START = "Ready Set Go"

    INTRODUCE = "I am Jarvis"
    SAD = "You seem sad"
    NO_COMMEND = "No match for commend"
    HELP = "How may I help you"

    def __str__(self) -> str:
        return str(self.value)


@unique
class JarvisPhrases(Enum):
    """
    Enum used for storing hard coded phrases, which Jarvis will say
    """
    NO_NOTES = "There are no notes saved"
    NO_CITY = "City Not Found"
    BROWSE = "What do you want to browse?"
    GOOGLE = "What do you want to google?"
    WIKIPEDIA = "What do you want to search in wikipedia?",
    WEATHER = "Where do you want to check the weather?"
    FINISH = "Finish"
    TIME = "How long?"
    CREATE_NOTE = "What do you wanna note?"
    INSERTED_NOTE = "Note inserted"
    HOW_LONG = "How long"

    def __str__(self) -> str:
        return str(self.value)
