# coding=utf8

"""This file provides ConfigFrame"""

# pylint: disable=too-many-ancestors

from wx import (
    BoxSizer,
    EVT_MENU,
    EXPAND,
    Frame,
    HORIZONTAL,
    ID_ANY,
    NB_LEFT,
    Notebook,
    Panel,
    StatusBar,
)

from wxpy_rofi_config.config import Rofi
from wxpy_rofi_config.gui import ConfigFrameMenuBar, ConfigPage


class ConfigFrame(Frame):
    """ConfigFrame is used as the primary app context"""

    config = None
    menu_bar = None
    groups = None

    def __init__(self, parent, title=""):
        Frame.__init__(
            self,
            parent=parent,
            id=ID_ANY,
            size=(800, 640),
            title=title
        )

    def construct_gui(self):
        """Constructs ConfigFrame's GUI"""
        self.menu_bar = ConfigFrameMenuBar()
        self.SetMenuBar(self.menu_bar)
        status_bar = StatusBar(self)
        self.SetStatusBar(status_bar)

    def construct_config(self):
        """Constucts the Rofi config object and parses its groups"""
        self.config = Rofi()
        self.config.build()
        self.groups = {}
        for _, entry in self.config.config.items():
            if entry.group in self.groups:
                self.groups[entry.group].append(entry)
            else:
                self.groups[entry.group] = [entry]

    def construct_notebook(self):
        """Constructs the main Notebook panel"""
        panel = Panel(self)
        notebook = Notebook(panel, style=NB_LEFT)
        for key, config_list in self.groups.items():
            page = ConfigPage(notebook, config_list)
            notebook.AddPage(page, key)
        sizer = BoxSizer(HORIZONTAL)
        sizer.Add(notebook, 1, EXPAND)
        panel.SetSizer(sizer)

    def bind_events(self):
        """Binds events on ConfigFrame"""
        self.Bind(
            EVT_MENU,
            self.menu_bar.exit,
            self.menu_bar.exit_menu_item
        )
        self.Bind(
            EVT_MENU,
            self.menu_bar.toggle_display,
            self.menu_bar.help_values_menu_item
        )
        self.Bind(
            EVT_MENU,
            self.menu_bar.toggle_display,
            self.menu_bar.man_values_menu_item
        )
