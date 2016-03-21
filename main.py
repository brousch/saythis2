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
from tts_engines import osx_say
from tts_engines import watson


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
        osx_say.speak(text, kwargs['voice'], kwargs['rate'])

    def sayit_watson(self, text, kwargs):
        print("Attempting to speak using Watson TTS:\n"+text)
        watson.speak(text, kwargs['voice'])


class SayThisApp(App):
    def build(self):
        return SayThis()

    def on_pause(self):
        return True

    def on_resume(self):
        pass


if __name__ == '__main__':
    SayThisApp().run()
