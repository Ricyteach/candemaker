from ...parse import parmatter_registry
from ...cande.pipe import plastic


plastic_types = (NT for NT in vars(plastic) if isinstance(NT, type) and not NT.__name__.startswith('_'))

for plastic_type in plastic_types:
    exec('{} = parmatter_registry[plastic_type]'.format(plastic_type._name))

del plastic
del plastic_types
del parmatter_registry
