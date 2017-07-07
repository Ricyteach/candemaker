from ...parse import parmatter_registry
from ...cande.pipe.concrete import Concrete1, Concrete2, Concrete3, Concrete4Case1_2, Concrete4Case3, Concrete4bCase3, Concrete4Case4, Concrete4Case5, Concrete5

concrete_types = Concrete1, Concrete2, Concrete3, Concrete4Case1_2, Concrete4Case3, Concrete4bCase3, Concrete4Case4, Concrete4Case5, Concrete5

for concrete_type in concrete_types:
    exec('{} = parmatter_registry[concrete_type]'.format(concrete_type._name))

del concrete_type
del concrete_types
del parmatter_registry
