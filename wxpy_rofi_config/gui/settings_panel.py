# coding=utf8

"""This file provides the SettingsPanel class"""

# pylint: disable=too-many-ancestors

from wx import (
    ALIGN_RIGHT,
    ALL,
    BoxSizer,
    CheckBox,
    EXPAND,
    FlexGridSizer,
    Font,
    FONTFAMILY_DEFAULT,
    FONTSTYLE_NORMAL,
    FONTWEIGHT_BOLD,
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

from wxpy_rofi_config.gui import FittedStaticText


class SettingsPanel(ScrolledPanel):
    """
    The SettingsPanel contains all of the settings entries for a given settings
    group. It attempts to resize and scroll where possible
    """

    def __init__(self, config, parent):
        ScrolledPanel.__init__(
            self,
            parent=parent,
            size=(-1, -1)
        )
        self.config = config
        self.resizable_texts = []
        self.font = Font(
            12,
            FONTFAMILY_DEFAULT,
            FONTSTYLE_NORMAL,
            FONTWEIGHT_BOLD
        )

        self.create_main_grid()

    def create_main_grid(self):
        """Creates the primary grid and enables scrolling"""
        self.main_sizer = BoxSizer(HORIZONTAL)
        self.grid_sizer = FlexGridSizer(2, 10, 10)
        self.populate_entries(self.config)
        self.grid_sizer.AddGrowableCol(1, 1)
        self.main_sizer.Add(
            self.grid_sizer,
            proportion=1,
            flag=EXPAND | ALL,
            border=10
        )
        self.SetSizer(self.main_sizer)
        self.SetupScrolling()

    def create_entry_label(self, entry):
        """Creates an entry label, which usually contains the setting name"""
        sizer = BoxSizer(VERTICAL)
        text = StaticText(
            self,
            label=entry.key_name + ':',
            style=ALIGN_RIGHT | EXPAND,
        )
        text.SetFont(self.font)
        sizer.Add((0, 0), proportion=1, flag=EXPAND)
        sizer.Add(text, proportion=0, flag=EXPAND)
        sizer.Add((0, 0), proportion=1, flag=EXPAND)
        self.grid_sizer.Add(sizer, proportion=1, flag=EXPAND)

    def create_entry_control(self, entry):
        """Creates an accessible control for the entry"""
        if entry.var_type in ('string', 'mouse', 'key'):
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
        self.grid_sizer.Add(control, proportion=-1, flag=EXPAND)

    def create_entry_doc(self, entry, kind='help_value'):
        """Creates the documentation labels for an entry"""
        self.grid_sizer.Add(
            BoxSizer(HORIZONTAL),
            proportion=1,
            flag=EXPAND
        )
        sizer = BoxSizer(HORIZONTAL)
        text = FittedStaticText(self)
        text.set_label(getattr(entry, kind))
        self.resizable_texts.append(text)
        sizer.Add(text, proportion=-1, flag=EXPAND)
        self.grid_sizer.Add(sizer, proportion=-1, flag=EXPAND)

    def create_horizontal_rule(self):
        """Creates a simple horizontal rule"""
        rule = StaticLine(
            self,
            style=LI_HORIZONTAL,
            size=(-1, 2)
        )
        self.grid_sizer.Add(rule, proportion=1, flag=EXPAND)

    def create_entry_rows(self, entry, not_first=True):
        """
        Creates all the items for a single entry. It creates horizontal rules,
        entry label and control, and documentation where available
        """
        if not_first:
            self.create_horizontal_rule()
            self.create_horizontal_rule()
        if entry.help_value:
            self.create_entry_doc(entry, 'help_value')
        self.create_entry_label(entry)
        self.create_entry_control(entry)
        self.grid_sizer.Layout()
        if entry.man:
            self.create_entry_doc(entry, 'man')

    def populate_entries(self, config):
        """
        Parses all the available config options and generates their content
        """
        not_first = False
        for entry in config:
            self.create_entry_rows(entry, not_first)
            not_first = True

    def resize(self):
        """Forces each man label to resize and redefines its own layout"""
        for resizable_text in self.resizable_texts:
            resizable_text.resize()
        self.GetSizer().Layout()
