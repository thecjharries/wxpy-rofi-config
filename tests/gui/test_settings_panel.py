# pylint: disable=attribute-defined-outside-init
# pylint: disable=missing-docstring
# pylint: disable=too-many-instance-attributes
# pylint: disable=unused-argument

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
