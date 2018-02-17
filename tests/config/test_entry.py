# pylint: disable=missing-docstring
# pylint: disable=unused-argument

from __future__ import print_function

from unittest import TestCase

from mock import MagicMock, patch

from wxpy_rofi_config.config import Entry


class EntryTestCase(TestCase):

    def setUp(self):
        self.construct_entry()
        self.addCleanup(self.wipe_entry)

    def wipe_entry(self):
        del self.entry

    def construct_entry(self):
        self.entry = Entry()
