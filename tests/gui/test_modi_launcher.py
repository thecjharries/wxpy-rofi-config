# pylint: disable=missing-docstring
# pylint: disable=too-many-instance-attributes
# pylint: disable=unused-argument

from __future__ import print_function

from unittest import TestCase

from mock import MagicMock, patch

from wx import ID_OK  # pylint: disable=no-name-in-module

from wxpy_rofi_config.gui import ModiLauncher


class ModiLauncherTestCase(TestCase):

    def setUp(self):
        self.patch_wx()
        self.construct_modi()
        self.addCleanup(self.wipe_modi)

    def wipe_modi(self):
        del self.modi

    def patch_wx(self):
        singlechoice_patcher = patch(
            'wxpy_rofi_config.gui.modi_launcher.SingleChoiceDialog'
        )
        self.mock_singlechoice = singlechoice_patcher.start()
        self.addCleanup(singlechoice_patcher.stop)

    def construct_modi(self):
        runner_patcher = patch.object(ModiLauncher, 'select_and_launch')
        self.mock_runner = runner_patcher.start()
        self.modi = ModiLauncher(None)
        runner_patcher.stop()


class ConstructorUnitTests(ModiLauncherTestCase):

    def test_calls(self):
        self.mock_runner.assert_called_once_with()


class SelectModiUnitTests(ModiLauncherTestCase):
    MODI = 'window'

    def test_ok_modal(self):
        self.mock_singlechoice.return_value = MagicMock(
            __enter__=MagicMock(
                return_value=MagicMock(
                    ShowModal=MagicMock(return_value=ID_OK),
                    GetStringSelection=MagicMock(return_value=self.MODI)
                )
            )
        )
        result = self.modi.select_modi()
        self.assertEquals(result, self.MODI)

    def test_cancelled_modal(self):
        self.assertIsNone(self.modi.select_modi())
