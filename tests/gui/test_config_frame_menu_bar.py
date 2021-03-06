# pylint: disable=missing-docstring
# pylint: disable=too-many-instance-attributes
# pylint: disable=unused-argument

from __future__ import print_function

from unittest import TestCase

from mock import MagicMock, patch

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
        pub_patcher = patch(
            'wxpy_rofi_config.gui.config_frame_menu_bar.send'
        )
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


class ConstructRofiMenuUnitTests(ConfigFrameMenuBarTestCase):

    @patch.object(ConfigFrameMenuBar, 'Append')
    def test_construction(self, mock_append):
        mock_append.assert_not_called()
        self.assertIsNone(self.menu_bar.launch_menu_item)
        self.menu_bar.construct_rofi_menu()
        mock_append.assert_called_once()
        self.assertIsNotNone(self.menu_bar.launch_menu_item)


class ConstructDocsMenuUnitTests(ConfigFrameMenuBarTestCase):

    def test_construction(self):
        self.mock_new_id.assert_not_called()
        self.assertIsNone(self.menu_bar.help_values_menu_item)
        self.assertIsNone(self.menu_bar.man_values_menu_item)
        self.menu_bar.construct_docs_menu()
        self.assertEqual(
            2,
            self.mock_new_id.call_count
        )
        self.assertIsNotNone(self.menu_bar.help_values_menu_item)
        self.assertIsNotNone(self.menu_bar.man_values_menu_item)


class ConstructPrefsMenuUnitTests(ConfigFrameMenuBarTestCase):

    @patch.object(ConfigFrameMenuBar, 'construct_docs_menu')
    @patch.object(ConfigFrameMenuBar, 'Append')
    def test_construction(self, mock_append, mock_docs):
        mock_docs.assert_not_called()
        mock_append.assert_not_called()
        self.assertIsNone(self.menu_bar.backup_on_menu_item)
        self.menu_bar.construct_prefs_menu()
        mock_append.assert_called_once()
        mock_docs.assert_called_once_with()
        self.assertIsNotNone(self.menu_bar.backup_on_menu_item)


class ConstructGuiUnitTests(ConfigFrameMenuBarTestCase):

    @patch.object(ConfigFrameMenuBar, 'construct_file_menu')
    @patch.object(ConfigFrameMenuBar, 'construct_rofi_menu')
    @patch.object(ConfigFrameMenuBar, 'construct_prefs_menu')
    def test_calls(self, mock_prefs, mock_rofi, mock_file):
        mock_file.assert_not_called()
        mock_rofi.assert_not_called()
        mock_prefs.assert_not_called()
        self.menu_bar.construct_gui()
        mock_file.assert_called_once_with()
        mock_rofi.assert_called_once_with()
        mock_prefs.assert_called_once_with()


class ToggleDisplayUnitTests(ConfigFrameMenuBarTestCase):
    HELP_ID = 47
    MAN_ID = 99

    TESTS = [
        [
            MagicMock(
                Id=HELP_ID,
                IsChecked=MagicMock(return_value=True)
            ),
            True,
            'toggle_display_help_value',
            {'message': True}
        ],
        [
            MagicMock(
                Id=MAN_ID,
                IsChecked=MagicMock(return_value=False)
            ),
            True,
            'toggle_display_man',
            {'message': False}
        ],
        [
            MagicMock(),
            False
        ]
    ]

    def test_parameters(self):
        self.menu_bar.help_values_menu_item = MagicMock(Id=self.HELP_ID)
        self.menu_bar.man_values_menu_item = MagicMock(Id=self.MAN_ID)
        for entry in self.TESTS:
            self.mock_pub.assert_not_called()
            self.menu_bar.toggle_display(entry[0])
            if entry[1]:
                self.mock_pub.assert_called_once_with(entry[2], **entry[3])
            else:
                self.mock_pub.assert_not_called()
            self.mock_pub.reset_mock()


class ExitUnitTests(ConfigFrameMenuBarTestCase):

    @patch.object(ConfigFrameMenuBar, 'GetTopLevelParent')
    def test_call(self, mock_top):
        mock_top.assert_not_called()
        self.menu_bar.exit()
        mock_top.assert_called_once_with()
