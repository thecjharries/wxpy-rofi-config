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


class AttemptToCleanValues(EntryTestCase):
    RETURN = 47
    DEFAULT = 22
    CURRENT = 12

    def setUp(self):
        EntryTestCase.setUp(self)
        self.entry.default = self.DEFAULT
        self.entry.current = self.CURRENT

    @patch.object(Entry, 'clean_number', return_value=RETURN)
    def test_without_method(self, mock_clean):
        self.entry.var_type = 'not a method'
        self.entry.attempt_to_clean_values()
        self.assertEquals(mock_clean.call_count, 0)
        self.assertEquals(self.entry.default, self.DEFAULT)
        self.assertEquals(self.entry.current, self.CURRENT)

    @patch.object(Entry, 'clean_number', return_value=RETURN)
    def test_without_method(self, mock_clean):
        self.entry.var_type = 'number'
        self.entry.attempt_to_clean_values()
        self.assertEquals(mock_clean.call_count, 2)
        self.assertEquals(self.entry.default, self.RETURN)
        self.assertEquals(self.entry.current, self.RETURN)
