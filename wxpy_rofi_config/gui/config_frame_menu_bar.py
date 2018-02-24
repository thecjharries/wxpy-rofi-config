# coding=utf8

"""This file provides ConfigFrameMenuBar"""

# pylint: disable=too-many-ancestors

from wx import (
    ID_EXIT,
    ID_OPEN,
    ID_SAVE,
    ID_SAVEAS,
    ITEM_CHECK,
    Menu,
    MenuBar,
    NewId,
)
from pydispatch.dispatcher import send


class ConfigFrameMenuBar(MenuBar):  # pylint:disable=too-many-instance-attributes
    """ConfigFrameMenuBar collects menu construction and actions"""
    backup_on_menu_item = None
    exit_menu_item = None
    help_values_menu_item = None
    launch_menu_item = None
    man_values_menu_item = None
    open_menu_item = None
    refresh_menu_item = None
    restore_menu_item = None
    save_menu_item = None
    save_as_menu_item = None

    def __init__(self):
        MenuBar.__init__(self)
        self.construct_gui()

    def construct_file_menu(self):
        """Constructs the file menu"""
        file_menu = Menu()
        self.open_menu_item = file_menu.Append(
            ID_OPEN,
            '&Open File\tCtrl+o'
        )
        self.refresh_menu_item = file_menu.Append(
            NewId(),
            '&Refresh Config\tCtrl+r'
        )
        self.refresh_menu_item.Enable(False)
        self.restore_menu_item = file_menu.Append(
            NewId(),
            'Restore Backup Config'
        )
        self.restore_menu_item.Enable(False)
        self.save_as_menu_item = file_menu.Append(
            ID_SAVEAS,
            'Save As\tCtrl+Shift+s'
        )
        self.save_menu_item = file_menu.Append(
            ID_SAVE,
            '&Save\tCtrl+s'
        )
        self.exit_menu_item = file_menu.Append(
            ID_EXIT,
            'E&xit\tCtrl+w'
        )
        self.Append(file_menu, '&File')

    def construct_rofi_menu(self):
        """Creates the Rofi menu"""
        rofi_menu = Menu()
        self.launch_menu_item = rofi_menu.Append(
            NewId(),
            '&Launch Modi\tCtrl+t',
            'Launch any available modi'
        )
        self.Append(rofi_menu, '&Rofi')

    def construct_docs_menu(self):
        """Constructs the docs menu"""
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
        return docs_menu

    def construct_prefs_menu(self):
        """Creates the preferences menu"""
        prefs_menu = Menu()
        self.backup_on_menu_item = prefs_menu.Append(
            NewId(),
            'Backup pre save',
            'Backs up the existing config before saving',
            ITEM_CHECK
        )
        self.backup_on_menu_item.Check(True)
        prefs_menu.AppendSubMenu(self.construct_docs_menu(), '&Docs')
        self.Append(prefs_menu, '&Preferences')

    def construct_gui(self):
        """Construct the MenuBar GUI"""
        self.construct_file_menu()
        self.construct_rofi_menu()
        self.construct_prefs_menu()

    def toggle_display(self, event):
        """Publishes show/hide messages via pub"""
        if self.help_values_menu_item.Id == event.Id:
            kind = 'help_value'
        elif self.man_values_menu_item.Id == event.Id:
            kind = 'man'
        else:
            kind = None
        if kind:
            send("toggle_display_%s" % kind, message=event.IsChecked())

    def exit(self, event=None):  # pylint: disable=unused-argument
        """Kills the app"""
        self.GetTopLevelParent().Close()
