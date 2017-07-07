from itertools import zip_longest
from collections import namedtuple as nt
from .parse import register_cid_parmatter, register_cid_generator


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
    method = cid.method
    if method == 1:  # LRFD
        generators = (A1_gen, A2_gen, C1_gen, D1_gen, E1_gen)
        labels = 'Master PipeGroup Problem Materials Factors'.split()
    elif method == 0:  # WSD
        generators = (A1_gen, A2_gen, C1_gen, D1_gen)
        labels = 'Master PipeGroup Problem Materials'.split()
    for obj_type in parse_file(cid, struct, generators, labels):
        line_type = lookup_linetype[obj_type]
        yield UnformatLine(line_type, obj_type)
