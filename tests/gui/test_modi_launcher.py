# pylint: disable=missing-docstring
# pylint: disable=too-many-instance-attributes
# pylint: disable=unused-argument

from __future__ import print_function

from unittest import TestCase

from mock import patch

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
            'wxpy_rofi_config.gui.modi_launcherSingleChoiceDialog'
        )
        self.mock_singlechoice = singlechoice_patcher.start()
        self.addCleanup(singlechoice_patcher.stop)

    def construct_modi(self):
        runner_patcher = patch.object(ModiLauncher, 'select_and_launch')
        self.mock_runner = runner_patcher.start()
        self.modi = ModiLauncher(None)
        runner_patcher.stop()
