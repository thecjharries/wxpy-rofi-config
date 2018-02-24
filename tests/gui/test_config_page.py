# pylint: disable=invalid-name
# pylint: disable=missing-docstring
# pylint: disable=no-member
# pylint: disable=too-many-instance-attributes
# pylint: disable=unused-argument

from __future__ import print_function

from unittest import TestCase

from mock import MagicMock, patch

from wxpy_rofi_config.gui import ConfigPage


class ConfigPageTestCase(TestCase):

    def setUp(self):
        self.patch_wx()
        self.construct_page()
        self.addCleanup(self.wipe_page)

    def wipe_page(self):
        del self.page

    def patch_wx(self):
        boxsizer_patcher = patch(
            'wxpy_rofi_config.gui.config_page.BoxSizer'
        )
        self.mock_boxsizer = boxsizer_patcher.start()
        self.addCleanup(boxsizer_patcher.stop)
        checkbox_patcher = patch(
            'wxpy_rofi_config.gui.config_page.CheckBox'
        )
        self.mock_checkbox = checkbox_patcher.start()
        self.addCleanup(checkbox_patcher.stop)
        flexgridsizer_patcher = patch(
            'wxpy_rofi_config.gui.config_page.FlexGridSizer'
        )
        self.mock_flexgridsizer = flexgridsizer_patcher.start()
        self.addCleanup(flexgridsizer_patcher.stop)
        font_patcher = patch(
            'wxpy_rofi_config.gui.config_page.Font'
        )
        self.mock_font = font_patcher.start()
        self.addCleanup(font_patcher.stop)
        fontinfo_patcher = patch(
            'wxpy_rofi_config.gui.config_page.FontInfo'
        )
        self.mock_fontinfo = fontinfo_patcher.start()
        self.addCleanup(fontinfo_patcher.stop)
        panel_patcher = patch(
            'wxpy_rofi_config.gui.config_page.Panel.__init__'
        )
        self.mock_panel = panel_patcher.start()
        self.addCleanup(panel_patcher.stop)
        scrolledpanel_patcher = patch(
            'wxpy_rofi_config.gui.config_page.ScrolledPanel'
        )
        self.mock_scrolledpanel = scrolledpanel_patcher.start()
        self.addCleanup(scrolledpanel_patcher.stop)
        spinctrl_patcher = patch(
            'wxpy_rofi_config.gui.config_page.SpinCtrl'
        )
        self.mock_spinctrl = spinctrl_patcher.start()
        self.addCleanup(spinctrl_patcher.stop)
        staticline_patcher = patch(
            'wxpy_rofi_config.gui.config_page.StaticLine'
        )
        self.mock_staticline = staticline_patcher.start()
        self.addCleanup(staticline_patcher.stop)
        statictext_patcher = patch(
            'wxpy_rofi_config.gui.config_page.StaticText'
        )
        self.mock_statictext = statictext_patcher.start()
        self.addCleanup(statictext_patcher.stop)
        textctrl_patcher = patch(
            'wxpy_rofi_config.gui.config_page.TextCtrl'
        )
        self.mock_textctrl = textctrl_patcher.start()
        self.addCleanup(textctrl_patcher.stop)

    def construct_page(self):
        construct_gui_patcher = patch.object(ConfigPage, 'construct_gui')
        self.mock_construct_gui = construct_gui_patcher.start()
        self.page = ConfigPage(None, None)
        construct_gui_patcher.stop()
        self.page.grid_sizer = MagicMock()


class ConstructorUnitTests(ConfigPageTestCase):

    def test_calls(self):
        self.mock_panel.assert_called_once()
        self.mock_font.assert_called_once()
        self.mock_fontinfo.assert_called_once()
        self.mock_construct_gui.assert_called_once_with()


class ConstructHorizontalRuleUnitTests(ConfigPageTestCase):

    def test_calls(self):
        self.mock_staticline.assert_not_called()
        self.page.construct_horizontal_rule()
        self.mock_staticline.assert_called_once()


class ConstructDocsLabelUnitTests(ConfigPageTestCase):

    @patch('wxpy_rofi_config.gui.config_page.HidableAutoWrapStaticText')
    def test_calls(self, mock_hidable):
        mock_hidable.assert_not_called()
        self.page.construct_docs_label('man', 'qqq')
        mock_hidable.assert_called_once()


class ConstructEntryLabelUnitTests(ConfigPageTestCase):

    def test_calls(self):
        self.mock_statictext.assert_not_called()
        self.page.construct_entry_label('qqq')
        self.mock_statictext.assert_called_once()


class ConstructEntryControlUnitTests(ConfigPageTestCase):

    CONTROLS = ['checkbox', 'spinctrl', 'textctrl']

    TESTS = [
        [
            MagicMock(
                var_type='string',
                current='qqq'
            ),
            'textctrl'
        ],
        [
            MagicMock(
                var_type='key',
                current='qqq'
            ),
            'textctrl'
        ],
        [
            MagicMock(
                var_type='number',
                current=-1
            ),
            'spinctrl'
        ],
        [
            MagicMock(
                var_type='boolean',
                current=False
            ),
            'checkbox'
        ],
        [
            MagicMock(
                var_type='qqq',
                current='qqq'
            ),
            'textctrl'
        ]
    ]

    def test_calls(self):
        for entry in self.TESTS:
            for control in self.CONTROLS:
                getattr(self, "mock_%s" % control).assert_not_called()
            self.page.construct_entry_control(entry[0])
            for control in self.CONTROLS:
                mock = getattr(self, "mock_%s" % control)
                if control == entry[1]:
                    mock.assert_called_once()
                else:
                    mock.assert_not_called()
                mock.reset_mock()


class ConstructEntryRowUnitTests(ConfigPageTestCase):

    def setUp(self):
        ConfigPageTestCase.setUp(self)
        construct_horizontal_rule_patcher = patch.object(
            ConfigPage,
            'construct_horizontal_rule'
        )
        self.mock_construct_horizontal_rule = construct_horizontal_rule_patcher.start()
        self.addCleanup(construct_horizontal_rule_patcher.stop)
        construct_docs_label_patcher = patch.object(
            ConfigPage,
            'construct_docs_label'
        )
        self.mock_construct_docs_label = construct_docs_label_patcher.start()
        self.addCleanup(construct_docs_label_patcher.stop)
        construct_entry_label_patcher = patch.object(
            ConfigPage,
            'construct_entry_label'
        )
        self.mock_construct_entry_label = construct_entry_label_patcher.start()
        self.addCleanup(construct_entry_label_patcher.stop)
        construct_entry_control_patcher = patch.object(
            ConfigPage,
            'construct_entry_control'
        )
        self.mock_construct_entry_control = construct_entry_control_patcher.start()
        self.addCleanup(construct_entry_control_patcher.stop)
        self.entry = MagicMock(
            key_name='qqq',
            help_value=None,
            man=None
        )

    def test_hr_generation(self):
        self.mock_construct_horizontal_rule.assert_not_called()
        self.page.construct_entry_row(self.entry, 0)
        self.mock_construct_horizontal_rule.assert_not_called()
        self.page.construct_entry_row(self.entry, 1)
        self.mock_construct_horizontal_rule.assert_called_once_with()

    def test_help_value_generation(self):
        self.mock_construct_docs_label.assert_not_called()
        self.page.construct_entry_row(self.entry, 0)
        self.mock_construct_docs_label.assert_not_called()
        self.entry.help_value = 'qqq'
        self.page.construct_entry_row(self.entry, 0)
        self.mock_construct_docs_label.assert_called_once_with(
            'help_value',
            'qqq'
        )

    def test_man_generation(self):
        self.mock_construct_docs_label.assert_not_called()
        self.page.construct_entry_row(self.entry, 0)
        self.mock_construct_docs_label.assert_not_called()
        self.entry.man = 'qqq'
        self.page.construct_entry_row(self.entry, 0)
        self.mock_construct_docs_label.assert_called_once_with(
            'man',
            'qqq'
        )

    def test_label_and_control_generation(self):
        self.mock_construct_entry_label.assert_not_called()
        self.mock_construct_entry_control.assert_not_called()
        self.page.construct_entry_row(self.entry, 0)
        self.mock_construct_entry_label.assert_called_once_with(
            self.entry.key_name
        )
        self.mock_construct_entry_control.assert_called_once_with(self.entry)


class ConstructGuiUnitTests(ConfigPageTestCase):
    CONFIG = ['one', 'two', 'three']

    @patch.object(ConfigPage, 'construct_entry_row')
    @patch.object(ConfigPage, 'SetSizer')
    def test_calls(self, mock_set, mock_construct):
        self.page.config = self.CONFIG
        mock_construct.assert_not_called()
        mock_set.assert_not_called()
        self.page.construct_gui()
        self.assertEqual(
            len(self.CONFIG),
            mock_construct.call_count
        )
        mock_set.assert_called_once()
