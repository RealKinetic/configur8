"""
Configur8 is meant to help tame the beast that is configuration.
"""

from . import schema, util

__all__ = [
    'Config',
]


class UnknownConfigKey(Exception):
    pass


class ConfigAlreadySet(Exception):
    """
    Raised when there is an attempt to set a config key but there is already a
    value and the schema has set the key to override: false.
    """


class Config(object):
    def __init__(self, schema_file=None):
        self.schema = None
        self.config = {}

        if schema_file:
            self.load_schema(schema_file)

    def load_schema(self, schema_file):
        """
        Load a schema from a file
        """
        self.schema = schema.load_file(schema_file)

    def validate(self):
        self.schema.validate(self)

    def populate(self, dest):
        for key, value in self.config.copy().iteritems():
            dest[key] = value['value']

    def load_from_py(self, filename):
        config_values = {}

        execfile(filename, {}, config_values)

        for key, value in config_values.iteritems():
            if not key.isupper():
                continue

            self.set_value(key, value, filename)

    def set_value(self, key, value, source=None):
        """
        Attempt to set a value for a configuration key.
        """
        if key not in self.schema:
            raise UnknownConfigKey(
                'Trying to set {!r} but it is not listed in the schema'.format(
                    key
                )
            )

        existing_config = self.config.get(key, None)

        if existing_config and not self.schema.is_overridable(key):
            raise ConfigAlreadySet(
                'Attempt to change config for {!r} failed. '
                'Attempted in {!r} but already set in {!r}.'.format(
                    key,
                    source or '<unknown>',
                    existing_config['source'] or '<unknown>'
                )
            )

        self.config[key] = {
            'value': value,
            'source': source,
        }

    def __setitem__(self, key, value):
        # maybe we can use the stack to guestimate the source
        self.set_value(key, value)

    def get(self, key, default=None):
        value = self.config.get(key, util.missing)

        if value is util.missing:
            return default

        if value:
            return value['value']

    def __repr__(self):
        return repr(self.config)

    def as_dict(self):
        ret = {}

        self.populate(ret)

        return ret
