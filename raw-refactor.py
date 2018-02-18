# coding=utf8
# pylint: disable=W,C,R
# pylint: disable=no-member
import wx
from wx.lib.pubsub import pub
from wx.lib.scrolledpanel import ScrolledPanel
from wx.lib.agw.infobar import AutoWrapStaticText
import wx.lib.mixins.inspection

from wxpy_rofi_config.config import Rofi


class HidableAutoWrapStaticText(AutoWrapStaticText):

    def __init__(self, parent=None, label="", kind='help_value'):
        AutoWrapStaticText.__init__(self, parent, label)
        pub.subscribe(self.toggle_display, "toggle_display_%s" % kind)

    def toggle_display(self, data):
        if data:
            action = 'Show'
        else:
            action = 'Hide'
        if hasattr(self, action):
            getattr(self, action)()
            self.GetParent().GetSizer().Layout()
            # wx.PostEvent(self.GetParent(), wx.SizeEvent((-1, -1)))


class ConfigPage(wx.Panel):

    def __init__(self, parent, config):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        scrolled_panel = ScrolledPanel(self)
        scrolled_panel.SetAutoLayout(1)
        scrolled_panel.SetupScrolling()
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer = wx.FlexGridSizer(2, 10, 10)
        for index, entry in enumerate(config):
            if index > 0:
                for _ in range(0, 2):
                    rule = wx.StaticLine(
                        scrolled_panel,
                        style=wx.LI_HORIZONTAL,
                        size=(-1, 2)
                    )
                    grid_sizer.Add(rule, proportion=1, flag=wx.EXPAND |
                                   wx.TOP | wx.BOTTOM, border=10)
            if entry.help_value:
                grid_sizer.Add(1, 0, 1, wx.EXPAND)
                help_sizer = wx.BoxSizer(wx.HORIZONTAL)
                help_label = HidableAutoWrapStaticText(
                    parent=scrolled_panel,
                    label=u"%s" % entry.help_value.decode('utf8', 'ignore'),
                    kind='help_value',
                )
                help_sizer.Add(help_label, -1, wx.EXPAND)
                grid_sizer.Add(help_sizer, 1, wx.EXPAND)
            label_sizer = wx.BoxSizer(wx.VERTICAL)
            label_sizer.Add(0, 1, 1, wx.EXPAND)
            label = wx.StaticText(
                scrolled_panel,
                label=entry.key_name,
                style=wx.ALIGN_RIGHT
            )
            label_sizer.Add(label, flag=wx.ALIGN_RIGHT)
            label_sizer.Add(0, 1, 1, wx.EXPAND)
            grid_sizer.Add(label_sizer, 0, wx.EXPAND)
            current_value = wx.TextCtrl(
                scrolled_panel,
                value=str(entry.current),
                size=(-1, -1)
            )
            grid_sizer.Add(current_value, -1, wx.EXPAND)
            if entry.man:
                grid_sizer.Add(1, 0, 1, wx.EXPAND)
                man_sizer = wx.BoxSizer(wx.HORIZONTAL)
                man_label = HidableAutoWrapStaticText(
                    parent=scrolled_panel,
                    label=u"%s" % entry.man.decode('utf8', 'ignore'),
                    kind='man',
                )
                man_sizer.Add(man_label, -1, wx.EXPAND)
                grid_sizer.Add(man_sizer, 1, wx.EXPAND)
        grid_sizer.AddGrowableCol(1, 1)
        scroll_sizer = wx.BoxSizer(wx.HORIZONTAL)
        scroll_sizer.Add(grid_sizer, 1, wx.EXPAND | wx.ALL, 10)
        scrolled_panel.SetSizer(scroll_sizer)
        main_sizer.Add(scrolled_panel, 1, wx.EXPAND)
        self.SetSizer(main_sizer)


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


class ConfigApp(wx.App, wx.lib.mixins.inspection.InspectionMixin):

    def OnInit(self):
        self.Init()  # initialize the inspection tool
        frame = ConfigFrame(None, title="rofi Configuration")
        frame.Show()
        self.SetTopWindow(frame)
        return True

runner = ConfigApp()
runner.MainLoop()
