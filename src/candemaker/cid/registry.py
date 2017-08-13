from collections import namedtuple as nt
from mytools import getfields, InvalidField
from .enum import CidRegistry, ObjRegistry
from .linedefreg import LineDefReg
from .unformatter import UnformatterReg as CidUnformatterReg

def defaults(linedef):
    '''Generate the defaults from a line definition sequence'''
    try:
        yield from (field.default for field in linedef)
    except AttributeError as e:
        raise TypeError('The lindef argument did not contain '
                        'valid fields') from e

def names(linedef):
    '''Generate the names from a line definition sequence'''
    try:
        yield from (field.name for field in linedef)
    except AttributeError as e:
        raise TypeError('The lindef argument did not contain '
                        'valid fields') from e

##    Not done yet
def cidnt(name, linedefregmember, *fields, **def_values):
    '''Factory to create a special CID named tuple
    Created from a line definition sequence using its
    default values'''
    linedef = linedefregmember.value
    linenames = tuple(names(linedef))
    linedefaults = tuple(defaults(linedef))
    invalid_defaults = [k for k in def_values.keys()
                          if k not in linenames]
    if invalid_defaults:
        raise ValueError('One or more supplied default value names '
                         'do not appear in the linedef:\n'
                         '{!r}'.format(invalid_defaults))
    defaults_dict = {n: def_values.get(n, d)
                    for n, d in zip(linenames, linedefaults)}
    if fields:
        validator = lambda f: f in linenames
        try:
            fieldseq = tuple(getfields(*fields, validator=validator))
        except InvalidField as e:
            raise ValueError('One or more field names does not appear '
                             'in the linedef:\n{!r}'
                             ''.format(linedef)) from e
    else:
        fieldseq = linenames

    NT = nt(name, fieldseq)
    new_defaults = (defaults_dict[fieldname] for fieldname in fieldseq)
    NT.__new__.__defaults__ = tuple(new_defaults)
    return NT


class CidNtReg(ObjRegistry):
    # any
    Master = cidnt('Master', LineDefReg.A1)
    Factor = cidnt('Factor', LineDefReg.E1)

    # L3
    PipeGroup = cidnt('PipeGroup', LineDefReg.A2)
    Info = cidnt('Info', LineDefReg.C1, ['Title'])
    Control = cidnt('Control', LineDefReg.C2, 'NSteps Check NNodes NElements '
                                              'NBoundaries NSoilMaterials '
                                              'NInterfMaterials Bandwidth')
    Node = cidnt('Node', LineDefReg.C3, 'Num X Y')
    # NodeLast = cidnt('NodeLast', LineDefReg.C3, 'Limit', Limit='L')
    Element = cidnt('Element', LineDefReg.C4, 'Num I J K L Mat Step InterfLink')
    TriaElement = cidnt('TriaElement', LineDefReg.C4, 'Num I J K')
    QuadElement = cidnt('QuadElement', LineDefReg.C4, 'Num I J K L')
    SoilElement = cidnt('SoilElement', LineDefReg.C4, 'Num I J K L')
    BeamElement = cidnt('BeamElement', LineDefReg.C4, 'Num I J')
    InterfElement = cidnt('InterfElement', LineDefReg.C4, 
                          'Num I J K InterfLink', InterfLink=1)
    # ElementLast = cidnt('ElementLast', LineDefReg.C4, 'Limit', Limit='L')
    Bound = cidnt('Bound', LineDefReg.C5, 'Node Xcode Xvalue Ycode Yvalue Angle Step')
    ForceBound = cidnt('ForceBound', LineDefReg.C5, 'Node Xvalue Yvalue')
    SideBound = cidnt('SideBound', LineDefReg.C5, 'Node Xcode', Xcode=1)
    BotBound = cidnt('BotBound', LineDefReg.C5, 'Node Ycode', Ycode=1)
    CornerBound = cidnt('CornerBound', LineDefReg.C5, 'Node Xcode Ycode', Xcode=1, Ycode=1)
    # BoundLast = cidnt('BoundLast', LineDefReg.C5, 'Limit', Limit='L')

    #soil
    Material = cidnt('Material', LineDefReg.D1, 'ID Model Density Name Layers')
    # MaterialLast = cidnt('MaterialLast', LineDefReg.D1, 'Limit', Limit='L')
    SoilMaterial = cidnt('SoilMaterial', LineDefReg.D1, 'ID Model Density Name')
    InterfMaterial = cidnt('InterfMaterial', LineDefReg.D1, 'ID Name Model', Model=6)
    OverMaterial = cidnt('OverMaterial', LineDefReg.D1, 
                         'ID Density Name Layers Model', Layers=1, Model=4)
    Isotropic = cidnt('Isotropic', LineDefReg.D2Isotropic)
    Orthotropic = cidnt('Orthotropic', LineDefReg.D2Orthotropic)
    Duncan2 = cidnt('Duncan2', LineDefReg.D2Duncan)
    Duncan3 = cidnt('Duncan3', LineDefReg.D3Duncan)
    Duncan4 = cidnt('Duncan4', LineDefReg.D4Duncan)
    Overburden = cidnt('Overburden', LineDefReg.D2Over)
    Hardin = cidnt('Hardin', LineDefReg.D2Hardin)
    HardinTRIA = cidnt('HardinTRIA', LineDefReg.D2HardinTRIA)
    Interface = cidnt('Interface', LineDefReg.D2Interface)
    Composite = cidnt('Composite', LineDefReg.D2Composite)
    MohrCoulomb = cidnt('MohrCoulomb', LineDefReg.D2MohrCoulomb)

    # alum
    Alum1 = cidnt('Alum1', LineDefReg.B1Alum)
    Alum2A = cidnt('Alum2A', LineDefReg.B2AlumA)
    Alum2DWSD = cidnt('Alum2DWSD', LineDefReg.B2AlumDWSD)
    Alum2DLRFD = cidnt('Alum2DLRFD', LineDefReg.B2AlumDLRFD)
    Alum3ADLRFD = cidnt('Alum3ADLRFD', LineDefReg.B3AlumADLRFD)

    # steel
    Steel1 = cidnt('Steel1', LineDefReg.B1Steel)
    Steel2A = cidnt('Steel2A', LineDefReg.B2SteelA)
    Steel2DWSD = cidnt('Steel2DWSD', LineDefReg.B2SteelDWSD)
    Steel2DLRFD = cidnt('Steel2DLRFD', LineDefReg.B2SteelDLRFD)
    Steel2b = cidnt('Steel2b', LineDefReg.B2bSteel)
    Steel2c = cidnt('Steel2c', LineDefReg.B2cSteel, ' '.join('Element{}'.format(i)
                                                        for i in range(1,16)))
    Steel2d = cidnt('Steel2d', LineDefReg.B2dSteel, ' '.join('LengthRatio{}'.format(i)
                                                        for i in range(1,16)))
    Steel3ADLRFD = cidnt('Steel3ADLRFD', LineDefReg.B3SteelADLRFD)

    # plastic
    Plastic1 = cidnt('Plastic1', LineDefReg.B1Plastic)
    Plastic2 = cidnt('Plastic2', LineDefReg.B2Plastic)
    Plastic3AGeneral = cidnt('Plastic3AGeneral', LineDefReg.B3PlasticAGeneral)
    Plastic3ASmooth = cidnt('Plastic3ASmooth', LineDefReg.B3PlasticASmooth)
    Plastic3AProfile = cidnt('Plastic3AProfile', LineDefReg.B3PlasticAProfile)
    Plastic3bAProfile = cidnt('Plastic3bAProfile', LineDefReg.B3bPlasticAProfile)
    Plastic3DWSD = cidnt('Plastic3DWSD', LineDefReg.B3PlasticDWSD)
    Plastic3DLRFD = cidnt('Plastic3DLRFD', LineDefReg.B3PlasticDLRFD)
    Plastic4 = cidnt('Plastic4', LineDefReg.B4Plastic)

class CidTagReg(CidRegistry):
    # any
    A1 = CidNtReg.Master.value
    E1 = CidNtReg.Factor.value

    # L3
    A2 = CidNtReg.PipeGroup.value
    C1 = CidNtReg.Info.value
    C2 = CidNtReg.Control.value
    C3 = CidNtReg.Node.value
    # C3L = CidNtReg.NodeLast
    C4 = CidNtReg.Element.value
    # C4 = CidNtReg.TriaElement
    # C4 = CidNtReg.QuadElement
    # C4 = CidNtReg.SoilElement
    # C4 = CidNtReg.BeamElement
    # C4 = CidNtReg.InterfElement
    # C4L = CidNtReg.ElementLast
    C5 = CidNtReg.Bound.value
    # C5 = CidNtReg.ForceBound
    # C5 = CidNtReg.SideBound
    # C5 = CidNtReg.BotBound
    # C5 = CidNtReg.CornerBound
    # C5L = CidNtReg.BoundLast

    #soil
    D1 = CidNtReg.Material.value
    # D1L = CidNtReg.MaterialLast.value
    # D1Soil = CidNtReg.SoilMaterial
    # D1Interf = CidNtReg.InterfMaterial
    # D1 = CidNtReg.OverMaterial
    D2Isotropic = CidNtReg.Isotropic.value
    D2Orthotropic = CidNtReg.Orthotropic.value
    D2Duncan = CidNtReg.Duncan2.value
    D3Duncan = CidNtReg.Duncan3.value
    D4Duncan = CidNtReg.Duncan4.value
    D2Over = CidNtReg.Overburden.value
    D2Hardin = CidNtReg.Hardin.value
    D2HardinTRIA = CidNtReg.HardinTRIA.value
    D2Interface = CidNtReg.Interface.value
    D2Composite = CidNtReg.Composite.value
    D2MohrCoulomb = CidNtReg.MohrCoulomb.value

    # alum
    B1Alum = CidNtReg.Alum1.value
    B2AlumA = CidNtReg.Alum2A.value
    B2AlumDWSD = CidNtReg.Alum2DWSD.value
    B2AlumDLRFD = CidNtReg.Alum2DLRFD.value
    B3AlumADLRFD = CidNtReg.Alum3ADLRFD.value

    # steel
    B1Steel = CidNtReg.Steel1.value
    B2SteelA = CidNtReg.Steel2A.value
    B2SteelDWSD = CidNtReg.Steel2DWSD.value
    B2SteelDLRFD = CidNtReg.Steel2DLRFD.value
    B2bSteel = CidNtReg.Steel2b.value
    B2cSteel = CidNtReg.Steel2c.value
    B2dSteel = CidNtReg.Steel2d.value
    B3SteelADLRFD = CidNtReg.Steel3ADLRFD.value

    # plastic
    B1Plastic = CidNtReg.Plastic1.value
    B2Plastic = CidNtReg.Plastic2.value
    B3PlasticAGeneral = CidNtReg.Plastic3AGeneral.value
    B3PlasticASmooth = CidNtReg.Plastic3ASmooth.value
    B3PlasticAProfile = CidNtReg.Plastic3AProfile.value
    B3bPlasticAProfile = CidNtReg.Plastic3bAProfile.value
    B3PlasticDWSD = CidNtReg.Plastic3DWSD.value
    B3PlasticDLRFD = CidNtReg.Plastic3DLRFD.value
    B4Plastic = CidNtReg.Plastic4.value


class CidNameReg(ObjRegistry):
    # any
    Master = 'A1'
    Factor = 'E1'

    # L3
    PipeGroup = 'A2'
    Info = 'C1'
    Control = 'C2'
    Node = 'C3'
    # NodeLast = 'C3L'
    Element = 'C4'
    TriaElement = 'C4'
    QuadElement = 'C4'
    SoilElement = 'C4'
    BeamElement = 'C4'
    InterfElement = 'C4'
    # ElementLast = 'C4L'
    Bound = 'C5'
    ForceBound = 'C5'
    SideBound = 'C5'
    BotBound = 'C5'
    CornerBound = 'C5'
    # BoundLast = 'C5L'

    #soil
    Material = 'D1'
    # MaterialLast = 'D1L'
    SoilMaterial = 'D1'
    InterfMaterial = 'D1'
    OverMaterial = 'D1'
    Isotropic = 'D2Isotropic'
    Orthotropic = 'D2Orthotropic'
    Duncan2 = 'D2Duncan'
    Duncan3 = 'D3Duncan'
    Duncan4 = 'D4Duncan'
    Overburden = 'D2Over'
    Hardin = 'D2Hardin'
    HardinTRIA = 'D2HardinTRIA'
    Interface = 'D2Interface'
    Composite = 'D2Composite'
    MohrCoulomb = 'D2MohrCoulomb'

    # alum
    Alum1 = 'B1Alum'
    Alum2A = 'B2AlumA'
    Alum2DWSD = 'B2AlumDWSD'
    Alum2DLRFD = 'B2AlumDLRFD'
    Alum3ADLRFD = 'B3AlumADLRFD'

    # steel
    Steel1 = 'B1Steel'
    Steel2A = 'B2SteelA'
    Steel2DWSD = 'B2SteelDWSD'
    Steel2DLRFD = 'B2SteelDLRFD'
    Steel2b = 'B2bSteel'
    Steel2c = 'B2cSteel'
    Steel2d = 'B2dSteel'
    Steel3ADLRFD = 'B3SteelADLRFD'

    # plastic
    Plastic1 = 'B1Plastic'
    Plastic2 = 'B2Plastic'
    Plastic3AGeneral = 'B3PlasticAGeneral'
    Plastic3ASmooth = 'B3PlasticASmooth'
    Plastic3AProfile = 'B3PlasticAProfile'
    Plastic3bAProfile = 'B3bPlasticAProfile'
    Plastic3DWSD = 'B3PlasticDWSD'
    Plastic3DLRFD = 'B3PlasticDLRFD'
    Plastic4 = 'B4Plastic'
