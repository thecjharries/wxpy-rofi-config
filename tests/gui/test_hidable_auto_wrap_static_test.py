# pylint: disable=missing-docstring
# pylint: disable=too-many-instance-attributes
# pylint: disable=unused-argument

from __future__ import print_function

from unittest import TestCase

from mock import MagicMock, patch

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
            'wxpy_rofi_config.gui.hidable_auto_wrap_static_test.AutoWrapStaticText.__init__'
        )
        self.mock_autostaticwraptext = autostaticwraptext_patcher.start()
        self.addCleanup(autostaticwraptext_patcher.stop)

    def construct_text(self):
        self.text = HidableAutoWrapStaticText()


class ConstructorUnitTests(HidableAutoWrapStaticTextTestCase):

    def test_calls(self):
        self.mock_autostaticwraptext.assert_called_once()
        self.mock_pub.assert_called_once_with(
            self.text.toggle_display,
            "toggle_display_%s" % HidableAutoWrapStaticText.DEFAULT_KIND
        )


class ToggleDisplayUnitTests(HidableAutoWrapStaticTextTestCase):

    HIDE = MagicMock()
    SHOW = MagicMock()

    TESTS = [
        [True, SHOW, HIDE],
        [False, HIDE, SHOW]
    ]

    def setUp(self):
        HidableAutoWrapStaticTextTestCase.setUp(self)
        self.text.Show = self.SHOW
        self.text.Hide = self.HIDE
        self.text.GetParent = MagicMock()

    def test_toggle(self):
        for entry in self.TESTS:
            print(entry)
            self.SHOW.assert_not_called()
            self.HIDE.assert_not_called()
            self.text.toggle_display(entry[0])
            entry[1].assert_called_once_with()
            entry[2].assert_not_called()
            self.SHOW.reset_mock()
            self.HIDE.reset_mock()
