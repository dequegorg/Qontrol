#!usr/bin/env python

from Xlib.display import Display
from Xlib import X

class Window(object):

    """
        Abstract object representing the X Window of an application
        obtained with the window ID.
    """

    def __init__(self, windowID):

        self._display = Display()
        self._root = self._display.screen().root
        self._window = self._display.create_resource_object('window', windowID)


    def reserve_space(self, left=0, right=0, top=0, bottom=0):

        """ Reserves screen-space for toplevel window. """

        LEFT    = left
        RIGHT   = right
        TOP     = top
        BOTTOM  = bottom

        self._window.change_property(self._display.intern_atom('_NET_WM_STRUT'),
                                    self._display.intern_atom('CARDINAL'),
                                    32, [LEFT, RIGHT, TOP, BOTTOM])
        self._display.sync()


    def set_wm_state_skip_taskbar(self):

        """ Change state of the window. """

        self._window.set_wm_state(Display().intern_atom('_NET_WM_STATE_SKIP_TASKBAR'))

