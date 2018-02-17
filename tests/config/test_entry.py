# pylint: disable=missing-docstring
# pylint: disable=unused-argument

from __future__ import print_function

from unittest import TestCase

from mock import MagicMock, patch
# from pytest.mark import parametrize
from pytest import mark

from wxpy_rofi_config.config import Entry


class EntryTestCase(TestCase):

    def setUp(self):
        self.construct_entry()
        self.addCleanup(self.wipe_entry)

    def wipe_entry(self):
        del self.entry

    def construct_entry(self):
        self.entry = Entry()


class ConstructorUnitTests(EntryTestCase):

    NOT_DEFAULT = {
        'key_name': 'qqq',
        'var_type': 'number',
        'group': 'Mouse',
        'default': 10,
        'current': 20,
        'man': 'no soup for you'
    }

    def test_values(self):
        for key, value in self.NOT_DEFAULT.iteritems():
            entry = Entry(**{key: value})
            self.assertEquals(getattr(entry, key), value)


class AssignCurrentUnitTests(EntryTestCase):
    DEFAULT = [None, 10]
    CURRENT = [None, 20]
    EXPECTED = [None, 20, 10, 20]

    def test_values(self):
        index = 0
        for default in self.DEFAULT:
            for current in self.CURRENT:
                self.entry.default = default
                self.entry.current = current
                self.entry.assign_current()
                self.assertEquals(self.entry.current, self.EXPECTED[index])
                index += 1
