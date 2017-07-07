from ...parse import parmatter_registry
from ...cande.pipe.steel import Steel1, Steel2A, Steel2DWSD, Steel2DLRFD, Steel2b, Steel2c, Steel2d, Steel3ADLRFD

steel_types = Steel1, Steel2A, Steel2DWSD, Steel2DLRFD, Steel2b, Steel2c, Steel2d, Steel3ADLRFD

for steel_type in steel_types:
    exec('{} = parmatter_registry[steel_type]'.format(steel_type._name))

del steel_type
del steel_types
del parmatter_registry
