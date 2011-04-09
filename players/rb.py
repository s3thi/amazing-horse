#!/usr/bin/env python2
# vim: set sts=4 sw=4 et tw=0:

from gi.repository import Gio, GLib

import players.base

class Player(players.base.Player):
    def __init__(self):
        self.BUS_NAME = "org.gnome.Rhythmbox"
        self.OBJ_NAME = "/org/gnome/Rhythmbox/Player"
        self.IFACE_NAME = "org.gnome.Rhythmbox.Player"
        self.proxy = self._get_proxy()

    def _get_proxy(self):
        flags = Gio.DBusProxyFlags.DO_NOT_AUTO_START | Gio.DBusProxyFlags.DO_NOT_LOAD_PROPERTIES
        return Gio.DBusProxy.new_for_bus_sync(Gio.BusType.SESSION, flags,
                                              Gio.DBusInterfaceInfo(),
                                              self.BUS_NAME, self.OBJ_NAME, self.IFACE_NAME, None)

    def _call_proxy(self, method, data):
        return self.proxy.call_sync(self.IFACE_NAME+'.'+method, data,
                                    Gio.DBusCallFlags.NONE, -1, None)
 
    def is_running(self):
        if self.proxy.get_name_owner():
            return True
        return False

    def is_playing(self):
        return self._call_proxy("getPlaying", None).unpack()[0]

    def volume_up(self):
        return self._call_proxy("setVolumeRelative", GLib.Variant("(d)", (0.1,)))

    def volume_down(self):
        return self._call_proxy("setVolumeRelative", GLib.Variant("(d)", (-0.1,)))

    def next(self):
        return self._call_proxy("next", None)

    def previous(self):
        return self._call_proxy("previous", None)

    def play_pause(self):
        return self._call_proxy("playPause", GLib.Variant("(b)", (True,)),)

    def play(self):
        if not self.is_playing():
            self.play_pause()

    def pause(self):
        if self.is_playing():
            self.play_pause()

if __name__ == "__main__":
    player = RBPlayer()
