# coding=utf8

"""This file provides ConfigPage"""

from wx import (
    ALIGN_RIGHT,
    ALL,
    BOTTOM,
    BoxSizer,
    EXPAND,
    FlexGridSizer,
    HORIZONTAL,
    ID_ANY,
    LI_HORIZONTAL,
    Panel,
    StaticLine,
    StaticText,
    TextCtrl,
    TOP,
    VERTICAL,
)
from wx.lib.scrolledpanel import ScrolledPanel

from wxpy_rofi_config.gui import HidableAutoWrapStaticText


class ConfigPage(Panel):
    """ConfigPage holds the GUI for a single tab pane"""

    def __init__(self, parent, config):
        Panel.__init__(self, parent=parent, id=ID_ANY)

        self.scrolled_panel = ScrolledPanel(self)
        self.scrolled_panel.SetAutoLayout(1)
        self.scrolled_panel.SetupScrolling()
        self.main_sizer = BoxSizer(HORIZONTAL)
        self.grid_sizer = FlexGridSizer(2, 10, 10)
        for index, entry in enumerate(config):
            if index > 0:
                for _ in range(0, 2):
                    rule = StaticLine(
                        self.scrolled_panel,
                        style=LI_HORIZONTAL,
                        size=(-1, 2)
                    )
                    self.grid_sizer.Add(rule, proportion=1, flag=EXPAND |
                                        TOP | BOTTOM, border=10)
            if entry.help_value:
                self.grid_sizer.Add(1, 0, 1, EXPAND)
                help_sizer = BoxSizer(HORIZONTAL)
                help_label = HidableAutoWrapStaticText(
                    parent=self.scrolled_panel,
                    label=u"%s" % entry.help_value.decode('utf8', 'ignore'),
                    kind='help_value',
                )
                help_sizer.Add(help_label, -1, EXPAND)
                self.grid_sizer.Add(help_sizer, 1, EXPAND)
            label_sizer = BoxSizer(VERTICAL)
            label_sizer.Add(0, 1, 1, EXPAND)
            label = StaticText(
                self.scrolled_panel,
                label=entry.key_name,
                style=ALIGN_RIGHT
            )
            label_sizer.Add(label, flag=ALIGN_RIGHT)
            label_sizer.Add(0, 1, 1, EXPAND)
            self.grid_sizer.Add(label_sizer, 0, EXPAND)
            current_value = TextCtrl(
                self.scrolled_panel,
                value=str(entry.current),
                size=(-1, -1)
            )
            self.grid_sizer.Add(current_value, -1, EXPAND)
            if entry.man:
                self.grid_sizer.Add(1, 0, 1, EXPAND)
                man_sizer = BoxSizer(HORIZONTAL)
                man_label = HidableAutoWrapStaticText(
                    parent=self.scrolled_panel,
                    label=u"%s" % entry.man.decode('utf8', 'ignore'),
                    kind='man',
                )
                man_sizer.Add(man_label, -1, EXPAND)
                self.grid_sizer.Add(man_sizer, 1, EXPAND)
        self.grid_sizer.AddGrowableCol(1, 1)
        scroll_sizer = BoxSizer(HORIZONTAL)
        scroll_sizer.Add(self.grid_sizer, 1, EXPAND | ALL, 10)
        self.scrolled_panel.SetSizer(scroll_sizer)
        self.main_sizer.Add(self.scrolled_panel, 1, EXPAND)
        self.SetSizer(self.main_sizer)
