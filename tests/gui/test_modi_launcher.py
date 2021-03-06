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

    PROMPT = 'qqq'

    def test_calls(self):
        self.mock_runner.assert_called_once_with()

    @patch.object(ModiLauncher, 'select_and_launch')
    def test_prompt(self, mock_runner):
        modi = ModiLauncher(None, prompt=self.PROMPT)
        self.assertEquals(
            modi.prompt,
            self.PROMPT
        )


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


class SelectAndLaunchUnitTests(ModiLauncherTestCase):
    MODI = 'window'

    @patch.object(
        ModiLauncher,
        'select_modi',
        return_value=MODI
    )
    @patch.object(ModiLauncher, 'launch_modi')
    def test_with_selection(self, mock_launch, mock_select):
        mock_select.assert_not_called()
        mock_launch.assert_not_called()
        self.modi.select_and_launch()
        mock_select.assert_called_once_with()
        mock_launch.assert_called_once_with(self.MODI)

    @patch.object(
        ModiLauncher,
        'select_modi',
        return_value=None
    )
    @patch.object(ModiLauncher, 'launch_modi')
    def test_without_selection(self, mock_launch, mock_select):
        mock_select.assert_not_called()
        mock_launch.assert_not_called()
        self.modi.select_and_launch()
        mock_select.assert_called_once_with()
        mock_launch.assert_not_called()


@patch('wxpy_rofi_config.gui.modi_launcher.call')
def test_launch_modi(mock_call):
    mock_call.assert_not_called()
    ModiLauncher.launch_modi('qqq')
    mock_call.assert_called_once_with(['rofi', '-show', 'qqq'])
