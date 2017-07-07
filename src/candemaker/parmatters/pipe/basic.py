from ...parse import parmatter_registry
from ...cande.pipe import basic


basic_types = (NT for NT in vars(basic) if isinstance(NT, type) and not NT.__name__.startswith('_'))

for basic_type in basic_types:
    exec('{} = parmatter_registry[basic_type]'.format(basic_type._name))

del basic
del basic_types
del parmatter_registry
