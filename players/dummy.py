#!/usr/bin/env python2
# vim: set sts=4 sw=4 et tw=0:
#
# Author(s): Nirbheek Chauhan
# License: MIT (2011)
#

import players.base

class Player(players.base.Player):
    """
    Dummy player module

    Should be loaded when there's no running players found
    """
    def __init__(self): 
        self.name = "Dummy Player"
 
    def _msg(self):
        return "This is the dummy player module, there were probably no running players found"

    def _ret(self):
        return True

    status = get_volume = _msg
    is_running = is_playing = _ret
    volume_up = volume_down = volume_mute = volume_max = _ret
    next = previous = play_pause = play = pause = _ret
