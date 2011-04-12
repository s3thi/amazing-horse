#!/usr/bin/env python2
# vim: set sts=4 sw=4 et tw=0:
#
# Author(s): Ankur Sethi
#            Nirbheek Chauhan
# License: MIT (2011)
#

from gi.repository import Gio, GLib

import players.base

class Player(players.base.Player):
    def __init__(self):
        self.BUS_NAME = "org.gnome.Rhythmbox"
        self.PLAYER_OBJ_NAME = "/org/gnome/Rhythmbox/Player"
        self.PLAYER_IFACE_NAME = "org.gnome.Rhythmbox.Player"
        self.SHELL_OBJ_NAME = "/org/gnome/Rhythmbox/Shell"
        self.SHELL_IFACE_NAME = "org.gnome.Rhythmbox.Shell"
        self.player_proxy = self._get_proxy(obj_name=self.PLAYER_OBJ_NAME,
                                            iface_name=self.PLAYER_IFACE_NAME)
        self.shell_proxy = self._get_proxy(obj_name=self.SHELL_OBJ_NAME,
                                            iface_name=self.SHELL_IFACE_NAME)

    def _get_proxy(self, obj_name, iface_name):
        flags = Gio.DBusProxyFlags.DO_NOT_AUTO_START | Gio.DBusProxyFlags.DO_NOT_LOAD_PROPERTIES
        return Gio.DBusProxy.new_for_bus_sync(Gio.BusType.SESSION, flags,
                                              Gio.DBusInterfaceInfo(),
                                              self.BUS_NAME, obj_name,
                                              iface_name, None)

    def _call_player_proxy(self, method, data):
        return self.player_proxy.call_sync(self.PLAYER_IFACE_NAME+'.'+method, data,
                                           Gio.DBusCallFlags.NONE, -1, None)

    def _call_shell_proxy(self, method, data):
        return self.shell_proxy.call_sync(self.SHELL_IFACE_NAME+'.'+method, data,
                                          Gio.DBusCallFlags.NONE, -1, None)
    def _current_song_props(self):
        playing_uri = self._call_player_proxy('getPlayingUri', None)
        song_props = self._call_shell_proxy('getSongProperties', playing_uri)
        return song_props.unpack()[0]

    def is_running(self):
        if self.shell_proxy.get_name_owner() and self.player_proxy.get_name_owner():
            return True
        return False

    def is_playing(self):
        return self._call_player_proxy("getPlaying", None).unpack()[0]

    def status(self):
        msg = None
        if self.is_playing():
            msg = '[playing]'
        else:
            msg = '[paused]'
        props = self._current_song_props()
        return msg + ' "%s" by "%s" from "%s"' % (props['title'],
                                                  props['artist'],
                                                  props['album'])

    def get_volume(self):
        return str(round(self._call_player_proxy("getVolume", None).unpack()[0]*100))

    def volume_up(self):
        return self._call_player_proxy("setVolumeRelative", GLib.Variant("(d)", (0.1,)))

    def volume_down(self):
        return self._call_player_proxy("setVolumeRelative", GLib.Variant("(d)", (-0.1,)))

    def next(self):
        return self._call_player_proxy("next", None)

    def previous(self):
        return self._call_player_proxy("previous", None)

    def play_pause(self):
        return self._call_player_proxy("playPause", GLib.Variant("(b)", (True,)),)

    def play(self):
        if not self.is_playing():
            self.play_pause()

    def pause(self):
        if self.is_playing():
            self.play_pause()
