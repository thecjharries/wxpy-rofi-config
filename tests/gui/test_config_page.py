# pylint: disable=missing-docstring
# pylint: disable=too-many-instance-attributes
# pylint: disable=unused-argument

from __future__ import print_function

from unittest import TestCase

from mock import patch

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
        flexgridsizer_patcher = patch(
            'wxpy_rofi_config.gui.config_page.FlexGridSizer'
        )
        self.mock_flexgridsizer = flexgridsizer_patcher.start()
        self.addCleanup(flexgridsizer_patcher.stop)
        panel_patcher = patch(
            'wxpy_rofi_config.gui.config_page.Panel.__init__'
        )
        self.mock_panel = panel_patcher.start()
        self.addCleanup(panel_patcher.stop)
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


class ConstructorUnitTests(ConfigPageTestCase):

    def test_calls(self):
        self.mock_panel.assert_called_once()
        self.mock_construct_gui.assert_called_once_with()
