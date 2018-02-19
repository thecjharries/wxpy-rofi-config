# coding=utf8

"""This file provides ConfigApp"""

# pylint: disable=too-many-ancestors

import wx
import wx.lib.mixins.inspection

from wxpy_rofi_config.gui import ConfigFrame


class ConfigApp(wx.App, wx.lib.mixins.inspection.InspectionMixin):
    """This class runs the main application"""

    def OnInit(self):
        """
        The OnInit is used instead of __init__ to properly handle the wxPython
        boot and InspectionMixin
        """
        self.Init()  # initialize the inspection tool
        frame = ConfigFrame(None, title="rofi Configuration")
        frame.Show()
        self.SetTopWindow(frame)
        return True
