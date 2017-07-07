from ..parse import parmatter_registry
from .. import cande

universal_types = cande.Master, cande.Factor

for universal_type in universal_types:
    exec('{} = parmatter_registry[universal_type]'.format(universal_type._name))

del universal_type
del universal_types
del parmatter_registry
