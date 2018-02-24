# pylint: disable=missing-docstring
# pylint: disable=too-many-instance-attributes
# pylint: disable=unused-argument

from __future__ import print_function

from collections import OrderedDict
from unittest import TestCase

from mock import call, MagicMock, patch

from wxpy_rofi_config.gui import ConfigFrame


class ConfigFrameTestCase(TestCase):

    ONE = MagicMock(group='one')
    TWO = MagicMock(group='two')
    THREE = MagicMock(group='two')

    CONFIG = OrderedDict()
    CONFIG['one'] = ONE
    CONFIG['two'] = TWO
    CONFIG['three'] = THREE
    # {
    #     'one': ONE,
    #     'two': TWO,
    #     'three': THREE
    # }

    GROUPS = OrderedDict()
    GROUPS['one'] = [ONE]
    GROUPS['two'] = [TWO, THREE]
    # {
    #     'one': [ONE],
    #     'two': [TWO, THREE]
    # }

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
        for group_key in self.GROUPS:
            for index, value in enumerate(self.GROUPS[group_key]):
                self.assertEqual(
                    value,
                    self.frame.groups[group_key][index]
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
            call(self.NOTEBOOK, [self.ONE]),
            call(self.NOTEBOOK, [self.TWO, self.THREE]),
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
    @patch.object(ConfigFrame, 'toggle_restoration')
    def test_construction(  # pylint: disable=too-many-arguments
            self,
            mock_restoration,
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
        mock_holder.attach_mock(mock_restoration, 'toggle_restoration')
        mock_holder.assert_not_called()
        self.frame.construct_gui()
        print(mock_holder.mock_calls)
        mock_holder.assert_has_calls(
            [
                call.ConfigFrameMenuBar(),
                call.SetMenuBar(self.MENU_BAR),
                call.ConfigFrameStatusBar(self.frame),
                call.SetStatusBar(self.STATUS_BAR),
                call.construct_notebook(),
                call.toggle_restoration()
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
            ConfigFrame.BOUND_ACTIONS,
            mock_bind.call_count
        )


class ModiLauncherUnitTests(ConfigFrameTestCase):
    MODI = ['one', 'two']

    @patch('wxpy_rofi_config.gui.config_frame.ModiLauncher')
    def test_construction(self, mock_modi):
        self.frame.config = MagicMock(available_modi=self.MODI)
        mock_modi.assert_not_called()
        self.frame.modi_launcher()
        mock_modi.assert_called_once_with(self.MODI)


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


class UpdateConfigUnitTests(ConfigFrameTestCase):
    CONFIG = OrderedDict()
    CONFIG['one'] = 'one entry'
    CONFIG['two'] = 'two entry'
    CONFIG['three'] = 'three entry'

    CALLS = [
        call('one', 'one entry'),
        call('two', 'two entry'),
        call('three', 'three entry'),
    ]

    @patch.object(ConfigFrame, 'update_config_entry')
    def test_calls(self, mock_update):
        self.frame.config = MagicMock(config=self.CONFIG)
        mock_update.assert_not_called()
        self.frame.update_config()
        mock_update.assert_has_calls(self.CALLS)


class SaveUnitTests(ConfigFrameTestCase):

    @patch.object(ConfigFrame, 'update_config')
    def test_calls(self, mock_update):
        for backup in [True, False]:
            mock_save = MagicMock()
            self.frame.config = MagicMock(save=mock_save)
            self.frame.menu_bar = MagicMock(
                backup_on_menu_item=MagicMock(
                    IsChecked=MagicMock(
                        return_value=backup
                    )
                )
            )
            mock_update.assert_not_called()
            mock_save.assert_not_called()
            self.frame.save()
            mock_update.assert_called_once_with()
            mock_save.assert_called_once_with(backup=backup)
            mock_update.reset_mock()


class UpdateEntryControlUnitTests(ConfigFrameTestCase):
    KEY_NAME = 'qqq'
    PRE = 9
    VALUE = 10
    LABEL = 12

    SET_VALUE = MagicMock()
    SET_LABEL = MagicMock()

    def setUp(self):
        ConfigFrameTestCase.setUp(self)
        self.SET_VALUE.reset_mock()
        self.SET_LABEL.reset_mock()

    def test_with_value(self):
        self.mock_findwindow.return_value = MagicMock(
            spec=['SetValue'],
            SetValue=self.SET_VALUE
        )
        self.SET_VALUE.assert_not_called()
        self.SET_LABEL.assert_not_called()
        self.frame.update_entry_control(
            MagicMock(
                key_name=self.KEY_NAME,
                current=self.VALUE
            )
        )
        self.SET_VALUE.assert_called_once_with(self.VALUE)
        self.SET_LABEL.assert_not_called()

    def test_with_label(self):
        self.mock_findwindow.return_value = MagicMock(
            spec=['SetLabel'],
            SetLabel=self.SET_LABEL
        )
        self.SET_VALUE.assert_not_called()
        self.SET_LABEL.assert_not_called()
        self.frame.update_entry_control(
            MagicMock(
                key_name=self.KEY_NAME,
                current=self.LABEL
            )
        )
        self.SET_VALUE.assert_not_called()
        self.SET_LABEL.assert_called_once_with(self.LABEL)
