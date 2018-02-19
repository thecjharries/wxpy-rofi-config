# coding=utf8

"""This file provides ConfigApp"""

# pylint: disable=too-many-ancestors

from wx import App
from wx.lib.mixins.inspection import InspectionMixin

from wxpy_rofi_config.gui import ConfigFrame


class ConfigApp(App, InspectionMixin):
    """This class runs the main application"""

    def OnInit(self):  # pylint:disable=invalid-name
        """
        The OnInit is used instead of __init__ to properly handle the wxPython
        boot and InspectionMixin
        """
        self.Init()  # initialize the inspection tool
        frame = ConfigFrame(None, title="rofi Configuration")
        frame.Show()
        self.SetTopWindow(frame)
        return True
