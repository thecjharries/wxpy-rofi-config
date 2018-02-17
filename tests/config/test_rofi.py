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
