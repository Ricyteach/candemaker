from collections import namedtuple as nt
from mytools import getfields, InvalidField
from . import linedef as ld
from .validdict import CidRegistry, ObjRegistry
from .unformatter import UnformatterReg as CidUnformatterReg

##    Not done yet
def cidnt(name, linedefregmember, *fields, **def_values):
    '''Factory to create a special CID named tuple
    Created from a line definition sequence using its
    default values'''
    linedef = linedefregmember
    linenames = tuple(ld.names(linedef))
    linedefaults = tuple(ld.defaults(linedef))
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


CidNtReg = ObjRegistry(
    # any
    Master = cidnt('Master', ld.LineDefReg['A1']),
    Factor = cidnt('Factor', ld.LineDefReg['E1']),

    # L3
    PipeGroup = cidnt('PipeGroup', ld.LineDefReg['A2']),
    Info = cidnt('Info', ld.LineDefReg['C1'], ['Title']),
    Control = cidnt('Control', ld.LineDefReg['C2'], 'NSteps Check NNodes NElements '
                                              'NBoundaries NSoilMaterials '
                                              'NInterfMaterials Bandwidth'),
    Node = cidnt('Node', ld.LineDefReg['C3'], 'Num X Y'),
    # NodeLast = cidnt('NodeLast', ld.LineDefReg['C3'], 'Limit', Limit='L'),
    Element = cidnt('Element', ld.LineDefReg['C4'], 'Num I J K L Mat Step InterfLink'),
    TriaElement = cidnt('TriaElement', ld.LineDefReg['C4'], 'Num I J K'),
    QuadElement = cidnt('QuadElement', ld.LineDefReg['C4'], 'Num I J K L'),
    SoilElement = cidnt('SoilElement', ld.LineDefReg['C4'], 'Num I J K L'),
    BeamElement = cidnt('BeamElement', ld.LineDefReg['C4'], 'Num I J'),
    InterfElement = cidnt('InterfElement', ld.LineDefReg['C4'], 
                          'Num I J K InterfLink', InterfLink=1),
    # ElementLast = cidnt('ElementLast', ld.LineDefReg['C4'], 'Limit', Limit='L'),
    Bound = cidnt('Bound', ld.LineDefReg['C5'], 'Node Xcode Xvalue Ycode Yvalue Angle Step'),
    ForceBound = cidnt('ForceBound', ld.LineDefReg['C5'], 'Node Xvalue Yvalue'),
    SideBound = cidnt('SideBound', ld.LineDefReg['C5'], 'Node Xcode', Xcode=1),
    BotBound = cidnt('BotBound', ld.LineDefReg['C5'], 'Node Ycode', Ycode=1),
    CornerBound = cidnt('CornerBound', ld.LineDefReg['C5'], 'Node Xcode Ycode', Xcode=1, Ycode=1),
    # BoundLast = cidnt('BoundLast', ld.LineDefReg['C5'], 'Limit', Limit='L'),

    #soil
    Material = cidnt('Material', ld.LineDefReg['D1'], 'ID Model Density Name Layers'),
    # MaterialLast = cidnt('MaterialLast', ld.LineDefReg['D1'], 'Limit', Limit='L'),
    SoilMaterial = cidnt('SoilMaterial', ld.LineDefReg['D1'], 'ID Model Density Name'),
    InterfMaterial = cidnt('InterfMaterial', ld.LineDefReg['D1'], 'ID Name Model', Model=6),
    OverMaterial = cidnt('OverMaterial', ld.LineDefReg['D1'], 
                         'ID Density Name Layers Model', Layers=1, Model=4),
    Isotropic = cidnt('Isotropic', ld.LineDefReg['D2Isotropic']),
    Orthotropic = cidnt('Orthotropic', ld.LineDefReg['D2Orthotropic']),
    Duncan2 = cidnt('Duncan2', ld.LineDefReg['D2Duncan']),
    Duncan3 = cidnt('Duncan3', ld.LineDefReg['D3Duncan']),
    Duncan4 = cidnt('Duncan4', ld.LineDefReg['D4Duncan']),
    Overburden = cidnt('Overburden', ld.LineDefReg['D2Over']),
    Hardin = cidnt('Hardin', ld.LineDefReg['D2Hardin']),
    HardinTRIA = cidnt('HardinTRIA', ld.LineDefReg['D2HardinTRIA']),
    Interface = cidnt('Interface', ld.LineDefReg['D2Interface']),
    Composite = cidnt('Composite', ld.LineDefReg['D2Composite']),
    MohrCoulomb = cidnt('MohrCoulomb', ld.LineDefReg['D2MohrCoulomb']),

    # alum
    Alum1 = cidnt('Alum1', ld.LineDefReg['B1Alum']),
    Alum2A = cidnt('Alum2A', ld.LineDefReg['B2AlumA']),
    Alum2DWSD = cidnt('Alum2DWSD', ld.LineDefReg['B2AlumDWSD']),
    Alum2DLRFD = cidnt('Alum2DLRFD', ld.LineDefReg['B2AlumDLRFD']),
    Alum3ADLRFD = cidnt('Alum3ADLRFD', ld.LineDefReg['B3AlumADLRFD']),

    # steel
    Steel1 = cidnt('Steel1', ld.LineDefReg['B1Steel']),
    Steel2A = cidnt('Steel2A', ld.LineDefReg['B2SteelA']),
    Steel2DWSD = cidnt('Steel2DWSD', ld.LineDefReg['B2SteelDWSD']),
    Steel2DLRFD = cidnt('Steel2DLRFD', ld.LineDefReg['B2SteelDLRFD']),
    Steel2b = cidnt('Steel2b', ld.LineDefReg['B2bSteel']),
    Steel2c = cidnt('Steel2c', ld.LineDefReg['B2cSteel'], ' '.join('Element{}'.format(i)
                                                        for i in range(1,16))),
    Steel2d = cidnt('Steel2d', ld.LineDefReg['B2dSteel'], ' '.join('LengthRatio{}'.format(i)
                                                        for i in range(1,16))),
    Steel3ADLRFD = cidnt('Steel3ADLRFD', ld.LineDefReg['B3SteelADLRFD']),

    # plastic
    Plastic1 = cidnt('Plastic1', ld.LineDefReg['B1Plastic']),
    Plastic2 = cidnt('Plastic2', ld.LineDefReg['B2Plastic']),
    Plastic3AGeneral = cidnt('Plastic3AGeneral', ld.LineDefReg['B3PlasticAGeneral']),
    Plastic3ASmooth = cidnt('Plastic3ASmooth', ld.LineDefReg['B3PlasticASmooth']),
    Plastic3AProfile = cidnt('Plastic3AProfile', ld.LineDefReg['B3PlasticAProfile']),
    Plastic3bAProfile = cidnt('Plastic3bAProfile', ld.LineDefReg['B3bPlasticAProfile']),
    Plastic3DWSD = cidnt('Plastic3DWSD', ld.LineDefReg['B3PlasticDWSD']),
    Plastic3DLRFD = cidnt('Plastic3DLRFD', ld.LineDefReg['B3PlasticDLRFD']),
    Plastic4 = cidnt('Plastic4', ld.LineDefReg['B4Plastic']),
    )

CidTagReg = CidRegistry(
    # any
    A1 = CidNtReg['Master'],
    E1 = CidNtReg['Factor'],

    # L3
    A2 = CidNtReg['PipeGroup'],
    C1 = CidNtReg['Info'],
    C2 = CidNtReg['Control'],
    C3 = CidNtReg['Node'],
    # C3L = CidNtReg['NodeLast'],
    C4 = CidNtReg['Element'],
    # C4 = CidNtReg['TriaElement'],
    # C4 = CidNtReg['QuadElement'],
    # C4 = CidNtReg['SoilElement'],
    # C4 = CidNtReg['BeamElement'],
    # C4 = CidNtReg['InterfElement'],
    # C4L = CidNtReg['ElementLast'],
    C5 = CidNtReg['Bound'],
    # C5 = CidNtReg['ForceBound'],
    # C5 = CidNtReg['SideBound'],
    # C5 = CidNtReg['BotBound'],
    # C5 = CidNtReg['CornerBound'],
    # C5L = CidNtReg['BoundLast'],

    #soil
    D1 = CidNtReg['Material'],
    # D1L = CidNtReg['MaterialLast'],
    # D1Soil = CidNtReg['SoilMaterial'],
    # D1Interf = CidNtReg['InterfMaterial'],
    # D1 = CidNtReg['OverMaterial'],
    D2Isotropic = CidNtReg['Isotropic'],
    D2Orthotropic = CidNtReg['Orthotropic'],
    D2Duncan = CidNtReg['Duncan2'],
    D3Duncan = CidNtReg['Duncan3'],
    D4Duncan = CidNtReg['Duncan4'],
    D2Over = CidNtReg['Overburden'],
    D2Hardin = CidNtReg['Hardin'],
    D2HardinTRIA = CidNtReg['HardinTRIA'],
    D2Interface = CidNtReg['Interface'],
    D2Composite = CidNtReg['Composite'],
    D2MohrCoulomb = CidNtReg['MohrCoulomb'],

    # alum
    B1Alum = CidNtReg['Alum1'],
    B2AlumA = CidNtReg['Alum2A'],
    B2AlumDWSD = CidNtReg['Alum2DWSD'],
    B2AlumDLRFD = CidNtReg['Alum2DLRFD'],
    B3AlumADLRFD = CidNtReg['Alum3ADLRFD'],

    # steel
    B1Steel = CidNtReg['Steel1'],
    B2SteelA = CidNtReg['Steel2A'],
    B2SteelDWSD = CidNtReg['Steel2DWSD'],
    B2SteelDLRFD = CidNtReg['Steel2DLRFD'],
    B2bSteel = CidNtReg['Steel2b'],
    B2cSteel = CidNtReg['Steel2c'],
    B2dSteel = CidNtReg['Steel2d'],
    B3SteelADLRFD = CidNtReg['Steel3ADLRFD'],

    # plastic
    B1Plastic = CidNtReg['Plastic1'],
    B2Plastic = CidNtReg['Plastic2'],
    B3PlasticAGeneral = CidNtReg['Plastic3AGeneral'],
    B3PlasticASmooth = CidNtReg['Plastic3ASmooth'],
    B3PlasticAProfile = CidNtReg['Plastic3AProfile'],
    B3bPlasticAProfile = CidNtReg['Plastic3bAProfile'],
    B3PlasticDWSD = CidNtReg['Plastic3DWSD'],
    B3PlasticDLRFD = CidNtReg['Plastic3DLRFD'],
    B4Plastic = CidNtReg['Plastic4'],
    )


CidNameReg = ObjRegistry(
    # any
    Master = 'A1',
    Factor = 'E1',

    # L3
    PipeGroup = 'A2',
    Info = 'C1',
    Control = 'C2',
    Node = 'C3',
    # NodeLast = 'C3L',
    Element = 'C4',
    TriaElement = 'C4',
    QuadElement = 'C4',
    SoilElement = 'C4',
    BeamElement = 'C4',
    InterfElement = 'C4',
    # ElementLast = 'C4L',
    Bound = 'C5',
    ForceBound = 'C5',
    SideBound = 'C5',
    BotBound = 'C5',
    CornerBound = 'C5',
    # BoundLast = 'C5L',

    #soil
    Material = 'D1',
    # MaterialLast = 'D1L',
    SoilMaterial = 'D1',
    InterfMaterial = 'D1',
    OverMaterial = 'D1',
    Isotropic = 'D2Isotropic',
    Orthotropic = 'D2Orthotropic',
    Duncan2 = 'D2Duncan',
    Duncan3 = 'D3Duncan',
    Duncan4 = 'D4Duncan',
    Overburden = 'D2Over',
    Hardin = 'D2Hardin',
    HardinTRIA = 'D2HardinTRIA',
    Interface = 'D2Interface',
    Composite = 'D2Composite',
    MohrCoulomb = 'D2MohrCoulomb',

    # alum
    Alum1 = 'B1Alum',
    Alum2A = 'B2AlumA',
    Alum2DWSD = 'B2AlumDWSD',
    Alum2DLRFD = 'B2AlumDLRFD',
    Alum3ADLRFD = 'B3AlumADLRFD',

    # steel
    Steel1 = 'B1Steel',
    Steel2A = 'B2SteelA',
    Steel2DWSD = 'B2SteelDWSD',
    Steel2DLRFD = 'B2SteelDLRFD',
    Steel2b = 'B2bSteel',
    Steel2c = 'B2cSteel',
    Steel2d = 'B2dSteel',
    Steel3ADLRFD = 'B3SteelADLRFD',

    # plastic
    Plastic1 = 'B1Plastic',
    Plastic2 = 'B2Plastic',
    Plastic3AGeneral = 'B3PlasticAGeneral',
    Plastic3ASmooth = 'B3PlasticASmooth',
    Plastic3AProfile = 'B3PlasticAProfile',
    Plastic3bAProfile = 'B3bPlasticAProfile',
    Plastic3DWSD = 'B3PlasticDWSD',
    Plastic3DLRFD = 'B3PlasticDLRFD',
    Plastic4 = 'B4Plastic',
    )
