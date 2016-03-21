import os
import re

from utils import whereis_exe


class osx_voice():
    def __init__(self, voice_line):
        mess = voice_line.split('  ')
        cleaned = [ part for part in mess if len(part)>0 ]
        self.name = cleaned[0]
        self.locality = cleaned[1]
        self.desc = cleaned[2].replace('# ', '')

    def __str__(self):
        return self.name + ' ' + self.locality + ' ' + self.desc


def fetch_voices():
    osx_voices = []
    if whereis_exe("say"):
        voices_raw = os.popen("say -v ?").read()
        voice_lines = voices_raw.split('\n')
        for line in voice_lines:
            try:
                osx_voices.append(osx_voice(line))
            except IndexError:
                pass
    return osx_voices
