from enum import Enum, auto
from parmatter import FormatGroupMeta, FloatIntParmatter, BlankParmatter, PositionalDefaultParmatter, AttrParmatter
from mytools import update_special
from .linedefreg import LineDefReg
from .prefix import PrefixReg
from .enum import CidRegistry


class CandeParmatter(BlankParmatter, FloatIntParmatter, PositionalDefaultParmatter, AttrParmatter):
    pass


class CandeFieldGroup(FormatGroupMeta):
    _formatter_type = CandeParmatter
    _sep = ''


class CandeFieldGroupEnum(Enum):
    '''Creates CandeFieldGroup classes for members of LineDefReg.'''
    def _generate_next_value_(name, start, count, last_values):
        tag, linedef = name, LineDefReg[name].value
        namespace = {f.name: (f.spec, f.default) for f in linedef}
        update_special(namespace, _prefix=PrefixReg[tag].value)
        return CandeFieldGroup(tag, (), namespace)


class UnformatterReg(CandeFieldGroupEnum, CidRegistry):
    A1 = auto()
    E1 = auto()
    A2 = auto()
    C1 = auto()
    C2 = auto()
    C3 = auto()
    # C3L = auto()
    C4 = auto()
    # C4L = auto()
    C5 = auto()
    # C5L = auto()
    D1 = auto()
    # D1L = auto()
    D2Isotropic = auto()
    D2Orthotropic = auto()
    D2Duncan = auto()
    D3Duncan = auto()
    D4Duncan = auto()
    D2Over = auto()
    D2Hardin = auto()
    D2HardinTRIA = auto()
    D2Interface = auto()
    D2Composite = auto()
    D2MohrCoulomb = auto()
    B1Alum = auto()
    B2AlumA = auto()
    B2AlumDWSD = auto()
    B2AlumDLRFD = auto()
    B3AlumADLRFD = auto()
    B2Plastic = auto()
    B3PlasticAGeneral = auto()
    B3PlasticASmooth = auto()
    B3PlasticAProfile = auto()
    B3bPlasticAProfile = auto()
    B3PlasticDWSD = auto()
    B3PlasticDLRFD = auto()
    B4Plastic = auto()
    B1Steel = auto()
    B2SteelA = auto()
    B2SteelDWSD = auto()
    B2SteelDLRFD = auto()
    B2bSteel = auto()
    B2cSteel = auto()
    B2dSteel = auto()
    B3SteelADLRFD = auto()
