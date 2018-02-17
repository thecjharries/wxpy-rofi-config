# pylint: disable=attribute-defined-outside-init
# pylint: disable=missing-docstring
# pylint: disable=unused-argument

from __future__ import print_function

from unittest import TestCase

from mock import call, MagicMock, patch
from pytest import mark

from wxpy_rofi_config.config import Rofi


class RofiTestCase(TestCase):

    def setUp(self):
        self.construct_rofi()
        self.addCleanup(self.wipe_rofi)

    def wipe_rofi(self):
        del self.rofi

    def construct_rofi(self):
        self.rofi = Rofi()


def test_constructor():
    rofi = Rofi()
    assert not rofi.config
    assert not rofi.groups


class AssignRasiEntryUnitTests(RofiTestCase):

    @patch('wxpy_rofi_config.config.rofi.Entry')
    def test_existing_key(self, mock_entry):
        mock_match = MagicMock(group=lambda x: x)
        self.rofi.config['key'] = MagicMock(default='not value')
        self.rofi.assign_rasi_entry(mock_match)
        self.assertEquals(mock_entry.call_count, 0)
        self.assertEquals(self.rofi.config['key'].default, 'value')

    @patch('wxpy_rofi_config.config.rofi.Entry')
    def test_new_key(self, mock_entry):
        mock_match = MagicMock(group=lambda x: x)
        self.rofi.assign_rasi_entry(mock_match)
        mock_entry.assert_called_once_with(
            key_name='key',
            default='value',
        )


class ParseRasiUnitTests(RofiTestCase):
    RUNS = [
        [
            ' modi: qqq;\n'
            ' bad_opt: qqq;\n'
            ' good-opt: qqq;\n',
            2
        ]
    ]

    @patch.object(Rofi, 'assign_rasi_entry')
    def test_rasi_discover(self, mock_assign):
        for run in self.RUNS:
            mock_assign.reset_mock()
            self.rofi.parse_rasi(run[0])
            self.assertEquals(
                mock_assign.call_count,
                run[1]
            )


class LoadDefaultConfigUnitTests(RofiTestCase):
    OUTPUT = 'qqq'

    @patch('wxpy_rofi_config.config.rofi.check_output', return_value=OUTPUT)
    @patch.object(Rofi, 'parse_rasi')
    def test_calls(self, mock_parse, mock_check):
        self.rofi.load_default_config()
        mock_parse.assert_called_once_with(self.OUTPUT, 'default')
