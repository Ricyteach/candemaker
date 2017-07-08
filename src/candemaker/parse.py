from parmatter import FormatGroupMeta, VersatileParmatter
from mytools.utilities import update_special
from .format_specs import prefix_spec

class FileParseError(Exception):
    pass

class RegistrationError(Exception):
    pass

class CANDE_formatter(FormatGroupMeta):
    _formatter_type = VersatileParmatter
    _sep = ''

def CANDE_formatter_factory(cande_obj, obj_dict):
    namespace = obj_dict.copy()
    update_special(namespace, _prefix=prefix_spec.format(cande_obj._prefix))
    return CANDE_formatter(cande_obj._name, (), namespace)

# cid file generator mapping
gen_registry = {}

def register_cid_generator(cande_obj, cid_generator):
    '''Add cande objects to the cid generator registry'''
    try:
        gen_registry[cande_obj] = cid_generator
    except AttributeError as e:
        raise RegistrationError('Failed to register {} with generator registry'.format(type(cande_obj).__name__)) from e

# cid file formatter mapping
parmatter_registry = {}

def register_cid_parmatter(cande_obj, obj_dict):
    '''Add cande objects to the cande parser registry'''
    try:
        parmatter = CANDE_formatter_factory(cande_obj, obj_dict)
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
