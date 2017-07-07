from ..parse import parmatter_registry
from ..cande import L3


L3_types = (NT for NT in vars(L3) if isinstance(NT, type) and not NT.__name__.startswith('_'))

for L3_type in L3_types:
    print(L3_type)
    input('\n')
    exec('{} = parmatter_registry[L3_type]'.format(L3_type._name))

del L3
del L3_types
del parmatter_registry
