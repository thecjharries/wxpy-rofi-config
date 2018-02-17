# pylint: disable=attribute-defined-outside-init
# pylint: disable=missing-docstring
# pylint: disable=too-many-instance-attributes
# pylint: disable=unused-argument

from __future__ import print_function

from unittest import TestCase

from mock import call, MagicMock, patch

from wxpy_rofi_config.gui import ConfigFrame


class ConfigFrameTestCase(TestCase):

    def setUp(self):
        self.patch_wx()
        self.construct_frame()
        self.addCleanup(self.wipe_frame)

    def wipe_frame(self):
        del self.frame

    def patch_wx(self):
        boxsizer_patcher = patch('wxpy_rofi_config.gui.config_frame.BoxSizer')
        self.mock_boxsizer = boxsizer_patcher.start()
        self.addCleanup(boxsizer_patcher.stop)
        frame_patcher = patch('wxpy_rofi_config.gui.config_frame.Frame')
        self.mock_frame = frame_patcher.start()
        self.addCleanup(frame_patcher.stop)
        menu_patcher = patch('wxpy_rofi_config.gui.config_frame.Menu')
        self.mock_menu = menu_patcher.start()
        self.addCleanup(menu_patcher.stop)
        menubar_patcher = patch('wxpy_rofi_config.gui.config_frame.MenuBar')
        self.mock_menubar = menubar_patcher.start()
        self.addCleanup(menubar_patcher.stop)
        newid_patcher = patch('wxpy_rofi_config.gui.config_frame.NewId')
        self.mock_newid = newid_patcher.start()
        self.addCleanup(newid_patcher.stop)
        panel_patcher = patch('wxpy_rofi_config.gui.config_frame.Panel')
        self.mock_panel = panel_patcher.start()
        self.addCleanup(panel_patcher.stop)

    def construct_frame(self):
        settings_notebook_patcher = patch(
            'wxpy_rofi_config.gui.config_frame.SettingsNotebook')
        self.mock_settings_notebook = settings_notebook_patcher.start()
        self.addCleanup(settings_notebook_patcher.stop)
        create_menu_patcher = patch.object(ConfigFrame, 'create_menu')
        self.mock_create_menu = create_menu_patcher.start()
        create_panel_patcher = patch.object(ConfigFrame, 'create_panel')
        self.mock_create_panel = create_panel_patcher.start()
        bind_events_patcher = patch.object(ConfigFrame, 'bind_events')
        self.mock_bind_events = bind_events_patcher.start()
        self.frame = ConfigFrame()
        create_menu_patcher.stop()
        create_panel_patcher.stop()
        bind_events_patcher.stop()


class ConstructorUnitTests(ConfigFrameTestCase):

    def test_calls(self):
        self.mock_create_menu.assert_called_once()
        self.mock_create_panel.assert_called_once()
        self.mock_bind_events.assert_called_once()


class CreatePanelUnitTests(ConfigFrameTestCase):

    @patch.object(ConfigFrame, 'Layout')
    @patch.object(ConfigFrame, 'Center')
    def test_construction(self, mock_center, mock_layout):
        self.frame.create_panel()
        mock_center.assert_called_once()
        mock_layout.assert_called_once()


class CreateMenuUnitTests(ConfigFrameTestCase):

    @patch.object(ConfigFrame, 'SetMenuBar')
    def test_construction(self, mock_set):
        self.frame.create_menu()
        mock_set.assert_called_once()

    @patch.object(ConfigFrame, 'SetMenuBar')
    def test_menu_creation(self, mock_set):
        self.assertIsNone(getattr(self.frame, 'save_menu_item', None))
        self.assertIsNone(getattr(self.frame, 'exit_menu_item', None))
        self.frame.create_menu()
        self.assertIsNotNone(self.frame.save_menu_item)
        self.assertIsNotNone(self.frame.exit_menu_item)
