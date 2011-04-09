#!/usr/bin/env python2
# vim: set sts=4 sw=4 et tw=0:
#
# Author(s): Akshay Gupta
# License: MIT (2011)
#

import os
import subprocess

import players.base

class Player(players.base.Player):
    def __init__(self):
        pass

    def _exa_script(self, script):
        subprocess.check_call(r'exaile --{0}'.format(script), shell=True)

    def is_running(self):
        try:
            return subprocess.Popen("exaile -q", shell=True, stdout=subprocess.PIPE).communicate()[0].strip() != ''
        except OSError:
            return False

    def is_playing(self):
        try:
            return subprocess.Popen("exaile -q", shell=True, stdout=subprocess.PIPE).communicate()[0].startswith("status: playing")
        except OSError:
            return False

    def play_pause(self):
        self._exa_script(r'play-pause')

    def play(self):
        if not self.is_playing():
            self.play_pause()

    def pause(self):
        if self.is_playing():
            self.play_pause()

    def next(self):
        self._exa_script(r'next')

    def previous(self):
        self._exa_script(r'prev')

if __name__ == "__main__":
    player = RBPlayer()
