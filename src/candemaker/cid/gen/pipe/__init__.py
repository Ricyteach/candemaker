from . import alum
# from . import basic
# from . import concrete
from . import plastic
from . import steel


lookup = dict(
            ALUMINUM=alum.B1Alum,
            BASIC=NotImplemented,
            CONCRETE=NotImplemented,
            PLASTIC=plastic.B1Plastic,
            STEEL=steel.B1Steel,
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
