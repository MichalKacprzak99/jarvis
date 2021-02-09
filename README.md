# Personal voice assistant - Jarvis
***Last Updated: 9 February, 2021***
## Table of Contents
 * [What is Jarvis AI?](#what-is-jarvis-ai)
 * [Installation](#installation)
 * [How to use it?](#how-to-use-it)
 * [Create own personal assistant](#create-own-personal-assistant)
 * [Features](#features)
 * [Future](#future)

## What is Jarvis AI?
We all know the Iron Man, the genius. He created Jarvis during his lifetime. 
It was an artificial intelligence that helped him fight evil. 
This project is my approach to the subject of a personal assistant.

## Installation
    $ git clone https://github.com/MichalKacprzak99/jarvis.git
    $ cd jarvis/
    $ sudo pip3 install -r requirements.txt

## How to use it?
If you've cloned the repository, just run main.py from the src folder. 
## Create own personal assistant
Main class in this project is PersonalAssistant. This class provides basic features as 
* introduce yourself
* convert text to speech
* handle microphone input
* welcome you, different greeting depending on the time of day
* tell a joke
* shutdown computer
* say goodbye

<a></a>
If you want to create your own version of Jarvis, you can simply create a class
which will inherit from the PersonalAssistant.
Then you can add additional functionalities as you like.
## Features
Jarvis can:
* set timer
* take note and read the last note
* browse in google
* open specific web page
* search in wikipedia
* tell a weather in given city

## Future?

There are many possibilities. More features, GUI, face / voice recognition,
home automation (as in Mark Zuckerberg's project), file management, project creation and git management
