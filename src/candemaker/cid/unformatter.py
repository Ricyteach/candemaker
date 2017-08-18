from parmatter import FormatGroupMeta, FloatIntParmatter, BlankParmatter, PositionalDefaultParmatter, AttrParmatter
from mytools import update_special
from .linedef import LineDefReg
from .prefix import PrefixReg
from .validdict import CidRegistry


class CandeParmatter(BlankParmatter, FloatIntParmatter, PositionalDefaultParmatter, AttrParmatter):
    pass


class CandeFieldGroup(FormatGroupMeta):
    _formatter_type = CandeParmatter
    _sep = ''


def MakeCandeFieldGroup(name):
    '''Creates CandeFieldGroup classes for members of LineDefReg.'''
    tag, linedef = name, LineDefReg[name]
    namespace = {f.name: (f.spec, f.default) for f in linedef}
    update_special(namespace, _prefix=PrefixReg[tag])
    return CandeFieldGroup(tag, (), namespace)


UnformatterReg = CidRegistry(
    {k:MakeCandeFieldGroup(k) for k in (
    'A1',
    'E1',
    'A2',
    'C1',
    'C2',
    'C3',
    # 'C3L',
    'C4',
    # 'C4L',
    'C5',
    # 'C5L',
    'D1',
    # 'D1L',
    'D2Isotropic',
    'D2Orthotropic',
    'D2Duncan',
    'D3Duncan',
    'D4Duncan',
    'D2Over',
    'D2Hardin',
    'D2HardinTRIA',
    'D2Interface',
    'D2Composite',
    'D2MohrCoulomb',
    'B1Alum',
    'B2AlumA',
    'B2AlumDWSD',
    'B2AlumDLRFD',
    'B3AlumADLRFD',
    'B2Plastic',
    'B3PlasticAGeneral',
    'B3PlasticASmooth',
    'B3PlasticAProfile',
    'B3bPlasticAProfile',
    'B3PlasticDWSD',
    'B3PlasticDLRFD',
    'B4Plastic',
    'B1Steel',
    'B2SteelA',
    'B2SteelDWSD',
    'B2SteelDLRFD',
    'B2bSteel',
    'B2cSteel',
    'B2dSteel',
    'B3SteelADLRFD',
    )}
    )
