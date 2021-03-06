import os

from dotenv import load_dotenv
from pathlib import Path  # python3 only
from enum import Enum, unique

# set path to env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


@unique
class Config(Enum):
    """
    Enum used for storing environment variables
    """
    API_KEY_WEATHER = os.getenv('API_KEY_WEATHER')

    def __str__(self) -> str:
        return str(self.value)
