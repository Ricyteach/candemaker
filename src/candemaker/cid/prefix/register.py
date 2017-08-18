from ..registry import CidRegistry
from .prefix import *
from . import L3


PrefixReg = CidRegistry(
    A1 = A1,
    E1 = E1,
    A2 = L3.A2,
    C1 = L3.C1,
    C2 = L3.C2,
    D2Isotropic = D2Isotropic,
    D2Orthotropic = D2Orthotropic,
    D2Duncan = D2Duncan,
    D3Duncan = D3Duncan,
    D4Duncan = D4Duncan,
    D2Over = D2Over,
    D2Hardin = D2Hardin,
    D2HardinTRIA = D2HardinTRIA,
    D2Interface = D2Interface,
    D2Composite = D2Composite,
    D2MohrCoulomb = D2MohrCoulomb,
    B1Alum = B1Alum,
    B2AlumA = B2AlumA,
    B2AlumDWSD = B2AlumDWSD,
    B2AlumDLRFD = B2AlumDLRFD,
    B3AlumADLRFD = B3AlumADLRFD,
    B2Plastic = B2Plastic,
    B3PlasticAGeneral = B3PlasticAGeneral,
    B3PlasticASmooth = B3PlasticASmooth,
    B3PlasticAProfile = B3PlasticAProfile,
    B3bPlasticAProfile = B3bPlasticAProfile,
    B3PlasticDWSD = B3PlasticDWSD,
    B3PlasticDLRFD = B3PlasticDLRFD,
    B4Plastic = B4Plastic,
    B1Steel = B1Steel,
    B2SteelA = B2SteelA,
    B2SteelDWSD = B2SteelDWSD,
    B2SteelDLRFD = B2SteelDLRFD,
    B2bSteel = B2bSteel,
    B2cSteel = B2cSteel,
    B2dSteel = B2dSteel,
    B3SteelADLRFD = B3SteelADLRFD,

    # CID lines with SPACE Limit value
    C3 = L3.C3,
    C4 = L3.C4,
    C5 = L3.C5,
    D1 = D1,

    # CID lines with "L" Limit value
    C3L = L3.C3,
    C4L = L3.C4,
    C5L = L3.C5,
    D1L = D1,
    )
