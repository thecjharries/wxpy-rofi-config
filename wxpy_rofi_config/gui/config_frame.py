# coding=utf8

"""This file provides the ConfigFrame class"""

# pylint:disable=too-many-ancestors

from wx import (
    BoxSizer,
    EVT_INIT_DIALOG,
    EVT_MENU,
    EXPAND,
    Frame,
    ITEM_CHECK,
    Menu,
    MenuBar,
    NewId,
    Panel,
    PostEvent,
    SizeEvent,
    VERTICAL,
)


# from wxpy_rofi_config.config import Rofi
from wxpy_rofi_config.gui import SettingsNotebook


class ConfigFrame(Frame):
    """ConfigFrame is responsible for booting the app and running its menus"""

    def __init__(self):
        Frame.__init__(
            self,
            None,
            title='rofi Config',
            size=(600, 600)
        )
        self.create_menu()
        self.create_panel()
        self.bind_events()

    def create_panel(self):
        """Creates the main app panel"""
        panel = Panel(self)
        sizer = BoxSizer(VERTICAL)
        self.notebook = SettingsNotebook(panel)
        sizer.Add(self.notebook, -1, EXPAND)
        panel.SetSizer(sizer)
        self.Layout()
        self.Center()

    def create_menu(self):
        """Creates the app menu"""
        menu_bar = MenuBar()
        file_menu = Menu()
        self.save_menu_item = file_menu.Append(NewId(), '&Save\tCtrl+s')
        self.exit_menu_item = file_menu.Append(NewId(), 'E&xit\tCtrl+w')
        menu_bar.Append(file_menu, '&File')
        self.SetMenuBar(menu_bar)

    def bind_events(self):
        """Binds all useful events"""
        self.Bind(EVT_INIT_DIALOG, self.boot)
        self.Bind(EVT_MENU, self.save, self.save_menu_item)
        self.Bind(EVT_MENU, self.exit, self.exit_menu_item)

    def boot(self, event=None):  # pylint:disable=unused-argument
        """Sends a resize request to app to coddle StaticTexts"""
        PostEvent(self.notebook, SizeEvent((-1, -1)))

    def save(self, event=None):  # pylint:disable=unused-argument
        """Fires a save event"""
        self.notebook.save()

    def exit(self, event=None):  # pylint:disable=unused-argument
        """Exits the app"""
        self.Close()
