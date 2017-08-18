from collections import namedtuple as nt

Field = nt('Field', 'name spec default')

def line(**field_defs):
    '''Return a cid file line definition composed of a tuple of fields'''
    return tuple(Field(n, s, d) for n, (s, d) in field_defs.items())

def defaults(linedef):
    '''Generate the defaults from a line definition sequence'''
    try:
        yield from (field.default for field in linedef)
    except AttributeError as e:
        raise TypeError('The lindef argument did not contain '
                        'valid fields') from e

def names(linedef):
    '''Generate the names from a line definition sequence'''
    try:
        yield from (field.name for field in linedef)
    except AttributeError as e:
        raise TypeError('The lindef argument did not contain '
                        'valid fields') from e
