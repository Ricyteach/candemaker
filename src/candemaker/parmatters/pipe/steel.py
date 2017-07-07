from ...parse import parmatter_registry
from ...cande.pipe import steel


steel_types = (NT for NT in vars(steel) if isinstance(NT, type) and not NT.__name__.startswith('_'))

for steel_type in steel_types:
    exec('{} = parmatter_registry[steel_type]'.format(steel_type._name))

del steel
del steel_types
del parmatter_registry
