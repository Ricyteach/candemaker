modules = ['soil']
for m in modules:
    exec('from .{} import __dict__ as d'.format(m))
    for obj in d:
        if obj.startswith('D'):
            exec('from .{} import {}'.format(m, obj))
    del d
    
del m
del modules