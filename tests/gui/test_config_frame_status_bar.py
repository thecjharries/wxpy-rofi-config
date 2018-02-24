# pylint: disable=missing-docstring
# pylint: disable=too-many-instance-attributes
# pylint: disable=unused-argument

from __future__ import print_function

from unittest import TestCase

from mock import call, patch

from pydispatch.dispatcher import Any

from wxpy_rofi_config.gui import ConfigFrameStatusBar


class ConfigFrameStatusBarTestCase(TestCase):

    STATUS_ID = 0

    def setUp(self):
        self.patch_wx()
        self.construct_status_bar()
        self.addCleanup(self.wipe_status_bar)

    def wipe_status_bar(self):
        del self.status_bar

    def patch_wx(self):
        status_bar_patcher = patch(
            'wxpy_rofi_config.gui.config_frame_status_bar.StatusBar.__init__'
        )
        self.mock_status_bar = status_bar_patcher.start()
        self.addCleanup(status_bar_patcher.stop)
        pub_patcher = patch(
            'wxpy_rofi_config.gui.config_frame_status_bar.connect')
        self.mock_pub = pub_patcher.start()
        self.addCleanup(pub_patcher.stop)

    def construct_status_bar(self):
        self.status_bar = ConfigFrameStatusBar(None)


class ConstructorUnitTests(ConfigFrameStatusBarTestCase):

    def test_calls(self):
        self.mock_status_bar.assert_called_once()
        self.mock_pub.assert_has_calls(
            [
                call(self.status_bar.update, signal='status_update', sender=Any),
                call(self.status_bar.clear, signal='status_clear', sender=Any)
            ],
            True
        )


class UpdateUnitTests(ConfigFrameStatusBarTestCase):
    STATUS = 'qqq'

    @patch.object(ConfigFrameStatusBar, 'SetStatusText')
    def test_update(self, mock_set):
        mock_set.assert_not_called()
        self.status_bar.update(self.STATUS)
        mock_set.assert_called_once_with(self.STATUS, self.STATUS_ID)


class ClearUnitTests(ConfigFrameStatusBarTestCase):

    @patch.object(ConfigFrameStatusBar, 'SetStatusText')
    def test_update(self, mock_set):
        mock_set.assert_not_called()
        self.status_bar.clear()
        mock_set.assert_called_once_with('', self.STATUS_ID)
