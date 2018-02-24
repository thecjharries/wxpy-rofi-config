# pylint: disable=missing-docstring
# pylint: disable=too-many-instance-attributes
# pylint: disable=unused-argument

from __future__ import print_function

from unittest import TestCase

from mock import patch

from wxpy_rofi_config.gui import ConfigFrameStatusBar


class ConfigFrameStatusBarTestCase(TestCase):

    def setUp(self):
        self.patch_wx()
        self.construct_status_bar()
        self.addCleanup(self.wipe_status_bar)

    def wipe_status_bar(self):
        del self.status_bar

    def patch_wx(self):
        status_bar_patcher = patch(
            'wxpy_rofi_config.gui.config_frame_status_bar.StatusBar'
        )
        self.mock_status_bar = status_bar_patcher.start()
        self.addCleanup(status_bar_patcher.stop)
        pub_patcher = patch(
            'wxpy_rofi_config.gui.config_frame_menu_bar.pub.subscribe')
        self.mock_pub = pub_patcher.start()
        self.addCleanup(pub_patcher.stop)

    def construct_status_bar(self):
        self.status_bar = ConfigFrameStatusBar(None)
