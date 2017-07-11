from mytools import update_special
import logging
from types import ModuleType
from .. import register

logger = logging.getLogger(__name__)

gen = {}

def register_all():
    '''Register cid definitions from cid modules'''
    logger.debug('cid generator registration starting')
    from . import cid, L3, soil, pipe
    modules = cid, L3, soil, *(getattr(pipe, item) for item in vars(pipe) if isinstance(getattr(pipe, item), ModuleType))
    for module in modules:
        register(module, attr='reg_dict', registry=gen)
    logger.debug('cid generator registration complete:')
    logger.debug(', '.join(gen.keys()))
