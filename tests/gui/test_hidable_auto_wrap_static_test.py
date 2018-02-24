# pylint: disable=missing-docstring
# pylint: disable=too-many-instance-attributes
# pylint: disable=unused-argument

from __future__ import print_function

from unittest import TestCase

from mock import patch

from wxpy_rofi_config.gui import HidableAutoWrapStaticText


class HidableAutoWrapStaticTextTestCase(TestCase):

    def setUp(self):
        self.patch_wx()
        self.construct_text()
        self.addCleanup(self.wipe_text)

    def wipe_text(self):
        del self.text

    def patch_wx(self):
        pub_patcher = patch(
            'wxpy_rofi_config.gui.hidable_auto_wrap_static_test.pub.subscribe'
        )
        self.mock_pub = pub_patcher.start()
        self.addCleanup(pub_patcher.stop)
        autostaticwraptext_patcher = patch(
            'wxpy_rofi_config.gui.hidable_auto_wrap_static_test.AutoWrapStaticText'
        )
        self.mock_autostaticwraptext = autostaticwraptext_patcher.start()
        self.addCleanup(autostaticwraptext_patcher.stop)

    def construct_text(self):
        self.text = HidableAutoWrapStaticText()
