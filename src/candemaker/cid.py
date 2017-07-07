from itertools import zip_longest
from collections import namedtuple as nt
from .parse import register_cid_parmatter, register_cid_generator, gen_registry, parmatter_registry

def register(cande_obj, obj_dict, cid_generator):
    '''Register cande objects'''
    register_cid_generator(cande_obj, cid_generator)
    register_cid_parmatter(cande_obj, obj_dict)


class FileParseError(Exception):
    pass

# General CID

UnformatLine = nt('UnformatFile', 'type obj')

CID = nt('CID', 'master pipes problem materials')
CIDLRFD = nt('CIDLRFD', 'master pipes problem materials factors')

def parse(cid, struct=None):
    if struct is None:
        yield from parse_cid(cid, struct)
    else:
        yield from parse_dict[struct[-1]](cid, struct)


def parse_file(source, structure, generators, labels=None):
    if labels is None:
        labels = []
    for gen, label in zip_longest(generators, labels, fill_value=''):
        try:
            for obj in gen(source, structure):
                structure.append(obj)
                yield obj
        except Exception as e:
            raise FileParseError('Failed to parse {!r} '
                                 'from {!r}'.format(label, gen)) from e


def parse_cid(cid, struct):
    from .cande import Master
    generators = gen_registry[Master],
    labels = 'Master',
    for obj_type in parse_file(cid, struct, generators, labels):
        line_type = parmatter_registry[obj_type]
        yield UnformatLine(line_type, obj_type)
