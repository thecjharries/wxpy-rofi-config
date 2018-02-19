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
    ID_EXIT,
    ITEM_CHECK,
    Menu,
    MenuBar,
    NB_LEFT,
    NewId,
    Notebook,
    Panel,
    StatusBar,
)
from wx.lib.pubsub import pub

from wxpy_rofi_config.config import Rofi
from wxpy_rofi_config.gui import ConfigPage


class ConfigFrame(Frame):
    """ConfigFrame is used as the primary app context"""

    def __init__(self, parent, title=""):
        Frame.__init__(
            self,
            parent=parent,
            id=ID_ANY,
            size=(800, 640),
            title=title
        )
        menu_bar = MenuBar()
        file_menu = Menu()
        self.exit_menu_item = file_menu.Append(
            ID_EXIT,
            'E&xit\tCtrl+w'
        )
        menu_bar.Append(file_menu, '&File')
        docs_menu = Menu()
        self.help_values_menu_item = docs_menu.Append(
            NewId(),
            'rofi --help',
            'Show or hide pertinent rofi --help info',
            ITEM_CHECK,
        )
        self.help_values_menu_item.Check(True)
        self.man_values_menu_item = docs_menu.Append(
            NewId(),
            'man rofi',
            'Show or hide pertinent man rofi info',
            ITEM_CHECK
        )
        self.man_values_menu_item.Check(True)
        menu_bar.Append(docs_menu, '&Docs')
        self.SetMenuBar(menu_bar)
        status_bar = StatusBar(self)
        self.SetStatusBar(status_bar)
        panel = Panel(self)
        notebook = Notebook(panel, style=NB_LEFT)
        config = Rofi()
        config.build()
        groups = {}
        for _, entry in config.config.items():
            if entry.group in groups:
                groups[entry.group].append(entry)
            else:
                groups[entry.group] = [entry]
        for key, config_list in groups.items():
            page = ConfigPage(notebook, config_list)
            notebook.AddPage(page, key)
        sizer = BoxSizer(HORIZONTAL)
        sizer.Add(notebook, 1, EXPAND)
        panel.SetSizer(sizer)

        self.Bind(EVT_MENU, self.exit, self.exit_menu_item)
        self.Bind(EVT_MENU, self.toggle_display, self.help_values_menu_item)
        self.Bind(EVT_MENU, self.toggle_display, self.man_values_menu_item)

    def toggle_display(self, event):
        """Publishes show/hide messages via pub"""
        if self.help_values_menu_item.Id == event.Id:
            kind = 'help_value'
        elif self.man_values_menu_item.Id == event.Id:
            kind = 'man'
        else:
            kind = None
        if kind:
            pub.sendMessage("toggle_display_%s" % kind, data=event.IsChecked())

    def exit(self, event=None):  # pylint: disable=unused-argument
        """Kills the app"""
        self.GetTopLevelParent().Close()
