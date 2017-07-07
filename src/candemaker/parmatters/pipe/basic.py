from ...parse import parmatter_registry
from ...cande.pipe.basic import Basic1, Basic2

basic_types = Basic1, Basic2

for basic_type in basic_types:
    exec('{} = parmatter_registry[basic_type]'.format(basic_type._name))

del basic_type
del basic_types
del parmatter_registry
