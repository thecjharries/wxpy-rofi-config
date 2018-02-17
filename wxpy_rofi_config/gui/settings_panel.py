# pylint: disable=W,C,R

# pylint: disable=no-name-in-module
from wx import (
    ALIGN_RIGHT,
    BoxSizer,
    CheckBox,
    EXPAND,
    FlexGridSizer,
    HORIZONTAL,
    LI_HORIZONTAL,
    StaticLine,
    StaticText,
    SYS_COLOUR_WINDOWTEXT,
    SystemSettings,
    TextCtrl,
    VERTICAL,
)
from wx.lib.scrolledpanel import ScrolledPanel
from wx.lib.intctrl import IntCtrl
# pylint: enable=no-name-in-module

from wxpy_rofi_config.gui import FittedStaticText


class SettingsPanel(ScrolledPanel):

    def __init__(self, config, parent):
        ScrolledPanel.__init__(
            self,
            parent=parent,
            size=(-1, -1)
        )
        self.config = config
        self.man_texts = []
        self.create_main_grid()

    def create_main_grid(self):
        self.main_sizer = BoxSizer(HORIZONTAL)
        self.grid_sizer = FlexGridSizer(2, 10, 10)
        self.populate_entries(self.config)
        self.grid_sizer.AddGrowableCol(1, 1)
        self.main_sizer.Add(self.grid_sizer, -1, EXPAND)
        self.SetSizer(self.main_sizer)
        self.SetupScrolling()

    def create_entry_label(self, entry):
        sizer = BoxSizer(VERTICAL)
        text = StaticText(
            self,
            label=entry.key_name + ':',
            style=ALIGN_RIGHT | EXPAND
        )
        sizer.Add((0, 0), 1, EXPAND)
        sizer.Add(text, 0, EXPAND)
        sizer.Add((0, 0), 1, EXPAND)
        self.grid_sizer.Add(sizer, -1, EXPAND)

    def create_entry_control(self, entry):
        if 'string' == entry.var_type:
            control = TextCtrl(
                self,
                value=entry.current,
                name=entry.key_name,
                size=(-1, -1),
            )
        elif 'number' == entry.var_type:
            control = IntCtrl(
                self,
                value=entry.current,
                name=entry.key_name,
                default_color=SystemSettings().GetColour(SYS_COLOUR_WINDOWTEXT),
                size=(-1, -1),
            )
        elif 'boolean' == entry.var_type:
            control = CheckBox(
                self,
                name=entry.key_name
            )
            control.SetValue(entry.current)
        else:
            control = StaticText(
                self,
                label=entry.current,
                name=entry.key_name,
                size=(-1, -1),
            )
        self.grid_sizer.Add(control, -1, EXPAND)

    def create_entry_man(self, entry):
        self.grid_sizer.Add(BoxSizer(), 1, EXPAND)
        sizer = BoxSizer(HORIZONTAL)
        text = FittedStaticText(self)
        text.SetLabel(entry.man)
        self.man_texts.append(text)
        sizer.Add(text, 1, EXPAND)
        self.grid_sizer.Add(sizer, -1, EXPAND)

    def create_horizontal_rule(self):
        rule = StaticLine(
            self,
            style=LI_HORIZONTAL,
            size=(-1, 2)
        )
        self.grid_sizer.Add(rule, 1, EXPAND)

    def create_entry_rows(self, entry, not_first=True):
        if not_first:
            self.create_horizontal_rule()
            self.create_horizontal_rule()
        self.create_entry_label(entry)
        self.create_entry_control(entry)
        if entry.man:
            self.create_entry_man(entry)

    def populate_entries(self, config):
        not_first = False
        for entry in config:
            self.create_entry_rows(entry, not_first)
            not_first = True

    def resize(self):
        for man_text in self.man_texts:
            man_text.resize()
