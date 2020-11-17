import os
import nltk
from gtts import gTTS
import playsound

AUDIO_FOLDER = "../audio_files"

SOUNDS = ["Good Morning", "Good Afternoon", "Good Evening",
          "Sphinx could not understand audio can you repeat", "Sphinx error",
          "GoodBye", "I have a joke for u", "See you again", "How long",
          "Ready Set Go", "Finish", "I am Jarvis", "You seem sad", "What note",
          "No match for commend", "City Not Found", "How may I help you",
          "There are no notes saved", "Where do you want to check the weather",
          "What do you want to search in wikipedia", "What do you want to google",
          "What do you want to browse"]


def create_images_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        return True
    return False


def create_audio_file(sound):
    tts = gTTS(text=sound, lang="en")
    filename = "_".join(sound.lower().split())
    tts.save(f'{AUDIO_FOLDER}/{filename}.mp3')


def run_audio_file(text):
    filename = "_".join(text.lower().split())
    file_path = f'{AUDIO_FOLDER}/{filename}.mp3'
    playsound.playsound(file_path)


def preset():
    if create_images_folder(AUDIO_FOLDER):
        list(map(lambda sound: create_audio_file(sound), SOUNDS))
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('averaged_perceptron_tagger')
