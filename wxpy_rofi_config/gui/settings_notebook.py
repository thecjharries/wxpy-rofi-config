# pylint: disable=W,C,R

from collections import OrderedDict
# pylint: disable=no-name-in-module
from wx import (
    EVT_NOTEBOOK_PAGE_CHANGED,
    EVT_SIZE,
    NB_LEFT,
    Notebook,
)
# pylint: enable=no-name-in-module

from wxpy_rofi_config.config import Rofi
from wxpy_rofi_config.gui import SettingsPanel


class SettingsNotebook(Notebook):

    def __init__(self, parent):
        super(SettingsNotebook, self).__init__(
            self,
            parent=parent,
            style=NB_LEFT,
            size=(-1, -1)
        )
        self.tabs = []
        self.config = None
        self.groups = OrderedDict()
        self.create_tabs()
        self.bind_events()

    def group_config(self):
        self.config = Rofi()
        self.config.build()
        for key, entry in self.config.config.iteritems():
            if entry.group in self.groups:
                self.groups[entry.group].append(entry)
            else:
                self.groups[entry.group] = [entry]

    def create_tab(self, group):
        tab = SettingsPanel(self.groups[group], self)
        self.tabs.append(tab)
        self.AddPage(tab, group)

    def create_tabs(self):
        self.group_config()
        for group in self.groups.keys():
            self.create_tab(group)

    def bind_events(self):
        self.Bind(EVT_NOTEBOOK_PAGE_CHANGED, self.resize)
        self.Bind(EVT_SIZE, self.resize)

    def resize(self):
        self.tabs[self.GetSelection()].resize()
