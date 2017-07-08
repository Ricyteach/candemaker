from mytools import update_special
import logging
from types import ModuleType

logger = logging.getLogger(__name__)

gen = {}

def register(module, attr='reg_dict'):
    '''Register cid definitions in modules'''
    try:
        mod_registry = getattr(module, attr)
        update_special(gen, **mod_registry)
    except AttributeError:
        logger.debug('No {} object in {} module'
                    ''.format(attr, module.__name__))
    else:
        logger.debug('Registered {:d} objects in {} module'
                    ''.format(len(mod_registry), module.__name__))


def register_all():
    logger.debug('cid generator registration starting')
    from . import cid, L3, soil, pipe
    modules = cid, L3, soil, *(getattr(pipe, item) for item in vars(pipe) if isinstance(getattr(pipe, item), ModuleType))
    for module in modules:
        register(module)
    logger.debug('cid generator registration complete:')
    logger.debug(', '.join(gen.keys()))
