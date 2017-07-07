from ...parse import parmatter_registry
from ...cande import soil


soil_types = (NT for NT in vars(soil) if isinstance(NT, type) and not NT.__name__.startswith('_'))

for soil_type in soil_types:
    exec('{} = parmatter_registry[soil_type]'.format(soil_type._name))

del soil
del soil_types
del parmatter_registry
