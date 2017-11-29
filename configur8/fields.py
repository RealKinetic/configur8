"""
"""

from .util import missing


class FieldError(Exception):
    pass


class BaseField(object):
    def __init__(self, required, override, help):
        self.required = required
        self.override = override
        self.help = help

    def validate(self, value, errors=None):
        errors = errors or []

        if self.required and value is missing:
            errors.append('required value')

            return errors

        if value is not missing and not isinstance(value, self.type):
            errors.append('{!r} type required (received {!r})'.format(
                self.type,
                type(value)
            ))

        return errors


class StringField(BaseField):
    type = basestring


class IntegerField(BaseField):
    type = (int, long)


class BooleanField(BaseField):
    type = bool


class ListField(BaseField):
    type = (list, tuple)


class DictField(BaseField):
    type = dict


def field_from_type(type_, *args, **kwargs):
    field_cls = None

    if type_ == 'string':
        field_cls = StringField
    elif type_ == 'int':
        field_cls = IntegerField
    elif type_ == 'bool':
        field_cls = BooleanField
    elif type_ == 'list':
        field_cls = ListField
    elif type_ == 'dict':
        field_cls = DictField

    if not field_cls:
        raise FieldError('Unknown type {!r}'.format(type_))

    return field_cls(*args, **kwargs)
