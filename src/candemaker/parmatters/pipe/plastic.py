from ...parse import parmatter_registry
from ...cande.pipe.plastic import Plastic1, Plastic2, Plastic3AGeneral, Plastic3ASmooth, Plastic3AProfile, Plastic3bAProfile, Plastic3DWSD, Plastic3DLRFD, Plastic4

plastic_types = Plastic1, Plastic2, Plastic3AGeneral, Plastic3ASmooth, Plastic3AProfile, Plastic3bAProfile, Plastic3DWSD, Plastic3DLRFD, Plastic4

for plastic_type in plastic_types:
    exec('{} = parmatter_registry[plastic_type]'.format(plastic_type._name))

del plastic_type
del plastic_types
del parmatter_registry
