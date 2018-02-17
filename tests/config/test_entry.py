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
    def test_with_method(self, mock_clean):
        self.entry.var_type = 'number'
        self.entry.attempt_to_clean_values()
        self.assertEquals(mock_clean.call_count, 2)
        self.assertEquals(self.entry.default, self.RETURN)
        self.assertEquals(self.entry.current, self.RETURN)


class ForceVarTypeUnitTests(EntryTestCase):

    # MOCK_NUMBER = lambda

    RESULTS = ['string', 'number']

    @patch.object(
        Entry,
        'is_number',
        side_effect=lambda x: x > 0
    )
    def test_values(self, mock_number):
        for default in [0, 1]:
            for current in [0, 1]:
                self.entry.default = default
                self.entry.current = current
                var_type = self.entry.force_var_type()
                self.assertEquals(self.RESULTS[default & current], var_type)


class EnsureUsefulVarTypeUnitTests(EntryTestCase):

    @patch.object(
        Entry,
        'force_var_type',
        return_value='string'
    )
    @patch.object(
        Entry,
        'guess_var_type_from_value',
        return_value='unknown'
    )
    @patch.object(
        Entry,
        'guess_var_type_from_key',
        return_value='unknown'
    )
    def test_known_type(self, mock_key, mock_value, mock_force):
        self.entry.var_type = 'string'
        self.entry.ensure_useful_var_type()
        self.assertEquals(mock_key.call_count, 0)
        self.assertEquals(mock_value.call_count, 0)
        self.assertEquals(mock_force.call_count, 0)

    @patch.object(
        Entry,
        'force_var_type',
        return_value='string'
    )
    @patch.object(
        Entry,
        'guess_var_type_from_value',
        return_value='unknown'
    )
    @patch.object(
        Entry,
        'guess_var_type_from_key',
        return_value='string'
    )
    def test_key_type(self, mock_key, mock_value, mock_force):
        self.entry.var_type = 'unknown'
        self.entry.ensure_useful_var_type()
        mock_key.assert_called_once_with(Entry.DEFAULTS['key_name'])
        self.assertEquals(mock_value.call_count, 0)
        self.assertEquals(mock_force.call_count, 0)

    @patch.object(
        Entry,
        'force_var_type',
        return_value='string'
    )
    @patch.object(
        Entry,
        'guess_var_type_from_value',
        return_value='string'
    )
    @patch.object(
        Entry,
        'guess_var_type_from_key',
        return_value='unknown'
    )
    def test_value_type(self, mock_key, mock_value, mock_force):
        self.entry.var_type = 'unknown'
        self.entry.ensure_useful_var_type()
        self.assertEquals(mock_key.call_count, 1)
        mock_value.assert_called_once_with(Entry.DEFAULTS['default'])
        self.assertEquals(mock_force.call_count, 0)

    @patch.object(
        Entry,
        'force_var_type',
        return_value='string'
    )
    @patch.object(
        Entry,
        'guess_var_type_from_value',
        return_value='unknown'
    )
    @patch.object(
        Entry,
        'guess_var_type_from_key',
        return_value='unknown'
    )
    def test_force_type(self, mock_key, mock_value, mock_force):
        self.entry.var_type = 'unknown'
        self.entry.ensure_useful_var_type()
        self.assertEquals(mock_key.call_count, 1)
        self.assertEquals(mock_value.call_count, 2)
        mock_force.assert_called_once_with(None)


class LookForUsefulGroupUnitTests(EntryTestCase):

    @patch.object(Entry, 'guess_group_from_key')
    def test_changed_group(self, mock_guess):
        self.entry.group = 'qqq'
        self.entry.look_for_useful_group()
        self.assertEquals(mock_guess.call_count, 0)

    @patch.object(Entry, 'guess_group_from_key')
    def test_default_group(self, mock_guess):
        self.entry.look_for_useful_group()
        mock_guess.assert_called_once_with(Entry.DEFAULTS['key_name'])


class ToRasiUnitTests(EntryTestCase):

    RUNS = [
        {
            'var_type': 'number',
            'key_name': 'qqq',
            'current': 10,
            'expected': 'qqq: 10;'
        },
        {
            'var_type': 'boolean',
            'key_name': 'qqq',
            'current': False,
            'expected': 'qqq: false;'
        },
        {
            'var_type': 'string',
            'key_name': 'qqq',
            'current': 'zzz',
            'expected': 'qqq: "zzz";'
        },
        {
            'key_name': 'qqq',
            'current': 'testing',
            'expected': 'qqq: testing;'
        }
    ]

    def test_values(self):
        for run in self.RUNS:
            self.entry = Entry(**run)
            result = self.entry.to_rasi()
            self.assertEquals(result, run['expected'])
