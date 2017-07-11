from .. import format_specs as fs, cid_line

'''
from ..parmatters import prefix_spec, Pardef, s10, d5, f10, CANDE_formatter

class B1Concrete(metaclass=CANDE_formatter):
    _prefix = prefix_spec.format('B-1.Concrete')
    fc = Pardef(f10, 4E6) # psi
    Modulus = Pardef(f10, 33*150**1.5*4000**0.5) # psi
    Poissons = Pardef(f10, 0.17)
    ShearFactor = Pardef(f10, 0)
    # 1: pipes/arches, 2: boxes/3 sided structures with >= 2 feet fill, 3: boxes/3 sided structures with < 2 feet fill
    ShearEquation = Pardef(d5, 1)
    
class B2Concrete(metaclass=CANDE_formatter):
    _prefix = prefix_spec.format('B-2.Concrete')
    TensionStrain = Pardef(f10, 0) # in/in
    CompressiveStrain = Pardef(f10, 0.5*4000**0.5/(33*150**1.5)) # in/in
    LimitStrain = Pardef(f10, 0.002) # in/in
    UnitWeight = Pardef(f10, 0)
    # 0: Heger-McGrath, -1: Gergely-Lutz, >0: specified crack spacing length
    CrackModel = Pardef(f10, 0) # inches if positive
    # Small Deformation: 0, Large Deformation: 1, Plus Buckling: 2
    Mode = Pardef(d5, 0)
    
class B3Concrete(metaclass=CANDE_formatter):
    _prefix = prefix_spec.format('B-3.Concrete')
    # STAND, ELLIP, ARBIT, BOXES
    Shape = Pardef(s10, 'STAND')
    Yield = Pardef(f10, 60E3) # psi
    Modulus = Pardef(f10, 29E6) # psi
    Poissons = Pardef(f10, 0.3)
    SpacingInner = Pardef(f10, 2) # in
    SpacingOuter = Pardef(f10, 2) # in
    NumInner = Pardef(d5, 1)
    NumOuter = Pardef(d5, 1)
    # 1: Smooth wire/Plain bars, 2: Welded/Deformed wire, 3: Deformed bars or with stirrups
    Type = Pardef(d5, 2)
    # 1: Cracking only, 2: Add concrete plastic behavior, 3: Add steel yielding behavior
    Behavior = Pardef(d5, 3)
    
class B4ConcreteCase1_2(metaclass=CANDE_formatter):
    # for ANALYS only
    # for Shape = ARBIT, STAND, or ELLIP only
    # repeatable (multiple properties in one pipe group) if Shape = ARBIT
    _prefix = prefix_spec.format('B-4.Concrete.Case1_2')
    Thickness = Pardef(f10, 0) # in
    Area1 = Pardef(f10, 0) # in2/in
    Area2 = Pardef(f10, 0) # in2/in
    Cover1 = Pardef(f10, 1.25) # in
    Cover2 = Pardef(f10, 1.25) # in
    First = Pardef(d5, 0)
    Last = Pardef(d5, 0)
    
class B4ConcreteCase3(metaclass=CANDE_formatter):
    # for Level 2 only
    # ANALYS only
    # Shape = BOXES only
    _prefix = prefix_spec.format('B-4.Concrete.Case3')
    Thickness = Pardef(f10, 0) # in
    Top = Pardef(f10, 0) # in
    Sides = Pardef(f10, 0) # in
    Bottom = Pardef(f10, 0) # in
    HorizontalHaunch = Pardef(f10, 0) # in
    VerticalHaunch = Pardef(f10, 0) # in
    
class B4bConcreteCase3(metaclass=CANDE_formatter):
    # for Level 2 only
    # ANALYS only
    # Shape = BOXES only
    _prefix = prefix_spec.format('B-4b.Concrete.Case3')
    AreaOuterSides = Pardef(f10, 0) # in2/in
    AreaInnerTop = Pardef(f10, 0) # in2/in
    AreaInnerBottom = Pardef(f10, 0) # in2/in
    AreaInnerSides = Pardef(f10, 0) # in2/in
    LengthRatio = Pardef(f10, 0)
    Cover = Pardef(f10, 1.25) # in
    
class B4ConcreteCase4(metaclass=CANDE_formatter):
    # DESIGN only
    # Non LRFD only
    # Shape = STAND or ELLIP
    _prefix = prefix_spec.format('B-4.Concrete.Case4')
    Thickness = Pardef(f10, 0) # in
    YieldFS = Pardef(f10, 1.5)
    CrushingFS = Pardef(f10, 2)
    ShearFS = Pardef(f10, 2)
    TensionFS = Pardef(f10, 2)
    CrackAllow = Pardef(f10, 0.01) # in
    Cover = Pardef(f10, 1.25) # in
    OuterInnerRatio = Pardef(f10, 0.75)
    
class B4ConcreteCase5(metaclass=CANDE_formatter):
    # DESIGN only
    # LRFD only
    # Shape = STAND or ELLIP
    _prefix = prefix_spec.format('B-4.Concrete.Case5')
    Thickness = Pardef(f10, 0) # in
    Yield = Pardef(f10, 1)
    Crusing = Pardef(f10, 1)
    Shear = Pardef(f10, 1)
    Tension = Pardef(f10, 1)
    CrackAllow = Pardef(f10, 1)
    Cover = Pardef(f10, 1.25) # in
    OuterInnerRatio = Pardef(f10, 0.75)
    
class B5Concrete(metaclass=CANDE_formatter):
    # LRFD only
    _prefix = prefix_spec.format('B-5.Concrete')
    Yieldϕ = Pardef(f10, 0.9)
    Crushingϕ = Pardef(f10, 0.75)
    Shearϕ = Pardef(f10, 0.9)
    Tensionϕ = Pardef(f10, 0.9)
    CrackAllow = Pardef(f10, 0.01) # in
'''