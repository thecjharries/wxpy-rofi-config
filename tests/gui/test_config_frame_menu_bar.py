# pylint: disable=missing-docstring
# pylint: disable=too-many-instance-attributes
# pylint: disable=unused-argument

from __future__ import print_function

from unittest import TestCase

from mock import patch

from wxpy_rofi_config.gui import ConfigFrameMenuBar


class ConfigFrameMenuBarTestCase(TestCase):

    def setUp(self):
        self.patch_wx()
        self.construct_menu_bar()
        self.addCleanup(self.wipe_menu_bar)

    def wipe_menu_bar(self):
        del self.menu_bar

    def patch_wx(self):
        menu_patcher = patch('wxpy_rofi_config.gui.config_frame_menu_bar.Menu')
        self.mock_menu = menu_patcher.start()
        self.addCleanup(menu_patcher.stop)
        menu_bar_patcher = patch(
            'wxpy_rofi_config.gui.config_frame_menu_bar.MenuBar.__init__')
        self.mock_menu_bar = menu_bar_patcher.start()
        self.addCleanup(menu_bar_patcher.stop)
        new_id_patcher = patch(
            'wxpy_rofi_config.gui.config_frame_menu_bar.NewId')
        self.mock_new_id = new_id_patcher.start()
        self.addCleanup(new_id_patcher.stop)
        pub_patcher = patch('wxpy_rofi_config.gui.config_frame_menu_bar.pub')
        self.mock_pub = pub_patcher.start()
        self.addCleanup(pub_patcher.stop)

    def construct_menu_bar(self):
        construct_gui_patcher = patch.object(
            ConfigFrameMenuBar,
            'construct_gui'
        )
        self.mock_construct_gui = construct_gui_patcher.start()
        self.menu_bar = ConfigFrameMenuBar()
        construct_gui_patcher.stop()


class ConstructorUnitTests(ConfigFrameMenuBarTestCase):

    def test_construction(self):
        self.mock_menu_bar.assert_called_once()
        self.mock_construct_gui.assert_called_once_with()


class ConstructFileMenuUnitTests(ConfigFrameMenuBarTestCase):

    @patch.object(ConfigFrameMenuBar, 'Append')
    def test_construction(self, mock_append):
        mock_append.assert_not_called()
        self.assertIsNone(self.menu_bar.exit_menu_item)
        self.menu_bar.construct_file_menu()
        mock_append.assert_called_once()
        self.assertIsNotNone(self.menu_bar.exit_menu_item)
