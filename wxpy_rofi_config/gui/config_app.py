# coding=utf8
# pylint: disable=W,C,R
# pylint: disable=no-member
import wx
import wx.lib.mixins.inspection

from wxpy_rofi_config.gui import ConfigFrame


class ConfigApp(wx.App, wx.lib.mixins.inspection.InspectionMixin):

    def OnInit(self):
        self.Init()  # initialize the inspection tool
        frame = ConfigFrame(None, title="rofi Configuration")
        frame.Show()
        self.SetTopWindow(frame)
        return True
