# pylint: disable=missing-docstring
# pylint: disable=too-many-instance-attributes
# pylint: disable=unused-argument

from __future__ import print_function

from unittest import TestCase

from mock import patch

from wxpy_rofi_config.gui import ConfigApp


class ConfigAppTestCase(TestCase):

    def setUp(self):
        self.patch_wx()
        self.construct_app()
        self.addCleanup(self.wipe_app)

    def wipe_app(self):
        del self.app

    def patch_wx(self):
        app_patcher = patch('wxpy_rofi_config.gui.config_app.App')
        self.mock_app = app_patcher.start()
        self.addCleanup(app_patcher.stop)
        frame_patcher = patch('wxpy_rofi_config.gui.config_app.ConfigFrame')
        self.mock_frame = frame_patcher.start()
        self.addCleanup(frame_patcher.stop)
        inspectionmixin_patcher = patch(
            'wxpy_rofi_config.gui.config_app.InspectionMixin')
        self.mock_inspectionmixin = inspectionmixin_patcher.start()
        self.addCleanup(inspectionmixin_patcher.stop)

    def construct_app(self):
        init_patcher = patch.object(ConfigApp, 'Init')
        self.mock_init = init_patcher.start()
        construct_gui_patcher = patch.object(ConfigApp, 'construct_gui')
        self.mock_construct_gui = construct_gui_patcher.start()
        self.app = ConfigApp()
        init_patcher.stop()
        construct_gui_patcher.stop()


class OnInitUnitTests(ConfigAppTestCase):

    @patch.object(ConfigApp, 'Init')
    @patch.object(ConfigApp, 'construct_gui')
    def test_construction(self, mock_gui, mock_init):
        mock_init.assert_not_called()
        mock_gui.assert_not_called()
        self.app.OnInit()
        mock_init.assert_called_once_with()
        mock_gui.assert_called_once_with()
