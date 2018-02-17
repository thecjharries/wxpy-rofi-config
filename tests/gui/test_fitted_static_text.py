# pylint: disable=attribute-defined-outside-init
# pylint: disable=missing-docstring
# pylint: disable=too-many-instance-attributes
# pylint: disable=unused-argument

from __future__ import print_function

from unittest import TestCase

from mock import call, MagicMock, patch

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
        self.text = FittedStaticText(None)
        set_label_patcher.stop()


class ConstructorUnitTests(FittedStaticTextTestCase):

    def test_construction(self):
        self.mock_statictext.assert_called_once()
        self.mock_set_label.assert_called_once()


class SetLabelUnitTests(FittedStaticTextTestCase):

    @patch.object(FittedStaticText, 'fit_label')
    def test_calls(self, mock_fit):
        mock_fit.assert_not_called()
        self.text.set_label('qqq')
        mock_fit.assert_called()


class ResizeUnitTests(FittedStaticTextTestCase):

    @patch.object(FittedStaticText, 'GetSize')
    @patch.object(FittedStaticText, 'fit_label')
    def test_calls(self, mock_fit, mock_size):
        mock_holder = MagicMock()
        mock_holder.attach_mock(mock_fit, 'fit_label')
        mock_holder.attach_mock(mock_size, 'GetSize')
        self.text.resize()
        mock_holder.assert_has_calls([
            call.fit_label(),
            call.GetSize(),
            call.fit_label()
        ])


class FitLabelUnitTests(FittedStaticTextTestCase):
    WIDTH = 2
    LABEL = 'qqq'

    @patch.object(
        FittedStaticText,
        'GetSize',
        return_value=MagicMock(width=WIDTH)
    )
    def test_fitting(self, mock_size):
        self.text.label = self.LABEL
        mock_text = MagicMock()
        self.text.text = mock_text
        self.text.fit_label()
        mock_text.assert_has_calls([
            call.Freeze(),
            call.SetLabel(self.LABEL),
            call.Wrap(self.WIDTH),
            call.Thaw()
        ])
