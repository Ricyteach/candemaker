from enum import Enum, auto


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class CidEnum(AutoName):
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
    D1Soil = auto()
    D1SoilL = auto()
    D1Interf = auto()
    D1InterfL = auto()
    D2Orthotropic = auto()
    D2Overburden = auto()
    D2Hardin = auto()
    D2HardinTRIA = auto()
    D2Composite = auto()
    D2MohrCoulomb = auto()
    D2Isotropic = auto()
    D2Duncan = auto()
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
    