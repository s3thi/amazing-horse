#!/usr/bin/env python2
# vim: set sts=4 sw=4 et tw=0:
#
# Author(s): Rohan Garg <rohan16garg@gmail.com>
# License: GPL (2011)
#

import players.base
import dbus
import time

class Player(players.base.Player):
    def __init__(self):
        self.sessionBus = dbus.SessionBus()
        self.player = self.sessionBus.get_object("org.mpris.amarok",
						 "/Player")
 
    def is_running(self):
        """Is the player running?"""
        status = self.player.GetStatus()
        if status[3] == 1:
          return True
        return False
        
    def is_playing(self):
        """Is the player playing"""
        """Introduce a time delay, DBus seems to lag with python"""
        time.sleep(0.1)
        if self.player.GetStatus()[0] == 0:
          return True
        else:
          return False
        
    def status(self):
        """Returns the current song"""
        """Introduce a time delay, DBus seems to lag with python"""
        time.sleep(0.1)
        msg = None
        if self.is_playing():
          msg = "[Playing]"
        else:
          msg = "[Paused]"
        metadata = self.player.GetMetadata()
        return msg + ' "%s" by "%s" from "%s"' % (metadata['title'],
                                                  metadata['artist'],
                                                  metadata['album'])
            
    def get_volume(self):
        """Get the current volume"""
        return str(round(self.player.VolumeGet()))
        
    def volume_up(self):
        """Increase volume by 10%"""
        return self.player.VolumeUp(10)
        
    def volume_down(self):
        """Decrease volume by 10%"""
        return self.player.VolumeDown(10)
        
    def volume_mute(self):
        """Mute volume"""
        return self.player.Mute()
        
    def volume_max(self):
        """Set volume to maximum"""
        return self.player.VolumeSet(100)
        
    def next(self):
        """Next song in playlist"""
        return self.player.Next()
        
    def previous(self):
        """Previous song in playlist"""
        return self.player.Prev()
        
    def play_pause(self):
        """Toggle play/pause on current song"""
        return self.player.PlayPause()
        
    def play(self):
        """Play current song"""
        if not self.is_playing():
          return self.play_pause()
        
    def pause(self):
        """Pause current song"""
        if self.is_playing():
          return self.play_pause()
