# Personal voice assistant - Jarvis
![GitHub](https://img.shields.io/github/license/MichalKacprzak99/jarvis?logo=Github)
![GitHub last commit](https://img.shields.io/github/last-commit/MichalKacprzak99/jarvis)
![PyPI](https://img.shields.io/pypi/v/jarvis-assistant)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jarvis-assistant)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/jarvis-assistant)
![GitHub top language](https://img.shields.io/github/languages/top/MichalKacprzak99/jarvis)
![GitHub followers](https://img.shields.io/github/followers/MichalKacprzak99?style=social)

## Table of Contents
 
 * [What is this project about?](#what-is-this-project-about)
 * [Installation](#installation)
 * [How to use it?](#how-to-use-it)
 * [How Jarvis work?](#how-jarvis-work)
 * [Basic Personal Assistant](#basic-personal-assistant)
 * [Jarvis](#jarvis)
 * [Future](#future)
 * [Documentation and code for pypi package version](#documentation-and-code-for-pypi-package-version)
 * [Resources](#resources)
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
  1. Go to https://openweathermap.org/api and create own api key
  2. Create .env file in the same folder as your main.py file and create environment variable like this
   ```dosini
# .env, private
API_KEY_WEATHER=yours_top_secret_api_key_weather
```
## How Jarvis work?
To make Jarvis more flexible and responsible topic analysis was used. Gaussian Naive Bayes classifier model is the core of Jarvis.
Jarvis can detect the topic of command given from user and respond in the most appropriate way. 

### Dataset
To be able to train used model the dataset was created. It is based on scrapped posts from Twitter. Each tweet was assigned to one of 7 different 
topic:
- wikipedia 
- google
- weather 
- jokes
- notes management
- end of work
- time measurement

Text of each tweet for preprocess in purpose to delete not needed text like links, emoji, stopwords, tags etc.
### Classifier
Gaussian Naive Bayes classifier was chosen because it gives relatively good result from small amounts of training data 
and limited computational resources. Data from a self-made dataset was vectorized, that is, transformed into numbers that
could feed to the machine learning algorithm. Next, data was separate to training and test set, in order to obtain 
performance results. After this finally model was trained and saved.

### Results
Results based on classification report from sklearn
```
         precision    recall  f1-score   support
google        0.48      0.82      0.61       234
joke          0.75      0.86      0.80       274
note          0.97      0.74      0.84       341
stop          0.66      0.84      0.73       237
timer         0.97      0.68      0.80       244
weather       0.97      0.95      0.96       237
wikipedia     0.80      0.44      0.57       235

accuracy                          0.76      1802
macro avg     0.80      0.76      0.76      1802
weighted avg  0.81      0.76      0.77      1802
```
It's not a stellar performance, but considering the size of the dataset it's not bad.
The worst results are achieved for google and wikipedia topic, because these are really similar topics
## Basic Personal Assistant
Main class in this project is PersonalAssistant([code](https://github.com/MichalKacprzak99/jarvis/blob/master/jarvis/personal_assistant.py)). 
The class represent voice personal assistant with basic features. 
The basic implemented features are:
* introduce yourself
* convert text to speech
* handle microphone input
* welcome you, different greeting depending on the time of day
* tell a joke
* say goodbye(stop working)

<a></a>
A lot of phrases which personal assistant will tell are hard coded, so I decided to create simple enum class called BasicPhrases([code](https://github.com/MichalKacprzak99/jarvis/blob/master/jarvis/phrases.py)).
This is very simple class, which only purpose is to store messages, which will be said by a personal assistant.
## Jarvis
Jarvis([code](https://github.com/MichalKacprzak99/jarvis/blob/master/jarvis/jarvis.py)) 
inherits after PersonalAssistant class and provide extra features:
* set timer
* take note and read the last note
* search in google
* search in wikipedia
* tell a weather in given city


## Future?

There are many possibilities. More features, GUI, face / voice recognition,
home automation (as in Mark Zuckerberg's project), file management, project creation and git management

## Documentation and code for pypi package version

The documentation and code for Jarvis pypi package version is available on [package_version](https://github.com/MichalKacprzak99/jarvis/tree/package_version) branch

## Resources

- https://monkeylearn.com/topic-analysis/ - brief description of topic analysis
- https://stackoverflow.com/questions/64719706/cleaning-twitter-data-pandas-python - function for cleaning data
- https://medium.com/@kohlishivam5522/understanding-a-classification-report-for-your-machine-learning-model-88815e2ce397 - explanation of performance metrics