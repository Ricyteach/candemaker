from ...parse import parmatter_registry
from ...cande.pipe import concrete


concrete_types = (NT for NT in vars(concrete) if isinstance(NT, type) and not NT.__name__.startswith('_'))

for concrete_type in concrete_types:
    exec('{} = parmatter_registry[concrete_type]'.format(concrete_type._name))

del concrete
del concrete_types
del parmatter_registry
