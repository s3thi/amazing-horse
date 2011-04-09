#!/usr/bin/env python

import irclib
import subprocess
from datetime import datetime

FLOOD_CONTROL_TIME = 10


class MusicBot(irclib.SimpleIRCClient):
    def __init__(self):
        irclib.SimpleIRCClient.__init__(self)

        self.last_change = datetime.now()
        
        self.handlers = {
            '!play': self.play,
            '!pause': self.pause,
            '!next': self.next,
            '!prev': self.prev,
            '!up': self.up,
            '!down': self.down,
            '!max': self.max
        }
        
    def start(self):
        self.connection.join('#communityhack')
        irclib.SimpleIRCClient.start(self)

    def say(self, msg):
        self.connection.privmsg('#communityhack', msg)

    def osascript(self, script):
        subprocess.check_call(r'osascript -e "{0}"'.format(script), shell=True)

    def on_pubmsg(self, conn, event):
        text = event.arguments()[0]
        if text in self.handlers:
            self.handlers[text](text)

    def play(self, text):
        self.osascript(r'tell application \"iTunes\" to play')

    def pause(self, text):
        self.osascript(r'tell application \"iTunes\" to pause')

    def next(self, text):
        now = datetime.now()
        if (now - self.last_change).seconds > FLOOD_CONTROL_TIME:
            self.osascript(r'tell application \"iTunes\" to next track')
            self.last_change = now

    def prev(self, text):
        now = datetime.now()
        if (now - self.last_change).seconds > FLOOD_CONTROL_TIME:
            self.osascript(r'tell application \"iTunes\" to previous track')
            self.last_change = now

    def up(self, text):
        self.osascript(r'tell application \"iTunes\"' + 
                        '\n set sound volume to (sound volume + 10)' +
                        '\n end tell')

    def down(self, text):
        self.osascript(r'tell application \"iTunes\"' +
                        '\n set sound volume to (sound volume - 10)' +
                        '\n end tell')

    def max(self, text):
        self.osascript(r'tell application \"iTunes\"' +
                        '\n set sound volume to 100' +
                        '\n end tell')


def main():
    irc = MusicBot()
    irc.connect('irc.freenode.net', 6667, 'AmazingHorse')
    irc.start()


if __name__ == '__main__':
    main()
