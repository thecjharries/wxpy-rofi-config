# coding=utf8
# pylint: disable=W,C,R
# pylint: disable=no-member
import wx
from wx.lib.pubsub import pub
from wx.lib.agw.infobar import AutoWrapStaticText

from wxpy_rofi_config.config import Rofi


class HidableAutoWrapStaticText(AutoWrapStaticText):

    def __init__(self, parent=None, label="", kind='help_value'):
        AutoWrapStaticText.__init__(self, parent, label)
        pub.subscribe(self.toggle_display, "toggle_display_%s" % kind)

    def toggle_display(self, data):
        if data:
            action = 'Show'
        else:
            action = 'Hide'
        if hasattr(self, action):
            getattr(self, action)()
            self.GetParent().GetSizer().Layout()
