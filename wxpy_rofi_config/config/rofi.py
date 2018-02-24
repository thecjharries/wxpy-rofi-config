# coding=utf8

"""This file provides the Rofi class"""

from collections import OrderedDict
from filecmp import cmp as file_cmp
from os import environ
from os.path import exists, expanduser, join
from re import (
    compile as re_compile,
    DOTALL,
    finditer,
    IGNORECASE,
    MULTILINE,
    search,
    sub,
    VERBOSE
)
from shutil import copyfile
from subprocess import check_output

from wxpy_rofi_config.config import Entry


class Rofi(object):  # pylint: disable=too-many-public-methods
    """Rofi holds all the config for rofi"""

    PATTERNS = {
        'RASI_ENTRY': re_compile(
            r"^.*?(?:\s|\/|\*)(?P<key>[a-z][a-z0-9-]*):\s*(?P<value>.*?);.*?$",
            MULTILINE
        ),
        'RASI_COMMENT': re_compile(r"(\/\*.*?\*\/|\/\/.*?$)", MULTILINE),
        'MAN_CONFIG_BLOCK': re_compile(
            r"\nconfiguration(.*?)\n\w",
            DOTALL | IGNORECASE
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
                re_compile(r" (\w+)(?:‐|-)\n([^\s])"),
                r" \1\2"
            ],
            [
                re_compile(r"(\w+)\n([^\s])"),
                r"\1 \2"
            ]
        ],
        'HELP_BLOCK': re_compile(
            r"\n?global options:(?P<contents>.*?)(?:\n\n)",
            DOTALL | IGNORECASE
        ),
        'HELP_ENTRY': re_compile(
            r"""
            ^\s+-(?:\[no-\])?               # Preface stuff; skip it
            (?P<key>[a-z0-9-]+?)            # The entry key
            (?:\s+\[(?P<help_type>\w+)\])?  # Type info is not always there
            \s+(?P<help_value>.*?)$         # The short help string
            """,
            MULTILINE | VERBOSE
        ),
        'HELP_ACTIVE_FILE': re_compile(
            r"^.*?configuration\s+file:\s+(?P<file_path>.*?)$",
            MULTILINE | IGNORECASE
        ),
        'HELP_AVAILABLE_MODI_BLOCK': re_compile(
            r"(?:detected modi:)(?P<modi>.*?\n)\n",
            DOTALL | IGNORECASE
        ),
        'HELP_MODI': re_compile(
            r"^\s+\*\s+\+?(?P<modi>.*?)$",
            MULTILINE | IGNORECASE
        )
    }

    def __init__(self):
        self.config = OrderedDict()
        self.groups = []
        self.active_file = None
        self.active_backup = None
        self.available_modi = []

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
        if not self.active_file:
            self.active_file = self.create_default_path()

    def clean_entry_man(self, contents):
        """Cleans a single man entry"""
        for substitution in self.PATTERNS['CLEAN_MAN']:
            contents = sub(
                substitution[0],
                substitution[1],
                contents,
                0
            )
        return contents.decode('utf8', 'ignore')

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

    def parse_help_modi(self, modi_group):
        """Parses out all available modi"""
        for discovered_modi in finditer(
                self.PATTERNS['HELP_MODI'],
                modi_group
        ):
            modi = discovered_modi.group('modi')
            if modi:
                self.available_modi.append(modi)

    def parse_help_modi_block(self, raw_help):
        """Parses help for the modi block"""
        possible_modi = search(
            self.PATTERNS['HELP_AVAILABLE_MODI_BLOCK'],
            raw_help
        )
        if possible_modi:
            self.parse_help_modi(possible_modi.group('modi'))

    def parse_help_active_file(self, raw_help):
        """Parses help for the active config file"""
        possible_file = search(
            self.PATTERNS['HELP_ACTIVE_FILE'],
            raw_help
        )
        if possible_file:
            self.active_file = possible_file.group('file_path')

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

    def parse_help_config_block(self, raw_help):
        """Parses help for the config block"""
        possible_config = search(self.PATTERNS['HELP_BLOCK'], raw_help)
        if possible_config:
            self.parse_help_config(possible_config)

    def load_help(self):
        """Loads rofi --help in an attempt to parse it"""
        raw = check_output(['rofi', '--help'])
        self.parse_help_config_block(raw)
        self.parse_help_active_file(raw)
        self.parse_help_modi_block(raw)

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

    def backup(self, source=None, destination=None, restore=False):
        """Backs up the provided config file"""
        if source is None:
            source = self.active_file
        if destination is None:
            destination = "%s.bak" % source
        self.active_backup = destination
        if restore:
            copyfile(destination, source)
        else:
            copyfile(source, destination)

    def write_config(self, path=None):
        """Writes the config to a file"""
        if path is None:
            path = self.active_file
        with open(path, 'w') as rasi_file:
            rasi_file.write(self.to_rasi())

    def save(self, path=None, backup_path=None, backup=True):
        """Saves the config file"""
        self.active_backup = None
        if backup:
            self.backup(path, backup_path)
        self.write_config(path)

    def can_restore(self):
        """Checks if the config can be restored"""
        active = self.active_file
        if active is None:
            active = Rofi.create_default_path()
        if not exists(active):
            return False
        backup = self.active_backup
        if backup is None:
            backup = "%s.bak" % active
        if not exists(backup):
            return False
        return not file_cmp(active, backup)

    @staticmethod
    def create_default_path():
        """Creates the default save path"""
        if 'XDG_USER_CONFIG_DIR' in environ:
            lead = environ['XDG_USER_CONFIG_DIR']
        else:
            lead = join('~', '.config')
        return expanduser(join(lead, 'rofi', 'config.rasi'))
