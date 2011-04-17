#!/usr/bin/env python2
# vim: set sts=4 sw=4 et tw=0:
#
# Author(s): Rohan Garg <rohan16garg@gmail.com>
# License: MIT (2011)
#

import players.base
import time
from gi.repository import Gio, GLib


class Player(players.base.Player):
    def __init__(self):
        self.BUS_NAME = "org.mpris.amarok"
        self.PLAYER_OBJ_NAME = "/Player"
        self.PLAYER_IFACE_NAME = "org.freedesktop.MediaPlayer"
        self.player_proxy = self._get_proxy(obj_name=self.PLAYER_OBJ_NAME,
                                            iface_name=self.PLAYER_IFACE_NAME)
                                            
    def _get_proxy(self, obj_name, iface_name):
        flags = Gio.DBusProxyFlags.DO_NOT_AUTO_START | Gio.DBusProxyFlags.DO_NOT_LOAD_PROPERTIES
        return Gio.DBusProxy.new_for_bus_sync(Gio.BusType.SESSION, flags,
                                              Gio.DBusInterfaceInfo(),
                                              self.BUS_NAME, obj_name,
                                              iface_name, None)
    def _call_player_proxy(self, method, data):
      time.sleep(0.35)
      return self.player_proxy.call_sync(self.PLAYER_IFACE_NAME+'.'+method, data,
                                           Gio.DBusCallFlags.NONE, -1, None)

    def is_running(self):
        """Is the player running?"""
        status = self._call_player_proxy('GetStatus', None).unpack()[0]
        if status[3] == 1:
          return True
        return False
        
    def is_playing(self):
        """Is the player playing"""
        if (self._call_player_proxy('GetStatus', None).unpack()[0])[0] == 0:
          return True
        return False
        
    def status(self):
        """Returns the current song"""
        msg = None
        if self.is_playing():
          msg = "[Playing]"
        else:
          msg = "[Paused]"
        metadata = self._call_player_proxy('GetMetadata', None).unpack()[0]
        return msg + ' "%s" by "%s" from "%s"' % (metadata['title'],
                                                  metadata['artist'],
                                                  metadata['album'])
            
    def get_volume(self):
        """Get the current volume"""
        return str(round(self._call_player_proxy('VolumeGet', None).unpack()[0]))
        
    def volume_up(self):
        """Decrease volume by 10%"""
        return self._call_player_proxy('VolumeUp', GLib.Variant("(i)", (10,)))
        
    def volume_down(self):
        """Decrease volume by 10%"""
        return self._call_player_proxy('VolumeDown', GLib.Variant("(i)", (10,)))
        
    def volume_mute(self):
        """Mute volume"""
        return self._call_player_proxy('Mute', None)
        
    def volume_max(self):
        """Set volume to maximum"""
        return self._call_player_proxy('VolumeSet', GLib.Variant("(i)", (100,)))
        
    def next(self):
        """Next song in playlist"""
        return self._call_player_proxy('Next', None)
        
    def previous(self):
        """Previous song in playlist"""
        return self._call_player_proxy('Prev', None)
        
    def play_pause(self):
        """Toggle play/pause on current song"""
        return self._call_player_proxy('PlayPause', None)
        
    def play(self):
        """Play current song"""
        if not self.is_playing():
          return self.play_pause()
        
    def pause(self):
        """Pause current song"""
        if self.is_playing():
          return self.play_pause()
