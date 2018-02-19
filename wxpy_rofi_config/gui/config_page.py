# coding=utf8

"""This file provides ConfigPage"""

from wx import (
    ALIGN_RIGHT,
    ALL,
    BOTTOM,
    BoxSizer,
    EXPAND,
    FlexGridSizer,
    HORIZONTAL,
    ID_ANY,
    LI_HORIZONTAL,
    Panel,
    StaticLine,
    StaticText,
    TextCtrl,
    TOP,
    VERTICAL,
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
        self.construct_gui()

    def construct_horizontal_rule(self):
        """Adds a horizontal rule to the grid"""
        for _ in range(0, 2):
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
        self.grid_sizer.Add(1, 0, 1, EXPAND)
        sizer = BoxSizer(HORIZONTAL)
        label = HidableAutoWrapStaticText(
            parent=self.scrolled_panel,
            label=u"%s" % value.decode('utf8', 'ignore'),
            kind=kind,
        )
        sizer.Add(label, -1, EXPAND)
        self.grid_sizer.Add(sizer, 1, EXPAND)

    def construct_entry_label(self, value):
        """Creates the primary entry label"""
        label_sizer = BoxSizer(VERTICAL)
        label_sizer.Add(0, 1, 1, EXPAND)
        label = StaticText(
            self.scrolled_panel,
            label=value,
            style=ALIGN_RIGHT
        )
        label_sizer.Add(label, flag=ALIGN_RIGHT)
        label_sizer.Add(0, 1, 1, EXPAND)
        self.grid_sizer.Add(label_sizer, 0, EXPAND)

    def construct_entry_control(self, entry):
        """Creates the primary entry control"""
        current_value = TextCtrl(
            self.scrolled_panel,
            value=str(entry.current),
            size=(-1, -1)
        )
        self.grid_sizer.Add(current_value, -1, EXPAND)

    def construct_entry_rows(self, entry, index=0):
        """Constructs all the necessary rows for a single entry"""
        if index > 0:
            self.construct_horizontal_rule()
        if entry.help_value:
            self.construct_docs_label('help_value', entry.help_value)
        self.construct_entry_label(entry.key_name)
        self.construct_entry_label(entry)
        if entry.man:
            self.construct_docs_label('man', entry.man)

    def construct_gui(self):
        """Constructs the page GUI"""
        self.scrolled_panel = ScrolledPanel(self)
        self.scrolled_panel.SetAutoLayout(1)
        self.scrolled_panel.SetupScrolling()
        self.main_sizer = BoxSizer(HORIZONTAL)
        self.grid_sizer = FlexGridSizer(2, 10, 10)
        for index, entry in enumerate(self.config):
            self.construct_entry_rows(entry, index)
        self.grid_sizer.AddGrowableCol(1, 1)
        scroll_sizer = BoxSizer(HORIZONTAL)
        scroll_sizer.Add(self.grid_sizer, 1, EXPAND | ALL, 10)
        self.scrolled_panel.SetSizer(scroll_sizer)
        self.main_sizer.Add(self.scrolled_panel, 1, EXPAND)
        self.SetSizer(self.main_sizer)
