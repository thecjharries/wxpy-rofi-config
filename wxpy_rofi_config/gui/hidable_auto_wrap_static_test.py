# coding=utf8

"""This file provide HidableAutoWrapStaticText"""

import wx
from wx.lib.pubsub import pub
from wx.lib.agw.infobar import AutoWrapStaticText

from wxpy_rofi_config.config import Rofi


class HidableAutoWrapStaticText(AutoWrapStaticText):
    """
    HidableAutoWrapStaticText adds a toggle handler and listens for hide/show
    actions. Its parent automatically resizes StaticText controls.
    """

    def __init__(self, parent=None, label="", kind='help_value'):
        AutoWrapStaticText.__init__(self, parent, label)
        pub.subscribe(self.toggle_display, "toggle_display_%s" % kind)

    def toggle_display(self, data):
        """Shows or hides the control based on the published message"""
        if data:
            action = 'Show'
        else:
            action = 'Hide'
        if hasattr(self, action):
            getattr(self, action)()
            self.GetParent().GetSizer().Layout()
