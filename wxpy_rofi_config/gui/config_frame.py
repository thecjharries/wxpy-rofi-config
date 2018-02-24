# coding=utf8

"""This file provides ConfigFrame"""

# pylint: disable=too-many-ancestors

from os.path import dirname
from pydispatch.dispatcher import send
from wx import (
    BoxSizer,
    EVT_CHECKBOX,
    EVT_MENU,
    EVT_SPINCTRL,
    EVT_TEXT,
    EXPAND,
    FD_FILE_MUST_EXIST,
    FD_OPEN,
    FD_OVERWRITE_PROMPT,
    FD_SAVE,
    FileDialog,
    FindWindowByName,
    Frame,
    HORIZONTAL,
    ICON_QUESTION,
    ID_ANY,
    ID_OK,
    ID_YES,
    MessageDialog,
    NB_LEFT,
    Notebook,
    Panel,
    YES_NO,
)

from wxpy_rofi_config.config import Rofi
from wxpy_rofi_config.gui import (
    ConfigFrameMenuBar,
    ConfigFrameStatusBar,
    ConfigPage,
    ModiLauncher
)


class ConfigFrame(Frame):  # pylint: disable=too-many-public-methods
    """ConfigFrame is used as the primary app context"""

    BOUND_ACTIONS = 12

    PROMPTS = {
        'dirty_values': 'You have unsaved changes. ',
        'probably_modified': 'File has been modified. '
    }

    config = None
    dirty_values = []
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

    def construct_config(self, config_path=None):
        """Constucts the Rofi config object and parses its groups"""
        self.config = Rofi()
        self.config.build(config_path)
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
        self.clean_edit_state()

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
        self.toggle_restoration()

    def bind_events(self):
        """Binds events on ConfigFrame"""
        self.Bind(
            EVT_MENU,
            self.open,
            self.menu_bar.open_menu_item
        )
        self.Bind(
            EVT_MENU,
            self.force_refresh_config,
            self.menu_bar.refresh_menu_item
        )
        self.Bind(
            EVT_MENU,
            self.restore,
            self.menu_bar.restore_menu_item
        )
        self.Bind(
            EVT_MENU,
            self.save_as,
            self.menu_bar.save_as_menu_item
        )
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
        self.Bind(EVT_CHECKBOX, self.dirty_edit_state)
        self.Bind(EVT_SPINCTRL, self.dirty_edit_state)
        self.Bind(EVT_TEXT, self.dirty_edit_state)

    def modi_launcher(self, event=None):  # pylint: disable=unused-argument
        """Launches a modi selection dialog"""
        ModiLauncher(self.config.available_modi)

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
        send('status_update', message='Saved!')
        self.clean_edit_state()
        self.toggle_refresh()
        self.toggle_restoration()

    def toggle_restoration(self, event=None):  # pylint: disable=unused-argument
        """Enables/disables the restore menu item"""
        self.menu_bar.restore_menu_item.Enable(self.config.can_restore())

    def refresh_config(self, event=None, config_path=None):  # pylint: disable=unused-argument
        """Refreshes the config object and controls"""
        current_page = self.notebook.GetSelection()
        self.construct_config(config_path)
        while self.notebook.GetPageCount() > 0:
            self.notebook.DeletePage(0)
        self.construct_tabs()
        if current_page >= 0 and current_page < self.notebook.GetPageCount():
            self.notebook.SetSelection(current_page)
        self.toggle_refresh()
        self.toggle_restoration()

    def restore(self, event=None):  # pylint: disable=unused-argument
        """Restores a previously backed up config"""
        if self.config.can_restore():
            self.config.backup(restore=True)
            self.refresh_config()

    def clean_edit_state(self):
        """Resets the dirty value list"""
        self.dirty_values = []

    def dirty_edit_state(self, event=None):
        """Updates the dirty value list"""
        if event is None:
            return
        control_value = event.EventObject.GetValue()
        control_name = event.EventObject.GetName()
        config_value = self.config.config[control_name].current
        is_dirty = control_value != config_value
        if is_dirty:
            if not control_name in self.dirty_values:
                self.dirty_values.append(control_name)
        else:
            self.dirty_values = [
                key
                for key in self.dirty_values
                if control_name != key
            ]
        self.toggle_refresh()

    def toggle_refresh(self):
        """Toggle refresh availability"""
        self.menu_bar.refresh_menu_item.Enable(
            len(self.dirty_values) > 0
            or
            self.config.probably_modified()
        )

    @staticmethod
    def ignore_dirty_state(prompt=None):
        """Checks if dirty state can be abandoned"""
        with MessageDialog(
            None,
            "%sContinue?" % prompt,
            'Confirm overwrite',
            YES_NO | ICON_QUESTION
        ) as dialog:
            if ID_YES == dialog.ShowModal():
                return True
        return False

    def force_refresh_config(self, event=None):  # pylint: disable=unused-argument
        """Forces a config refresh"""
        if self.dirty_values:
            if self.ignore_dirty_state(self.PROMPTS['dirty_values']):
                self.refresh_config()
        elif self.config.probably_modified():
            if self.ignore_dirty_state(self.PROMPTS['probably_modified']):
                self.refresh_config()

    def file_dialog(self, style=None):
        """Opens a dialog to find a file"""
        with FileDialog(
            None,
            'Choose a file',
            dirname(self.config.active_file),
            wildcard='Rasi files (*.rasi)|*.rasi|All Files (*.*)|*.*',
            style=style
        ) as dialog:
            if ID_OK == dialog.ShowModal():
                return dialog.GetPath()
        return None

    def pick_save_file(self):
        """Launches a dialog to pick the save location"""
        return self.file_dialog(FD_SAVE | FD_OVERWRITE_PROMPT)

    def save_as(self, event=None):  # pylint: disable=unused-argument
        """Saves the config as an arbitrary file"""
        new_location = self.pick_save_file()
        if new_location:
            self.config.active_file = new_location
        self.save()

    def pick_open_file(self):
        """Launches a dialog to pick the open location"""
        return self.file_dialog(FD_OPEN | FD_FILE_MUST_EXIST)

    def open(self, event=None):  # pylint: disable=unused-argument
        """Opens the chosen config for editing"""
        new_location = self.pick_open_file()
        if new_location:
            self.refresh_config(config_path=new_location)
