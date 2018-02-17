# pylint: disable=attribute-defined-outside-init
# pylint: disable=missing-docstring
# pylint: disable=too-many-instance-attributes
# pylint: disable=unused-argument

from __future__ import print_function

from unittest import TestCase

from mock import MagicMock, patch

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
