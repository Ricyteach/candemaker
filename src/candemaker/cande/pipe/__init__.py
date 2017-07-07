from . import alum
# from . import basic
# from . import concrete
from . import plastic
from . import steel


parse_dict = dict(
        ALUMINUM=alum.Alum_gen,
        BASIC=NotImplemented,
        CONCRETE=NotImplemented,
        PLASTIC=plastic.Plastic_gen,
        STEEL=steel.Steel_gen,
        CONRIB=NotImplemented,
        CONTUBE=NotImplemented
        )

'''
Key
===

A:      cid.mode == 'ANALYS' only
D:      cid.mode == 'DESIGN' only
AD:     cid.mode == 'ANALYS' or 'DESIGN'
WSD:    cid.method == 0 only
LRFD:   cid.method == 1 only
'''
