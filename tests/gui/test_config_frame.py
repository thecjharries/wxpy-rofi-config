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
        findwindow_patcher = patch(
            'wxpy_rofi_config.gui.config_frame.FindWindowByName'
        )
        self.mock_findwindow = findwindow_patcher.start()
        self.addCleanup(findwindow_patcher.stop)
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


class ConstructNotebookUnitTests(ConfigFrameTestCase):

    @patch.object(ConfigFrame, 'construct_tabs')
    def test_construction(self, mock_tabs):
        self.mock_notebook.assert_not_called()
        mock_tabs.assert_not_called()
        self.frame.construct_notebook()
        self.mock_notebook.assert_called_once()
        mock_tabs.assert_called_once()


class ConstructGuiUnitTests(ConfigFrameTestCase):

    MENU_BAR = MagicMock()
    STATUS_BAR = MagicMock()

    @patch(
        'wxpy_rofi_config.gui.config_frame.ConfigFrameMenuBar',
        return_value=MENU_BAR
    )
    @patch.object(ConfigFrame, 'SetMenuBar')
    @patch(
        'wxpy_rofi_config.gui.config_frame.ConfigFrameStatusBar',
        return_value=STATUS_BAR
    )
    @patch.object(ConfigFrame, 'SetStatusBar')
    @patch.object(ConfigFrame, 'construct_notebook')
    def test_construction(  # pylint: disable=too-many-arguments
            self,
            mock_notebook,
            mock_set_status,
            mock_status,
            mock_set_menu,
            mock_menu,
    ):
        mock_holder = MagicMock()
        mock_holder.attach_mock(mock_menu, 'ConfigFrameMenuBar')
        mock_holder.attach_mock(mock_set_menu, 'SetMenuBar')
        mock_holder.attach_mock(mock_status, 'ConfigFrameStatusBar')
        mock_holder.attach_mock(mock_set_status, 'SetStatusBar')
        mock_holder.attach_mock(mock_notebook, 'construct_notebook')
        mock_holder.assert_not_called()
        self.frame.construct_gui()
        print(mock_holder.mock_calls)
        mock_holder.assert_has_calls(
            [
                call.ConfigFrameMenuBar(),
                call.SetMenuBar(self.MENU_BAR),
                call.ConfigFrameStatusBar(self.frame),
                call.SetStatusBar(self.STATUS_BAR),
                call.construct_notebook()
            ],
            True
        )


class BindEventsUnitTests(ConfigFrameTestCase):
    MENU_BAR = MagicMock()

    @patch.object(ConfigFrame, 'Bind')
    def test_binds(self, mock_bind):
        self.frame.menu_bar = self.MENU_BAR
        mock_bind.assert_not_called()
        self.frame.bind_events()
        self.assertEqual(
            4,
            mock_bind.call_count
        )


class UpdateConfigEntryUnitTests(ConfigFrameTestCase):
    KEY_NAME = 'qqq'
    PRE = 9
    VALUE = 10
    LABEL = 12
    CURRENT = 13

    def setUp(self):
        ConfigFrameTestCase.setUp(self)
        self.frame.config = MagicMock(
            config={
                self.KEY_NAME: MagicMock(current=self.PRE)
            }
        )

    def test_with_value(self):
        self.mock_findwindow.return_value = MagicMock(
            spec=['GetValue'],
            GetValue=MagicMock(return_value=self.VALUE)
        )
        self.assertEqual(
            self.PRE,
            self.frame.config.config[self.KEY_NAME].current
        )
        self.frame.update_config_entry(self.KEY_NAME, MagicMock())
        self.assertEqual(
            self.VALUE,
            self.frame.config.config[self.KEY_NAME].current
        )

    def test_with_label(self):
        self.mock_findwindow.return_value = MagicMock(
            spec=['GetLabel'],
            GetLabel=MagicMock(return_value=self.LABEL)
        )
        self.assertEqual(
            self.PRE,
            self.frame.config.config[self.KEY_NAME].current
        )
        self.frame.update_config_entry(self.KEY_NAME, MagicMock())
        self.assertEqual(
            self.LABEL,
            self.frame.config.config[self.KEY_NAME].current
        )

    def test_with_current(self):
        self.mock_findwindow.return_value = MagicMock(spec=[])
        self.assertEqual(
            self.PRE,
            self.frame.config.config[self.KEY_NAME].current
        )
        self.frame.update_config_entry(
            self.KEY_NAME,
            MagicMock(current=self.CURRENT)
        )
        self.assertEqual(
            self.CURRENT,
            self.frame.config.config[self.KEY_NAME].current
        )
