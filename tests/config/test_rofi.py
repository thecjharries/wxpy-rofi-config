# pylint: disable=missing-docstring
# pylint: disable=unused-argument

from __future__ import print_function

from unittest import TestCase

from mock import call, MagicMock, patch

from wxpy_rofi_config.config import Entry, Rofi


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
        mock_entry.assert_not_called()
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


class LoadCurrentConfigUnitTests(RofiTestCase):
    OUTPUT = '''
 modi/* something */: qqq;
// something
 display-window: "stuff";
'''
    RESULT = r'''
 modi: qqq;

 display-window: "stuff";
'''

    @patch('wxpy_rofi_config.config.rofi.check_output', return_value=OUTPUT)
    @patch.object(Rofi, 'parse_rasi')
    def test_calls(self, mock_parse, mock_check):
        self.rofi.load_current_config()
        mock_parse.assert_called_once_with(self.RESULT, 'current')


class ProcessConfigUnitTests(RofiTestCase):
    INPUT = {
        'one': MagicMock(group='one'),
        'two': MagicMock(group='one'),
        'three': MagicMock(group='two')
    }
    GROUPS = ['one', 'two']

    def test_construction(self):
        self.rofi.config = self.INPUT
        self.rofi.process_config()
        if hasattr(self, 'assertCountEqual'):
            getattr(self, 'assertCountEqual')(self.rofi.groups, self.GROUPS)
        elif hasattr(self, 'assertItemsEqual'):
            getattr(self, 'assertItemsEqual')(self.rofi.groups, self.GROUPS)
        else:
            assert 0


@patch('wxpy_rofi_config.config.rofi.sub')
def test_clean_entry_man(mock_sub):
    rofi = Rofi()
    rofi.clean_entry_man('gibberish')
    assert mock_sub.call_count == len(Rofi.PATTERNS['CLEAN_MAN'])


class ParseManEntryUnitTests(RofiTestCase):

    def setUp(self):
        RofiTestCase.setUp(self)
        self.match = MagicMock(
            group=lambda x: x
        )
        self.rofi.config['key'] = MagicMock(
            group=Entry.DEFAULTS['group'],
            man=None
        )
        clean_patcher = patch.object(
            Rofi,
            'clean_entry_man',
            return_value='man',
        )
        self.mock_clean = clean_patcher.start()
        self.addCleanup(clean_patcher.stop)

    def test_missing_key(self):
        self.rofi.config = MagicMock()
        self.rofi.parse_man_entry('group', self.match)
        self.mock_clean.assert_not_called()

    def test_existing_key_without_man(self):
        self.mock_clean.return_value = None
        self.rofi.parse_man_entry('group', self.match)
        self.mock_clean.assert_called_once_with('man')
        self.assertEquals(
            self.rofi.config['key'].group,
            Entry.DEFAULTS['group']
        )
        self.assertIsNone(
            self.rofi.config['key'].man
        )

    def test_existing_key_with_man(self):
        self.rofi.parse_man_entry('group', self.match)
        self.mock_clean.assert_called_once_with('man')
        self.assertEquals(
            self.rofi.config['key'].group,
            'group'
        )
        self.assertEquals(
            self.rofi.config['key'].man,
            'man'
        )


class ParseManGroupUnitTests(RofiTestCase):
    INPUT = """

       -one

       one

       -two

       two

       -three

       three
"""

    @patch.object(Rofi, 'parse_man_entry')
    def test_construction(self, mock_parse):
        match = MagicMock(group=lambda x: self.INPUT)
        self.rofi.parse_man_group(match)
        self.assertEquals(
            mock_parse.call_count,
            3
        )


class ParseManConfigUnitTests(RofiTestCase):
    INPUT = """
   one
        -one

   two
        -two

   three
        -three
"""

    @patch.object(Rofi, 'parse_man_group')
    def test_construction(self, mock_parse):
        match = self.INPUT
        self.rofi.parse_man_config(match)
        self.assertEquals(
            mock_parse.call_count,
            3
        )


class LoadManUnitTests(RofiTestCase):

    @patch(
        'wxpy_rofi_config.config.rofi.check_output',
        return_value='''
CONFIGURATION
    stuff
q
'''
    )
    @patch.object(Rofi, 'parse_man_config')
    def test_with_config(self, mock_parse, mock_output):
        self.rofi.load_man()
        mock_parse.assert_called_once()

    @patch(
        'wxpy_rofi_config.config.rofi.check_output',
        return_value=''
    )
    @patch.object(Rofi, 'parse_man_config')
    def test_without_config(self, mock_parse, mock_output):
        self.rofi.load_man()
        mock_parse.assert_not_called()


class BuildUnitTests(RofiTestCase):

    @patch.object(Rofi, 'load_default_config')
    @patch.object(Rofi, 'load_current_config')
    @patch.object(Rofi, 'load_help')
    @patch.object(Rofi, 'load_man')
    @patch.object(Rofi, 'process_config')
    def test_call(  # pylint: disable=too-many-arguments
            self,
            mock_process,
            mock_man,
            mock_help,
            mock_current,
            mock_default
    ):
        mock_holder = MagicMock()
        mock_holder.attach_mock(mock_default, 'load_default_config')
        mock_holder.attach_mock(mock_current, 'load_current_config')
        mock_holder.attach_mock(mock_help, 'load_help')
        mock_holder.attach_mock(mock_man, 'load_man')
        mock_holder.attach_mock(mock_process, 'process_config')
        self.rofi.build()
        mock_holder.assert_has_calls([
            call.load_default_config(),
            call.load_current_config(),
            call.load_help(),
            call.load_man(),
            call.process_config()
        ])


class ToRasiUnitTests(RofiTestCase):
    RESULT = (
        'configuration {\n'
        '    key: value;\n'
        '}\n'
    )

    def test_result(self):
        self.rofi.config = {
            'key': MagicMock(to_rasi=lambda: 'key: value;')
        }
        self.assertEquals(
            self.rofi.to_rasi(),
            self.RESULT
        )


@patch('wxpy_rofi_config.config.rofi.open', return_value=MagicMock())
@patch.object(Rofi, 'to_rasi')
def test_save(mock_rasi, mock_open):
    rofi = Rofi()
    rofi.save()
    mock_rasi.assert_called_once_with()
