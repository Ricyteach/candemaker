from .cid_parmatters import Pardef, s1, d1, d3, d4, d5, f10, CANDE_formatter

prefix_spec = '{: >22s}.L3!!'

class A2(metaclass=CANDE_formatter):
    _prefix = prefix_spec.format('A-2')
    # Options:
    # ALUMINUM, BASIC, CONCRETE, PLASTIC, STEEL, CONRIB, CONTUBE
    PipeType = Pardef('{: <10s}', 'NO_DEFAULT')
    Num = Pardef('{: >5d}', 0)

class C1(metaclass=CANDE_formatter):
    _prefix = prefix_spec.format('C-1')
    Prep = Pardef('{: <5s}', 'PREP')
    Title = Pardef('{: <67s}', '')

class C2(metaclass=CANDE_formatter):
    _prefix = prefix_spec.format('C-2')
    Steps = Pardef(d5, 1)
    # 1: control data, 2: input data, 3: created data, 4: maximum
    MeshOutput = Pardef(d5, 3)
    Check = Pardef(d5, 1) # 0: run, 1: check
    PlotControl = Pardef(d5, 3) # always 3
    # 0: minimal, 1: standard, 2: plus Duncan, 3: plus interface, 4: plus Mohr Coulomb
    ResponseOutput = Pardef(d5, 1)
    Nodes = Pardef(d5, 0)
    Elements = Pardef(d5, 0)
    Boundaries = Pardef(d5, 0)
    SoilMaterials = Pardef(d5, 0)
    InterfMaterials = Pardef(d5, 0)
    # 0: none, 1: minimize, 2: minimize and print
    Bandwidth = Pardef(d5, 1)
    
class C3(metaclass=CANDE_formatter):
    _prefix = prefix_spec.format('C-3')
    Limit = Pardef(s1, ' ')
    Num = Pardef(d4, 0)
    SpecialReferenceCode = Pardef(d3, 0)
    SpecialGenerationCode = Pardef(d1, 0)
    BasicGenerationCode = Pardef(d1, 0)
    X = Pardef(f10, 0)
    Y = Pardef(f10, 0)
    Increment = Pardef(d5, 0)
    Spacing = Pardef(f10, 0)
    Radius = Pardef(f10, 0)

class C4(metaclass=CANDE_formatter):
    _prefix = prefix_spec.format('C-4')
    Limit = Pardef(s1, ' ')
    Num = Pardef(d4, 0)
    I = Pardef(d5, 0)
    J = Pardef(d5, 0)
    K = Pardef(d5, 0)
    L = Pardef(d5, 0)
    I = Pardef(d5, 0)
    Mat = Pardef(d5, 0)
    Step = Pardef(d5, 0)
    # 1 for interface, 8 for link element fixed, 9 for link element pinned
    InterfLink = Pardef(d5, 1)
    IncrementAdded = Pardef(d5, 1)
    RowsAdded = Pardef(d5, 1)
    IncrementBetween = Pardef(d5, 0)
    Death = Pardef(d5, 100)
    
class C5(metaclass=CANDE_formatter):
    _prefix = prefix_spec.format('C-5')
    Limit = Pardef(s1, ' ')
    Node = Pardef(d4, 0)
    Xcode = Pardef(d5, 0)
    Xvalue = Pardef(f10, 0)
    Ycode = Pardef(d5, 0)
    Yvalue = Pardef(f10, 0)
    Angle = Pardef(f10, 0)
    Step = Pardef(d5, 0)
    EndNode = Pardef(d5, 0)
    Increment = Pardef(d5, 0)
    Pressure1 = Pardef(f10, 0)
    Pressure2 = Pardef(f10, 0)