import os

from dotenv import load_dotenv
from pathlib import Path  # python3 only

# set path to env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    API_KEY_WEATHER = os.getenv('API_KEY_WEATHER')
