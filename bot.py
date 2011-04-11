#!/usr/bin/env python2
# vim: set sts=4 sw=4 et tw=0:
#
# Author(s): Ankur Sethi
#            Nirbheek Chauhan
# License: MIT (2011)
#

import random
from datetime import datetime

from external import irclib

from players.base import Player

PLAYERS = {'rhythmbox': 'players.rb',
	   'iTunes': 'players.iT',
           'exaile': 'players.ex'}
FLOOD_CONTROL_TIME = 1
NETWORK = "irc.oftc.net"
CHANNEL = "#hackers-india"

class MusicBot(irclib.SimpleIRCClient):
    def __init__(self):
        irclib.SimpleIRCClient.__init__(self)
        self.last_change = datetime.now()
	self._find_running_player()
        self.handlers = {
            '!play': self.player.play,
            '!pause': self.player.pause,
            '!playpause': self.player.play_pause,
            '!next': self.player.next,
            '!prev': self.player.previous,
            '!up': self.player.volume_up,
            '!down': self.player.volume_down,
        }

    def _import(self, name):
	# http://docs.python.org/library/functions.html#__import__
	mod = __import__(name)
	for each in name.split('.')[1:]:
	    mod = getattr(mod, each)
	return mod

    def _find_running_player(self):
	"""
	Find the currently running player

	uses the is_running() function for each module
	"""
	for (player_name, player_module) in PLAYERS.items():
	    self.player_name = player_name
            try:
	        self.player_module = self._import(player_module)
            except ImportError:
                print "Ignoring " + player_name
                continue
	    self.player = self.player_module.Player()
	    if self.player.is_running():
		return
        else:
            raise Exception("OMG NO RUNNING PLAYERS FOUND.")

    def _flood_control(self):
        now = datetime.now()
        if (now - self.last_change).seconds > FLOOD_CONTROL_TIME:
            self.last_change = now
            return False
	return True

    def start(self):
        self.connection.join(CHANNEL)
        irclib.SimpleIRCClient.start(self)

    def say(self, msg):
        self.connection.privmsg(CHANNEL, msg)

    def on_pubmsg(self, conn, event):
        text = event.arguments()[0]
        if text in self.handlers:
            if not self._flood_control():
                self.handlers[text]()
            else:
                print "Ignored command, flood control!"
                print "Command: %s" % text

def main():
    irc = MusicBot()
    # FIXME: HACK HACK HACK.
    # Add ident + nick fallback
    irc.connect(NETWORK, 6667, 'AmazingHorse'+str(random.randint(0, 100)))
    irc.start()

if __name__ == '__main__':
    main()
