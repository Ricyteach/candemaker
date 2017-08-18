from ... import format_specs as fs
from ..general import line

'''
from ..parmatters import prefix_spec, Pardef, d5, f10, CANDE_formatter

class B1Basic(metaclass=CANDE_formatter):
    # ANALYS only
    # repeatable (multiple properties in one pipe group)
    _prefix = prefix_spec.format('B-1.Basic')
    First = Pardef(d5, 0)
    Last = Pardef(d5, 0)
    Modulus = Pardef(f10, 0) # psi
    Poissons = Pardef(f10, 0)
    Area = Pardef(f10, 0) # in2/in
    I = Pardef(f10, 0) # in4/in
    Load = Pardef(f10, 0) # lbs/in
    
class B2Basic(metaclass=CANDE_formatter):
    # for ANALYS mode only
    _prefix = prefix_spec.format('B-2.Basic')
    # Small Deformation: 0, Large Deformation: 1, Plus Buckling: 2
    Mode = Pardef(d5, 0)
'''