from ...parse import parmatter_registry
from ...cande.soil import Material, MaterialLast, Overburden, OverburdenLast, Isotropic, Orthotropic, Duncan2, Duncan3, Duncan4, Overburden2, Hardin, HardinTRIA, Interface, Composite, MohrCoulomb

soil_types = Material, MaterialLast, Overburden, OverburdenLast, Isotropic, Orthotropic, Duncan2, Duncan3, Duncan4, Overburden2, Hardin, HardinTRIA, Interface, Composite, MohrCoulomb

for soil_type in soil_types:
    exec('{} = parmatter_registry[soil_type]'.format(soil_type._name))

del soil_type
del soil_types
del parmatter_registry
