#!/usr/bin/env python

import requests
import subprocess

from gtts import gTTS

import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from utils import whereis_exe
from secret import WATSON_USERNAME
from secret import WATSON_PASSWORD


__version__ = '0.0.1'


class SayThis(BoxLayout):
    saywhat_text = ObjectProperty(None)

    def clear(self):
        self.saywhat_text.text = ""
        self.saywhat_text.focus = True

    def sayit_espeak(self, text):
        print("Attempting to speak using espeak:\n"+text)
        if whereis_exe("espeak"):
            subprocess.call(["espeak", self.saywhat_text.text])

    def sayit_google(self, text):
        print("Attempting to speak using Google TTS:\n"+text)
        tts = gTTS(text=self.saywhat_text.text, lang='en')
        tts.save("out.mp3")
        sound = SoundLoader.load("out.mp3")
        if sound:
            sound.play()

    def sayit_osx(self, text, kwargs):
        print("Attempting to speak using OSX TTS:\n"+text)
        if whereis_exe("say"):
            subprocess.call(["say", text, "-v", kwargs['voice'], "-r", kwargs['rate']])

    def sayit_watson(self, text):
        print("Attempting to speak using Watson TTS:\n"+text)
        watson_api_url = 'https://stream.watsonplatform.net/text-to-speech/api/v1/synthesize?text='
        r = requests.get(watson_api_url+text,
                         auth=(WATSON_USERNAME, WATSON_PASSWORD))
        if r.status_code == 200:
            file = open("out.wav", "wb")
            file.write(r.content)
            file.close()
            sound = SoundLoader.load("out.wav")
            if sound:
                sound.play()


class SayThisApp(App):
    def build(self):
        return SayThis()

    def on_pause(self):
        return True

    def on_resume(self):
        pass


if __name__ == '__main__':
    SayThisApp().run()
