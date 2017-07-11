from mytools import update_special
import logging

logger = logging.getLogger(__name__)

def register(module, attr, registry):
    '''Register a module attribute to a registry'''
    try:
        mod_registry = getattr(module, attr)
        update_special(registry, mod_registry)
    except AttributeError:
        logger.debug('No {} object in {} module'
                    ''.format(attr, module.__name__))
    else:
        logger.debug('Registered {:d} objects in {} module'
                    ''.format(len(mod_registry), module.__name__))


'''
def register(cande_obj, obj_dict, cid_generator):
    'Register cid definitions'
    register_cid_generator(cande_obj, cid_generator)
    register_cid_parmatter(cande_obj, obj_dict)
'''