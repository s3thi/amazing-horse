#!/usr/bin/env python2
# vim: set sts=4 sw=4 et tw=0:

class Player(object):
    def __init__(self):
        pass
 
    def is_running(self):
        """Is the player running?"""
        raise NotImplementedError("This method must be set by a subclass")

    def is_playing(self):
        """Is the player playing"""
        raise NotImplementedError("This method must be set by a subclass")

    def volume_up(self):
        """Increase volume by 10%"""
        raise NotImplementedError("This method must be set by a subclass")

    def volume_down(self):
        """Decrease volume by 10%"""
        raise NotImplementedError("This method must be set by a subclass")

    def volume_mute(self):
        """Mute volume"""
        raise NotImplementedError("This method must be set by a subclass")

    def volume_max(self):
        """Set volume to maximum"""
        raise NotImplementedError("This method must be set by a subclass")

    def next(self):
        """Next song in playlist"""
        raise NotImplementedError("This method must be set by a subclass")

    def previous(self):
        """Previous song in playlist"""
        raise NotImplementedError("This method must be set by a subclass")

    def play_pause(self):
        """Toggle play/pause on current song"""
        raise NotImplementedError("This method must be set by a subclass")

    def play(self):
        """Play current song"""
        raise NotImplementedError("This method must be set by a subclass")

    def pause(self):
        """Pause current song"""
        raise NotImplementedError("This method must be set by a subclass")
