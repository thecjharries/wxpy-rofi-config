# coding=utf8

"""This file provide HidableAutoWrapStaticText"""

# pylint: disable=too-many-ancestors

from wx.lib.pubsub.pub import subscribe
from wx.lib.agw.infobar import AutoWrapStaticText


class HidableAutoWrapStaticText(AutoWrapStaticText):
    """
    HidableAutoWrapStaticText adds a toggle handler and listens for hide/show
    actions. Its parent automatically resizes StaticText controls.
    """

    DEFAULT_KIND = 'help_value'

    def __init__(self, parent=None, label="", kind=DEFAULT_KIND):
        AutoWrapStaticText.__init__(self, parent, label)
        subscribe(self.toggle_display, "toggle_display_%s" % kind)

    def toggle_display(self, data):
        """Shows or hides the control based on the published message"""
        if data:
            action = 'Show'
        else:
            action = 'Hide'
        if hasattr(self, action):
            getattr(self, action)()
            self.GetParent().GetParent().Layout()
