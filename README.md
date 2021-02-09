# Personal voice assistant - Jarvis
![GitHub](https://img.shields.io/github/license/MichalKacprzak99/jarvis?logo=Github)
![GitHub last commit](https://img.shields.io/github/last-commit/MichalKacprzak99/jarvis)
![GitHub followers](https://img.shields.io/github/followers/MichalKacprzak99?style=social)


## Table of Contents
 * [ What is this project about?](#what-is-this-project-about)
 * [Installation](#installation)
 * [How to use it?](#how-to-use-it)
 * [Basic Personal Assistant](#basic-personal-assistant)
 * [Jarvis](#jarvis)
 * [Create own personal assistant](#create-own-personal-assistant)
 * [Future](#future)

## What is this project about?
We all know the Iron Man, the genius. He created Jarvis during his lifetime. 
It was an artificial intelligence that helped him fight evil. 
This project is my approach to the subject of a personal assistant.

## Installation
    $ git clone https://github.com/MichalKacprzak99/jarvis.git
    $ cd jarvis/
    $ sudo pip3 install -r requirements.txt

## How to use it?
If you've cloned the repository, just run main.py from the src folder.
## Basic Personal Assistant
Main class in this project is PersonalAssistant([here](src/personal_assistant.py)). This class represent voice personal assistant with basic features. 
The basic implemented features are:
* introduce yourself
* convert text to speech
* handle microphone input
* welcome you, different greeting depending on the time of day
* tell a joke
* shutdown computer
* say goodbye

<a></a>
A lot of phrases which personal assistant will tell are hard coded 
so I decided to create simple enum class called Sounds([here](src/sounds.py)).
This is very simple class, which only purpose is to store messages, which will be said by personal assistant.
## Jarvis
Jarvis([here](src/jarvis.py)) inherits after PersonalAssistant class and provide extra features:
* set timer
* take note and read the last note
* browse in google
* open specific web page
* search in wikipedia
* tell a weather in given city

## Create own personal assistant

If you want to create your own version of Jarvis, you can simply create a class
which will inherit from the PersonalAssistant.
Then you can add additional functionalities as you like.

## Future?

There are many possibilities. More features, GUI, face / voice recognition,
home automation (as in Mark Zuckerberg's project), file management, project creation and git management
