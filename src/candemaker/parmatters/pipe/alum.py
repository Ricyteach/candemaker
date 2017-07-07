from ...parse import parmatter_registry
from ...cande.pipe import alum


alum_types = (NT for NT in vars(alum) if isinstance(NT, type) and not NT.__name__.startswith('_'))

for alum_type in alum_types:
    exec('{} = parmatter_registry[alum_type]'.format(alum_type._name))

del alum
del alum_types
del parmatter_registry
