# coding=utf8

import wx
from wx.lib.pubsub import pub

from wxpy_rofi_config.config import Rofi
from wxpy_rofi_config.gui import ConfigPage


class ConfigFrame(wx.Frame):

    def __init__(self, parent, title=""):
        wx.Frame.__init__(
            self,
            parent=parent,
            id=wx.ID_ANY,
            size=(800, 640),
            title=title
        )
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        self.exit_menu_item = file_menu.Append(
            wx.ID_EXIT,
            'E&xit\tCtrl+w'
        )
        menu_bar.Append(file_menu, '&File')
        docs_menu = wx.Menu()
        self.help_values_menu_item = docs_menu.Append(
            wx.NewId(),
            'rofi --help',
            'Show or hide pertinent rofi --help info',
            wx.ITEM_CHECK,
        )
        self.help_values_menu_item.Check(True)
        self.man_values_menu_item = docs_menu.Append(
            wx.NewId(),
            'man rofi',
            'Show or hide pertinent man rofi info',
            wx.ITEM_CHECK
        )
        self.man_values_menu_item.Check(True)
        menu_bar.Append(docs_menu, '&Docs')
        self.SetMenuBar(menu_bar)
        status_bar = wx.StatusBar(self)
        self.SetStatusBar(status_bar)
        panel = wx.Panel(self)
        notebook = wx.Notebook(panel, style=wx.NB_LEFT)
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
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(notebook, 1, wx.EXPAND)
        panel.SetSizer(sizer)

        self.Bind(wx.EVT_MENU, self.exit, self.exit_menu_item)
        self.Bind(wx.EVT_MENU, self.toggle_display, self.help_values_menu_item)
        self.Bind(wx.EVT_MENU, self.toggle_display, self.man_values_menu_item)

    def toggle_display(self, event):
        if self.help_values_menu_item.Id == event.Id:
            kind = 'help_value'
        elif self.man_values_menu_item.Id == event.Id:
            kind = 'man'
        else:
            kind = None
        if kind:
            pub.sendMessage("toggle_display_%s" % kind, data=event.IsChecked())

    def exit(self, event=None):
        self.GetTopLevelParent().Close()
