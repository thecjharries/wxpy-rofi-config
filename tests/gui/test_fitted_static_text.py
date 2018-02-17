# pylint: disable=attribute-defined-outside-init
# pylint: disable=missing-docstring
# pylint: disable=too-many-instance-attributes
# pylint: disable=unused-argument

from __future__ import print_function

from unittest import TestCase

from mock import MagicMock, patch

from wxpy_rofi_config.gui import FittedStaticText


class FittedStaticTextTestCase(TestCase):

    def setUp(self):
        self.patch_wx()
        self.construct_text()
        self.addCleanup(self.wipe_text)

    def wipe_text(self):
        del self.text

    def patch_wx(self):
        control_patcher = patch(
            'wxpy_rofi_config.gui.fitted_static_text.Control'
        )
        self.mock_control = control_patcher.start()
        self.addCleanup(control_patcher.stop)
        statictext_patcher = patch(
            'wxpy_rofi_config.gui.fitted_static_text.StaticText'
        )
        self.mock_statictext = statictext_patcher.start()
        self.addCleanup(statictext_patcher.stop)

    def construct_text(self):
        set_label_patcher = patch.object(FittedStaticText, 'set_label')
        self.mock_set_label = set_label_patcher.start()
        self.text = FittedStaticText()
        set_label_patcher.stop()
