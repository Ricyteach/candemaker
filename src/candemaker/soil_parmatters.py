from .cid_parmatters import Pardef, d5, f10, CANDE_formatter

class D1(metaclass=CANDE_formatter):
    _prefix = prefix_spec.format('D-1')
    Limit = Pardef(s1, ' ')
    ID = Pardef(d4, 0)
    # 1: isotropic, 2: orthotropic, 3: Duncan/Seling, 4: Overburden Dependent,
    # 5: Extended Hardin, 6: Interface, 7: Composite Link, 8: Mohr/Coulomb
    Model = Pardef(d5, 1)
    Density = Pardef(f10, 0)
    Name = Pardef(s20, '')
    Layers = Pardef(d2, 0)
    
