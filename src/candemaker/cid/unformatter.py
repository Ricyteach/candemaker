# from collections import namedtuple as nt
# from . import format_specs as fs
from parmatter import FormatGroupMeta, VersatileParmatter
from mytools import update_special
from .. import reg
from .linedef import linedef_reg
from .prefix import prefix_reg


'''
class FileParseError(Exception):
    pass

class RegistrationError(Exception):
    pass
'''


class CandeFieldGroup(FormatGroupMeta):
    _formatter_type = VersatileParmatter
    _sep = ''


def CandeFieldGroup_factory(name, linedef):
    namespace = {f.name: (f.spec, f.default) for f in linedef}
    update_special(namespace, _prefix=prefix_reg[name])
    return CandeFieldGroup(name, (), namespace)


# cid file generator mapping
unformatter_reg = reg.CidRegistry()

for name, linedef in linedef_reg.items():
    unformatter_reg[name] = CandeFieldGroup_factory(name, linedef)


'''
def register_cid_generator(cande_obj, cid_generator):
    '''#Add cande objects to the cid generator registry
'''
    try:
        gen_registry[cande_obj] = cid_generator
    except AttributeError as e:
        raise RegistrationError('Failed to register {} with generator registry'.format(type(cande_obj).__name__)) from e

# cid file formatter mapping
parmatter_reg = {}

def register_cid_parmatter(cande_obj, obj_dict):
    '''#Add cande objects to the cande parser registry
'''
    try:
        parmatter = CANDE_unformatter_factory(cande_obj, obj_dict)
        parmatter_registry[cande_obj] = parmatter
    except AttributeError as e:
        raise RegistrationError('Failed to register {} with parmatter registry'.format(type(cande_obj).__name__)) from e


UnformatLine = nt('UnformatFile', 'type obj')

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
'''