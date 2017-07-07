from parmatter import FormatGroupMeta, VersatileParmatter
from mytools.utilities import update_special
from .format_specs import prefix_spec

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
