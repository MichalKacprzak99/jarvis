# Personal voice assistant - Jarvis
![GitHub](https://img.shields.io/github/license/MichalKacprzak99/jarvis?logo=Github)
![GitHub last commit](https://img.shields.io/github/last-commit/MichalKacprzak99/jarvis)
![PyPI](https://img.shields.io/pypi/v/jarvis-assistant)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jarvis-assistant)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/jarvis-assistant)
![GitHub top language](https://img.shields.io/github/languages/top/MichalKacprzak99/jarvis)
![GitHub followers](https://img.shields.io/github/followers/MichalKacprzak99?style=social)

## Table of Contents
 * [ What is this project about?](#what-is-this-project-about)
 * [Installation](#installation)
 * [How to use it?](#how-to-use-it)
 * [Basic Personal Assistant](#basic-personal-assistant)
 * [Jarvis](#jarvis)
 * [Create your own personal assistant](#create-your-own-personal-assistant)
 * [Future](#future)

## What is this project about?
We all know the Iron Man, the genius. He created Jarvis during his lifetime. 
It was artificial intelligence that helped him fight evil. 
This project is my approach to the subject of a personal assistant.

## Installation
There are two ways to use my library:

    $ git clone https://github.com/MichalKacprzak99/jarvis.git
    $ cd jarvis/
    $ sudo pip install -r requirements.txt
    
 <a></a>  
  
    $ pip install jarvis-assistant
    
<a></a> 

## How to use it?
After installation create file e.g. "main.py" and write:

```python
from jarvis import Jarvis

if __name__ == '__main__':
    jarvis = Jarvis()
    jarvis.start()
```
 This will run jarvis, and you will be able to enjoy your own voice assistant. 
 If you want to have access to feature which give you weather in specific city 
 you have to do two things:
  1. Go to https://openweathermap.org/api and create own api key/
  2. Create .env file in the same folder as your main.py file and create environment variable like this
   ```dosini
# .env, private
API_KEY_WEATHER=yours_top_secret_api_key_weather
```
## Basic Personal Assistant
Main class in this project is PersonalAssistant([code](https://github.com/MichalKacprzak99/jarvis/blob/master/jarvis/personal_assistant.py)). 
This class represents voice personal assistant with basic features. 
The basic implemented features are:
* introduce yourself
* convert text to speech
* handle microphone input
* welcome you, different greeting depending on the time of day
* tell a joke
* shutdown computer
* say goodbye

<a></a>
A lot of phrases which personal assistant will tell are hard coded, so I decided to create simple enum class called BasicPhrases([code](https://github.com/MichalKacprzak99/jarvis/blob/master/jarvis/phrases.py)).
This is very simple class, which only purpose is to store messages, which will be said by a personal assistant.
## Jarvis
Jarvis([code](https://github.com/MichalKacprzak99/jarvis/blob/master/jarvis/jarvis.py)) 
inherits after PersonalAssistant class and provide extra features:
* set timer
* take note and read the last note
* browse in google
* open specific web page
* search in wikipedia
* tell a weather in given city

## Create your own personal assistant

If you want to create your own version of personal assistant, you can simply create a class
which will inherit from the PersonalAssistant.
Then you can add additional functionalities as you like.

## Future?

There are many possibilities. More features, GUI, face / voice recognition,
home automation (as in Mark Zuckerberg's project), file management, project creation and git management
