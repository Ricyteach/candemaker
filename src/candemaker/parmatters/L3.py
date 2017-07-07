from ..parse import parmatter_registry
from ..cande.L3 import PipeGroup, L3Info, L3Control, Node, NodeLast, Element, TriaElement, QuadElement, SoilElement, BeamElement, InterfElement, ElementLast, Bound, ForceBound, SideBound, BotBound, CornerBound, BoundLast

L3_types = PipeGroup, L3Info, L3Control, Node, NodeLast, Element, TriaElement, QuadElement, SoilElement, BeamElement, InterfElement, ElementLast, Bound, ForceBound, SideBound, BotBound, CornerBound, BoundLast

for L3_type in L3_types:
    exec('{} = parmatter_registry[L3_type]'.format(L3_type._name))

del L3_type
del L3_types
del parmatter_registry
