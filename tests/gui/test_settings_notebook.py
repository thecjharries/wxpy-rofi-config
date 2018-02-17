# pylint: disable=missing-docstring

from __future__ import print_function

from unittest import TestCase

from mock import call, MagicMock, patch

from wxpy_rofi_config.gui import SettingsNotebook


class SettingsNotebookTestCase(TestCase):

    def setUp(self):
        self.patch_wx()
        self.construct_notebook()
        self.addCleanup(self.wipe_notebook)

    def wipe_notebook(self):
        del self.notebook

    def patch_wx(self):
        findwindowbyname_patcher = patch(
            'wxpy_rofi_config.gui.settings_notebook.FindWindowByName'
        )
        self.mock_findwindowbyname = findwindowbyname_patcher.start()
        self.addCleanup(findwindowbyname_patcher.stop)
        notebook_patcher = patch(
            'wxpy_rofi_config.gui.settings_notebook.Notebook'
        )
        self.mock_notebook = notebook_patcher.start()
        self.addCleanup(notebook_patcher.stop)

    def construct_notebook(self):
        settings_panel_patcher = patch(
            'wxpy_rofi_config.gui.settings_notebook.SettingsPanel'
        )
        self.mock_settings_panel = settings_panel_patcher.start()
        self.addCleanup(settings_panel_patcher.stop)
        rofi_patcher = patch('wxpy_rofi_config.gui.settings_notebook.Rofi')
        self.mock_rofi = rofi_patcher.start()
        self.addCleanup(rofi_patcher.stop)
        create_tabs_patcher = patch.object(SettingsNotebook, 'create_tabs')
        self.mock_create_tabs = create_tabs_patcher.start()
        bind_events_patcher = patch.object(SettingsNotebook, 'bind_events')
        self.mock_bind_events = bind_events_patcher.start()
        self.notebook = SettingsNotebook(None)
        create_tabs_patcher.stop()
        bind_events_patcher.stop()


class ConstructorUnitTests(SettingsNotebookTestCase):

    def test_construction(self):
        self.mock_create_tabs.assert_called_once()
        self.mock_bind_events.assert_called_once()


class GroupConfigUnitTests(SettingsNotebookTestCase):

    CONFIG = {
        'one': MagicMock(group='one'),
        'two': MagicMock(group='two'),
        'three': MagicMock(group='two')
    }

    RESULT = ['one', 'two']

    def test_config_creation(self):
        self.mock_rofi.assert_not_called()
        self.notebook.group_config()
        self.mock_rofi.assert_called_once()

    def test_group_list(self):
        self.mock_rofi.return_value = MagicMock(config=self.CONFIG)
        self.notebook.group_config()
        if hasattr(self, 'assertCountEqual'):
            getattr(self, 'assertCountEqual')(
                self.notebook.groups,
                self.RESULT
            )
        elif hasattr(self, 'assertItemsEqual'):
            getattr(self, 'assertItemsEqual')(
                self.notebook.groups,
                self.RESULT
            )
        else:
            assert 0


class CreateTabUnitTests(SettingsNotebookTestCase):

    @patch.object(SettingsNotebook, 'AddPage')
    def test_construction(self, mock_add):
        self.notebook.groups = MagicMock()
        self.mock_settings_panel.assert_not_called()
        mock_add.assert_not_called()
        self.notebook.create_tab('qqq')
        self.mock_settings_panel.assert_called_once()
        mock_add.assert_called_once()


class CreateTabsUnitTests(SettingsNotebookTestCase):
    GROUPS = {
        'one': 'one',
        'two': 'two',
        'three': 'three'
    }

    CALLS = [call(value) for key, value in GROUPS.items()]

    @patch.object(SettingsNotebook, 'group_config')
    @patch.object(SettingsNotebook, 'create_tab')
    def test_construction(self, mock_tab, mock_config):
        self.notebook.groups = self.GROUPS
        self.notebook.create_tabs()
        mock_config.assert_called_once()
        mock_tab.assert_has_calls(self.CALLS)


class BindEventsUnitTests(SettingsNotebookTestCase):

    @patch.object(SettingsNotebook, 'Bind')
    def test_calls(self, mock_bind):
        mock_bind.assert_not_called()
        self.notebook.bind_events()
        mock_bind.assert_called()


class ResizeUnitTests(SettingsNotebookTestCase):

    @patch.object(SettingsNotebook, 'GetSelection', return_value=0)
    def test_calls(self, mock_selection):
        self.notebook.tabs = [MagicMock()]
        mock_selection.assert_not_called()
        self.notebook.resize()
        mock_selection.assert_called_once()


class SaveUnitTests(SettingsNotebookTestCase):
    TABS = ['one', 'two']
    GROUPS = {
        'one': [
            MagicMock(
                key_name='one',
                current='one'
            )
        ],
        'two': [
            MagicMock(
                key_name='two',
                current='two'
            ),
            MagicMock(
                key_name='three',
                current='three'
            )
        ],
    }

    WINDOWS = {
        'one': MagicMock(GetValue=MagicMock(return_value=1)),
        'two': MagicMock(
            spec=['GetLabel'],
            GetLabel=MagicMock(return_value=22)
        ),
        'three': MagicMock(spec=[])
    }

    CONFIG = {
        'one': MagicMock(
            key_name='one',
            current='one'
        ),
        'two': MagicMock(
            key_name='two',
            current='two'
        ),
        'three': MagicMock(
            key_name='three',
            current='three'
        )
    }

    RESULT = {
        'one': 1,
        'two': 22,
        'three': 'three'
    }

    def test_execution(self):
        self.notebook.config = MagicMock(config=self.CONFIG)
        self.notebook.tabs = self.TABS
        self.notebook.groups = self.GROUPS
        self.mock_findwindowbyname.side_effect = lambda x: self.WINDOWS[x]
        self.notebook.save()
        for key, value in self.RESULT.items():
            self.assertEquals(
                self.notebook.config.config[key].current,
                value
            )


class ChangeDisplayStateUnitTests(SettingsNotebookTestCase):
    CHANGE_STATE = MagicMock()

    TABS = [
        MagicMock(change_display_state=CHANGE_STATE),
        MagicMock(change_display_state=CHANGE_STATE),
        MagicMock(change_display_state=CHANGE_STATE),
    ]

    @patch.object(SettingsNotebook, 'resize')
    def test_state_change(self, mock_resize):
        self.notebook.tabs = self.TABS
        self.notebook.change_display_state('target', True)
        self.CHANGE_STATE.assert_has_calls([
            call('target', True),
            call('target', True),
            call('target', True),
        ])
        mock_resize.assert_called_once_with()
