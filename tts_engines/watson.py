import json
import requests

from kivy.core.audio import SoundLoader

from secret import WATSON_USERNAME
from secret import WATSON_PASSWORD


class watson_voice():
    def __init__(self, voice_record):
        self.name = voice_record['name']
        self.language = voice_record['language']
        self.gender = voice_record['gender']
        self.url = voice_record['url']
        self.desc = voice_record['description']

    def __str__(self):
        return self.name + ' ' + self.desc


def fetch_voices():
    watson_voices = []
    watson_voices_api_url = 'https://stream.watsonplatform.net/text-to-speech/api/v1/voices'
    r = requests.get(watson_voices_api_url,
                     auth=(WATSON_USERNAME, WATSON_PASSWORD))
    if r.status_code == 200:
        for voice_rec in r.json()['voices']:
            watson_voices.append(watson_voice(voice_rec))
    return watson_voices


def speak(text, voice):
    watson_api_url = 'https://stream.watsonplatform.net/text-to-speech/api/v1/synthesize'
    voice_arg = 'voice=' + voice
    text_arg = 'text=' + text
    r = requests.get(watson_api_url + '?' + voice_arg + '&' + text_arg,
                     auth=(WATSON_USERNAME, WATSON_PASSWORD))
    if r.status_code == 200:
        file = open("out.wav", "wb")
        file.write(r.content)
        file.close()
        sound = SoundLoader.load("out.wav")
        if sound:
            sound.play()
