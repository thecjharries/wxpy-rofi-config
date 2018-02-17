# pylint: disable=W,C,R
# coding=utf8

from re import compile as re_compile, IGNORECASE, match as re_match, sub


class Entry(object):
    DEFAULTS = {
        'key_name': None,
        'var_type': 'unknown',
        'group': 'Miscellaneous',
        'default': None,
        'current': None,
        'man': None
    }

    CLEAN_PATTERNS = {
        'key': re_compile(r"_"),
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
    group = DEFAULTS['group']
    var_type = DEFAULTS['var_type']

    def __init__(self, **kwargs):
        for key, value in self.DEFAULTS.iteritems():
            if key in kwargs:
                result = kwargs[key]
                del kwargs[key]
            else:
                result = value
            setattr(self, key, result)

    def assign_current(self):
        if not self.current and self.default:
            self.current = self.default

    def attempt_to_clean_values(self):
        cleaner_method = "clean_%s" % self.var_type
        if hasattr(self, cleaner_method):
            callable_method = getattr(self, cleaner_method)
            self.default = callable_method(self.default)
            self.current = callable_method(self.current)

    def force_var_type(self, hint=None):
        if self.is_number(self.default) and self.is_number(self.current):
            return 'number'
        return 'string'

    def ensure_useful_var_type(self):
        calls = [
            [self.force_var_type, None],
            [self.guess_var_type_from_value, self.current],
            [self.guess_var_type_from_value, self.default],
            [self.guess_var_type_from_key, self.key_name],
        ]
        while 'unknown' == self.var_type and calls:
            current_call = calls.pop()
            self.var_type = current_call[0](current_call[1])

    def look_for_useful_group(self):
        if self.DEFAULTS['group'] == self.group:
            self.group = self.guess_group_from_key(self.key_name)

    def process_entry(self):
        self.assign_current()
        self.ensure_useful_var_type()
        self.attempt_to_clean_values()
        self.look_for_useful_group()

    def to_rasi(self):
        if 'number' == self.var_type:
            return "%s: %d;" % (self.key_name, self.current)
        elif 'boolean' == self.var_type:
            return ("%s: %s;" % (self.key_name, self.current)).lower()
        return '%s: "%s";' % (self.key_name, self.current)

    @staticmethod
    def clean_config_key(key):
        return sub(Entry.CLEAN_PATTERNS['key'], '-', key)

    @staticmethod
    def clean_number(value):
        return int(sub(Entry.CLEAN_PATTERNS['number'], '', value))

    @staticmethod
    def clean_string(value):
        if value:
            return sub(
                Entry.CLEAN_PATTERNS['string'],
                '',
                value
            )
        return ''

    @staticmethod
    def clean_boolean(value):
        return 'true' == value

    @staticmethod
    def is_number(value):
        try:
            int(Entry.clean_string(value))
            return True
        except (ValueError, TypeError):
            pass
        return False

    @staticmethod
    def guess_something_from_patterns(value, pattern_dict, default):
        if value is None:
            value = ''
        for key, pattern in pattern_dict.iteritems():
            if re_match(pattern, value):
                return key
            # else:
            #     print(value)
        return default

    @staticmethod
    def guess_var_type_from_value(value):
        return Entry.guess_something_from_patterns(
            value,
            Entry.VAR_TYPE_VALUE_PATTERNS,
            Entry.DEFAULTS['var_type']
        )

    @staticmethod
    def guess_var_type_from_key(value):
        return Entry.guess_something_from_patterns(
            value,
            Entry.VAR_TYPE_KEY_PATTERNS,
            Entry.DEFAULTS['var_type']
        )

    @staticmethod
    def guess_group_from_key(value):
        return Entry.guess_something_from_patterns(
            value,
            Entry.GROUP_KEY_PATTERNS,
            Entry.DEFAULTS['group']
        )

# if 'false' and re_match(Entry.VAR_TYPE_VALUE_PATTERNS['boolean'], 'false'):
#     print('cool')
print(Entry.guess_var_type_from_value('false'))
