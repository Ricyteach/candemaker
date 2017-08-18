from enum import Enum, auto


class AutoName(Enum):
    '''Automatic member names set to member attribute name'''
    def _generate_next_value_(name, start, count, last_values):
        return name


class CidEnum(AutoName):
    '''Valid CID line labels.
    
    To be used as a convenient key access to CID
    related collections.'''
    # any
    A1 = auto()
    E1 = auto()
    # L3 Only
    A2 = auto()
    C1 = auto()
    C2 = auto()
    C3 = auto()
    C3L = auto()
    C4 = auto()
    C4L = auto()
    C5 = auto()
    C5L = auto()
    # soil
    D1 = auto()
    D1L = auto()
    D1Soil = auto()
    # D1SoilL = auto()
    D1Interf = auto()
    # D1InterfL = auto()
    D2Orthotropic = auto()
    D2Over = auto()
    D2Hardin = auto()
    D2HardinTRIA = auto()
    D2Composite = auto()
    D2MohrCoulomb = auto()
    D2Isotropic = auto()
    D2Duncan = auto()
    D3Duncan = auto()
    D4Duncan = auto()
    D2Interface = auto()
    # alum
    B1Alum = auto()
    B2AlumA = auto()
    B2AlumDWSD = auto()
    B2AlumDLRFD = auto()
    B3AlumADLRFD = auto()
    # plastic
    B1Plastic = auto()
    B2Plastic = auto()
    B3PlasticAGeneral = auto()
    B3PlasticASmooth = auto()
    B3PlasticDWSD = auto()
    B3PlasticDLRFD = auto()
    B3PlasticAProfile = auto()
    B3bPlasticAProfile = auto()
    B4Plastic = auto()
    # steel
    B1Steel = auto()
    B2SteelA = auto()
    B2SteelDWSD = auto()
    B2SteelDLRFD = auto()
    B2bSteel = auto()
    B2cSteel = auto()
    B2dSteel = auto()
    B3SteelADLRFD = auto()

class ObjEnum(AutoName):
    '''Names of objects that will be used to represent CID
    line information. Have created this name catalog so 
    they are easier to remember later.'''
    # any
    Master = auto()
    Factor = auto()
    
    # L3
    PipeGroup = auto()
    Info = auto()
    Control = auto()
    Node = auto()
    # NodeLast = auto()
    Element = auto()
    TriaElement = auto()
    QuadElement = auto()
    SoilElement = auto()
    BeamElement = auto()
    InterfElement = auto()
    # ElementLast = auto()
    Bound = auto()
    ForceBound = auto()
    SideBound = auto()
    BotBound = auto()
    TopBound = auto()
    CornerBound = auto()
    # BoundLast = auto()
    
    #soil
    Material = auto()
    # MaterialLast = auto()
    SoilMaterial = auto()
    InterfMaterial = auto()
    OverMaterial = auto()
    Isotropic = auto()
    Orthotropic = auto()
    Duncan2 = auto()
    Duncan3 = auto()
    Duncan4 = auto()
    Overburden = auto()
    Hardin = auto()
    HardinTRIA = auto()
    Interface = auto()
    Composite = auto()
    MohrCoulomb = auto()
    
    # alum
    Alum1 = auto()
    Alum2A = auto()
    Alum2DWSD = auto()
    Alum2DLRFD = auto()
    Alum3ADLRFD = auto()
    
    # plastic
    Plastic1 = auto()
    Plastic2 = auto()
    Plastic3AGeneral = auto()
    Plastic3ASmooth = auto()
    Plastic3AProfile = auto()
    Plastic3bAProfile = auto()
    Plastic3DWSD = auto()
    Plastic3DLRFD = auto()
    Plastic4 = auto()
    
    # steel
    Steel1 = auto()
    Steel2A = auto()
    Steel2DWSD = auto()
    Steel2DLRFD = auto()
    Steel2b = auto()
    Steel2c = auto()
    Steel2d = auto()
    Steel3ADLRFD = auto()
