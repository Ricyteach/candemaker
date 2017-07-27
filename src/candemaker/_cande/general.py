from collections import namedtuple as nt

__all__ = ()

def add_specs_defaults_to_nts(obj, d):
    obj._field_specs = tuple(d[field_name].spec for field_name in obj._fields)
    obj._defaults = tuple(d[field_name].default for field_name in obj._fields)
