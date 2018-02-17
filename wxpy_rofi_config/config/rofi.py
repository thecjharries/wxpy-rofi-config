# pylint: disable=W,C,R
# coding=utf8

from collections import OrderedDict
from os.path import join
from re import compile as re_compile, DOTALL, finditer, MULTILINE, search, sub
from subprocess import check_output

from wxpy_rofi_config.config import Entry


class Rofi(object):

    DEFAULT_PATH = join('~', '.config', 'rofi', 'config.rasi')

    PATTERNS = {
        'RASI_ENTRY': re_compile(
            r"^.*?(?P<key>[\w-]*):\s*(?P<value>.*?);.*?$",
            MULTILINE
        ),
        'RASI_COMMENT': re_compile(r"(\/\*.*?\*\/|\/\/.*?$)"),
        'MAN_CONFIG_BLOCK': re_compile(
            r"\nCONFIGURATION(.*?)\n\w",
            DOTALL
        ),
        'MAN_GROUP': re_compile(
            r"\n {3}(?P<group>\w.*?)\n(?P<contents>(.(?!\n {3}\w|$))*)",
            DOTALL
        ),
        'MAN_ITEM': re_compile(
            r"(?:^|\n\n) {7}-(?!no-)(?P<key>[\w-]+).*?\n\n(?P<man>(.(?!\n\n {7}-\w|$))*.(?!$))",
            DOTALL
        ),
        'CLEAN_GROUP': re_compile(r" settings? ?"),
        'CLEAN_MAN': [
            [
                re_compile(r"^ {7}", MULTILINE),
                ''
            ],
            [
                re_compile(r" (\w+)‐\n([^\s])"),
                r" \1\2"
            ],
            [
                re_compile(r"(\w+)\n([^\s])"),
                r"\1 \2"
            ]
        ]
    }

    def __init__(self):
        self.config = OrderedDict()

    def assign_rasi_entry(self, key_value_match, destination='default'):
        key = key_value_match.group('key')
        value = key_value_match.group('value')
        if key in self.config:
            setattr(self.config[key], destination, value)
        else:
            arg_dict = {'key_name': key}
            arg_dict[destination] = value
            self.config[key] = Entry(**arg_dict)

    def parse_rasi(self, rasi, destination='default'):
        for discovered_entry in finditer(self.PATTERNS['RASI_ENTRY'], rasi):
            self.assign_rasi_entry(discovered_entry, destination)

    def load_default_config(self):
        raw = check_output(['rofi', '-no-config', '-dump-config'])
        self.parse_rasi(raw, 'default')

    def load_current_config(self):
        raw = check_output(['rofi', '-dump-config'])
        raw_cleaned = sub(self.PATTERNS['RASI_COMMENT'], '', raw)
        self.parse_rasi(raw_cleaned, 'current')

    def process_config(self):
        for _, entry in self.config.iteritems():
            entry.process_entry()

    def clean_entry_man(self, contents):
        for substitution in self.PATTERNS['CLEAN_MAN']:
            contents = sub(
                substitution[0],
                substitution[1],
                contents,
                0
            )
        return contents

    def parse_man_entry(self, group, man_entry_match):
        key = man_entry_match.group('key')
        if key in self.config:
            man = self.clean_entry_man(man_entry_match.group('man'))
            if man:
                setattr(self.config[key], 'group', group)
                setattr(self.config[key], 'man', man)

    def parse_man_group(self, man_group_match):
        group = sub(
            self.PATTERNS['CLEAN_GROUP'],
            '',
            man_group_match.group('group')
        )
        for discovered_entry in finditer(
            self.PATTERNS['MAN_ITEM'],
            man_group_match.group('contents')
        ):
            self.parse_man_entry(group, discovered_entry)

    def parse_man_config(self, man_config_match):
        for discovered_group in finditer(
            self.PATTERNS['MAN_GROUP'],
            man_config_match
        ):
            self.parse_man_group(discovered_group)

    def load_man(self):
        raw = check_output(['man', 'rofi'])
        possible_config = search(self.PATTERNS['MAN_CONFIG_BLOCK'], raw)
        if possible_config:
            self.parse_man_config(possible_config.group())

    def build(self):
        self.load_default_config()
        self.load_current_config()
        self.load_man()
        self.process_config()

    def to_rasi(self):
        output = "configuration {\n"
        for key in self.config:
            output += "    %s\n" % self.config[key].to_rasi()
        output += "}\n"
        return output

    def save(self, path=None):
        if path is None:
            path = self.DEFAULT_PATH
        with open(path, 'w') as rasi_file:
            rasi_file.write(self.to_rasi())
