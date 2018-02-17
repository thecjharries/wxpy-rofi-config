# coding=utf8

"""This file provides the Entry class"""

from re import compile as re_compile, IGNORECASE, match as re_match, sub


class Entry(object):
    """The Entry class attempts to describe a single settings entry"""
    DEFAULTS = {
        'key_name': None,
        'var_type': 'unknown',
        'group': 'Miscellaneous',
        'default': None,
        'current': None,
        'help_value': None,
        'help_type': None,
        'man': None,
    }

    CLEAN_PATTERNS = {
        'key_name': re_compile(r"_"),
        'number': re_compile(r"[^\d\-\.]"),
        'string': re_compile(r"(^(\"|')|(\"|')$)")
    }

    VAR_TYPE_VALUE_PATTERNS = {
        'string': re_compile(r"^(\"|'|null)", IGNORECASE),
        'number': re_compile(r"^[\d\-\.]+$"),
        'boolean': re_compile(r"(true|false)", IGNORECASE)
    }

    VAR_TYPE_KEY_PATTERNS = {
        'key': re_compile(r"^kb-"),
        'mouse': re_compile(r"^m(e|l)-"),
        'string': re_compile(r"^display-")
    }

    GROUP_KEY_PATTERNS = {
        'Mouse': VAR_TYPE_KEY_PATTERNS['mouse'],
        'Keybindings': VAR_TYPE_KEY_PATTERNS['key'],
        'Display': re_compile(r"^display-")
    }

    key_name = None
    var_type = DEFAULTS['var_type']
    group = DEFAULTS['group']
    default = None
    current = None
    help_value = None
    help_type = None
    man = None

    def __init__(self, **kwargs):
        for key, value in self.DEFAULTS.items():
            if key in kwargs:
                result = kwargs[key]
                del kwargs[key]
            else:
                result = value
            setattr(self, key, result)

    def assign_current(self):
        """Checks if current exists and copies default if it's not"""
        if not self.current and self.default:
            self.current = self.default

    def attempt_to_clean_values(self):
        """
        Looks at the entry's type and available cleaning methods to clean both
        current and default
        """
        cleaner_method = "clean_%s" % self.var_type
        if hasattr(self, cleaner_method):
            callable_method = getattr(self, cleaner_method)
            self.default = callable_method(self.default)
            self.current = callable_method(self.current)

    def force_var_type(self, hint=None):  # pylint: disable=unused-argument
        """
        Forces a variable type. Defaults to string. Only used as a last resort.
        """
        if self.is_number(self.default) and self.is_number(self.current):
            return 'number'
        return 'string'

    def get_type_from_help(self, hint=None):  # pylint: disable=unused-argument
        """
        Attempts to set the type from the help option.

        It seems like this would be a no-brainer, but I'd like to experiment
        with some enums and the like before just giving in here. Especially
        when it's an input binding. Something more than a string is useful.
        """
        if self.help_type:
            return self.help_type
        return self.var_type

    def ensure_useful_var_type(self):
        """Runs all available methods to determine the setting's type."""
        calls = [
            [self.force_var_type, None],
            [self.get_type_from_help, None],
            [self.guess_var_type_from_value, self.current],
            [self.guess_var_type_from_value, self.default],
            [self.guess_var_type_from_key, self.key_name],
        ]
        while 'unknown' == self.var_type and calls:
            current_call = calls.pop()
            self.var_type = current_call[0](current_call[1])

    def look_for_useful_group(self):
        """Attempts to find a more useful group using available methods"""
        if self.DEFAULTS['group'] == self.group:
            self.group = self.guess_group_from_key(self.key_name)

    def process_entry(self):
        """
        Assigns a current variable, generates a variable type, cleans values
        where possible, and looks for a better group
        """
        self.assign_current()
        self.ensure_useful_var_type()
        self.attempt_to_clean_values()
        self.look_for_useful_group()

    def to_rasi(self):
        """Converts the entry to a rasi line format."""
        if 'number' == self.var_type:
            return "%s: %d;" % (self.key_name, self.current)
        elif 'boolean' == self.var_type:
            return ("%s: %s;" % (self.key_name, self.current)).lower()
        elif 'string' == self.var_type:
            return '%s: "%s";' % (self.key_name, self.current)
        return "%s: %s;" % (self.key_name, self.current)

    @staticmethod
    def clean_key_name(key):
        """Cleans key_name"""
        return sub(Entry.CLEAN_PATTERNS['key_name'], '-', key)

    @staticmethod
    def clean_number(value):
        """Cleans numbers"""
        return int(sub(Entry.CLEAN_PATTERNS['number'], '', value))

    @staticmethod
    def clean_string(value):
        """Cleans strings"""
        if value:
            return sub(
                Entry.CLEAN_PATTERNS['string'],
                '',
                value
            )
        return ''

    @staticmethod
    def clean_boolean(value):
        """Cleans booleans"""
        return 'true' == value

    @staticmethod
    def is_number(value):
        """Checks if a value could be a number"""
        try:
            int(Entry.clean_string(value))
            return True
        except (ValueError, TypeError):
            pass
        return False

    @staticmethod
    def guess_something_from_patterns(value, pattern_dict, default):
        """
        Using patterns, attempts to discover a match for value. If one is not
        found, returns default.
        """
        for key, pattern in pattern_dict.items():
            if value and re_match(pattern, value):
                return key
        return default

    @staticmethod
    def guess_var_type_from_value(value):
        """Attempts to guess type from value"""
        return Entry.guess_something_from_patterns(
            value,
            Entry.VAR_TYPE_VALUE_PATTERNS,
            Entry.DEFAULTS['var_type']
        )

    @staticmethod
    def guess_var_type_from_key(value):
        """Attempts to guess type from the key"""
        return Entry.guess_something_from_patterns(
            value,
            Entry.VAR_TYPE_KEY_PATTERNS,
            Entry.DEFAULTS['var_type']
        )

    @staticmethod
    def guess_group_from_key(value):
        """Attempts to guess the group from the key"""
        return Entry.guess_something_from_patterns(
            value,
            Entry.GROUP_KEY_PATTERNS,
            Entry.DEFAULTS['group']
        )
