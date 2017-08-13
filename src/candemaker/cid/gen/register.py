from ..enum import CidRegistry
from .cid import A1, E1
from . import L3
from . import soil

class CidGenReg(CidRegistry):
    # required for assigning members to descriptors
    # (all functions are descriptors)
    _member_names = 'A1 E1 A2 C1 C2 C3 C4 C5 D1'.split()
    A1 = A1
    E1 = E1
    A2 = L3.A2
    C1 = L3.C1
    C2 = L3.C2
    C3 = L3.C3
    C4 = L3.C4
    C5 = L3.C5
    D1 = soil.D1
