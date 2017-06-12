from ..cid_parmatters import Pardef, d5, f10, CANDE_formatter

class B1Alum(metaclass=CANDE_formatter):
    _prefix = prefix_spec.format('B-1.Alum')
    Modulus = Pardef(f10, 10E6) # psi
    Poissons = Pardef(f10, 0.33)
    Yield = Pardef(f10, 24E3) # psi
    Seam = Pardef(f10, 24E3) # psi
    Density = Pardef(f10, 0) # pci
    UpperModulus = Pardef(f10, 0.05*10E6) # psi
    Behavior = Pardef(d5, 2) # Linear: 1, Bilinear: 2
    # Small Deformation: 0, Large Deformation: 1, Plus Buckling: 2
    Mode = Pardef(d5, 0)
    
class B2AlumA(metaclass=CANDE_formatter):
    # for ANALYS mode only
    _prefix = prefix_spec.format('B-2.Alum.A')
    Area = Pardef(f10, 0) # in2/in
    I = Pardef(f10, 0) # in4/in
    S = Pardef(f10, 0) # in3/in
    
class B2AlumDWSD(metaclass=CANDE_formatter):
    # for DESIGN mode only and no LRFD only
    _prefix = prefix_spec.format('B-2.Alum.D.WSD')
    YieldFS = Pardef(f10, 3)
    BucklingFS = Pardef(f10, 2)
    SeamFS = Pardef(f10, 2)
    PlasticFS = Pardef(f10, 4)
    Deflection = Pardef(f10, 5) # percent
    
class B2AlumDLRFD(metaclass=CANDE_formatter):
    # for DESIGN mode and LRFD mode only
    _prefix = prefix_spec.format('B-2.Alum.D.LRFD')
    Yield = Pardef(f10, 1)
    Buckling = Pardef(f10, 1)
    Seam = Pardef(f10, 1)
    Plastic = Pardef(f10, 1)
    Deflection = Pardef(f10, 1)
    
class B3AlumADLRFD(metaclass=CANDE_formatter):
    # LRFD only
    _prefix = prefix_spec.format('B-3.Alum.AD.LRFD')
    Yieldϕ = Pardef(f10, 1)
    Bucklingϕ = Pardef(f10, 1)
    Seamϕ = Pardef(f10, 0.67)
    Plasticϕ = Pardef(f10, 0.85)
    Deflection = Pardef(f10, 5) # percent
    
