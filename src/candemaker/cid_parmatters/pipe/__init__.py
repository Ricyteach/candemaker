from ..cid_parmatters import prefix_spec, Pardef, s10, d5, f10, CANDE_formatter

types = 'alum basic concrete plastic steel'.split()
modules = (t+'_parmatters' for t in types)
for m in modules:
    exec('from .{} import __dict__ as d'.format(m))
    for obj in d:
        if obj.startswith('B'):
            exec('from .{} import {}'.format(m, obj))
    del d
    
del m
del modules
del types