# pylint: disable=missing-docstring
# pylint: disable=too-many-instance-attributes
# pylint: disable=unused-argument

from __future__ import print_function

from unittest import TestCase

from mock import call, MagicMock, patch

from wxpy_rofi_config.gui import ConfigFrame


class ConfigFrameTestCase(TestCase):

    ONE = MagicMock(group='one')
    TWO = MagicMock(group='two')
    THREE = MagicMock(group='two')

    CONFIG = {
        'one': ONE,
        'two': TWO,
        'three': THREE
    }

    GROUPS = {
        'one': [ONE],
        'two': [THREE, TWO]
    }

    NOTEBOOK = MagicMock()

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
        notebook_patcher = patch('wxpy_rofi_config.gui.config_frame.Notebook')
        self.mock_notebook = notebook_patcher.start()
        self.addCleanup(notebook_patcher.stop)
        panel_patcher = patch('wxpy_rofi_config.gui.config_frame.Panel')
        self.mock_panel = panel_patcher.start()
        self.addCleanup(panel_patcher.stop)

    def construct_frame(self):
        construct_config_patcher = patch.object(
            ConfigFrame,
            'construct_config'
        )
        self.mock_construct_config = construct_config_patcher.start()
        construct_gui_patcher = patch.object(
            ConfigFrame,
            'construct_gui'
        )
        self.mock_construct_gui = construct_gui_patcher.start()
        bind_events_patcher = patch.object(
            ConfigFrame,
            'bind_events'
        )
        self.mock_bind_events = bind_events_patcher.start()
        self.frame = ConfigFrame(None)
        bind_events_patcher.stop()
        construct_gui_patcher.stop()
        construct_config_patcher.stop()


class ConstructorUnitTests(ConfigFrameTestCase):

    def test_calls(self):
        self.mock_construct_config.assert_called_once()
        self.mock_construct_gui.assert_called_once()
        self.mock_bind_events.assert_called_once()


class ConstructConfigUnitTests(ConfigFrameTestCase):

    @patch('wxpy_rofi_config.gui.config_frame.Rofi')
    def test_construction(self, mock_rofi):
        mock_rofi.assert_not_called()
        self.frame.construct_config()
        mock_rofi.assert_called_once_with()

    @patch(
        'wxpy_rofi_config.gui.config_frame.Rofi',
        return_value=MagicMock(
            config=ConfigFrameTestCase.CONFIG
        )
    )
    def test_grouping(self, mock_rofi):
        self.frame.construct_config()
        self.assertDictEqual(
            self.frame.groups,
            self.GROUPS
        )


class ConstructTabsUnitTests(ConfigFrameTestCase):

    def setUp(self):
        ConfigFrameTestCase.setUp(self)
        self.frame.groups = self.GROUPS
        self.frame.notebook = self.NOTEBOOK

    @patch('wxpy_rofi_config.gui.config_frame.ConfigPage')
    def test_page_construction(self, mock_page):
        self.frame.construct_tabs()
        mock_page.assert_has_calls([
            call(self.NOTEBOOK, [self.THREE, self.TWO]),
            call(self.NOTEBOOK, [self.ONE]),
        ])
