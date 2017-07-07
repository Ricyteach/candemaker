from ...parse import parmatter_registry
from ...cande.pipe.alum import Alum1, Alum2A, Alum2DLRFD, Alum2DWSD, Alum3ADLRFD

alum_types = Alum1, Alum2A, Alum2DLRFD, Alum2DWSD, Alum3ADLRFD

for alum_type in alum_types:
    exec('{} = parmatter_registry[alum_type]'.format(alum_type._name))

del alum_type
del alum_types
del parmatter_registry
