# coding=utf8

"""This file provides ConfigPage"""

from wx import (
    ALIGN_LEFT,
    ALL,
    BOTTOM,
    BoxSizer,
    CheckBox,
    EXPAND,
    FlexGridSizer,
    Font,
    FontInfo,
    HORIZONTAL,
    ID_ANY,
    LI_HORIZONTAL,
    Panel,
    SpinCtrl,
    StaticLine,
    StaticText,
    TextCtrl,
    TOP,
)
from wx.lib.scrolledpanel import ScrolledPanel

from wxpy_rofi_config.gui import HidableAutoWrapStaticText


class ConfigPage(Panel):
    """ConfigPage holds the GUI for a single tab pane"""

    config = None
    grid_sizer = None
    main_sizer = None
    scrolled_panel = None

    def __init__(self, parent, config):
        Panel.__init__(self, parent=parent, id=ID_ANY)
        self.config = config
        self.header_font = Font(FontInfo(24).Bold())
        self.construct_gui()

    def construct_horizontal_rule(self):
        """Adds a horizontal rule to the grid"""
        rule = StaticLine(
            self.scrolled_panel,
            style=LI_HORIZONTAL,
            size=(-1, 2)
        )
        self.grid_sizer.Add(
            rule,
            proportion=1,
            flag=EXPAND | TOP | BOTTOM,
            border=10
        )

    def construct_docs_label(self, kind, value):
        """Constructs a documentation label"""
        sizer = BoxSizer(HORIZONTAL)
        label = HidableAutoWrapStaticText(
            parent=self.scrolled_panel,
            label=value,
            kind=kind,
        )
        sizer.Add(label, -1, EXPAND)
        self.grid_sizer.Add(sizer, -1, EXPAND)

    def construct_entry_label(self, value):
        """Creates the primary entry label"""
        sizer = BoxSizer(HORIZONTAL)
        label = StaticText(
            self.scrolled_panel,
            label=value,
            style=ALIGN_LEFT
        )
        label.SetFont(self.header_font)
        sizer.Add(label, -1, EXPAND)
        self.grid_sizer.Add(sizer, -1, EXPAND)

    def construct_entry_control(self, entry):
        """Creates the primary entry control"""
        if 'boolean' == entry.var_type:
            control = CheckBox(
                self.scrolled_panel,
                name=entry.key_name
            )
            control.SetValue(entry.current)
        elif 'number' == entry.var_type:
            control = SpinCtrl(
                self.scrolled_panel,
                name=entry.key_name,
            )
            control.SetValue(entry.current)
        else:
            control = TextCtrl(
                self.scrolled_panel,
                value=str(entry.current),
                name=entry.key_name,
                size=(-1, -1)
            )
        self.grid_sizer.Add(control, -1, EXPAND)

    def construct_entry_row(self, entry, index=0):
        """Constructs all the necessary rows for a single entry"""
        if index > 0:
            self.construct_horizontal_rule()
        self.construct_entry_label(entry.key_name)
        if entry.help_value:
            self.construct_docs_label('help_value', entry.help_value)
        self.construct_entry_control(entry)
        if entry.man:
            self.construct_docs_label('man', entry.man)

    def construct_gui(self):
        """Constructs the page GUI"""
        self.scrolled_panel = ScrolledPanel(self)
        self.scrolled_panel.SetAutoLayout(1)
        self.scrolled_panel.SetupScrolling()
        self.main_sizer = BoxSizer(HORIZONTAL)
        self.grid_sizer = FlexGridSizer(1, 10, 10)
        for index, entry in enumerate(self.config):
            self.construct_entry_row(entry, index)
        self.grid_sizer.AddGrowableCol(0, 1)
        scroll_sizer = BoxSizer(HORIZONTAL)
        scroll_sizer.Add(self.grid_sizer, 1, EXPAND | ALL, 10)
        self.scrolled_panel.SetSizer(scroll_sizer)
        self.main_sizer.Add(self.scrolled_panel, 1, EXPAND)
        self.SetSizer(self.main_sizer)
