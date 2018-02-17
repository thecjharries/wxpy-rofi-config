# pylint: disable=W,C,R

from collections import OrderedDict
# pylint: disable=no-name-in-module
from wx import (
    BoxSizer,
    EVT_INIT_DIALOG,
    EVT_MENU,
    EXPAND,
    Frame,
    Menu,
    MenuBar,
    NewId,
    Panel,
    PostEvent,
    SizeEvent,
    VERTICAL,
)
# pylint: enable=no-name-in-module

# from wxpy_rofi_config.config import Rofi
from wxpy_rofi_config.gui import SettingsNotebook


class ConfigFrame(Frame):

    def __init__(self, parent):
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
        panel = Panel(self)
        sizer = BoxSizer(VERTICAL)
        self.notebook = SettingsNotebook(panel)
        sizer.Add(self.notebook, -1, EXPAND)
        panel.SetSizer(sizer)
        self.Layout()
        self.Center()

    def create_menu(self):
        menu_bar = MenuBar()
        file_menu = Menu()
        self.save_menu_item = file_menu.Append(NewId(), '&Save\tCtrl+s')
        self.exit_menu_item = file_menu.Append(NewId(), 'E&xit\tCtrl+w')
        menu_bar.Append(file_menu, '&File')
        self.SetMenuBar(menu_bar)

    def bind_events(self):
        self.Bind(EVT_INIT_DIALOG, self.boot)
        self.Bind(EVT_MENU, self.on_save, self.save_menu_item)
        self.Bind(EVT_MENU, self.on_exit, self.exit_menu_item)

    def boot(self):
        PostEvent(self.notebook, SizeEvent((-1, -1)))

    def save(self):
        print('saving')

    def exit(self):
        self.Close()
