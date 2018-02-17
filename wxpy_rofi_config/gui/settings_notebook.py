"""This file provides the SettingsNotebook class"""
# pylint: disable=too-many-ancestors

from collections import OrderedDict
from operator import attrgetter

from wx import (
    EVT_NOTEBOOK_PAGE_CHANGED,
    EVT_SIZE,
    FindWindowByName,
    NB_LEFT,
    Notebook,
)

from wxpy_rofi_config.config import Rofi
from wxpy_rofi_config.gui import SettingsPanel


class SettingsNotebook(Notebook):
    """The SettingsNotebook creates tabs for each group of settings"""

    def __init__(self, parent):
        Notebook.__init__(
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
        """Parses the available config into groups"""
        self.config = Rofi()
        self.config.build()
        for key, entry in self.config.config.iteritems():
            if entry.group in self.groups:
                self.groups[entry.group].append(entry)
            else:
                self.groups[entry.group] = [entry]

    def create_tab(self, group):
        """Creates a single tab for a single settings group"""
        sorted_list = sorted(self.groups[group], key=attrgetter('key_name'))
        tab = SettingsPanel(sorted_list, self)
        self.tabs.append(tab)
        self.AddPage(tab, group)

    def create_tabs(self):
        """Creates all tabs for all settings groups"""
        self.group_config()
        for group in self.groups.keys():
            self.create_tab(group)

    def bind_events(self):
        """
        Binds all events. Whenever the window is resized or the tab is changed,
        the active tab will resize its content
        """
        self.Bind(EVT_NOTEBOOK_PAGE_CHANGED, self.resize)
        self.Bind(EVT_SIZE, self.resize)

    def resize(self, event=None):
        """Resizes only the active tab"""
        self.tabs[self.GetSelection()].resize()

    def save(self, event=None):
        """Saves the config to the default location"""
        for index, tab in enumerate(self.tabs):
            group = self.groups.keys()[index]
            for entry in self.groups[group]:
                widget = FindWindowByName(entry.key_name)
                if hasattr(widget, 'GetValue'):
                    value = widget.GetValue()
                elif hasattr(widget, 'GetLabel'):
                    value = widget.GetLabel()
                else:
                    value = entry.current
                self.config.config[entry.key_name].current = value
        self.config.save()
