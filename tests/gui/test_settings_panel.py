# pylint: disable=missing-docstring
# pylint: disable=too-many-instance-attributes

from __future__ import print_function

from unittest import TestCase

from mock import call, MagicMock, patch

from wxpy_rofi_config.gui import SettingsPanel


class SettingsPanelTestCase(TestCase):

    def setUp(self):
        self.patch_wx()
        self.construct_panel()
        self.addCleanup(self.wipe_panel)

    def wipe_panel(self):
        del self.panel

    def patch_wx(self):
        boxsizer_patcher = patch(
            'wxpy_rofi_config.gui.settings_panel.BoxSizer'
        )
        self.mock_boxsizer = boxsizer_patcher.start()
        self.addCleanup(boxsizer_patcher.stop)
        checkbox_patcher = patch(
            'wxpy_rofi_config.gui.settings_panel.CheckBox'
        )
        self.mock_checkbox = checkbox_patcher.start()
        self.addCleanup(checkbox_patcher.stop)
        flexgridsizer_patcher = patch(
            'wxpy_rofi_config.gui.settings_panel.FlexGridSizer'
        )
        self.mock_flexgridsizer = flexgridsizer_patcher.start()
        self.addCleanup(flexgridsizer_patcher.stop)
        font_patcher = patch(
            'wxpy_rofi_config.gui.settings_panel.Font'
        )
        self.mock_font = font_patcher.start()
        self.addCleanup(font_patcher.stop)
        intctrl_patcher = patch(
            'wxpy_rofi_config.gui.settings_panel.IntCtrl'
        )
        self.mock_intctrl = intctrl_patcher.start()
        self.addCleanup(intctrl_patcher.stop)
        scrolledpanel_patcher = patch(
            'wxpy_rofi_config.gui.settings_panel.ScrolledPanel'
        )
        self.mock_scrolledpanel = scrolledpanel_patcher.start()
        self.addCleanup(scrolledpanel_patcher.stop)
        staticline_patcher = patch(
            'wxpy_rofi_config.gui.settings_panel.StaticLine'
        )
        self.mock_staticline = staticline_patcher.start()
        self.addCleanup(staticline_patcher.stop)
        statictext_patcher = patch(
            'wxpy_rofi_config.gui.settings_panel.StaticText'
        )
        self.mock_statictext = statictext_patcher.start()
        self.addCleanup(statictext_patcher.stop)
        systemsettings_patcher = patch(
            'wxpy_rofi_config.gui.settings_panel.SystemSettings'
        )
        self.mock_systemsettings = systemsettings_patcher.start()
        self.addCleanup(systemsettings_patcher.stop)
        textctrl_patcher = patch(
            'wxpy_rofi_config.gui.settings_panel.TextCtrl'
        )
        self.mock_textctrl = textctrl_patcher.start()
        self.addCleanup(textctrl_patcher.stop)

    def construct_panel(self):
        fittedstatictext_patcher = patch(
            'wxpy_rofi_config.gui.settings_panel.FittedStaticText'
        )
        self.mock_fittedstatictext = fittedstatictext_patcher.start()
        self.addCleanup(fittedstatictext_patcher.stop)
        create_main_grid_patcher = patch.object(
            SettingsPanel, 'create_main_grid')
        self.mock_create_main_grid = create_main_grid_patcher.start()
        self.panel = SettingsPanel(None, None)
        create_main_grid_patcher.stop()


class ConstructorUnitTests(SettingsPanelTestCase):

    def test_construction(self):
        self.mock_create_main_grid.assert_called_once()


class CreateMainGridUnitTests(SettingsPanelTestCase):

    @patch.object(SettingsPanel, 'populate_entries')
    @patch.object(SettingsPanel, 'SetSizer')
    @patch.object(SettingsPanel, 'SetupScrolling')
    def test_construction(self, mock_scroll, mock_sizer, mock_populate):
        main_sizer = MagicMock()
        self.mock_boxsizer.return_value = main_sizer
        self.panel.config = None
        mock_holder = MagicMock()
        mock_holder.attach_mock(mock_populate, 'populate_entries')
        mock_holder.attach_mock(mock_sizer, 'SetSizer')
        mock_holder.attach_mock(mock_scroll, 'SetupScrolling')
        mock_holder.assert_not_called()
        self.panel.create_main_grid()
        mock_holder.assert_has_calls([
            call.populate_entries(None),
            call.SetSizer(main_sizer),
            call.SetupScrolling()

        ])


class CreateEntryLabelUnitTests(SettingsPanelTestCase):

    def test_construction(self):
        self.panel.grid_sizer = MagicMock()
        self.mock_boxsizer.assert_not_called()
        self.mock_statictext.assert_not_called()
        self.panel.create_entry_label(MagicMock())
        self.mock_boxsizer.assert_called()
        self.mock_statictext.assert_called()


class CreateEntryControlUnitTests(SettingsPanelTestCase):
    RUNS = [
        [MagicMock(var_type='string'), 'mock_textctrl'],
        [MagicMock(var_type='number'), 'mock_intctrl'],
        [MagicMock(var_type='boolean'), 'mock_checkbox'],
        [MagicMock(var_type='none'), 'mock_statictext']
    ]

    def test_creation(self):
        self.panel.grid_sizer = MagicMock()
        for run in self.RUNS:
            self.panel.create_entry_control(run[0])
            caller = getattr(self, run[1])
            caller.assert_called_once()
            caller.reset_mock()


class CreateEntryManUnitTests(SettingsPanelTestCase):

    def test_creation(self):
        self.panel.grid_sizer = MagicMock()
        self.mock_fittedstatictext.assert_not_called()
        self.mock_boxsizer.assert_not_called()
        self.panel.create_entry_doc(MagicMock())
        self.mock_boxsizer.assert_called()
        self.mock_fittedstatictext.assert_called()


class CreateHorizontalRuleUnitTests(SettingsPanelTestCase):

    def test_creation(self):
        self.panel.grid_sizer = MagicMock()
        self.mock_staticline.assert_not_called()
        self.panel.create_horizontal_rule()
        self.mock_staticline.assert_called()


class CreateEntryRowsUnitTests(SettingsPanelTestCase):

    def setUp(self):
        SettingsPanelTestCase.setUp(self)
        rule_patcher = patch.object(SettingsPanel, 'create_horizontal_rule')
        self.mock_rule = rule_patcher.start()
        self.addCleanup(rule_patcher.stop)
        label_patcher = patch.object(SettingsPanel, 'create_entry_label')
        self.mock_label = label_patcher.start()
        self.addCleanup(label_patcher.stop)
        control_patcher = patch.object(SettingsPanel, 'create_entry_control')
        self.mock_control = control_patcher.start()
        self.addCleanup(control_patcher.stop)
        doc_patcher = patch.object(SettingsPanel, 'create_entry_doc')
        self.mock_doc = doc_patcher.start()
        self.addCleanup(doc_patcher.stop)
        self.mock_layout = MagicMock()
        self.panel.grid_sizer = MagicMock(Layout=self.mock_layout)

        self.mock_holder = MagicMock()
        self.mock_holder.attach_mock(self.mock_rule, 'create_horizontal_rule')
        self.mock_holder.attach_mock(self.mock_label, 'create_entry_label')
        self.mock_holder.attach_mock(self.mock_control, 'create_entry_control')
        self.mock_holder.attach_mock(self.mock_layout, 'Layout')
        self.mock_holder.attach_mock(self.mock_doc, 'create_entry_doc')

    def test_first_help_man(self):
        entry = MagicMock(
            help_value='qqq',
            man='qqq'
        )
        self.panel.create_entry_rows(entry, False)
        self.mock_holder.assert_has_calls([
            call.create_entry_doc(entry, 'help_value'),
            call.create_entry_label(entry),
            call.create_entry_control(entry),
            call.Layout(),
            call.create_entry_doc(entry, 'man')
        ])

    def test_not_first_help_man(self):
        entry = MagicMock(
            help_value='qqq',
            man='qqq'
        )
        self.panel.create_entry_rows(entry, True)
        self.mock_holder.assert_has_calls([
            call.create_horizontal_rule(),
            call.create_horizontal_rule(),
            call.create_entry_doc(entry, 'help_value'),
            call.create_entry_label(entry),
            call.create_entry_control(entry),
            call.Layout(),
            call.create_entry_doc(entry, 'man')
        ])

    def test_first_help_no_man(self):
        entry = MagicMock(
            help_value='qqq',
            man=None,
        )
        self.panel.create_entry_rows(entry, False)
        self.mock_holder.assert_has_calls([
            call.create_entry_doc(entry, 'help_value'),
            call.create_entry_label(entry),
            call.create_entry_control(entry),
            call.Layout(),
        ])

    def test_not_first_help_no_man(self):
        entry = MagicMock(
            help_value='qqq',
            man=None,
        )
        self.panel.create_entry_rows(entry, True)
        self.mock_holder.assert_has_calls([
            call.create_horizontal_rule(),
            call.create_horizontal_rule(),
            call.create_entry_doc(entry, 'help_value'),
            call.create_entry_label(entry),
            call.create_entry_control(entry),
            call.Layout(),
        ])

    def test_first_no_help_man(self):
        entry = MagicMock(
            help_value=None,
            man='qqq',
        )
        self.panel.create_entry_rows(entry, False)
        self.mock_holder.assert_has_calls([
            call.create_entry_label(entry),
            call.create_entry_control(entry),
            call.Layout(),
            call.create_entry_doc(entry, 'man')
        ])

    def test_not_first_no_help_man(self):
        entry = MagicMock(
            help_value=None,
            man='qqq',
        )
        self.panel.create_entry_rows(entry, True)
        self.mock_holder.assert_has_calls([
            call.create_horizontal_rule(),
            call.create_horizontal_rule(),
            call.create_entry_label(entry),
            call.create_entry_control(entry),
            call.Layout(),
            call.create_entry_doc(entry, 'man')
        ])

    def test_not_first_no_help_no_man(self):
        entry = MagicMock(
            help_value=None,
            man=None,
        )
        self.panel.create_entry_rows(entry, True)
        self.mock_holder.assert_has_calls([
            call.create_horizontal_rule(),
            call.create_horizontal_rule(),
            call.create_entry_label(entry),
            call.create_entry_control(entry),
            call.Layout(),
        ])

    def test_first_no_help_no_man(self):
        entry = MagicMock(
            help_value=None,
            man=None,
        )
        self.panel.create_entry_rows(entry, False)
        self.mock_holder.assert_has_calls([
            call.create_entry_label(entry),
            call.create_entry_control(entry),
            call.Layout(),
        ])


class PopulateEntriesUnitTests(SettingsPanelTestCase):
    CONFIG = ['one', 'two', 'three']
    CALLS = [
        call('one', False),
        call('two', True),
        call('three', True),
    ]

    @patch.object(SettingsPanel, 'create_entry_rows')
    def test_calls(self, mock_create):
        mock_create.assert_not_called()
        self.panel.populate_entries(self.CONFIG)
        mock_create.assert_has_calls(self.CALLS)


class ResizeUnitTests(SettingsPanelTestCase):
    MAN_TEXTS_COUNT = 5

    @patch.object(SettingsPanel, 'GetSizer')
    def test_calls(self, mock_sizer):
        mock_resize = MagicMock()
        self.panel.man_texts = []
        for _ in range(0, self.MAN_TEXTS_COUNT):
            self.panel.man_texts.append(MagicMock(resize=mock_resize))
        mock_layout = MagicMock()
        mock_sizer.return_value = MagicMock(Layout=mock_layout)
        self.panel.resize()
        self.assertEquals(mock_resize.call_count, self.MAN_TEXTS_COUNT)
        mock_layout.assert_called_once()
