from . import prefix_spec, Pardef, s10, d5, f10, CANDE_formatter

class B1Plastic(metaclass=CANDE_formatter):
    _prefix = prefix_spec.format('B-1.Plastic')
    # GENERAL, SMOOTH, PROFILE
    WallType = Pardef(s10, 'GENERAL')
    # HDPE, PVC, PP, OTHER
    PipeType = Pardef(s10, 'HDPE')
    # 1: Short term, 2: Long term
    Duration = Pardef(d5, 1)
    # Small Deformation: 0, Large Deformation: 1, Plus Buckling: 2
    Mode = Pardef(d5, 0)
    
class B2Plastic(metaclass=CANDE_formatter):
    _prefix = prefix_spec.format('B-2.Plastic')
    ShortModulus = Pardef(f10, 0) # psi
    ShortStrength = Pardef(f10, 0) # psi
    LongModulus = Pardef(f10, 0) # psi
    LongStrength = Pardef(f10, 0) # psi
    Poissons = Pardef(f10, 0.3)
    Density = Pardef(f10, 0) # pci
    
class B3PlasticAGeneral(metaclass=CANDE_formatter):
    # for ANALYS only
    # WallType = GENERAL
    _prefix = prefix_spec.format('B-3.Plastic.A.General')
    Height = Pardef(f10, 0) # in
    
class B3PlasticASmooth(metaclass=CANDE_formatter):
    # for ANALYS only
    # WallType = SMOOTH
    _prefix = prefix_spec.format('B-3.Plastic.A.Smooth')
    Height = Pardef(f10, 0) # in
    Area = Pardef(f10, 0) # in2/in
    I = Pardef(f10, 0) # in4/in
    Centroid = Pardef(f10, 0) # in
    
class B3PlasticAProfile(metaclass=CANDE_formatter):
    # for ANALYS only
    # WallType = PROFILE
    # repeatable (multiple properties in one pipe group)
    _prefix = prefix_spec.format('B-3.Plastic.A.Profile')
    Period = Pardef(f10, 0) # in
    Height = Pardef(f10, 0) # in
    WebAngle = Pardef(f10, 90) # degrees
    WebThickness = Pardef(f10, 0) # in
    WebK = Pardef(f10, 4)
    # 0 to 4
    NumHorizontal = Pardef(d5, 0)
    # 1: include, -1: ignore
    Buckling = Pardef(d5, 1)
    First = Pardef(d5, 0)
    Last = Pardef(d5, 1)
    
class B3bPlasticAProfile(metaclass=CANDE_formatter):
    # for ANALYS only
    # WallType = PROFILE
    # Required for each NumHorizontal elements
    _prefix = prefix_spec.format('B-3b.Plastic.A.Profile')
    # 1: inner valey, 2: inner liner, 3: outer crest, 4: outer link
    Identifier = Pardef(d5, 0)
    Length = Pardef(f10, 0) # in
    Thickness = Pardef(f10, 0) # in
    SupportK = Pardef(f10, 4)
    
class B3PlasticDWSD(metaclass=CANDE_formatter):
    # for DESIGN only
    # WallType = SMOOTH
    # Non LRFD only
    _prefix = prefix_spec.format('B-3.Plastic.D.WSD')
    YieldFS = Pardef(f10, 2)
    BucklingFS = Pardef(f10, 3)
    StrainFS = Pardef(f10, 2)
    Deflection = Pardef(f10, 5) # percent
    Tension = Pardef(f10, 0.05) # in/in
    
class B3PlasticDLRFD(metaclass=CANDE_formatter):
    # for DESIGN only
    # WallType = SMOOTH
    # LRFD only
    _prefix = prefix_spec.format('B-3.Plastic.D.LRFD')
    Yield = Pardef(f10, 1)
    Buckling = Pardef(f10, 1)
    Strain = Pardef(f10, 1)
    Deflection = Pardef(f10, 1)
    Tension = Pardef(f10, 1)
    
class B4Plastic(metaclass=CANDE_formatter):
    # for DESIGN only
    # WallType = SMOOTH
    # LRFD only
    _prefix = prefix_spec.format('B-4.Plastic')
    Yieldϕ = Pardef(f10, 1)
    Bucklingϕ = Pardef(f10, 1)
    Strainϕ = Pardef(f10, 1)
    Deflection = Pardef(f10, 5) # percent
    Tension = Pardef(f10, 0.05) # in/in
    