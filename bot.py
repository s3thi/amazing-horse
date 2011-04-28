#!/usr/bin/env python2
# vim: set sts=4 sw=4 et tw=0 :
#
# Author(s): Ankur Sethi
#            Nirbheek Chauhan
# License: MIT (2011)
#

import ConfigParser
import random
import sys
from datetime import datetime

from external import irclib

from players.base import Player

# dummy module must always be the last one
PLAYERS = ['players.'+i for i in ['rb', 'iT', 'ex', 'amarok', 'dummy']]
FLOOD_CONTROL_TIME = 1
irc_config = ConfigParser.SafeConfigParser()
irc_config.readfp(open("default.cfg", 'r'))
SERVER = irc_config.get("irc", "server")
PORT = irc_config.get("irc", "port")
CHANNEL = irc_config.get("irc", "channel")
CMDSTR = ['!', '@']
LYRICS = []
INSULTS = []

class MusicBot(irclib.SimpleIRCClient):
    def __init__(self):
        irclib.SimpleIRCClient.__init__(self)
        self._init()

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
        global INSULTS
        global LYRICS
        self._hacky_insults_state = range(len(INSULTS))
        self.last_change = datetime.now()
        # May crash due to bugs in pygobject, etc
        self._find_running_player()
        self._lyrics_pos = 0
        # Chomp newlines because they break ACTIONs
        INSULTS = [i.strip() for i in open('insults.txt', 'r').readlines()]
        # http://lookatmyhorsemyhorseisamazing.com/
        LYRICS = [i.strip() for i in open('lyrics.txt', 'r').readlines()]
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
            'reload': (self._reload, self._noop),
        }
        self.input_handlers = {
            'insult': (self._insult, self._noop),
        }

    def _reload(self):
        self.say("Reloading myself...")
        del(self.player)
        del(self.player_module)
        self._init()
        self.say("... Done.")

    def _import(self, name):
        # http://docs.python.org/library/functions.html#__import__
        mod = __import__(name)
        for each in name.split('.')[1:]:
            mod = getattr(mod, each)
        # Reload in case it was already loaded and self._reload was called
        return reload(mod)

    def _find_running_player(self):
        """
        Find the currently running player

        uses the is_running() function for each module
        """
        for player_module in PLAYERS:
            try:
                self.player_module = self._import(player_module)
            except ImportError:
                print "Could not import %s, ignoring..." % player_module
                continue
            self.player = self.player_module.Player()
            if self.player.is_running():
                break
            print self.player.name + " not running"
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
        if msg:
            self.connection.privmsg(CHANNEL, msg)

    def _insult(self, *args):
        target = "everyone"
        if args and len(args[0].split()) > 1:
            # Extract the command string and assign the target
            target = args[0].split()[1]
        insult = self._biased_choice(INSULTS)
        if target == "self":
            self.connection.action(CHANNEL, "is " + insult)
        else:
            self.say("%s is %s" % (target, insult))

    def _lyric_say(self):
        ret = LYRICS[self._lyrics_pos]
        self._lyrics_pos += 1
        if self._lyrics_pos > len(LYRICS) - 1:
            self._lyrics_pos = 0
        return ret

    def _lyric_randsay(self):
        return self._biased_choice(LYRICS)

    def _call_cmd(self, handler, *args):
        """
        Run the command handler provided.
        Optional args are passed on to handler[0].
        """
        if self._flood_control():
            print "Ignored command, flood control!"
            print "Command: %s, %s" % handler
            return
        try:
            handler[0](*args)
            self.say(handler[1]())
        except:
            # Really dangerous to capture all possible exceptions, but meh
            self.say("Received error %s on command" % sys.exc_info()[1])
            self._reload()

    def _strip_cmdstr(self, text):
        for cmdstr in CMDSTR:
            if text.startswith(cmdstr):
                return text.lstrip(cmdstr)
        return text

    def on_pubmsg(self, conn, event):
        self.event = event
        text = self.event.arguments()[0].strip()
        cmd = self._strip_cmdstr(text)
        if not cmd or text == cmd:
            # Not a command at all
            return
        if cmd in self.handlers:
            # Command that doesn't need to know the command string
            return self._call_cmd(self.handlers[cmd])
        for each in self.input_handlers:
            cmd = cmd.split()[0]
            if each.startswith(cmd):
                # Command that needs to know the command string
                return self._call_cmd(self.input_handlers[each], text)

    def on_error(self, conn, event):
        print "!!! Error:" + event.arguments()[0]

    def _join(self):
        print "Joining channel:" + CHANNEL
        self.connection.join(CHANNEL)

    def on_kick(self, conn, event):
        print "Was kicked, rejoining..."
        self._join()

    def on_join(self, conn, event):
        print "Joined channel."

    def on_pubnotice(self, conn, event):
        print "Public Notice: " + event.arguments()[0]

    def on_privnotice(self, conn, event):
        print "Private Notice from %s: %s" % (event.source(), event.arguments()[0])
        # FIXME: Major hack to allow bot to join channels on IRC networks that
        # don't allow channel joins till private notices have been sent to the user
        self._join()

def main():
    irc = MusicBot()
    # FIXME: HACK HACK HACK.
    # Add ident + nick fallback
    nick = 'AmazingHorse'+str(random.randint(0, 100))
    params = (SERVER, int(PORT), nick)
    print "Connecting to server %s:%s as %s" % params
    irc.connect(*params)
    irc.start()

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        # Override defaults with user configuration
        irc_config.read(sys.argv[1])
    SERVER = irc_config.get("irc", "server")
    PORT = irc_config.get("irc", "port")
    CHANNEL = irc_config.get("irc", "channel")
    main()
