# basic and concrete not yet implemented

modules = 'alum plastic steel'.split()
for m in modules:
    exec('from .{} import __dict__ as d'.format(m))
    for obj in d:
        if obj.startswith('B'):
            exec('from .{} import {}'.format(m, obj))
    del d
    
del m
del modules

from . import alum
# from . import basic
# from . import concrete
from . import plastic
from . import steel
