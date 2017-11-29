import yaml

from . import fields, util


class SchemaError(Exception):
    pass


class ValidationError(Exception):
    pass


class Schema(object):
    def __init__(self):
        self.mapping = {}

    def add_field(self, key, field):
        self.mapping[key] = field

    def validate(self, config):
        """
        Validate the supplied config dictionary.
        """
        errors = []

        for key, field in self.mapping.iteritems():
            config_value = config.get(key, util.missing)

            try:
                field_errors = field.validate(config_value)
            except Exception as exc:
                errors.append((key, str(exc)))
            else:
                if field_errors:
                    for fe in field_errors:
                        errors.append((key, fe))

        if errors:
            raise ValidationError(errors)

    def is_overridable(self, key):
        mapping = self.mapping.get(key, None)

        if not mapping:
            return False

        return mapping.override

    def __contains__(self, key):
        return key in self.mapping

    def __getitem__(self, key):
        return self.mapping[key]


def load_file(schema_file):
    """
    Load a schame from a YAML file.
    """
    with open(schema_file, 'rb') as fp:
        yaml_schema = yaml.load(fp)

    if 'config' not in yaml_schema:
        raise SchemaError(
            'No `config` root specified in {!r}'.format(schema_file)
        )

    schema_root = yaml_schema['config']

    if not isinstance(schema_root, dict):
        raise SchemaError('`config` must be a dictionary of Key -> mapping')

    schema = Schema()

    for key, mapping in schema_root.iteritems():
        try:
            field = field_from_mapping(mapping)
        except Exception as exc:
            raise SchemaError(
                'Error while processing {}: {}'.format(key, str(exc))
            )

        schema.add_field(key, field)

    return schema


def field_from_mapping(mapping):
    """
    Builds a `field.Field` from a yaml mapping
    """
    mapping = mapping.copy()

    try:
        field_type = mapping.pop('type')
    except KeyError:
        raise SchemaError('No `type` defined')

    return fields.field_from_type(field_type, **mapping)
