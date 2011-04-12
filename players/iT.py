#!/usr/bin/env python2
# vim: set sts=4 sw=4 et tw=0:
#
# Author(s): Ankur Sethi
#            Nirbheek Chauhan
# License: MIT (2011)
#

import subprocess

import players.base

class Player(players.base.Player):
    def __init__(self):
        pass

    def _osa_script(self, script):
        subprocess.check_call(r'osascript -e "{0}"'.format(script), shell=True)
 
    def is_running(self):
        ''' returning true here means iTunes is _runnable_, not _running_. '''
        try:
            return subprocess.call('osascript --lol', shell=True, stderr=subprocess.PIPE) == 2
        except OSError:
            return False

    def is_playing(self):
        cmd = r'tell application \"iTunes\"' +\
               '\n get player state' +\
               '\n end tell'
        out = subprocess.Popen('osascript -e "{0}"'.format(cmd),
                               stdout=subprocess.PIPE).communicate()[0]
        return out.strip() == 'playing'

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
        if self.is_playing():
            self.pause()
        else:
            self.play()

    def play(self):
        self._osa_script(r'tell application \"iTunes\" to play')

    def pause(self):
        self._osa_script(r'tell application \"iTunes\" to pause')
