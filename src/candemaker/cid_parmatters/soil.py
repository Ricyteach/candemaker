from .cid_parmatters import prefix_spec, Pardef, d2, d4, s20, s1, d5, f10, CANDE_formatter

class D1(metaclass=CANDE_formatter):
    _prefix = prefix_spec.format('D-1')
    Limit = Pardef(s1, ' ')
    ID = Pardef(d4, 0)
    # 1: isotropic, 2: orthotropic, 3: Duncan/Selig, 4: Overburden Dependent,
    # 5: Extended Hardin, 6: Interface, 7: Composite Link, 8: Mohr/Coulomb
    Model = Pardef(d5, 1)
    Density = Pardef(f10, 0)
    Name = Pardef(s20, '')
    Layers = Pardef(d2, 0) # overburden model only
    
class D2Isotropic(metaclass=CANDE_formatter):
    # only for Model = 1
    _prefix = prefix_spec.format('D-2.Isotropic')
    Modulus = Pardef(f10, 0) # psi
    Poissons = Pardef(f10, 0)
    
class D2Orthotropic(metaclass=CANDE_formatter):
    # only for Model = 2
    _prefix = prefix_spec.format('D-2.Orthotropic')
    ModulusX = Pardef(f10, 0) # psi
    ModulusZ = Pardef(f10, 0) # psi
    ModulusY = Pardef(f10, 0) # psi
    ModulusG = Pardef(f10, 0) # psi
    Angle = Pardef(f10, 0) # degrees
    
class D2Duncan(metaclass=CANDE_formatter):
    # only for Model = 3
    _prefix = prefix_spec.format('D-2.Duncan')
    LRFDControl = Pardef(d5, 0) 
    # 1.0 for in-situ materials
    ModuliAveraging = Pardef(f10, 0.5)
    # Duncan: 0, Dancan/Selig: 1
    Model = Pardef(d5, 1) 
    # Original: 0, Unloading: 1
    Unloading = Pardef(d5, 1)
    
class D3Duncan(metaclass=CANDE_formatter):
    # only for Model = 3
    _prefix = prefix_spec.format('D-3.Duncan')
    Cohesion = Pardef(f10, 0) # psi
    Phi_i = Pardef(f10, 0) # degrees
    Delta_Phi = Pardef(f10, 0) # degrees
    Modulus_i = Pardef(f10, 0)
    Modulus_n = Pardef(f10, 0)
    Ratio = Pardef(f10, 0)
    
class D4Duncan(metaclass=CANDE_formatter):
    # only for Model = 3
    _prefix = prefix_spec.format('D-4.Duncan')
    Bulk_i = Pardef(f10, 0)
    Bulk_m = Pardef(f10, 0)
    Poissons = Pardef(f10, 0)
    
class D2Over(metaclass=CANDE_formatter):
    # only for Model = 4
    # repeatable
    _prefix = prefix_spec.format('D-2.Over')
    Limit = Pardef(s1, ' ')
    Pressure = Pardef('{: >9f}', 0)
    Modulus = Pardef(f10, 0) # psi
    # granular: 0.3-0.35, mixed: 0.3-0.4, cohesive: 0.33-0.4
    Poissons = Pardef(f10, 0)
    # End to indicate last entry of table
    End = Pardef('{: <3s}', '   ')
    
class D2Hardin(metaclass=CANDE_formatter):
    # only for Model = 5
    _prefix = prefix_spec.format('D-2.Hardin')
    PoissonsLow = Pardef(f10, 0.01)
    PoissonsHigh = Pardef(f10, 0.49)
    Shape = Pardef(f10, 0.26)
    # GRAN: 0.60, MIXE: 0.5, COHE: 1.0
    VoidRatio = Pardef(f10, 0.6)
    # GRAN: 0, MIXE: 0.5, COHE: 0.9
    Saturation = Pardef(f10, 0)
    # GRAN: 0, MIXE: 0.05, COHE: 0.20
    PI = Pardef(f10, 0)
    Nonlinear = Pardef(d5, 0) # ignored
    
class D2HardinTRIA(metaclass=CANDE_formatter):
    # only for Model = 5
    _prefix = prefix_spec.format('D-2.Hardin.TRIA')
    PoissonsLow = Pardef(f10, 0.01)
    PoissonsHigh = Pardef(f10, 0.49)
    Shape = Pardef(f10, 0.26)
    S1 = Pardef(f10, 0)
    C1 = Pardef(f10, 0)
    A = Pardef(f10, 0)
    Nonlinear = Pardef(d5, 0) # ignored
    
class D2Interface(metaclass=CANDE_formatter):
    # only for Model = 6
    _prefix = prefix_spec.format('D-2.Interface')
    Angle = Pardef(f10, 0) # degrees
    Friction = Pardef(f10, 0)
    Tensile = Pardef(f10, 1) # lbs/in
    Gap = Pardef(f10, 0) # in
    
class D2Composite(metaclass=CANDE_formatter):
    # only for Model = 7
    _prefix = prefix_spec.format('D-2.Composite')
    Group1 = Pardef(d5, 0)
    Group2 = Pardef(d5, 0)
    Fraction = Pardef(f10, 0)
    
class D2MohrCoulomb(metaclass=CANDE_formatter):
    # only for Model = 8
    _prefix = prefix_spec.format('D-2.MohrCoulomb')
    Modulus = Pardef(f10, 0) # psi
    Poissons = Pardef(f10, 0)
    Cohesion = Pardef(f10, 0) # psi
    Phi = Pardef(f10, 0) # degrees