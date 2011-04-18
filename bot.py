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
           'exaile': 'players.ex',}
FLOOD_CONTROL_TIME = 1
SERVER = "irc.oftc.net"
PORT = 6667
CHANNEL = "#hackers-india"
CMDSTR = ['!', '@']
INSULTS = ["a cunt", "a piece of piss", "gayer than NPH", "scared of wee-wees",
           "a poop-monster", "in love with pratual kalia's cock",
           "under observation for pedophilic behaviour", "thinking about you",
           "looking at my horse my horse is amazing", "a nub", "a boob",
           "a creature who puts baboons to shame",
           "a nihilistic, masochistic, gay ayn-rand lover", "allergic to cats",
           "under the impression that he fits in", "in desperate need of some skull-fucking",
           "a terrible, terrible driver", "a fan of justin bieber",
           "a secret member of the chipmunk-andolan movement",
           "currently engaged in dirty acts such as eating Glucon-D",
           "currently occupied, please try again later", "not a funny person at all",
           "thirsty, give him some of your man-juice", "not a big fan of boobs at all",
           "just asking for it", "not going to be happy with this",
           "jealous of pratual kalia's success as a ladies man", "an impudent bastard",
           "afraid of cockroaches", "actually a hermaphrodite",
           "shocked at your blatant disregard for his feelings",
           "crying over the loss of his left ball", "drooling all over his keyboard",
           "saving his virginity for pratual kalia", "self-sufficient in masturbation",
           "not looking for a life at the moment, thank you very much",
           "A BEAUTIFUL BUTTERFLY~~", "a Haiku OS developer, lol"]
# http://lookatmyhorsemyhorseisamazing.com/
LYRICS = ["Look at my horse, my horse is amazing",
          "Give it a lick, Mmm it tastes just like raisins",
          "Stroke on it's mane it turns into a plane",
          "And then it turns back again when you tug on it's winky",
          "Eww that's dirty!",
          "Do you think so? Well I better not show you where the lemonade is made",
          "Sweet Lemonade, Mmm Sweet lemonade",
          "Sweet lemonade, yeah sweet lemonade",
          "(Synth Solo)",
          "Get on my horse, I'll take you round the Universe and all the other places too",
          "I think you'll find that the Universe pretty much covers everything",
          "Shut up woman, get on my horse"]

class MusicBot(irclib.SimpleIRCClient):
    def __init__(self):
        irclib.SimpleIRCClient.__init__(self)
        self._init()
        # First command returns nothing, second command returns what to say
        self.handlers = {
            'play': (self.player.play, self.player.status),
            'pause': (self.player.pause, self.player.status),
            'playpause': (self.player.play_pause, self.player.status),
            'next': (self.player.next, self.player.status),
            'prev': (self.player.previous, self.player.status),
            'up': (self.player.volume_up, self.player.get_volume),
            'down': (self.player.volume_down, self.player.get_volume),
            'status': (self._noop, self.player.status),
            'say': (self._noop, self._lyric_say),
            'randsay': (self._noop, self._lyric_randsay),
            'insult': (self._insult, self._noop),
            'reload': (self._reload, self._noop),
        }

    def _noop(self):
        """Do nothing!"""
        pass

    def _biased_choice(self, objects):
        """Return a random object with bias towards not repeating"""
        import random
        if not self._hacky_insults_state:
            self._hacky_insults_state = range(len(objects))
        i = random.choice(self._hacky_insults_state)
        if random.choice((True, False)) and random.choice((True, False)):
            pass
        else:
            self._hacky_insults_state.remove(i)
        return objects[i]
    
    def _init(self):
        self._hacky_insults_state = range(len(INSULTS))
        self.last_change = datetime.now()
        self._find_running_player()
        self._lyrics_pos = 0

    def _reload(self):
        self.say("Reloading the player module...")
        del(self.player)
        del(self.player_module)
        del(self.player_name)
        self._init()
        self.say("... Done.")

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
            print self.player_name + " not running"
        else:
            raise Exception("OMG NO RUNNING PLAYERS FOUND.")

    def _flood_control(self):
        now = datetime.now()
        if (now - self.last_change).seconds > FLOOD_CONTROL_TIME:
            self.last_change = now
            return False
	return True

    def start(self):
        irclib.SimpleIRCClient.start(self)

    def say(self, msg):
        self.connection.privmsg(CHANNEL, msg)

    def _insult(self):
        self.say("GeneralMaximus is %s" % self._biased_choice(INSULTS))

    def _lyric_say(self):
        ret = LYRICS[self._lyrics_pos]
        self._lyrics_pos += 1
        if self._lyrics_pos > len(LYRICS) - 1:
            self._lyrics_pos = 0
        return ret

    def _lyric_randsay(self):
        return self._biased_choice(LYRICS)

    def _call_cmd(self, cmd):
        """Run the requested command using the appropriate handler"""
        self.handlers[cmd][0]()
        output = self.handlers[cmd][1]()
        if output:
            self.say(output)

    def on_pubmsg(self, conn, event):
        self.event = event
        text = self.event.arguments()[0]
        for each in CMDSTR:
            if text.startswith(each):
                text = text.lstrip(each)
                break
        else:
            return
        if text not in self.handlers:
            return
        if self._flood_control():
            print "Ignored command, flood control!"
            print "Command: %s" % text
            return
        self._call_cmd(text)

def main():
    irc = MusicBot()
    # FIXME: HACK HACK HACK.
    # Add ident + nick fallback
    nick = 'AmazingHorse'+str(random.randint(0, 100))
    print "Connecting to server %s:%s as %s" % (SERVER, PORT, nick)
    irc.connect(SERVER, PORT, nick)
    print "Joining channel %s" % CHANNEL
    irc.connection.join(CHANNEL)
    irc.start()

if __name__ == '__main__':
    main()
