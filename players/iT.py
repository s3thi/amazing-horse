#!/usr/bin/env python2
# vim: set sts=4 sw=4 et tw=0:

import subprocess

import players.base

class Player(players.base.Player):
    def __init__(self):
        pass

    def _osa_script(self, script):
        subprocess.check_call(r'osascript -e "{0}"'.format(script), shell=True)
 
    def is_running(self):
        #raise NotImplementedError("Kill GM")
        return False

    def is_playing(self):
        raise NotImplementedError("Kill GM")

    def volume_up(self):
        self._osa_script(r'tell application \"iTunes\"' + 
                        '\n set sound volume to (sound volume + 10)' +
                        '\n end tell')

    def volume_down(self):
        self._osa_script(r'tell application \"iTunes\"' +
                        '\n set sound volume to (sound volume - 10)' +
                        '\n end tell')

    def next(self):
        self._osa_script(r'tell application \"iTunes\" to next track')

    def previous(self):
        self._osa_script(r'tell application \"iTunes\" to previous track')

    def play_pause(self):
        raise NotImplementedError("Kill GM")

    def play(self):
        self._osa_script(r'tell application \"iTunes\" to play')

    def pause(self):
        self._osa_script(r'tell application \"iTunes\" to pause')

if __name__ == "__main__":
    player = RBPlayer()
