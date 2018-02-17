# coding=utf8

"""This file provides the Rofi class"""

from collections import OrderedDict
from os.path import expanduser, join
from re import compile as re_compile, DOTALL, finditer, MULTILINE, search, sub
from subprocess import check_output

from wxpy_rofi_config.config import Entry


class Rofi(object):
    """Rofi holds all the config for rofi"""

    DEFAULT_PATH = expanduser(join('~', '.config', 'rofi', 'config.rasi'))

    PATTERNS = {
        'RASI_ENTRY': re_compile(
            r"^.*?(?:\s|\/|\*)(?P<key>[a-z][a-z0-9-]*):\s*(?P<value>.*?);.*?$",
            MULTILINE
        ),
        'RASI_COMMENT': re_compile(r"(\/\*.*?\*\/|\/\/.*?$)", MULTILINE),
        'MAN_CONFIG_BLOCK': re_compile(
            r"\nCONFIGURATION(.*?)\n\w",
            DOTALL
        ),
        'MAN_GROUP': re_compile(
            r"\n {3}(?P<group>\w.*?)\n(?P<contents>(.(?!\n {3}\w|$))*)",
            DOTALL
        ),
        'MAN_ITEM': re_compile(
            r"(?:^|\n\n) {7}-(?!no-)(?P<key>[\w-]+).*?\n\n(?P<man>(.(?!\n\n {7}-\w|$))*.?)",
            DOTALL
        ),
        'CLEAN_GROUP': re_compile(r" settings? ?"),
        'CLEAN_MAN': [
            [
                re_compile(r"^ {7}", MULTILINE),
                ''
            ],
            [
                re_compile(r" (\w+)(‐|-)\n([^\s])"),
                r" \1\2"
            ],
            [
                re_compile(r"(\w+)\n([^\s])"),
                r"\1 \2"
            ]
        ],
        'HELP_BLOCK': re_compile(
            r"\nGlobal options:(.*?)(?:\n\n)",
            DOTALL
        ),
        'HELP_ENTRY': re_compile(
            r"^\s+-(?:\[no-\])?(?P<key>[a-z0-9-]+?)(?:\s+\[(?P<help_type>\w+)\])?\s+(?P<help_value>.*?)$",
            MULTILINE
        )
    }

    def __init__(self):
        self.config = OrderedDict()
        self.groups = []

    def assign_rasi_entry(self, key_value_match, destination='default'):
        """
        Given a match from a rasi file, attempts to pull values from the input.
        Assigns either default or current.
        """
        key = key_value_match.group('key')
        value = key_value_match.group('value')
        if key in self.config:
            setattr(self.config[key], destination, value)
        else:
            arg_dict = {'key_name': key}
            arg_dict[destination] = value
            self.config[key] = Entry(**arg_dict)

    def parse_rasi(self, rasi, destination='default'):
        """Parses the provided rasi string for entries"""
        for discovered_entry in finditer(self.PATTERNS['RASI_ENTRY'], rasi):
            self.assign_rasi_entry(discovered_entry, destination)

    def load_default_config(self):
        """
        Loads the default configuration.

        WARNING: This can actually create broken config depending on what you've
        got on your system. For example, the official file_browser example
        creates `display-file_browser`, which kills rofi.
        see: https://gitcrate.org/qtools/rofi-file_browser
        """
        raw = check_output(['rofi', '-no-config', '-dump-config'])
        self.parse_rasi(raw, 'default')

    def load_current_config(self):
        """
        Loads the currently active config (what exists of it)
        """
        raw = check_output(['rofi', '-dump-config'])
        raw_cleaned = sub(
            self.PATTERNS['RASI_COMMENT'],
            '',
            raw,
            0
        )
        self.parse_rasi(raw_cleaned, 'current')

    def process_config(self):
        """Process all entries for useful information"""
        for _, entry in self.config.items():
            entry.process_entry()
            if not entry.group in self.groups:
                self.groups.append(entry.group)

    def clean_entry_man(self, contents):
        """Cleans a single man entry"""
        for substitution in self.PATTERNS['CLEAN_MAN']:
            contents = sub(
                substitution[0],
                substitution[1],
                contents,
                0
            )
        return contents

    def parse_man_entry(self, group, man_entry_match):
        """Looks for a single man entry"""
        key = man_entry_match.group('key')
        if key in self.config:
            man = self.clean_entry_man(man_entry_match.group('man'))
            if man:
                setattr(self.config[key], 'group', group)
                setattr(self.config[key], 'man', man)

    def parse_man_group(self, man_group_match):
        """Looks for a group of settings in man"""
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
        """Looks for the config man section"""
        for discovered_group in finditer(
                self.PATTERNS['MAN_GROUP'],
                man_config_match
        ):
            self.parse_man_group(discovered_group)

    def load_man(self):
        """Loads man rofi"""
        raw = check_output(['man', 'rofi'])
        possible_config = search(self.PATTERNS['MAN_CONFIG_BLOCK'], raw)
        if possible_config:
            self.parse_man_config(possible_config.group())

    def parse_help_entry(self, help_entry_match):
        """Parses a single help entry"""
        key = help_entry_match.group('key')
        if key in self.config:
            help_value = help_entry_match.group('help_value')
            setattr(self.config[key], 'help_value', help_value)
            help_type = help_entry_match.group('help_type')
            if help_type:
                setattr(self.config[key], 'help_type', help_type)

    def parse_help_config(self, help_block_match):
        """Parses the entire help config block"""
        for discovered_entry in finditer(
                self.PATTERNS['HELP_ENTRY'],
                help_block_match.group('contents')
        ):
            self.parse_help_entry(discovered_entry)

    def load_help(self):
        """Loads rofi --help in an attempt to parse it"""
        raw = check_output(['rofi', '--help'])
        possible_config = search(self.PATTERNS['HELP_BLOCK'], raw)
        if possible_config:
            self.parse_help_config(possible_config)

    def build(self):
        """
        Loads defaults, adds current values, discovers available documentation,
        and processes all entries
        """
        self.load_default_config()
        self.load_current_config()
        self.load_help()
        self.load_man()
        self.process_config()

    def to_rasi(self):
        """Returns a rasi string composed of all its entries"""
        output = "configuration {\n"
        for key in self.config:
            output += "    %s\n" % self.config[key].to_rasi()
        output += "}\n"
        return output

    def save(self, path=None):
        """Saves the config file"""
        if path is None:
            path = self.DEFAULT_PATH
        with open(path, 'w') as rasi_file:
            rasi_file.write(self.to_rasi())
