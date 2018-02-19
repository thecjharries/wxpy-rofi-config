# coding=utf8

import wx
from wx.lib.scrolledpanel import ScrolledPanel

from wxpy_rofi_config.config import Rofi
from wxpy_rofi_config.gui import HidableAutoWrapStaticText


class ConfigPage(wx.Panel):

    def __init__(self, parent, config):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        scrolled_panel = ScrolledPanel(self)
        scrolled_panel.SetAutoLayout(1)
        scrolled_panel.SetupScrolling()
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer = wx.FlexGridSizer(2, 10, 10)
        for index, entry in enumerate(config):
            if index > 0:
                for _ in range(0, 2):
                    rule = wx.StaticLine(
                        scrolled_panel,
                        style=wx.LI_HORIZONTAL,
                        size=(-1, 2)
                    )
                    grid_sizer.Add(rule, proportion=1, flag=wx.EXPAND |
                                   wx.TOP | wx.BOTTOM, border=10)
            if entry.help_value:
                grid_sizer.Add(1, 0, 1, wx.EXPAND)
                help_sizer = wx.BoxSizer(wx.HORIZONTAL)
                help_label = HidableAutoWrapStaticText(
                    parent=scrolled_panel,
                    label=u"%s" % entry.help_value.decode('utf8', 'ignore'),
                    kind='help_value',
                )
                help_sizer.Add(help_label, -1, wx.EXPAND)
                grid_sizer.Add(help_sizer, 1, wx.EXPAND)
            label_sizer = wx.BoxSizer(wx.VERTICAL)
            label_sizer.Add(0, 1, 1, wx.EXPAND)
            label = wx.StaticText(
                scrolled_panel,
                label=entry.key_name,
                style=wx.ALIGN_RIGHT
            )
            label_sizer.Add(label, flag=wx.ALIGN_RIGHT)
            label_sizer.Add(0, 1, 1, wx.EXPAND)
            grid_sizer.Add(label_sizer, 0, wx.EXPAND)
            current_value = wx.TextCtrl(
                scrolled_panel,
                value=str(entry.current),
                size=(-1, -1)
            )
            grid_sizer.Add(current_value, -1, wx.EXPAND)
            if entry.man:
                grid_sizer.Add(1, 0, 1, wx.EXPAND)
                man_sizer = wx.BoxSizer(wx.HORIZONTAL)
                man_label = HidableAutoWrapStaticText(
                    parent=scrolled_panel,
                    label=u"%s" % entry.man.decode('utf8', 'ignore'),
                    kind='man',
                )
                man_sizer.Add(man_label, -1, wx.EXPAND)
                grid_sizer.Add(man_sizer, 1, wx.EXPAND)
        grid_sizer.AddGrowableCol(1, 1)
        scroll_sizer = wx.BoxSizer(wx.HORIZONTAL)
        scroll_sizer.Add(grid_sizer, 1, wx.EXPAND | wx.ALL, 10)
        scrolled_panel.SetSizer(scroll_sizer)
        main_sizer.Add(scrolled_panel, 1, wx.EXPAND)
        self.SetSizer(main_sizer)
