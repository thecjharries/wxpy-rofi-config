# coding=utf8

"""This file provides ConfigFrame"""

# pylint: disable=too-many-ancestors

from wx import (
    BoxSizer,
    EVT_MENU,
    EXPAND,
    FindWindowByName,
    Frame,
    HORIZONTAL,
    ID_ANY,
    NB_LEFT,
    Notebook,
    Panel,
)
from wx.lib.pubsub import pub

from wxpy_rofi_config.config import Rofi
from wxpy_rofi_config.gui import (
    ConfigFrameMenuBar,
    ConfigFrameStatusBar,
    ConfigPage
)


class ConfigFrame(Frame):
    """ConfigFrame is used as the primary app context"""

    config = None
    groups = None
    menu_bar = None
    notebook = None

    def __init__(self, parent, title=""):
        Frame.__init__(
            self,
            parent=parent,
            id=ID_ANY,
            size=(800, 640),
            title=title
        )
        self.construct_config()
        self.construct_gui()
        self.bind_events()

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

    def construct_tabs(self):
        """Constructs all available tabs"""
        for key, config_list in self.groups.items():
            page = ConfigPage(self.notebook, config_list)
            self.notebook.AddPage(page, key)

    def construct_notebook(self):
        """Constructs the main Notebook panel"""
        panel = Panel(self)
        self.notebook = Notebook(panel, style=NB_LEFT)
        self.construct_tabs()
        sizer = BoxSizer(HORIZONTAL)
        sizer.Add(self.notebook, 1, EXPAND)
        panel.SetSizer(sizer)

    def construct_gui(self):
        """Constructs ConfigFrame's GUI"""
        self.menu_bar = ConfigFrameMenuBar()
        self.SetMenuBar(self.menu_bar)
        self.status_bar = ConfigFrameStatusBar(self)
        self.SetStatusBar(self.status_bar)
        self.construct_notebook()

    def bind_events(self):
        """Binds events on ConfigFrame"""
        self.Bind(
            EVT_MENU,
            self.save,
            self.menu_bar.save_menu_item
        )
        self.Bind(
            EVT_MENU,
            self.menu_bar.exit,
            self.menu_bar.exit_menu_item
        )
        self.Bind(
            EVT_MENU,
            self.modi_launcher,
            self.menu_bar.launch_menu_item
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

    def modi_launcher(self, event=None):  # pylint: disable=unused-argument
        """Launches a modi selection dialog"""
        print(event)
        print(self)

    def update_config_entry(self, key_name, entry):
        """Updates the value for a single entry"""
        widget = FindWindowByName(key_name)
        if hasattr(widget, 'GetValue'):
            value = widget.GetValue()
        elif hasattr(widget, 'GetLabel'):
            value = widget.GetLabel()
        else:
            value = entry.current
        self.config.config[key_name].current = value

    def update_config(self):
        """Updates the entire config object"""
        for key_name, entry in self.config.config.items():
            self.update_config_entry(key_name, entry)

    def save(self, event=None):  # pylint: disable=unused-argument
        """Saves the config file"""
        self.update_config()
        self.config.save(backup=self.menu_bar.backup_on_menu_item.IsChecked())
        pub.sendMessage('status_update', data='Saved!')
