import logging
import sys

handler = logging.StreamHandler(stream=sys.stdout)
handler.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

logger.info('candemaker initialized')

from . import cid
from .cid import linedef
from .cid.enum import CidEnum
from .obj import *
from .cande import CandeObj, CandeNT
# from . import parmatters
from . import reg

#  reg.register_all()

logger.info('candemaker initialization complete')

#  __all__ = 'cid linedef'.split()
