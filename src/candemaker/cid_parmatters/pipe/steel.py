from . import prefix_spec, Pardef, d5, f10, CANDE_formatter

d4 = '{: >4d}'
f4 = '{: >4f}'

class B1Steel(metaclass=CANDE_formatter):
    _prefix = prefix_spec.format('B-1.Steel')
    Modulus = Pardef(f10, 29E6) # psi
    Poissons = Pardef(f10, 0.3)
    Yield = Pardef(f10, 33E3) # psi
    Seam = Pardef(f10, 33E3) # psi
    Density = Pardef(f10, 0) # pci
    UpperModulus = Pardef(f10, 0) # psi
    # None: 0, Yes: 1, Yes, print trace: 2
    JointSlip = Pardef(d5, 0)
    Behavior = Pardef(d5, 2) # Linear: 1, Bilinear: 2
    # Small Deformation AASHTO Buckling: 0
    # Large Deformation AASHTO Buckling: 1
    # Large Deformation CANDE Buckling:  2
    # Small Deformation Deep Corrugation Buckling: 3
    # Large Deformation Deep Corrugation Buckling: 4
    Mode = Pardef(d5, 0)
    
class B2SteelA(metaclass=CANDE_formatter):
    # for ANALYS only
    _prefix = prefix_spec.format('B-2.Steel.A')
    Area = Pardef(f10, 0) # in2/in
    I = Pardef(f10, 0) # in4/in
    S = Pardef(f10, 0) # in3/in
    Z = Pardef(f10, 0) # in3/in
    
class B2SteelDWSD(metaclass=CANDE_formatter):
    # for DESIGN only
    # Non LRFD only
    _prefix = prefix_spec.format('B-2.Steel.D.WSD')
    YieldFS = Pardef(f10, 2)
    BucklingFS = Pardef(f10, 2)
    SeamFS = Pardef(f10, 2)
    PlasticFS = Pardef(f10, 3)
    Deflection = Pardef(f10, 5) # percent
    
class B2SteelDLRFD(metaclass=CANDE_formatter):
    # for DESIGN only
    # LRFD only
    _prefix = prefix_spec.format('B-2.Steel.D.LRFD')
    Yield = Pardef(f10, 1)
    Buckling = Pardef(f10, 1)
    Seam = Pardef(f10, 1)
    Plastic = Pardef(f10, 1)
    Deflection = Pardef(f10, 1)
    
class B2bSteel(metaclass=CANDE_formatter):
    # use if JointSlip>0
    _prefix = prefix_spec.format('B-2b.Steel')
    Slip = Pardef(f10, 4950) # psi
    Yield = Pardef(f10, 33E3) # psi
    SlipRatio = Pardef(f10, 0.0003)
    PostSlipRatio = Pardef(f10, 0.5)
    YieldRatio = Pardef(f10, 0)
    Travel = Pardef(f10, 1) # in
    NumJoints = Pardef(d5, 1) # max 15
    # Same lengths: 0; Different: 1
    VaryTravel = Pardef(d5, 0)
    
class B2cSteel(metaclass=CANDE_formatter):
    # Level 2 or 3 only
    # use if JointSlip>0
    _prefix = prefix_spec.format('B-2c.Steel')
    Element = Pardef(d4*15, [0]*15) # up to 15 fields of d4 integers
    
class B2dSteel(metaclass=CANDE_formatter):
    # Level 2 or 3 only
    # use if JointSlip>0
    _prefix = prefix_spec.format('B-2d.Steel')
    LengthRatio = Pardef(f4*15, [0]*15) # up to 15 fields of f4 floats
    
class B3SteelADLRFD(metaclass=CANDE_formatter):
    # LRFD only
    _prefix = prefix_spec.format('B-2.Steel.AD.LRFD')
    Yieldϕ = Pardef(f10, 1)
    Bucklingϕ = Pardef(f10, 1)
    Seamϕ = Pardef(f10, 1)
    Plasticϕ = Pardef(f10, 0.9)
    Deflection = Pardef(f10, 5) # percent
    Combined = Pardef(f10, 0.9) # deep corrug only
    